##
# @file
# serial_funcs.py
#
# @brief
# Helper file for serial communication with the STM32 microcontroller. \n

# Imports
import serial

# Constants
BAUDRATE = 115200
endianness = 'little'

# Global variables
g_list_connected_device_info = [0]

# Functions
def connect_to_port(selected_com_port):
    """! Establishes connection with selected COM port
    @param selected_com_port   Selected COM port
    @return The COM port object if connected
    """
    is_port_open = False
    while not is_port_open:
        try:
            stm_32 = serial.Serial(
                                    port        = selected_com_port,
                                    baudrate    = BAUDRATE,
                                    timeout     = None,
                                    xonxoff     = False,
                                    rtscts      = False,
                                    dsrdtr      = False)

            stm_32.flushInput()
            stm_32.flushOutput()

            is_port_open = True
            print("STM32 is connected")

            return stm_32
        except:
            print("No connection found")
            
            return None

def send_new_vertical_speed(vertical_speed, list_com_device_info):
    if (list_com_device_info[0] != 0):
        bytes_vertical_speed = vertical_speed.to_bytes(1, endianness)
        list_com_device_info[0].write(bytes_vertical_speed)

        print("Vertical speed sent:", vertical_speed)
    else:
        print("Could not send vertical speed")

def receive_serial_data(list_com_device_info):
    rx_buffer = -1

    if (list_com_device_info[0] != 0):
        rx_buffer = list_com_device_info[0].read()
        rx_buffer = int.from_bytes(rx_buffer, endianness)
        print("RX received :", rx_buffer)
    else:
        print("Could not receive data")

    return rx_buffer