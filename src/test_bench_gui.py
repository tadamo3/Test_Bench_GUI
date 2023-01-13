"""
@name_of_file
test_bench_gui.py

@brief
This file acts as the main file for the Zimmer testbench GUI
All components positioning will be done here while the corresponding functions
    will be called from other files
"""

import tkinter
import customtkinter
import tkinter.messagebox

def button_event(textbox_name_of_program):
    print(textbox_name_of_program)

def set_appearance_gui(appearance_mode, default_color_theme):
    """Set appearance of the GUI
    """
    customtkinter.set_appearance_mode(appearance_mode)
    customtkinter.set_default_color_theme(default_color_theme)

class HomePage(customtkinter.CTk):
    """Main page for the testbench GUI
    """
    WIDTH = 780
    HEIGHT = 520

    def __init__(self, name_of_page):
        """Initialisation of a new window propreties upon creation of the object

        Args:
            name_of_page (string): Name to be given to the window object
        """
        
        super().__init__()

        self.title(name_of_page)
        self.geometry(f"{HomePage.WIDTH} x {HomePage.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        """Programs page button - Switches to the programs list page
        """
        button_programs_page = customtkinter.CTkButton( text = "Programs",
                                                        command = lambda: button_event("txtbx_name_of_program"),
                                                        width = 120,
                                                        height = 32,
                                                        border_width = 0,
                                                        corner_radius = 8)
        button_programs_page.place(relx = 0.3, rely = 0.3, anchor = tkinter.CENTER)

    def on_closing(self):
        """Procedure to follow upon closing a window object
        """
        self.destroy()


if __name__ == "__main__":
    """Entry point of file
    """
    set_appearance_gui("Dark", "blue")
    window_home = HomePage("Home - Zimmer Biomet Test Bench")
    window_home.mainloop()