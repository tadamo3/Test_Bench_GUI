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
from threading import Thread
from CTkMessagebox import CTkMessagebox
from glob import glob

from serial_funcs import *
import app
from common import *
from automatic_control import AutomaticMode

## Global constants
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

COMBOBOX_MOVEMENT_1_X = 100
COMBOBOX_MOVEMENT_1_Y = 200

## Maximal values we can travel to
MAX_HORIZONTAL  = 300
MAX_VERTICAL    = 300

## Name of file
ENTRY_POS_X = 300
ENTRY_POS_Y = 500

## Save settings file positon
BUTTON_SETTINGS_X          = 100
BUTTON_SETTINGS_Y          = 100

BUTTON_SELECT_X            = 250
BUTTON_SELECT_Y            = 100

BUTTON_DIRECTION_CENTER_X = 200
BUTTON_DIRECTION_CENTER_Y = 250

SLIDER_PREV_VALUE_INDEX = 0
SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX = 1

INDEX_COMBOBOX_MOVEMENTS        = 0
INDEX_ENTRY_DESIRED_POSITION    = 1
INDEX_ENTRY_DESIRED_TURNS       = 2
INDEX_LABEL_VERTICAL_SPEED      = 3
INDEX_LABEL_HORIZONTAL_SPEED    = 4
INDEX_LABEL_ADAPTOR_SPEED       = 5
INDEX_SLIDER_VERTICAL_SPEED     = 6
INDEX_SLIDER_HORIZONTAL_SPEED   = 7
INDEX_SLIDER_ADAPTOR_SPEED      = 8
INDEX_ENTRY_NUMBER_REPS_TO_DO   = 9
INDEX_LABEL_NUMBER_REPS_ACTUAL  = 10
INDEX_ENTRY_FILENAME            = 11

## Global variables
path_to_programs_folder = '..\\Test_Bench_GUI\\programs'

## Classes
class ProgramsList(customtkinter.CTkScrollableFrame):
    list_buttons_programs_names = []
    list_buttons_programs_objects = []

    counter_programs = 0

    flag_is_paused_requested = False
    flag_is_stop_requested = False

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add_all_available_programs()
    
    def add_all_available_programs(self):
        file_list = glob(path_to_programs_folder + '\*.txt')

        if (len(file_list) != 0):
            for f in file_list:
                name_button = f.replace(path_to_programs_folder + '\\', '')
                name_button = name_button.replace('.txt', '')
                print(name_button)
                self.list_buttons_programs_names.append(name_button)

                button_file = button_generate(self, self.counter_programs, 0, 1, 1, 20, 20, name_button)
                self.list_buttons_programs_objects.append(button_file)

                self.counter_programs = self.counter_programs + 1

    def add_individual_program(self, name_program):
        flag_is_program_already_existing = False

        for i in range(len(self.list_buttons_programs_names)):
            if (self.list_buttons_programs_names[i] == (name_program + '.txt')):
                flag_is_program_already_existing = True
        
        if (flag_is_program_already_existing == False):
            button_file = button_generate(self, self.counter_programs, 0, 1, 1, 20, 20, name_program)

            self.list_buttons_programs_names.append((name_program + '.txt'))
            self.list_buttons_programs_objects.append(button_file)
            self.counter_programs = self.counter_programs + 1

class ProgramsPageFrame(customtkinter.CTkFrame):
    """! Programs page class for the Zimmer Test Bench\n
    Defines the components and callback functions of the programs page
    """
    list_slider_vertical_info   = [0, 0]
    list_slider_horizontal_info = [0, 0]
    list_slider_adaptor_info    = [0, 0]
    list_objects_programs_page = []

    flag_is_auto_thread_stopped = False
    flag_is_auto_thread_created_once = False
    flag_is_pause_requested = False

    def slider_speed_callback(self, slider_value, list_slider_info, slider_type, label_slider, list_com_device_info):
        """! Every time a new value is set, sends the updated speed value to the device
        @param slider_value         The selected speed value for the vertical motor speed
        @param list_slider_info     Notable information for a specific slider
        @param list_com_device_info Notable information for all connected devices
        """
        if (list_com_device_info[0] != 0):
            slider_value = round(slider_value)
            previous_slider_value = round(list_slider_info[SLIDER_PREV_VALUE_INDEX])

            if (slider_value != previous_slider_value):
                if (slider_type == "Vertical"):
                    transmit_serial_data(
                                                        ID_MOTOR_VERTICAL_LEFT,
                                                        COMMAND_MOTOR_CHANGE_SPEED,
                                                        MODE_CHANGE_PARAMS,
                                                        slider_value,
                                                        list_com_device_info)
                    
                    speed_value_mm_per_sec = calculate_speed_mm_per_sec(slider_value)

                    list_slider_info[SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX] = speed_value_mm_per_sec
                    label_slider.configure(text = (str(speed_value_mm_per_sec) + " mm/s"))

                if (slider_type == "Horizontal"):
                    transmit_serial_data(
                                                        ID_MOTOR_HORIZONTAL,
                                                        COMMAND_MOTOR_CHANGE_SPEED,
                                                        MODE_CHANGE_PARAMS,
                                                        slider_value,
                                                        list_com_device_info)
                    
                    speed_value_mm_per_sec = calculate_speed_mm_per_sec(slider_value)

                    list_slider_info[SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX] = speed_value_mm_per_sec
                    label_slider.configure(text = (str(speed_value_mm_per_sec) + " mm/s"))
                
                if (slider_type == "Adaptor"):
                    transmit_serial_data(
                                                        ID_MOTOR_ADAPT,
                                                        COMMAND_MOTOR_CHANGE_SPEED,
                                                        MODE_CHANGE_PARAMS,
                                                        slider_value,
                                                        list_com_device_info)
                    
                    gearbox_speed_turn_per_sec = calculate_speed_turn_per_sec(slider_value)
                    gearbox_speed_string = f"{gearbox_speed_turn_per_sec:.2f}"

                    list_slider_info[SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX] = float(gearbox_speed_string)
                    label_slider.configure(text = (gearbox_speed_string + " turn/s"))

                list_slider_info[SLIDER_PREV_VALUE_INDEX] = slider_value
    
    def button_pause_click(self, button_pause):
        if (self.flag_is_pause_requested == False):
            app.auto_mode_pause_thread_event.set()

            button_pause.configure(text = "Resume Program", fg_color = '#66CD00', text_color = '#000000')
            self.flag_is_pause_requested = True
        else:
            app.auto_mode_pause_thread_event.clear()
            button_pause.configure(text = "Pause Program", fg_color = '#FFFF00')

            self.flag_is_pause_requested = False

    def button_submit_click(self, button_submit, button_pause, list_objects):
        desired_position = int(list_objects[INDEX_ENTRY_DESIRED_POSITION].get())
        desired_direction = list_objects[INDEX_COMBOBOX_MOVEMENTS].get()
        
        # Desired turns 
        desired_turns = float(list_objects[INDEX_ENTRY_DESIRED_TURNS].get())
        desired_reps = int(list_objects[INDEX_ENTRY_NUMBER_REPS_TO_DO].get())

        error_msg = None

        # Cannot exceed max value
        # For any vertical movement 
        if desired_direction == AutomaticMode.list_movement_entries[0] or desired_direction == AutomaticMode.list_movement_entries[1]:
            if desired_position > MAX_VERTICAL: 
                error_msg = CTkMessagebox(title="Error", message="Exceeds maximum value", icon="cancel")
            
        # For any horizontal movement
        if desired_direction == AutomaticMode.list_movement_entries[2] or desired_direction == AutomaticMode.list_movement_entries[3]:
            if desired_position > MAX_HORIZONTAL: 
                error_msg = CTkMessagebox(title="Error", message="Exceeds maximum value", icon="cancel")
        
        # Combobox cannot be empty
        if desired_direction == "Choose movement":
            error_msg = CTkMessagebox(title="Error", message="Missing desired direction", icon="cancel")
        
        if (error_msg == None):
            if (button_submit.cget("text") == "Start Program"): 
                button_submit.configure(text = "Stop Program", fg_color = '#EE3B3B')

                button_pause.configure(state = "normal")
            else:
                button_submit.configure(text = "Start Program", fg_color = '#66CD00', text_color = '#000000')

                button_pause.configure(state = "disabled")

            # Default thread
            thread_auto_mode = Thread(target = AutomaticMode.auto_mode, args = (desired_position, desired_direction, desired_turns, desired_reps, list_objects[INDEX_LABEL_NUMBER_REPS_ACTUAL], app.auto_mode_thread_event, app.auto_mode_pause_thread_event, ))

            if (self.flag_is_auto_thread_created_once == False):
                thread_auto_mode.start()

                self.flag_is_auto_thread_created_once = True
            else:
                if (self.flag_is_auto_thread_stopped == True):
                    app.auto_mode_thread_event.clear()

                    thread_auto_mode = None
                    thread_auto_mode = Thread(target = AutomaticMode.auto_mode, args = (desired_position, desired_direction, desired_turns, desired_reps, list_objects[INDEX_LABEL_NUMBER_REPS_ACTUAL], app.auto_mode_thread_event, app.auto_mode_pause_thread_event, ))
                    thread_auto_mode.start()

                    self.flag_is_auto_thread_stopped = False
                else:
                    app.auto_mode_thread_event.set()

                    self.flag_is_auto_thread_stopped = True

    def file_creator(self, filename, frame_programs_list):
        complete_path_new_file = path_to_programs_folder + '\\' + filename + '.txt'
        name_file_to_show = filename.replace(path_to_programs_folder + '\\', '') + ".txt"

        vertical_speed      = self.list_slider_vertical_info[SLIDER_PREV_VALUE_INDEX]
        horizontal_speed    = self.list_slider_horizontal_info[SLIDER_PREV_VALUE_INDEX]
        adaptor_speed       = self.list_slider_adaptor_info[SLIDER_PREV_VALUE_INDEX]

        with open(complete_path_new_file, "w") as f:
            f.write('Movement sequence\n')
            f.write(self.list_objects_programs_page[INDEX_COMBOBOX_MOVEMENTS].get() + '\n')

            f.write('Amplitude (mm)\n')
            f.write(self.list_objects_programs_page[INDEX_ENTRY_DESIRED_POSITION].get() + '\n')

            f.write('Number of turns to do\n')
            f.write(self.list_objects_programs_page[INDEX_ENTRY_DESIRED_TURNS].get() + '\n')

            f.write('Vertical speed (mm/s)\n')
            f.write(str(vertical_speed) + '\n')

            f.write('Horizontal speed (mm/s)\n')
            f.write(str(horizontal_speed) + '\n')

            f.write('Adaptor speed (turn/s)\n')
            f.write(str(adaptor_speed) + '\n')

            f.write('Number of repetitions to execute\n')
            f.write(self.list_objects_programs_page[INDEX_ENTRY_NUMBER_REPS_TO_DO].get() + '\n')

            f.write('Name given to test\n')
            f.write(filename + '\n')

            f.close()
        
            frame_programs_list.add_individual_program(filename)
            frame_programs_list.list_buttons_programs_objects[-1].configure(command = lambda : self.button_select_program_callback(filename))
            print(filename)

    def button_select_program_callback(self, filename):
        print(filename)
        filename_to_open = filename + '.txt'
        complete_path = path_to_programs_folder + '\\' + filename_to_open

        values = []
        with open((complete_path), "r") as f:
            for i in f:
                line = f.readline()
                separate_lines = line.split("\n")
                values.append(separate_lines[0])
            
            print(values)
            # Set the desired movement sequence combobox text
            self.list_objects_programs_page[INDEX_COMBOBOX_MOVEMENTS].set(values[0])

            # Set the desired amplitude
            self.list_objects_programs_page[INDEX_ENTRY_DESIRED_POSITION].delete(0, len(self.list_objects_programs_page[INDEX_ENTRY_DESIRED_POSITION].get()))
            self.list_objects_programs_page[INDEX_ENTRY_DESIRED_POSITION].insert(0, values[1])

            # Set the desired number of turns
            self.list_objects_programs_page[INDEX_ENTRY_DESIRED_TURNS].delete(0, len(self.list_objects_programs_page[INDEX_ENTRY_DESIRED_TURNS].get()))
            self.list_objects_programs_page[INDEX_ENTRY_DESIRED_TURNS].insert(0, values[2])

            # Set the vertical speed slider
            self.list_objects_programs_page[INDEX_SLIDER_VERTICAL_SPEED].set(int(values[3]))

            # Set the horizontal speed slider
            self.list_objects_programs_page[INDEX_SLIDER_HORIZONTAL_SPEED].set(int(values[4]))

            # Set the adaptor speed slider
            self.list_objects_programs_page[INDEX_SLIDER_ADAPTOR_SPEED].set(int(values[5]))

            # Set the filename
            self.list_objects_programs_page[INDEX_ENTRY_FILENAME].delete(0, len(self.list_objects_programs_page[INDEX_ENTRY_FILENAME].get()))
            self.list_objects_programs_page[INDEX_ENTRY_FILENAME].insert(0, values[7])

    def __init__(self, master, **kwargs):
        """! Initialisation of a Programs Page Frame
        """
        super().__init__(master, **kwargs)

        # Configure the grid system with specific weights for the programs frame
        self.grid_rowconfigure((0, 7), weight = 0)
        self.grid_rowconfigure(8, weight = 1)
        self.grid_columnconfigure((0, 1), weight = 0)
        self.grid_columnconfigure((2, 4), weight = 3)
        self.grid_columnconfigure(6, weight = 2)
    
        # Create frame for control buttons
        control_buttons_container = customtkinter.CTkFrame(self)
        control_buttons_container.grid(
                                        row         = 8,
                                        column      = 0,
                                        rowspan     = 1,
                                        columnspan  = 6,
                                        padx        = 20,
                                        pady        = 20,
                                        sticky      = 'nsew')
        
        # Configure the grid system with specified weights for the control button frame
        control_buttons_container.grid_rowconfigure(0, weight = 1)
        control_buttons_container.grid_columnconfigure((0, 3), weight = 1)

        # Generate scrollable frame containing all programs available on computer with corresponding callback functions for buttons
        programs_list_frame = ProgramsList(
                                            master = self, 
                                            width = 100)
        programs_list_frame.grid(
                                    row         = 0,
                                    column      = 6,
                                    rowspan     = 9,
                                    columnspan  = 1,
                                    padx        = 20,
                                    pady        = 20,
                                    sticky      = 'nsew')

        # Associate a callback function for every program button from the Program List Frame
        for i in range(len(programs_list_frame.list_buttons_programs_names)):
            print(programs_list_frame.list_buttons_programs_names[i])
            programs_list_frame.list_buttons_programs_objects[i].configure(command = lambda filename = programs_list_frame.list_buttons_programs_names[i] : self.button_select_program_callback(filename))

        # Position control input values
        label_movement = label_generate(self, 0, 0, 1, 1, 20, (20, 5), "Movement")
        combobox_movement = customtkinter.CTkOptionMenu(
                                                        master = self,
                                                        values = AutomaticMode.list_movement_entries, 
                                                        dynamic_resizing = False)
        combobox_movement.set("Choose")
        combobox_movement.grid(
                                    row         = 1,
                                    column      = 0,
                                    rowspan     = 1,
                                    columnspan  = 1,
                                    padx        = 20,
                                    pady        = (0, 20),
                                    sticky      = 'nsew')

        label_desired_position = label_generate(self, 0, 1, 1, 1, 20, (20, 5), "Amplitude (mm)")
        entry_desired_position = entry_generate(self, 1, 1, 1, 1, 20, (0, 20), "Enter here")

        label_desired_turns = label_generate(self, 2, 1, 1, 1, 20, (20, 5), "Number of turns")
        entry_desired_turns = entry_generate(self, 3, 1, 1, 1, 20, (0, 20), "Enter here")

        # Generate all slider information
        label_visualize_vertical_speed      = label_generate(self, 1, 5, 1, 1, 5, 20, "mm/s")
        label_visualize_horizontal_speed    = label_generate(self, 3, 5, 1, 1, 5, 20, "mm/s")
        label_visualize_adaptor_speed       = label_generate(self, 5, 5, 1, 1, 5, 20, "turn/s")

        slider_vertical_speed = slider_generate(self, 1, 2, 1, 3, 5, 5, SLIDER_VERTICAL_SPEED_RANGE_MAX)
        slider_vertical_speed.configure(command = lambda slider_value = slider_vertical_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_vertical_info,
                                                                                                                                "Vertical",
                                                                                                                                label_visualize_vertical_speed,
                                                                                                                                g_list_connected_device_info))

        slider_horizontal_speed = slider_generate(self, 3, 2, 1, 3, 5, 5, SLIDER_HORIZONTAL_SPEED_RANGE_MAX)
        slider_horizontal_speed.configure(command = lambda slider_value = slider_horizontal_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_horizontal_info,
                                                                                                                                "Horizontal",
                                                                                                                                label_visualize_horizontal_speed,
                                                                                                                                g_list_connected_device_info))
        
        slider_adaptor_speed = slider_generate(self, 5, 2, 1, 3, 5, 5, SLIDER_HORIZONTAL_SPEED_RANGE_MAX)
        slider_adaptor_speed.configure(command = lambda slider_value = slider_adaptor_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_adaptor_info,
                                                                                                                                "Adaptor",
                                                                                                                                label_visualize_adaptor_speed,
                                                                                                                                g_list_connected_device_info))

        label_vertical_speed_slider     = label_generate(self, 0, 2, 1, 1, 20, (20, 5), "Vertical Speed")
        label_horizontal_speed_slider   = label_generate(self, 2, 2, 1, 1, 20, (20, 5), "Horizontal speed")
        label_adaptor_speed_slider      = label_generate(self, 4, 2, 1, 1, 20, (20, 5), "Adaptor speed")

        label_number_reps_to_do_indicator = label_generate(self, 4, 1, 1, 1, 20, (20, 5), "Number of reps")
        entry_number_reps_to_do = entry_generate(self, 5, 1, 1, 1, 20, (0, 20), "Enter here")

        label_filename_entry = label_generate(self, 6, 1, 1, 1, 20, (20, 5), "Enter filename")
        entry_filename = entry_generate(self, 7, 1, 1, 1, 20, (0, 20), "File name")

        label_number_reps_actual_indicator = label_generate(control_buttons_container, 0, 2, 1, 1, (20, 5), 20, "Number of reps done: ")
        label_number_reps_actual_indicator.configure(width = 120, height = 50, fg_color = '#453D52')
        label_number_reps_actual = label_generate(control_buttons_container, 0, 3, 1, 1, (0, 20), 20, "0")
        label_number_reps_actual.configure(width = 50, height = 50, fg_color = '#453D52')

        # Add all useful objects for the save settings option
        self.list_objects_programs_page.extend((combobox_movement,
                                            entry_desired_position,
                                            entry_desired_turns,
                                            label_visualize_vertical_speed,
                                            label_visualize_horizontal_speed,
                                            label_visualize_adaptor_speed,
                                            slider_vertical_speed,
                                            slider_horizontal_speed,
                                            slider_adaptor_speed,
                                            entry_number_reps_to_do,
                                            label_number_reps_actual,
                                            entry_filename))

        # Generate buttons
        button_save_settings  = button_generate(self, 7, 2, 1, 1, 20, 20, "Save settings")
        button_save_settings.configure(command = lambda : self.file_creator(
                                                                            entry_filename.get(),
                                                                            programs_list_frame),
                                                                            fg_color = '#FFC0CB', 
                                                                            text_color = '#000000',
                                                                            width = 150,
                                                                            height = 50)

        btn_pause  = button_generate(control_buttons_container, 0, 1, 1, 1, 20, 20, "Pause Program")
        btn_pause.configure(command = lambda : self.button_pause_click(
                                                                        btn_pause), 
                                                                        fg_color = '#FFFF00', 
                                                                        text_color = '#000000',
                                                                        width = 100,
                                                                        height = 50,
                                                                        state = 'disabled')

        btn_submit  = button_generate(control_buttons_container, 0, 0, 1, 1, 20, 20, "Start Program")
        btn_submit.configure(command = lambda : self.button_submit_click(
                                                                            btn_submit,
                                                                            btn_pause,
                                                                            self.list_objects_programs_page), 
                                                                            fg_color = '#66CD00', 
                                                                            text_color = '#000000',
                                                                            width = 100,
                                                                            height = 50)