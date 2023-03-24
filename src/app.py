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
import serial_funcs
import manual_control
import programs_page

# Global constants
## The width and height of the App
APP_WIDTH = 1450
APP_HEIGHT = 1500

## Indexes to access different pages
INDEX_HOME = 0
INDEX_PROGRAMS = 1
INDEX_LOGS = 2

# Functions
def frame_selector(frame_to_init):
    """! Puts a new frame on top of the current frame and binds related keys to the frame's functionnalities
    @param frame_to_init    Frame to initialize and put on top of others
    """
    # Clear out every possible frame that is not the frame to initialize
    for i in range(len(App.dict_frames)):
        if (App.list_frames[i] != frame_to_init):
                App.dict_frames[App.list_frames[i]].pack_forget()

    # Bind / Unbind buttons related to the frames
    func_id = None
    if (frame_to_init == 'Home'):
        func_id = app_window.bind('<KeyPress>', manual_control.key_pressed)
        app_window.bind('<KeyRelease>', manual_control.key_released)
    else:
        app_window.unbind('<KeyPress>', func_id)

    # Initialize the correct frame
    App.dict_frames[frame_to_init].pack(
                                        in_         = app_window,
                                        side        = tkinter.TOP, 
                                        fill        = tkinter.BOTH,
                                        expand      = True, 
                                        padx        = 10, 
                                        pady        = 10)

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
        self.geometry(f'{APP_WIDTH}x{APP_HEIGHT}') 

        ## Closing procedure for App window
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        ## Left side panel creation for frame selection
        left_side_container = customtkinter.CTkFrame(self, width=150)
        left_side_container.pack(
                                    side    = tkinter.LEFT,
                                    fill    = tkinter.Y,
                                    expand  = False,
                                    padx    = 10,
                                    pady    = 10)

        ## Instanciate the different frames
        self.dict_frames[self.list_frames[INDEX_HOME]]      = home_page.HomePageFrame(master = self, fg_color="#1a1822")
        self.dict_frames[self.list_frames[INDEX_PROGRAMS]]  = programs_page.ProgramsPageFrame(master = self, fg_color="#1a1822")
        self.dict_frames[self.list_frames[INDEX_LOGS]]      = customtkinter.CTkFrame(master = self, fg_color="#1a1822")

        ## Instanciate the frame selector buttons and associate them with each frame
        list_btn_selector = []
        for i in range(len(self.dict_frames)):
            list_btn_selector.append(customtkinter.CTkButton(
                                                            left_side_container,
                                                            text        = self.list_frames[i],
                                                            hover_color = "red",
                                                            command     = lambda frame_to_init=self.list_frames[i] : frame_selector(frame_to_init)))
            list_btn_selector[i].place(
                                        x = 5,
                                        y = i * 50)

    def on_closing(self):
        """! Procedure on window closing to kill all remaining threads
        """
        home_page.home_page_stop_threads_event.set()
        self.destroy()

if __name__ == "__main__":
    """! Main program entry
    """
    app_window = App("Zimmer Test Bench")
    app_window.mainloop()