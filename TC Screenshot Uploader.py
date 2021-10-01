'''#-------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        TC Screenshot Uploader.py
# Purpose:     A program used to automatically upload game screenshots to the EHTC database.
# Version:     v1.0.3
# Author:      S. Macintosh AKA SkyShadow
#
# Created:     13/07/2021
# Copyright:   Open Source
# Licence:     Open Source
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
import ssl
#----------------------------------------------------------------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                      Functions.                                                                    #
#----------------------------------------------------------------------------------------------------------------------------------------------------#
def initialSetup():
    '''Function that sets up this application for use.'''

    # Create the required folder structure in each game direcory. e.g. Submitted folders.
    for option in config.options("folders"):
        folder = config.get("folders", option)
        try:
            os.mkdir(folder + "\\Submitted")
        except FileExistsError:
            pass # Folder already exists.
        except FileNotFoundError:
            os.system("cls")
            print("\n\n\n\n\tERROR! %s not found on this computer.\n\tPlease ensure that the folder paths are set correctly in 'settings.ini'."%folder)
            input("\n\tPress 'Enter' to exit.")
            raise Exception() # Force closes the application.
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


def askForGame():
    '''Function asks the user for which game the user is playing.'''

    #      User Input : [ "PvE Name" , "PvP Name" , "Game Name", "Screenshot Path Option"]
    gamesDict = {"xvt" : ["XvT2", "XvT", "X-Wing Vs. Tie Fighter", "screenshot_folder_xvt"],
                "xwa" : ["XWA2", "XWA", "X-Wing Alliance", "screenshot_folder_xwa"],
                "sc" :  ["SC2", "SC", "Star Conflict", "screenshot_folder_sc"],
                "bf1" : ["BF32", "BF3", "EA Star Wars Battlefront", "screenshot_folder_eabf1"],
                "bf2" : ["EABFII", "BF2", "EA Star Wars Battlefront II", "screenshot_folder_eabf2"],
                "sws" : ["SWS2", "SWS", "Star Wars Squadrons", "screenshot_folder_sws"]}

    print("\n")
    for game in gamesDict:
        if config.get("folders", gamesDict[game][3]):
            print("\t" + game + " = " + gamesDict[game][2])

    gameStr = input("\n\tWhich game are you playing? ").lower()

    while gameStr not in gamesDict.keys():
        os.system("cls")
        print(header)
        print("\n")
        for game in gamesDict:
            if config.get("folders", gamesDict[game][3]):
                print("\t" + game + " = " + gamesDict[game][2])
        gameStr = input("\n\tSorry that option isn't available...\n\n\tWhich game are you playing? ").lower()

    # Get the game mode to be played.
    os.system("cls")
    print(header)
    print("\n")
    mode, modeTitle = askForMode()
    if mode == "pve":
        modeNum = 0
    elif mode == "pvp":
        modeNum = 1

    return gamesDict[gameStr][modeNum], gamesDict[gameStr][2], mode, modeTitle
#----------------------------------------------------------------------------------------------------------------------------------------------------#

def askForMode():
    '''Function that asks the user for which game mode the user is playing.'''

    modes = ["pve", "pvp"]
    modeStr = input("\n\tAre you playing 'PvE' or 'PvP'? ").lower()

    while modeStr not in modes:
        os.system("cls")
        print(header)
        modeStr = input("\n\tSorry that option isn't available...\n\n\tAre you playing 'PvE' or 'PvP'? ").lower()

    if modeStr == "pve":
        gameModeTitle  = " PvE / COOP"
    elif modeStr == "pvp":
        gameModeTitle = " PvP"

    return modeStr, gameModeTitle
#----------------------------------------------------------------------------------------------------------------------------------------------------#


def askForPlayerCount():
    '''Function that asks the user for how many players are playing.'''

    if mode == "pve":
        max = 5
    elif mode == "pvp":
        max = 10

    count = 0
    while count <= 0 or count > max or not str(count).isdigit():
        count = input("\n\tHow many players are you submitting for? (1 to %s) "%str(max))
        try:
            count = int(count)
        except ValueError:
            os.system("cls")
            print(header)
            print(gameHeader)
            print("\n\n\tDetected: " + filename)
            print("\n\t" + count + " is not a valid entry...")
            count = 0

    return count
#----------------------------------------------------------------------------------------------------------------------------------------------------#


def askYesNo(text):
    '''Function that asks the user for a yes no question and returns a boolean response.'''

    response = input(text).lower()
    while response != "y" and response != "n" and response != "yes" and response != "no":
        response = input("\n\t%s is not a valid answer..."%response + text).lower()

    if response == "y" or response == "yes":
        return True
    elif response == "n" or response == "no":
        return False
#----------------------------------------------------------------------------------------------------------------------------------------------------#


def askForWinLose(name):
    '''Function that asks the user if a player won or loast a match.'''

    response = input("\n\tDid %s win or lose the last PvP match? (w/l)"%name).lower()
    while response != "w" and response != "l" and response != "win" and response != "lose":
        response = input("\n\t%s is not a valid answer..."%response).lower()

    if response == "w" or response == "win":
        return "w"
    elif response == "l" or response == "lose":
        return "l"
#----------------------------------------------------------------------------------------------------------------------------------------------------#


def getPartyInfo():
    '''Function that returns a multiline string of current party members.'''

    partyStr = ""
    counter = 1
    partyStr += "\n\tParty size: %s\n\tParty members:\n"%len(playerPins)
    for pilot in playerPins:
        partyStr += "\n\t\t%s - %s %s"%(str(counter), pilot[1], pilot[0])
        counter += 1

    return partyStr
#----------------------------------------------------------------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                     Main Program.                                                                  #
#----------------------------------------------------------------------------------------------------------------------------------------------------#
config = loadSettings()
initialSetup()

# Great the user and ask for game parameters.
header = """\n\n\t################################################################
\t#      Welcome to SkyShadow's Auto Screenshot Submitter.       #
\t################################################################"""
os.system("cls")
print(header)

# Get the game to be played.
game, gameName, mode, modeTitle = askForGame()
gameHeader = "\n\tPlaying " + gameName

# Set the folder to monitor for new screenshots.
if game == "XvT2" or game == "XvT":
    screenshotFolder == config.get("folders", "screenshot_folder_xvt")
elif game == "XWA2" or game == "XWA":
    screenshotFolder = config.get("folders", "screenshot_folder_xwa")
elif game == "SC2" or game == "SC":
    screenshotFolder = config.get("folders", "screenshot_folder_sc")
elif game == "BF32" or game == "BF3":
    screenshotFolder = config.get("folders", "screenshot_folder_eabf1")
elif game == "EABFII" or game == "BF2":
    screenshotFolder = config.get("folders", "screenshot_folder_eabf2")
elif game == "SWS2" or game == "SWS":
    screenshotFolder = config.get("folders", "screenshot_folder_sws")

# Get the game mode to be played.
os.system("cls")
print(header)
print(gameHeader)

# Set the url for uploading screenshots based on game mode selected.
if mode == "pve":
    url = config.get("urls", "tc_submit_coop_url")
elif mode == "pvp":
    url = config.get("urls", "tc_submit_pvp_url")

header = """\n\n\t#####################################################
\t#       SkyShadow's Auto Screenshot Submitter.      #
\t#####################################################"""

gameHeader += modeTitle + "\n\t-----------------------------------------------------"

# Main program monitor loop.
playerPins = [[config.get("user_settings", "pin"), config.get("user_settings", "callsign")]]
players = 0
samePlayers = False
runOnce = False
monitorMsg = "\n\n\tMonitoring for screenshots"

while True:

    winnerSlot = 1
    loserSlot = 1

    # Intro message.
    os.system("cls")
    print(header)
    print(gameHeader)
    print(monitorMsg)

    # Monitor load bar.
    monitorMsg += "."
    if monitorMsg == "\n\n\tMonitoring for screenshots......":
        monitorMsg = "\n\n\tMonitoring for screenshots"

    # Search for screenshots.
    filenames = glob.glob(screenshotFolder + r"\*")

    # Auto-submit any found screenshots.
    if filenames != []:
        for filename in filenames:
            if ".png" in filename or ".jpg" in filename or ".jpeg" in filename or ".gif" in filename:
                os.system("cls")
                print(header)
                print(gameHeader)
                print("\n\n\tDetected: " + filename)

                # Log in to the administration page of the TC website.
                browser = mechanize.Browser()

                # Disable SSL verification.
                try:
                    _create_unverified_https_context = ssl._create_unverified_context
                except AttributeError:
                    # Legacy Python that doesn't verify HTTPS certificates by default
                    pass
                else:
                    # Handle target environment that doesn't support HTTPS verification
                    ssl._create_default_https_context = _create_unverified_https_context

                browser.open(config.get("urls", "tc_admin_url"))
                browser.form = list(browser.forms())[0]
                browser["pin"] = config.get("user_settings", "pin")
                browser["pass"] = config.get("user_settings", "password")
                browser.submit()

                # Open and complete the match submission form.
                browser.open(url)
                browser.form = list(browser.forms())[0] # Get the first from from the webpage.
                browser["game"] = [game]

                # Add player information to the form.
                bringAppToFront() # Bring this app to the front and ask the user for the game report details.

                if runOnce:
                    print(getPartyInfo())
                    samePlayers = askYesNo("\n\tUse the same party details as above? (y/n): ")

                if not samePlayers:
                    playerPins = [[config.get("user_settings", "pin"), config.get("user_settings", "callsign")]] # Clear out the old pin data.
                    players = 0

                if players == 0:
                    players = askForPlayerCount()

                winners = []
                losers = []

                for player in range(players):
                    if samePlayers:
                        pin = playerPins[player][0]
                        name = playerPins[player][1]

                    else:
                        if player != 0:
                            validPin = False
                            while not validPin:
                                pin = input("\n\tPlease enter player %s's TC PIN and press 'enter': "%str(player + 1))

                                try:
                                    browser["name1w"] = [pin]
                                    validPin = True
                                except Exception:
                                    print("\n\tERROR! %s is not a valid PIN in the TC Database!..."%pin)

                            name = input("\tPlease enter player %s's NAME and press 'enter': "%str(player + 1))
                            playerPins.append([pin, name])

                        else: # Use the script owners details from settings.ini
                            pin = playerPins[0][0]
                            name = playerPins[0][1]

                    if mode == "pvp":
                        result = askForWinLose(name)
                    else:
                        result = "w"

                    kills = input("\n\tPlease enter %s's number of kills: "%name)

                    if result == "w":
                        winners.append([pin, name, int(kills)])
                    elif result == "l":
                        losers.append([pin, name, int(kills)])

                # Sort and apply the results based on highest score.
                winners.sort(key=lambda x: (-x[2]))
                losers.sort(key=lambda x: (-x[2]))

                winnerSlot = 1
                for player in winners:
                    result = "w"
                    slot = winnerSlot
                    winnerSlot += 1
                    pin = player[0]
                    kills = player[2]
                    browser["name%s%s"%(slot, result)] = [pin]
                    browser["kill%s%s"%(slot, result)] = str(kills)

                loserSlot = 1
                for player in losers:
                    result = "l"
                    slot = loserSlot
                    loserSlot += 1
                    pin = player[0]
                    kills = player[2]
                    browser["name%s%s"%(slot, result)] = [pin]
                    browser["kill%s%s"%(slot, result)] = str(kills)

                # Add the screenshot data and submit the form.
                screenshot = open(filename, 'rb')
                browser.form.add_file(screenshot, 'image/png', filename, 'ss1')
                browser.submit()
                screenshot.close()
                shutil.move(filename, screenshotFolder + "\\Submitted\\" + filename.split("\\")[-1])

                os.system("cls")
                print(header)
                print(gameHeader)
                print("\n\n\tUpload Complete - " + filename)

                runOnce = True
                sleep(2)

    sleep(0.5)
#----------------------------------------------------------------------------------------------------------------------------------------------------#
