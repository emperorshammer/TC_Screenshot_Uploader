'''#-------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        TC Screenshot Uploader.py
# Purpose:     A program used to automatically upload game screenshots to the EHTC database.
# Version:     v1.0.2
# Author:      S. Macintosh AKA SkyShadow
#
# Created:     25/05/2021
# Copyright:   None
# Licence:     None
#-------------------------------------------------------------------------------------------------------------------------------------------------#'''


#----------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                      Imports.                                                                      #
#----------------------------------------------------------------------------------------------------------------------------------------------------#
import mechanize
import shutil
import os
import glob
from PIL import Image
import win32gui, win32com.client
from time import sleep
import configparser
#----------------------------------------------------------------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                      Functions.                                                                    #
#----------------------------------------------------------------------------------------------------------------------------------------------------#
def initialSetup():
    '''Function that sets up this application for use.'''

    # Create the required folder structure.
    try:
        os.mkdir(os.getcwd() + "\\Submitted")
    except FileExistsError:
        pass # Folder already exists.
#----------------------------------------------------------------------------------------------------------------------------------------------------#


def loadSettings():
    '''Function that reads in the user settings from "settings.ini".'''

    config = configparser.ConfigParser()
    config.read("settings.ini")
    return config
#----------------------------------------------------------------------------------------------------------------------------------------------------#


def bringAppToFront():
    '''Function that brings this app to the front of all other windows.'''

    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if "tc screenshot uploader" in i[1].lower() or "cmd.exe" in i[1].lower():
            win32gui.ShowWindow(i[0],5)
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            win32gui.SetForegroundWindow(i[0])
            break
#----------------------------------------------------------------------------------------------------------------------------------------------------#


def windowEnumerationHandler(hwnd, top_windows):
    '''Function that handles itteration through windows.'''

    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
#----------------------------------------------------------------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                     Main Program.                                                                  #
#----------------------------------------------------------------------------------------------------------------------------------------------------#
initialSetup()
config = loadSettings()

# Main program monitor loop.
while True:
    # Search for screenshots.
    filenames = glob.glob("*.png")

    # Intro message.
    os.system("cls")
    print("\n\n------SkyShadow's Auto Screenshot Submitter.------")
    print("\n\nMonitoring for screenshots...")

    # Auto-submit any found screenshots.
    if filenames != []:

        # Log in to the administration page of the TC website.
        browser = mechanize.Browser()
        browser.open(config.get("settings", "tc_admin_url"))
        browser.form = list(browser.forms())[0]
        browser["pin"] = config.get("settings", "pin")
        browser["pass"] = config.get("settings", "password")
        browser.submit()

        for filename in filenames:
            print("\n\nDetected: " + filename)

            # Open and complete the match submission form.
            browser.open(config.get("settings", "tc_submit_coop_url"))
            browser.form = list(browser.forms())[0] # Get the first from from the webpage.
            browser["game"] = [config.get("settings", "game")]
            browser["name1w"] = [config.get("settings", "pin")]
            bringAppToFront()
            browser["kill1w"] = input("Please enter your number of kills and press 'enter': ")

            # Add the screenshot data and submit the form.
            screenshot = open(filename, 'rb')
            browser.form.add_file(screenshot, 'image/png', filename, 'ss1')
            browser.submit()
            screenshot.close()
            shutil.move(filename, "Submitted/" + filename)
            print("Upload Complete - " + filename)
            sleep(2)

    sleep(0.5)
#----------------------------------------------------------------------------------------------------------------------------------------------------#
