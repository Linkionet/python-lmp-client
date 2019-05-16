"""
    Copyright (c) 2016-2018 - Linkio SAS. All Rights Reserved.

    All information contained herein is, and remains the property of
    Linkio SAS.
    The intellectual and technical concepts contained herein are
    proprietary to Linkio SAS.
    Dissemination of this information or reproduction of this material
    is strictly forbidden unless prior written permission is obtained
    from Linkio SAS.

    Utility functions.
"""

import time
from struct import *

def fcs_calc(payload):
    result = 0
    for cr in payload[1:]:
        result ^= cr
    return result

def timestamp_now():
    return time.localtime()

def timestamp_ticks_now():
    return int(time.time())

def timestamp_str( timestamp ):
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timestamp))

def timestamp_str_hour( timestamp ):
    return time.strftime("%H:%M:%S",time.localtime(timestamp))

def debughex(frame_str):
    #larray = [c.encode("hex") for c in frame_str]
    larray = ["%02X"%(c) for c in frame_str]
    sarray = ' '.join(larray)
    return "[%d]=%s"%(len(frame_str),sarray)

def debughex2(frame_str):
    larray = ["%02X"%(c) for c in frame_str]
    sarray = ' '.join(larray)
    return "[%d]=%s"%(len(frame_str),sarray)

def string_to_array(hexstr):
    """
        Return list of bytes from variable hex string ('0102...0F')
    """
    lhex = []
    while len(hexstr)>1:
        substr = hexstr[0:2]
        hexstr = hexstr[2:]
        lhex.append(int(substr,16))
    #print lhex
    return lhex

def hexstr_to_u16_array(hexstr):
    s= string_to_array(hexstr)
    return s[::-1] # little endian

def binstr_to_hexstr(frame_str):
    if frame_str:
        larray = [c.encode("hex") for c in frame_str]
        sarray = ''.join(larray)
        return sarray
    return ""

def val_to_hexstr(val):
    return "%04X"%(val)

def u8_to_array(val):
    lval=[val]
    #data = map(ord,pack("<B",*lval))
    #return data
    r = []
    for i in pack("<B",*lval):
        r.append(i)
    return r


def u16_to_array(val):
    lval=[val]
    data = pack("<H",*lval)
    r = []
    for i in data:
        #print(i)
        r.append(i)
    #data = map(ord,pack("<H",*lval))
    #print(r)
    return r

def u32_to_array(val):
    lval=[val]
    data = map(ord,pack("<I",*lval))
    return data

def lmpaddr_to_array(addr):
    laddr = string_to_array(addr)
    return laddr[::-1]

def mac_to_array(mac):
    """
        Return list of bytes.
        mac in format E0:01:49:9D:08:D6
    """
    st = mac.split(":")
    lmac = [int(hex,16) for hex in st]
    return lmac[::-1] # reverse array as expected for mac parameter

def array_to_u16(array):
    """ little endian style
    """
    return (array[0] + array[1]*256)

def array_to_str(array):
    na = []
    for e in array:
        if e != 0:
            na.append(e)
        else :
            break
    return ''.join(chr(e) for e in na)

def array_to_signed(val):
    if val<127:
        return val
    else :
        return val-255

def array_to_u32(array):
    """ little endian style
    """
    return ( array[0] + array[1]*256  + array[2]*256*256  + array[3]*256*256*256 )
