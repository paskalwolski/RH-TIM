# HTML Amalgamator Program (HAP) written in Python 
# Program to grab all correctly named HTML files in a directory and amalgamate them into a single file, preferrably in order. 
# Paskal Wolski for RocketHour
# 6/1/2021


import fnmatch
import os
import webbrowser
import urllib.request as dl
import time


# Pulls all html files starting with integers (1, 2, 3, etc) under the assumption that these are challenge cards
# eg. '1. Scratch goes on a quest.html' 
# All html files must be in the same dir as the py file as well.
toOpen = None
html_list = []

# Get current working directory (cwd) of python script
dir_path = os.path.dirname(os.path.realpath(__file__))
css = False

# Iterate through challenge cards starting with int iterator i. 
i = 1
# listdir deprecated in python 3.9
print("Checking files for match")
for file in sorted(os.listdir(dir_path)):
    print("  " + file, end = '')
    if fnmatch.fnmatch(file, '*.*.html'):
        print("\t\t\t" + "MATCH")
        html_list.append(os.path.join(dir_path, file))
        i+=1
    else:
        print("")
    if fnmatch.fnmatch(file, '*.css'):
        css = True
    

if(len(html_list)==0):
    print("No challenge cards found.")
    exit()

# Ensure the HTML List is sorted
html_list.sort



# Set OutputFile as AllChallenges.html in cwd
outputFile = open(os.path.join(dir_path, "AllChallenges.html"), mode='w')

header = "<!DOCTYPE html>\n<link href='http://fonts.googleapis.com/css?family=Roboto' rel='stylesheet' type='text/css'>\n<link rel=\"stylesheet\" type=\"text/css\" href=\"https://rockethour.s3.af-south-1.amazonaws.com/Javascript%26CSS/rockethourcss.css\">"
outputFile.write(header)

# Read each file in html_list and put each line in OutputFile
print("\n\nCombining Files", end='')
for chal in html_list:
    print(".", end='')
    with open(chal) as challenge:
        for line in challenge:
            if "display: none" in line:
                line = "<ul id = \"rhhintsinner\">"
            if "onclick=\"hintsToggle()\"" in line:
                line = ""
            outputFile.write(line)
    challenge.close()

# Close output for memory's sake
outputFile.close()
print("Done")

# Opens the AllChallenges file in your browser automatically
webbrowser.open(os.path.join(dir_path, 'AllChallenges.html'), new=2)
time.sleep(5)
input("\nPress Enter to finish and clean up")

#Deletes the AllChallenges.html file, and the HAP.py file, just to clean up after itself 
os.remove(os.path.join(dir_path, "AllChallenges.html"))
os.remove(os.path.join(dir_path, "HAP.py"))

