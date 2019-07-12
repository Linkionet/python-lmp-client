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
    serial commands and events.
"""

SERIAL_CMD_LOCAL_VERSION_GET = 0x0000 # Request software version.
SERIAL_CMD_LOCAL_RESET = 0x0001 # Request a software reset.
SERIAL_CMD_LOCAL_FACTORY_RESET = 0x0002 # Request a factory reset.
SERIAL_CMD_LOCAL_CONFIG_STRUCT_GET = 0x0003 #
SERIAL_CMD_LOCAL_CONFIG_DATA_GET = 0x0004 #
SERIAL_CMD_LOCAL_CONFIG_DATA_SET = 0x0005 #
SERIAL_CMD_LOCAL_FACTORY_DATA_GET = 0x0006 # Get Factory FDS data.
SERIAL_CMD_LOCAL_FACTORY_DATA_SET = 0x0007 # Save Factory FDS data.
SERIAL_CMD_CENTRAL_CONNECT = 0x0010 #
SERIAL_CMD_CENTRAL_DISCONNECT = 0x0011 #
SERIAL_CMD_CENTRAL_LMS_SEND = 0x0020 #
SERIAL_CMD_LOCAL_LMP_SEND = 0x0021 #
SERIAL_CMD_LOCAL_ROLE_SET = 0x0022 # Set MESH role
SERIAL_CMD_NETWORK_GET = 0x002B # Request module network information, repeated <count> times.
SERIAL_CMD_LOCAL_UNREGISTER = 0x0030 # Unregister from MESH network.
SERIAL_CMD_LOCAL_REGISTER = 0x0031 # Register to MESH network.
SERIAL_CMD_LOCAL_REGISTRATION_GET = 0x0032 # Return registration state.
SERIAL_CMD_LOCAL_CRYPT_NONCE_GENERATE = 0x0033 # Generate a nonce buffer.
SERIAL_CMD_LOCAL_CRYPT_NONCE_GET = 0x0034 # Get the stored nonce buffer.
SERIAL_CMD_LOCAL_CRYPT_NONCE_SET = 0x0035 # Set and store a nonce buffer.
SERIAL_CMD_LOCAL_CRYPT_AUTHKEY_GENERATE = 0x0036 # Generate an authentication key.
SERIAL_CMD_LOCAL_CRYPT_AUTHKEY_GET = 0x0037 # Get an authentication key.
SERIAL_CMD_LOCAL_CRYPT_AUTHKEY_SET = 0x0038 # Set an authentication key.
SERIAL_CMD_LOCAL_CRYPT_SET = 0x0039 # Set encryption (start/stop).
SERIAL_CMD_LOCAL_MODULE_INFO_GET = 0x0040 # Return module information
SERIAL_CMD_LOCAL_MODULE_INFO_SET = 0x0041 # Not implemented
SERIAL_CMD_LOCAL_MODULE_EVENT_SET = 0x0044 # Not implemented
SERIAL_CMD_LOCAL_MODULE_STATUS_SET = 0x0045 # Not implemented
SERIAL_CMD_LOCAL_MODULE_PROPERTY_GET = 0x0046 # Get a module property.
SERIAL_CMD_LOCAL_MODULE_PROPERTY_SET = 0x0047 # Set a module property.
SERIAL_CMD_LOCAL_MODULE_PROPERTY_DELETE = 0x0048 # Delete a module property.
SERIAL_CMD_LOCAL_DEVICES_INFO_GET = 0x0050 #
SERIAL_CMD_LOCAL_DEVICES_INFO_SET = 0x0051 #
SERIAL_CMD_LOCAL_DEVICE_INFO_ADD = 0x0052 #
SERIAL_CMD_LOCAL_DEVICE_INFO_DELETE = 0x0053 #
SERIAL_CMD_LOCAL_DEVICE_DATA_EVENT_SET = 0x0055 #
SERIAL_CMD_LOCAL_DEVICE_DATA_STATUS_SET = 0x0056 #
SERIAL_CMD_LOCAL_DEVICE_PROPERTY_GET = 0x0057 # Get a device property.
SERIAL_CMD_LOCAL_DEVICE_PROPERTY_SET = 0x0058 # Set a device property.
SERIAL_CMD_LOCAL_DEVICE_PROPERTY_DELETE = 0x0059 # Delete a device property.
SERIAL_CMD_LOCAL_GROUPS_GET = 0x0060 #
SERIAL_CMD_LOCAL_GROUPS_SET = 0x0061 #
SERIAL_CMD_LOCAL_RULES_GET = 0x0070 #
SERIAL_CMD_LOCAL_RULES_SET = 0x0071 #
SERIAL_CMD_LOCAL_DATETIME_GET = 0x0080 # Get the current local timestamp.
SERIAL_CMD_LOCAL_DATETIME_SET = 0x0081 # Set the current local timestamp.
SERIAL_CMD_REMOTE_ROLE_SET = 0x0122 # Set MESH role on remote module.
SERIAL_CMD_REMOTE_MODULE_INFO_GET = 0x0140 # Request the specified module information.
SERIAL_CMD_HOST_MSG_EVENT = 0x0146 #
SERIAL_CMD_HOST_PARAM_SET_ACK = 0x0147 # Return an acknowledge for a parameter set command to the terminal.
SERIAL_CMD_HOST_PARAM_GET_ACK = 0x0148 # Return an acknowledge for a parameter get command to the terminal.
SERIAL_CMD_HOST_PARAM_IND = 0x0149 # Notify a host parameter change.
SERIAL_CMD_REMOTE_DEVICE_INFO_GET = 0x0150 # Request a remote device info (LMP request).
SERIAL_CMD_REMOTE_DEVICE_DATA_SET = 0x0155 # Command a remote device.
SERIAL_CMD_REMOTE_GROUP_DATA_SET = 0x0256 # Command a remote group.
SERIAL_EVT_LOCAL_DEBUG_STR = 0x1000 # Return a debug string
SERIAL_EVT_LOCAL_CONNECT_IND = 0x1010 #
SERIAL_EVT_LOCAL_DISCONNECT_IND = 0x1011 #
SERIAL_EVT_LOCAL_UNREGISTER_IND = 0x1030 #
SERIAL_EVT_LOCAL_REGISTER_IND = 0x1031 #
SERIAL_EVT_LOCAL_IDENTIFICATION_REQ = 0x1035 #
SERIAL_EVT_HOST_MSG_IND = 0x1046 #
SERIAL_EVT_HOST_PARAM_SET_REQ = 0x1047 # Request a parameter set on the host
SERIAL_EVT_HOST_PARAM_GET_REQ = 0x1048 # Request a parameter get from the host
SERIAL_EVT_LOCAL_DEVICE_INFO_IND = 0x1050 # Notify a local device addition or deletion.
SERIAL_EVT_LOCAL_DEVICE_DATA_SET_IND = 0x1052 # Notify a device data set.
SERIAL_EVT_REMOTE_GROUP_DATA_SET_IND = 0x1062 # Notify a group data set.
SERIAL_EVT_LOCAL_DATETIME_IND = 0x1080 # Notify the current timestamp.
SERIAL_EVT_REMOTE_LMP_DATA_EVENT_IND = 0x1100 #
SERIAL_EVT_REMOTE_LMP_DATA_STATUS_IND = 0x1101 #
SERIAL_EVT_REMOTE_MODULE_INFO_IND = 0x1140 #
SERIAL_EVT_REMOTE_NETWORK_INFO_IND = 0x1141 # Returns the list of gateways seen from this module
SERIAL_EVT_REMOTE_BEACON_IND = 0x1145 # Indicate a beacon message.
SERIAL_EVT_REMOTE_MODULE_MSG_IND = 0x1146 #
SERIAL_EVT_REMOTE_DEVICE_INFO_IND = 0x1150 #
SERIAL_EVT_REMOTE_DEVICE_DATA_EVENT_IND = 0x1151 #
SERIAL_EVT_REMOTE_DEVICE_DATA_STATUS_IND = 0x1152 #
SERIAL_EVT_CENTRAL_CONNECTED_IND = 0x1310 #
SERIAL_EVT_CENTRAL_DISCONNECTED_IND = 0x1311#

serial_opcodes_str_dict = {
SERIAL_CMD_LOCAL_VERSION_GET : 'SERIAL_CMD_LOCAL_VERSION_GET',
SERIAL_CMD_LOCAL_RESET : 'SERIAL_CMD_LOCAL_RESET',
SERIAL_CMD_LOCAL_FACTORY_RESET : 'SERIAL_CMD_LOCAL_FACTORY_RESET',
SERIAL_CMD_LOCAL_CONFIG_STRUCT_GET : 'SERIAL_CMD_LOCAL_CONFIG_STRUCT_GET',
SERIAL_CMD_LOCAL_CONFIG_DATA_GET : 'SERIAL_CMD_LOCAL_CONFIG_DATA_GET',
SERIAL_CMD_LOCAL_CONFIG_DATA_SET : 'SERIAL_CMD_LOCAL_CONFIG_DATA_SET',
SERIAL_CMD_LOCAL_FACTORY_DATA_GET : 'SERIAL_CMD_LOCAL_FACTORY_DATA_GET',
SERIAL_CMD_LOCAL_FACTORY_DATA_SET : 'SERIAL_CMD_LOCAL_FACTORY_DATA_SET',
SERIAL_CMD_CENTRAL_CONNECT : 'SERIAL_CMD_CENTRAL_CONNECT',
SERIAL_CMD_CENTRAL_DISCONNECT : 'SERIAL_CMD_CENTRAL_DISCONNECT',
SERIAL_CMD_CENTRAL_LMS_SEND : 'SERIAL_CMD_CENTRAL_LMS_SEND',
SERIAL_CMD_LOCAL_LMP_SEND : 'SERIAL_CMD_LOCAL_LMP_SEND',
SERIAL_CMD_LOCAL_ROLE_SET : 'SERIAL_CMD_LOCAL_ROLE_SET',
SERIAL_CMD_NETWORK_GET : 'SERIAL_CMD_NETWORK_GET',
SERIAL_CMD_LOCAL_UNREGISTER : 'SERIAL_CMD_LOCAL_UNREGISTER',
SERIAL_CMD_LOCAL_REGISTER : 'SERIAL_CMD_LOCAL_REGISTER',
SERIAL_CMD_LOCAL_REGISTRATION_GET : 'SERIAL_CMD_LOCAL_REGISTRATION_GET',
SERIAL_CMD_LOCAL_CRYPT_NONCE_GENERATE : 'SERIAL_CMD_LOCAL_CRYPT_NONCE_GENERATE',
SERIAL_CMD_LOCAL_CRYPT_NONCE_GET : 'SERIAL_CMD_LOCAL_CRYPT_NONCE_GET',
SERIAL_CMD_LOCAL_CRYPT_NONCE_SET : 'SERIAL_CMD_LOCAL_CRYPT_NONCE_SET',
SERIAL_CMD_LOCAL_CRYPT_AUTHKEY_GENERATE : 'SERIAL_CMD_LOCAL_CRYPT_AUTHKEY_GENERATE',
SERIAL_CMD_LOCAL_CRYPT_AUTHKEY_GET : 'SERIAL_CMD_LOCAL_CRYPT_AUTHKEY_GET',
SERIAL_CMD_LOCAL_CRYPT_AUTHKEY_SET : 'SERIAL_CMD_LOCAL_CRYPT_AUTHKEY_SET',
SERIAL_CMD_LOCAL_CRYPT_SET : 'SERIAL_CMD_LOCAL_CRYPT_SET',
SERIAL_CMD_LOCAL_MODULE_INFO_GET : 'SERIAL_CMD_LOCAL_MODULE_INFO_GET',
SERIAL_CMD_LOCAL_MODULE_INFO_SET : 'SERIAL_CMD_LOCAL_MODULE_INFO_SET',
SERIAL_CMD_LOCAL_MODULE_EVENT_SET : 'SERIAL_CMD_LOCAL_MODULE_EVENT_SET',
SERIAL_CMD_LOCAL_MODULE_STATUS_SET : 'SERIAL_CMD_LOCAL_MODULE_STATUS_SET',
SERIAL_CMD_LOCAL_MODULE_PROPERTY_GET : 'SERIAL_CMD_LOCAL_MODULE_PROPERTY_GET',
SERIAL_CMD_LOCAL_MODULE_PROPERTY_SET : 'SERIAL_CMD_LOCAL_MODULE_PROPERTY_SET',
SERIAL_CMD_LOCAL_MODULE_PROPERTY_DELETE : 'SERIAL_CMD_LOCAL_MODULE_PROPERTY_DELETE',
SERIAL_CMD_LOCAL_DEVICES_INFO_GET : 'SERIAL_CMD_LOCAL_DEVICES_INFO_GET',
SERIAL_CMD_LOCAL_DEVICES_INFO_SET : 'SERIAL_CMD_LOCAL_DEVICES_INFO_SET',
SERIAL_CMD_LOCAL_DEVICE_INFO_ADD : 'SERIAL_CMD_LOCAL_DEVICE_INFO_ADD',
SERIAL_CMD_LOCAL_DEVICE_INFO_DELETE : 'SERIAL_CMD_LOCAL_DEVICE_INFO_DELETE',
SERIAL_CMD_LOCAL_DEVICE_DATA_EVENT_SET : 'SERIAL_CMD_LOCAL_DEVICE_DATA_EVENT_SET',
SERIAL_CMD_LOCAL_DEVICE_DATA_STATUS_SET : 'SERIAL_CMD_LOCAL_DEVICE_DATA_STATUS_SET',
SERIAL_CMD_LOCAL_DEVICE_PROPERTY_GET : 'SERIAL_CMD_LOCAL_DEVICE_PROPERTY_GET',
SERIAL_CMD_LOCAL_DEVICE_PROPERTY_SET : 'SERIAL_CMD_LOCAL_DEVICE_PROPERTY_SET',
SERIAL_CMD_LOCAL_DEVICE_PROPERTY_DELETE : 'SERIAL_CMD_LOCAL_DEVICE_PROPERTY_DELETE',
SERIAL_CMD_LOCAL_GROUPS_GET : 'SERIAL_CMD_LOCAL_GROUPS_GET',
SERIAL_CMD_LOCAL_GROUPS_SET : 'SERIAL_CMD_LOCAL_GROUPS_SET',
SERIAL_CMD_LOCAL_RULES_GET : 'SERIAL_CMD_LOCAL_RULES_GET',
SERIAL_CMD_LOCAL_RULES_SET : 'SERIAL_CMD_LOCAL_RULES_SET',
SERIAL_CMD_LOCAL_DATETIME_GET : 'SERIAL_CMD_LOCAL_DATETIME_GET',
SERIAL_CMD_LOCAL_DATETIME_SET : 'SERIAL_CMD_LOCAL_DATETIME_SET',
SERIAL_CMD_REMOTE_ROLE_SET : 'SERIAL_CMD_REMOTE_ROLE_SET',
SERIAL_CMD_REMOTE_MODULE_INFO_GET : 'SERIAL_CMD_REMOTE_MODULE_INFO_GET',
SERIAL_CMD_HOST_MSG_EVENT : 'SERIAL_CMD_HOST_MSG_EVENT',
SERIAL_CMD_HOST_PARAM_SET_ACK : 'SERIAL_CMD_HOST_PARAM_SET_ACK',
SERIAL_CMD_HOST_PARAM_GET_ACK : 'SERIAL_CMD_HOST_PARAM_GET_ACK',
SERIAL_CMD_HOST_PARAM_IND : 'SERIAL_CMD_HOST_PARAM_IND',
SERIAL_CMD_REMOTE_DEVICE_INFO_GET : 'SERIAL_CMD_REMOTE_DEVICE_INFO_GET',
SERIAL_CMD_REMOTE_DEVICE_DATA_SET : 'SERIAL_CMD_REMOTE_DEVICE_DATA_SET',
SERIAL_CMD_REMOTE_GROUP_DATA_SET : 'SERIAL_CMD_REMOTE_GROUP_DATA_SET',
SERIAL_EVT_LOCAL_DEBUG_STR : 'SERIAL_EVT_LOCAL_DEBUG_STR',
SERIAL_EVT_LOCAL_CONNECT_IND : 'SERIAL_EVT_LOCAL_CONNECT_IND',
SERIAL_EVT_LOCAL_DISCONNECT_IND : 'SERIAL_EVT_LOCAL_DISCONNECT_IND',
SERIAL_EVT_LOCAL_UNREGISTER_IND : 'SERIAL_EVT_LOCAL_UNREGISTER_IND',
SERIAL_EVT_LOCAL_REGISTER_IND : 'SERIAL_EVT_LOCAL_REGISTER_IND',
SERIAL_EVT_LOCAL_IDENTIFICATION_REQ : 'SERIAL_EVT_LOCAL_IDENTIFICATION_REQ',
SERIAL_EVT_HOST_MSG_IND : 'SERIAL_EVT_HOST_MSG_IND',
SERIAL_EVT_HOST_PARAM_SET_REQ : 'SERIAL_EVT_HOST_PARAM_SET_REQ',
SERIAL_EVT_HOST_PARAM_GET_REQ : 'SERIAL_EVT_HOST_PARAM_GET_REQ',
SERIAL_EVT_LOCAL_DEVICE_INFO_IND : 'SERIAL_EVT_LOCAL_DEVICE_INFO_IND',
SERIAL_EVT_LOCAL_DEVICE_DATA_SET_IND : 'SERIAL_EVT_LOCAL_DEVICE_DATA_SET_IND',
SERIAL_EVT_REMOTE_GROUP_DATA_SET_IND : 'SERIAL_EVT_REMOTE_GROUP_DATA_SET_IND',
SERIAL_EVT_LOCAL_DATETIME_IND : 'SERIAL_EVT_LOCAL_DATETIME_IND',
SERIAL_EVT_REMOTE_LMP_DATA_EVENT_IND : 'SERIAL_EVT_REMOTE_LMP_DATA_EVENT_IND',
SERIAL_EVT_REMOTE_LMP_DATA_STATUS_IND : 'SERIAL_EVT_REMOTE_LMP_DATA_STATUS_IND',
SERIAL_EVT_REMOTE_MODULE_INFO_IND : 'SERIAL_EVT_REMOTE_MODULE_INFO_IND',
SERIAL_EVT_REMOTE_NETWORK_INFO_IND : 'SERIAL_EVT_REMOTE_NETWORK_INFO_IND',
SERIAL_EVT_REMOTE_BEACON_IND : 'SERIAL_EVT_REMOTE_BEACON_IND',
SERIAL_EVT_REMOTE_MODULE_MSG_IND : 'SERIAL_EVT_REMOTE_MODULE_MSG_IND',
SERIAL_EVT_REMOTE_DEVICE_INFO_IND : 'SERIAL_EVT_REMOTE_DEVICE_INFO_IND',
SERIAL_EVT_REMOTE_DEVICE_DATA_EVENT_IND : 'SERIAL_EVT_REMOTE_DEVICE_DATA_EVENT_IND',
SERIAL_EVT_REMOTE_DEVICE_DATA_STATUS_IND : 'SERIAL_EVT_REMOTE_DEVICE_DATA_STATUS_IND',
SERIAL_EVT_CENTRAL_CONNECTED_IND : 'SERIAL_EVT_CENTRAL_CONNECTED_IND',
SERIAL_EVT_CENTRAL_DISCONNECTED_IND : 'SERIAL_EVT_CENTRAL_DISCONNECTED_IND',

}
