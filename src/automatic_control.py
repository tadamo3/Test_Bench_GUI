##
# @file
# automatic_control.py
#
# @brief
# Automatic control of the test bench.\n

# Imports
import time

from serial_funcs import *

# Constants
INDEX_MOVEMENT_UP_DOWN          = 0
INDEX_MOVEMENT_DOWN_UP          = 1
INDEX_MOVEMENT_LEFT_RIGHT       = 2
INDEX_MOVEMENT_RIGHT_LEFT       = 3
INDEX_MOVEMENT_SCREW_UP_DOWN    = 4
INDEX_MOVEMENT_SCREW_DOWN_UP    = 5

AUTO_MODE_STATE_INIT                    = 0
AUTO_MODE_STATE_WAITING_FOR_ANSWER      = 1
AUTO_MODE_STATE_WAITING_END_OF_TRAJ     = 2
AUTO_MODE_STATE_READY_TO_SEND_COMMAND   = 3

CHECKPOINT_A = 0
CHECKPOINT_B = 1

def determine_trajectory_parameters(directions, list_movements):
    """! Determines the parameters to send to the microcontroler to ensure correct control
    @param directions       Movement type to be executed by the bench test
    @param list_movements   All possible combination of movements that can be executed by the bench test
    @return The motor id to control and the two commands to alternately send to the microcontroler 
    """     
    command_a = COMMAND_RESERVED
    command_b = COMMAND_RESERVED
    id = ID_RESERVED

    if (directions == list_movements[INDEX_MOVEMENT_UP_DOWN]):
        command_a = COMMAND_MOTOR_VERTICAL_UP
        command_b = COMMAND_MOTOR_VERTICAL_DOWN
        id = ID_MOTOR_VERTICAL_LEFT

    elif (directions == list_movements[INDEX_MOVEMENT_DOWN_UP]):
        command_a = COMMAND_MOTOR_VERTICAL_DOWN
        command_b = COMMAND_MOTOR_VERTICAL_UP
        id = ID_MOTOR_VERTICAL_LEFT
    
    elif (directions == list_movements[INDEX_MOVEMENT_LEFT_RIGHT]):
        command_a = COMMAND_MOTOR_HORIZONTAL_LEFT
        command_b = COMMAND_MOTOR_HORIZONTAL_RIGHT
        id = ID_MOTOR_HORIZONTAL

    elif (directions == list_movements[INDEX_MOVEMENT_RIGHT_LEFT]):
        command_a = COMMAND_MOTOR_HORIZONTAL_RIGHT
        command_b = COMMAND_MOTOR_HORIZONTAL_LEFT
        id = ID_MOTOR_HORIZONTAL
    
    elif (directions == list_movements[INDEX_MOVEMENT_SCREW_UP_DOWN]):
        command_a = COMMAND_MOTOR_ADAPT_UP
        command_b = COMMAND_MOTOR_ADAPT_DOWN
        id = ID_MOTOR_ADAPT
    
    elif (directions == list_movements[INDEX_MOVEMENT_SCREW_DOWN_UP]):
        command_a = COMMAND_MOTOR_ADAPT_DOWN
        command_b = COMMAND_MOTOR_ADAPT_UP
        id = ID_MOTOR_ADAPT

    return id, command_a, command_b

# Classes
class AutomaticMode():
    """! Gives access to the automatic control mode functions in order to repeat or test a specific movement
    """
    ## The position that the tool needs to currently reach
    current_checkpoint_to_reach    = CHECKPOINT_A

    ## The previous tool position
    previous_checkpoint_to_reach   = CHECKPOINT_B

    ## List of all the possible movement combinations from the movement combobox
    list_movement_entries = ["Up to down", 
                            "Down to up", 
                            "Left to right", 
                            "Right to left",
                            "Screw up to screw down",
                            "Screw down to screw up"]

    def convert_data_number_of_turns(motor_id, position_to_reach, number_of_turns):
        """! Converts the data to send if the motor adaptor is chosen
        @param motor_id             The ID of the selected motor for the movement
        @param position_to_reach    The amplitude of the movement in millimeters
        @param number_of_turns      Number of turns to be done by the adaptor motor
        @return     The data to send to the microcontroler
        """
        if (motor_id == ID_MOTOR_ADAPT):
            data = int(number_of_turns * 100)
        else:
            data = position_to_reach
        
        return data

    def auto_mode(position_to_reach, directions, number_of_turns, number_reps_to_do, label_reps_actual, connected_device, stop_event, pause_event):
        """! Sends correct commands alternately to the microcontroler in order to make the tool move from point A to point B and back to point A\n
                This function is initialized every time a test needs to be executed (and will subsequently end with its corresponding thread)
        @param position_to_reach    The amplitude of the movement in millimeters
        @param directions           Combination of movements given to determine the trajectory
        @param number_of_turns      Number of turns to be done by the adaptor motor
        @param number_reps_to_do    Number of repetitions to execute before a test is deemed complete
        @param label_reps_actual    Label object to update the number of repetitions that have been completed by the testbench
        @param connected_device     The Serial object currently connected to the application
        @param stop_event           Thread event to stop any other movement to be executed - If set, will reset the number of repetitions executed
        @param pause_event          Thread event to pause the execution of movements - If set, will not reset the number of repetitions executed   
        """
        id, command_a, command_b = determine_trajectory_parameters(directions, AutomaticMode.list_movement_entries)
        counter_repetitions = 0
        current_process_state = AUTO_MODE_STATE_INIT

        data_to_send = AutomaticMode.convert_data_number_of_turns(id, position_to_reach, number_of_turns)

        # Initial movement - Needs to produce correct movement downwards
        if ((AutomaticMode.current_checkpoint_to_reach == CHECKPOINT_A) and (AutomaticMode.previous_checkpoint_to_reach == CHECKPOINT_B)):
            transmit_serial_data(
                                    id,
                                    command_a,
                                    MODE_POSITION_CONTROL,
                                    data_to_send,
                                    connected_device)

            AutomaticMode.previous_checkpoint_to_reach = AutomaticMode.current_checkpoint_to_reach
            AutomaticMode.current_checkpoint_to_reach = CHECKPOINT_B

        current_process_state = AUTO_MODE_STATE_WAITING_FOR_ANSWER

        """Process for auto mode
            The while loop makes the automatic mode run continously until the stop thread event is set to true
            The loop is controlled by a process state variable
            3 steps are involved:
                1 - While the first movement is in execution, the current state will be awaiting the end of trajectory
                2 - At the end of the trajectory, the current state variable will shift to let the application send a new command
                3 - While this command is being sent, the current state variable will wait until an indication that the new trajectory has been started to update itself
        """
        # Control loop with thread events and number of reps
        while ((stop_event.is_set() != True) and (counter_repetitions < number_reps_to_do)):
            if (pause_event.is_set() != True):
                if (current_process_state == AUTO_MODE_STATE_WAITING_FOR_ANSWER):
                    if (g_list_message_info[INDEX_STATUS_MOTOR] == MOTOR_STATE_AUTO_IN_TRAJ):
                        current_process_state = AUTO_MODE_STATE_WAITING_END_OF_TRAJ

                elif (current_process_state == AUTO_MODE_STATE_WAITING_END_OF_TRAJ):
                    if (g_list_message_info[INDEX_STATUS_MOTOR] == MOTOR_STATE_AUTO_END_OF_TRAJ):
                        current_process_state = AUTO_MODE_STATE_READY_TO_SEND_COMMAND

                elif (current_process_state == AUTO_MODE_STATE_READY_TO_SEND_COMMAND):
                    # Go to A position
                    if (AutomaticMode.current_checkpoint_to_reach == CHECKPOINT_A and AutomaticMode.previous_checkpoint_to_reach == CHECKPOINT_B):
                        transmit_serial_data(
                                                id,
                                                command_a,
                                                MODE_POSITION_CONTROL,
                                                data_to_send,
                                                connected_device)
                        
                        current_process_state = AUTO_MODE_STATE_WAITING_FOR_ANSWER
                        
                        AutomaticMode.previous_checkpoint_to_reach = AutomaticMode.current_checkpoint_to_reach
                        AutomaticMode.current_checkpoint_to_reach = CHECKPOINT_B

                    elif (AutomaticMode.current_checkpoint_to_reach == CHECKPOINT_B and AutomaticMode.previous_checkpoint_to_reach == CHECKPOINT_A):
                        # Go to B position
                        transmit_serial_data(
                                                id,
                                                command_b,
                                                MODE_POSITION_CONTROL,
                                                data_to_send,
                                                connected_device)
                        
                        current_process_state = AUTO_MODE_STATE_WAITING_FOR_ANSWER

                        AutomaticMode.previous_checkpoint_to_reach = AutomaticMode.current_checkpoint_to_reach
                        AutomaticMode.current_checkpoint_to_reach = CHECKPOINT_A
                        
                        counter_repetitions = counter_repetitions + 1

                label_reps_actual.configure(text = str(counter_repetitions))

                time.sleep(0.1)

            time.sleep(0.1)

        # Reset the checkpoints in case of stop
        if (stop_event.is_set() == True):
            AutomaticMode.current_checkpoint_to_reach    = CHECKPOINT_A
            AutomaticMode.previous_checkpoint_to_reach   = CHECKPOINT_B

    def auto_mode_test(position_to_reach, directions, number_of_turns, connected_device, stop_event):
        """! This function lets the user test an iteration of an automatic movement
                It executes a back-and-forth between the two positions once
        @param position_to_reach    The amplitude of the movement in millimeters
        @param directions           Combination of movements given to determine the trajectory
        @param number_of_turns      Number of turns to be done by the adaptor motor
        @param connected_device     The Serial object currently connected to the application
        @param stop_event           Thread event to stop any other movement to be executed - If set, will reset the number of repetitions executed
        """
        id, command_a, command_b = determine_trajectory_parameters(directions, AutomaticMode.list_movement_entries)
        current_process_state = AUTO_MODE_STATE_INIT

        data_to_send = AutomaticMode.convert_data_number_of_turns(id, position_to_reach, number_of_turns)

        # Start auto mode trajectory
        transmit_serial_data(
                                id,
                                command_a,
                                MODE_POSITION_CONTROL,
                                data_to_send,
                                connected_device)
        
        current_process_state = AUTO_MODE_STATE_WAITING_FOR_ANSWER

        # Static checkpoint since there is only one repetition needed
        static_current_checkpoint_to_reach = CHECKPOINT_B
        flag_is_trajectory_completed = False

        while (stop_event.is_set() != True and flag_is_trajectory_completed == False):
            if (current_process_state == AUTO_MODE_STATE_WAITING_FOR_ANSWER):
                if (g_list_message_info[INDEX_STATUS_MOTOR] == MOTOR_STATE_AUTO_IN_TRAJ):
                    current_process_state = AUTO_MODE_STATE_WAITING_END_OF_TRAJ

            elif (current_process_state == AUTO_MODE_STATE_WAITING_END_OF_TRAJ):
                if (g_list_message_info[INDEX_STATUS_MOTOR] == MOTOR_STATE_AUTO_END_OF_TRAJ):
                    current_process_state = AUTO_MODE_STATE_READY_TO_SEND_COMMAND

            elif (current_process_state == AUTO_MODE_STATE_READY_TO_SEND_COMMAND):
                if ((g_list_message_info[INDEX_STATUS_MOTOR] == MOTOR_STATE_AUTO_END_OF_TRAJ) and (static_current_checkpoint_to_reach == CHECKPOINT_B)):
                    transmit_serial_data(
                                            id,
                                            command_b,
                                            MODE_POSITION_CONTROL,
                                            data_to_send,
                                            connected_device)

                    static_current_checkpoint_to_reach = CHECKPOINT_A
                    flag_is_trajectory_completed = True
                    
            time.sleep(0.1)