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

# Global constants
## The width and height of the home page
HOME_PAGE_WIDTH = 780
HOME_PAGE_HEIGHT = 520

CBBOX_COM_PORTS_X = 20
CBBOX_COM_PORTS_Y = 20
CBBOX_WIDTH = 175

# Functions
def combobox_com_ports_callback(choice):
    """! Prints out the current COM port selected in the combobox
    @param choice   Selected COM port
    """
    print("COM port selected: ", choice)

def combobox_com_ports_generate(frame):
    """! Creates a combobox to list out all COM ports currently used by computer
    @param frame    Frame on which the combobox will appear
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
                                        master = frame,
                                        width = CBBOX_WIDTH,
                                        values = list_com_ports,
                                        command = lambda : combobox_com_ports_callback)
    combobox.place(
                    x = CBBOX_COM_PORTS_X,
                    y = CBBOX_COM_PORTS_Y)

    return combobox

def button_com_ports_click(combobox_com_ports):
    """! On click, prints out the current value of the COM ports combobox
    @param combobox_com_ports   The COM ports combobox
    """
    print("COM port to be connected: ", combobox_com_ports)

def populate_home_page(home_page_frame):
    """! Generates all different components of the home page
    @param home_page_frame  The frame on which to place all the components
    """
    cbbox_com_ports = combobox_com_ports_generate(home_page_frame)

    ## Generate all buttons
    btn_com_ports = customtkinter.CTkButton(
                                            master = home_page_frame,
                                            text = "Connect",
                                            command = lambda combobox_com_ports = cbbox_com_ports.get() : button_com_ports_click(combobox_com_ports))
    btn_com_ports.place(
                        x = (CBBOX_COM_PORTS_X * 12),
                        y = CBBOX_COM_PORTS_Y)