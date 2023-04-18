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
from automatic_control import auto_mode, auto_mode_test, list_movement_entries
from common import *
import app

## Global constants
## The width and height of the home page
HOME_PAGE_WIDTH     = 1450
HOME_PAGE_HEIGHT    = 1500

## Info about the encoders values placeholders
LABEL_ENCODER_VERTICAL_LEFT_VALUE_X = 215
LABEL_ENCODER_VERTICAL_LEFT_VALUE_Y = 700

INDEX_LABEL_ENCODER_VERTICAL_LEFT   = 0
INDEX_LABEL_ENCODER_VERTICAL_RIGHT  = 1
INDEX_LABEL_ENCODER_HORIZONTAL      = 2

BUTTON_DIRECTION_CENTER_X   = 400
BUTTON_DIRECTION_CENTER_Y   = 350

## Info about the vertical speed slider
SLIDER_VERTICAL_SPEED_X                 = BUTTON_DIRECTION_CENTER_X + 350
SLIDER_VERTICAL_SPEED_Y                 = BUTTON_DIRECTION_CENTER_Y - 50
SLIDER_VERTICAL_SPEED_RANGE_MAX         = 100

## Info about the horizontal speed slider
SLIDER_HORIZONTAL_SPEED_X                   = BUTTON_DIRECTION_CENTER_X + 350
SLIDER_HORIZONTAL_SPEED_Y                   = BUTTON_DIRECTION_CENTER_Y + 50
SLIDER_HORIZONTAL_SPEED_RANGE_MAX           = 100

SLIDER_ADAPTOR_SPEED_RANGE_MAX         = 100

SLIDER_PREV_VALUE_INDEX = 0
SLIDER_SPEED_PREV_VALUE_INDEX = 1

BUTTON_MANUAL_MODE_X        = 20
BUTTON_MANUAL_MODE_Y        = 100
BUTTON_AUTO_MODE_X          = 20 
BUTTON_AUTO_MODE_Y          = BUTTON_MANUAL_MODE_Y + 100

## Info about the Return button
BUTTON_BACK_VALUE_X = 1000
BUTTON_BACK_VALUE_Y = 60

## Info about the entry textbox for position control
ASK_ENTRY_VALUE_X = 200
ASK_ENTRY_VALUE_Y = 400

COMBOBOX_MOVEMENT_1_X = 100
COMBOBOX_MOVEMENT_1_Y = 300

LABEL_NUMBER_REPS_X = COMBOBOX_MOVEMENT_1_X + 500
LABEL_NUMBER_REPS_Y = COMBOBOX_MOVEMENT_1_Y + 350

LABEL_MODE_X = 400
LABEL_MODE_Y = 150

## Maximal values we can travel to
MAX_HORIZONTAL  = 400
MAX_VERTICAL    = 400
MAX_SCREW       = 50

CLOCK_FREQUENCY         = 72000000
PULSE_PER_MM            = 80
ARR_MINIMUM             = 6500
SPEED_INCREMENT         = 45
PULSE_PER_TURN_ADAPTOR  = 400
RATIO_GEARBOX_ADAPTOR   = 10
PRESCALOR               = 10

## Global variables
list_buttons_manual_control = []

## Classes
class HomePageFrame(customtkinter.CTkFrame):
    """! Home page class for the Zimmer Test Bench\n
    Defines the components and callback functions of the home page
    """
    list_slider_vertical_info   = [0, 0]
    list_slider_horizontal_info = [0, 0]
    list_slider_adaptor_info    = [0, 0]

    flag_is_auto_thread_stopped = False
    flag_auto_thread_created_once = False

    counter_repetitions = 0

    def read_rx_buffer(self, stop_event):
        """! Threaded function to receive data in a continuous stream\n
        Sleeps for 10ms to match the send rate of the uC
        @param list_labels      List of labels that are meant to be updated periodically
        """
        while (stop_event.is_set() != True):
            receive_serial_data(
                                                g_list_message_info,
                                                g_list_connected_device_info)

            time.sleep(0.05)

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

                    list_slider_info[SLIDER_SPEED_PREV_VALUE_INDEX] = speed_value_mm_per_sec
                    label_slider.configure(text = (str(speed_value_mm_per_sec) + " mm/s"))

                if (slider_type == "Horizontal"):
                    transmit_serial_data(
                                                        ID_MOTOR_HORIZONTAL,
                                                        COMMAND_MOTOR_CHANGE_SPEED,
                                                        MODE_CHANGE_PARAMS,
                                                        slider_value,
                                                        list_com_device_info)
                    
                    speed_value_mm_per_sec = calculate_speed_mm_per_sec(slider_value)

                    list_slider_info[SLIDER_SPEED_PREV_VALUE_INDEX] = speed_value_mm_per_sec
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

                    list_slider_info[SLIDER_SPEED_PREV_VALUE_INDEX] = float(gearbox_speed_string)
                    label_slider.configure(text = (gearbox_speed_string + " turn/s"))

                list_slider_info[SLIDER_PREV_VALUE_INDEX] = slider_value
    
    def button_back_click(self, btn_back, list):
        # This function is utilized when the back button is clicked 
        # Destroy all previous components generated beforehand
        btn_back.place_forget() 

        for i in range(len(list)):
            list[i].place_forget()

        # Generate button modes
        btn_manual_mode = button_generate(self, BUTTON_MANUAL_MODE_X, BUTTON_MANUAL_MODE_Y, "Manual Mode")
        btn_manual_mode.configure(command=lambda:self.button_manual_mode_click(btn_auto_mode, btn_manual_mode))

        btn_auto_mode = button_generate(self, BUTTON_AUTO_MODE_X, BUTTON_AUTO_MODE_Y, "Automatic mode")
        btn_auto_mode.configure(command = lambda : self.button_start_auto_mode_click(btn_auto_mode, btn_manual_mode))

    def button_submit_test_click(self, button_submit, entry_position, entry_turns, combobox_direction):
        # This function is utilized when the submit button is clicked 
        # Desired position
        desired_position = int(entry_position.get())
        desired_direction = combobox_direction.get()
        
        # Desired turns 
        desired_turns = float(entry_turns.get())

        # Generate message errors 
        error_msg = None

        # Cannot exceed max value
        # For any vertical movement 
        if desired_direction == list_movement_entries[0] or desired_direction == list_movement_entries[1]:
            if desired_position > MAX_VERTICAL: 
                error_msg = CTkMessagebox(title="Error", message="Exceeds maximum value", icon="cancel")
            
        # For any horizontal movement
        if desired_direction == list_movement_entries[2] or desired_direction == list_movement_entries[3]:
            if desired_position > MAX_HORIZONTAL: 
                error_msg = CTkMessagebox(title="Error", message="Exceeds maximum value", icon="cancel")

        # For any screwing movement
        if desired_direction == list_movement_entries[4] or desired_direction == list_movement_entries[5]:
            if desired_position > MAX_SCREW: 
                error_msg = CTkMessagebox(title="Error", message="Exceeds maximum value", icon="cancel")
        
        # Combobox cannot be empty
        if desired_direction == "Choose movement":
            error_msg = CTkMessagebox(title="Error", message="Missing desired direction", icon="cancel")
        
        if (error_msg == None):
            if (button_submit.cget("text") == "Test One Repetition"): 
                button_submit.configure(text = "Stop test", fg_color = '#EE3B3B')
            else:
                button_submit.configure(text = "Test One Repetition", fg_color = '#66CD00', text_color = '#000000')

            # Default thread
            thread_auto_mode = Thread(target = auto_mode_test, args = (desired_position, desired_direction, desired_turns, app.home_page_auto_mode_thread_event, ))

            if (self.flag_auto_thread_created_once == False):
                thread_auto_mode.start()

                self.flag_auto_thread_created_once = True
            else:
                if (self.flag_is_auto_thread_stopped == True):
                    app.home_page_auto_mode_thread_event.clear()

                    thread_auto_mode = None
                    thread_auto_mode = Thread(target = auto_mode_test, args = (desired_position, desired_direction, desired_turns, app.home_page_auto_mode_thread_event, ))
                    thread_auto_mode.start()

                    self.flag_is_auto_thread_stopped = False
                else:
                    app.home_page_auto_mode_thread_event.set()

                    self.flag_is_auto_thread_stopped = True


    def button_start_auto_mode_click(self, button_manual_mode, button_auto_mode):
        # Destroy the modes buttons
        button_manual_mode.place_forget()
        button_auto_mode.place_forget()

        # Generate components
        # Label automatic mode 
        
        label_auto = customtkinter.CTkLabel(master = self, 
                                            text_color = "dodger blue", 
                                            font = ("Arial",40),
                                            text = "AUTOMATIC MODE") 
    
        label_auto.place(x=LABEL_MODE_X,y=LABEL_MODE_Y)

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

        entry_desired_turns = entry_generate(self, COMBOBOX_MOVEMENT_1_X + 200, COMBOBOX_MOVEMENT_1_Y+100, "Enter here")
        label_desired_turns = label_generate(self, COMBOBOX_MOVEMENT_1_X + 200, COMBOBOX_MOVEMENT_1_Y +100 - 30, "Number of turns : ")

        label_speed = label_generate(self, COMBOBOX_MOVEMENT_1_X+400, COMBOBOX_MOVEMENT_1_Y - 30 , "Choose speed : ")

        label_visualize_vertical_speed      = label_generate(self, COMBOBOX_MOVEMENT_1_X + 600, COMBOBOX_MOVEMENT_1_Y + 20, (str(self.list_slider_vertical_info[SLIDER_SPEED_PREV_VALUE_INDEX]) + " mm/s"))
        label_visualize_horizontal_speed    = label_generate(self, COMBOBOX_MOVEMENT_1_X + 600, COMBOBOX_MOVEMENT_1_Y + 100, (str(self.list_slider_horizontal_info[SLIDER_SPEED_PREV_VALUE_INDEX]) + " mm/s"))
        label_visualize_rotation_speed      = label_generate(self, COMBOBOX_MOVEMENT_1_X + 600, COMBOBOX_MOVEMENT_1_Y + 180, (str(self.list_slider_adaptor_info[SLIDER_SPEED_PREV_VALUE_INDEX]) + " turn/s"))

        slider_vertical_speed = slider_generate(self, COMBOBOX_MOVEMENT_1_X + 400, COMBOBOX_MOVEMENT_1_Y + 40, SLIDER_VERTICAL_SPEED_RANGE_MAX)
        slider_vertical_speed.set(self.list_slider_vertical_info[SLIDER_PREV_VALUE_INDEX])
        slider_vertical_speed.configure(command = lambda slider_value = slider_vertical_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_vertical_info,
                                                                                                                                "Vertical",
                                                                                                                                label_visualize_vertical_speed,
                                                                                                                                g_list_connected_device_info))

        slider_horizontal_speed = slider_generate(self, COMBOBOX_MOVEMENT_1_X + 400, COMBOBOX_MOVEMENT_1_Y + 120, SLIDER_HORIZONTAL_SPEED_RANGE_MAX)
        slider_horizontal_speed.set(self.list_slider_horizontal_info[SLIDER_PREV_VALUE_INDEX])
        slider_horizontal_speed.configure(command = lambda slider_value = slider_horizontal_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_horizontal_info,
                                                                                                                                "Horizontal",
                                                                                                                                label_visualize_horizontal_speed,
                                                                                                                                g_list_connected_device_info))

        slider_adaptor_speed = slider_generate(self, COMBOBOX_MOVEMENT_1_X + 400, COMBOBOX_MOVEMENT_1_Y + 200, SLIDER_ADAPTOR_SPEED_RANGE_MAX)
        slider_adaptor_speed.set(self.list_slider_adaptor_info[SLIDER_PREV_VALUE_INDEX])
        slider_adaptor_speed.configure(command = lambda slider_value = slider_adaptor_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_adaptor_info,
                                                                                                                                "Adaptor",
                                                                                                                                label_visualize_rotation_speed,
                                                                                                                                g_list_connected_device_info))

        label_vertical_speed_slider     = label_generate(self, COMBOBOX_MOVEMENT_1_X + 400, COMBOBOX_MOVEMENT_1_Y - 30, "Vertical Speed")
        label_horizontal_speed_slider   = label_generate(self, COMBOBOX_MOVEMENT_1_X + 400, COMBOBOX_MOVEMENT_1_Y + 70, "Horizontal speed")
        label_adaptor_speed_slider      = label_generate(self, COMBOBOX_MOVEMENT_1_X + 400, COMBOBOX_MOVEMENT_1_Y + 170, "Adaptor speed")

        btn_submit_test  = button_generate(self, COMBOBOX_MOVEMENT_1_X + 800, COMBOBOX_MOVEMENT_1_Y + 50, "Test One Repetition")
        btn_submit_test.configure(
                                    command = lambda : self.button_submit_test_click(btn_submit_test, entry_desired_position, entry_desired_turns, combobox_movement), 
                                    fg_color = '#66CD00', 
                                    text_color = '#000000',
                                    width = 150,
                                    height = 50)
    
        # Return button configuration
        list_items_to_delete = [
                                label_desired_position,
                                entry_desired_position,
                                slider_horizontal_speed,
                                slider_vertical_speed,
                                slider_adaptor_speed,
                                combobox_movement,
                                btn_submit_test,
                                label_auto, 
                                label_desired_turns,
                                entry_desired_turns,
                                label_movement,
                                label_speed,
                                label_horizontal_speed_slider,
                                label_visualize_vertical_speed, 
                                label_visualize_horizontal_speed,
                                label_vertical_speed_slider,
                                label_adaptor_speed_slider,
                                label_visualize_rotation_speed]

        btn_back  = button_generate(self, BUTTON_BACK_VALUE_X, BUTTON_BACK_VALUE_Y, "Back")
        btn_back.configure(command = lambda : self.button_back_click(btn_back, list_items_to_delete))

    def button_manual_mode_click(self, button_manual_mode, button_auto_mode):
        # This function is utilized when the manual mode is activated (clicked by user)
        # Delete mode selection buttons
        button_manual_mode.place_forget()
        button_auto_mode.place_forget()

        # Generate manual label 
        label_manual = customtkinter.CTkLabel(master = self, 
                                            text_color = "dodger blue", 
                                            font = ("Arial",40),
                                            text = "MANUAL MODE") 
    
        label_manual.place(x=LABEL_MODE_X, y=LABEL_MODE_Y)

        # Generate direction buttons
        btn_direction_up = button_generate(self, BUTTON_DIRECTION_CENTER_X, (BUTTON_DIRECTION_CENTER_Y - 100), "Going Up")
        btn_direction_up.configure(fg_color = '#3D59AB', state = "disabled")
            
        btn_direction_down = button_generate(self, BUTTON_DIRECTION_CENTER_X, (BUTTON_DIRECTION_CENTER_Y + 100), "Going Down")
        btn_direction_down.configure(fg_color = '#3D59AB', state = "disabled")

        btn_direction_left = button_generate(self, (BUTTON_DIRECTION_CENTER_X - 100), BUTTON_DIRECTION_CENTER_Y, "Going Left")
        btn_direction_left.configure(fg_color = '#3D59AB', state = "disabled")

        btn_direction_right = button_generate(self, (BUTTON_DIRECTION_CENTER_X + 100), BUTTON_DIRECTION_CENTER_Y, "Going Right")
        btn_direction_right.configure(fg_color = '#3D59AB', state = "disabled")

        # List with all buttons for manual control to change their colors
        if (len(list_buttons_manual_control) == 0):
            list_buttons_manual_control.append(btn_direction_up)
            list_buttons_manual_control.append(btn_direction_down)
            list_buttons_manual_control.append(btn_direction_left)
            list_buttons_manual_control.append(btn_direction_right)

        ## Generate sliders
        label_visualize_vertical_speed      = label_generate(self, SLIDER_VERTICAL_SPEED_X + 200, SLIDER_VERTICAL_SPEED_Y - 5, (str(self.list_slider_vertical_info[SLIDER_SPEED_PREV_VALUE_INDEX]) + " mm/s"))
        label_visualize_horizontal_speed    = label_generate(self, SLIDER_HORIZONTAL_SPEED_X + 200, SLIDER_HORIZONTAL_SPEED_Y - 5, (str(self.list_slider_horizontal_info[SLIDER_SPEED_PREV_VALUE_INDEX]) + " mm/s"))
        label_visualize_rotation_speed      = label_generate(self, SLIDER_HORIZONTAL_SPEED_X + 200, SLIDER_HORIZONTAL_SPEED_Y + 95, (str(self.list_slider_adaptor_info[SLIDER_SPEED_PREV_VALUE_INDEX]) + " turn/s"))

        slider_vertical_speed = slider_generate(self, SLIDER_VERTICAL_SPEED_X, BUTTON_DIRECTION_CENTER_Y - 50, SLIDER_VERTICAL_SPEED_RANGE_MAX)
        slider_vertical_speed.set(self.list_slider_vertical_info[SLIDER_PREV_VALUE_INDEX])
        slider_vertical_speed.configure(command = lambda slider_value = slider_vertical_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_vertical_info,
                                                                                                                                "Vertical",
                                                                                                                                label_visualize_vertical_speed,
                                                                                                                                g_list_connected_device_info))

        slider_horizontal_speed = slider_generate(self, SLIDER_HORIZONTAL_SPEED_X, BUTTON_DIRECTION_CENTER_Y + 50, SLIDER_HORIZONTAL_SPEED_RANGE_MAX)
        slider_horizontal_speed.set(self.list_slider_horizontal_info[SLIDER_PREV_VALUE_INDEX])
        slider_horizontal_speed.configure(command = lambda slider_value = slider_horizontal_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_horizontal_info,
                                                                                                                                "Horizontal",
                                                                                                                                label_visualize_horizontal_speed,
                                                                                                                                g_list_connected_device_info))

        slider_adaptor_speed = slider_generate(self, SLIDER_HORIZONTAL_SPEED_X, BUTTON_DIRECTION_CENTER_Y + 150, SLIDER_HORIZONTAL_SPEED_RANGE_MAX)
        slider_adaptor_speed.set(self.list_slider_adaptor_info[SLIDER_PREV_VALUE_INDEX])
        slider_adaptor_speed.configure(command = lambda slider_value = slider_adaptor_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_adaptor_info,
                                                                                                                                "Adaptor",
                                                                                                                                label_visualize_rotation_speed,
                                                                                                                                g_list_connected_device_info))

        label_vertical_speed_slider     = label_generate(self, SLIDER_VERTICAL_SPEED_X, BUTTON_DIRECTION_CENTER_Y - 80, "Vertical Speed")
        label_horizontal_speed_slider   = label_generate(self, SLIDER_HORIZONTAL_SPEED_X, BUTTON_DIRECTION_CENTER_Y + 20, "Horizontal speed")
        label_adaptor_speed_slider      = label_generate(self, SLIDER_HORIZONTAL_SPEED_X, BUTTON_DIRECTION_CENTER_Y + 120, "Adaptor speed")

        # Generate return button and items to delete when pressed
        list_items_to_delete = [
                                btn_direction_up, 
                                btn_direction_down, 
                                btn_direction_left,
                                btn_direction_right,
                                slider_vertical_speed,
                                slider_horizontal_speed,
                                slider_adaptor_speed,
                                label_manual,
                                label_horizontal_speed_slider,
                                label_vertical_speed_slider,
                                label_adaptor_speed_slider,
                                label_visualize_vertical_speed,
                                label_visualize_horizontal_speed,
                                label_visualize_rotation_speed]

        btn_back = button_generate(self, BUTTON_BACK_VALUE_X, BUTTON_BACK_VALUE_Y, "Back")
        btn_back.configure(command = lambda : self.button_back_click(btn_back, list_items_to_delete))

    def __init__(self, master, **kwargs):
        """! Initialisation of a Home Page Frame
        """
        super().__init__(master, **kwargs)
    
        btn_manual_mode = button_generate(self, BUTTON_MANUAL_MODE_X, BUTTON_MANUAL_MODE_Y, "Manual Mode")
        btn_auto_mode   = button_generate(self, BUTTON_AUTO_MODE_X, BUTTON_AUTO_MODE_Y, "Automatic mode")


        btn_manual_mode.configure(command = lambda : self.button_manual_mode_click(btn_auto_mode, btn_manual_mode))
        btn_auto_mode.configure(command = lambda : self.button_start_auto_mode_click(btn_auto_mode, btn_manual_mode))

        ## Start thread to read data rx buffer
        # Continous read of the serial communication RX data
        thread_rx_data = Thread(target = self.read_rx_buffer, args = (app.home_page_stop_threads_event, ))
        thread_rx_data.start()