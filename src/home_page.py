##
# @file
# home_page.py
#
# @brief
# This file acts as the setup file for the home page of the GUI. \n
# All its components and callback functions will be defined here.

# Imports
import tkinter
import customtkinter
import tkinter.messagebox
from serial.tools import list_ports
from threading import Thread
from threading import Event
import time

import serial_funcs

# Global constants
## The width and height of the home page
HOME_PAGE_WIDTH     = 780
HOME_PAGE_HEIGHT    = 520

## Info about the combobox ports
CBBOX_COM_PORTS_X   = 20
CBBOX_COM_PORTS_Y   = 20
CBBOX_WIDTH         = 175

## Info about the vertical speed slider
SLIDER_VERTICAL_SPEED_X                 = 20
SLIDER_VERTICAL_SPEED_Y                 = 100
SLIDER_VERTICAL_SPEED_PREV_VALUE_INDEX  = 0

ID_NONE         = 0
COMMAND_NONE    = 0
DATA_NONE       = 0

## Global variables
# Event variable is false by default
home_page_stop_threads_event = Event()

# Classes
class HomePage(customtkinter.CTkFrame):
    """! Home page class for the Zimmer Test Bench\n
    Defines the components and callback functions of the home page
    """
    list_slider_vertical_info = [0]
    
    def periodic_process_queue(self):
        """! Calls the Home Page task processor every 100ms
        """
        self.home_page_thread_manager.process_incoming_tasks()
        self.after(100, self.periodic_process_queue)

    def read_rx_buffer(self):
        """! Inserts in the task queue the message sent by the STM32 over serial communication\n
        Sleeps for 500ms to keep a reasonable update rate
        """
        while (home_page_stop_threads_event.is_set() != True):
            serial_funcs.receive_serial_data(
                                                serial_funcs.g_list_message_info,
                                                serial_funcs.g_list_connected_device_info)
            time.sleep(0.5)

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

    def btn_vertical_dir_click(self, command, data, list_com_device_info):
        serial_funcs.transmit_serial_data(
                                            serial_funcs.ID_MOTOR_VERTICAL_LEFT,
                                            command,
                                            data,
                                            list_com_device_info)

    def slider_vertical_speed_callback(self, slider_value, list_slider_info, list_com_device_info):
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
                                                    serial_funcs.ID_ENCODER_VERTICAL_LEFT,
                                                    COMMAND_NONE,
                                                    slider_value,
                                                    list_com_device_info)
                list_slider_info[SLIDER_VERTICAL_SPEED_PREV_VALUE_INDEX] = slider_value

    def __init__(self):
        """! Initialisation of a Home Page class
        """
        super().__init__()

        ## Stores the current selected COM port in the combobox
        strvar_current_com_port = customtkinter.StringVar(self)

        ## Generate all comboboxes
        cbbox_com_ports = self.combobox_com_ports_generate(strvar_current_com_port)

        ## Generate all buttons
        btn_com_ports = customtkinter.CTkButton(
                                                master = self,
                                                text = "Connect",
                                                command = lambda : self.button_com_ports_click(
                                                                                                cbbox_com_ports.get(),
                                                                                                serial_funcs.g_list_connected_device_info))
        btn_com_ports.place(
                            x = (CBBOX_COM_PORTS_X * 12),
                            y = CBBOX_COM_PORTS_Y)

        btn_vertical_dir_up = customtkinter.CTkButton(
                                                        master = self,
                                                        text = "Go up!",
                                                        command = lambda : self.btn_vertical_dir_click(
                                                                                                            serial_funcs.COMMAND_MOTOR_VERTICAL_UP,
                                                                                                            DATA_NONE,
                                                                                                            serial_funcs.g_list_connected_device_info))
        btn_vertical_dir_up.place(
                                    x = (CBBOX_COM_PORTS_X * 20),
                                    y = CBBOX_COM_PORTS_Y)
        
        btn_vertical_dir_down = customtkinter.CTkButton(
                                                        master = self,
                                                        text = "Go Down!",
                                                        command = lambda : self.btn_vertical_dir_click(
                                                                                                            serial_funcs.COMMAND_MOTOR_VERTICAL_DOWN,
                                                                                                            DATA_NONE,
                                                                                                            serial_funcs.g_list_connected_device_info))
        btn_vertical_dir_down.place(
                                    x = (CBBOX_COM_PORTS_X * 28),
                                    y = CBBOX_COM_PORTS_Y)

        btn_vertical_dir_up = customtkinter.CTkButton(
                                                        master = self,
                                                        text = "Stop",
                                                        command = lambda : self.btn_vertical_dir_click(
                                                                                                            serial_funcs.COMMAND_MOTOR_VERTICAL_STOP,
                                                                                                            DATA_NONE,
                                                                                                            serial_funcs.g_list_connected_device_info))
        btn_vertical_dir_up.place(
                                    x = (CBBOX_COM_PORTS_X * 20),
                                    y = CBBOX_COM_PORTS_Y + 100)
        
        ## Generate all sliders
        slider_vertical_speed = customtkinter.CTkSlider(
                                                        master          = self,
                                                        from_           = 0,
                                                        to              = 100,
                                                        number_of_steps = 100)
        slider_vertical_speed.command = lambda slider_value = slider_vertical_speed.get() : self.slider_vertical_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                self.list_slider_vertical_info,
                                                                                                                                serial_funcs.g_list_connected_device_info)
        slider_vertical_speed.place(
                                    x = SLIDER_VERTICAL_SPEED_X,
                                    y = SLIDER_VERTICAL_SPEED_Y)

        ## Generate all labels
        label_encoder_1_value = customtkinter.CTkLabel(
                                                        master          = self,
                                                        text            = "Encoder 1 value goes here",
                                                        corner_radius   = 8)
        label_encoder_1_value.place(
                                    x = SLIDER_VERTICAL_SPEED_X + 100,
                                    y = SLIDER_VERTICAL_SPEED_Y + 100)

        ## Start thread to read data rx buffer
        # Continous read of the serial communication RX data
        thread_rx_data = Thread(target = self.read_rx_buffer)
        thread_rx_data.start()