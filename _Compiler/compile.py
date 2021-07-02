'''#-------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        compile.py
# Purpose:     Used to compile X.py into X.exe.
# Version:     v1.00
# Author:      Stuart. Macintosh
#
# Created:     17/01/2021
# Copyright:   None
# Licence:     None
#-------------------------------------------------------------------------------------------------------------------------------------------------#'''

#----------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                      Imports.                                                                      #
#----------------------------------------------------------------------------------------------------------------------------------------------------#
import PyInstaller.__main__
import os
import shutil
import platform
import sys
#----------------------------------------------------------------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                     Main Program.                                                                  #
#----------------------------------------------------------------------------------------------------------------------------------------------------#
# Detect the location of the TCSU folder.
os.chdir("..")
directory = os.path.abspath(os.curdir)

# Remove any old builds of TCSU.
print("\nRemoving old build files...")
shutil.rmtree(directory + "\\_Compiler\\TCSU", ignore_errors=True)

# Compile TCSU.
print("\nCompiling TC Screenshot Uploader.exe...\n")
PyInstaller.__main__.run([
     "--onefile",
     os.path.join(directory, "TC Screenshot Uploader.py"),
])
print("\nTC Screenshot Uploader.exe created.")

# Clean up the build, copy in 'Settings' and 'Data' folders. Remove unnecessary files and renaming 'dist' to 'TCSU'.
shutil.rmtree(directory + "\\_Compiler\\build", ignore_errors=True)
os.remove(directory + "\\_Compiler\\TC Screenshot Uploader.spec")
os.rename(directory + "\\_Compiler\\dist", directory + "\\_Compiler\\TCSU")
shutil.copy(directory + "\\settings.ini", directory + "\\_Compiler\\TCSU\\")
bits = sys.version[ : sys.version.index(" bit")][-3:]
version = platform.platform().split("-")[0] + bits + "-bit"
print("\n\n----------- Compile for %s Complete -----------\n\n" % version)
#----------------------------------------------------------------------------------------------------------------------------------------------------#
