from ftplib import FTP
import ftplib
import os
import datetime
import sys
import json

json_settings = json.load(open("settings.json"))

folder = json_settings["folder_to_backup"]
outputFolder = json_settings["output_folder"]

def isDirectory(x):
  counter = 0
  currentFile = None
  def wrap(y):
    nonlocal counter
    nonlocal currentFile
    counter = counter + 1
    currentFile = y
  if("." in x):
    return False
  ftp.dir(x,wrap);
  if currentFile == None and counter == 0:
    return True
  if counter > 1:
    return True
  if currentFile[-len(x):] == x:
    return False
  return True

def recursiveDownload(folder,base_folder):
  ftp.cwd(folder)
  working_dir = os.path.join(base_folder,folder)
  if not os.path.isdir(os.path.join(backup_folder,working_dir)):
    os.mkdir(os.path.join(backup_folder,working_dir))
  for file in ftp.nlst():
    print(file)
    if(isDirectory(file)):
      recursiveDownload(file,working_dir)
    else:
      for i in range(100):
        try:
          save_path = os.path.join(backup_folder,working_dir,file)
          ftp.retrbinary("RETR " + file ,open(os.path.join(backup_folder,working_dir,file), 'wb').write )
        except ftplib.all_errors as e:
          print(e);
        else:
          break
  ftp.cwd("..")

if len(sys.argv) > 1 and sys.argv[1] == "auto":
	number_suffix = len([f for f in os.listdir(outputFolder) if "auto backup" in f])
	folder_name = str(datetime.date.today()) + " auto backup " + str(number_suffix)
	backup_folder = os.path.join(outputFolder,folder_name)
else:
  backup_name = input("Backup name:") 
  folder_name = (str(datetime.date.today()) + " " +  backup_name)
  backup_folder = os.path.join(outputFolder,folder_name)
os.mkdir(backup_folder)
ftp = FTP(json_settings["ftp_server"],json_settings["ftp_username"],json_settings["ftp_password"],timeout=100);
ftp.set_pasv(False)
ftp.cwd(folder)

recursiveDownload("","")
print("done");