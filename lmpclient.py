#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Copyright (c) 2016-2018 - Linkio SAS. All Rights Reserved.

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
__version__     = "1.0.0"
__status__      = "Development"

import argparse

from lmp.lmpserial import *

try:
    # python 2.x
    #import Tkinter as tk
    from Tkinter import *
except ImportError:
    # python 3.x
    #import tkinter as tk
    from tkinter import *
from tkMessageBox import *

#from ui.scroll import *
from ui.log import *
from ui.itemlist import *

class Param() :
    def __init__(self, widget, name, side, width, default):
        self.name = name
        #self.format = format
        self.f = Frame(widget, width = 32,borderwidth=1) #, relief=SUNKEN
        self.f.pack(fill=BOTH, expand=False, side=side )
        self.lTitle = Label(self.f, text=name, width = 16)
        self.lTitle.pack(fill=BOTH,side=LEFT, padx=5)
        self.var = StringVar()
        self.entry = Entry(self.f, textvariable=self.var,width = width)
        self.entry.pack(fill=BOTH, expand=False,side=LEFT,padx=5)
        if len(default):
            self.entry.insert(0,default)
    def set(self,value) :
        return self.var.set(value)
    def get(self) :
        return self.var.get()
    def get_int(self) :
        return int(self.var.get())
    def get_hexstr4(self) :
        val = int(self.var.get())
        return "%1x"%(val)
    def get_hexstr8(self) :
        val = int(self.var.get())
        return "%02x"%(val)
    def get_hexstr16(self) :
        val = int(self.var.get())
        s = "%04x"%(val)
        return s[2:4]+s[0:2] # little endian
    def get_hexstr32(self) :
        val = int(self.var.get())
        s = "%08x"%(val)
        return s[6:8]+s[4:6]+s[2:4]+s[0:2] # little endian

class LocalModuleFrame() :
    def __init__(self, widget, name):
        self.uid = None
        self.name = name
        self.fLocal = LabelFrame(widget,text=name,borderwidth=2,relief=GROOVE)
        self.fLocal.pack(fill=BOTH, expand=False,side=LEFT,padx=2,pady=2)
        self.fLocalConfig = Frame(self.fLocal,borderwidth=1)
        self.fLocalConfig.pack(fill=BOTH, expand=False,side=TOP,padx=5,pady=5)
        self.fLocalButtons = Frame(self.fLocal,borderwidth=1)
        self.fLocalButtons.pack(fill=BOTH, expand=False,side=TOP,padx=5,pady=5)

        self.pMac = Param(self.fLocalConfig,"MAC addr",TOP,12,"")
        self.pLMPAddr = Param(self.fLocalConfig,"LMP addr",TOP,4,"")
        self.pManufacturer = Param(self.fLocalConfig,"Manufacturer",TOP,8,"")
        self.pModel = Param(self.fLocalConfig,"Model",TOP,8,"")
        self.pName = Param(self.fLocalConfig,"Name",TOP,8,"")
        self.pSWVersion = Param(self.fLocalConfig,"SW version",TOP,16,"")
        self.pHWVersion = Param(self.fLocalConfig,"HW version",TOP,16,"")
        self.pType = Param(self.fLocalConfig,"Type",TOP,20,"")
        self.pRole = Param(self.fLocalConfig,"Role",TOP,8,"")
        self.pMsg = Param(self.fLocalConfig,"Last message",TOP,32,"")

        self.fRegistration = LabelFrame(self.fLocalConfig,text="Registration",borderwidth=2,relief=SUNKEN)
        self.fRegistration.pack(fill=BOTH, expand=False,side=TOP,padx=5,pady=5)
        self.fRegistration_opened = False
        self.pReg = Param(self.fRegistration,"Registered",LEFT,2,"")
        self.bEdit = Button(self.fRegistration, text = "Edit", width=12, command = self.cRegistration)
        self.bEdit.pack(side=LEFT,padx=10,pady=1)

        self.ui_devices = []

        self.bConfig = Button(self.fLocalButtons, text = "Config", width=12, command = self.cConfig)
        self.bConfig.pack(side=TOP,padx=10,pady=1)
        self.bReset = Button(self.fLocalButtons, text = "Reset", width=12, command = self.cReset)
        self.bReset.pack(side=TOP,padx=10,pady=1)
        self.bUnregister = Button(self.fLocalButtons, text = "Unregister", width=12, command = self.cUnregister)
        self.bUnregister.pack(side=TOP,padx=10,pady=1)
        self.bDiscover = Button(self.fLocalButtons, text = "Discover", width=12, command = self.cDiscover)
        self.bDiscover.pack(side=TOP,padx=10,pady=1)

    def ui_device_get(self,device_id):
        for ui_device in self.ui_devices:
            if ui_device.device_id == device_id:
                return ui_device
        # no module, create it
        ui_device = DeviceFrame(self.fLocalConfig, self.uid, device_id)
        self.ui_devices.append(ui_device)
        ui_log.debug("UI","new ui device %d"%(device_id))
        return ui_device

    def cRegistration(self):
        if self.fRegistration_opened == False:
            self.fRegistration_opened = True
            self.wRegistration = Toplevel()
            self.wRegistration.title("Local registration")
            self.wRegistration.protocol("WM_DELETE_WINDOW", self.wRegistration.iconify)
            self.pEnc = Param(self.wRegistration,"Encryption",TOP,2,"")
            self.pNonce = Param(self.wRegistration,"Nonce",TOP,40,"")
            self.pKey0 = Param(self.wRegistration,"Key[0]",TOP,40,"")
            self.pKey1 = Param(self.wRegistration,"Key[1]",TOP,40,"")
            self.bRegRead = Button(self.wRegistration, text = "Read", width=12, command = self.cRegRead)
            self.bRegRead.pack(side=TOP,padx=10,pady=1)
            self.bRegWrite = Button(self.wRegistration, text = "Write", width=12, command = self.cRegWrite)
            self.bRegWrite.pack(side=TOP,padx=10,pady=1)

            self.cRegRead() # refresh data

            #self.pEnc.set(client_lmp.local_module().encryption)
            #client_lmp.command_local_crypt_nonce_get(on_local_crypt_nonce_get)
            #client_lmp.command_local_crypt_key0_get(on_local_crypt_key0_get)
            #client_lmp.command_local_crypt_key1_get(on_local_crypt_key1_get)

    def cRegRead(self):
        """ Read registration and encryption values.
        """
        #self.pEnc.set(client_lmp.local_module().encryption)
        client_lmp.command_local_crypt_nonce_get(None)
        client_lmp.command_local_crypt_key0_get(None)
        client_lmp.command_local_crypt_key1_get(None)

    def cRegWrite(self):
        """ Write encryption values.
        """
        client_lmp.command_local_crypt_nonce_set(self.pNonce.get(),None)
        client_lmp.command_local_crypt_key0_set(self.pKey0.get(),None)
        client_lmp.command_local_crypt_key1_set(self.pKey1.get(),None)

    def cConfig(self):
        ui_log.debug("UI","module config get")
        client_lmp.command_local_config_get()

    def cReset(self):
        ui_log.debug("UI","module reset required")
        client_lmp.command_local_reset()

    def cUnregister(self):
        ui_log.debug("UI","module unregister")
        client_lmp.command_local_unregister()

    def cDiscover(self):
        ui_log.debug("UI","module unregister")
        client_lmp.command_remote_module_info()

class ModulesFrame():
    def __init__(self,widget):
        self.ui_modules = []
        self.widget = widget

    def get(self,uid):
        for ui_module in self.ui_modules :
            if ui_module.uid == uid:
                return ui_module
        # no module, create it
        ui_module = ModuleFrame(self.widget, uid)
        self.ui_modules.append(ui_module)
        ui_log.info("UI","new ui module %s"%(uid))
        return ui_module

class ModuleFrame():
    def __init__(self, widget, uid):
        self.uid = uid
        self.widget = widget
        self.ui_devices = []
        module = client_lmp.module_get(self.uid)
        module_title = "%s / %04X"%(self.uid, module.lmp_addr)
        self.fModule = LabelFrame(widget,text=module_title,borderwidth=2,relief=GROOVE)
        self.fModule.pack(fill=BOTH, expand=False,side=TOP,padx=2,pady=2)
        self.fModuleRole = Frame(self.fModule,borderwidth=1)
        self.fModuleRole.pack(fill=BOTH, expand=False,side=TOP,padx=5,pady=5)
        #self.pLMPAddr = Param(self.fModule,"LMP addr",TOP,5,"")
        self.pRole = Param(self.fModuleRole,"Role",LEFT,8,"")
        self.pTimestamp = Param(self.fModuleRole,"last time",LEFT,8,"")
        self.fModule2 = Frame(self.fModule,borderwidth=1) #, relief=SUNKEN
        self.fModule2.pack(fill=BOTH, expand=False, side=TOP )
        self.pRssi = Param(self.fModule2,"RSSI",LEFT,8,"")
        self.pBattery = Param(self.fModule2,"Battery",LEFT,8,"")
        #self.fDevices = LabelFrame(self.fModule,text="devices",borderwidth=2,relief=SUNKEN)
        #self.fDevices.pack(fill=BOTH, expand=False,side=TOP,padx=2,pady=2)

    def ui_device_get(self,device_id):
        for ui_device in self.ui_devices:
            if ui_device.device_id == device_id:
                return ui_device
        # no module, create it
        ui_device = DeviceFrame(self.fModule, self.uid, device_id)
        self.ui_devices.append(ui_device)
        ui_log.info("UI","new ui device %s/%d"%(ui_device.device.module.uid,device_id))
        return ui_device

class DeviceFrame():
    def __init__(self, widget, module_uid, device_id):
        self.module_uid = module_uid
        self.device_id = device_id
        self.device = client_lmp.device_get(module_uid,device_id)
        if self.device :
            device_title = "device %d : %s (%s)"%(device_id,self.device.name,self.device.type_str())
        else :
            device_title = "device %d"%(device_id)
        self.fDevice = LabelFrame(widget,text=device_title,borderwidth=2,relief=SUNKEN)
        self.fDevice.pack(fill=BOTH, expand=False,side=TOP,padx=5,pady=5)
        #self.pName = Param(self.fDevice,"Name",TOP,9,"")
        #self.pType = Param(self.fDevice,"Type",TOP,20,"")

        self.fDeviceEdit = DeviceEdit(self.fDevice,self.module_uid,self.device_id)

class DeviceEdit(DeviceFrame):
    def __init__(self, widget, module_uid, device_id):
        self.widget = widget
        self.module_uid = module_uid
        self.device_id = device_id
        self.fDeviceLine = Frame(self.widget,borderwidth=1)
        self.fDeviceLine.pack(fill=BOTH, expand=False,side=TOP,padx=5,pady=5)
        self.pData = Param(self.fDeviceLine,"Data",LEFT,30,"")
        self.bEdit = Button(self.fDeviceLine, text = "Edit", width=12, command = self.open)
        self.bEdit.pack(side=LEFT,padx=10,pady=1)
        self.ui_devices_dict = {
        DEVICE_TYPE_BINARY_SENSOR: {
            'param':self.param_device_unknown,
            'command': self.send_device_unknown,
            'data':self.data_update_device_binary_sensor
            },
        DEVICE_TYPE_BINARY_OUTPUT: {
            'param':self.param_device_binary_output,
            'command': self.send_device_binary_output,
            'data':self.data_update_device_binary_output
            },
        DEVICE_TYPE_LEVEL_OUTPUT: {
            'param':self.param_device_level_output,
            'command': self.send_device_level_output,
            'data':self.data_update_device_level_output
            },
        DEVICE_TYPE_COLOR_DIMMABLE_LIGHT: {
            'param':self.param_device_color_dimmable_light,
            'command': self.send_device_color_dimmable_light,
            'data':self.data_update_device_color_dimmable_light
            },
        DEVICE_TYPE_COLOR_WHITE_DIMMABLE_LIGHT: {
            'param':self.param_device_color_white_dimmable_light,
            'command': self.send_device_color_white_dimmable_light,
            'data':self.data_update_device_color_white_dimmable_light
            },
        DEVICE_TYPE_ANALOG_SENSOR: {
            'param':self.param_device_unknown,
            'command': self.send_device_unknown,
            'data':self.data_update_device_analog_sensor
            },
        DEVICE_TYPE_TEMPERATURE_SENSOR: {
            'param':self.param_device_unknown,
            'command': self.send_device_unknown,
            'data':self.data_update_device_temperature
            },
        DEVICE_TYPE_UNKNOWN: {
            'param':self.param_device_unknown,
            'command': self.send_device_unknown,
            'data':self.data_update_device_unknown
            }
        }
        self.ui_device_unknown = {
            'param':self.param_device_unknown,
            'command': self.send_device_unknown,
            'data':self.data_update_device_unknown
            }

    def send_device_color_dimmable_light(self):
        hexdata = self.pMode.get_hexstr4()+self.pAction.get_hexstr4()
        hexdata = hexdata+self.pLevel.get_hexstr8()+self.pHue.get_hexstr16()+self.pSaturation.get_hexstr8()
        hexdata = hexdata+self.pParam.get_hexstr16()
        device_data = string_to_array(hexdata)
        client_lmp.command_lmp_device_data_set(self.module_uid,self.device_id,device_data)

    def param_device_color_dimmable_light(self,widget):
        self.pAction = Param(widget,"OnOff [0,1]",TOP,1,"1")
        self.pMode = Param(widget,"Mode [0,6]",TOP,1,"1")
        self.pLevel = Param(widget,"Value [0,100]",TOP,3,"100")
        self.pHue = Param(widget,"Hue [0,360]",TOP,3,"0")
        self.pSaturation = Param(widget,"Saturation [0,100]",TOP,3,"100")
        self.pParam = Param(widget,"Time [0,65535]",TOP,5,"50")

    def data_update_device_color_dimmable_light(self,data):
        self.pData.set(binstr_to_hexstr(data))

    def send_device_color_white_dimmable_light(self):
        hexdata = self.pMode.get_hexstr4()+self.pAction.get_hexstr4()
        hexdata = hexdata+self.pLevel.get_hexstr8()+self.pHue.get_hexstr16()+self.pSaturation.get_hexstr8()
        hexdata = hexdata+self.pParam.get_hexstr16()+self.pWhite.get_hexstr8()
        device_data = string_to_array(hexdata)
        client_lmp.command_lmp_device_data_set(self.module_uid,self.device_id,device_data)

    def param_device_color_white_dimmable_light(self,widget):
        self.pAction = Param(widget,"OnOff [0,1]",TOP,1,"1")
        self.pMode = Param(widget,"Mode [0,6]",TOP,1,"1")
        self.pLevel = Param(widget,"Value [0,100]",TOP,3,"100")
        self.pHue = Param(widget,"Hue [0,360]",TOP,3,"0")
        self.pSaturation = Param(widget,"Saturation [0,100]",TOP,3,"100")
        self.pWhite = Param(widget,"White [0,100]",TOP,3,"0")
        self.pParam = Param(widget,"Time [0,65535]",TOP,5,"50")

    def data_update_device_color_white_dimmable_light(self,data):
        self.pData.set(binstr_to_hexstr(data))

    def send_device_unknown(self):
        ui_log.debug("UI","send")
        device_data = string_to_array(self.pData.get())
        client_lmp.command_lmp_device_data_set(self.module_uid,self.device_id,device_data)

    def param_device_unknown(self,widget):
        #self.pData = Param(widget,"Data",TOP,40,"")
        pass

    def data_update_device_unknown(self,data):
        ui_log.debug("UI","data_update_device_unknown %s"%(binstr_to_hexstr(data)))
        self.pData.set(binstr_to_hexstr(data))

    def data_update_device_binary_sensor(self,data):
        # parse binary_sensor data
        ui_log.debug("UI","data_update_device_binary_sensor %s"%(binstr_to_hexstr(data)))
        timestamp,status,value = unpack('<IBB', data)
        ui_log.debug("UI","=> at %d status=%d, value=%d"%(timestamp,status,value))
        data_str = "%s input=%d"%(timestamp_str_hour(timestamp),value)
        self.pData.set(data_str)

    def data_update_device_analog_sensor(self,data):
        # parse analog_sensor data
        ui_log.debug("UI","data_update_device_analog_sensor %s"%(binstr_to_hexstr(data)))
        timestamp,status,value = unpack('<IBI', data)
        ui_log.debug("UI","=> at %d status=%d, value=%d"%(timestamp,status,value))
        data_str = "%s analog=%d"%(timestamp_str_hour(timestamp),value)
        self.pData.set(data_str)

    def data_update_device_temperature(self,data):
        # parse temperature data
        ui_log.debug("UI","data_update_device_temperature %s"%(binstr_to_hexstr(data)))
        timestamp,status,value = unpack('<IBI', data)
        ui_log.debug("UI","=> at %d status=%d, value=%d"%(timestamp,status,value))
        data_str = "%s temp=%2.2f°C"%(timestamp_str_hour(timestamp),value/100)
        self.pData.set(data_str)

    def data_update_device_binary_output(self,data):
        # parse binary_output data
        ui_log.debug("UI","data_update_device_binary_output %s"%(binstr_to_hexstr(data)))
        timestamp,status,value = unpack('<IBB', data)
        ui_log.debug("UI","=> at %d status=%d, value=%d"%(timestamp,status,value))
        data_str = "%s output=%d"%(timestamp_str_hour(timestamp),value)
        self.pData.set(data_str)

    def send_device_binary_output(self):
        hexdata = self.pAction.get_hexstr8()
        device_data = string_to_array(hexdata)
        client_lmp.command_lmp_device_data_set(self.module_uid,self.device_id,device_data)

    def param_device_binary_output(self,widget):
        self.pAction = Param(widget,"OnOff [0,1]",TOP,1,"1")

    def data_update_device_level_output(self,data):
        # parse level_output data
        ui_log.debug("UI","data_update_device_level_output %s"%(binstr_to_hexstr(data)))
        timestamp,status,value = unpack('<IBB', data)
        ui_log.debug("UI","=> at %d status=%d, value=%d"%(timestamp,status,value))
        data_str = "%s output=%d"%(timestamp_str_hour(timestamp),value)
        self.pData.set(data_str)

    def send_device_level_output(self):
        hexdata = self.pAction.get_hexstr8()
        hexdata = hexdata+self.pLevel.get_hexstr8()
        device_data = string_to_array(hexdata)
        client_lmp.command_lmp_device_data_set(self.module_uid,self.device_id,device_data)

    def param_device_level_output(self,widget):
        self.pAction = Param(widget,"OnOff [0,1]",TOP,1,"1")
        self.pLevel = Param(widget,"Value [0,100]",TOP,3,"100")

    def param_func(self,widget):
        type_id = client_lmp.device_get(self.module_uid,self.device_id).type_id
        return self.ui_devices_dict.get(type_id,self.ui_device_unknown)['param'](widget)

    def command_func(self):
        type_id = client_lmp.device_get(self.module_uid,self.device_id).type_id
        self.ui_devices_dict.get(type_id,self.ui_device_unknown)['command']()

    def data_update(self,data):
        if data:
            #ui_log.debug("UI","data_update %s"%(binstr_to_hexstr(data)))
            type_id = client_lmp.device_get(self.module_uid,self.device_id).type_id
            self.ui_devices_dict.get(type_id,self.ui_device_unknown)['data'](data)


    def open(self):
        #fDevice = Toplevel()
        fDevice = self.widget
        ui_log.debug("UI","edit id=%s/%d"%(self.module_uid,self.device_id))
        self.bEdit.destroy()
        #self.fDeviceEdit = LabelFrame(self.widget,text="device edit %d"%(self.device_id),borderwidth=2,relief=SUNKEN)
        self.fDeviceEdit = Frame(fDevice,borderwidth=1)
        self.fDeviceEdit.pack(fill=BOTH, expand=False,side=TOP,padx=5,pady=5)
        self.fDeviceEditLeft = Frame(self.fDeviceEdit,borderwidth=1)
        self.fDeviceEditLeft.pack(fill=BOTH, expand=False, side=LEFT )
        self.fDeviceEditRight = Frame(self.fDeviceEdit,borderwidth=1)
        self.fDeviceEditRight.pack(fill=BOTH, expand=False, side=LEFT )

        self.param_func(self.fDeviceEditLeft)
        self.bSend = Button(self.fDeviceEditRight, text = "Send", width=12, command = self.command_func)
        self.bSend.pack(side=TOP,padx=10,pady=1)

        self.bClose = Button(self.fDeviceLine, text = "Close", width=12, command = self.close)
        self.bClose.pack(side=LEFT,padx=10,pady=1)

    def close(self):
        self.fDeviceEdit.destroy()
        self.bClose.destroy()
        self.bEdit = Button(self.fDeviceLine, text = "Edit", width=12, command = self.open)
        self.bEdit.pack(side=LEFT,padx=10,pady=1)

quit_req = False

def on_closing():
    print("close")

def on_module_open(ui_item):
    """ Called when module open button in list is clicked.
    """
    if ui_item.window_opened == False:
        print("module %s open"%(ui_item.uid))
        wModule = Toplevel()
        wModule.title("Module %s"%(ui_item.uid))
        wModule.protocol("WM_DELETE_WINDOW", wModule.iconify)
        ui_item.window = ModuleFrame(wModule, ui_item.uid)
        ui_item.window_opened = True
        # update fields
        module = client_lmp.module_get(ui_item.uid)
        ui_item.window.pTimestamp.set(timestamp_str_hour(module.timestamp))
        ui_item.window.pRole.set(module.role_str())
        ui_item.window.pRssi.set("%d dBm"%(module.rssi))
        ui_item.window.pBattery.set(module.battery_str())

        for device in module.devices :
            ui_log.debug("UI","device %d %s"%(device.id,device.name))
            ui_device = ui_item.window.ui_device_get(device.id)
            #ui_device.pName.set(device.name)
            #ui_device.pType.set(device.type_str())
            ui_device.fDeviceEdit.data_update(device.data)


def on_registered(updated_module):
    ui_log.debug("UI","module %s registered"%(updated_module.uid))

def on_unregistered(updated_module):
    ui_log.debug("UI","module %s unregistered"%(updated_module.uid))

def on_module_update(updated_module):
    ui_log.debug("UI","module %s update"%(updated_module.uid))
    # clean frame...
    #for widget in fRemote.winfo_children():
    #    widget.destroy()
    #ui_module = ui_remote_modules.get(updated_module.uid)

    ui_item = ui_list_remote_modules.get(updated_module.uid,on_module_open)
    ui_item.text.set("%04X %12s %8s %8sdBm"%
        (updated_module.lmp_addr,
        timestamp_str_hour(updated_module.timestamp),
        updated_module.role_str(),updated_module.rssi))
    if ui_item.window :
        #ui_module.pLMPAddr.set("%04X"%(updated_module.lmp_addr))
        ui_item.window.pTimestamp.set(timestamp_str_hour(updated_module.timestamp))
        ui_item.window.pRole.set(updated_module.role_str())
        ui_item.window.pRssi.set("%d dBm"%(updated_module.rssi))
        ui_item.window.pBattery.set(updated_module.battery_str())

        for device in updated_module.devices :
            ui_log.debug("UI","device %d %s"%(device.id,device.name))
            ui_device = ui_item.window.ui_device_get(device.id)
            #ui_device.pName.set(device.name)
            #ui_device.pType.set(device.type_str())
            ui_device.fDeviceEdit.data_update(device.data)

def on_device_data_event(module, device, frame):
    ui_log.debug("UI","on_device_data_event module=%s device_id=%d data=%s"%(module.uid,device.id,debughex(frame)))
    ui_item = ui_list_remote_modules.get(module.uid,on_module_open)
    if ui_item.window :
        #ui_module = ui_remote_modules.get(module.uid)
        ui_device = ui_item.window.ui_device_get(device.id)
        ui_device.fDeviceEdit.data_update(device.data)

def on_device_data_status(module, device, frame):
    ui_log.debug("UI","on_device_data_status module=%s device_id=%d data=%s"%(module.uid,device.id,debughex(frame)))
    ui_item = ui_list_remote_modules.get(module.uid,on_module_open)
    if ui_item.window :
        #ui_module = ui_remote_modules.get(module.uid)
        ui_device = ui_item.window.ui_device_get(device.id)
        ui_device.fDeviceEdit.data_update(device.data)

def on_app_ready() :
    """ Build the main page. Get the current mode first. """
    ui_log.debug("UI","on_app_ready")


def on_quit():
    global quit_req
    quit_req = True

def ui_local_module_update(local_module):
    ui_log.debug("UI","ui_local_module_update")
    print("\tlmp_addr = %04X"%(local_module.lmp_addr))
    print("\tmac_addr = %s"%(local_module.uid))
    print("\ttype_id = %d"%(local_module.type_id))
    print("\tsw_version = %s"%(local_module.sw_version))
    print("\tmanufacturer = %s"%(local_module.manufacturer))
    print("\tmodel = %s"%(local_module.model))
    print("\tname = %s"%(local_module.name))
    #serial_central_connect("C6:31:61:AF:9C:E2",on_app_ready,on_quit)
    ui_local_module.uid = local_module.uid
    ui_local_module.pMac.set(local_module.uid)
    ui_local_module.pLMPAddr.set("%04X"%(local_module.lmp_addr))
    ui_local_module.pManufacturer.set(local_module.manufacturer)
    ui_local_module.pModel.set(local_module.model)
    ui_local_module.pName.set(local_module.name)
    ui_local_module.pSWVersion.set(local_module.sw_version)
    ui_local_module.pHWVersion.set(local_module.hw_version)
    ui_local_module.pType.set(local_module.type_str())
    ui_local_module.pRole.set(local_module.role_str())
    ui_local_module.pReg.set(local_module.registered)
    #ui_local_module.pEnc.set(local_module.encryption)
    for device in local_module.devices :
        ui_log.debug("UI","device %d %s"%(device.id,device.name))
        ui_device = ui_local_module.ui_device_get(device.id)
        ui_device.fDeviceEdit.data_update(device.data)

    if ui_local_module.fRegistration_opened :
        ui_local_module.pEnc.set(local_module.encryption)
        ui_local_module.pNonce.set(binstr_to_hexstr(local_module.crypt_nonce))
        ui_local_module.pKey0.set(binstr_to_hexstr(local_module.crypt_key0))
        ui_local_module.pKey1.set(binstr_to_hexstr(local_module.crypt_key1))

def on_init_complete(status):

    print("on_init_complete")
    local_module = client_lmp.local_module()
    ui_local_module_update(local_module)

def on_local_module_update(local_module):

    print("on_local_module_update")
    ui_local_module_update(local_module)


if __name__ == "__main__":
    """
    if permission error when start, use
    sudo usermod -a -G dialout $USER
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-D', action='store',
                        default="/dev/ttyUSB0",
                        dest='serial_device',
                        help='serial device')

    presults = parser.parse_args()
    print 'serial_device =', presults.serial_device
    # init serial port

    root = Tk()
    root.wm_title("Linkio Mesh Controller")

    ui_log = UILog()

    fRemote = LabelFrame(root,text="Remote modules",borderwidth=2,relief=GROOVE)
    fRemote.pack(fill="both", expand=False,side=RIGHT,padx=2,pady=2)

    #sFrame = VerticalScrolledFrame(fRemote)
    #sFrame.pack(fill="both", expand=False,side=RIGHT)
    #ui_remote_modules = ModulesFrame(sFrame.interior)

    ui_local_module = LocalModuleFrame(root,"Local module")
    #ui_remote_modules = ModulesFrame(fRemote)
    ui_list_remote_modules = ItemsList(fRemote)

    client_lmp = Lmp(presults.serial_device)
    # define callbacks
    client_lmp.on_registered(on_registered)
    client_lmp.on_unregistered(on_unregistered)
    client_lmp.on_local_module_update(on_local_module_update)
    client_lmp.on_module_update(on_module_update)
    client_lmp.on_device_data_event_ind(on_device_data_event)
    client_lmp.on_device_data_status_ind(on_device_data_status)
    client_lmp.init(on_init_complete)
    client_lmp.command_remote_module_info()

    root.mainloop()
