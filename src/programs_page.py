##
# @file
# programs_page.py
#
# @brief
# This file acts as the setup file for the programs page of the GUI. \n
# All its components and callback functions will be defined here.

# Imports
import tkinter
import customtkinter
from serial.tools import list_ports
from threading import Thread
from threading import Event
from CTkMessagebox import CTkMessagebox
import time

import serial_funcs
import app
from common import button_generate, entry_generate, label_generate, combobox_generate, slider_generate

import os
from glob import glob

import numpy as np

## Global constants
## The width and height of the home page
HOME_PAGE_WIDTH     = 1450
HOME_PAGE_HEIGHT    = 1500

BUTTON_DIRECTION_CENTER_X   = 400
BUTTON_DIRECTION_CENTER_Y   = 250

## Info about the vertical speed slider
SLIDER_VERTICAL_SPEED_X                 = 200
SLIDER_VERTICAL_SPEED_Y                 = 400
SLIDER_VERTICAL_SPEED_PREV_VALUE_INDEX  = 0
SLIDER_VERTICAL_SPEED_RANGE_MAX         = 100

## Info about the horizontal speed slider
SLIDER_HORIZONTAL_SPEED_X                   = 200
SLIDER_HORIZONTAL_SPEED_Y                   = 500
SLIDER_HORIZONTAL_SPEED_PREV_VALUE_INDEX    = 0
SLIDER_HORIZONTAL_SPEED_RANGE_MAX           = 100

## Info about the entry textbox for position control
ASK_ENTRY_VALUE_X = 200
ASK_ENTRY_VALUE_Y = 300

COMBOBOX_MOVEMENT_1_X = 100
COMBOBOX_MOVEMENT_1_Y = 200

LABEL_NUMBER_REPS_X = 100
LABEL_NUMBER_REPS_Y = 450

## Maximal values we can travel to
MAX_HORIZONTAL  = 30
MAX_VERTICAL    = 30

CHECKPOINT_A = 0
CHECKPOINT_B = 1

INDEX_MOVEMENT_UP       = 0
INDEX_MOVEMENT_DOWN     = 1
INDEX_MOVEMENT_RIGHT    = 2
INDEX_MOVEMENT_LEFT     = 3

## Listbox position
FRAME_POS_X = 780
FRAME_POS_Y = 0

## Name of file
ENTRY_POS_X = 300
ENTRY_POS_Y = 200

## Save settings file positon
BUTTON_SETTINGS_X          = 100
BUTTON_SETTINGS_Y          = 100

BUTTON_SELECT_X            = 250
BUTTON_SELECT_Y            = 100


NP_VALUE_X       = 50
NP_VALUE_Y       = 50

BUTTON_DIRECTION_CENTER_X = 200
BUTTON_DIRECTION_CENTER_Y = 250

## Global variables
list_buttons_manual_control = []
path_to_programs_folder = '..\\Test_Bench_GUI\\programs'

## Classes
class ProgramsPageFrame(customtkinter.CTkFrame):
    """! Programs page class for the Zimmer Test Bench\n
    Defines the components and callback functions of the programs page
    """
    list_slider_vertical_info = [0]
    list_slider_horizontal_info = [0]
    current_checkpoint_to_reach = 1
    list_movement_entries = ["Up", "Down", "Right", "Left"]

    flag_is_auto_thread_stopped = False
    flag_auto_thread_created_once = False

    counter_repetitions = 0


    def determine_trajectory_parameters(self, direction_a, direction_b):
        command_a = serial_funcs.COMMAND_RESERVED
        command_b = serial_funcs.COMMAND_RESERVED
        id = serial_funcs.ID_RESERVED

        if (direction_a == "Up"):
            command_a = serial_funcs.COMMAND_MOTOR_VERTICAL_UP
            id = serial_funcs.ID_MOTOR_VERTICAL_LEFT

        elif (direction_a == "Down"):
            command_a = serial_funcs.COMMAND_MOTOR_VERTICAL_DOWN
            id = serial_funcs.ID_MOTOR_VERTICAL_LEFT
        
        elif (direction_a == "Right"):
            command_a = serial_funcs.COMMAND_MOTOR_HORIZONTAL_RIGHT
            id = serial_funcs.ID_MOTOR_HORIZONTAL

        elif (direction_a == "Left"):
            command_a = serial_funcs.COMMAND_MOTOR_HORIZONTAL_LEFT
            id = serial_funcs.ID_MOTOR_HORIZONTAL

        if (direction_b == "Up"):
            command_b = serial_funcs.COMMAND_MOTOR_VERTICAL_UP
            id = serial_funcs.ID_MOTOR_VERTICAL_LEFT

        elif (direction_b == "Down"):
            command_b = serial_funcs.COMMAND_MOTOR_VERTICAL_DOWN
            id = serial_funcs.ID_MOTOR_VERTICAL_LEFT
        
        elif (direction_b == "Right"):
            command_b = serial_funcs.COMMAND_MOTOR_HORIZONTAL_RIGHT
            id = serial_funcs.ID_MOTOR_HORIZONTAL

        elif (direction_b == "Left"):
            command_b = serial_funcs.COMMAND_MOTOR_HORIZONTAL_LEFT
            id = serial_funcs.ID_MOTOR_HORIZONTAL

        return id, command_a, command_b

    def auto_mode(self, position_to_reach, direction_a, direction_b, label_reps, stop_event):
        id, command_a, command_b = self.determine_trajectory_parameters(direction_a, direction_b)

        # Start auto mode trajectory
        serial_funcs.transmit_serial_data(
                                                    id,
                                                    command_a,
                                                    serial_funcs.MODE_POSITION_CONTROL,
                                                    position_to_reach,
                                                    serial_funcs.g_list_connected_device_info)

        #while (stop_event.is_set() != True):
        #    self.counter_repetitions = self.counter_repetitions + 1
        #    while (serial_funcs.g_list_message_info[serial_funcs.INDEX_STATUS_MOTOR] == serial_funcs.MOTOR_STATE_AUTO_IN_TRAJ):
        #        pass

        #   if ((serial_funcs.g_list_message_info[serial_funcs.INDEX_STATUS_MOTOR] == serial_funcs.MOTOR_STATE_AUTO_END_OF_TRAJ) and (self.current_checkpoint_to_reach == 1)):
        #        serial_funcs.transmit_serial_data(
        #                                            id,
        #                                            command_b,
        #                                            serial_funcs.MODE_POSITION_CONTROL,
        #                                            position_to_reach,
        #                                            serial_funcs.g_list_connected_device_info)

        #       self.current_checkpoint_to_reach = 0

        #    elif ((serial_funcs.g_list_message_info[serial_funcs.INDEX_STATUS_MOTOR] == serial_funcs.MOTOR_STATE_AUTO_END_OF_TRAJ) and (self.current_checkpoint_to_reach == 0)):
        #        serial_funcs.transmit_serial_data(
        #                                            id,
        #                                            command_a,
        #                                            serial_funcs.MODE_POSITION_CONTROL,
        #                                            position_to_reach,
        #                                            serial_funcs.g_list_connected_device_info)

        #        self.current_checkpoint_to_reach = 1
        #        self.counter_repetitions = self.counter_repetitions + 1

        #    label_reps.configure(text = str(self.counter_repetitions))

        #    time.sleep(0.1)

        #if (stop_event.is_set() == True):
        #    self.counter_repetitions = -99
        #    label_reps.configure(text = str(self.counter_repetitions))


    def slider_speed_callback(self, slider_value, list_slider_info, slider_type, label_slider, list_com_device_info):
        """! Every time a new value is set, sends the updated speed value to the device
        @param slider_value         The selected speed value for the vertical motor speed
        @param list_slider_info     Notable information for a specific slider
        @param list_com_device_info Notable information for all connected devices
        """
        if (list_com_device_info[0] != 0):
            slider_value = round(slider_value)
            previous_slider_value = round(list_slider_info[SLIDER_VERTICAL_SPEED_PREV_VALUE_INDEX])

            if (slider_value != previous_slider_value):
                if (slider_type == "Vertical"):
                    serial_funcs.transmit_serial_data(
                                                        serial_funcs.ID_MOTOR_VERTICAL_LEFT,
                                                        serial_funcs.COMMAND_MOTOR_CHANGE_SPEED,
                                                        serial_funcs.MODE_CHANGE_PARAMS,
                                                        slider_value,
                                                        list_com_device_info)

                if (slider_type == "Horizontal"):
                    serial_funcs.transmit_serial_data(
                                                        serial_funcs.ID_MOTOR_HORIZONTAL,
                                                        serial_funcs.COMMAND_MOTOR_CHANGE_SPEED,
                                                        serial_funcs.MODE_CHANGE_PARAMS,
                                                        slider_value,
                                                        list_com_device_info)
                list_slider_info[SLIDER_VERTICAL_SPEED_PREV_VALUE_INDEX] = slider_value
        
        speed_value_mm_per_sec = int((72000000 / (65000 - 450 * slider_value)) * (1 / 80))
        label_slider.configure(text = (str(speed_value_mm_per_sec) + " mm/s"))
    

    def button_submit_click(self, button_submit, entry_position, combobox_direction_1, combobox_direction_2, label_reps):
        dp_str = entry_position.get()
        desired_position = int(dp_str)
        desired_direction_1 = combobox_direction_1.get()
        desired_direction_2 = combobox_direction_2.get()

        # User input checkup
        # Cannot exceed max value
        if ((desired_direction_1 == "Up" or desired_direction_1 == "Down") &
        desired_position > MAX_VERTICAL):
            message_err_input = CTkMessagebox(title="Error", message="Desired position not possible", icon="cancel")
        elif ((desired_direction_1 == "Right" or desired_direction_1 == "Left") &
        desired_position > MAX_HORIZONTAL):
            message_err_input = CTkMessagebox(title="Error", message="Desired position not possible", icon="cancel")

        # Entry box for desired position cannot be empty
        if (dp_str == ''):
            message_err_input = CTkMessagebox(title="Error", message="Missing desired position", icon="cancel")

        # Cannot have incompatible 2nd movement
        if (desired_direction_1 == "Up" and desired_direction_2 != "Down"):
            message_err_input = CTkMessagebox(title="Error", message="Incompatible directions", icon="cancel")
        elif (desired_direction_1 == "Down" and desired_direction_2 != "Up"):
            message_err_input = CTkMessagebox(title="Error", message="Incompatible directions", icon="cancel")
        elif (desired_direction_1 == "Right" and desired_direction_2 != "Left"):
            message_err_input = CTkMessagebox(title="Error", message="Incompatible directions", icon="cancel")
        elif (desired_direction_1 == "Left" and desired_direction_2 != "Right"):
            message_err_input = CTkMessagebox(title="Error", message="Incompatible directions", icon="cancel")

        # Combobox cannot be empty
        if combobox_direction_1.get() == '':
            message_combo1_no_input = CTkMessagebox(title="Error", message="Missing input for first direction", icon="cancel")
        elif combobox_direction_2.get() == '':
            message_combo2_no_input = CTkMessagebox(title="Error", message="Missing input for second direction", icon="cancel")

        if (button_submit.cget("text") == "Submit"):
            button_submit.configure(text = "Stop", fg_color = '#EE3B3B')
        else:
            button_submit.configure(text = "Submit", fg_color = '#66CD00')

        # Default thread
        thread_auto_mode = Thread(target = self.auto_mode, args = (desired_position, desired_direction_1, desired_direction_2, label_reps, app.home_page_auto_mode_thread_event, ))

        if (self.flag_auto_thread_created_once == False):
            thread_auto_mode.start()

            self.flag_auto_thread_created_once = True
        else:
            if (self.flag_is_auto_thread_stopped == True):
                app.home_page_auto_mode_thread_event.clear()

                thread_auto_mode = None
                thread_auto_mode = Thread(target = self.auto_mode, args = (desired_position, desired_direction_1, desired_direction_2, label_reps, app.home_page_auto_mode_thread_event, ))
                thread_auto_mode.start()

                self.flag_is_auto_thread_stopped = False
            else:
                app.home_page_auto_mode_thread_event.set()

                self.flag_is_auto_thread_stopped = True

    def file_creator(self, name, m1, m2, A, VS, HS, N, current_programs_list, list_of_prog):
        complete_path_new_file = path_to_programs_folder + '\\' + name + '.txt'
        name = name.replace(path_to_programs_folder + '\\', '')
        name_file_to_show = name + ".txt"
        VS = round((72000000 / (65000 - 450 * VS)) * (1 / 80))
        HS = round((72000000 / (65000 - 450 * HS)) * (1 / 80))
        with open(complete_path_new_file, "w") as f:
            f.write('Movement 1')
            f.write('\n')
            f.write(m1)
            f.write('\n')
            f.write('Movement 2')
            f.write('\n')
            f.write(m2)
            f.write('\n')
            f.write('Amplitude (mm)')
            f.write('\n')
            f.write(A)
            f.write('\n')
            f.write('Vertical speed (mm/s)')
            f.write('\n')
            f.write(str(VS))
            f.write('\n')
            f.write('Horizontal speed (mm/s)')
            f.write('\n')
            f.write(str(HS))
            f.write('\n')
            f.write('Number of repetitions')
            f.write('\n')
            f.write(N)
            f.write('\n')

            f.close()
        
        if complete_path_new_file not in list_of_prog:
            list_of_prog.append(complete_path_new_file)
            current_programs_list.insert(0, name_file_to_show)
        print("Settings saved in "+name_file_to_show)

    def Select(self, list, m1, m2, A, LVS, VS, LHS, HS, N, n):
        name = list.get(tkinter.ANCHOR)
        name = name.replace('.txt', '')
        print(path_to_programs_folder + '\\' + list.get(tkinter.ANCHOR))
        values = []
        with open((path_to_programs_folder + '\\' + list.get(tkinter.ANCHOR)), "r") as f:
            for i in f:
                v = f.readline()
                v1 = v.split("\n")
                values.append(v1[0])
            
            m1.set(values[0]) 
            m2.set(values[1]) 
            self.cleartext(A)
            A.insert(0, values[2])
            LVS.configure(text = (str(values[3]) + " mm/s"))
            VS.configure(float(values[3]))
            LHS.configure(text = (str(values[4]) + " mm/s"))
            HS.configure(float(values[4]))
            self.cleartext(N)
            N.insert(0, values[5])
            self.cleartext(n)
            n.insert(0, name)

        

    def cleartext(self, var):
        var.delete(0,"end")

    def __init__(self, master, **kwargs):
        """! Initialisation of a Programs Page Frame
        """
        super().__init__(master, **kwargs)

        # Stores the current selected COM port in the combobox
        strvar_current_com_port = customtkinter.StringVar(self)
        
        # Generate all entry
        file_name = entry_generate(self, ENTRY_POS_X, ENTRY_POS_Y, "File name")

        # Generate ListBox object
        programs_list = tkinter.Listbox(
                                        master  =   self,
                                        width   =   80, 
                                        height  =   50)
        programs_list.place(
                            relx = 1,
                            rely = 0,
                            anchor = tkinter.NE)

        # Fill up scrollable list with existing test configs
        file_list = glob(path_to_programs_folder + '\*.txt')
        if (len(file_list) != 0):
            for f in file_list:
                name_file_to_show = f.replace(path_to_programs_folder + '\\', '')
                programs_list.insert(0, name_file_to_show)
            
        # Generate components
        # Position control input values
        combobox_movement_1 = customtkinter.CTkOptionMenu(
                                                        master = self,
                                                        values = self.list_movement_entries, 
                                                        dynamic_resizing = False)
        combobox_movement_1.set("Choose 1st movement")
        combobox_movement_1.place(x = COMBOBOX_MOVEMENT_1_X, y = COMBOBOX_MOVEMENT_1_Y)

        combobox_movement_2 = customtkinter.CTkOptionMenu(
                                                        master = self,
                                                        values = self.list_movement_entries, 
                                                        dynamic_resizing = False)
        combobox_movement_2.set("Choose 2nd movement")
        combobox_movement_2.place(x = COMBOBOX_MOVEMENT_1_X, y = COMBOBOX_MOVEMENT_1_Y + 100)

        entry_desired_position = entry_generate(self, COMBOBOX_MOVEMENT_1_X, COMBOBOX_MOVEMENT_1_Y + 200, "Enter here")
        label_desired_position = label_generate(self, COMBOBOX_MOVEMENT_1_X, COMBOBOX_MOVEMENT_1_Y + 170, "Amplitude (mm)")

        label_visualize_vertical_speed      = label_generate(self, COMBOBOX_MOVEMENT_1_X + 600, COMBOBOX_MOVEMENT_1_Y - 5, "20 mm/s")
        label_visualize_horizontal_speed    = label_generate(self, COMBOBOX_MOVEMENT_1_X + 600, COMBOBOX_MOVEMENT_1_Y + 95, "20 mm/s")

        slider_vertical_speed = slider_generate(self, COMBOBOX_MOVEMENT_1_X + 400, COMBOBOX_MOVEMENT_1_Y, SLIDER_VERTICAL_SPEED_RANGE_MAX)
        slider_vertical_speed.configure(command = lambda slider_value = slider_vertical_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_vertical_info,
                                                                                                                                "Vertical",
                                                                                                                                label_visualize_vertical_speed,
                                                                                                                                serial_funcs.g_list_connected_device_info))

        slider_horizontal_speed = slider_generate(self, COMBOBOX_MOVEMENT_1_X + 400, COMBOBOX_MOVEMENT_1_Y + 100, SLIDER_HORIZONTAL_SPEED_RANGE_MAX)
        slider_horizontal_speed.configure(command = lambda slider_value = slider_horizontal_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_horizontal_info,
                                                                                                                                "Horizontal",
                                                                                                                                label_visualize_horizontal_speed,
                                                                                                                                serial_funcs.g_list_connected_device_info))

        label_vertical_speed_slider     = label_generate(self, COMBOBOX_MOVEMENT_1_X + 400, COMBOBOX_MOVEMENT_1_Y - 30, "Vertical Speed (mm/s)")
        label_horizontal_speed_slider   = label_generate(self, COMBOBOX_MOVEMENT_1_X + 400, COMBOBOX_MOVEMENT_1_Y + 70, "Horizontal speed (mm/s)")

        label_number_reps_indicator = label_generate(self, LABEL_NUMBER_REPS_X, LABEL_NUMBER_REPS_Y, "Number of reps: ")
        entry_number_reps = entry_generate(self, LABEL_NUMBER_REPS_X, LABEL_NUMBER_REPS_Y + 30, "Enter here")

        button_save_settings  = button_generate(self, BUTTON_SETTINGS_X, BUTTON_SETTINGS_Y, "Save settings")
        button_save_settings.configure(command = lambda : self.file_creator(
                                                                            file_name.get(), 
                                                                            combobox_movement_1.get(), 
                                                                            combobox_movement_2.get(), 
                                                                            entry_desired_position.get(), 
                                                                            slider_vertical_speed.get(), 
                                                                            slider_horizontal_speed.get(), 
                                                                            entry_number_reps.get(), 
                                                                            programs_list,
                                                                            file_list))
        
        button_select_settings  = button_generate(self, BUTTON_SELECT_X, BUTTON_SELECT_Y, "Select settings")
        button_select_settings.configure(command = lambda : self.Select(
                                                                        programs_list, 
                                                                        combobox_movement_1, 
                                                                        combobox_movement_2, 
                                                                        entry_desired_position, 
                                                                        label_visualize_vertical_speed, 
                                                                        slider_vertical_speed,
                                                                        label_visualize_horizontal_speed, 
                                                                        slider_horizontal_speed, 
                                                                        entry_number_reps, 
                                                                        file_name))

        btn_submit  = button_generate(self, ENTRY_POS_X, ENTRY_POS_Y + 300, "Submit")
        btn_submit.configure(command = lambda : self.button_submit_click(
                                                                         btn_submit, 
                                                                         entry_desired_position, 
                                                                         combobox_movement_1, 
                                                                         combobox_movement_2, 
                                                                         label_number_reps_indicator), 
                                                                         fg_color = '#66CD00')
