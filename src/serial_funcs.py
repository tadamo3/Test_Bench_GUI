##
# @file
# serial_funcs.py
#
# @brief
# Helper file for serial communication with the STM32 microcontroller. \n

# Imports
import serial
import time

from common import *

path_logs = 'logs/encoder_logs.txt'

# Constants
## Index position of the connected device
INDEX_STM32 = 0

## Used baudrate for serial communication
BAUDRATE = 115200

## Used endianness for sending data
ENDIANNESS = 'little'

## Number of bytes to read for every frame sent by the microcontroler
NUM_BYTES_TO_READ = 4

## Number of bytes to send to send a complete frame
NUM_BYTES_TO_SEND = 4

## ID of Test Bench components - Must be the same as the ones found in Serial_Communication/serial_com.h
ID_RESERVED                 = 0
ID_ENCODER_VERTICAL_LEFT    = 1
ID_ENCODER_VERTICAL_RIGHT   = 2
ID_ENCODER_HORIZONTAL       = 3
ID_MOTOR_VERTICAL_LEFT      = 4
ID_MOTOR_VERTICAL_RIGHT     = 5
ID_MOTOR_HORIZONTAL         = 6
ID_MOTOR_ADAPT              = 7

## Commands of Test Bench comoponents - Must be the same as the ones found in Serial_Communication/serial_com.h
COMMAND_RESERVED                    = 0
COMMAND_MOTOR_VERTICAL_UP           = 1
COMMAND_MOTOR_VERTICAL_DOWN         = 2
COMMAND_MOTOR_VERTICAL_STOP         = 3
COMMAND_MOTOR_HORIZONTAL_RIGHT      = 4
COMMAND_MOTOR_HORIZONTAL_LEFT       = 5
COMMAND_MOTOR_HORIZONTAL_STOP       = 6
COMMAND_MOTOR_CHANGE_SPEED          = 7
COMMAND_MOTOR_ADAPT_UP              = 8
COMMAND_MOTOR_ADAPT_DOWN            = 9
COMMAND_MOTOR_ADAPT_STOP            = 10
COMMAND_SOFT_RESET                  = 11

## Motor possible states
MOTOR_STATE_RESERVED            = 0
MOTOR_STATE_VERTICAL_UP         = 1
MOTOR_STATE_VERTICAL_DOWN       = 2
MOTOR_STATE_HORIZONTAL_RIGHT    = 3
MOTOR_STATE_HORIZONTAL_LEFT     = 4
MOTOR_STATE_VERTICAL_STOP       = 5
MOTOR_STATE_HORIZONTAL_STOP     = 6
MOTOR_STATE_AUTO_IN_TRAJ        = 7
MOTOR_STATE_AUTO_END_OF_TRAJ    = 8
MOTOR_STATE_CHANGE_PARAMS       = 9
MOTOR_STATE_ADAPT_UP            = 10
MOTOR_STATE_ADAPT_DOWN          = 11
MOTOR_STATE_ADAPT_STOP          = 12

## Motor possible faults
MOTOR_FAULT_NONE         = 0
MOTOR_FAULT_INVALID_ID   = 1

## Available modes
MODE_RESERVED           = 0
MODE_MANUAL_CONTROL     = 1
MODE_POSITION_CONTROL   = 2
MODE_RESET              = 3
MODE_CHANGE_PARAMS      = 4

## Masks to retrieve information from the data received
MASK_ID         = 0xFF000000
MASK_MODE       = 0x00C00000
MASK_COMMAND    = 0x003F0000
MASK_DATA       = 0x0000FFFF

## Indexes to access different parts of the message to transmit
INDEX_ID        = 0
INDEX_MODE      = 1
INDEX_COMMAND   = 2
INDEX_DATA      = 3

## Indexes to access different parts of the message to transmit
INDEX_ID                        = 0
INDEX_STATUS_MOVEMENT_MOTOR     = 1
INDEX_STATUS_MOTOR              = 2
INDEX_MOTOR_POSITION            = 3

DATA_NONE = 0

# Global variables
g_list_connected_device_info = [0]
g_list_message_info = [0, 0, 0, 0]

# Functions
def read_rx_buffer(stop_event, connected_device):
    """! Reads serial data in a continuous stream\n
    Rate of reading must be the same of higher than the rate of sending from the uC
    @param stop_event      When set (true), stops the data reception
    """
    while (stop_event.is_set() != True):
        receive_serial_data(
                            g_list_message_info,
                            connected_device)

        time.sleep(0.05)

def connect_to_port(selected_com_port):
    """! Establishes connection with selected COM port
    @param selected_com_port   The selected communication port on the computer
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

def receive_serial_data(list_message_info, list_com_device_info):
    """! Reads a constant number of bytes from the serial input buffer\n
    Divides a message in its core components
    @param list_message_info        Notable information for the received serial message
    @param list_com_device_info     Notable information for all connected devices
    """
    rx_buffer = [0]

    if (list_com_device_info[0] != None):
        rx_buffer[0] = list_com_device_info[0].read(NUM_BYTES_TO_READ)
        rx_buffer[0] = int.from_bytes(rx_buffer[0], ENDIANNESS)

        list_message_info[INDEX_ID]                     = ((rx_buffer[0] & 0x00FF0000) >> 16)
        list_message_info[INDEX_STATUS_MOVEMENT_MOTOR]  = ((rx_buffer[0] & 0x0000FF00) >> 8)
        list_message_info[INDEX_STATUS_MOTOR]           = (rx_buffer[0] & 0x000000FF)
        print(
                "ID: "                  + str(list_message_info[INDEX_ID]) +
                " Status movement: "     + str(list_message_info[INDEX_STATUS_MOVEMENT_MOTOR]) +
                " State: "               + str(list_message_info[INDEX_STATUS_MOTOR])
            )

def transmit_serial_data(id, command, mode, data, connected_device):
    """! Builds the desired message to transmit and writes it to the microcontroler
    @param id               The ID of the component to write to
    @param command          The command to write to the component
    @param mode             The mode in which the test bench is functionning
    @param data             The data to transmit to the component
    @connected_device       The serial object currently connected to the application
    """
    if (connected_device[INDEX_STM32] != None):
        # Create message with appropriate positioning of bytes
        message_to_send = data + (command << 16) + (mode << 21) + (id << 24)

        bytes_to_send = message_to_send.to_bytes(NUM_BYTES_TO_SEND, ENDIANNESS)
        connected_device[INDEX_STM32].write(bytes_to_send)

        print("Message sent: ", bytes_to_send.hex())
    else:
        print("Could not send data")
        