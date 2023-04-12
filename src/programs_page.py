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
from automatic_control import auto_mode, list_movement_entries

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

## Listbox position
FRAME_POS_X = 780
FRAME_POS_Y = 0

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
SLIDER_SPEED_PREV_VALUE_INDEX = 1

CLOCK_FREQUENCY         = 72000000
PULSE_PER_MM            = 80
ARR_MINIMUM             = 6500
SPEED_INCREMENT         = 45
PULSE_PER_TURN_ADAPTOR  = 400
RATIO_GEARBOX_ADAPTOR   = 10
PRESCALOR               = 10

## Global variables
path_to_programs_folder = '..\\Test_Bench_GUI\\programs'

## Classes
class ProgramsList(customtkinter.CTkScrollableFrame):
    list_buttons_programs_names = []
    list_buttons_programs_objects = []
    counter_programs = 0

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

                button_file = button_generate(self, 0, 0, name_button)
                button_file.grid(row = self.counter_programs, column = 0, padx = 20, pady = 20)
                self.list_buttons_programs_objects.append(button_file)

                self.counter_programs = self.counter_programs + 1

    def add_individual_program(self, name_program):
        flag_is_program_already_existing = False

        for i in range(len(self.list_buttons_programs_names)):
            if (self.list_buttons_programs_names[i] == (name_program + '.txt')):
                flag_is_program_already_existing = True
        
        if (flag_is_program_already_existing == False):
            button_file = button_generate(self, 0, 0, name_program)
            button_file.grid(row = self.counter_programs, column = 0, padx = 20, pady = 20)

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

    flag_is_auto_thread_stopped = False
    flag_auto_thread_created_once = False

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
                    
                    numerator = CLOCK_FREQUENCY
                    denominator = ((ARR_MINIMUM - (SPEED_INCREMENT * slider_value)) + 1) * (PRESCALOR + 1)

                    speed_value_mm_per_sec = int((numerator / denominator) * (1 / PULSE_PER_MM))
                    list_slider_info[SLIDER_SPEED_PREV_VALUE_INDEX] = speed_value_mm_per_sec

                    label_slider.configure(text = (str(speed_value_mm_per_sec) + " mm/s"))

                if (slider_type == "Horizontal"):
                    transmit_serial_data(
                                                        ID_MOTOR_HORIZONTAL,
                                                        COMMAND_MOTOR_CHANGE_SPEED,
                                                        MODE_CHANGE_PARAMS,
                                                        slider_value,
                                                        list_com_device_info)
                    
                    numerator = CLOCK_FREQUENCY
                    denominator = ((ARR_MINIMUM - (SPEED_INCREMENT * slider_value)) + 1) * (PRESCALOR + 1)

                    speed_value_mm_per_sec = int((numerator / denominator) * (1 / PULSE_PER_MM))
                    list_slider_info[SLIDER_SPEED_PREV_VALUE_INDEX] = speed_value_mm_per_sec

                    label_slider.configure(text = (str(speed_value_mm_per_sec) + " mm/s"))
                
                if (slider_type == "Adaptor"):
                    transmit_serial_data(
                                                        ID_MOTOR_ADAPT,
                                                        COMMAND_MOTOR_CHANGE_SPEED,
                                                        MODE_CHANGE_PARAMS,
                                                        slider_value,
                                                        list_com_device_info)
                    
                    numerator = CLOCK_FREQUENCY
                    denominator = ((ARR_MINIMUM - (SPEED_INCREMENT * slider_value)) + 1) * (PRESCALOR + 1)

                    speed_value_turn_per_sec = int(numerator / denominator) * (2 / PULSE_PER_TURN_ADAPTOR)
                    gearbox_turn_per_sec = speed_value_turn_per_sec / RATIO_GEARBOX_ADAPTOR
                    
                    gearbox_speed_string = f"{gearbox_turn_per_sec:.2f}"

                    list_slider_info[SLIDER_SPEED_PREV_VALUE_INDEX] = float(gearbox_speed_string)
                    label_slider.configure(text = (gearbox_speed_string + " turn/s"))

                list_slider_info[SLIDER_PREV_VALUE_INDEX] = slider_value
    
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
        thread_auto_mode = Thread(target = auto_mode, args = (desired_position, desired_direction_1, desired_direction_2, label_reps, app.home_page_auto_mode_thread_event, ))

        if (self.flag_auto_thread_created_once == False):
            thread_auto_mode.start()

            self.flag_auto_thread_created_once = True
        else:
            if (self.flag_is_auto_thread_stopped == True):
                app.home_page_auto_mode_thread_event.clear()

                thread_auto_mode = None
                thread_auto_mode = Thread(target = auto_mode, args = (desired_position, desired_direction_1, desired_direction_2, label_reps, app.home_page_auto_mode_thread_event, ))
                thread_auto_mode.start()

                self.flag_is_auto_thread_stopped = False
            else:
                app.home_page_auto_mode_thread_event.set()

                self.flag_is_auto_thread_stopped = True

    def file_creator(self, filename, combobox_movements, entry_amplitude, entry_number_of_reps, slider_vertical, slider_horizontal, slider_adaptor, frame_programs_list):
        print(filename)
        complete_path_new_file = path_to_programs_folder + '\\' + filename + '.txt'
        name_file_to_show = filename.replace(path_to_programs_folder + '\\', '') + ".txt"

        vertical_speed      = self.list_slider_vertical_info[SLIDER_PREV_VALUE_INDEX]
        horizontal_speed    = self.list_slider_horizontal_info[SLIDER_PREV_VALUE_INDEX]
        adaptor_speed       = self.list_slider_adaptor_info[SLIDER_PREV_VALUE_INDEX]

        with open(complete_path_new_file, "w") as f:
            f.write('Movement sequence\n')
            f.write(combobox_movements.get() + '\n')

            f.write('Amplitude (mm)\n')
            f.write(entry_amplitude.get() + '\n')

            #f.write('Number of turns to do\n')
            #f.write(number_of_turns + '\n')

            f.write('Vertical speed (mm/s)\n')
            f.write(str(vertical_speed) + '\n')

            f.write('Horizontal speed (mm/s)\n')
            f.write(str(horizontal_speed) + '\n')

            f.write('Adaptor speed (turn/s)\n')
            f.write(str(adaptor_speed) + '\n')

            f.write('Number of repetitions to execute\n')
            f.write(entry_number_of_reps.get() + '\n')

            f.close()
        
            frame_programs_list.add_individual_program(filename)
            frame_programs_list.list_buttons_programs_objects[-1].configure(command = lambda : self.button_select_program_callback(
                                                                                                                                    frame_programs_list.list_buttons_programs_objects[-1],
                                                                                                                                    combobox_movements,
                                                                                                                                    entry_amplitude,
                                                                                                                                    slider_vertical,
                                                                                                                                    slider_horizontal,
                                                                                                                                    slider_adaptor))
        
    def button_select_program_callback(self, button_object, combobox_movements, entry_amplitude, slider_vertical, slider_horizontal, slider_adaptor):
        filename_to_open = button_object.cget("text") + '.txt'
        complete_path = path_to_programs_folder + '\\' + filename_to_open
        print(complete_path)

        values = []
        with open((complete_path), "r") as f:
            for i in f:
                line = f.readline()
                separate_lines = line.split("\n")
                values.append(separate_lines[0])
            
            # Set the desired movement sequence combobox text
            combobox_movements.set(values[0])

            # Set the desired amplitude
            entry_amplitude.delete(0, len(entry_amplitude.get()))
            entry_amplitude.insert(0, values[1])

            # Set the desired number of turns
            #self.entry_desired_turns.configure(textvariable = values[2])

            # Set the vertical speed slider
            slider_vertical.set(int(values[2]))

            # Set the horizontal speed slider
            slider_horizontal.set(int(values[3]))

            # Set the adaptor speed slider
            slider_adaptor.set(int(values[4]))

    def cleartext(self, var):
        var.delete(0,"end")

    def __init__(self, master, **kwargs):
        """! Initialisation of a Programs Page Frame
        """
        super().__init__(master, **kwargs)

        # Generate components
        # Position control input values
        label_movement = label_generate(self,COMBOBOX_MOVEMENT_1_X,COMBOBOX_MOVEMENT_1_Y-30, "Movement : ")
        combobox_movement = customtkinter.CTkOptionMenu(
                                                        master = self,
                                                        values = list_movement_entries, 
                                                        dynamic_resizing = False)
        combobox_movement.set("Choose movement")
        combobox_movement.place(x = COMBOBOX_MOVEMENT_1_X, y = COMBOBOX_MOVEMENT_1_Y)

        entry_desired_position = entry_generate(self, COMBOBOX_MOVEMENT_1_X + 200, COMBOBOX_MOVEMENT_1_Y, "Enter here")
        label_desired_position = label_generate(self, COMBOBOX_MOVEMENT_1_X + 200, COMBOBOX_MOVEMENT_1_Y - 30, "Amplitude (mm) : ")

        entry_desired_turns = entry_generate(self, COMBOBOX_MOVEMENT_1_X + 200, COMBOBOX_MOVEMENT_1_Y + 100, "Enter here")
        label_desired_turns = label_generate(self, COMBOBOX_MOVEMENT_1_X + 200, COMBOBOX_MOVEMENT_1_Y + 100 - 30, "Number of turns : ")

        # Generate all slider information
        label_visualize_vertical_speed      = label_generate(self, COMBOBOX_MOVEMENT_1_X + 600, COMBOBOX_MOVEMENT_1_Y - 5, "mm/s")
        label_visualize_horizontal_speed    = label_generate(self, COMBOBOX_MOVEMENT_1_X + 600, COMBOBOX_MOVEMENT_1_Y + 95, "mm/s")
        label_visualize_adaptor_speed       = label_generate(self, COMBOBOX_MOVEMENT_1_X + 600, COMBOBOX_MOVEMENT_1_Y + 195, "turn/s")

        slider_vertical_speed = slider_generate(self, COMBOBOX_MOVEMENT_1_X + 400, COMBOBOX_MOVEMENT_1_Y, SLIDER_VERTICAL_SPEED_RANGE_MAX)
        slider_vertical_speed.configure(command = lambda slider_value = slider_vertical_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_vertical_info,
                                                                                                                                "Vertical",
                                                                                                                                label_visualize_vertical_speed,
                                                                                                                                g_list_connected_device_info))

        slider_horizontal_speed = slider_generate(self, COMBOBOX_MOVEMENT_1_X + 400, COMBOBOX_MOVEMENT_1_Y + 100, SLIDER_HORIZONTAL_SPEED_RANGE_MAX)
        slider_horizontal_speed.configure(command = lambda slider_value = slider_horizontal_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_horizontal_info,
                                                                                                                                "Horizontal",
                                                                                                                                label_visualize_horizontal_speed,
                                                                                                                                g_list_connected_device_info))
        
        slider_adaptor_speed = slider_generate(self, COMBOBOX_MOVEMENT_1_X + 400, COMBOBOX_MOVEMENT_1_Y + 200, SLIDER_HORIZONTAL_SPEED_RANGE_MAX)
        slider_adaptor_speed.configure(command = lambda slider_value = slider_adaptor_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_adaptor_info,
                                                                                                                                "Horizontal",
                                                                                                                                label_visualize_adaptor_speed,
                                                                                                                                g_list_connected_device_info))

        label_vertical_speed_slider     = label_generate(self, COMBOBOX_MOVEMENT_1_X + 400, COMBOBOX_MOVEMENT_1_Y - 30, "Vertical Speed")
        label_horizontal_speed_slider   = label_generate(self, COMBOBOX_MOVEMENT_1_X + 400, COMBOBOX_MOVEMENT_1_Y + 70, "Horizontal speed")
        label_adaptor_speed_slider      = label_generate(self, COMBOBOX_MOVEMENT_1_X + 400, COMBOBOX_MOVEMENT_1_Y + 170, "Adaptor speed")

        label_number_reps_indicator = label_generate(self, COMBOBOX_MOVEMENT_1_X + 200, COMBOBOX_MOVEMENT_1_Y + 170, "Number of reps: ")
        entry_number_reps = entry_generate(self, COMBOBOX_MOVEMENT_1_X + 200, COMBOBOX_MOVEMENT_1_Y + 200, "Enter here")

        label_filename_entry = label_generate(self, ENTRY_POS_X, ENTRY_POS_Y - 30, "Enter filename: ")
        entry_filename = entry_generate(self, ENTRY_POS_X, ENTRY_POS_Y, "File name")

        # Generate scrollable frame containing all programs available on computer with corresponding callback functions for buttons
        programs_list_frame = ProgramsList(
                                            master = self, 
                                            width = 200, 
                                            height = 150)
        programs_list_frame.pack(
                                    side    = tkinter.RIGHT,
                                    fill    = tkinter.Y,
                                    expand  = False,
                                    padx    = 10,
                                    pady    = 10)

        for i in range(len(programs_list_frame.list_buttons_programs_objects)):
            programs_list_frame.list_buttons_programs_objects[i].configure(command = lambda : self.button_select_program_callback(
                                                                                                                                    programs_list_frame.list_buttons_programs_objects[i],
                                                                                                                                    combobox_movement,
                                                                                                                                    entry_desired_position,
                                                                                                                                    slider_vertical_speed,
                                                                                                                                    slider_horizontal_speed,
                                                                                                                                    slider_adaptor_speed))

        button_save_settings  = button_generate(self, BUTTON_SETTINGS_X, BUTTON_SETTINGS_Y, "Save settings")
        button_save_settings.configure(command = lambda : self.file_creator(
                                                                            entry_filename.get(), 
                                                                            combobox_movement, 
                                                                            entry_desired_position, 
                                                                            entry_number_reps,
                                                                            slider_vertical_speed,
                                                                            slider_horizontal_speed,
                                                                            slider_adaptor_speed,
                                                                            programs_list_frame))

        btn_submit  = button_generate(self, ENTRY_POS_X, ENTRY_POS_Y + 100, "Submit")
        btn_submit.configure(command = lambda : self.button_submit_click(
                                                                         btn_submit, 
                                                                         entry_desired_position, 
                                                                         combobox_movement_1, 
                                                                         combobox_movement_2, 
                                                                         label_number_reps_indicator), 
                                                                         fg_color = '#66CD00')
