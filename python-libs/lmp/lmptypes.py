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

LMP_ROLE_NODE=0x0
LMP_ROLE_GATEWAY=0x1
LMP_ROLE_CONNECTABLE=0x2
LMP_ROLE_GATEWAY_BROADCASTER=0x3
LMP_ROLE_BROADCASTER=0x4
LMP_ROLE_MASTER=0x5
LMP_ROLE_LEAF=0x6
LMP_ROLE_BEACON=0x7

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

LMP_PACKET_TYPE_CMD_NOACK=0x0
LMP_PACKET_TYPE_CMD_ACK=0x1
LMP_PACKET_TYPE_ACK=0x2
LMP_PACKET_TYPE_STATUS=0x3
LMP_PACKET_TYPE_EVENT=0x4

LMP_COMMAND_DEVICE_DATA_SET = 0x41 #Set new device data

LMP_STATUS_ACK = 0x80 # Acknowledge status */
LMP_STATUS_NETWORK = 0x82 # Network status */
LMP_STATUS_DEVICE_INFO = 0x91 # Device info status change */
LMP_EVENT_DEVICE_DATA = 0x92 # New device data event */
LMP_STATUS_DEVICE_DATA = 0x93 # Device data status change */
LMP_PARAM_MODULE_REFERENCE = 0xAF # Module Linkio full reference */
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
