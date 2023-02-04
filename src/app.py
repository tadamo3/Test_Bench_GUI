##
# @file
# app.py
#
# @brief
# Base of the Zimmer Test Bench GUI.\n

# Imports
import tkinter
import customtkinter

import common
import home_page

# Global constants
## The width and height of the App
APP_WIDTH = 780
APP_HEIGHT = 520

## Indexes to access different pages
INDEX_HOME = 0
INDEX_PROGRAMS = 1
INDEX_LOGS = 2

# Functions
def frame_selector(position, frame_to_init):
        """! Puts a new frame on top of the current frame.
        @param position         Desired location of the frame
        @param frame_to_init    Frame to initialize and put on top of others
        """
        # Clear out every possible frame that is not the frame to initialize
        for i in range(len(App.dict_frames)):
            if (App.list_frames[i] != frame_to_init):
                    App.dict_frames[App.list_frames[i]].pack_forget()
        
        # Initialize the correct frame
        App.dict_frames[frame_to_init].pack(
                                            in_         = position, 
                                            side        = tkinter.TOP, 
                                            fill        = tkinter.BOTH, 
                                            expand      = True, 
                                            padx        = 0, 
                                            pady        = 0)

# Classes
class App(customtkinter.CTk):
    """! App class for the Zimmer Test Bench\n
    Defines the components to select different pages
    """

    ## All frames to be shown - The list purpose is to simplify index accessing
    list_frames = ["Home", "Programs", "Logs"]
    dict_frames = {"Home" : None, "Programs" : None, "Logs" : None}

    def __init__(self, name_of_window):
        """! Initialisation of a new App object and generation of all related frames
        @param name_of_window     Name to be given to the App window
        @return An instance of the App window containing all different populated frames to be shown
        """
        super().__init__()

        ## Title of the App window
        self.title(name_of_window)

        ## Set appearance of the App window
        common.set_appearance("Dark", "blue")

        ## Shape and size of the App window
        self.state('zoomed')
        self.geometry(f"{APP_WIDTH} x {APP_HEIGHT}")

        ## Closing procedure for App window
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        ## Generate main container to contain all frames
        main_container = customtkinter.CTkFrame(self)
        main_container.pack(
                            fill    = tkinter.BOTH,
                            expand  = True,
                            padx    = 10,
                            pady    = 10)

        ## Left side panel creation for frame selection
        left_side_panel = customtkinter.CTkFrame(main_container, width=150)
        left_side_panel.pack(
                            side    = tkinter.LEFT,
                            fill    = tkinter.Y,
                            expand  = False,
                            padx    = 10,
                            pady    = 10)

        ## Right side panel to show all different frames
        right_side_panel = customtkinter.CTkFrame(main_container)
        right_side_panel.pack(
                            side    = tkinter.LEFT,
                            fill    = tkinter.BOTH,
                            expand  = True, 
                            padx    = 0,
                            pady    = 0)

        ## Right side container to contain the right panel
        right_side_container = customtkinter.CTkFrame(right_side_panel)
        right_side_container.pack(
                                side    = tkinter.LEFT,
                                fill    = tkinter.BOTH,
                                expand  = True,
                                padx    = 0,
                                pady    = 0)

        ## Instanciate the different frames and generate the window selector
        list_btn_selector = []
        for i in range(len(self.dict_frames)):
            self.dict_frames[self.list_frames[i]] = customtkinter.CTkFrame(fg_color="#1a1822")
            list_btn_selector.append(customtkinter.CTkButton(
                                                            left_side_panel, 
                                                            padx        = 10,
                                                            pady        = 20,
                                                            text        = self.list_frames[i],
                                                            hover_color = "red",
                                                            command     = lambda frame_to_init=self.list_frames[i] : frame_selector(right_side_container, frame_to_init)))
            list_btn_selector[i].pack()

        ## Populate the different frames
        home_page.populate_home_page(self.dict_frames[self.list_frames[INDEX_HOME]])

    def on_closing(self):
        """! Procedure to follow upon closing the App object
        """
        self.destroy()

if __name__ == "__main__":
    """! Main program entry
    """
    app_window = App("Zimmer Test Bench")
    app_window.mainloop()