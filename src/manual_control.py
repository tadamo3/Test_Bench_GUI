##
# @file
# manual_control.py
#
# @brief
# Manual control of the test bench.\n

import serial_funcs
import home_page

# Global constants
INDEX_PREVIOUS_MOTOR = 0

INDEX_BUTTON_UP     = 0
INDEX_BUTTON_DOWN   = 1
INDEX_BUTTON_LEFT   = 2
INDEX_BUTTON_RIGHT  = 3

# Global variables
previous_motor_controlled = [serial_funcs.ID_MOTOR_VERTICAL_LEFT]

# Functions
def key_pressed(event, previous_motor, list_buttons):
    """! Sends appropriate command to the uC depending on the pressed key on keyboard (WASD possible)
    @param event            Event object containing different data about the physical event that the computer recorded
    @param previous_motor   The previous motor that was controlled - is necessary to send the appropriate stop condition to the uC
    """
    if (event.char and event.char in 'wads'):
        if event.char == 'w':
            serial_funcs.transmit_serial_data(
                                            serial_funcs.ID_MOTOR_VERTICAL_LEFT,
                                            serial_funcs.COMMAND_MOTOR_VERTICAL_UP,
                                            serial_funcs.MODE_MANUAL_CONTROL,
                                            serial_funcs.DATA_NONE,
                                            serial_funcs.g_list_connected_device_info)
            
            list_buttons[INDEX_BUTTON_UP].configure(fg_color = '#EE1289')
            
            previous_motor[INDEX_PREVIOUS_MOTOR] = serial_funcs.ID_MOTOR_VERTICAL_LEFT

        elif event.keysym == 's':
            serial_funcs.transmit_serial_data(
                                            serial_funcs.ID_MOTOR_VERTICAL_LEFT,
                                            serial_funcs.COMMAND_MOTOR_VERTICAL_DOWN,
                                            serial_funcs.MODE_MANUAL_CONTROL,
                                            serial_funcs.DATA_NONE,
                                            serial_funcs.g_list_connected_device_info)

            list_buttons[INDEX_BUTTON_DOWN].configure(fg_color = '#EE1289')
            
            previous_motor[INDEX_PREVIOUS_MOTOR] = serial_funcs.ID_MOTOR_VERTICAL_LEFT
        
        elif event.keysym == 'a':
            serial_funcs.transmit_serial_data(
                                            serial_funcs.ID_MOTOR_HORIZONTAL,
                                            serial_funcs.COMMAND_MOTOR_HORIZONTAL_LEFT,
                                            serial_funcs.MODE_MANUAL_CONTROL,
                                            serial_funcs.DATA_NONE,
                                            serial_funcs.g_list_connected_device_info)

            list_buttons[INDEX_BUTTON_LEFT].configure(fg_color = '#EE1289')

            previous_motor[INDEX_PREVIOUS_MOTOR] = serial_funcs.ID_MOTOR_HORIZONTAL

        elif event.keysym == 'd':
            serial_funcs.transmit_serial_data(
                                            serial_funcs.ID_MOTOR_HORIZONTAL,
                                            serial_funcs.COMMAND_MOTOR_HORIZONTAL_RIGHT,
                                            serial_funcs.MODE_MANUAL_CONTROL,
                                            serial_funcs.DATA_NONE,
                                            serial_funcs.g_list_connected_device_info)

            list_buttons[INDEX_BUTTON_RIGHT].configure(fg_color = '#EE1289')

            previous_motor[INDEX_PREVIOUS_MOTOR] = serial_funcs.ID_MOTOR_HORIZONTAL

def key_released(event, previous_motor, list_buttons):
    """! Sends appropriate stop condition when a keyboard key is released
    @param event            Event object containing different data about the physical event that the computer recorded
    @param previous_motor   The previous motor that was controlled
    """
    for i in range(len(list_buttons)):
        list_buttons[i].configure(fg_color = '#3D59AB')

    if (previous_motor[INDEX_PREVIOUS_MOTOR] == serial_funcs.ID_MOTOR_VERTICAL_LEFT):
        serial_funcs.transmit_serial_data(
                                                serial_funcs.ID_MOTOR_VERTICAL_LEFT,
                                                serial_funcs.COMMAND_MOTOR_VERTICAL_STOP,
                                                serial_funcs.MODE_MANUAL_CONTROL,
                                                serial_funcs.DATA_NONE,
                                                serial_funcs.g_list_connected_device_info)

    elif (previous_motor[INDEX_PREVIOUS_MOTOR] == serial_funcs.ID_MOTOR_HORIZONTAL):
        serial_funcs.transmit_serial_data(
                                                serial_funcs.ID_MOTOR_HORIZONTAL,
                                                serial_funcs.COMMAND_MOTOR_HORIZONTAL_STOP,
                                                serial_funcs.MODE_MANUAL_CONTROL,
                                                serial_funcs.DATA_NONE,
                                                serial_funcs.g_list_connected_device_info)