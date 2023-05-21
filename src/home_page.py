##
# @file
# home_page.py
#
# @brief
# This file acts as the setup file for the home page of the GUI. \n
# All its components and callback functions will be defined here.

# Imports
import customtkinter
from threading import Thread
from threading import Event
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
import time

from serial_funcs import *
from automatic_control import AutomaticMode
from common import *
import app

## Classes
class HomePageFrame(customtkinter.CTkFrame):
    """! Home page class for the Zimmer Test Bench\n
    Defines the components and callback functions of the home page
    """
    ## List to contain the direction buttons
    # It is kept accessible to the main app class to bind and unbind the keys when not in the home page frame
    list_directions_buttons = []

    ## Flag to indicate to class functions the state of the thread
    flag_is_auto_test_thread_stopped = True

    def generate_title_frame(self, title):
        """! Generates and places the title of the frame
        @param title    The title to be given to the frame
        @return    The label object created
        """
        # Generate auto label 
        label = customtkinter.CTkLabel(master    = self, 
                                            text_color  = "dodger blue", 
                                            font        = ("Arial", 40),
                                            text        = title) 
        label.grid(
                            row         = ROW_ZERO,
                            column      = COLUMN_ZERO,
                            rowspan     = 1,
                            columnspan  = 4,
                            padx        = PAD_X_USUAL,
                            pady        = PAD_Y_USUAL,
                            sticky      = 'nsew')
        
        return label

    def generate_directions_buttons(self):
        """! Generates and places the direction buttons on the home page frame
        @return     A list containing all of the buttons objects
        """
        btn_direction_up = button_generate(
                                            self,
                                            ROW_ONE,
                                            COLUMN_ONE,
                                            2,
                                            2,
                                            PAD_X_USUAL,
                                            PAD_Y_USUAL,
                                            "Going Up")
        btn_direction_up.configure(fg_color = '#3D59AB', state = "disabled")
            
        btn_direction_down = button_generate(
                                                self,
                                                ROW_FIVE,
                                                COLUMN_ONE,
                                                2,
                                                2,
                                                PAD_X_USUAL,
                                                PAD_Y_USUAL,
                                                "Going Down")
        btn_direction_down.configure(fg_color = '#3D59AB', state = "disabled")

        btn_direction_left = button_generate(
                                                self,
                                                ROW_THREE,
                                                COLUMN_ZERO,
                                                2,
                                                2,
                                                PAD_X_USUAL,
                                                PAD_Y_USUAL,
                                                "Going Left")
        btn_direction_left.configure(fg_color = '#3D59AB', state = "disabled")

        btn_direction_right = button_generate(
                                                self,
                                                ROW_THREE,
                                                COLUMN_TWO,
                                                2,
                                                2,
                                                PAD_X_USUAL,
                                                PAD_Y_USUAL,
                                                "Going Right")
        btn_direction_right.configure(fg_color = '#3D59AB', state = "disabled")

        list_buttons_manual_control = [btn_direction_up, btn_direction_down, btn_direction_left, btn_direction_right]
        
        return list_buttons_manual_control
    
    def button_back_click(self, btn_back, list_items_to_delete, thread_services, connected_device):
        """! Clears all items that were placed on the frame and replaces the control buttons
        @param btn_back                 The back button object
        @param list_items_to_delete     The list of items to clear off the grid of the frame
        """
        btn_back.grid_forget()

        for i in range(len(list_items_to_delete)):
            # Need to check if item is a list passed in the list of items to delete
            if (isinstance(list_items_to_delete[i], type([])) == True):
                for j in range(len(list_items_to_delete[i])):
                    list_items_to_delete[i][j].grid_forget()
            else:
                list_items_to_delete[i].grid_forget()

        self.grid_rowconfigure((ROW_ZERO, ROW_ONE), weight = 0)
        self.grid_columnconfigure(0, weight = 0)
    
        btn_manual_mode = button_generate(
                                            self, 
                                            ROW_ZERO, 
                                            COLUMN_ONE, 
                                            1, 
                                            1, 
                                            PAD_X_USUAL, 
                                            PAD_Y_USUAL, 
                                            "Manual Mode")
        btn_auto_mode   = button_generate(
                                            self, 
                                            ROW_ONE, 
                                            COLUMN_ZERO, 
                                            1, 
                                            1, 
                                            PAD_X_USUAL, 
                                            PAD_Y_USUAL, 
                                            "Automatic mode")

        btn_manual_mode.configure(command = lambda : self.button_manual_mode_click(btn_auto_mode, btn_manual_mode, thread_services, connected_device))
        btn_auto_mode.configure(command = lambda : self.button_auto_mode_click(btn_auto_mode, btn_manual_mode, thread_services, connected_device))

    def button_submit_test_click(self, button_submit, entry_position, entry_turns, combobox_direction, thread_services, connected_device):
        """! Verifies the inputs given in the automatic mode control page and starts the appropriate thread to test the desired movement
        @param button_submit        The submit button object
        @param entry_position       Contains the number of mm of movement to be done
        @param entry_turns          Contains the number of turns to be done
        @param combobox_direction   Contains the combination of directions of the movement
        @param thread_services      All thread related services to be dispatched throughout the different GUI frames 
        @param connected_device     The Serial object that is currently connected to the application
        """
        desired_position = int(entry_position.get())
        desired_direction = combobox_direction.get()
        desired_turns = float(entry_turns.get())

        error_msg = None

        #error_msg = verify_test_inputs()
        
        if (error_msg == None):
            if (button_submit.cget("text") == "Test One Repetition"):
                button_submit.configure(text = "Stop test", fg_color = '#EE3B3B')

                if (self.flag_is_auto_test_thread_stopped == True):
                    thread_services.start_test_repetition_thread(desired_position, desired_direction, desired_turns, connected_device)
                    self.flag_is_auto_test_thread_stopped = False
            else:
                button_submit.configure(text = "Test One Repetition", fg_color = '#66CD00', text_color = '#000000')
                
                if (self.flag_is_auto_test_thread_stopped == False):
                    thread_services.stop_test_repetition_thread()
                    self.flag_is_auto_test_thread_stopped = True


    def button_auto_mode_click(self, button_manual_mode, button_auto_mode, thread_services, device):
        """! Generates and places all items related to the automatic mode
        @param button_manual_mode   Button object for the manual mode option
        @param button_auto_mode     Button object for the automatic mode option
        @param thread_services      All thread related services to be dispatched throughout the different GUI frames
        @param device               The serial object connected to the application
        """
        button_manual_mode.grid_forget()
        button_auto_mode.grid_forget()

        self.rowconfigure((ROW_ZERO, ROW_SIX), weight = 0)
        self.rowconfigure(ROW_SEVEN, weight = 1)
        self.columnconfigure((COLUMN_ZERO, COLUMN_THREE), weight = 0)
        self.columnconfigure((COLUMN_FOUR, COLUMN_SIX), weight = 2)
        self.columnconfigure((COLUMN_SEVEN, COLUMN_EIGHT), weight = 0)

        label_title_frame = self.generate_title_frame("AUTOMATIC MODE")

        # Generate position control inputs
        label_movement = label_generate(
                                        self,
                                        ROW_ONE,
                                        COLUMN_ONE,
                                        1,
                                        1,
                                        PAD_X_USUAL,
                                        (PAD_Y_USUAL, 5),
                                        "Movement : ")
        combobox_movement = customtkinter.CTkOptionMenu(
                                                        master = self,
                                                        values = AutomaticMode.list_movement_entries, 
                                                        dynamic_resizing = False)
        combobox_movement.set("Choose movement")
        combobox_movement.grid(
                                row         = ROW_TWO,
                                column      = COLUMN_ONE,
                                rowspan     = 1,
                                columnspan  = 1,
                                padx        = PAD_X_USUAL,
                                pady        = (0, PAD_Y_USUAL),
                                sticky      = 'nsew')

        list_slider_items = generate_sliders(self, MODE_AUTOMATIC_TEST, device)

        label_desired_position = label_generate(
                                                    self,
                                                    ROW_ONE,
                                                    COLUMN_TWO,
                                                    1,
                                                    1,
                                                    PAD_X_USUAL, 
                                                    (PAD_Y_USUAL, 5), 
                                                    "Amplitude (mm)")
        entry_desired_position = entry_generate(
                                                    self, 
                                                    ROW_TWO,
                                                    COLUMN_TWO,
                                                    1,
                                                    1,
                                                    PAD_X_USUAL, 
                                                    (0, PAD_Y_USUAL), 
                                                    "Enter here")

        label_desired_turns = label_generate(
                                                self,
                                                ROW_THREE,
                                                COLUMN_TWO,
                                                1,
                                                1,
                                                PAD_X_USUAL, 
                                                (PAD_Y_USUAL, 5), 
                                                "Number of turns")
        entry_desired_turns = entry_generate(
                                                self,
                                                ROW_FOUR,
                                                COLUMN_TWO,
                                                1,
                                                1,
                                                PAD_X_USUAL,
                                                (0, PAD_Y_USUAL),
                                                "Enter here")

        # Create frame for control buttons
        control_buttons_container = customtkinter.CTkFrame(self)
        control_buttons_container.grid(
                                        row         = ROW_SEVEN,
                                        column      = COLUMN_ZERO,
                                        rowspan     = 1,
                                        columnspan  = 9,
                                        padx        = PAD_X_USUAL,
                                        pady        = PAD_Y_USUAL,
                                        sticky      = 'nsew')
        
        # Configure the grid system with specified weights for the control button frame
        control_buttons_container.grid_rowconfigure(ROW_ZERO, weight = 1)
        control_buttons_container.grid_columnconfigure(COLUMN_ZERO, weight = 1)

        btn_submit_test  = button_generate(
                                            control_buttons_container, 
                                            0, 
                                            0, 
                                            1, 
                                            1, 
                                            PAD_X_USUAL, 
                                            PAD_Y_USUAL, 
                                            "Test One Repetition")
        btn_submit_test.configure(
                                    command = lambda : self.button_submit_test_click(btn_submit_test, entry_desired_position, entry_desired_turns, combobox_movement, thread_services, device), 
                                    fg_color = '#66CD00', 
                                    text_color = '#000000',
                                    width = 150,
                                    height = 50)
    
        # Generate return button and items to delete when pressed
        list_items_to_delete = [
                                label_desired_position,
                                entry_desired_position,
                                list_slider_items,
                                combobox_movement,
                                btn_submit_test,
                                label_desired_turns,
                                entry_desired_turns,
                                label_title_frame,
                                label_movement,
                                control_buttons_container]

        btn_back = button_generate(
                                    self, 
                                    ROW_ZERO, 
                                    COLUMN_EIGHT, 
                                    1, 
                                    1, 
                                    PAD_X_USUAL, 
                                    PAD_Y_USUAL, 
                                    "Back")
        btn_back.configure(command = lambda : self.button_back_click(btn_back, list_items_to_delete, thread_services, device))

    def button_manual_mode_click(self, button_manual_mode, button_auto_mode, thread_services, device):
        """! Generates and places all items related to the manual mode
        @param button_manual_mode   Button object for the manual mode option
        @param button_auto_mode     Button object for the automatic mode option
        @param thread_services
        @param device               Serial object currently connected to the application
        """
        # Reset the grid positioning
        button_manual_mode.grid_forget()
        button_auto_mode.grid_forget()

        self.rowconfigure((ROW_ZERO, ROW_SIX), weight = 0)
        self.columnconfigure((COLUMN_ZERO, COLUMN_THREE), weight = 0)
        self.columnconfigure((COLUMN_FOUR, COLUMN_SIX), weight = 2)
        self.columnconfigure((COLUMN_SEVEN, COLUMN_EIGHT), weight = 0)

        label_title_frame = self.generate_title_frame("MANUAL_MODE")

        # Generate direction buttons
        self.list_directions_buttons = self.generate_directions_buttons()

        # Generate sliders
        list_slider_items = generate_sliders(self, MODE_MANUAL, device)
        
        # Generate return button and items to delete when pressed
        list_items_to_delete = [
                                self.list_directions_buttons,
                                list_slider_items,
                                label_title_frame]

        btn_back = button_generate(
                                    self,
                                    ROW_ZERO,
                                    COLUMN_EIGHT,
                                    1,
                                    1,
                                    PAD_X_USUAL, 
                                    PAD_Y_USUAL, 
                                    "Back")
        btn_back.configure(command = lambda : self.button_back_click(btn_back, list_items_to_delete, thread_services, device))

    def __init__(self, master, thread_services, connected_device, **kwargs):
        """! Initialisation of a Home Page Frame
        """
        super().__init__(master, **kwargs)

        # Configure the grid system with specific weights
        self.grid_rowconfigure((ROW_ZERO, ROW_ONE), weight = 0)
        self.grid_columnconfigure(COLUMN_ZERO, weight = 0)
    
        btn_manual_mode = button_generate(
                                            self, 
                                            ROW_ZERO,
                                            COLUMN_ZERO, 
                                            1, 
                                            1, 
                                            PAD_X_USUAL, 
                                            PAD_Y_USUAL, 
                                            "Manual Mode")
        btn_auto_mode   = button_generate(
                                            self, 
                                            ROW_ONE, 
                                            COLUMN_ZERO, 
                                            1, 
                                            1, 
                                            PAD_X_USUAL, 
                                            PAD_Y_USUAL, 
                                            "Automatic mode")

        btn_manual_mode.configure(command = lambda : self.button_manual_mode_click(btn_auto_mode, btn_manual_mode, thread_services, connected_device))
        btn_auto_mode.configure(command = lambda : self.button_auto_mode_click(btn_auto_mode, btn_manual_mode, thread_services, connected_device))