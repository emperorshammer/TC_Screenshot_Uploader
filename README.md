# TC Screenshot Uploader
A program used to automatically upload game screenshots to the EHTC database.

TC Screenshot Uploader now supports all TIE Corps official games and also supports both PvE / COOP and PvP modes playing solo or with a group.

The program will retain the PIN numbers and names your party members if you are gaming as a group for ease of use and will prompt you before each submission if there are
any changes to your group’s makeup.
Because of this it may be useful to write down the PIN numbers and names of the people you are playing with so allow you to easily reconfigure your group in the app
should it change.

# Disclaimer:
The user of this software is responsible for ensuring that all submissions comply with current platform and COO policies. Failure to do so WILL result in your submission being rejected.

# Antivirus Notice:
The .exe version of this software WILL trigger a false positive antivirus alert. This is because the software moves screenshots to a "Submitted" folder after it submits the report.
Antivirus software rightly identifies this as an act of Malware because of this. 
To use the .exe version you will most likely need to make an exception for this program within your antivirus software.
This issue does not affect the .py version.

# Instructions for use:
Bear in mind this program is very early in its development and completely experimental at this point.

For the .exe version of the software:

Download both "TC Screenshot Uploader.exe" and "settings.ini" from:
https://github.com/emperorshammer/TC_Screenshot_Uploader/tree/main/Latest%20Build

for the .py version of the software:

Note: Python 3 is required to use this script. Python 2 is not supported at this time.
Download both "TC Screenshot Uploader.py" and "settings.ini" from:
https://github.com/emperorshammer/TC_Screenshot_Uploader

 
Edit settings.ini with your TC username, password, callsign and add the directories where your screenshots are saved to for each game, if you don't own a specific game, then you may leave it blank. 
This program is designed to be run while playing a game. Simply run the .exe or .py if you have Python 3 installed and follow the on-screen instructions to set the program up for your game / format of choice.
Once your match is complete take your screenshot of the scoreboard as normal. TC Screenshot Uploaded will automatically detect your new screenshot and prompt you for the match player pins and their kills. 
Once all entries are complete this program will then submit your screenshot to the TC database for approval.
