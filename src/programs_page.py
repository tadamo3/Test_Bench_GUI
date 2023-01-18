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
import tkinter.messagebox

import common
import home_page

# Global constants
## The width and height of the home page
WIDTH_PROGRAMS_PAGE = 780
HEIGHT_PROGRAMS_PAGE = 520

## Relative positions and appearance of the button to return to the home page
RELX_BTN_RETURN_HOME = 0.25
RELY_BTN_RETURN_HOME = 0.25
WIDTH_BTN_RETURN_HOME = 500
HEIGHT_BTN_RETURN_HOME = 100
BORDER_WIDTH_BTN_RETURN_HOME = 0
CORNER_RADIUS_BTN_RETURN_HOME = 8

# Functions
def setup_programs_page():
    """! Setups and starts the programs page window with an appropriate name
    """
    window_programs = common.generate_window('Programs', 'Programs - Zimmer Biomet Test Bench GUI')
    common.start_window(window_programs)

def btn_event_return_home(current_window):
    """! Upon calling, destroys the programs page and sends user back to the home page
    @param current_window   Window to be closed
    """
    common.close_window(current_window)

    home_page.setup_home_page()

# Classes
class ProgramsPage(customtkinter.CTk):
    def __init__(self, name_of_page):
        """! Initialisation of a new window propreties upon creation of the object
        @param name_of_page Name to be given to the programs page window
        @return An instance of the test bench GUI programs page
        """
        super().__init__()

        ## Title of the home page
        self.title(name_of_page)

        ## Shape of the home page
        self.geometry(f"{WIDTH_PROGRAMS_PAGE} x {HEIGHT_PROGRAMS_PAGE}")

        ## Closing procedure for home page window
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

         ## Button to return to home page
        btn_return_home = customtkinter.CTkButton(  text            = "Back",
                                                    command         = lambda: btn_event_return_home(self),
                                                    width           = WIDTH_BTN_RETURN_HOME,
                                                    height          = HEIGHT_BTN_RETURN_HOME,
                                                    border_width    = BORDER_WIDTH_BTN_RETURN_HOME,
                                                    corner_radius   = CORNER_RADIUS_BTN_RETURN_HOME
                                                    )

        btn_return_home.place(  relx = RELX_BTN_RETURN_HOME, 
                                rely = RELY_BTN_RETURN_HOME,
                                anchor = tkinter.CENTER
                                )

    def on_closing(self):
        """! Procedure to follow upon closing a window object
        """
        self.destroy()
