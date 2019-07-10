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
__copyright__   = "Copyright 2019, Linkio SAS"
__version__     = "1.0.0"
__status__      = "Development"

import argparse
import os,sys

root_dir = os.path.dirname(os.path.abspath(__file__))
libpath = os.path.join(root_dir, 'python-libs')
sys.path.append(libpath)

from lmp.lmpserial import LmpSerial, Lmp
from lmp.utils import debughex
from lmp.utils import string_to_array
import time
import logging

quit_req = False
mqtt_client = None
local_module = None
remote_modules = []

def on_registered(updated_module):
    logging.debug("module %s registered"%(updated_module.uid))

def on_unregistered(updated_module):
    logging.debug("module %s unregistered"%(updated_module.uid))

def on_remote_module_update(updated_module):
    global remote_modules
    if updated_module.uid not in remote_modules:
        remote_modules.append( updated_module.uid)

    logging.debug("module %s update"%(updated_module.uid))

def on_device_data_event(module, device, frame):
    logging.debug("on_device_data_event module=%s device_id=%d data=%s"%(module.uid,device.id,debughex(frame)))

def on_device_data_status(module, device, frame):
    logging.debug("on_device_data_status module=%s device_id=%d data=%s"%(module.uid,device.id,debughex(frame)))

def on_local_device_property_get(status):
    logging.debug("on_local_device_property_get")

def on_quit():
    global quit_req
    quit_req = True

def on_init_complete(status):
    global local_module
    local_module = client_lmp.local_module()

    logging.debug("on_init_complete status:%d"%(status))

    logging.debug("\tlmp_addr = %04X"%(local_module.lmp_addr))
    logging.debug("\tmac_addr = %s"%(local_module.uid))
    logging.debug("\ttype_id = %d"%(local_module.type_id))
    logging.debug("\tsw_version = %s"%(local_module.sw_version))
    logging.debug("\tmanufacturer = '%s'"%(local_module.manufacturer))
    logging.debug("\tmodel = '%s'"%(local_module.model))
    logging.debug("\tname = '%s'"%(local_module.name))

    client_lmp.command_remote_module_info()

def on_local_module_update(local_module):

    logging.debug("on_local_module_update")

    logging.debug("\tlmp_addr = %04X"%(local_module.lmp_addr))
    logging.debug("\tmac_addr = %s"%(local_module.uid))
    logging.debug("\ttype_id = %d"%(local_module.type_id))
    logging.debug("\tsw_version = %s"%(local_module.sw_version))
    logging.debug("\tmanufacturer = '%s'"%(local_module.manufacturer))
    logging.debug("\tmodel = '%s'"%(local_module.model))
    logging.debug("\tname = '%s'"%(local_module.name))


def on_peripheral_connected():
    logging.debug("Connected")

def on_peripheral_disconnected():
    logging.debug("Disconnected")

def on_host_msg_update(frame):
    logging.debug("on_host_msg_update data=%s"%(binstr_to_hexstr(frame)))

def on_local_debug_update(level,log):
    logging.debug("Debug[%d] %s"%(level,log))


if __name__ == "__main__":
    """
    if permission error when start, use
    sudo usermod -a -G dialout $USER
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-D', action='store',
                        default="/dev/ttyUSB0",
                        dest='serial_device',
                        help='Serial device')
    parser.add_argument('-o', action='store',
                        dest='file',
                        default='log.txt',
                        help='Output file')

    presults = parser.parse_args()
    logging.basicConfig(filename=presults.file,
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.DEBUG )
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    logging.debug("serial_device =%s"%(presults.serial_device))
    # init serial port

    client_lmp = Lmp(presults.serial_device)
    # define callbacks
    client_lmp.on_registered(on_registered)
    client_lmp.on_unregistered(on_unregistered)
    client_lmp.on_local_module_update(on_local_module_update)
    client_lmp.on_module_update(on_remote_module_update)
    client_lmp.on_device_data_event_ind(on_device_data_event)
    client_lmp.on_device_data_status_ind(on_device_data_status)
    client_lmp.init(on_init_complete, debug=False)
    #client_lmp.command_remote_module_info()
    client_lmp.on_peripheral_connected(on_peripheral_connected)
    client_lmp.on_peripheral_disconnected(on_peripheral_disconnected)
    client_lmp.on_host_msg_update(on_host_msg_update)
    client_lmp.on_local_debug_ind(on_local_debug_update)


    #global remote_modules

    stop = False
    onoff = 0
    actions = ["0","1"]
    while (stop == False):
        time.sleep(5)
        # build light data (toggle on off) for detected modules
        for module_uid in remote_modules:
            hexdata = "1" # Mode
            hexdata = hexdata + actions[onoff] # Action : toggle
            hexdata = hexdata + "63" # Value
            hexdata = hexdata + "0000" # Hue
            hexdata = hexdata + "63" # Saturation
            hexdata = hexdata + "0100" # param/time
            hexdata = hexdata + "00" # White
            device_data = string_to_array(hexdata)
            # write on device 0
            client_lmp.command_remote_device_data_set(module_uid,0,device_data)
        onoff = 1 - onoff
