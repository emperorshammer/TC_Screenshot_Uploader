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
br["pass"] = "PASSWORT"
br.submit()


for filename in filenames:
   print "Uploading " + filename
   br.open("http://tc.emperorshammer.org/submitmp.php")
   br.form = list(br.forms())[0]
   br["game"] = ["SC"]
   br["name1w"] = ["TC-PIN#"]
   br["kill1w"] = "1"
   br["name1l"] = ["99"]
   br["kill1l"] = "0"
   br["name2w"] = ["TC-PIN#2"]
   br["kill2w"] = "1"
   br["name2l"] = ["99"]
   br["kill2l"] = "0"
   br["name3w"] = ["TC-PIN#3"]
   br["kill3w"] = "1"
   br["name3l"] = ["99"]
   br["kill3l"] = "0"
   br["name4w"] = ["TC-PIN#4"]
   br["kill4w"] = "1"
   br["name4l"] = ["99"]
   br["kill4l"] = "0"
   f=open(filename, 'rb')
   br.form.add_file(f, 'image/jpeg', filename, 'ss1')
   br.submit()
   f.close()
   shutil.move(filename, "C:/gesendet/PVP/"+filename)