##
# @file
# common.py
#
# @brief
# This file contains all common functions to help setup of every page of the GUI. \n

# Imports
import tkinter
import customtkinter

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

def button_generate(self, button_pos_x, button_pos_y, text):
        button = customtkinter.CTkButton(
                                            master = self,
                                            text = text)
        
        button.place(
                        x = button_pos_x,
                        y = button_pos_y)

        
        return button
    
def combobox_generate(self, combobox_pos_x, combobox_pos_y, text): 
    combobox = customtkinter.CTkComboBox(
                                            master = self,
                                            values = text, 
                                            dynamic_resizing = True
                                        )

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

def entry_generate(self, label_pos_x, label_pos_y, text):
    entry = customtkinter.CTkEntry(
                                    master = self,
                                    placeholder_text= text)
    
    entry.place(
                x = label_pos_x,
                y = label_pos_y)
    
    return entry