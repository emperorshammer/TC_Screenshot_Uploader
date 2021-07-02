#!/usr/bin/python

import mechanize
import shutil
import sys
import os
import glob

filenames=glob.glob("*.png")
print filenames

br = mechanize.Browser()
br.open("http://tc.emperorshammer.org/admin.php")
br.form = list(br.forms())[0]
br["pin"] = "TC-PIN#"
br["pass"] = "passwort"
br.submit()

print "Schleife beginnt mit dem PVE upload"
for filename in filenames:
   print "Uploading " + filename
   br.open("http://tc.emperorshammer.org/submitcoop.php")
   br.form = list(br.forms())[0]
   br["game"] = ["EABFII"]
   br["name1w"] = ["TC-PIN#"]
   br["kill1w"] = "1"
   f=open(filename, 'rb')
   br.form.add_file(f, 'image/jpeg', filename, 'ss1')
   br.submit()
   f.close()
   shutil.move(filename, "C:/Users/Jeff/OneDrive/One Drive Docs/Tie Corps/Completed missions/Alone/BF2 PvE/BF2 PvE Submitted/"+filename)
