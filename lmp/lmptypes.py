"""
    Copyright (c) 2016-2018 - Linkio SAS. All Rights Reserved.

    All information contained herein is, and remains the property of
    Linkio SAS.
    The intellectual and technical concepts contained herein are
    proprietary to Linkio SAS.
    Dissemination of this information or reproduction of this material
    is strictly forbidden unless prior written permission is obtained
    from Linkio SAS.

    Linkio serial console.
    LMP commands and events.
"""
LMP_ERR_SUCCESS = 0
LMP_ERR_NOT_SUPPORTED = 1
LMP_ERR_INVALID_COMMAND = 2
LMP_ERR_INVALID_PARAMETER = 3
LMP_ERR_INVALID_DEVICE = 4
LMP_ERR_UNREGISTERED = 5
LMP_ERR_CLEAR_MSG_UNAUTHORIZED = 6
LMP_ERR_CRYPT_MSG = 7
LMP_ERR_TIMEOUT = 8
LMP_ERR_CONNECT_ERROR = 9
LMP_ERR_MEMORY_FAIL = 10
LMP_ERR_MEMORY_FULL = 11
LMP_ERR_INVALID_SIZE = 12
LMP_ERR_ITEM_NOT_FOUND = 20

lmp_errors_list = [
'ERR_SUCCESS' ,
'ERR_NOT_SUPPORTED' ,
'ERR_INVALID_COMMAND' ,
'ERR_INVALID_PARAMETER' ,
'ERR_INVALID_DEVICE' ,
'ERR_UNREGISTERED' ,
'ERR_CLEAR_MSG_UNAUTHORIZED' ,
'ERR_CRYPT_MSG' ,
'ERR_TIMEOUT' ,
'ERR_CONNECT_ERROR' ,
'ERR_MEMORY_FAIL' ,
'ERR_MEMORY_FULL' ,
'ERR_INVALID_SIZE' ,
'','','','','','','',
'ERR_ITEM_NOT_FOUND' ,
]

lmp_roles_str_dict = {
    0:'NODE',
    1:'GTWAY',
    2:'CONB',
    3:'GW_BR',
    4:'BRCTR',
    5:'MASTR',
    6:'LEAF',
    7:'BEACN'
}


LMP_COMMAND_DEVICE_DATA_SET = 0x41 #Set new device data
LMP_STATUS_NETWORK = 0x82 # Network status */
LMP_STATUS_DEVICE_INFO = 0x91 # Device info status change */
LMP_EVENT_DEVICE_DATA = 0x92 # New device data event */
LMP_STATUS_DEVICE_DATA = 0x93 # Device data status change */
LMP_PARAM_MAC_ADDRESS = 0xB0 # MAC address parameter */
LMP_PARAM_SHORT_ADDRESS = 0xB1 # LMP short address parameter */
LMP_PARAM_MANUFACTURER_NAME = 0xB2 # Module manufacturer name */
LMP_PARAM_MODEL_NAME = 0xB3 # Module model name */
LMP_PARAM_MODULE_TYPE = 0xB4 # Module type */
LMP_PARAM_MODULE_SW_VERSION = 0xB5 # Module software version */
LMP_PARAM_MODULE_HW_VERSION = 0xB6 # Module hardware version */
LMP_PARAM_MODULE_NAME = 0xB7 # Module user name */
LMP_PARAM_MODULE_API_VERSION = 0xB8 # Module API version */
LMP_PARAM_BATTERY_LEVEL = 0xC0 # Battery level parameter */
LMP_PARAM_ROLE = 0xC1 # Module role */
LMP_PARAM_RSSI = 0xC2 # Module RSSI */
LMP_PARAM_CONFIG_STRUCT = 0xCA # Module configuration structure parameter */



LEDS_MODE_INIT = 0
LEDS_MODE_COLOR=1
LEDS_MODE_COLOR_FADE=2
LEDS_MODE_COLOR_RAINBOW=3
LEDS_MODE_COLOR_CANDLE=4
LEDS_MODE_COLOR_BLINK=5
LEDS_MODE_NOTIFICATION=6
