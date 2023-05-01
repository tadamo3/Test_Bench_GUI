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
    ## Thread event to stop the serial buffer reading
    home_page_stop_threads_event = Event()

    ## Thread event to stop the automatic mode position control
    auto_mode_thread_event = Event()

    ## Thread event to pause the automatic mode position control
    auto_mode_pause_thread_event = Event()

    ## List of thread events for further management purposes
    list_thread_events = [home_page_stop_threads_event, auto_mode_thread_event, auto_mode_pause_thread_event]

    def close_all_threads(self):
        for i in range(len(self.list_thread_events)):
            self.list_thread_events[i].set()

    def start_test_repetition_thread(self, desired_position, desired_direction, desired_turns):
        self.home_page_stop_threads_event.clear()

        thread_auto_mode = None
        thread_auto_mode = Thread(target = AutomaticMode.auto_mode_test, args = (desired_position, desired_direction, desired_turns, self.home_page_stop_threads_event, ))
        thread_auto_mode.start()

    def stop_test_repetition_thread(self):
        self.home_page_stop_threads_event.set()