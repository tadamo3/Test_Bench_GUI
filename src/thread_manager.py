##
# @file
# thread_manager.py
#
# @brief
# Thread manager of the GUI.\n

# Imports
from threading import Event, Thread

from automatic_control import *

class ThreadManager():
    """! Thread managing class giving specific access to the thread managing events and functions
    """
    ## Thread event to stop the serial buffer reading
    serial_buffer_read_thread_event = Event()

    ## Thread event to stop the test of automatic movement in the home page
    auto_test_mode_thread_event = Event()

    ## Thread event to stop the automatic mode position control
    auto_mode_thread_event = Event()

    ## Thread event to pause the automatic mode position control
    auto_mode_pause_thread_event = Event()

    ## List of thread events for further management purposes
    list_thread_events = [serial_buffer_read_thread_event, auto_mode_thread_event, auto_mode_pause_thread_event, auto_test_mode_thread_event]

    def close_all_threads(self):
        """! Closes all threads in order to correctly quit the application
        """
        for i in range(len(self.list_thread_events)):
            self.list_thread_events[i].set()

    def start_test_repetition_thread(self, desired_position, desired_direction, desired_turns, connected_device):
        """! Manages the start of the automatic test mode available in the home page
        @param desired_position     Amplitude of movement in millimeters
        @param desired_direction    Combination of movements to execute in repetition
        @param desired_turns        Number of turns for the adaptor motor to execute
        @param connected_device     The Serial object currently connected to the application
        """
        self.auto_test_mode_thread_event.clear()

        thread_auto_mode = None
        thread_auto_mode = Thread(target = AutomaticMode.auto_mode_test, args = (desired_position, desired_direction, desired_turns, connected_device, self.auto_test_mode_thread_event, ))
        thread_auto_mode.start()

    def stop_test_repetition_thread(self):
        """! Manages the stop of the automatic test mode available in the home page
        """
        self.auto_test_mode_thread_event.set()