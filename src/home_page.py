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
import time

import serial_funcs

# Global constants
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

SLIDER_HORIZONTAL_SPEED_X                   = 20
SLIDER_HORIZONTAL_SPEED_Y                   = 575
SLIDER_HORIZONTAL_SPEED_PREV_VALUE_INDEX    = 0
SLIDER_HORIZONTAL_SPEED_RANGE_MAX           = 100

LABEL_ENCODER_VERTICAL_LEFT_VALUE_X = 215
LABEL_ENCODER_VERTICAL_LEFT_VALUE_Y = 700

BUTTON_DIRECTION_CENTER_X = 500
BUTTON_DIRECTION_CENTER_Y = 200

BUTTON_BACK_VALUE_X = 1000
BUTTON_BACK_VALUE_Y = 60

ASK_ENTRY_VALUE_X = 550
ASK_ENTRY_VALUE_Y = 200

ID_NONE         = 0
COMMAND_NONE    = 0
DATA_NONE       = 0

INDEX_LABEL_ENCODER_VERTICAL_LEFT = 0
INDEX_LABEL_ENCODER_VERTICAL_RIGHT = 1
INDEX_LABEL_ENCODER_HORIZONTAL = 2

INDEX_MANUAL_MODE = 1
INDEX_AUTOMATIC_MODE = 2

## Global variables
# Event variable is false by default
home_page_stop_threads_event = Event()

# Classes
class HomePageFrame(customtkinter.CTkFrame):
    """! Home page class for the Zimmer Test Bench\n
    Defines the components and callback functions of the home page
    """
    list_slider_vertical_info = [0]
    list_slider_horizontal_info = [0]

    def read_rx_buffer(self, list_labels):
        """! Inserts in the task queue the message sent by the STM32 over serial communication\n
        Sleeps for 500ms to keep a reasonable update rate
        @param list_labels      List of labels that are meant to be updated periodically
        """
        while (home_page_stop_threads_event.is_set() != True):
            serial_funcs.receive_serial_data(
                                                serial_funcs.g_list_message_info,
                                                serial_funcs.g_list_connected_device_info)

            self.update_labels_encoders(list_labels)

            time.sleep(0.01)

    def update_labels_encoders(self, list_labels):
        """! Updates Home Page frame labels according to the information received from the STM32 feedback
        @param list_labels      List of labels that are meant to be updated periodically
        """
        id = serial_funcs.g_list_message_info[serial_funcs.INDEX_ID]

        # We decrement by one because the id of encoders are shifted of 1 (1, 2, 3 instead of list positioning 0, 1, 2)
        list_labels[id - 1].configure(text = str(serial_funcs.g_list_message_info[serial_funcs.INDEX_DATA])) 

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

    def button_generate(self, button_pos_x, button_pos_y, text):
        button = customtkinter.CTkButton(
                                            master = self,
                                            text = text)
        
        button.place(
                        x = button_pos_x,
                        y = button_pos_y)

        
        return button
    
    def combobox_generate(self,combobox_pos_x, combobox_pos_y,text): 
        combobox = customtkinter.CTkComboBox(
                                               master = self,
                                               values = text, 
                                               dynamic_resizing = True
                                            )
        
      

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

    def slider_generate(self, slider_pos_x, slider_pos_y, range):
        slider = customtkinter.CTkSlider(
                                            master          = self,
                                            from_           = 0,
                                            to              = range,
                                            number_of_steps = range)
        slider.place(
                        x = slider_pos_x,
                        y = slider_pos_y)

        return slider

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
                                                    slider_value,
                                                    list_com_device_info)
                list_slider_info[SLIDER_VERTICAL_SPEED_PREV_VALUE_INDEX] = slider_value

    def label_generate(self, label_pos_x, label_pos_y, text):
        label = customtkinter.CTkLabel(
                                        master          = self,
                                        text            = text,
                                        corner_radius   = 8)
        
        label.place(
                    x = label_pos_x,
                    y = label_pos_y)

        return label
    
    def entry_generate(self, label_pos_x, label_pos_y, text):
        entry = customtkinter.CTkEntry(
                                            master = self,
                                            placeholder_text= text)
        
        entry.place(
                        x = label_pos_x,
                        y = label_pos_y+30)
        
        return entry
    

    def back_clicked(self, btn_back, list): 
        
        ## Destroy the back button
        btn_back.place_forget() 

        ## Destroy any button that are generated in the modes
        for i in range(len(list)): 
            list[i].place_forget()

        ## Generate button modes 
        btn_manual_mode = self.button_generate(200,200, "Manual Mode")
        btn_auto_mode = self.button_generate((BUTTON_DIRECTION_CENTER_X), BUTTON_DIRECTION_CENTER_Y, "Automatic mode")
        btn_manual_mode.configure(command=lambda:self.manual_mode_clicked(INDEX_MANUAL_MODE,btn_auto_mode,btn_manual_mode))
        btn_auto_mode.configure(command = lambda : self.button_start_auto_mode_click(serial_funcs.g_list_connected_device_info,btn_auto_mode,btn_manual_mode))


    def button_start_auto_mode_click(self, list_com_device_info,mode1,mode2):
        serial_funcs.transmit_serial_data(
                                            serial_funcs.ID_MOTOR_VERTICAL_LEFT,
                                            serial_funcs.COMMAND_MOTOR_HORIZONTAL_LEFT,
                                            serial_funcs.MODE_POSITION_CONTROL,
                                            serial_funcs.DATA_NONE,
                                            serial_funcs.g_list_connected_device_info)
        ## Destroy the modes buttons  
        mode1.place_forget()
        mode2.place_forget()

        ## Ask user for desired position in mm
        label_desired_position = self.label_generate(ASK_ENTRY_VALUE_X, ASK_ENTRY_VALUE_Y, "Enter desired position in mm")
        entry_desired_position = self.entry_generate(ASK_ENTRY_VALUE_X,ASK_ENTRY_VALUE_Y,"Enter here")
        
        ## Ask user the direction of the motion 
        combobox_motion = customtkinter.CTkOptionMenu(master = self,
                                               values = ["Horizontal", "Vertical"], 
                                               dynamic_resizing = True)
        combobox_motion.set("Choose direction")
        combobox_motion.place(x=ASK_ENTRY_VALUE_X,y=ASK_ENTRY_VALUE_Y+70)
        ## Get the desired position from the user 
        desired_position = entry_desired_position.get()
        ## Check input 

        

        ## Generate back button 
        list_auto = [label_desired_position,entry_desired_position,combobox_motion]
        btn_back  = self.button_generate(BUTTON_BACK_VALUE_X, BUTTON_BACK_VALUE_Y, "Back")
        btn_back.configure(command = lambda : self.back_clicked(btn_back, list_auto))

    def manual_mode_clicked(self, mode_index, mode1, mode2):
        # Action to take when the manuel mode is clicked 
        if (mode_index == INDEX_MANUAL_MODE):
            ## Destroy mode buttons 
            mode1.place_forget()
            mode2.place_forget()

            ## Generate direction buttons 
            btn_direction_up    = self.button_generate(BUTTON_DIRECTION_CENTER_X, (BUTTON_DIRECTION_CENTER_Y - 100), "Going Up")
            btn_direction_up.configure(state = "disabled")
            
            btn_direction_down  = self.button_generate(BUTTON_DIRECTION_CENTER_X, (BUTTON_DIRECTION_CENTER_Y + 100), "Going Down")
            btn_direction_down.configure(state = "disabled")

            btn_direction_left  = self.button_generate((BUTTON_DIRECTION_CENTER_X - 100), BUTTON_DIRECTION_CENTER_Y, "Going Left")
            btn_direction_left.configure(state = "disabled")

            btn_direction_right = self.button_generate((BUTTON_DIRECTION_CENTER_X + 100), BUTTON_DIRECTION_CENTER_Y, "Going Right")
            btn_direction_right.configure(state = "disabled")

            list_btn_manual = [btn_direction_up,btn_direction_down,btn_direction_left,btn_direction_right]
            
            ## Generate back button 
            btn_back  = self.button_generate(BUTTON_BACK_VALUE_X, BUTTON_BACK_VALUE_Y, "Back")
            btn_back.configure(command = lambda : self.back_clicked(btn_back, list_btn_manual))

            ## Generate sliders 
            slider_vertical_speed = self.slider_generate(SLIDER_VERTICAL_SPEED_X, SLIDER_VERTICAL_SPEED_Y, SLIDER_VERTICAL_SPEED_RANGE_MAX)
            slider_vertical_speed.configure(command = lambda slider_value = slider_vertical_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_vertical_info,
                                                                                                                                serial_funcs.g_list_connected_device_info))

            slider_horizontal_speed = self.slider_generate(SLIDER_HORIZONTAL_SPEED_X, SLIDER_HORIZONTAL_SPEED_Y, SLIDER_HORIZONTAL_SPEED_RANGE_MAX)
            slider_horizontal_speed.configure(command = lambda slider_value = slider_horizontal_speed.get() : self.slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_horizontal_info,
                                                                                                                                serial_funcs.g_list_connected_device_info))
            label_vertical_speed_slider = self.label_generate(SLIDER_VERTICAL_SPEED_X, SLIDER_VERTICAL_SPEED_Y - 30, "Vertical Speed (mm/s)")
            label_horizontal_speed_slider = self.label_generate(SLIDER_HORIZONTAL_SPEED_X, SLIDER_HORIZONTAL_SPEED_Y - 30, "Horizontal speed (mm/s)")
        
        if (mode_index != INDEX_MANUAL_MODE):
            # Error as this function is only for manual mode 
            print("Error in mode indexing")
    

    def __init__(self, master, **kwargs):
        """! Initialisation of a Home Page Frame
        """
        super().__init__(master, **kwargs)

        ## Stores the current selected COM port in the combobox
        strvar_current_com_port = customtkinter.StringVar(self)

        ## Generate all comboboxes
        cbbox_com_ports = self.combobox_com_ports_generate(strvar_current_com_port)

        ## Generate all buttons
        btn_com_ports = self.button_generate((CBBOX_COM_PORTS_X * 12), CBBOX_COM_PORTS_Y, "Connect")
        btn_com_ports.configure(command = lambda : self.button_com_ports_click(
                                                                                cbbox_com_ports.get(),
                                                                                serial_funcs.g_list_connected_device_info))
    
        btn_manual_mode = self.button_generate(200,200, "Manual Mode")
        btn_auto_mode = self.button_generate((BUTTON_DIRECTION_CENTER_X), BUTTON_DIRECTION_CENTER_Y, "Automatic mode")
        btn_manual_mode.configure(command=lambda:self.manual_mode_clicked(INDEX_MANUAL_MODE,btn_auto_mode,btn_manual_mode))
        btn_auto_mode.configure(command = lambda : self.button_start_auto_mode_click(serial_funcs.g_list_connected_device_info,btn_auto_mode,btn_manual_mode))


        ## Generate all labels
        label_encoder_vertical_left_value = self.label_generate(LABEL_ENCODER_VERTICAL_LEFT_VALUE_X, LABEL_ENCODER_VERTICAL_LEFT_VALUE_Y, "12345")
        label_encoder_1_indication = self.label_generate((LABEL_ENCODER_VERTICAL_LEFT_VALUE_X - 200), LABEL_ENCODER_VERTICAL_LEFT_VALUE_Y, "Vertical Motor Position (mm): ")

        label_encoder_vertical_right_value = self.label_generate(LABEL_ENCODER_VERTICAL_LEFT_VALUE_X, LABEL_ENCODER_VERTICAL_LEFT_VALUE_Y + 50, "12345")
        label_encoder_1_indication = self.label_generate((LABEL_ENCODER_VERTICAL_LEFT_VALUE_X - 200), LABEL_ENCODER_VERTICAL_LEFT_VALUE_Y + 50, "Horizontal Motor Position (mm): ")

        # label_vertical_speed_slider = self.label_generate(SLIDER_VERTICAL_SPEED_X, SLIDER_VERTICAL_SPEED_Y - 30, "Vertical Speed (mm/s)")
        # label_horizontal_speed_slider = self.label_generate(SLIDER_HORIZONTAL_SPEED_X, SLIDER_HORIZONTAL_SPEED_Y - 30, "Horizontal speed (mm/s)")

        list_label = [label_encoder_vertical_left_value, label_encoder_vertical_right_value]

        ## Start thread to read data rx buffer
        # Continous read of the serial communication RX data
        thread_rx_data = Thread(target = self.read_rx_buffer, args = (list_label,))
        thread_rx_data.start()