import json

json_settings = json.load(open("settings.json"))

f = open("run.bat","w")
g = open("manual.bat","w")

f.write("\"%s\" \"%s\" auto\npause" % (json_settings["python3_interpreter"], json_settings["app_location"]))
g.write("\"%s\" \"%s\"\npause" % (json_settings["python3_interpreter"], json_settings["app_location"]))

f.close()
g.close()