##
# @file
# home_page.py
#
# @brief
# This file acts as the setup file for the home page of the GUI. \n
# All its components and callback functions will be defined here.

# Imports
import customtkinter
from serial.tools import list_ports
from threading import Thread
from threading import Event
from CTkMessagebox import CTkMessagebox
import time

import serial_funcs
import app
from common import button_generate, entry_generate, label_generate, combobox_generate, slider_generate

## Global constants
## The width and height of the home page
HOME_PAGE_WIDTH     = 1450
HOME_PAGE_HEIGHT    = 1500

## Info about the combobox ports
CBBOX_COM_PORTS_X   = 20
CBBOX_COM_PORTS_Y   = 20
CBBOX_WIDTH         = 175

## Info about the encoders values placeholders
LABEL_ENCODER_VERTICAL_LEFT_VALUE_X = 215
LABEL_ENCODER_VERTICAL_LEFT_VALUE_Y = 700

INDEX_LABEL_ENCODER_VERTICAL_LEFT   = 0
INDEX_LABEL_ENCODER_VERTICAL_RIGHT  = 1
INDEX_LABEL_ENCODER_HORIZONTAL      = 2

BUTTON_DIRECTION_CENTER_X   = 400
BUTTON_DIRECTION_CENTER_Y   = 250

## Info about the vertical speed slider
SLIDER_VERTICAL_SPEED_X                 = BUTTON_DIRECTION_CENTER_X + 350
SLIDER_VERTICAL_SPEED_Y                 = BUTTON_DIRECTION_CENTER_Y - 50
SLIDER_VERTICAL_SPEED_PREV_VALUE_INDEX  = 0
SLIDER_VERTICAL_SPEED_RANGE_MAX         = 100

## Info about the horizontal speed slider
SLIDER_HORIZONTAL_SPEED_X                   = BUTTON_DIRECTION_CENTER_X + 350
SLIDER_HORIZONTAL_SPEED_Y                   = BUTTON_DIRECTION_CENTER_Y + 50
SLIDER_HORIZONTAL_SPEED_PREV_VALUE_INDEX    = 0
SLIDER_HORIZONTAL_SPEED_RANGE_MAX           = 100

BUTTON_MANUAL_MODE_X        = 20
BUTTON_MANUAL_MODE_Y        = 100
BUTTON_AUTO_MODE_X          = 20 
BUTTON_AUTO_MODE_Y          = BUTTON_MANUAL_MODE_Y + 100

## Info about the Return button
BUTTON_BACK_VALUE_X = 1000
BUTTON_BACK_VALUE_Y = 60

## Info about the entry textbox for position control
ASK_ENTRY_VALUE_X = 200
ASK_ENTRY_VALUE_Y = 300

COMBOBOX_MOVEMENT_1_X = 100
COMBOBOX_MOVEMENT_1_Y = 200

LABEL_NUMBER_REPS_X = COMBOBOX_MOVEMENT_1_X + 700
LABEL_NUMBER_REPS_Y = COMBOBOX_MOVEMENT_1_Y + 150

## Maximal values we can travel to
MAX_HORIZONTAL  = 400
MAX_VERTICAL    = 400
MAX_SCREW       = 50

CHECKPOINT_A = 0
CHECKPOINT_B = 1

INDEX_MOVEMENT_UP       = 0
INDEX_MOVEMENT_DOWN     = 1
INDEX_MOVEMENT_RIGHT    = 2
INDEX_MOVEMENT_LEFT     = 3

## Global variables
list_buttons_manual_control = []
list_movement_entries = ["Up to down", "Down to up", "Left to right", "Right to left","Screw up to screw down", "Screw down to screw up"]

## Classes
class HomePageFrame(customtkinter.CTkFrame):
    """! Home page class for the Zimmer Test Bench\n
    Defines the components and callback functions of the home page
    """
    list_slider_vertical_info = [0]
    list_slider_horizontal_info = [0]
    current_checkpoint_to_reach = 1
    list_movement_entries = ["Up to down", "Down to up", "Right to left", "Left to right","Screw up to screw down", "Screw down to screw up"]


    flag_is_auto_thread_stopped = False
    flag_auto_thread_created_once = False

    counter_repetitions = 0

    def read_rx_buffer(self, stop_event):
        """! Threaded function to receive data in a continuous stream\n
        Sleeps for 10ms to match the send rate of the uC
        @param list_labels      List of labels that are meant to be updated periodically
        """
        while (stop_event.is_set() != True):
            serial_funcs.receive_serial_data(
                                                serial_funcs.g_list_message_info,
                                                serial_funcs.g_list_connected_device_info)

            time.sleep(0.01)

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

        while (stop_event.is_set() != True):
            self.counter_repetitions = self.counter_repetitions + 1
            while (serial_funcs.g_list_message_info[serial_funcs.INDEX_STATUS_MOTOR] == serial_funcs.MOTOR_STATE_AUTO_IN_TRAJ):
                pass

            if ((serial_funcs.g_list_message_info[serial_funcs.INDEX_STATUS_MOTOR] == serial_funcs.MOTOR_STATE_AUTO_END_OF_TRAJ) and (self.current_checkpoint_to_reach == 1)):
                serial_funcs.transmit_serial_data(
                                                    id,
                                                    command_b,
                                                    serial_funcs.MODE_POSITION_CONTROL,
                                                    position_to_reach,
                                                    serial_funcs.g_list_connected_device_info)

                self.current_checkpoint_to_reach = 0

            elif ((serial_funcs.g_list_message_info[serial_funcs.INDEX_STATUS_MOTOR] == serial_funcs.MOTOR_STATE_AUTO_END_OF_TRAJ) and (self.current_checkpoint_to_reach == 0)):
                serial_funcs.transmit_serial_data(
                                                    id,
                                                    command_a,
                                                    serial_funcs.MODE_POSITION_CONTROL,
                                                    position_to_reach,
                                                    serial_funcs.g_list_connected_device_info)

                self.current_checkpoint_to_reach = 1
                self.counter_repetitions = self.counter_repetitions + 1

            label_reps.configure(text = str(self.counter_repetitions))

            time.sleep(0.1)

        if (stop_event.is_set() == True):
            self.counter_repetitions = -99
            label_reps.configure(text = str(self.counter_repetitions))

    def combobox_com_ports_generate(frame, strvar_com_port_placeholder):
        """! Creates a combobox to list out all COM ports currently used by computer
        @param frame                    Frame on which the combobox will appear
        @param com_port_placeholder     StringVar to contain the combobox current text
        @return An instance of the created combobox
        """
        com_ports = list_ports.comports()
        list_com_ports = []
        
        if (len(com_ports) != 0):
            for port in com_ports:
                list_com_ports.append(port.name)
        else:
            list_com_ports += ["No COM Port detected"]

        combobox = customtkinter.CTkComboBox(
                                            master      = frame,
                                            width       = CBBOX_WIDTH,
                                            values      = list_com_ports,
                                            variable    = strvar_com_port_placeholder)
        combobox.place(
                        x = CBBOX_COM_PORTS_X,
                        y = CBBOX_COM_PORTS_Y)

        return combobox

    def button_com_ports_click(self, combobox_com_port, list_com_device_info):
        """! On click, prints out the current value of the COM ports combobox
        @param combobox_com_port    StringVar containing the current COM port selected
        @param list_com_device_info Notable information for all connected devices
        """
        if (combobox_com_port != ""):
            print("COM port to be connected: ", combobox_com_port)
            list_com_device_info[0] = serial_funcs.connect_to_port(combobox_com_port)
        else:
            print("No COM port selected")

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
    
    def button_back_click(self, btn_back, list):
        # Destroy all previous components generated beforehand
        btn_back.place_forget() 

        for i in range(len(list)):
            list[i].place_forget()

        # Generate button modes 
        btn_manual_mode = button_generate(self, BUTTON_MANUAL_MODE_X, BUTTON_MANUAL_MODE_Y, "Manual Mode")
        btn_manual_mode.configure(command=lambda:self.button_manual_mode_click(btn_auto_mode, btn_manual_mode))

        btn_auto_mode = button_generate(self, BUTTON_AUTO_MODE_X, BUTTON_AUTO_MODE_Y, "Automatic mode")
        btn_auto_mode.configure(command = lambda : self.button_start_auto_mode_click(btn_auto_mode, btn_manual_mode))

    def button_submit_click(self, button_submit, entry_position, combobox_direction, label_reps):
        # Get user input
        desired_position = int(entry_position.get())
        desired_direction = combobox_direction.get()

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
            if (button_submit.cget("text") == "Submit"): 
                button_submit.configure(text = "Stop", fg_color = '#EE3B3B')
            else:
                button_submit.configure(text = "Submit", fg_color = '#66CD00')

            # Default thread
            thread_auto_mode = Thread(target = self.auto_mode, args = (desired_position, desired_direction, label_reps, app.home_page_auto_mode_thread_event, ))

            if (self.flag_auto_thread_created_once == False):
                thread_auto_mode.start()

                self.flag_auto_thread_created_once = True
            else:
                if (self.flag_is_auto_thread_stopped == True):
                    app.home_page_auto_mode_thread_event.clear()

                    thread_auto_mode = None
                    thread_auto_mode = Thread(target = self.auto_mode, args = (desired_position, desired_direction,  label_reps, app.home_page_auto_mode_thread_event, ))
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
        # Position control input values
        combobox_movement = customtkinter.CTkOptionMenu(
                                                        master = self,
                                                        values = self.list_movement_entries, 
                                                        dynamic_resizing = False)
        combobox_movement.set("Choose movement")
        combobox_movement.place(x = COMBOBOX_MOVEMENT_1_X, y = COMBOBOX_MOVEMENT_1_Y)

        
        entry_desired_position = entry_generate(self, COMBOBOX_MOVEMENT_1_X + 200, COMBOBOX_MOVEMENT_1_Y, "Enter here")
        label_desired_position = label_generate(self, COMBOBOX_MOVEMENT_1_X + 200, COMBOBOX_MOVEMENT_1_Y - 30, "Amplitude (mm)")

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
        label_number_reps = label_generate(self, LABEL_NUMBER_REPS_X + 100, LABEL_NUMBER_REPS_Y, "")

        btn_submit  = button_generate(self, COMBOBOX_MOVEMENT_1_X + 700, COMBOBOX_MOVEMENT_1_Y + 75, "Submit")
        btn_submit.configure(command = lambda : self.button_submit_click(btn_submit, entry_desired_position, combobox_movement, label_number_reps), fg_color = '#66CD00')

        
    
        # Return button configuration
        list_items_to_delete = [
                                label_desired_position,
                                entry_desired_position,
                                slider_horizontal_speed,
                                slider_vertical_speed,
                                combobox_movement,
                                btn_submit,
                                label_number_reps,
                                label_number_reps_indicator,
                                label_horizontal_speed_slider,
                                label_visualize_vertical_speed, 
                                label_visualize_horizontal_speed,
                                label_vertical_speed_slider]

        btn_back  = button_generate(self, BUTTON_BACK_VALUE_X, BUTTON_BACK_VALUE_Y, "Back")
        btn_back.configure(command = lambda : self.button_back_click(btn_back, list_items_to_delete))

    def button_manual_mode_click(self,  button_manual_mode, button_auto_mode):
        # Delete mode selection buttons
        button_manual_mode.place_forget()
        button_auto_mode.place_forget()

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
        label_visualize_vertical_speed      = label_generate(self, SLIDER_VERTICAL_SPEED_X + 200, SLIDER_VERTICAL_SPEED_Y - 5, "20 mm/s")
        label_visualize_horizontal_speed    = label_generate(self, SLIDER_HORIZONTAL_SPEED_X + 200, SLIDER_HORIZONTAL_SPEED_Y - 5, "20 mm/s")
        
        slider_vertical_speed = slider_generate(self, SLIDER_VERTICAL_SPEED_X, BUTTON_DIRECTION_CENTER_Y - 50, SLIDER_VERTICAL_SPEED_RANGE_MAX)
        slider_vertical_speed.configure(command = lambda slider_value = slider_vertical_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_vertical_info,
                                                                                                                                "Vertical",
                                                                                                                                label_visualize_vertical_speed,
                                                                                                                                serial_funcs.g_list_connected_device_info))

        slider_horizontal_speed = slider_generate(self, SLIDER_HORIZONTAL_SPEED_X, BUTTON_DIRECTION_CENTER_Y + 50, SLIDER_HORIZONTAL_SPEED_RANGE_MAX)
        slider_horizontal_speed.configure(command = lambda slider_value = slider_horizontal_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_horizontal_info,
                                                                                                                                "Horizontal",
                                                                                                                                label_visualize_horizontal_speed,
                                                                                                                                serial_funcs.g_list_connected_device_info))

        label_vertical_speed_slider     = label_generate(self, SLIDER_VERTICAL_SPEED_X, BUTTON_DIRECTION_CENTER_Y - 80, "Vertical Speed (mm/s)")
        label_horizontal_speed_slider   = label_generate(self, SLIDER_HORIZONTAL_SPEED_X, BUTTON_DIRECTION_CENTER_Y + 20, "Horizontal speed (mm/s)")

        # Generate return button and items to delete when pressed
        list_items_to_delete = [
                                btn_direction_up, 
                                btn_direction_down, 
                                btn_direction_left,
                                btn_direction_right,
                                slider_vertical_speed,
                                slider_horizontal_speed,
                                label_horizontal_speed_slider,
                                label_vertical_speed_slider,
                                label_visualize_vertical_speed,
                                label_visualize_horizontal_speed]

        btn_back = button_generate(self, BUTTON_BACK_VALUE_X, BUTTON_BACK_VALUE_Y, "Back")
        btn_back.configure(command = lambda : self.button_back_click(btn_back, list_items_to_delete))

    def __init__(self, master, **kwargs):
        """! Initialisation of a Home Page Frame
        """
        super().__init__(master, **kwargs)

        # Stores the current selected COM port in the combobox
        strvar_current_com_port = customtkinter.StringVar(self)

        # Generate all comboboxes
        cbbox_com_ports = self.combobox_com_ports_generate(strvar_current_com_port)

        # Generate all buttons
        btn_com_ports = button_generate(self, (CBBOX_COM_PORTS_X * 12), CBBOX_COM_PORTS_Y, "Connect")
        btn_com_ports.configure(command = lambda : self.button_com_ports_click(
                                                                                cbbox_com_ports.get(),
                                                                                serial_funcs.g_list_connected_device_info))
    
        btn_manual_mode = button_generate(self, BUTTON_MANUAL_MODE_X, BUTTON_MANUAL_MODE_Y, "Manual Mode")
        btn_auto_mode   = button_generate(self, BUTTON_AUTO_MODE_X, BUTTON_AUTO_MODE_Y, "Automatic mode")

        btn_manual_mode.configure(command = lambda : self.button_manual_mode_click(btn_auto_mode, btn_manual_mode))
        btn_auto_mode.configure(command = lambda : self.button_start_auto_mode_click(btn_auto_mode, btn_manual_mode))

        ## Start thread to read data rx buffer
        # Continous read of the serial communication RX data
        thread_rx_data = Thread(target = self.read_rx_buffer, args = (app.home_page_stop_threads_event, ))
        thread_rx_data.start()