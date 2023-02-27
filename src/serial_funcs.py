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
COMMAND_RESERVED                    = 0
COMMAND_MOTOR_VERTICAL_UP           = 1
COMMAND_MOTOR_VERTICAL_DOWN         = 2
COMMAND_MOTOR_VERTICAL_STOP         = 3
COMMAND_MOTOR_HORIZONTAL_RIGHT      = 4
COMMAND_MOTOR_HORIZONTAL_LEFT       = 5
COMMAND_MOTOR_CHANGE_SPEED          = 6
COMMAND_READ_ENCODER_VERTICAL_LEFT  = 7
COMMAND_READ_ENCODER_VERTICAL_RIGHT = 8
COMMAND_READ_ENCODER_HORIZONTAL     = 9
COMMAND_ENABLE_MANUAL_MODE          = 10
COMMAND_ENABLE_AUTOMATIC_MODE       = 11

DATA_NONE = 0

## Masks to retrieve information from the data received
MASK_ID         = 0xFF000000
MASK_COMMAND    = 0x00FF0000
MASK_DATA       = 0x0000FFFF

## Indexes to access different parts of the message
INDEX_ID        = 0
INDEX_COMMAND   = 1
INDEX_DATA      = 2

# Global variables
g_list_connected_device_info = [0]
g_list_message_info = [0, 0, 0]

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
            #print("No connection found")
            
            return None

def receive_serial_data(list_message_info, list_com_device_info):
    """! Reads a constant number of bytes from the serial input buffer\n
    Divides a message in its core components
    @param list_message_info        Notable information for the received serial message
    @param list_com_device_info     Notable information for all connected devices
    """
    rx_buffer = -1

    if (list_com_device_info[0] != 0):
        rx_buffer = list_com_device_info[0].read(NUM_BYTES_TO_READ)
        rx_buffer = int.from_bytes(rx_buffer, ENDIANNESS)

        list_message_info[INDEX_ID]         = (rx_buffer & MASK_ID) >> 24
        list_message_info[INDEX_COMMAND]    = (rx_buffer & MASK_COMMAND) >> 16
        list_message_info[INDEX_DATA]       = (rx_buffer & MASK_DATA)
        
        print(
                "Component ID: " + str(list_message_info[INDEX_ID]) + 
                "Command: " + str(list_message_info[INDEX_ID]) + 
                "Data: " + str(list_message_info[INDEX_DATA]))
    #else:
        #print("No data received, check COM port")

def transmit_serial_data(id, command, data, list_com_device_info):
    """! Builds the desired message to transmit and writes it to the microcontroler
    @param id       The ID of the component to write to
    @param command  The command to write to the component
    @param data     The data to transmit to the component
    """
    if (list_com_device_info[0] != 0):
        # Create message with appropriate positioning of bytes
        message_to_send = data + (command << 16) + (id << 24)

        bytes_to_send = message_to_send.to_bytes(NUM_BYTES_TO_SEND, ENDIANNESS)
        list_com_device_info[0].write(bytes_to_send)

        print("Message sent: ", bytes_to_send)
    else:
        print("Could not send data")