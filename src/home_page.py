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

import common

# Global constants
## The width of the home page
WIDTH = 780

## The height of the home page
HEIGHT = 520

# Functions
def button_event(text):
    """! Prints out a given text
    @param textbox_name_of_program  The text to be printed out
    """
    print(text)

# Classes
class HomePage(customtkinter.CTk):
    """! Home page for the testbench GUI
    Defines all components of the home page
    """

    def __init__(self, name_of_page):
        """! Initialisation of a new window propreties upon creation of the object
        @param name_of_page Name to be given to the home page window
        @return An instance of the test bench GUI home page
        """
        super().__init__()

        ## Title of the home page
        self.title(name_of_page)

        ## Shape of the home page
        self.geometry(f"{WIDTH} x {HEIGHT}")

        ## Closing procedure for home page window
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        ## Button to access the available test programs
        btn_programs_page = customtkinter.CTkButton( text = "Programs",
                                                        command = lambda: button_event("txtbx_name_of_program"),
                                                        width = 120,
                                                        height = 32,
                                                        border_width = 0,
                                                        corner_radius = 8)
        btn_programs_page.place(relx = 0.3, rely = 0.3, anchor = tkinter.CENTER)

    def on_closing(self):
        """! Procedure to follow upon closing a window object
        """
        self.destroy()

if __name__ == "__main__":
    """! Main program entry
    """
    common.set_appearance("Dark", "blue")
    window_home = HomePage("Home - Zimmer Biomet Test Bench")
    window_home.mainloop()