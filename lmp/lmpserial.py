#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Copyright (c) 2016-2019 - Linkio SAS. All Rights Reserved.

    All information contained herein is, and remains the property of
    Linkio SAS.
    The intellectual and technical concepts contained herein are
    proprietary to Linkio SAS.
    Dissemination of this information or reproduction of this material
    is strictly forbidden unless prior written permission is obtained
    from Linkio SAS.

"""

__author__      = "Bruno DEGUET"
__email__       = "bruno@linkio.net"
__copyright__   = "Copyright 2018, Linkio SAS"
__version__     = "1.1.0"
__status__      = "Development"


import serial
import time
import binascii
import threading
import colorsys
import traceback
from struct import *

from .errors import *
from .utils import *
from .lmptypes import *
from .opcodes import *
from .devices import *

SERIAL_SOF = 0xFE

BAUDRATE = 57600
#BAUDRATE = 115200
#BAUDRATE = 19200

myserial = None

global_debug = False
def mylog(string):
    if global_debug :
        date = timestamp_str(None)
        print("%s %s"%(date,string))


av_rssi = []
av_mean_size = 20

# def average_rssi(rssi):
#     import numpy
#     global av_rssi
#     av_rssi.append(rssi)
#     if (len(av_rssi)>=av_mean_size):
#         av_rssi = av_rssi[1:av_mean_size]
#     res = sum(av_rssi) / float(len(av_rssi))
#     return numpy.mean(av_rssi), numpy.std(av_rssi)

class ItQueue():
    def __init__(self,opcode,payload,serial_ack_cb,ui_ack_cb):
        self.opcode = opcode
        self.payload = payload
        self.serial_ack_cb = serial_ack_cb
        self.ui_ack_cb = ui_ack_cb
        self.state = 'to_send'

class Module():
    def __init__(self,mac_addr):
        self.uid = mac_addr
        self.lmp_addr = 0
        self.name = None
        #self.reference = None
        self.manufacturer_id = None
        self.model_id = None
        self.module_type = None
        self.custom_id = None
        self.manufacturer = None
        self.model = None
        self.hw_version = None
        self.sw_version = None
        self.type_id = None
        self.configuration = None
        self.factory_config = None
        self.power_source = None
        self.battery_level = 0
        self.rssi = 0
        self.interval = None
        self.status = None
        self.timestamp = None
        self.heartbeat_timestamp = None
        self.registered = 0
        self.encryption = 0
        self.crypt_nonce = []
        self.crypt_key0 = []
        self.crypt_key1 = []
        self.role = 0
        self.devices_info_available = False
        self.devices = []
        self.storage_format = ""
        self.storage_params = []
        self.gtw_list = []

    def type_str(self):
        return lmp_devices_str_dict.get(int(self.type_id),'unknown')

    def role_str(self):
        return lmp_roles_str_dict.get(int(self.role),'')

    def battery_str(self):
        if self.battery_level<=100 :
            return "%d %%"%(self.battery_level)
        if self.battery_level == 255:
            return "powered"
        return "---"

    def device_create_or_get(self, device_id):
        for device in self.devices:
            if device.id == device_id:
                mylog("found device %d"%(device_id))
                return device
        # no device, create it
        device = Device(self,device_id)
        self.devices.append(device)
        mylog("new device %d"%(device_id))
        return device

    def device_get(self, device_id):
        for device in self.devices:
            if device.id == device_id:
                mylog("found device %d"%(device_id))
                return device
        return None

class Device():
    def __init__(self,module,device_id):
        self.id = device_id
        self.name = None
        self.type_id = 0
        self.status = None
        self.timestamp = None
        self.data = None
        self.module = module
    def type_str(self):
        return lmp_devices_str_dict.get(int(self.type_id),'unknown')

class Response():
    def __init__(self,status):
        self.status = status
        self.payload = None
        self.payload_len = 0

class LmpSerial(threading.Thread):
    """
        Ask the thread to stop by calling its join() method.
    """
    def __init__(self,portTarget):
        super(LmpSerial, self).__init__()
        self.stoprequest = threading.Event()
        self.stateParse = 0
        self.countParse = 0
        self.messageParse = []
        self.lengthParse = 0
        self.cmd_queue = []
        self.debug = False
        self.peripheral_connected_cb = None
        self.peripheral_disconnected_cb = None
        self.central_connected = False
        self.central_connected_cb = None
        self.central_disconnected_cb = None
        self.on_local_module_update_cb = None
        self.on_module_update_cb = None
        self.on_beacon_update_cb = None
        self.on_host_msg_cb = None
        self.on_device_data_status_cb = None
        self.on_local_debug_cb = None
        self.on_device_data_event_cb = None
        self.modules = []
        self.local_module_addr = None
        self.ack_done = False
        self.response = None
        self.port = serial.Serial(portTarget, baudrate=BAUDRATE, timeout=0.2)
        mylog("init serial port on %s"%(portTarget))

    def join(self, timeout=None):
        self.stoprequest.set()
        super(LmpSerial, self).join(timeout)
        print("this thread is finished")

    def run(self):
        """ Read serial port and call data parser.
        """
        while not self.stoprequest.isSet():
            if self.port :
                rcv = self.port.read(256)
            else :
                rcv = ""
            #begin parse:
            i = 0
            #print("DEBUG: len rcv=" + "%d"%len(rcv))
            if len(rcv)>1:
                while i < len(rcv):
                    self.parse_buffer(rcv[i])
                    i += 1

    def parse_buffer(self,buffer_cara):
        if self.stateParse == 0:
            #print("DEBUG: message start x%02x\n"%(buffer_cara))
            #if buffer_cara == "\xfe":
            if buffer_cara == 0xfe:
                self.stateParse = 1
                return
        elif self.stateParse == 1:
            #length = unpack('<B', buffer_cara)
            self.lengthParse = buffer_cara + 2
            #print("DEBUG: len=" + "%d\n"%self.lengthParse)
            self.messageParse.append(buffer_cara)
            self.stateParse = 2
            return
        elif self.stateParse == 2:
            self.messageParse.append(buffer_cara)
            #print("DEBUG: len messageParse=  %d, length= %d  value= %d"%(len(self.messageParse),self.lengthParse,unpack('<B', buffer_cara)[0]))
            #print("DEBUG: len messageParse=  %d, length= %d  value= %d"%(len(self.messageParse),self.lengthParse,buffer_cara))
            if len(self.messageParse) >= self.lengthParse:
                #print("DEBUG: message received %s" % (self.messageParse))
                #print(self.messageParse)
                self.parse_frame(self.messageParse)
                self.stateParse = 0
                self.countParse = 0
                self.messageParse = []
                self.lengthParse = 0
                return

    def send(self,payload):
        mylog("SERIAL>%s"%(debughex2(payload)))
        self.port.write(payload)


    def cmd_add(self,opcode,data,serial_ack_cb,ui_ack_cb):
        payload = []
        payload.append(SERIAL_SOF)
        payload.append(0) # serial data len, defined later
        cmd = u16_to_array(opcode)
        payload = payload + cmd
        payload = payload + data
        payload[1] = 2+len(data)
        fcs = fcs_calc(payload)
        payload.append(fcs) # FCS
        #self.send(payload)
        #print(payload)
        item_queue = ItQueue(opcode,payload,serial_ack_cb,ui_ack_cb)
        self.cmd_queue.append(item_queue)
        self.process_queue()

    def cmd_add_blocking(self,opcode,data,timeout,serial_ack_cb,ui_ack_cb):
        self.ack_done = False
        self.response = Response(LMP_ERR_TIMEOUT)
        self.cmd_add(opcode,data,serial_ack_cb,ui_ack_cb)
        for i in range(timeout):
            if self.ack_done :
                return self.response
            time.sleep(0.1)
        return self.response

    def process_queue(self):
        if self.cmd_queue :
            cmd = self.cmd_queue[0]
            if cmd.state == 'to_send':
                cmd.state = 'sent'
                self.send(cmd.payload)

    def cmd_ack_handle(self,ack_opcode,frame_str):
        if self.cmd_queue :
            cmd = self.cmd_queue[0]
            if cmd.opcode == ack_opcode :
                #print("ack received : %s"%(serial_opcodes_str_dict.get(ack_opcode)))
                if cmd.serial_ack_cb is not None :
                    cmd.serial_ack_cb(cmd.ui_ack_cb,frame_str)

                self.cmd_queue.pop(0) # remove item
                self.process_queue() # next command

    def on_central_connected(self,function_cb):
        self.central_connected_cb = function_cb

    def on_central_disconnected(self,function_cb):
        self.central_disconnected_cb = function_cb

    def on_peripheral_connected(self,function_cb):
        self.peripheral_connected_cb = function_cb

    def on_peripheral_disconnected(self,function_cb):
        self.peripheral_disconnected_cb = function_cb

    def parse_frame(self,frame_str):
        """ Data parser.
            Look at data after SOF
        """
        if len(frame_str) >0 :
            try :
                pass
            except:
                print("err in parsing",debughex(frame_str))
            else:
                #data_len, event, status = unpack('<BHB', frame_str[:4])
                #print(frame_str[:4])
                data_len = frame_str[0]
                event = array_to_u16(frame_str[1:])
                status = frame_str[3]
                mylog("event=%s (x%04x) status=%s (x%02x)"%(serial_opcodes_str_dict.get(event&0x7fff),event,serial_errors_str_dict.get(status),status))
                event_ack = event&0x7fff
                if event&0x8000 :
                    self.cmd_ack_handle(event_ack,frame_str)

                    if event_ack == SERIAL_CMD_LOCAL_GROUPS_GET :
                        mylog("SERIAL_CMD_LOCAL_GROUPS_GET ack status=%s (%d)"%(serial_errors_str_dict.get(status),status))
                        parse_group_data(frame_str[4:-1])

                elif event == SERIAL_EVT_REMOTE_MODULE_INFO_IND :
                    """ format : src_addr (H) + LMP fields """
                    src_addr = array_to_u16(frame_str[4:])
                    mylog( "Evt SERIAL_EVT_REMOTE_MODULE_INFO_IND from %04X"%(src_addr))
                    module = Module(None) #self.module_get_by_lmp_addr(src_addr)
                    module.lmp_addr = src_addr
                    if module :
                        self.parse_lmp_fields(module,frame_str[6:-1])
                        updated_module = self.modules_update(module)
                        if updated_module :
                            if self.on_module_update_cb:
                                self.on_module_update_cb(updated_module)
                            # if devices info are not available, request them
                            if  updated_module.devices_info_available == False :
                                updated_module.devices_info_available = True
                                self.command_remote_device_info(src_addr)


                elif event == SERIAL_EVT_REMOTE_LMP_DATA_EVENT_IND :
                    """ format : src_addr (H) + LMP fields """
                    src_addr = array_to_u16(frame_str[4])
                    mylog( "Evt SERIAL_EVT_REMOTE_LMP_DATA_EVENT_IND from %04X"%(src_addr))
                    module = Module(None) #self.module_get_by_lmp_addr(src_addr)
                    module.lmp_addr = src_addr
                    if module :
                        self.parse_lmp_fields(module,frame_str[6:-1])
                        updated_module = self.modules_update(module)

                elif event == SERIAL_EVT_REMOTE_LMP_DATA_STATUS_IND :
                    """ format : src_addr (H) + LMP fields """
                    src_addr = array_to_u16(frame_str[4:])
                    mylog( "Status SERIAL_EVT_REMOTE_LMP_DATA_STATUS_IND from %04X"%(src_addr))
                    module = Module(None) #self.module_get_by_lmp_addr(src_addr)
                    module.lmp_addr = src_addr
                    if module :
                        self.parse_lmp_fields(module,frame_str[6:-1])
                        updated_module = self.modules_update(module)

                elif event == SERIAL_EVT_LOCAL_DEVICE_DATA_SET_IND :
                    src_addr = array_to_u16(frame_str[4:])
                    device_id =  frame_str[6] #unpack('<HB', frame_str[4:7])
                    payload = frame_str[7:-1]
                    mylog("SERIAL_EVT_LOCAL_DEVICE_DATA_SET_IND from %04X : %s"%(src_addr,debughex(payload)))

                elif event == SERIAL_EVT_REMOTE_DEVICE_DATA_EVENT_IND:
                    src_addr = array_to_u16(frame_str[4:])
                    device_id =  frame_str[6] #unpack('<HB', frame_str[4:7])
                    payload = frame_str[7:-1]
                    mylog("SERIAL_EVT_REMOTE_DEVICE_DATA_EVENT_IND from %04X : %s"%(src_addr,debughex(payload)))
                    updated_module = self.module_get_by_lmp_addr(src_addr)
                    if updated_module :
                        device = updated_module.device_get(device_id)
                        if device :
                            device.data = payload
                            if self.on_device_data_event_cb :
                                self.on_device_data_event_cb(updated_module,device,payload)

                elif event == SERIAL_EVT_REMOTE_DEVICE_DATA_STATUS_IND:
                    src_addr = array_to_u16(frame_str[4:])
                    device_id =  frame_str[6] #unpack('<HB', frame_str[4:7])
                    payload = frame_str[7:-1]
                    mylog("SERIAL_EVT_REMOTE_DEVICE_DATA_STATUS_IND from %04X : %s"%(src_addr,debughex(payload)))
                    updated_module = self.module_get_by_lmp_addr(src_addr)
                    if updated_module :
                        device = updated_module.device_get(device_id)
                        if device :
                            device.data = payload
                            if self.on_device_data_event_cb :
                                self.on_device_data_status_cb(updated_module,device,payload)

                elif event == SERIAL_EVT_LOCAL_DEBUG_STR:
                    level = frame_str[4]#unpack('<B', frame_str[4:5])
                    str = array_to_str(frame_str[5:-1])
                    mylog("%d debug[%d]:%s"%(len(frame_str),level,str))
                    if self.on_local_debug_cb :
                        self.on_local_debug_cb( level, str )


                elif event == SERIAL_EVT_LOCAL_CONNECT_IND :
                    #d0,d1,d2,d3,d4,d5 = unpack('<BBBBBB', frame_str[4:10])
                    d0 = frame_str[4]
                    d1 = frame_str[5]
                    d2 = frame_str[6]
                    d3 = frame_str[7]
                    d4 = frame_str[8]
                    d5 = frame_str[9]
                    mac_address = "%02X:%02X:%02X:%02X:%02X:%02X"%(d5,d4,d3,d2,d1,d0)
                    mylog( "Connected to mac %s"%(mac_address))
                    # update local module info
                    if self.on_local_module_update_cb :
                        self.on_local_module_update_cb( self.local_module() )
                    if self.peripheral_connected_cb:
                        self.peripheral_connected_cb()

                elif event == SERIAL_EVT_CENTRAL_CONNECTED_IND :
                    mylog( "SERIAL_EVT_CENTRAL_CONNECTED_IND")
                    self.central_connected = True
                    # update local module info
                    if self.on_local_module_update_cb :
                        self.on_local_module_update_cb( self.local_module() )
                    if self.central_connected_cb:
                        self.central_connected_cb()

                elif event == SERIAL_EVT_CENTRAL_DISCONNECTED_IND :
                    mylog( "SERIAL_EVT_CENTRAL_DISCONNECTED_IND")
                    self.central_connected = False
                    # update local module info
                    if self.on_local_module_update_cb :
                        self.on_local_module_update_cb( self.local_module() )
                    if self.central_disconnected_cb:
                        self.central_disconnected_cb()

                elif event == SERIAL_EVT_LOCAL_DISCONNECT_IND :
                    reason = frame_str[4]
                    mylog( "Disconnected, reason=%02X"%(reason))
                    # update local module info
                    if self.on_local_module_update_cb :
                        self.on_local_module_update_cb( self.local_module() )
                    if self.peripheral_disconnected_cb:
                        self.peripheral_disconnected_cb()

                elif event == SERIAL_EVT_LOCAL_UNREGISTER_IND :
                    mylog( "Event : local unregistered")
                    self.cmd_add(SERIAL_CMD_LOCAL_REGISTRATION_GET,[],self.opcode_ack_registration_get,None)
                    # This will update local module info
                    if self.on_unregistered_cb :
                        self.on_unregistered_cb( self.local_module() )

                elif event == SERIAL_EVT_LOCAL_REGISTER_IND :
                    mylog( "Event : local registered")
                    self.cmd_add(SERIAL_CMD_LOCAL_REGISTRATION_GET,[],self.opcode_ack_registration_get,None)
                    # This will update local module info
                    if self.on_registered_cb :
                        self.on_registered_cb( self.local_module() )

                elif event == SERIAL_EVT_LOCAL_DATETIME_IND :
                    timestamp = array_to_u32(frame_str[4:-1])
                    mylog("timestamp=%s (%08X)"%(timestamp_str(timestamp),timestamp))

                elif event == SERIAL_EVT_LOCAL_DEVICE_DATA_SET_IND :
                    device_id = frame_str[4]
                    device_payload = frame_str[5:-1]
                    mylog( "Event : local device %d"%(device_id))
                    mylog( "data %s"%(debughex(device_payload)))
                    #mylog( "Event : device %d %s"%(device_id,debughex(device_payload)))
                elif event == SERIAL_EVT_REMOTE_DEVICE_INFO_IND:
                    src_addr = array_to_u16(frame_str[4:])
                    payload = frame_str[6:-1]
                    #print( "%s"%(debughex(payload)))
                    dnr = frame_str[6]
                    did = frame_str[7]
                    dtype = array_to_u16(frame_str[8:])
                    dname = array_to_str(frame_str[10:14])
                    dstatus = frame_str[15]
                    dname=dname.split('\0')[0]
                    mylog("Status from module=%04X device=%d/%d type=%04X name=%s status=%X"%(src_addr,did,dnr,dtype,dname,dstatus))
                    updated_module = self.module_get_by_lmp_addr(src_addr)
                    if updated_module:
                        device = updated_module.device_create_or_get(did)
                        device.name = dname
                        device.type_id = dtype
                        device.status = dstatus
                        if self.on_module_update_cb:
                            self.on_module_update_cb(updated_module)
                        #if updated_module and self.on_device_data_status_cb :
                        #    self.on_device_data_status_cb(updated_module,payload)
                elif event == SERIAL_EVT_REMOTE_NETWORK_INFO_IND:
                    src_addr = array_to_u16(frame_str[4:])
                    module = self.module_get_by_lmp_addr(src_addr)
                    if module:
                        payload = frame_str[6:-1]
                        module.gtw_list = [0xffff,0xffff,0xffff,0xffff,0xffff,0xffff]
                        module.gtw_list[0] = array_to_u16(frame_str[6:])
                        module.gtw_list[1] = array_to_u16(frame_str[8:])
                        module.gtw_list[2] = array_to_u16(frame_str[10:])
                        module.gtw_list[3] = array_to_u16(frame_str[12:])
                        module.gtw_list[4] = array_to_u16(frame_str[14:])
                        module.gtw_list[5] = array_to_u16(frame_str[16:])
                        mylog("Network list from %04X = %04X %04X %04X %04X %04X %04X"
                        %(src_addr,module.gtw_list[0],module.gtw_list[1],module.gtw_list[2],module.gtw_list[3],module.gtw_list[4],module.gtw_list[5]))
                        if self.on_module_update_cb:
                            self.on_module_update_cb(module)
                elif event == SERIAL_EVT_REMOTE_BEACON_IND:
                    src_addr = array_to_u16(frame_str[4:])
                    payload = frame_str[6:-1]
                    # beacon modules may not be visible, just return src_addr
                    #module = self.module_get_by_lmp_addr(src_addr)
                    #if module :
                    if self.on_beacon_update_cb:
                        self.on_beacon_update_cb(src_addr,payload)
                elif event == SERIAL_EVT_HOST_MSG_IND:
                    payload = frame_str[4:-1]
                    if self.on_host_msg_cb:
                        self.on_host_msg_cb(payload)


    def parse_lmp_fields(self,module,frame_str):
        while len(frame_str) >=0 :
            frame_str = self.parse_lmp_field(module,frame_str)
            if frame_str is None :
                return

    def parse_lmp_field(self,module,frame_str):
        """ Parse LMP fields.
        """
        #mylog("parse_lmp_field : %s"%frame_str)

        if len(frame_str) >=2 :
            try:
                lmp_len = frame_str[0]
                lmp_command = frame_str[1]
                mylog("field[%d]=%02X %s"%(lmp_len, lmp_command,frame_str[2:lmp_len+1]))
                if lmp_command == LMP_PARAM_MODULE_SW_VERSION :
                    magic = frame_str[2] #unpack('<BBBB', frame_str[2:6])
                    major = frame_str[3] #unpack('<BBBB', frame_str[2:6])
                    minor = frame_str[4] #unpack('<BBBB', frame_str[2:6])
                    revision = frame_str[5] #unpack('<BBBB', frame_str[2:6])
                    mylog( "software version %d.%d.%d(x%02X)"%(major, minor, revision,magic))
                    module.sw_version = ("%d.%d.%d (x%02X)"%(major, minor, revision,magic))

                elif lmp_command == LMP_PARAM_MODULE_HW_VERSION :
                    major = frame_str[2] #unpack('<BBBB', frame_str[2:6])
                    minor = frame_str[3] #unpack('<BBBB', frame_str[2:6])
                    revision = frame_str[4] #unpack('<BBBB', frame_str[2:6])
                    #major, minor, revision = unpack('<BBB', frame_str[2:5])
                    mylog( "hardware version %d.%d.%d"%(major, minor, revision))
                    module.hw_version = ("%d.%d.%d"%(major, minor, revision))

                elif lmp_command == LMP_PARAM_SHORT_ADDRESS :
                    module.lmp_addr = array_to_u16(frame_str[2:]) #unpack('<H', frame_str[2:4])
                    mylog( "lmp_addr = %04X"%(module.lmp_addr))

                elif lmp_command == LMP_PARAM_MODULE_REFERENCE :
                    #d0,d1,d2,d3,d4,d5 = unpack('<BBBBBB', frame_str[2:8])
                    d0 = frame_str[2]
                    d1 = frame_str[3]
                    d2 = frame_str[4]
                    d3 = frame_str[5]
                    d4 = frame_str[6]
                    d5 = frame_str[7]
                    mac_address = "%02X%02X%02X%02X%02X%02X"%(d5,d4,d3,d2,d1,d0)
                    mylog( "mac %s"%(mac_address))
                    module.uid = mac_address

                    module.manufacturer_id = array_to_u16(frame_str[8:]) #unpack('<H', frame_str[8:10])
                    mylog( "manufacturer_id %d"%(module.manufacturer_id))

                    module.model_id = array_to_u16(frame_str[10:]) #unpack('<H', frame_str[10:12])
                    mylog( "model_id %d"%(module.model_id))

                    module.module_type = array_to_u16(frame_str[12:]) #unpack('<H', frame_str[12:14])
                    mylog( "module_type %d"%(module.module_type))

                    module.custom_id = array_to_u16(frame_str[14:]) #unpack('<B', frame_str[14:15])
                    mylog( "custom_id %d"%(module.custom_id))

                elif lmp_command == LMP_PARAM_MAC_ADDRESS :
                    #d0,d1,d2,d3,d4,d5 = unpack('<BBBBBB', frame_str[2:8])
                    d0 = frame_str[2]
                    d1 = frame_str[3]
                    d2 = frame_str[4]
                    d3 = frame_str[5]
                    d4 = frame_str[6]
                    d5 = frame_str[7]
                    mac_address = "%02X%02X%02X%02X%02X%02X"%(d5,d4,d3,d2,d1,d0)
                    #mac_address = "%02X:%02X:%02X:%02X:%02X:%02X"%(d5,d4,d3,d2,d1,d0)
                    #print "mac %s"%(mac_address)
                    mylog( "mac %s"%(mac_address))
                    #pMac=(mac_address)
                    module.uid = mac_address

                elif lmp_command == LMP_PARAM_MODULE_TYPE :
                    module.type_id = array_to_u16(frame_str[2:]) #unpack('<H', frame_str[2:4])
                    #print "type %d"%(module_type)
                    mylog( "type %d"%(module.type_id))

                elif lmp_command == LMP_PARAM_MANUFACTURER_NAME:
                    module.manufacturer = array_to_str(frame_str[2:1+lmp_len]) #frame_str[2:1+lmp_len]
                    mylog( "manufacturer[%d] '%s'"%(len(module.manufacturer), module.manufacturer))

                elif lmp_command == LMP_PARAM_MODEL_NAME:
                    module.model = array_to_str(frame_str[2:1+lmp_len]) #frame_str[2:1+lmp_len]
                    mylog( "model '%s'"%(module.model))

                elif lmp_command == LMP_PARAM_MODULE_NAME:
                    module.name = array_to_str(frame_str[2:1+lmp_len]) #frame_str[2:1+lmp_len]
                    mylog( "name '%s'"%(module.name))

                #elif lmp_command == LMP_PARAM_MODULE_API_VERSION:

                elif lmp_command == LMP_PARAM_RSSI :
                    rssi = array_to_signed(frame_str[2])
                    #mean,std = average_rssi(rssi)
                    #mylog( "Rssi = %d (average = %2.1f, std = %2.1f)"%(rssi,mean,std))
                    module.rssi = rssi

                elif lmp_command == LMP_PARAM_ROLE :
                    module.role = frame_str[2]
                    mylog( "role %d"%(module.role))

                elif lmp_command == LMP_STATUS_DEVICE_INFO :
                    dnr = frame_str[2]
                    did = frame_str[3]
                    dtype = array_to_u16(frame_str[4:])
                    dname = array_to_str(frame_str[6:10])
                    dstatus = frame_str[11]
                    dname=dname.split('\0')[0]
                    mylog("device src=%04X id=%d/%d type=%04X name=%s status=%X"%(src_addr,did,dnr,dtype,dname,dstatus))

                elif lmp_command == LMP_PARAM_CONFIG_STRUCT :
                    pns = frame_str[2:1+lmp_len]
                    params = pns.split('\n')
                    #print "names",params
                    formats = []
                    self.storage_params = []
                    for p in params :
                        param = p.split(',')
                        formats.append(param[1])
                        self.storage_params.append([param[0],param[1]])
                    self.storage_format = "<"+"".join(formats)
                    #print storage_format
                elif lmp_command == LMP_PARAM_BATTERY_LEVEL :
                    module.battery_level = frame_str[2] #unpack('<B', frame_str[2:])
                    #print "batt_level=%d"%(batt_level)
                    mylog( "battery_level %d"%(module.battery_level))

                return frame_str[1+lmp_len:]
            except Exception as e:
                print("err in field parsing")
                print(e)
                print("%s"%(traceback.print_exc()))
                return None

    def local_module(self):
        return self.module_get(self.local_module_addr)

    def module_get(self,mac_addr):
        for module in self.modules:
            if module.uid == mac_addr:
                mylog("found module %s"%(mac_addr))
                return module
        # no module, create it
        module = Module(mac_addr)
        self.modules.append(module)
        mylog("new module %s"%(mac_addr))
        return module

    def module_get_by_lmp_addr(self,lmp_addr):
        for module in self.modules:
            if module.lmp_addr == lmp_addr:
                return module
        return None

    def device_get(self,mac_addr,device_id):
        return self.module_get(mac_addr).device_get(device_id)
        try :
            pass
        except :
            return None

    def modules_update(self,module):
        """ Given module info,
            find an existing module and update it.
        """
        mylog("module_update")
        existing_module = None
        if module :
            if module.uid :
                #print("I know uid=%s"%(module.uid))
                existing_module = self.module_get(module.uid)
                if existing_module == None :
                    mylog("Add module %04X"%(module.lmp_addr))
                    existing_module = Module(module.uid)
            elif module.lmp_addr :
                #print("I know lmp_addr=%04X"%(module.lmp_addr))
                existing_module = self.module_get_by_lmp_addr(module.lmp_addr)
            if existing_module :
                #print("existing_module %04X"%(module.lmp_addr))
                # update fields of existing_module
                if module.lmp_addr != existing_module.lmp_addr:
                    existing_module.lmp_addr = module.lmp_addr
                    mylog("update lmp addr")
                if module.name :
                    existing_module.name = module.name
                if module.manufacturer :
                    existing_module.manufacturer = module.manufacturer
                if module.model :
                    existing_module.model = module.model
                if module.hw_version:
                    existing_module.hw_version = module.hw_version
                if module.sw_version :
                    existing_module.sw_version = module.sw_version
                if module.type_id:
                    existing_module.type_id = module.type_id
                if module.role:
                    existing_module.role = module.role
                #existing_module.configuration
                #existing_module.power_source
                if module.battery_level :
                    existing_module.battery_level = module.battery_level
                if module.rssi:
                    existing_module.rssi = module.rssi
                #existing_module.interval
                #existing_module.status
                if module.timestamp :
                    existing_module.timestamp = module.timestamp
                else :
                    module.timestamp = timestamp_now()
                #existing_module.heartbeat_timestamp
                return existing_module
            else :
                 return None


    def parse_storage_struct(self,frame_str):
        module = self.local_module()
        while len(frame_str) >=0 :
            frame_str = self.parse_lmp_field(module,frame_str)
            if frame_str is None :
                break

    def parse_storage_data(self,frame_str):
        #print repr(frame_str)
        data = unpack(self.storage_format, frame_str)
        for p, d in zip(self.storage_params,data):
            mylog("set config[%s]=%s"%(p[0],d))
            #p.var.set(d)

    def pack_storage_data(self):
        data = []
        for p in self.storage_params:
            data.append(p.value())
        #print data,storage_format, repr(pack(storage_format,*data))
        return pack(self.storage_format,*data)


class Lmp(LmpSerial):
    def __init__(self,serial_device):
        super(Lmp, self).__init__(serial_device)
        #self.lms_send_callback_fct = None

    #def on_init_complete(self,callback_fct):
    #    self.on_init_complete_cb = callback_fct

    def on_registered(self,callback_fct):
        self.on_registered_cb = callback_fct

    def on_unregistered(self,callback_fct):
        self.on_unregistered_cb = callback_fct

    def on_local_module_update(self,callback_fct):
        self.on_local_module_update_cb = callback_fct

    def on_module_update(self,callback_fct):
        self.on_module_update_cb = callback_fct

    def on_beacon_update(self,callback_fct):
        self.on_beacon_update_cb = callback_fct

    def on_host_msg_update(self,callback_fct):
        self.on_host_msg_cb = callback_fct

    def on_local_debug_ind(self,callback_fct):
        self.on_local_debug_cb = callback_fct

    def on_device_data_status_ind(self,callback_fct):
        """ called when received a SERIAL_EVT_REMOTE_DEVICE_DATA_STATUS_IND frame.
        """
        self.on_device_data_status_cb = callback_fct

    def on_device_data_event_ind(self,callback_fct):
        """ called when received a SERIAL_EVT_REMOTE_DEVICE_DATA_EVENT_IND frame.
        """
        self.on_device_data_event_cb = callback_fct

    def init(self,on_init_complete_cb, debug=False):
        global global_debug
        self.start()
        self.cmd_add(SERIAL_CMD_LOCAL_VERSION_GET,[],self.opcode_ack_local_version,None)
        self.cmd_add(SERIAL_CMD_LOCAL_MODULE_INFO_GET,[], self.opcode_ack_local_module_info,None )
        self.cmd_add(SERIAL_CMD_LOCAL_DEVICES_INFO_GET,[], self.opcode_ack_local_devices_info,None )
        #self.cmd_add(SERIAL_CMD_LOCAL_REGISTER,[0],self.opcode_ack_register)
        self.command_local_registration_get(on_init_complete_cb)
        self.debug = debug
        global_debug = debug

    def command_local_register(self):
        return self.cmd_add_blocking(SERIAL_CMD_LOCAL_REGISTER,[0],50,None,None)

    def command_local_config_get(self):
        self.cmd_add(SERIAL_CMD_LOCAL_CONFIG_STRUCT_GET,[],self.opcode_ack_local_config_struct_get,None)

    def command_local_config_data_get(self):
        self.cmd_add(SERIAL_CMD_LOCAL_CONFIG_DATA_GET,[],self.opcode_ack_local_config_data_get,None)

    def command_local_reset(self):
        self.cmd_add(SERIAL_CMD_LOCAL_RESET,[],None,None)

    def command_local_factory_reset(self):
        self.cmd_add(SERIAL_CMD_LOCAL_FACTORY_RESET,[],None,None)

    def command_local_register(self):
        self.cmd_add(SERIAL_CMD_LOCAL_REGISTER,[],None,None)

    def command_local_device_data_status_set(self,device_id,device_data):
        self.cmd_add(SERIAL_CMD_LOCAL_DEVICE_DATA_STATUS_SET,[device_id]+device_data,None,None)

    def command_local_registration_get(self,callback_fct):
        self.cmd_add(SERIAL_CMD_LOCAL_REGISTRATION_GET,[],self.opcode_ack_registration_get,callback_fct)

    def command_local_factory_read(self):
        self.cmd_add(SERIAL_CMD_LOCAL_FACTORY_DATA_GET,[],self.opcode_ack_factory_get,None)

    def command_local_factory_write(self,data):
        # complete data with 0 to 32 bytes before sending.
        for i in range(32-len(data)):
            data.append(0)
        self.cmd_add(SERIAL_CMD_LOCAL_FACTORY_DATA_SET,data,None,None)

    def command_local_host_msg_event(self,data):
        self.cmd_add(SERIAL_CMD_HOST_MSG_EVENT,data,None,None)

    def command_local_crypt_nonce_get(self,callback_fct):
        self.cmd_add(SERIAL_CMD_LOCAL_CRYPT_NONCE_GET,[],self.opcode_ack_local_crypt_nonce_get,callback_fct)

    def command_local_crypt_key0_get(self,callback_fct):
        self.cmd_add(SERIAL_CMD_LOCAL_CRYPT_AUTHKEY_GET,[0],self.opcode_ack_local_crypt_key0_get,callback_fct)

    def command_local_crypt_key1_get(self,callback_fct):
        #self.on_local_crypt_nonce_get = callback_fct
        self.cmd_add(SERIAL_CMD_LOCAL_CRYPT_AUTHKEY_GET,[1],self.opcode_ack_local_crypt_key1_get,callback_fct)

    def command_local_crypt_nonce_set(self,data,callback_fct):
        #self.on_local_crypt_nonce_get = callback_fct
        payload = string_to_array(data)
        self.cmd_add(SERIAL_CMD_LOCAL_CRYPT_NONCE_SET,payload,None,callback_fct)

    def command_local_crypt_key0_set(self,data,callback_fct):
        #self.on_local_crypt_nonce_get = callback_fct
        payload = [0] + string_to_array(data)
        self.cmd_add(SERIAL_CMD_LOCAL_CRYPT_AUTHKEY_SET,payload,None,callback_fct)

    def command_local_crypt_key1_set(self,data,callback_fct):
        #self.on_local_crypt_nonce_get = callback_fct
        payload = [1] + string_to_array(data)
        self.cmd_add(SERIAL_CMD_LOCAL_CRYPT_AUTHKEY_SET,payload,None,None)

    def command_local_unregister(self):
        self.cmd_add(SERIAL_CMD_LOCAL_UNREGISTER,[],self.opcode_ack_local_unregister,None)
        self.command_local_registration_get(None)

    def command_network_discover(self):
        mylog("command_network_discover")
        self.cmd_add(SERIAL_CMD_NETWORK_GET,[0xff,0xff,0x2],None,None)

    def command_remote_module_info(self):
        mylog("command_remote_module_info")
        self.cmd_add(SERIAL_CMD_REMOTE_MODULE_INFO_GET,[0xff,0xff],None,None)

    def command_remote_device_info(self, lmp_addr):
        mylog("command_remote_device_info %04X"%(lmp_addr))
        dst = u16_to_array(lmp_addr)
        self.cmd_add(SERIAL_CMD_REMOTE_DEVICE_INFO_GET,dst,None,None)

    def command_local_module_property_get(self,property_id,callback_fct):
        self.cmd_add(SERIAL_CMD_LOCAL_MODULE_PROPERTY_GET,[property_id],self.opcode_ack_module_property_get,None)

    def command_local_module_property_set(self,property_id,property_data,callback_fct):
        self.cmd_add(SERIAL_CMD_LOCAL_MODULE_PROPERTY_SET,[property_id]+property_data,self.opcode_ack_module_property_set,None)

    def command_local_module_property_delete(self,property_id,callback_fct):
        self.cmd_add(SERIAL_CMD_LOCAL_MODULE_PROPERTY_DELETE,[property_id],self.opcode_ack_module_property_delete,None)

    def command_local_device_property_get(self,device_id,property_id,callback_fct):
        self.cmd_add(SERIAL_CMD_LOCAL_DEVICE_PROPERTY_GET,[device_id,property_id],self.opcode_ack_device_property_get,None)

    def command_local_device_property_set(self,device_id,property_id,property_data,callback_fct):
        self.cmd_add(SERIAL_CMD_LOCAL_DEVICE_PROPERTY_SET,[device_id,property_id]+property_data,self.opcode_ack_device_property_set,None)

    def command_local_device_property_delete(self,device_id,property_id,callback_fct):
        self.cmd_add(SERIAL_CMD_LOCAL_DEVICE_PROPERTY_DELETE,[device_id,property_id],self.opcode_ack_device_property_delete,None)

    def command_lmp_device_data_set(self,module_uid,device_id,device_data):
        """ TODO implement instead SERIAL_CMD_LMP_DEVICE_DATA_SET """

        module = self.module_get(module_uid)
        if module :
            module.data = device_data
            dest_addr = module.lmp_addr
            d_addr = u16_to_array(dest_addr)
            lmp_msg = []
            lmp_msg.append(2+len(device_data))
            lmp_msg.append(LMP_COMMAND_DEVICE_DATA_SET)
            lmp_msg.append(device_id)
            lmp_msg += device_data

            data = d_addr + lmp_msg
            self.cmd_add(SERIAL_CMD_LOCAL_LMP_SEND,data,None,None)

    def central_connect(self,mac_address,on_connected_cb, on_disconnected_cb) :
        mylog("Connect req to %s"%(mac_address))
        lmac = mac_to_array(mac_address)
        self.on_central_connected(on_connected_cb)
        self.on_central_disconnected(on_disconnected_cb)
        r = self.cmd_add_blocking(SERIAL_CMD_CENTRAL_CONNECT,lmac,50,self.opcode_ack_central_connect,None)
        if r.status == LMP_ERR_SUCCESS :
            # wait for connected ind event
            for i in range(50):
                if self.central_connected :
                    return r
                time.sleep(0.1)
            return LMP_ERR_TIMEOUT


    def central_disconnect(self):
        mylog("Disconnect")
        self.cmd_add_blocking(SERIAL_CMD_CENTRAL_DISCONNECT,[],50,self.opcode_ack_central_disconnect,None)

    def central_lms_send(self,dest_addr,enc,lms_msg,callback_fct):
        #self.lms_send_callback_fct = None#callback_fct
        d_enc = u8_to_array(enc)
        d_addr = lmpaddr_to_array(dest_addr)
        data = d_enc + d_addr + lms_msg
        self.cmd_add(SERIAL_CMD_CENTRAL_LMS_SEND,data,self.opcode_ack_local_lms_send,callback_fct)
        #if ui_ack_cb is not None :
        #    ui_ack_cb(status)

    def b_central_lms_send(self,dest_addr,enc,lms_msg):
        #self.lms_send_callback_fct = None#callback_fct
        d_enc = u8_to_array(enc)
        d_addr = lmpaddr_to_array(dest_addr)
        data = d_enc + d_addr + lms_msg
        return self.cmd_add_blocking(SERIAL_CMD_CENTRAL_LMS_SEND,data,50,self.opcode_ack_local_lms_send,None)

    def opcode_ack_local_config_struct_get(self,ui_ack_cb,frame_str):
        """ Get local configuration structure.
        """
        status = frame_str[0]
        mylog("SERIAL_CMD_LOCAL_CONFIG_DATA_GET ack status=%s (%d)"%(serial_errors_str_dict.get(status),status))
        self.parse_storage_struct(frame_str[4:-1])
        self.command_local_config_data_get()
        if ui_ack_cb is not None :
            ui_ack_cb(status)

    def opcode_ack_local_config_data_get(self,ui_ack_cb,frame_str):
        """ Get local configuration.
        """
        status = frame_str[0]
        mylog("SERIAL_CMD_LOCAL_CONFIG_DATA_GET ack status=%s (%d)"%(serial_errors_str_dict.get(status),status))
        self.parse_storage_data(frame_str[4:-1])
        if ui_ack_cb is not None :
            ui_ack_cb(status)

    def opcode_ack_local_version(self,ui_ack_cb,frame_str):
        """ Get local module version.
        """
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        mylog("COMMAND_GET_FW_VERSION ack status=%s (%d)"%(serial_errors_str_dict.get(status),status))
        module = Module(None)
        self.parse_lmp_fields(module,frame_str[4:-1])
        self.local_module_addr = module.uid
        local_module = self.module_get(module.uid)
        local_module.sw_version = module.sw_version
        local_module.hw_version = module.hw_version
        if ui_ack_cb is not None :
            ui_ack_cb(status)

    def opcode_ack_local_module_info(self,ui_ack_cb,frame_str):
        """ Get local module info.
        """
        module = self.local_module()
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        mylog("SERIAL_CMD_LOCAL_MODULE_INFO_GET ack status=%s (%d)"%(serial_errors_str_dict.get(status),status))
        if status == LMP_ERR_SUCCESS:
            self.parse_lmp_fields(module,frame_str[4:-1])
            if ui_ack_cb is not None :
                ui_ack_cb(status)

    def opcode_ack_local_devices_info(self,ui_ack_cb,frame_str):
        """ Get local deices info.
        """
        module = self.local_module()
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        devices_nr = frame_str[4]
        mylog("SERIAL_CMD_LOCAL_DEVICES_INFO_GET ack status=%s (%d)"%(serial_errors_str_dict.get(status),status))
        if status == LMP_ERR_SUCCESS:
            mylog("devices nr=%d"%(devices_nr))
            frame_str = frame_str[5:-1]
            for i in range(devices_nr):
                devid = frame_str[0]
                devtype = array_to_u16(frame_str[1:])
                devname = array_to_str(frame_str[3:10])
                devstatus = frame_str[11] #unpack("<BH8sB", frame_str[:12])
                mylog("device[%d]: %d %d %s %d"%(i,devid,devtype,devname,devstatus))
                device = module.device_create_or_get(devid)
                device.name = devname
                device.type_id = devtype
                device.status = devstatus
                frame_str = frame_str[12:]
            if ui_ack_cb is not None :
                ui_ack_cb(status)

    def opcode_ack_factory_get(self,ui_ack_cb,frame_str):
        """ Get factory config data.
        """
        #print "ack:",debughex(frame_str)
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        mylog("SERIAL_CMD_LOCAL_FACTORY_GET ack status=%s (%d)"%(serial_errors_str_dict.get(status),status))
        if status == LMP_ERR_SUCCESS:
            frame_str = frame_str[5:-1]
            mylog("data=%s"%(debughex(frame_str)))
            local_module = self.local_module()
            local_module.factory_config = frame_str
            if ui_ack_cb is not None :
                ui_ack_cb(status)
            if self.on_local_module_update_cb :
                self.on_local_module_update_cb( local_module )

    def opcode_ack_registration_get(self,ui_ack_cb,frame_str):
        """ Get registration status.
        """
        #print "ack:",debughex(frame_str)
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        mylog("SERIAL_CMD_LOCAL_REGISTRATION_GET ack status=%s (%d)"%(serial_errors_str_dict.get(status),status))
        if status == LMP_ERR_SUCCESS:
            local_module = self.local_module()
            local_module.registered = frame_str[4]
            local_module.encryption = frame_str[5] #unpack('<BB', frame_str[4:-1])
            mylog("registered:%d, encryption:%d"%(local_module.registered, local_module.encryption))

        if ui_ack_cb is not None :
            ui_ack_cb(status)


    def opcode_ack_register(self,ui_ack_cb,frame_str):
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        if status == LMP_ERR_SUCCESS:
            if ui_ack_cb is not None :
                ui_ack_cb(status)

    def opcode_ack_local_unregister(self,ui_ack_cb,frame_str):
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        mylog("SERIAL_CMD_LOCAL_UNREGISTER ack status=%s (%d)"%(serial_errors_str_dict.get(status),status))
        if status == LMP_ERR_SUCCESS:
            if ui_ack_cb is not None :
                ui_ack_cb(status)

    def opcode_ack_local_crypt_nonce_get(self,ui_ack_cb,frame_str):
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        #print dlen, event, status
        if status == LMP_ERR_SUCCESS:
            local_module = self.local_module()
            local_module.crypt_nonce = frame_str[4:data_len+1]
            if ui_ack_cb is not None :
                ui_ack_cb(status)
            if self.on_local_module_update_cb :
                self.on_local_module_update_cb( local_module )

    def opcode_ack_local_crypt_key0_get(self,ui_ack_cb,frame_str):
        #TODO to merge with  opcode_ack_local_crypt_key1_get and add key_index in ack msg.
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        #print dlen, event, status
        if status == LMP_ERR_SUCCESS:
            local_module = self.local_module()
            local_module.crypt_key0 = frame_str[4:data_len+1]
            if ui_ack_cb is not None :
                ui_ack_cb(status)
            if self.on_local_module_update_cb :
                self.on_local_module_update_cb( local_module )


    def opcode_ack_local_crypt_key1_get(self,ui_ack_cb,frame_str):
        #TODO to merge with  opcode_ack_local_crypt_key1_get and add key_index in ack msg.
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        #print dlen, event, status
        if status == LMP_ERR_SUCCESS:
            local_module = self.local_module()
            local_module.crypt_key1 = frame_str[4:data_len+1]
            if ui_ack_cb is not None :
                ui_ack_cb(status)
            if self.on_local_module_update_cb :
                self.on_local_module_update_cb( local_module )

    def opcode_ack_module_property_get(self,ui_ack_cb,frame_str):
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        mylog("SERIAL_CMD_LOCAL_MODULE_PROPERTY_GET ack status=%s (%d)"%(serial_errors_str_dict.get(status),status))
        if status == LMP_ERR_SUCCESS:
            if ui_ack_cb is not None :
                ui_ack_cb(status)

    def opcode_ack_module_property_set(self,ui_ack_cb,frame_str):
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        mylog("SERIAL_CMD_LOCAL_MODULE_PROPERTY_SET ack status=%s (%d)"%(serial_errors_str_dict.get(status),status))
        if status == LMP_ERR_SUCCESS:
            if ui_ack_cb is not None :
                ui_ack_cb(status)

    def opcode_ack_module_property_delete(self,ui_ack_cb,frame_str):
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        mylog("SERIAL_CMD_LOCAL_MODULE_PROPERTY_DELETE ack status=%s%d"%(serial_errors_str_dict.get(status),status))
        if status == LMP_ERR_SUCCESS:
            if ui_ack_cb is not None :
                ui_ack_cb(status)

    def opcode_ack_device_property_get(self,ui_ack_cb,frame_str):
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        mylog("SERIAL_CMD_LOCAL_DEVICE_PROPERTY_GET ack status=%s (%d)"%(serial_errors_str_dict.get(status),status))
        if status == LMP_ERR_SUCCESS:
            if ui_ack_cb is not None :
                ui_ack_cb(status)

    def opcode_ack_device_property_set(self,ui_ack_cb,frame_str):
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        mylog("SERIAL_CMD_LOCAL_DEVICE_PROPERTY_SET ack status=%s (%d)"%(serial_errors_str_dict.get(status),status))
        if status == LMP_ERR_SUCCESS:
            if ui_ack_cb is not None :
                ui_ack_cb(status)

    def opcode_ack_device_property_delete(self,ui_ack_cb,frame_str):
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        mylog("SERIAL_CMD_LOCAL_DEVICE_PROPERTY_DELETE ack status=%s%d"%(serial_errors_str_dict.get(status),status))
        if status == LMP_ERR_SUCCESS:
            if ui_ack_cb is not None :
                ui_ack_cb(status)

    def opcode_ack_central_connect(self,ui_ack_cb,frame_str):
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        mylog("SERIAL_CMD_CENTRAL_CONNECT ack status=%s (%d)"%(serial_errors_str_dict.get(status),status))
        if status == LMP_ERR_SUCCESS:
            if ui_ack_cb is not None :
                ui_ack_cb(status)
            self.ack_done = True
            self.response.status = status

    def opcode_ack_central_disconnect(self,ui_ack_cb,frame_str):
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        mylog("SERIAL_CMD_CENTRAL_DISCONNECT ack status=%s (%d)"%(serial_errors_str_dict.get(status),status))
        if status == LMP_ERR_SUCCESS:
            if ui_ack_cb is not None :
                ui_ack_cb(status)

    def opcode_ack_local_lms_send(self,ui_ack_cb,frame_str):
        data_len = frame_str[0]
        event = array_to_u16(frame_str[1:])
        status = frame_str[3]
        payload = None
        if status == LMP_ERR_SUCCESS:
            payload = frame_str[4:-1]
        mylog("SERIAL_CMD_LOCAL_LMS_SEND ack status=%s (%d)"%(serial_errors_str_dict.get(status),status))
        if ui_ack_cb is not None :
            ui_ack_cb(status,payload)
        self.ack_done = True
        self.response.status = status
        self.response.payload = payload
        self.response.payload_len = data_len
