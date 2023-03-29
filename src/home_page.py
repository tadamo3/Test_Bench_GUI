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
from common import button_generate, entry_generate, label_generate, combobox_generate, slider_generate

## Global constants
## The width and height of the home page
HOME_PAGE_WIDTH     = 1450
HOME_PAGE_HEIGHT    = 1500

## Info about the combobox ports
CBBOX_COM_PORTS_X   = 20
CBBOX_COM_PORTS_Y   = 20
CBBOX_WIDTH         = 175

## Info about the vertical speed slider
SLIDER_VERTICAL_SPEED_X                 = 20
SLIDER_VERTICAL_SPEED_Y                 = 500
SLIDER_VERTICAL_SPEED_PREV_VALUE_INDEX  = 0
SLIDER_VERTICAL_SPEED_RANGE_MAX         = 100

## Info about the horizontal speed slider
SLIDER_HORIZONTAL_SPEED_X                   = 20
SLIDER_HORIZONTAL_SPEED_Y                   = 575
SLIDER_HORIZONTAL_SPEED_PREV_VALUE_INDEX    = 0
SLIDER_HORIZONTAL_SPEED_RANGE_MAX           = 100

## Info about the encoders values placeholders
LABEL_ENCODER_VERTICAL_LEFT_VALUE_X = 215
LABEL_ENCODER_VERTICAL_LEFT_VALUE_Y = 700

INDEX_LABEL_ENCODER_VERTICAL_LEFT   = 0
INDEX_LABEL_ENCODER_VERTICAL_RIGHT  = 1
INDEX_LABEL_ENCODER_HORIZONTAL      = 2

## Info about the manual control direction buttons
BUTTON_DIRECTION_CENTER_X   = 500
BUTTON_DIRECTION_CENTER_Y   = 300
BUTTON_MANUAL_MODE_X        = 350
BUTTON_MANUAL_MODE_Y        = 300
BUTTON_AUTO_MODE_X          = 650 
BUTTON_AUTO_MODE_Y          = 300

## Info about the Return button
BUTTON_BACK_VALUE_X = 1000
BUTTON_BACK_VALUE_Y = 60

## Info about the entry textbox for position control
ASK_ENTRY_VALUE_X = 400
ASK_ENTRY_VALUE_Y = 300

## Maximal values we can travel to
MAX_HORIZONTAL  = 30
MAX_VERTICAL    = 30

CHECKPOINT_A = 0
CHECKPOINT_B = 1

INDEX_ENTRY_VERTICAL_MOVEMENT   = 0
INDEX_ENTRY_HORIZONTAL_MOVEMENT = 1

## Global variables
# Event variable is false by default
home_page_stop_threads_event = Event()

## Classes
class HomePageFrame(customtkinter.CTkFrame):
    """! Home page class for the Zimmer Test Bench\n
    Defines the components and callback functions of the home page
    """
    list_slider_vertical_info = [0]
    list_slider_horizontal_info = [0]
    list_positions_to_reach = [50, 80]
    current_checkpoint_to_reach = 0
    list_movement_entries = [0, 0]

    def read_rx_buffer(self, list_labels):
        """! Threaded function to receive data in a continuous stream\n
        Sleeps for 10ms to match the send rate of the uC
        @param list_labels      List of labels that are meant to be updated periodically
        """
        while (home_page_stop_threads_event.is_set() != True):
            serial_funcs.receive_serial_data(
                                                serial_funcs.g_list_message_info,
                                                serial_funcs.g_list_connected_device_info)

            self.update_labels_encoders(list_labels)

            time.sleep(0.01)

    def auto_mode(self):
        serial_funcs.transmit_serial_data(
                                            serial_funcs.ID_MOTOR_VERTICAL_LEFT,
                                            serial_funcs.COMMAND_MOTOR_HORIZONTAL_LEFT,
                                            serial_funcs.MODE_POSITION_CONTROL,
                                            self.list_positions_to_reach[0],
                                            serial_funcs.g_list_connected_device_info)
        while (home_page_stop_threads_event.is_set() != True):
            if ((serial_funcs.g_list_message_info[serial_funcs.INDEX_STATUS_MOVEMENT_MOTOR] == serial_funcs.MOTOR_STATE_AUTO_END_OF_TRAJ) and (self.current_checkpoint_to_reach == 1)):
                time.sleep(1)

                serial_funcs.transmit_serial_data(
                                                    serial_funcs.ID_MOTOR_VERTICAL_LEFT,
                                                    serial_funcs.COMMAND_MOTOR_HORIZONTAL_LEFT,
                                                    serial_funcs.MODE_POSITION_CONTROL,
                                                    self.list_positions_to_reach[0],
                                                    serial_funcs.g_list_connected_device_info)

                self.current_checkpoint_to_reach = 0

            elif ((serial_funcs.g_list_message_info[serial_funcs.INDEX_STATUS_MOVEMENT_MOTOR] == serial_funcs.MOTOR_STATE_AUTO_END_OF_TRAJ) and (self.current_checkpoint_to_reach == 0)):
                time.sleep(1)

                serial_funcs.transmit_serial_data(
                                                    serial_funcs.ID_MOTOR_VERTICAL_LEFT,
                                                    serial_funcs.COMMAND_MOTOR_HORIZONTAL_LEFT,
                                                    serial_funcs.MODE_POSITION_CONTROL,
                                                    self.list_positions_to_reach[1],
                                                    serial_funcs.g_list_connected_device_info)

                self.current_checkpoint_to_reach = 1

            time.sleep(0.1)


    def update_labels_encoders(self, list_labels):
        """! Updates Home Page frame labels according to the information received from the STM32 feedback
        @param list_labels      List of labels that are meant to be updated periodically
        """
        id = serial_funcs.g_list_message_info[serial_funcs.INDEX_ID]

        if (id <= serial_funcs.ID_ENCODER_HORIZONTAL):
            # We decrement by 1 because the id of encoders are shifted of 1 (reason being the 0 value is reserved)
            id = id - 1
            list_labels[id].configure(text = str(serial_funcs.g_list_message_info[serial_funcs.INDEX_MOTOR_POSITION]))

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

    def slider_speed_callback(self, slider_value, list_slider_info, list_com_device_info):
        """! Every time a new value is set, sends the updated speed value to the device
        @param slider_value         The selected speed value for the vertical motor speed
        @param list_slider_info     Notable information for a specific slider
        @param list_com_device_info Notable information for all connected devices
        """
        if (list_com_device_info[0] != 0):
            slider_value = round(slider_value)
            previous_slider_value = round(list_slider_info[SLIDER_VERTICAL_SPEED_PREV_VALUE_INDEX])

            if (slider_value != previous_slider_value):
                serial_funcs.transmit_serial_data(
                                                    serial_funcs.ID_MOTOR_VERTICAL_LEFT,
                                                    serial_funcs.COMMAND_MOTOR_CHANGE_SPEED,
                                                    serial_funcs.MODE_CHANGE_PARAMS,
                                                    slider_value,
                                                    list_com_device_info)

                print(slider_value)
                list_slider_info[SLIDER_VERTICAL_SPEED_PREV_VALUE_INDEX] = slider_value
    
    def button_back_click(self, btn_back, list):
        # Destroy all previous components generated beforehand
        btn_back.place_forget() 

        for i in range(len(list)): 
            list[i].place_forget()

        # Generate button modes 
        btn_manual_mode = button_generate(self, BUTTON_MANUAL_MODE_X,BUTTON_MANUAL_MODE_Y, "Manual Mode")
        btn_manual_mode.configure(command=lambda:self.manual_mode_clicked(btn_auto_mode,btn_manual_mode))

        btn_auto_mode = button_generate(self, BUTTON_AUTO_MODE_X, BUTTON_AUTO_MODE_Y, "Automatic mode")
        btn_auto_mode.configure(command = lambda : self.button_start_auto_mode_click(serial_funcs.g_list_connected_device_info,btn_auto_mode,btn_manual_mode))

    def combobox_motion_callback(self, movement, label_to_modify):
        if (movement == "Vertical"):
            label_to_modify.configure(text = "Vertical movement (mm)")

        elif (movement == "Horizontal"):
            label_to_modify.configure(text = "Horizontal movement (mm)")

        elif (movement == "Vertical/Horizontal"):
            label_to_modify.configure(text = "asdf (mm)")
    
        elif (movement == "Screw"):
            label_to_modify.configure(text = "Screw pitch (mm)")

    def button_start_auto_mode_click(self, list_com_device_info, mode1, mode2):
        # Destroy the modes buttons  
        mode1.place_forget()
        mode2.place_forget()

        # Generate components 
        slider_vertical_speed = slider_generate(self, ASK_ENTRY_VALUE_X + 100, SLIDER_VERTICAL_SPEED_Y - 100, SLIDER_VERTICAL_SPEED_RANGE_MAX)
        slider_vertical_speed.configure(command = lambda slider_value = slider_vertical_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_vertical_info,
                                                                                                                                serial_funcs.g_list_connected_device_info))

        slider_horizontal_speed = slider_generate(self, ASK_ENTRY_VALUE_X + 100, SLIDER_HORIZONTAL_SPEED_Y - 100, SLIDER_HORIZONTAL_SPEED_RANGE_MAX)
        slider_horizontal_speed.configure(command = lambda slider_value = slider_horizontal_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_horizontal_info,
                                                                                                                                serial_funcs.g_list_connected_device_info))

        label_vertical_speed_slider     = label_generate(self, ASK_ENTRY_VALUE_X + 100, SLIDER_VERTICAL_SPEED_Y - 130, "Vertical Speed (mm/s)")
        label_horizontal_speed_slider   = label_generate(self, ASK_ENTRY_VALUE_X + 100, SLIDER_HORIZONTAL_SPEED_Y - 130, "Horizontal speed (mm/s)")
        
        # Position control input values
        entry_desired_position = entry_generate(self, ASK_ENTRY_VALUE_X + 100, ASK_ENTRY_VALUE_Y, "Enter here")
        label_desired_position = label_generate(self, ASK_ENTRY_VALUE_X + 100, ASK_ENTRY_VALUE_Y - 50, "Vertical movement (mm)")

        combobox_motion = customtkinter.CTkOptionMenu(
                                                        master = self,
                                                        values = ["Vertical", "Horizontal", "Vertical/Horizontal", "Screw"], 
                                                        dynamic_resizing = True)                                            
        combobox_motion.set("Choose movement")
        combobox_motion.configure(command = lambda movement = combobox_motion.get() : self.combobox_motion_callback(movement, label_desired_position))
        combobox_motion.place(x = ASK_ENTRY_VALUE_X - 100, y = ASK_ENTRY_VALUE_Y)

        btn_submit  = button_generate(self, ASK_ENTRY_VALUE_X + 300, ASK_ENTRY_VALUE_Y, "Submit")
        btn_submit.configure(command = lambda : self.submit_clicked(entry_desired_position, combobox_motion))

        # Return button configuration
        list_auto = [label_desired_position, entry_desired_position,combobox_motion, slider_horizontal_speed, slider_vertical_speed, btn_submit, label_horizontal_speed_slider, label_vertical_speed_slider]
        btn_back  = button_generate(self, BUTTON_BACK_VALUE_X, BUTTON_BACK_VALUE_Y, "Back")
        btn_back.configure(command = lambda : self.button_back_click(btn_back, list_auto))

    def manual_mode_clicked(self,  mode1, mode2):
        mode1.place_forget()
        mode2.place_forget()

        ## Generate direction buttons 
        btn_direction_up = button_generate(self, BUTTON_DIRECTION_CENTER_X, (BUTTON_DIRECTION_CENTER_Y - 100), "Going Up")
        btn_direction_up.configure(state = "disabled")
            
        btn_direction_down = button_generate(self, BUTTON_DIRECTION_CENTER_X, (BUTTON_DIRECTION_CENTER_Y + 100), "Going Down")
        btn_direction_down.configure(state = "disabled")

        btn_direction_left = button_generate(self, (BUTTON_DIRECTION_CENTER_X - 100), BUTTON_DIRECTION_CENTER_Y, "Going Left")
        btn_direction_left.configure(state = "disabled")

        btn_direction_right = button_generate(self, (BUTTON_DIRECTION_CENTER_X + 100), BUTTON_DIRECTION_CENTER_Y, "Going Right")
        btn_direction_right.configure(state = "disabled")

        ## Generate sliders 
        slider_vertical_speed = slider_generate(self, SLIDER_VERTICAL_SPEED_X, BUTTON_DIRECTION_CENTER_Y - 50, SLIDER_VERTICAL_SPEED_RANGE_MAX)
        slider_vertical_speed.configure(command = lambda slider_value = slider_vertical_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_vertical_info,
                                                                                                                                serial_funcs.g_list_connected_device_info))

        slider_horizontal_speed = slider_generate(self, SLIDER_HORIZONTAL_SPEED_X, BUTTON_DIRECTION_CENTER_Y + 50, SLIDER_HORIZONTAL_SPEED_RANGE_MAX)
        slider_horizontal_speed.configure(command = lambda slider_value = slider_horizontal_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_horizontal_info,
                                                                                                                                serial_funcs.g_list_connected_device_info))
        label_vertical_speed_slider = label_generate(self, SLIDER_VERTICAL_SPEED_X, BUTTON_DIRECTION_CENTER_Y - 80, "Vertical Speed (mm/s)")
        label_horizontal_speed_slider = label_generate(self, SLIDER_HORIZONTAL_SPEED_X, BUTTON_DIRECTION_CENTER_Y + 20, "Horizontal speed (mm/s)")
        
        list_btn_manual = [btn_direction_up,btn_direction_down,btn_direction_left,btn_direction_right, slider_vertical_speed, slider_horizontal_speed,label_horizontal_speed_slider, label_vertical_speed_slider]
            
        ## Generate back button 
        btn_back  = button_generate(self, BUTTON_BACK_VALUE_X, BUTTON_BACK_VALUE_Y, "Back")
        btn_back.configure(command = lambda : self.button_back_click(btn_back, list_btn_manual))

    
    def submit_clicked(self,position_entry, direction_entry): 
        # Get desired position and direction
        # desired_position = position_entry.get()  
        # desired_direction = direction_entry.get()
        pass 
        # # Check information 
        # if (desired_direction == 'Horizontal' & desired_position > MAX_HORIZONTAL): 
        #     message_err_input = CTkMessagebox(title="Error", message="Desired position not possible", icon="cancel")
        # if (desired_direction == 'Vertical' & desired_position > MAX_VERTICAL): 
        #     message_err_input = CTkMessagebox(title="Error", message="Desired position not possible", icon="cancel")

    def __init__(self, master, **kwargs):
        """! Initialisation of a Home Page Frame
        """
        super().__init__(master, **kwargs)

        ## Stores the current selected COM port in the combobox
        strvar_current_com_port = customtkinter.StringVar(self)

        ## Generate all comboboxes
        cbbox_com_ports = self.combobox_com_ports_generate(strvar_current_com_port)

        ## Generate all buttons
        btn_com_ports = button_generate(self, (CBBOX_COM_PORTS_X * 12), CBBOX_COM_PORTS_Y, "Connect")
        btn_com_ports.configure(command = lambda : self.button_com_ports_click(
                                                                                cbbox_com_ports.get(),
                                                                                serial_funcs.g_list_connected_device_info))
    
        btn_manual_mode = button_generate(self, BUTTON_MANUAL_MODE_X,BUTTON_MANUAL_MODE_Y, "Manual Mode")
        btn_auto_mode = button_generate(self, BUTTON_AUTO_MODE_X, BUTTON_AUTO_MODE_Y, "Automatic mode")
        btn_manual_mode.configure(command=lambda:self.manual_mode_clicked(btn_auto_mode,btn_manual_mode))
        btn_auto_mode.configure(command = lambda : self.button_start_auto_mode_click(serial_funcs.g_list_connected_device_info,btn_auto_mode,btn_manual_mode))


        ## Generate all labels
        label_encoder_vertical_left_value = label_generate(self, LABEL_ENCODER_VERTICAL_LEFT_VALUE_X, LABEL_ENCODER_VERTICAL_LEFT_VALUE_Y, "12345")
        label_encoder_1_indication = label_generate(self, (LABEL_ENCODER_VERTICAL_LEFT_VALUE_X - 200), LABEL_ENCODER_VERTICAL_LEFT_VALUE_Y, "Vertical Motor Position (mm): ")

        label_encoder_vertical_right_value = label_generate(self, LABEL_ENCODER_VERTICAL_LEFT_VALUE_X, LABEL_ENCODER_VERTICAL_LEFT_VALUE_Y + 50, "12345")
        label_encoder_1_indication = label_generate(self, (LABEL_ENCODER_VERTICAL_LEFT_VALUE_X - 200), LABEL_ENCODER_VERTICAL_LEFT_VALUE_Y + 50, "Horizontal Motor Position (mm): ")

        # label_vertical_speed_slider = label_generate(self, SLIDER_VERTICAL_SPEED_X, SLIDER_VERTICAL_SPEED_Y - 30, "Vertical Speed (mm/s)")
        # label_horizontal_speed_slider = label_generate(self, SLIDER_HORIZONTAL_SPEED_X, SLIDER_HORIZONTAL_SPEED_Y - 30, "Horizontal speed (mm/s)")

        list_label = [label_encoder_vertical_left_value, label_encoder_vertical_right_value]

        ## Start thread to read data rx buffer
        # Continous read of the serial communication RX data
        thread_rx_data = Thread(target = self.read_rx_buffer, args = (list_label,))
        thread_rx_data.start()