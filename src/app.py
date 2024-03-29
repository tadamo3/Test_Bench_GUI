##
# @file
# app.py
#
# @brief
# Base of the Zimmer Test Bench GUI.\n

# Imports
import customtkinter
from serial.tools import list_ports
from threading import Thread

from common import *
import home_page
from serial_funcs import *
import manual_control
import programs_page
import thread_manager

# Constants
## Base width of the App window
APP_WIDTH = 1920

## Base height of the App window
APP_HEIGHT = 1080

## Index to access the home page in the list of frames
INDEX_HOME = 0

## Index to access the programs page in the list of frames
INDEX_PROGRAMS = 1

## Available COM ports combobox width
CBBOX_WIDTH = 175

## Serial object representing the connected STM32
connected_device = [0]

binding_event_id = [0]

# Functions
def bind_unbind_keys_manual_control(frame_to_init, frame_object, connected_device_object):
    """! Binds keyboard events to specific actions for manual control of the tool
    @param frame_to_init    Name of the frame that is currently being initialized
    @param frame_object     Object of the frame that is currently being initialized
    @param connected_device_object          Serial object currently connected to the application
    """
    if (frame_to_init == 'Home'):
        binding_event_id[0] = app_window.bind('<KeyPress>', lambda event, previous_motor =  manual_control.previous_motor_controlled: manual_control.key_pressed(event, previous_motor, frame_object.list_directions_buttons, connected_device_object))
        app_window.bind('<KeyRelease>', lambda event, previous_motor = manual_control.previous_motor_controlled: manual_control.key_released(event, previous_motor, frame_object.list_directions_buttons, connected_device_object))
    else:
        if (binding_event_id[0] != None):
            app_window.unbind('<KeyPress>', binding_event_id[0])

def frame_selector(frame_to_init, connected_device_object):
    """! Sets desired frame as the visible frame (pushes back previous frame) \n
            Binds or unbinds keys related to the specific frame to be set
    @param frame_to_init                    Frame to initialize and put on top of others
    @param current_keyboard_binding_id      Current function ID corresponding to the binding or unbinding of the keyboard events
    @param connected_device_object          Serial object currently connected to the application
    """
    # Clear out every possible frame that is not the frame to initialize
    for i in range(len(App.dict_frames)):
        if (App.list_frames[i] != frame_to_init):
                App.dict_frames[App.list_frames[i]].grid_forget()

    # Initialize the correct frame
    App.dict_frames[frame_to_init].grid(
                                        row     = ROW_ONE,
                                        column  = COLUMN_ONE,
                                        padx    = PAD_X_USUAL,
                                        pady    = PAD_Y_USUAL,
                                        sticky  = 'nsew')
    
    bind_unbind_keys_manual_control(frame_to_init, App.dict_frames[frame_to_init], connected_device_object)

def combobox_com_ports_generate(frame, strvar_com_port_placeholder):
    """! Creates a combobox to list out all COM ports currently used by computer
    @param frame                            Frame on which the combobox will appear
    @param strvar_com_port_placeholder      StringVar object to contain the combobox current text
    @return An instance of the created combobox
    """
    # N.B: Separate function from the common.py function that generates comboboxes because of its relation with the serial port intialization
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
                                        variable    = strvar_com_port_placeholder,
                                        state       = "readonly")
    combobox.grid(
                    row         = ROW_ZERO,
                    column      = COLUMN_ZERO,
                    padx        = PAD_X_USUAL,
                    pady        = PAD_Y_USUAL,
                    sticky      = 'nsew')

    return combobox

def button_com_ports_click(combobox_com_port, thread_services, connected_device_object):
    """! On click, connects the GUI with the uC
    @param combobox_com_port        StringVar containing the current COM port selected
    @param connected_device_object  Connected device object to send and receive data
    """
    connected_device_object[INDEX_STM32] = connect_to_port(combobox_com_port)
    
    if (connected_device_object[INDEX_STM32] != None):
        print("COM port connected: ", combobox_com_port)
        print("Starting to read data")

        thread_rx_data = Thread(target = read_rx_buffer, args = (thread_services.serial_buffer_read_thread_event, connected_device_object, ))
        thread_rx_data.start()
    else:
        print("COM port unavailable")

    return connected_device_object

# Classes
class App(customtkinter.CTk):
    """! App class for the Zimmer Test Bench \n
    Is the main application base on which all the other frames exist
    """
    ## All frames to be shown - This list's purpose is to simplify index accessing
    list_frames = ["Home", "Programs"]

    ## Frame dictionnary associating a page name with its related frame
    dict_frames = {"Home" : None, "Programs" : None}

    ## List of buttons to select the frames - Initially empty (fills up when creating the buttons)
    list_btn_selector = []

    ## ID of the keyboard events
    keyboard_binding_event_id = None

    def instanciate_central_frames(self, frame_button_select_frames, thread_services, connected_device_object):
        """! Instanciates all of the main user frames (HomePage, ProgramsPage, etc.)
        @param frame_master             Master frame to contain the frame selection buttons
        @param thread_services          All thread related services to be dispatched throughout the different GUI frames
        @param connected_device_object  Serial object currently connected to the application
        """
        self.dict_frames[self.list_frames[INDEX_HOME]]      = home_page.HomePageFrame(
                                                                                        master = self,
                                                                                        thread_services = thread_services,
                                                                                        connected_device = connected_device_object,
                                                                                        fg_color="#1a1822")
        self.dict_frames[self.list_frames[INDEX_PROGRAMS]]  = programs_page.ProgramsPageFrame(
                                                                                                master = self, 
                                                                                                thread_services = thread_services,
                                                                                                connected_device = connected_device_object,
                                                                                                fg_color="#1a1822")

        # Populate the left side frame and link the correct frame to initialize with the correct button
        for i in range(len(self.dict_frames)):
            self.list_btn_selector.append(customtkinter.CTkButton(
                                                                    frame_button_select_frames,
                                                                    text        = self.list_frames[i],
                                                                    hover_color = "red",
                                                                    command     = lambda frame_to_init = self.list_frames[i] : frame_selector(frame_to_init, connected_device_object)))
            self.list_btn_selector[i].grid(
                                            row     = i,
                                            column  = COLUMN_ONE, 
                                            padx    = PAD_X_USUAL,
                                            pady    = 50,
                                            sticky  = "nsew")

    def __init__(self, name_of_window, thread_services):
        """! Initialisation of a new App class and generation of all of the GUI frames
        @param name_of_window     Name to be given to the App window
        @param thread_services    All thread related services to be dispatched throughout the different GUI frames  
        @return An instance of the App window containing all different populated frames to be shown
        """
        super().__init__()

        # Set appearance of the App window
        self.title(name_of_window)
        set_appearance('Dark', 'blue')
        self.state('zoomed')
        self.geometry(f'{APP_WIDTH}x{APP_HEIGHT}') 

        # Closing procedure to call when the App window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Configure the grid system with specific weights for the main window
        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure(0, weight = 0)
        self.grid_columnconfigure(1, weight = 1)

        # Position all necessary frames
        frame_left_side = customtkinter.CTkFrame(self)
        frame_left_side.grid(
                                row     = ROW_ZERO,
                                column  = COLUMN_ZERO,
                                rowspan = 2,
                                padx    = PAD_X_USUAL,
                                pady    = PAD_Y_USUAL,
                                sticky  = "nsew")

        frame_top_side = customtkinter.CTkFrame(self)
        frame_top_side.grid(
                            row     = ROW_ZERO, 
                            column  = COLUMN_ONE, 
                            padx    = PAD_X_USUAL, 
                            pady    = PAD_Y_USUAL, 
                            sticky  = "nsew")
        
        # Populate the top side frame
        strvar_current_com_port = customtkinter.StringVar(self)
        cbbox_com_ports = combobox_com_ports_generate(frame_top_side, strvar_current_com_port)

        btn_com_ports = button_generate(
                                            frame_top_side, 
                                            ROW_ZERO, 
                                            COLUMN_ONE, 
                                            1, 
                                            1, 
                                            PAD_X_USUAL, 
                                            PAD_Y_USUAL, 
                                            "Connect")
        btn_com_ports.configure(command = lambda : button_com_ports_click(
                                                                            cbbox_com_ports.get(),
                                                                            thread_services,
                                                                            connected_device))

        self.instanciate_central_frames(frame_left_side, thread_services, connected_device)

    def on_closing(self):
        """! Procedure to execute on window closing event
        """
        self.destroy()

if __name__ == "__main__":
    """! Main program entry
    """
    # Initialize different services
    thread_services = thread_manager.ThreadManager()

    app_window = App("Zimmer Test Bench", thread_services)
    app_window.mainloop()

    # Closing procedure in case of exit of mainloop
    thread_services.close_all_threads()