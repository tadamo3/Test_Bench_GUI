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

# Constants
MAX_HORIZONTAL  = 300
MAX_VERTICAL    = 300

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

INDEX_LIST_SLIDER_LABEL_VERTICAL_SPEED      = 0
INDEX_LIST_SLIDER_LABEL_HORIZONTAL_SPEED    = 1
INDEX_LIST_SLIDER_LABEL_ADAPTOR_SPEED       = 2
INDEX_LIST_SLIDER_SLIDER_VERTICAL_SPEED     = 3
INDEX_LIST_SLIDER_SLIDER_HORIZONTAL_SPEED   = 4
INDEX__LIST_SLIDER_SLIDER_ADAPTOR_SPEED     = 5

path_to_programs_folder = '..\\Test_Bench_GUI\\programs'

# Classes
class ProgramsList(customtkinter.CTkScrollableFrame):
    """! Scrollable frame to manage the different programs available to the user (upon creation of the programs page and further programs creation)
    """
    ## List to contain all of the names to write on the button objects to select different programs
    list_buttons_programs_names = []

    ## List to contain all of the button objects to select different programs
    list_buttons_programs_objects = []

    ## Number of programs currently generated and placed
    counter_programs = 0
    
    def add_all_available_programs(self):
        """! Skims through the programs folder and generates a button for each one of them
        """
        file_list = glob(path_to_programs_folder + '\*.txt')

        # Checks if the list containing all the returned paths is non-zero
        if (len(file_list) != 0):
            for f in file_list:
                name_button = f.replace(path_to_programs_folder + '\\', '')
                name_button = name_button.replace('.txt', '')
                print(name_button)
                self.list_buttons_programs_names.append(name_button)

                button_file = button_generate(
                                                self, 
                                                self.counter_programs, 
                                                COLUMN_ZERO, 
                                                1, 
                                                1, 
                                                PAD_X_USUAL, 
                                                PAD_Y_USUAL, 
                                                name_button)
                self.list_buttons_programs_objects.append(button_file)

                self.counter_programs = self.counter_programs + 1

    def add_individual_program(self, name_program):
        """! Upon creation of a program by the user after the creation of the programs page, generates and places a button corresponding to the saved settings
        @param name_program     Name of the program given by the user
        """
        flag_is_program_already_existing = False

        for i in range(len(self.list_buttons_programs_names)):
            if (self.list_buttons_programs_names[i] == (name_program + '.txt')):
                flag_is_program_already_existing = True
        
        if (flag_is_program_already_existing == False):
            button_file = button_generate(
                                            self,
                                            self.counter_programs,
                                            COLUMN_ZERO,
                                            1,
                                            1,
                                            PAD_X_USUAL,
                                            PAD_Y_USUAL,
                                            name_program)

            self.list_buttons_programs_names.append((name_program + '.txt'))
            self.list_buttons_programs_objects.append(button_file)
            self.counter_programs = self.counter_programs + 1

    def __init__(self, master, **kwargs):
        """! Initialisation of a scrollable frame to contain all the available programs
        @param master   The frame on which to attach the scrollable frame
        """
        super().__init__(master, **kwargs)

        self.add_all_available_programs()

class ProgramsPageFrame(customtkinter.CTkFrame):
    """! Programs page class for the Zimmer Test Bench\n
    Defines the components and callback functions of the programs page
    """
    list_objects_programs_page = []

    flag_is_auto_thread_stopped = True
    flag_is_auto_thread_paused = False
    
    def button_pause_click(self, button_pause, thread_services):
        """! Pauses or resumes a program and updates the color code of the displayed buttons
        @param button_pause     The button pause object
        @param thread_services  All thread related services to be dispatched throughout the different GUI frames 
        """
        if (self.flag_is_auto_thread_paused == False):
            thread_services.pause_auto_mode_thread()
            button_pause.configure(text = "Resume Program", fg_color = '#66CD00', text_color = '#000000')

            self.flag_is_auto_thread_paused = True
        else:
            thread_services.resume_auto_mode_thread()
            button_pause.configure(text = "Pause Program", fg_color = '#FFFF00')

            self.flag_is_auto_thread_paused = False

    def button_submit_click(self, button_submit, button_pause, list_objects, thread_services, connected_device):
        """! Stops or starts a program and updates the color code of the displayed button
        @param button_submit        The entry button object
        @param button_pause         The pause button object
        @param list_objects         List of the different parameters for the tests
        @param thread_services      All thread related services to be dispatched throughout the different GUI frames
        @param connected_device     The serial object connected to the application
        """
        desired_position = int(list_objects[INDEX_ENTRY_DESIRED_POSITION].get())
        desired_direction = list_objects[INDEX_COMBOBOX_MOVEMENTS].get()
        
        desired_turns = float(list_objects[INDEX_ENTRY_DESIRED_TURNS].get())
        desired_reps = int(list_objects[INDEX_ENTRY_NUMBER_REPS_TO_DO].get())

        error_msg = None
        
        if (error_msg == None):
            if (button_submit.cget("text") == "Start Program"): 
                button_submit.configure(text = "Stop Program", fg_color = '#EE3B3B')
                button_pause.configure(text = "Pause Program", fg_color = '#FFFF00', state = "normal")

                if (self.flag_is_auto_thread_stopped == True):
                    thread_services.start_auto_mode_thread(desired_position, desired_direction, desired_turns, desired_reps, list_objects[INDEX_LABEL_NUMBER_REPS_ACTUAL], connected_device)
                    self.flag_is_auto_thread_stopped = False
            else:
                button_submit.configure(text = "Start Program", fg_color = '#66CD00', text_color = '#000000')
                button_pause.configure(text = "Pause Program", fg_color = '#66CD00', text_color = '#000000', state = "disabled")

                if (self.flag_is_auto_thread_stopped == False):
                    thread_services.stop_auto_mode_thread()
                    self.flag_is_auto_thread_stopped = True

    def file_creator(self, filename, frame_programs_list):
        """! Creates a text file containing all relevant parameters for an automatic test
        @param filename             Name of the file to be created
        @param frame_programs_list  List of all the created automatic programs
        """
        complete_path_new_file = path_to_programs_folder + '\\' + filename + '.txt'
        name_file_to_show = filename.replace(path_to_programs_folder + '\\', '') + ".txt"

        vertical_speed      = list_slider_vertical_info[SLIDER_PREV_VALUE_INDEX]
        horizontal_speed    = list_slider_horizontal_info[SLIDER_PREV_VALUE_INDEX]
        adaptor_speed       = list_slider_adaptor_info[SLIDER_PREV_VALUE_INDEX]

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
        """! Callback function when selecting a program from the scrollable frame\n
                Inserts all the parameters of the selected test in their respective boxes
        @param filename     Name of the file that was selected
        """
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

    def __init__(self, master, thread_services, connected_device, **kwargs):
        """! Initialisation of a Programs Page Frame
                Defines the components and callback functions of the programs page
        """
        super().__init__(master, **kwargs)

        # Configure the grid system with specific weights for the programs frame
        self.grid_rowconfigure((ROW_ZERO, ROW_SEVEN), weight = 0)
        self.grid_rowconfigure(ROW_EIGHT, weight = 1)
        self.grid_columnconfigure((COLUMN_ZERO, COLUMN_ONE), weight = 0)
        self.grid_columnconfigure((COLUMN_TWO, COLUMN_FOUR), weight = 3)
        self.grid_columnconfigure(COLUMN_SIX, weight = 2)
    
        control_buttons_container = customtkinter.CTkFrame(self)
        control_buttons_container.grid(
                                        row         = ROW_EIGHT,
                                        column      = COLUMN_ZERO,
                                        rowspan     = 1,
                                        columnspan  = 6,
                                        padx        = PAD_X_USUAL,
                                        pady        = PAD_Y_USUAL,
                                        sticky      = 'nsew')
        
        control_buttons_container.grid_rowconfigure(0, weight = 1)
        control_buttons_container.grid_columnconfigure((0, 3), weight = 1)

        # Generate scrollable frame containing all programs available on computer with corresponding callback functions for buttons
        programs_list_frame = ProgramsList(
                                            master = self, 
                                            width = 100)
        programs_list_frame.grid(
                                    row         = ROW_ZERO,
                                    column      = COLUMN_SIX,
                                    rowspan     = 9,
                                    columnspan  = 1,
                                    padx        = PAD_X_USUAL,
                                    pady        = PAD_Y_USUAL,
                                    sticky      = 'nsew')

        # Associate a callback function for every program button from the Program List Frame
        for i in range(len(programs_list_frame.list_buttons_programs_names)):
            programs_list_frame.list_buttons_programs_objects[i].configure(command = lambda filename = programs_list_frame.list_buttons_programs_names[i] : self.button_select_program_callback(filename))

        # Position control input values
        label_movement = label_generate(
                                        self, 
                                        ROW_ZERO, 
                                        COLUMN_ZERO, 
                                        1,
                                        1, 
                                        PAD_X_USUAL, 
                                        (PAD_Y_USUAL, 5), 
                                        "Movement")
        combobox_movement = customtkinter.CTkOptionMenu(
                                                        master = self,
                                                        values = AutomaticMode.list_movement_entries, 
                                                        dynamic_resizing = False)
        combobox_movement.set("Choose")
        combobox_movement.grid(
                                    row         = ROW_ONE,
                                    column      = COLUMN_ZERO,
                                    rowspan     = 1,
                                    columnspan  = 1,
                                    padx        = PAD_X_USUAL,
                                    pady        = (0, PAD_Y_USUAL),
                                    sticky      = 'nsew')

        list_slider_items = generate_sliders(self, MODE_AUTOMATIC, connected_device)

        label_desired_position = label_generate(
                                                    self, 
                                                    ROW_ZERO, 
                                                    COLUMN_ONE, 
                                                    1, 
                                                    1, 
                                                    PAD_X_USUAL, 
                                                    (PAD_Y_USUAL, 5), 
                                                    "Amplitude (mm)")
        entry_desired_position = entry_generate(
                                                self, 
                                                ROW_ONE, 
                                                COLUMN_ONE, 
                                                1, 
                                                1, 
                                                PAD_X_USUAL, 
                                                (PAD_Y_USUAL, 20), 
                                                "Enter here")

        label_desired_turns = label_generate(
                                                self, 
                                                ROW_TWO, 
                                                COLUMN_ONE, 
                                                1, 
                                                1, 
                                                PAD_X_USUAL, 
                                                (PAD_Y_USUAL, 5), 
                                                "Number of turns")
        entry_desired_turns = entry_generate(
                                                self, 
                                                ROW_THREE, 
                                                COLUMN_ONE, 
                                                1, 
                                                1, 
                                                PAD_X_USUAL, 
                                                (PAD_Y_USUAL, 20), 
                                                "Enter here")

        label_number_reps_to_do_indicator = label_generate(
                                                            self, 
                                                            ROW_FOUR, 
                                                            COLUMN_ONE, 
                                                            1, 
                                                            1, 
                                                            PAD_X_USUAL, 
                                                            (PAD_Y_USUAL, 5), 
                                                            "Number of reps")
        entry_number_reps_to_do = entry_generate(
                                                    self, 
                                                    ROW_FIVE,
                                                    COLUMN_ONE, 
                                                    1, 
                                                    1, 
                                                    PAD_X_USUAL, 
                                                    (0, PAD_Y_USUAL), 
                                                    "Enter here")

        label_filename_entry = label_generate(
                                                self, 
                                                ROW_SIX, 
                                                COLUMN_ONE, 
                                                1, 
                                                1, 
                                                PAD_X_USUAL, 
                                                (PAD_Y_USUAL, 5), 
                                                "Enter filename")
        entry_filename = entry_generate(
                                            self, 
                                            ROW_SEVEN, 
                                            COLUMN_ONE, 
                                            1, 
                                            1, 
                                            PAD_X_USUAL, 
                                            (0, PAD_Y_USUAL), 
                                            "File name")

        label_number_reps_actual_indicator = label_generate(
                                                                control_buttons_container, 
                                                                ROW_ZERO,
                                                                COLUMN_TWO, 
                                                                1, 
                                                                1, 
                                                                (PAD_X_USUAL, 5), 
                                                                PAD_Y_USUAL, 
                                                                "Number of reps done: ")
        label_number_reps_actual_indicator.configure(width = 120, height = 50, fg_color = '#453D52')
        label_number_reps_actual = label_generate(
                                                    control_buttons_container, 
                                                    ROW_ZERO, 
                                                    COLUMN_THREE, 
                                                    1, 
                                                    1, 
                                                    (0, PAD_X_USUAL), 
                                                    PAD_Y_USUAL, 
                                                    "0")
        label_number_reps_actual.configure(width = 50, height = 50, fg_color = '#453D52')

        # Add all useful objects for the save settings option
        self.list_objects_programs_page.extend((combobox_movement,
                                            entry_desired_position,
                                            entry_desired_turns,
                                            list_slider_items[INDEX_LIST_SLIDER_LABEL_VERTICAL_SPEED],
                                            list_slider_items[INDEX_LIST_SLIDER_LABEL_HORIZONTAL_SPEED],
                                            list_slider_items[INDEX_LIST_SLIDER_LABEL_ADAPTOR_SPEED],
                                            list_slider_items[INDEX_LIST_SLIDER_SLIDER_VERTICAL_SPEED],
                                            list_slider_items[INDEX_LIST_SLIDER_SLIDER_HORIZONTAL_SPEED],
                                            list_slider_items[INDEX__LIST_SLIDER_SLIDER_ADAPTOR_SPEED],
                                            entry_number_reps_to_do,
                                            label_number_reps_actual,
                                            entry_filename))

        # Generate buttons
        button_save_settings  = button_generate(
                                                    self, 
                                                    ROW_SEVEN, 
                                                    COLUMN_TWO, 
                                                    1, 
                                                    1, 
                                                    PAD_X_USUAL, 
                                                    PAD_Y_USUAL, 
                                                    "Save settings")
        button_save_settings.configure(command = lambda : self.file_creator(
                                                                            entry_filename.get(),
                                                                            programs_list_frame),
                                                                            fg_color = '#FFC0CB', 
                                                                            text_color = '#000000',
                                                                            width = 150,
                                                                            height = 50)

        btn_pause  = button_generate(
                                        control_buttons_container,
                                        ROW_ZERO,
                                        COLUMN_ONE,
                                        1,
                                        1,
                                        PAD_X_USUAL,
                                        PAD_Y_USUAL,
                                        "Pause Program")
        btn_submit  = button_generate(
                                        control_buttons_container,
                                        ROW_ZERO,
                                        COLUMN_ZERO,
                                        1,
                                        1,
                                        PAD_X_USUAL,
                                        PAD_Y_USUAL,
                                        "Start Program")

        btn_pause.configure(command = lambda : self.button_pause_click(
                                                                            btn_pause,
                                                                            thread_services), 
                                                                            fg_color = '#FFFF00', 
                                                                            text_color = '#000000',
                                                                            width = 100,
                                                                            height = 50,
                                                                            state = 'disabled')
        btn_submit.configure(command = lambda : self.button_submit_click(
                                                                            btn_submit,
                                                                            btn_pause,
                                                                            self.list_objects_programs_page,
                                                                            thread_services,
                                                                            connected_device), 
                                                                            fg_color = '#66CD00', 
                                                                            text_color = '#000000',
                                                                            width = 100,
                                                                            height = 50)