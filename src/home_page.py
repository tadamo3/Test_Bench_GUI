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
WIDTH_HOME_PAGE = 780
HEIGHT_HOME_PAGE = 520

## Relative positions and appearance of the button to switch to the programs page
RELX_BTN_PROGRAMS_PAGE = 0.25
RELY_BTN_PROGRAMS_PAGE = 0.25
WIDTH_BTN_PROGRAMS_PAGE = 500
HEIGHT_BTN_PROGRAMS_PAGE = 100
BORDER_WIDTH_BTN_PROGRAMS_PAGE = 0
CORNER_RADIUS_BTN_PROGRAMS_PAGE = 8

# Functions
def setup_home_page():
    """! Setups and starts the home page window with an appropriate name
    """
    window_home = common.generate_window('Home', 'Home - Zimmer Biomet Test Bench GUI')
    common.start_window(window_home)

def btn_event_switch_to_programs_page(current_window):
    """! Upon calling, destroys the home page and creates the programs page
    @param current_window   Window to be closed
    """
    common.close_window(current_window)

    programs_page.setup_programs_page()

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
        self.geometry(f"{WIDTH_HOME_PAGE} x {HEIGHT_HOME_PAGE}")

        ## Closing procedure for home page window
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        ## Button to access the available test programs
        btn_programs_page = customtkinter.CTkButton(text            = "Programs",
                                                    command         = lambda: btn_event_switch_to_programs_page(self),
                                                    width           = WIDTH_BTN_PROGRAMS_PAGE,
                                                    height          = HEIGHT_BTN_PROGRAMS_PAGE,
                                                    border_width    = BORDER_WIDTH_BTN_PROGRAMS_PAGE,
                                                    corner_radius   = CORNER_RADIUS_BTN_PROGRAMS_PAGE
                                                    )

        btn_programs_page.place(relx = RELX_BTN_PROGRAMS_PAGE, 
                                rely = RELY_BTN_PROGRAMS_PAGE,
                                anchor = tkinter.CENTER
                                )

    def on_closing(self):
        """! Procedure to follow upon closing a window object
        """
        self.destroy()

if __name__ == "__main__":
    """! Main program entry
    """
    setup_home_page()