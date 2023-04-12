##
# @file
# automatic_control.py
#
# @brief
# Automatic control of the test bench.\n

# Imports
import time

from serial_funcs import *

# Global constants
INDEX_MOVEMENT_UP_DOWN          = 0
INDEX_MOVEMENT_DOWN_UP          = 1
INDEX_MOVEMENT_LEFT_RIGHT       = 2
INDEX_MOVEMENT_RIGHT_LEFT       = 3
INDEX_MOVEMENT_SCREW_UP_DOWN    = 4
INDEX_MOVEMENT_SCREW_DOWN_UP    = 5

CHECKPOINT_A = 0
CHECKPOINT_B = 1

list_movement_entries = ["Up to down", 
                        "Down to up", 
                        "Left to right", 
                        "Right to left",
                        "Screw up to screw down", 
                        "Screw down to screw up"]

# Functions
def determine_trajectory_parameters(directions, number_of_turns):
        command_a = COMMAND_RESERVED
        command_b = COMMAND_RESERVED
        id = ID_RESERVED

        if (directions == list_movement_entries[INDEX_MOVEMENT_UP_DOWN]):
            command_a = COMMAND_MOTOR_VERTICAL_UP
            command_b = COMMAND_MOTOR_VERTICAL_DOWN
            id = ID_MOTOR_VERTICAL_LEFT

        elif (directions == list_movement_entries[INDEX_MOVEMENT_DOWN_UP]):
            command_a = COMMAND_MOTOR_VERTICAL_DOWN
            command_b = COMMAND_MOTOR_VERTICAL_UP
            id = ID_MOTOR_VERTICAL_LEFT
        
        elif (directions == list_movement_entries[INDEX_MOVEMENT_LEFT_RIGHT]):
            command_a = COMMAND_MOTOR_HORIZONTAL_LEFT
            command_b = COMMAND_MOTOR_HORIZONTAL_RIGHT
            id = ID_MOTOR_HORIZONTAL

        elif (directions == list_movement_entries[INDEX_MOVEMENT_RIGHT_LEFT]):
            command_a = COMMAND_MOTOR_HORIZONTAL_RIGHT
            command_b = COMMAND_MOTOR_HORIZONTAL_LEFT
            id = ID_MOTOR_HORIZONTAL
        
        elif (directions == list_movement_entries[INDEX_MOVEMENT_SCREW_UP_DOWN]):
            command_a = COMMAND_MOTOR_ADAPT_UP
            command_b = COMMAND_MOTOR_ADAPT_DOWN
            id = ID_MOTOR_ADAPT
        
        elif (directions == list_movement_entries[INDEX_MOVEMENT_SCREW_DOWN_UP]):
            command_a = COMMAND_MOTOR_ADAPT_DOWN
            command_b = COMMAND_MOTOR_ADAPT_UP
            id = ID_MOTOR_ADAPT

        return id, command_a, command_b

def auto_mode(position_to_reach, directions, number_of_turns, label_reps, stop_event):
    id, command_a, command_b = determine_trajectory_parameters(directions, number_of_turns)
    counter_repetitions = 0
    current_checkpoint_to_reach = CHECKPOINT_B

    # Start auto mode trajectory
    transmit_serial_data(
                                                id,
                                                command_a,
                                                MODE_POSITION_CONTROL,
                                                position_to_reach,
                                                g_list_connected_device_info)

    while (stop_event.is_set() != True):
        if ((g_list_message_info[INDEX_STATUS_MOTOR] == MOTOR_STATE_AUTO_END_OF_TRAJ) and (current_checkpoint_to_reach == CHECKPOINT_B)):
            transmit_serial_data(
                                                id,
                                                command_b,
                                                MODE_POSITION_CONTROL,
                                                position_to_reach,
                                                g_list_connected_device_info)

            current_checkpoint_to_reach = CHECKPOINT_A

        elif ((g_list_message_info[INDEX_STATUS_MOTOR] == MOTOR_STATE_AUTO_END_OF_TRAJ) and (current_checkpoint_to_reach == CHECKPOINT_A)):
            transmit_serial_data(
                                                id,
                                                command_a,
                                                MODE_POSITION_CONTROL,
                                                position_to_reach,
                                                g_list_connected_device_info)

            current_checkpoint_to_reach = CHECKPOINT_B
            counter_repetitions = counter_repetitions + 1

        label_reps.configure(text = str(counter_repetitions))
        time.sleep(1)