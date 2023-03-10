##
# @file
# programs_page.py
#
# @brief
# This file acts as the setup file for the programs page of the GUI. \n
# All its components and callback functions will be defined here.

# Imports
import customtkinter
from threading import Thread
from threading import Event
import time

import serial_funcs

# Global constants
## The width and height of the home page
HOME_PAGE_WIDTH     = 780
HOME_PAGE_HEIGHT    = 520

TITLE_VALUE_X       = 50
TITLE_VALUE_Y       = 50

BUTTON_DIRECTION_CENTER_X = 200
BUTTON_DIRECTION_CENTER_Y = 275

BUTTON_NEXT_X = 300
BUTTON_NEXT_Y = 500



## Global variables
# Event variable is false by default
programs_page_stop_threads_event = Event()

# Classes
class ProgramsPageFrame(customtkinter.CTkFrame):
    """! Programs page class for the Zimmer Test Bench\n
    Defines the components and callback functions of the programs page
    """
    list_slider_vertical_info = [0]
    list_slider_horizontal_info = [0]

    def read_rx_buffer(self):
        """! Inserts in the task queue the message sent by the STM32 over serial communication\n
        Sleeps for 500ms to keep a reasonable update rate
        """
        while (programs_page_stop_threads_event.is_set() != True):
            serial_funcs.receive_serial_data(
                                                serial_funcs.g_list_message_info,
                                                serial_funcs.g_list_connected_device_info)
            time.sleep(0.01)


    def button_generate(self, button_pos_x, button_pos_y, text):
        button = customtkinter.CTkButton(
                                            master = self,
                                            text = text)
        
        button.place(
                        x = button_pos_x,
                        y = button_pos_y)

        return button


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


    def label_generate(self, label_pos_x, label_pos_y, text):
        label = customtkinter.CTkLabel(
                                        master          = self,
                                        text            = text,
                                        corner_radius   = 8)
        
        label.place(
                    x = label_pos_x,
                    y = label_pos_y)

        return label

    def __init__(self, master, **kwargs):
        """! Initialisation of a Programs Page Frame
        """
        super().__init__(master, **kwargs)


        ## Generate all comboboxes
        

        ## Generate all buttons
        btn_direction_up    = self.button_generate(BUTTON_DIRECTION_CENTER_X, (BUTTON_DIRECTION_CENTER_Y + 100), "Going Up")
        btn_direction_down  = self.button_generate(BUTTON_DIRECTION_CENTER_X, (BUTTON_DIRECTION_CENTER_Y - 100), "Going Down")
        btn_direction_left  = self.button_generate((BUTTON_DIRECTION_CENTER_X - 100), BUTTON_DIRECTION_CENTER_Y, "Going Left")
        btn_direction_right = self.button_generate((BUTTON_DIRECTION_CENTER_X + 100), BUTTON_DIRECTION_CENTER_Y, "Going Right")

        btn_next = self.button_generate(BUTTON_NEXT_X, BUTTON_NEXT_Y, "Next")


        btn_direction_up2    = self.button_generate(BUTTON_DIRECTION_CENTER_X + 400, (BUTTON_DIRECTION_CENTER_Y + 100), "Going Up")
        btn_direction_up2.configure(state = "disabled")

        btn_direction_down2  = self.button_generate(BUTTON_DIRECTION_CENTER_X +400, (BUTTON_DIRECTION_CENTER_Y - 100), "Going Down")
        btn_direction_down2.configure(state = "disabled")

        btn_direction_left2  = self.button_generate((BUTTON_DIRECTION_CENTER_X + 300), BUTTON_DIRECTION_CENTER_Y, "Going Left")
        btn_direction_left2.configure(state = "disabled")

        btn_direction_right2 = self.button_generate((BUTTON_DIRECTION_CENTER_X + 500), BUTTON_DIRECTION_CENTER_Y, "Going Right")
        btn_direction_right2.configure(state = "disabled")


        ## Generate all sliders
        

        ## Generate all labels
        title = self.label_generate(TITLE_VALUE_X, TITLE_VALUE_Y, "Tools positions")

        ## Start thread to read data rx buffer
        # Continous read of the serial communication RX data
        #thread_rx_data = Thread(target = self.read_rx_buffer)
        #thread_rx_data.start()