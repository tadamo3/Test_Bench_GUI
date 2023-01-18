##
# @file
# common.py
#
# @brief
# This file contains all common functions to help setup of every page of the GUI. \n

# Imports
import tkinter
import customtkinter

import home_page
import programs_page

# Functions
def set_appearance(appearance_mode, default_color_theme):
    """! Sets the appearance of a given page
    @param appearance_mode          Appearance to give to the page
    @param default_color_theme      Color theme to give to the page
    """
    customtkinter.set_appearance_mode(appearance_mode)
    customtkinter.set_default_color_theme(default_color_theme)

def generate_window(window_type, window_name):
    """! Generates a given window type
    @param window_type  Window type to be created
    @param window_name  Name to be associated with created winow
    @return window  The created window    
    """
    set_appearance("Dark", "blue")

    # Generate correct window type
    if (window_type == 'Home'):
        window = home_page.HomePage(window_name)

    elif (window_type == 'Programs'):
        window = programs_page.ProgramsPage(window_name)
    
    else:
        print('Not a valid window type')
    
    if (window != None):
        window.state('zoomed')

        return window
    else:
        print('Error in creating window')

def start_window(window_to_start):
    """! Start the main loop of a given window
    @param window_to_start  The window to call mainloop() function on
    """
    window_to_start.mainloop()

def close_window(window_to_close):
    """! Closes a given window
    @param window_to_close  The window to call the destroy() function on
    """
    window_to_close.destroy()