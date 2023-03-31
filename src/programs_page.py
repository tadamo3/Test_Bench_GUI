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
from threading import Event
import time
import serial_funcs
import os

# Global constants
## The width and height of the home page
HOME_PAGE_WIDTH     = 1450
HOME_PAGE_HEIGHT    = 1500

NP_VALUE_X       = 50
NP_VALUE_Y       = 50

BUTTON_DIRECTION_CENTER_X = 200
BUTTON_DIRECTION_CENTER_Y = 250

BUTTON_A_X          = 500
BUTTON_A_Y          = 200
BUTTON_B_X          = 500
BUTTON_B_Y          = 275

POSITION_X_X        = 50
POSITION_Y_X        = 100
POSITION_X_Y        = 50
POSITION_Y_Y        = 135

entry_pos_x         = 500
entry_pos_y         = 125

SLIDER_VERTICAL_SPEED_X                 = 20
SLIDER_VERTICAL_SPEED_Y                 = 500
SLIDER_VERTICAL_SPEED_PREV_VALUE_INDEX  = 0
SLIDER_VERTICAL_SPEED_RANGE_MAX         = 100

SLIDER_HORIZONTAL_SPEED_X                   = 20
SLIDER_HORIZONTAL_SPEED_Y                   = 575
SLIDER_HORIZONTAL_SPEED_PREV_VALUE_INDEX    = 0
SLIDER_HORIZONTAL_SPEED_RANGE_MAX           = 100

FRAME_POS_X = 780
FRAME_POS_Y = 0


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
        
        label.text = text

        return label
    
    def file_creator(self, name, point, x, y):
        #if (name != ''):
            with open(os.path.join("D:\Test_Bench_GUI\Zimmer Programs",name+".txt"), "a") as f:
                f.write(point)
                f.write('\n')
                f.write(x)
                f.write('\n')
                f.write(y)
                f.write('\n')
                f.close()
                print(point+" saved in "+name+".txt")
    

    

    def __init__(self, master, **kwargs):
        """! Initialisation of a Programs Page Frame
        """
        super().__init__(master, **kwargs)


        ## Generate all comboboxes

        ## Generate all labels
        pos_x = self.label_generate(POSITION_X_X, POSITION_Y_X, "X position : ")
        pos_x_val = self.label_generate((POSITION_X_X + 75), POSITION_Y_X, "123456")

        pos_y = self.label_generate(POSITION_X_Y, POSITION_Y_Y, "Y position : ")
        pos_y_val = self.label_generate((POSITION_X_Y + 75), POSITION_Y_Y, "123456")
        
        ## Generate all entry

        file_name = customtkinter.CTkEntry(
                                        master = self,
                                        placeholder_text="File name")
        file_name.place(
                    x = entry_pos_x, 
                    y = entry_pos_y, 
                    anchor = tkinter.CENTER)

        ## Generate all buttons
        
        
        new_prog            = self.button_generate(NP_VALUE_X, NP_VALUE_Y, "New Program")
        btn_direction_up    = self.button_generate(BUTTON_DIRECTION_CENTER_X, (BUTTON_DIRECTION_CENTER_Y - 50), "Going Up")
        btn_direction_down  = self.button_generate(BUTTON_DIRECTION_CENTER_X, (BUTTON_DIRECTION_CENTER_Y + 50), "Going Down")
        btn_direction_left  = self.button_generate((BUTTON_DIRECTION_CENTER_X - 100), BUTTON_DIRECTION_CENTER_Y, "Going Left")
        btn_direction_right = self.button_generate((BUTTON_DIRECTION_CENTER_X + 100), BUTTON_DIRECTION_CENTER_Y, "Going Right")

        button_A = customtkinter.CTkButton(
                                            master = self,
                                            text = "Save point A")
        
        button_A.configure(command = lambda : self.file_creator(file_name.get(), 'Position A :', pos_x_val.text, pos_y_val.text))
        
        button_A.place(
                        x = BUTTON_A_X,
                        y = BUTTON_A_Y)
        
        button_B = customtkinter.CTkButton(
                                            master = self,
                                            text = "Save point B")
        
        button_B.configure(command = lambda : self.file_creator(file_name.get(), 'Position B :', pos_x_val.text, pos_y_val.text))
        
        button_B.place(
                        x = BUTTON_B_X,
                        y = BUTTON_B_Y)




        ## Generate all sliders

        slider_vertical_speed = self.slider_generate(SLIDER_VERTICAL_SPEED_X, SLIDER_VERTICAL_SPEED_Y, SLIDER_VERTICAL_SPEED_RANGE_MAX)
        slider_horizontal_speed = self.slider_generate(SLIDER_HORIZONTAL_SPEED_X, SLIDER_HORIZONTAL_SPEED_Y, SLIDER_HORIZONTAL_SPEED_RANGE_MAX)

        ## Scrollable frame

        programs_list = customtkinter.CTkScrollableFrame(
                                        master  =   self, 
                                        width   =   200, 
                                        height  =   200)
        
        #programs_list.anchor("center")
        programs_list.place(
                       relx = 1,
                       rely = 0,
                       anchor = tkinter.NE)
