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
## Clock frequency used by the STM32
CLOCK_FREQUENCY = 72000000

# Prescalor value for stepper motor timers
PRESCALOR = 10

## Number of pulses necessary to travel one millimeter with vertical and horizontal rails
PULSE_PER_MM = 80

## ARR controlled speed value
ARR_MINIMUM = 6500

## Speed increment factor 
SPEED_INCREMENT = 45

## Number of pulses to execute one full rotation of the adaptor motor (without gearbox ratio)
PULSE_PER_TURN_ADAPTOR = 400

## Current gearbox ratio (10 turns of stepper motor for 1 turn of gearbox)
RATIO_GEARBOX_ADAPTOR = 10

## Maximal range of factor for vertical speed slider
SLIDER_VERTICAL_SPEED_RANGE_MAX = 100

## Maximal range of factor for horizontal speed slider
SLIDER_HORIZONTAL_SPEED_RANGE_MAX = 100

## Maximal range of factor for adaptor speed slider
SLIDER_ADAPTOR_SPEED_RANGE_MAX = 50

## Shared index for the previous  value of the slider
SLIDER_PREV_VALUE_INDEX = 0

## Shared index for the previous speed value of the slider
SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX = 1

## Maximal horizontal distance possible without any tools attached
MAX_HORIZONTAL  = 400

## Maximal vertical distance possible without any tools attached
MAX_VERTICAL    = 400

## First row index
ROW_ZERO = 0

## Second row index
ROW_ONE = 1

## Third row index
ROW_TWO = 2

## Fourth row index
ROW_THREE = 3

## Fifth row index
ROW_FOUR = 4

## Sixth row index
ROW_FIVE = 5

## Seventh row index
ROW_SIX = 6

## Eigth row index
ROW_SEVEN = 7

## Zero column index
COLUMN_ZERO = 0

## Second column index
COLUMN_ONE = 1

## Third column index
COLUMN_TWO = 2

## Fourth column index
COLUMN_THREE = 3

## Fifth column index
COLUMN_FOUR = 4

## Sixth column index
COLUMN_FIVE = 5

## Seventh column index
COLUMN_SIX = 6

## Eigth column index
COLUMN_SEVEN = 7

## Usual value for the padx argument in the grid positioning
PAD_X_USUAL = 20

## Usual value for the pady argument in the grid positioning
PAD_Y_USUAL = 20

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