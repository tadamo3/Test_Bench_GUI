##
# @file
# common.py
#
# @brief
# This file contains all common functions to help setup of every page of the GUI. \n

# Imports
import tkinter
import customtkinter

from serial_funcs import transmit_serial_data, ID_MOTOR_ADAPT, ID_MOTOR_HORIZONTAL, ID_MOTOR_VERTICAL_LEFT, COMMAND_MOTOR_CHANGE_SPEED, MODE_CHANGE_PARAMS

# Global constants
## List to contain the previous slider value and the previous speed value of the vertical slider
list_slider_vertical_info = [0, 0]

## List to contain the previous slider value and the previous speed value of the horizontal slider
list_slider_horizontal_info = [0, 0]

## List to contain the previous slider value and the previous speed value of the adaptor slider
list_slider_adaptor_info = [0, 0]

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

## Manual mode indicator
MODE_MANUAL = 0

## Automatic test mode indicator
MODE_AUTOMATIC_TEST = 1

## Automatic mode indicator
MODE_AUTOMATIC = 2

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

## Ninth row index
ROW_EIGHT = 8

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

## Ninth column index
COLUMN_EIGHT = 8

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

def button_generate(self, row, column, rowspan, columnspan, padx, pady, text):
    """! Generates a button and lays it out on a certain master frame
    @param row              The starting position of the button respective to rows
    @param column           The starting position of the button respective to columns
    @param rowspan          The amount of rows the button will take
    @param columnspan       The amount of columns the button will take
    @param padx             The amount of space to be left between any other component and the button on the x axis
    @param pady             The amount of space to be left between any other component and the button on the y axis
    @param text             Text to be written on the button
    @return     A button object
    """
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
    """! Generates a slider and lays it out on a certain master frame
    @param row              The starting position of the slider respective to rows
    @param column           The starting position of the slider respective to columns
    @param rowspan          The amount of rows the slider will take
    @param columnspan       The amount of columns the slider will take
    @param padx             The amount of space to be left between any other component and the slider on the x axis
    @param pady             The amount of space to be left between any other component and the slider on the y axis
    @param range            The maximal value to be reached by the slider and its number of steps (from 0 to range)
    @return     A slider object
    """
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
    """! Generates a label and lays it out on a certain master frame
    @param row              The starting position of the label respective to rows
    @param column           The starting position of the label respective to columns
    @param rowspan          The amount of rows the label will take
    @param columnspan       The amount of columns the label will take
    @param padx             The amount of space to be left between any other component and the label on the x axis
    @param pady             The amount of space to be left between any other component and the label on the y axis
    @param text             Text to be written on the label
    @return     A label object
    """
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
    """! Generates an entry and lays it out on a certain master frame
    @param row              The starting position of the entry respective to rows
    @param column           The starting position of the entry respective to columns
    @param rowspan          The amount of rows the entry will take
    @param columnspan       The amount of columns the entry will take
    @param padx             The amount of space to be left between any other component and the entry on the x axis
    @param pady             The amount of space to be left between any other component and the entry on the y axis
    @param text             Text to be written on the entry
    @return     A entry object
    """
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
    """! Converts the given slider value to a speed in mm per seconds
    @param slider_value     The slider value to be converted in a speed
    @return The converted speed in mm per seconds
    """
    numerator = CLOCK_FREQUENCY
    denominator = ((ARR_MINIMUM - (SPEED_INCREMENT * slider_value)) + 1) * (PRESCALOR + 1)

    speed_value_mm_per_sec = int((numerator / denominator) * (1 / PULSE_PER_MM))

    return speed_value_mm_per_sec


def calculate_speed_turn_per_sec(slider_value):
    """! Converts the given slider value to a number of turns by seconds
    @param slider_value     The slider value to be converted in a rotation speed
    @return The converted turn speed in turns per seconds
    """
    numerator = CLOCK_FREQUENCY
    denominator = ((ARR_MINIMUM - (SPEED_INCREMENT * slider_value)) + 1) * (PRESCALOR + 1)

    speed_value_turn_per_sec = int(numerator / denominator) * (2 / PULSE_PER_TURN_ADAPTOR)
    gearbox_turn_per_sec = speed_value_turn_per_sec / RATIO_GEARBOX_ADAPTOR

    return gearbox_turn_per_sec

def slider_speed_callback(slider_value, list_slider_info, slider_type, label_slider, device):
    """! Every time a new value is set, sends the updated desired speed value to the device
    @param slider_value         The selected speed value for the vertical motor speed
    @param list_slider_info     Notable information for a specific slider
    @param slider_type          Indicates the kind of slider to be addressed as the calculations can be different depending on the type
    @param label_slider         Label related to the slider to be modified
    @param device               Currently connected Serial object
    """
    if (device[0] != 0):
        slider_value = round(slider_value)
        previous_slider_value = round(list_slider_info[SLIDER_PREV_VALUE_INDEX])

        if (slider_value != previous_slider_value):
            if (slider_type == "Vertical"):
                transmit_serial_data(
                                        ID_MOTOR_VERTICAL_LEFT,
                                        COMMAND_MOTOR_CHANGE_SPEED,
                                        MODE_CHANGE_PARAMS,
                                        slider_value,
                                        device)
                
                speed_value_mm_per_sec = calculate_speed_mm_per_sec(slider_value)

                list_slider_info[SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX] = speed_value_mm_per_sec
                label_slider.configure(text = (str(speed_value_mm_per_sec) + " mm/s"))

            if (slider_type == "Horizontal"):
                transmit_serial_data(
                                        ID_MOTOR_HORIZONTAL,
                                        COMMAND_MOTOR_CHANGE_SPEED,
                                        MODE_CHANGE_PARAMS,
                                        slider_value,
                                        device)
                
                speed_value_mm_per_sec = calculate_speed_mm_per_sec(slider_value)

                list_slider_info[SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX] = speed_value_mm_per_sec
                label_slider.configure(text = (str(speed_value_mm_per_sec) + " mm/s"))
            
            if (slider_type == "Adaptor"):
                transmit_serial_data(
                                        ID_MOTOR_ADAPT,
                                        COMMAND_MOTOR_CHANGE_SPEED,
                                        MODE_CHANGE_PARAMS,
                                        slider_value,
                                        device)
                
                gearbox_speed_turn_per_sec = calculate_speed_turn_per_sec(slider_value)
                gearbox_speed_string = f"{gearbox_speed_turn_per_sec:.2f}"

                list_slider_info[SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX] = float(gearbox_speed_string)
                label_slider.configure(text = (gearbox_speed_string + " turn/s"))

            list_slider_info[SLIDER_PREV_VALUE_INDEX] = slider_value

def generate_sliders(self, chosen_mode, device):
    """! Generates and places the sliders and their labels depending on the type of mode chosen by the user\n
            This function is put in the common script since it is only a setup function and therefore takes useless space in more important files
    @param chosen_mode      Manual or automatic mode - Chosen by the user
    @param device           The Serial object currently connected to the application
    @return     A list of the items related to slider positioning
    """
    list_slider_items = []

    if (chosen_mode == MODE_MANUAL):
        label_visualize_vertical_speed      = label_generate(
                                                                self, 
                                                                ROW_TWO,
                                                                COLUMN_SEVEN,
                                                                1,
                                                                1,
                                                                (5, PAD_X_USUAL),
                                                                PAD_Y_USUAL,
                                                                (str(list_slider_vertical_info[SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX]) + " mm/s"))
        label_visualize_horizontal_speed    = label_generate(
                                                                self,
                                                                ROW_FOUR,
                                                                COLUMN_SEVEN,
                                                                1,
                                                                1,
                                                                (0, PAD_X_USUAL),
                                                                PAD_Y_USUAL, (str(list_slider_horizontal_info[SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX]) + " mm/s"))
        label_visualize_rotation_speed      = label_generate(
                                                                self,
                                                                ROW_SIX,
                                                                COLUMN_SEVEN,
                                                                1,
                                                                1,
                                                                (0, PAD_X_USUAL),
                                                                PAD_Y_USUAL,
                                                                (str(list_slider_adaptor_info[SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX]) + " turn/s"))

        slider_vertical_speed = slider_generate(
                                                self, 
                                                ROW_TWO, 
                                                COLUMN_FOUR, 
                                                1,
                                                3,
                                                5,
                                                5,
                                                SLIDER_VERTICAL_SPEED_RANGE_MAX)
        slider_vertical_speed.set(list_slider_vertical_info[SLIDER_PREV_VALUE_INDEX])
        slider_vertical_speed.configure(command = lambda slider_value = slider_vertical_speed.get() : slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                list_slider_vertical_info,
                                                                                                                                "Vertical",
                                                                                                                                label_visualize_vertical_speed,
                                                                                                                                device))

        slider_horizontal_speed = slider_generate(
                                                    self,
                                                    ROW_FOUR,
                                                    COLUMN_FOUR,
                                                    1,
                                                    3,
                                                    5,
                                                    5,
                                                    SLIDER_HORIZONTAL_SPEED_RANGE_MAX)
        slider_horizontal_speed.set(list_slider_horizontal_info[SLIDER_PREV_VALUE_INDEX])
        slider_horizontal_speed.configure(command = lambda slider_value = slider_horizontal_speed.get() : slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                list_slider_horizontal_info,
                                                                                                                                "Horizontal",
                                                                                                                                label_visualize_horizontal_speed,
                                                                                                                                device))

        slider_adaptor_speed = slider_generate(
                                                self,
                                                ROW_SIX,
                                                COLUMN_FOUR,
                                                1,
                                                3,
                                                5,
                                                5,
                                                SLIDER_ADAPTOR_SPEED_RANGE_MAX)
        slider_adaptor_speed.set(list_slider_adaptor_info[SLIDER_PREV_VALUE_INDEX])
        slider_adaptor_speed.configure(command = lambda slider_value = slider_adaptor_speed.get() : slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                list_slider_adaptor_info,
                                                                                                                                "Adaptor",
                                                                                                                                label_visualize_rotation_speed,
                                                                                                                                device))

        label_vertical_speed_slider     = label_generate(
                                                            self,
                                                            ROW_ONE,
                                                            COLUMN_FOUR,
                                                            1,
                                                            1,
                                                            (PAD_X_USUAL, 5),
                                                            PAD_Y_USUAL, 
                                                            "Vertical Speed")
        label_horizontal_speed_slider   = label_generate(
                                                            self,
                                                            ROW_THREE,
                                                            COLUMN_FOUR,
                                                            1,
                                                            1,
                                                            (PAD_X_USUAL, 5), 
                                                            PAD_Y_USUAL, 
                                                            "Horizontal speed")
        label_adaptor_speed_slider      = label_generate(
                                                            self,
                                                            ROW_FIVE,
                                                            COLUMN_FOUR,
                                                            1,
                                                            1,
                                                            (PAD_X_USUAL, 5), 
                                                            PAD_Y_USUAL, 
                                                            "Adaptor speed")
    elif (chosen_mode == MODE_AUTOMATIC_TEST):
        label_visualize_vertical_speed      = label_generate(
                                                                self,
                                                                ROW_TWO,
                                                                COLUMN_SEVEN,
                                                                1,
                                                                1,
                                                                (5, PAD_X_USUAL), 
                                                                PAD_Y_USUAL, 
                                                                (str(list_slider_vertical_info[SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX]) + "   mm/s"))
        label_visualize_horizontal_speed    = label_generate(
                                                                self, 
                                                                ROW_FOUR,
                                                                COLUMN_SEVEN,
                                                                1,
                                                                1,
                                                                (5, PAD_X_USUAL), 
                                                                PAD_Y_USUAL, 
                                                                (str(list_slider_horizontal_info[SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX]) + "   mm/s"))
        label_visualize_rotation_speed      = label_generate(
                                                                self, 
                                                                ROW_SIX, 
                                                                COLUMN_SEVEN, 
                                                                1, 
                                                                1,
                                                                (5, PAD_X_USUAL), 
                                                                PAD_Y_USUAL, 
                                                                (str(list_slider_adaptor_info[SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX]) + "   turn/s"))

        slider_vertical_speed = slider_generate(
                                                    self,
                                                    ROW_TWO,
                                                    COLUMN_FOUR,
                                                    1,
                                                    3,
                                                    5,
                                                    5,
                                                    SLIDER_VERTICAL_SPEED_RANGE_MAX)
        slider_vertical_speed.set(list_slider_vertical_info[SLIDER_PREV_VALUE_INDEX])
        slider_vertical_speed.configure(command = lambda slider_value = slider_vertical_speed.get() : slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                list_slider_vertical_info,
                                                                                                                                "Vertical",
                                                                                                                                label_visualize_vertical_speed,
                                                                                                                                device))

        slider_horizontal_speed = slider_generate(
                                                    self,
                                                    ROW_FOUR,
                                                    COLUMN_FOUR,
                                                    1,
                                                    3,
                                                    5,
                                                    5,
                                                    SLIDER_HORIZONTAL_SPEED_RANGE_MAX)
        slider_horizontal_speed.set(list_slider_horizontal_info[SLIDER_PREV_VALUE_INDEX])
        slider_horizontal_speed.configure(command = lambda slider_value = slider_horizontal_speed.get() : slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                list_slider_horizontal_info,
                                                                                                                                "Horizontal",
                                                                                                                                label_visualize_horizontal_speed,
                                                                                                                                device))

        slider_adaptor_speed = slider_generate(
                                                    self,
                                                    ROW_SIX,
                                                    COLUMN_FOUR,
                                                    1,
                                                    3,
                                                    5,
                                                    5,
                                                    SLIDER_ADAPTOR_SPEED_RANGE_MAX)
        slider_adaptor_speed.set(list_slider_adaptor_info[SLIDER_PREV_VALUE_INDEX])
        slider_adaptor_speed.configure(command = lambda slider_value = slider_adaptor_speed.get() : slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                list_slider_adaptor_info,
                                                                                                                                "Adaptor",
                                                                                                                                label_visualize_rotation_speed,
                                                                                                                                device))

        label_vertical_speed_slider     = label_generate(
                                                            self,
                                                            ROW_ONE,
                                                            COLUMN_FOUR,
                                                            1,
                                                            1,
                                                            PAD_X_USUAL,
                                                            (PAD_Y_USUAL, 5),
                                                            "Vertical Speed")
        label_horizontal_speed_slider   = label_generate(
                                                            self,
                                                            ROW_THREE,
                                                            COLUMN_FOUR,
                                                            1,
                                                            1,
                                                            PAD_X_USUAL,
                                                            (PAD_Y_USUAL, 5),
                                                            "Horizontal speed")
        label_adaptor_speed_slider      = label_generate(
                                                            self,
                                                            ROW_FIVE,
                                                            COLUMN_FOUR,
                                                            1,
                                                            1,
                                                            PAD_X_USUAL,
                                                            (PAD_Y_USUAL, 5), 
                                                            "Adaptor speed")
    elif (chosen_mode == MODE_AUTOMATIC):
        label_visualize_vertical_speed      = label_generate(
                                                                self, 
                                                                ROW_ONE,
                                                                COLUMN_FIVE,
                                                                1,
                                                                1,
                                                                (5, PAD_X_USUAL),
                                                                PAD_Y_USUAL,
                                                                (str(list_slider_vertical_info[SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX]) + " mm/s"))
        label_visualize_horizontal_speed    = label_generate(
                                                                self,
                                                                ROW_THREE,
                                                                COLUMN_FIVE,
                                                                1,
                                                                1,
                                                                (0, PAD_X_USUAL),
                                                                PAD_Y_USUAL, (str(list_slider_horizontal_info[SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX]) + " mm/s"))
        label_visualize_rotation_speed      = label_generate(
                                                                self,
                                                                ROW_FIVE,
                                                                COLUMN_FIVE,
                                                                1,
                                                                1,
                                                                (0, PAD_X_USUAL),
                                                                PAD_Y_USUAL,
                                                                (str(list_slider_adaptor_info[SLIDER_PREV_SPEED_VALUE_MM_PER_SEC_INDEX]) + " turn/s"))

        slider_vertical_speed = slider_generate(
                                                self, 
                                                ROW_ONE, 
                                                COLUMN_TWO, 
                                                1,
                                                3,
                                                5,
                                                5,
                                                SLIDER_VERTICAL_SPEED_RANGE_MAX)
        slider_vertical_speed.set(list_slider_vertical_info[SLIDER_PREV_VALUE_INDEX])
        slider_vertical_speed.configure(command = lambda slider_value = slider_vertical_speed.get() : slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                list_slider_vertical_info,
                                                                                                                                "Vertical",
                                                                                                                                label_visualize_vertical_speed,
                                                                                                                                device))

        slider_horizontal_speed = slider_generate(
                                                    self,
                                                    ROW_THREE,
                                                    COLUMN_TWO,
                                                    1,
                                                    3,
                                                    5,
                                                    5,
                                                    SLIDER_HORIZONTAL_SPEED_RANGE_MAX)
        slider_horizontal_speed.set(list_slider_horizontal_info[SLIDER_PREV_VALUE_INDEX])
        slider_horizontal_speed.configure(command = lambda slider_value = slider_horizontal_speed.get() : slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                list_slider_horizontal_info,
                                                                                                                                "Horizontal",
                                                                                                                                label_visualize_horizontal_speed,
                                                                                                                                device))

        slider_adaptor_speed = slider_generate(
                                                self,
                                                ROW_FIVE,
                                                COLUMN_TWO,
                                                1,
                                                3,
                                                5,
                                                5,
                                                SLIDER_ADAPTOR_SPEED_RANGE_MAX)
        slider_adaptor_speed.set(list_slider_adaptor_info[SLIDER_PREV_VALUE_INDEX])
        slider_adaptor_speed.configure(command = lambda slider_value = slider_adaptor_speed.get() : slider_speed_callback(
                                                                                                                                slider_value,
                                                                                                                                list_slider_adaptor_info,
                                                                                                                                "Adaptor",
                                                                                                                                label_visualize_rotation_speed,
                                                                                                                                device))

        label_vertical_speed_slider     = label_generate(
                                                            self,
                                                            ROW_ZERO,
                                                            COLUMN_TWO,
                                                            1,
                                                            1,
                                                            (PAD_X_USUAL, 5),
                                                            PAD_Y_USUAL, 
                                                            "Vertical Speed")
        label_horizontal_speed_slider   = label_generate(
                                                            self,
                                                            ROW_TWO,
                                                            COLUMN_TWO,
                                                            1,
                                                            1,
                                                            (PAD_X_USUAL, 5), 
                                                            PAD_Y_USUAL, 
                                                            "Horizontal speed")
        label_adaptor_speed_slider      = label_generate(
                                                            self,
                                                            ROW_FOUR,
                                                            COLUMN_TWO,
                                                            1,
                                                            1,
                                                            (PAD_X_USUAL, 5), 
                                                            PAD_Y_USUAL, 
                                                            "Adaptor speed")

    else:
        print("Invalid chosen mode")

    list_slider_items.extend((
        label_visualize_vertical_speed,
        label_visualize_horizontal_speed,
        label_visualize_rotation_speed,
        slider_vertical_speed,
        slider_horizontal_speed,
        slider_adaptor_speed,
        label_vertical_speed_slider,
        label_horizontal_speed_slider,
        label_adaptor_speed_slider
    ))

    return list_slider_items