##
# @file
# manual_control.py
#
# @brief
# Manual control of the test bench.\n

import serial_funcs
import home_page

# Functions
def key_pressed(event):
    if (event.char and event.char in 'wads'):
        if event.char == 'w':
            serial_funcs.transmit_serial_data(
                                            serial_funcs.ID_MOTOR_VERTICAL_LEFT,
                                            serial_funcs.COMMAND_MOTOR_VERTICAL_UP,
                                            serial_funcs.MODE_MANUAL_CONTROL,
                                            serial_funcs.DATA_NONE,
                                            serial_funcs.g_list_connected_device_info)
        elif event.keysym == 's':
            serial_funcs.transmit_serial_data(
                                            serial_funcs.ID_MOTOR_VERTICAL_LEFT,
                                            serial_funcs.COMMAND_MOTOR_VERTICAL_DOWN,
                                            serial_funcs.MODE_MANUAL_CONTROL,
                                            serial_funcs.DATA_NONE,
                                            serial_funcs.g_list_connected_device_info)
        
        elif event.keysym == 'a':
            serial_funcs.transmit_serial_data(
                                            serial_funcs.ID_MOTOR_HORIZONTAL,
                                            serial_funcs.COMMAND_MOTOR_HORIZONTAL_LEFT,
                                            serial_funcs.MODE_MANUAL_CONTROL,
                                            serial_funcs.DATA_NONE,
                                            serial_funcs.g_list_connected_device_info)

        elif event.keysym == 'd':
            serial_funcs.transmit_serial_data(
                                            serial_funcs.ID_MOTOR_HORIZONTAL,
                                            serial_funcs.COMMAND_MOTOR_HORIZONTAL_RIGHT,
                                            serial_funcs.MODE_MANUAL_CONTROL,
                                            serial_funcs.DATA_NONE,
                                            serial_funcs.g_list_connected_device_info)

def key_released(event):
    print("Stop")
    serial_funcs.transmit_serial_data(
                                            serial_funcs.ID_MOTOR_VERTICAL_LEFT,
                                            serial_funcs.COMMAND_MOTOR_VERTICAL_STOP,
                                            serial_funcs.MODE_MANUAL_CONTROL,
                                            serial_funcs.DATA_NONE,
                                            serial_funcs.g_list_connected_device_info)