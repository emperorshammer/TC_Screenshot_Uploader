#!/usr/bin/python

import mechanize
import shutil
import sys
import os
import glob

filenames=glob.glob("*.jpg")
print filenames

br = mechanize.Browser()
br.open("http://tc.emperorshammer.org/admin.php")
br.form = list(br.forms())[0]
br["pin"] = "TC-PIN#"
br["pass"] = "PASWORT"
br.submit()

print "Schleife beginnt mit dem PVE upload"
for filename in filenames:
   print "Uploading " + filename
   br.open("http://tc.emperorshammer.org/submitcoop.php")
   br.form = list(br.forms())[0]
   br["game"] = ["SC2"]
   br["name1w"] = ["TC-PIN#"]
   br["kill1w"] = "1"
   br["name2w"] = ["TC-PIN#2"]
   br["kill2w"] = "1"
   f=open(filename, 'rb')
   br.form.add_file(f, 'image/jpeg', filename, 'ss1')
   br.submit()
   f.close()
   shutil.move(filename, "C:/gesendet/PVE/"+filename)