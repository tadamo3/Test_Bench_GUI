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
import programs_page

# Global constants
## The width and height of the home page
HOME_PAGE_WIDTH = 780
HOME_PAGE_HEIGHT = 520

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
        self.geometry(f"{HOME_PAGE_WIDTH} x {HOME_PAGE_HEIGHT}")

        ## Closing procedure for home page window
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """! Procedure to follow upon closing a window object
        """
        self.destroy()