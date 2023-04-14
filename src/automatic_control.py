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
def determine_trajectory_parameters(directions):
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

def auto_mode(position_to_reach, directions, number_of_turns, number_reps_to_do, label_reps_actual, stop_event, pause_event):
    id, command_a, command_b = determine_trajectory_parameters(directions)
    counter_repetitions = 0

    if (id == ID_MOTOR_ADAPT):
        # Number of turns is multiplied by 100 to account for the fact that it is necessary to be able to insert up to 2 digits turn precision
        data_to_send = int(number_of_turns * 100)
        print(data_to_send)
    else:
        data_to_send = position_to_reach

    # Start auto mode trajectory
    transmit_serial_data(
                                                id,
                                                command_a,
                                                MODE_POSITION_CONTROL,
                                                data_to_send,
                                                g_list_connected_device_info)

    current_checkpoint_to_reach = CHECKPOINT_B

    while ((stop_event.is_set() != True) and (counter_repetitions <= number_reps_to_do)):
        if (pause_event.is_set() != True):
            if ((g_list_message_info[INDEX_STATUS_MOTOR] == MOTOR_STATE_AUTO_END_OF_TRAJ) and (current_checkpoint_to_reach == CHECKPOINT_B)):
                transmit_serial_data(
                                                    id,
                                                    command_b,
                                                    MODE_POSITION_CONTROL,
                                                    data_to_send,
                                                    g_list_connected_device_info)

                current_checkpoint_to_reach = CHECKPOINT_A

            elif ((g_list_message_info[INDEX_STATUS_MOTOR] == MOTOR_STATE_AUTO_END_OF_TRAJ) and (current_checkpoint_to_reach == CHECKPOINT_A)):
                transmit_serial_data(
                                                    id,
                                                    command_a,
                                                    MODE_POSITION_CONTROL,
                                                    data_to_send,
                                                    g_list_connected_device_info)

                current_checkpoint_to_reach = CHECKPOINT_B
                counter_repetitions = counter_repetitions + 1

            label_reps_actual.configure(text = str(counter_repetitions))

            # Sleep for 1 second to not overflow the serial buffer
            time.sleep(1)
        
        # Sleep for 1 second every loop of pause to not freeze App
        time.sleep(1)


def auto_mode_test(position_to_reach, directions, number_of_turns, stop_event):
    id, command_a, command_b = determine_trajectory_parameters(directions)
    counter_repetitions = 0

    if (id == ID_MOTOR_ADAPT):
        # Number of turns is multiplied by 100 to account for the fact that it is necessary to be able to insert up to 2 digits turn precision
        data_to_send = int(number_of_turns * 100)
        print(data_to_send)
    else:
        data_to_send = position_to_reach

    # Start auto mode trajectory
    transmit_serial_data(
                                                id,
                                                command_a,
                                                MODE_POSITION_CONTROL,
                                                data_to_send,
                                                g_list_connected_device_info)

    current_checkpoint_to_reach = CHECKPOINT_B

    while (stop_event.is_set() != True):
        if ((g_list_message_info[INDEX_STATUS_MOTOR] == MOTOR_STATE_AUTO_END_OF_TRAJ) and (current_checkpoint_to_reach == CHECKPOINT_B)):
            transmit_serial_data(
                                                id,
                                                command_b,
                                                MODE_POSITION_CONTROL,
                                                data_to_send,
                                                g_list_connected_device_info)

            current_checkpoint_to_reach = CHECKPOINT_A

        # Sleep for 1 second to not overflow the serial buffer
        time.sleep(1)

        # Break condition
        if (current_checkpoint_to_reach == CHECKPOINT_A):
            break