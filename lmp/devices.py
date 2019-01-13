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

DEVICE_TYPE_BINARY_SENSOR = 0 # binary-sensor, class binary-sensor, sensor
DEVICE_TYPE_SWITCH = 1 # switch, class binary-sensor, sensor
DEVICE_TYPE_DOOR_CONTACTOR = 2 # door-contactor, class binary-sensor, sensor
DEVICE_TYPE_FALL_SENSOR = 3 # fall-sensor, class binary-sensor, sensor
DEVICE_TYPE_MOTION_DETECTOR = 4 # motion-detector, class binary-sensor, sensor
DEVICE_TYPE_OCCUPANCY_DETECTOR = 5 # occupancy-detector, class binary-sensor, sensor
DEVICE_TYPE_PRESENCE_TAG = 6 # presence-tag, class binary-sensor, sensor
DEVICE_TYPE_TAMPER_SWITCH = 7 # tamper-switch, class binary-sensor, sensor
DEVICE_TYPE_PANIC = 8 # panic, class binary-sensor, sensor
DEVICE_TYPE_BEACON = 10 # beacon, class binary-sensor, sensor
DEVICE_TYPE_FLOOD_DETECTOR = 100 # flood-detector, class binary-sensor, sensor
DEVICE_TYPE_SMOKE_DETECTOR = 101 # smoke-detector, class binary-sensor, sensor
DEVICE_TYPE_CO_DETECTOR = 102 # co-detector, class binary-sensor, sensor
DEVICE_TYPE_GAZ_DETECTOR = 103 # gaz-detector, class binary-sensor, sensor
DEVICE_TYPE_BINARY_OUTPUT = 200 # binary-output, class binary-output, actuator
DEVICE_TYPE_MAINS_POWER = 202 # mains-power, class binary-output, actuator
DEVICE_TYPE_ONOFF_LIGHT = 204 # onoff-light, class onoff-light, actuator
DEVICE_TYPE_ANALOG_SENSOR = 300 # analog-sensor, class analog-sensor, sensor
DEVICE_TYPE_TEMPERATURE_SENSOR = 301 # temperature, class analog-sensor, sensor
DEVICE_TYPE_HUMIDITY_SENSOR = 302 # humidity, class analog-sensor, sensor
DEVICE_TYPE_PRESSURE_SENSOR = 303 # pressure, class analog-sensor, sensor
DEVICE_TYPE_ILLUMINANCE_SENSOR = 304 # illuminance, class analog-sensor, sensor
DEVICE_TYPE_SUNLIGHT_SENSOR = 305 # sunlight, class analog-sensor, sensor
DEVICE_TYPE_RAIN_SENSOR = 306 # rain, class analog-sensor, sensor
DEVICE_TYPE_WATER_SENSOR = 307 # water, class analog-sensor, sensor
DEVICE_TYPE_WIND_SENSOR = 308 # wind, class analog-sensor, sensor
DEVICE_TYPE_CO_LEVEL_SENSOR = 310 # co-level, class analog-sensor, sensor
DEVICE_TYPE_CO2_LEVEL_SENSOR = 311 # co2-level, class analog-sensor, sensor
DEVICE_TYPE_COUNT_SENSOR = 320 # count, class analog-sensor, sensor
DEVICE_TYPE_ADC_SENSOR = 330 # adc, class analog-sensor, sensor
DEVICE_TYPE_VOLTAGE_SENSOR = 331 # voltage, class analog-sensor, sensor
DEVICE_TYPE_CHARGE_SENSOR = 332 # charge, class analog-sensor, sensor
DEVICE_TYPE_CURRENT_SENSOR = 333 # current, class analog-sensor, sensor
DEVICE_TYPE_BATTERY_SENSOR = 334 # battery, class analog-sensor, sensor
DEVICE_TYPE_THERMOSTAT = 335 # thermostat, class controller, actuator
DEVICE_TYPE_TEXT = 340 # text, class string, actuator
DEVICE_TYPE_CHAT = 342 # chat, class string, actuator
DEVICE_TYPE_KEYFOB = 350 # keyfob, class controller, sensor
DEVICE_TYPE_LEVEL_CONTROLLER = 351 # level-controller, class controller, sensor
DEVICE_TYPE_INFRARED_CONTROLLER = 360 # infrared-controller, class controller, sensor
DEVICE_TYPE_LEVEL_OUTPUT = 400 # level-output, class level-output, actuator
DEVICE_TYPE_DIMMABLE_LIGHT = 401 # dimmable-light, class dimmable-light, actuator
DEVICE_TYPE_COLOR_DIMMABLE_LIGHT = 402 # color-dimmable-light, class color-dimmable-light, actuator
DEVICE_TYPE_COLOR_WHITE_DIMMABLE_LIGHT = 403 # color-white-dimmable-light, class color-white-dimmable-light, actuator
DEVICE_TYPE_TUNABLE_WHITE_LIGHT = 404 # tunable-white-light, class tunable-white-light, actuator
DEVICE_TYPE_SHADE_CONTROLLER = 410 # shade-controller, class level-output, actuator
DEVICE_TYPE_DOOR_LOCK = 411 # door-lock, class binary-output, actuator
DEVICE_TYPE_SERIAL = 420 # serial, class string, actuator
DEVICE_TYPE_SIREN = 430 # siren, class audio-output, actuator
DEVICE_TYPE_BELL = 431 # bell, class audio-output, actuator
DEVICE_TYPE_GATEWAY = 1000 # gateway, class gateway
DEVICE_TYPE_CAMERA = 2000 # camera, class video-input, sensor
DEVICE_TYPE_UNKNOWN = 0xFFFF # last dummy device

lmp_devices_str_dict = {
DEVICE_TYPE_BINARY_SENSOR : 'binary-sensor',
DEVICE_TYPE_SWITCH : 'switch',
DEVICE_TYPE_DOOR_CONTACTOR : 'door-contactor',
DEVICE_TYPE_FALL_SENSOR : 'fall-sensor',
DEVICE_TYPE_MOTION_DETECTOR : 'motion-detector',
DEVICE_TYPE_OCCUPANCY_DETECTOR : 'occupancy-detector',
DEVICE_TYPE_PRESENCE_TAG : 'presence-tag',
DEVICE_TYPE_TAMPER_SWITCH : 'tamper-switch',
DEVICE_TYPE_PANIC : 'panic',
DEVICE_TYPE_BEACON : 'beacon',
DEVICE_TYPE_FLOOD_DETECTOR : 'flood-detector',
DEVICE_TYPE_SMOKE_DETECTOR : 'smoke-detector',
DEVICE_TYPE_CO_DETECTOR : 'co-detector',
DEVICE_TYPE_GAZ_DETECTOR : 'gaz-detector',
DEVICE_TYPE_BINARY_OUTPUT : 'binary-output',
DEVICE_TYPE_MAINS_POWER : 'mains-power',
DEVICE_TYPE_ONOFF_LIGHT : 'onoff-light',
DEVICE_TYPE_ANALOG_SENSOR : 'analog-sensor',
DEVICE_TYPE_TEMPERATURE_SENSOR : 'temperature',
DEVICE_TYPE_HUMIDITY_SENSOR : 'humidity',
DEVICE_TYPE_PRESSURE_SENSOR : 'pressure',
DEVICE_TYPE_ILLUMINANCE_SENSOR : 'illuminance',
DEVICE_TYPE_SUNLIGHT_SENSOR : 'sunlight',
DEVICE_TYPE_RAIN_SENSOR : 'rain',
DEVICE_TYPE_WATER_SENSOR : 'water',
DEVICE_TYPE_WIND_SENSOR : 'wind',
DEVICE_TYPE_CO_LEVEL_SENSOR : 'co-level',
DEVICE_TYPE_CO2_LEVEL_SENSOR : 'co2-level',
DEVICE_TYPE_COUNT_SENSOR : 'count',
DEVICE_TYPE_ADC_SENSOR : 'adc',
DEVICE_TYPE_VOLTAGE_SENSOR : 'voltage',
DEVICE_TYPE_CHARGE_SENSOR : 'charge',
DEVICE_TYPE_CURRENT_SENSOR : 'current',
DEVICE_TYPE_BATTERY_SENSOR : 'battery',
DEVICE_TYPE_THERMOSTAT : 'thermostat',
DEVICE_TYPE_TEXT : 'text',
DEVICE_TYPE_CHAT : 'chat',
DEVICE_TYPE_KEYFOB : 'keyfob',
DEVICE_TYPE_LEVEL_CONTROLLER : 'level-controller',
DEVICE_TYPE_INFRARED_CONTROLLER : 'infrared-controller',
DEVICE_TYPE_LEVEL_OUTPUT : 'level-output',
DEVICE_TYPE_DIMMABLE_LIGHT : 'dimmable-light',
DEVICE_TYPE_COLOR_DIMMABLE_LIGHT : 'color-dimmable-light',
DEVICE_TYPE_COLOR_WHITE_DIMMABLE_LIGHT : 'color-white-dimmable-light',
DEVICE_TYPE_TUNABLE_WHITE_LIGHT : 'tunable-white-light',
DEVICE_TYPE_SHADE_CONTROLLER : 'shade-controller',
DEVICE_TYPE_DOOR_LOCK : 'door-lock',
DEVICE_TYPE_SERIAL : 'serial',
DEVICE_TYPE_SIREN : 'siren',
DEVICE_TYPE_BELL : 'bell',
DEVICE_TYPE_GATEWAY : 'gateway',
DEVICE_TYPE_CAMERA : 'camera'
}
