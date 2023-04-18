##
# @file
# app.py
#
# @brief
# Base of the Zimmer Test Bench GUI.\n

# Imports
import tkinter
import customtkinter
import time
from threading import Event
from serial.tools import list_ports

from common import *
import home_page
from serial_funcs import *
import manual_control
import programs_page

# Global constants
## The width and height of the App
APP_WIDTH = 1450
APP_HEIGHT = 1500

## Indexes to access different pages
INDEX_HOME      = 0
INDEX_PROGRAMS  = 1
#INDEX_LOGS      = 2

## Info about the combobox ports
CBBOX_COM_PORTS_X   = 20
CBBOX_COM_PORTS_Y   = 20
CBBOX_WIDTH         = 175

home_page_stop_threads_event = Event()
auto_mode_thread_event = Event()
auto_mode_pause_thread_event = Event()


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
        func_id = app_window.bind('<KeyPress>', lambda event, previous_motor =  manual_control.previous_motor_controlled: manual_control.key_pressed(event, previous_motor, home_page.list_buttons_manual_control))
        app_window.bind('<KeyRelease>', lambda event, previous_motor = manual_control.previous_motor_controlled: manual_control.key_released(event, previous_motor, home_page.list_buttons_manual_control))
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

def combobox_com_ports_generate(frame, strvar_com_port_placeholder):
        """! Creates a combobox to list out all COM ports currently used by computer
        @param frame                    Frame on which the combobox will appear
        @param com_port_placeholder     StringVar to contain the combobox current text
        @return An instance of the created combobox
        """
        com_ports = list_ports.comports()
        list_com_ports = []
        
        if (len(com_ports) != 0):
            for port in com_ports:
                list_com_ports.append(port.name)
        else:
            list_com_ports += ["No COM Port detected"]

        combobox = customtkinter.CTkComboBox(
                                            master      = frame,
                                            width       = CBBOX_WIDTH,
                                            values      = list_com_ports,
                                            variable    = strvar_com_port_placeholder)
        combobox.place(
                        x = CBBOX_COM_PORTS_X,
                        y = CBBOX_COM_PORTS_Y)

        return combobox

def button_com_ports_click(button_com_port, combobox_com_port, list_com_device_info):
    """! On click, prints out the current value of the COM ports combobox
    @param combobox_com_port    StringVar containing the current COM port selected
    @param list_com_device_info Notable information for all connected devices
    """
    if (combobox_com_port != ""):
        print("COM port to be connected: ", combobox_com_port)
        list_com_device_info[0] = connect_to_port(combobox_com_port)

        button_com_port.configure(state = "disabled")
    else:
        print("No COM port selected")

# Classes
class App(customtkinter.CTk):
    """! App class for the Zimmer Test Bench\n
    Defines the components to select different pages
    """
    ## All frames to be shown - The list purpose is to simplify index accessing
    list_frames = ["Home", "Programs"]
    dict_frames = {"Home" : None, "Programs" : None}

    def __init__(self, name_of_window):
        """! Initialisation of a new App object and generation of all related frames
        @param name_of_window     Name to be given to the App window
        @return An instance of the App window containing all different poSpulated frames to be shown
        """
        super().__init__()

        ## Title of the App window
        self.title(name_of_window)

        ## Set appearance of the App window
        set_appearance("Dark", "blue")

        ## Shape and size of the App window
        self.state('zoomed')
        self.geometry(f'{APP_WIDTH}x{APP_HEIGHT}') 

        ## Closing procedure for App window
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        ## Left side panel creation for frame selection
        left_side_container = customtkinter.CTkFrame(self, width = 150)
        left_side_container.pack(
                                    side    = tkinter.LEFT,
                                    fill    = tkinter.Y,
                                    expand  = False,
                                    padx    = 10,
                                    pady    = 10)

        ## Upper panel creation for connection settings
        connection_settings_container = customtkinter.CTkFrame(self, width = 150, height = 100)
        connection_settings_container.pack(
                                            side    = tkinter.TOP,
                                            fill    = tkinter.X,
                                            expand  = False,
                                            padx    = 10,
                                            pady    = 10)
        
        ## Create button for connection settings
        strvar_current_com_port = customtkinter.StringVar(self)

        # Generate all comboboxes
        cbbox_com_ports = combobox_com_ports_generate(connection_settings_container, strvar_current_com_port)

        btn_com_ports = button_generate(connection_settings_container, (CBBOX_COM_PORTS_X * 12), CBBOX_COM_PORTS_Y, "Connect")
        btn_com_ports.configure(command = lambda : button_com_ports_click(
                                                                            btn_com_ports,
                                                                            cbbox_com_ports.get(),
                                                                            g_list_connected_device_info))

        ## Instanciate the different frames
        self.dict_frames[self.list_frames[INDEX_HOME]]      = home_page.HomePageFrame(master = self, fg_color="#1a1822")
        self.dict_frames[self.list_frames[INDEX_PROGRAMS]]  = programs_page.ProgramsPageFrame(master = self, fg_color="#1a1822")
        #self.dict_frames[self.list_frames[INDEX_LOGS]]      = customtkinter.CTkFrame(master = self, fg_color="#1a1822")

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
        home_page_stop_threads_event.set()
        self.destroy()

if __name__ == "__main__":
    """! Main program entry
    """
    app_window = App("Zimmer Test Bench")
    app_window.mainloop()