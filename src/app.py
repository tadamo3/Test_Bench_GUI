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
import programs_page

# Global constants
## The width and height of the App
APP_WIDTH = 780
APP_HEIGHT = 520

## Indexes to access different pages
INDEX_HOME = 0
INDEX_PROGRAMS = 1
INDEX_LOGS = 2

# Classes
class App(customtkinter.CTk):
    """! App class for the Zimmer Test Bench
    Defines the components to select different pages
    """

    ## All pages accessible by user
    list_pages = ["Home", "Programs", "Logs"]
    dict_pages = {"Home" : None, "Programs" : None, "Logs" : None}

    ## Colors
    list_colors = ["red", "blue", "green"]

    def page_selector(self, page_to_switch):
        """! Puts a new page (frame) on top of the current page.
        @param page_to_switch      Page (frame) to put on top of the frame stack 
        """
        #self.pages[current_page].pack_forget()
        self.dict_pages[page_to_switch].pack(in_         = self.right_side_container, 
                                             side        = tkinter.TOP, 
                                             fill        = tkinter.BOTH, 
                                             expand      = True, 
                                             padx        = 0, 
                                             pady        = 0
                                            )

    def __init__(self, name_of_window):
        """! Initialisation of a new App object and generation of all related frames
        @param name_of_window     Name to be given to the App window
        @return An instance of the App window
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

        ## Generate main container and panel
        main_container = customtkinter.CTkFrame(self)
        main_container.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        # left side panel -> for frame selection
        left_side_panel = customtkinter.CTkFrame(main_container, width=150)
        left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False, padx=10, pady=10)

         # right side panel -> to show the frame1 or frame 2
        self.right_side_panel = customtkinter.CTkFrame(main_container)
        self.right_side_panel.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

        self.right_side_container = customtkinter.CTkFrame(self.right_side_panel)
        self.right_side_container.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

        ## Populate the different frames and generate window selector
        list_btn = []
        for i in range(len(self.list_pages)):
            self.dict_pages[self.list_pages[i]] = customtkinter.CTkFrame(fg_color=self.list_colors[i])
            list_btn.append(customtkinter.CTkButton(left_side_panel, 
                                                    padx        = 10,
                                                    pady        = 20,
                                                    text        = self.list_pages[i],
                                                    hover_color = "red",
                                                    command     = self.page_selector(self.list_pages[i])
                                                    )
                            )
            list_btn[i].grid(row    = i, 
                             column = 0
                            )

    def on_closing(self):
        """! Procedure to follow upon closing the App object
        """
        self.destroy()

if __name__ == "__main__":
    """! Main program entry
    """
    app_window = App("Zimmer Test Bench")
    app_window.mainloop()
    


