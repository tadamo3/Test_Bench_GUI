##
# @file
# common.py
#
# @brief
# This file contains all common functions to help setup of every page of the GUI. \n

# Imports
import tkinter
import customtkinter

# Functions
def set_appearance(appearance_mode, default_color_theme):
    """! Sets the appearance of a given page
    @param appearance_mode          Appearance to give to the page
    @param default_color_theme      Color theme to give to the page
    """
    customtkinter.set_appearance_mode(appearance_mode)
    customtkinter.set_default_color_theme(default_color_theme)