##
# @file
# test_bench_gui.py
#
# @brief
# This file acts as the main file for the Zimmer testbench GUI.
# All components positioning will be done here while the corresponding functions
#    will be called from other files.

# Imports
import tkinter
import customtkinter
import tkinter.messagebox

# Global constants
## The width of the GUI Home Page
WIDTH = 780

## The height of the GUI Home Page
HEIGHT = 520

# Functions
def button_event(text):
    """! Prints out a given text
    @param textbox_name_of_program      The text to be printed out
    """
    print(text)

def set_appearance_gui(appearance_mode, default_color_theme):
    """! Sets the appearance of the GUI
    @param appearance_mode          Appearance to give to the GUI
    @param default_color_theme      Color theme to give to the GUI
    """
    customtkinter.set_appearance_mode(appearance_mode)
    customtkinter.set_default_color_theme(default_color_theme)

# Classes
class HomePage(customtkinter.CTk):
    """! Main page for the testbench GUI
    Defines all components of the testbench home page
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
        button_programs_page = customtkinter.CTkButton( text = "Programs",
                                                        command = lambda: button_event("txtbx_name_of_program"),
                                                        width = 120,
                                                        height = 32,
                                                        border_width = 0,
                                                        corner_radius = 8)
        button_programs_page.place(relx = 0.3, rely = 0.3, anchor = tkinter.CENTER)

    def on_closing(self):
        """! Procedure to follow upon closing a window object
        """
        self.destroy()

if __name__ == "__main__":
    """! Main program entry
    """
    set_appearance_gui("Dark", "blue")
    window_home = HomePage("Home - Zimmer Biomet Test Bench")
    window_home.mainloop()