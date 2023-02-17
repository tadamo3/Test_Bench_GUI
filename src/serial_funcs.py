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
ENDIANNESS = 'little'
NUM_BYTES_TO_READ = 4
NUM_BYTES_TO_SEND = 4

## ID of Test Bench components - Must be the same as the ones found in Serial_Communication/serial_com.h
ID_RESERVED                 = 0
ID_ENCODER_VERTICAL_LEFT    = 1
ID_ENCODER_VERTICAL_RIGHT   = 2
ID_ENCODER_HORIZONTAL       = 3
ID_MOTOR_VERTICAL_LEFT      = 4
ID_MOTOR_VERTICAL_RIGHT     = 5
ID_MOTOR_HORIZONTAL         = 6

## Commands of Test Bench comoponents - Must be the same as the ones found in Serial_Communication/serial_com.h
COMMAND_RESERVED                = 0
COMMAND_MOTOR_VERTICAL_UP       = 1
COMMAND_MOTOR_VERTICAL_DOWN     = 2
COMMAND_MOTOR_VERTICAL_STOP     = 3

## Masks to retrieve information from the data received
MASK_ID = 0xFF000000
MASK_DATA = 0x0000FFFF

# Global variables
g_list_connected_device_info = [0]

# Functions
def connect_to_port(selected_com_port):
    """! Establishes connection with selected COM port
    @param selected_com_port   Selected COM port
    @return The COM port object if connected, else None
    """
    is_port_open = False
    while not is_port_open:
        try:
            stm_32 = serial.Serial(
                                    port            = selected_com_port,
                                    baudrate        = BAUDRATE,
                                    timeout         = None,
                                    write_timeout   = 0,
                                    xonxoff         = False,
                                    rtscts          = False,
                                    dsrdtr          = False)

            stm_32.flushInput()
            stm_32.flushOutput()

            is_port_open = True
            print("STM32 is connected")

            return stm_32
        except:
            print("No connection found")
            
            return None

def receive_serial_data(list_com_device_info):
    rx_buffer = -1

    if (list_com_device_info[0] != 0):
        rx_buffer = list_com_device_info[0].read(NUM_BYTES_TO_READ)
        rx_buffer = int.from_bytes(rx_buffer, ENDIANNESS)

        id = find_message_id(rx_buffer)
        data = find_message_data(rx_buffer)

        print("Component ID: ", id)
        print("Data: ", data)
    else:
        print("No data received, check COM port")

    return rx_buffer

def find_message_id(message_received):
    command = (message_received & MASK_ID) >> 24

    return command

def find_message_data(message_received):
    data = (message_received & MASK_DATA)

    return data

def transmit_serial_data(id, data, list_com_device_info):
    if (list_com_device_info[0] != 0):
        # Create message with appropriate positioning of data and component id
        message_to_send = data + (id << 24)

        bytes_to_send = message_to_send.to_bytes(NUM_BYTES_TO_SEND, ENDIANNESS)
        list_com_device_info[0].write(message_to_send)

        print("Message sent: ", bytes_to_send)
    else:
        print("Could not send data")