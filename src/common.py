##
# @file
# common.py
#
# @brief
# This file contains all common functions to help setup of every page of the GUI. \n

# Imports
import tkinter
import customtkinter

# Global constants
CLOCK_FREQUENCY         = 72000000
PULSE_PER_MM            = 80
ARR_MINIMUM             = 6500
SPEED_INCREMENT         = 45
PULSE_PER_TURN_ADAPTOR  = 400
RATIO_GEARBOX_ADAPTOR   = 10
PRESCALOR               = 10

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

def button_generate(self, row, column, rowspan, columnspan, padx, pady, text):
        button = customtkinter.CTkButton(
                                            master = self,
                                            text = text)
        
        button.grid(
                        row = row,
                        column = column,
                        rowspan = rowspan,
                        columnspan = columnspan,
                        padx = padx,
                        pady = pady,
                        sticky = 'nsew'
                       )

        return button

def slider_generate(self, row, column, rowspan, columnspan, padx, pady, range):
    slider = customtkinter.CTkSlider(
                                        master          = self,
                                        from_           = 0,
                                        to              = range,
                                        number_of_steps = range,
                                        height          = 10)
    slider.grid(
                    row         = row,
                    column      = column,
                    rowspan     = rowspan,
                    columnspan  = columnspan,
                    padx        = padx,
                    pady        = pady,
                    sticky      = 'nsew')

    return slider

def label_generate(self, row, column, rowspan, columnspan, padx, pady, text):
        label = customtkinter.CTkLabel(
                                        master          = self,
                                        text            = text,
                                        corner_radius   = 8)
        
        label.grid(
                    row         = row,
                    column      = column,
                    rowspan     = rowspan,
                    columnspan  = columnspan,
                    padx        = padx,
                    pady        = pady,
                    sticky      = 'nsew')

        return label

def entry_generate(self, row, column, rowspan, columnspan, padx, pady, text):
    entry = customtkinter.CTkEntry(
                                    master = self,
                                    placeholder_text= text)
    
    entry.grid(
                    row         = row,
                    column      = column,
                    rowspan     = rowspan,
                    columnspan  = columnspan,
                    padx        = padx,
                    pady        = pady,
                    sticky      = 'nsew')
    
    return entry

def calculate_speed_mm_per_sec(slider_value):
    numerator = CLOCK_FREQUENCY
    denominator = ((ARR_MINIMUM - (SPEED_INCREMENT * slider_value)) + 1) * (PRESCALOR + 1)

    speed_value_mm_per_sec = int((numerator / denominator) * (1 / PULSE_PER_MM))

    return speed_value_mm_per_sec


def calculate_speed_turn_per_sec(slider_value):
    numerator = CLOCK_FREQUENCY
    denominator = ((ARR_MINIMUM - (SPEED_INCREMENT * slider_value)) + 1) * (PRESCALOR + 1)

    speed_value_turn_per_sec = int(numerator / denominator) * (2 / PULSE_PER_TURN_ADAPTOR)
    gearbox_turn_per_sec = speed_value_turn_per_sec / RATIO_GEARBOX_ADAPTOR

    return gearbox_turn_per_sec