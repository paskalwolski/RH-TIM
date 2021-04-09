# Imports
import csv
import fnmatch
import os
import urllib.request


#ROCKET LAUNCH
# FOR V4
# Defaults for hint/example images to be different
# MAYBE take challenge # and insert into the filenames
# Center align hint images/all images
# Sanitize subtitle for filename



#CHANGELOG 1/29/2021
# Automatically updates image, video, download links to the bucket
# Grabs csv filename and uses this for amazon link
# Pulls HTML Template from bucket
# 




# Check current directory for csv file, and set that as toOpen
# Only 1 csv file should be present. Otherwise script gets confused.
toOpen = None

# Lesson information - See 'Lesson Information' block below
lessonname = None
try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for file in os.listdir(dir_path):
        if fnmatch.fnmatch(file, '*.csv'):  #Python RegEx
            toOpen = os.path.join(dir_path, file)
            lessonname = str(file)[:-4]
            break
    print("Creating Lesson " + lessonname)
except:
    print("Could not find CSV file")
    input()
    exit()
challenge_list = []

# Block to fill in lesson information
track_id = lessonname[:2].lower()
lesson_id = lessonname[3:].lower()
bucket = "https://rockethour.s3.af-south-1.amazonaws.com/product_development/{TRACK}/{LESSON}".format(TRACK=track_id, LESSON=lesson_id)


# Variables used for error checking 
csvCorrect = True
errorlist = []
rownum = 2

# Current open function
print("Reading CSV File...", end="\t\t")
actions = []
try:
    with open(toOpen, mode='r') as csv_file:
        delimChar = next(csv_file).split('=')[1][0]
        next(csv_file)  # Skip csv header row. Might be able to do this with lib?
        # Delimiter and quotechar set here - will need to be changed as necessary for output file.
        data_list = csv.reader(csv_file, delimiter=delimChar, quotechar='"')

        challenge = {"title": "",
                    "subtitle": "",
                    "instruction": "", # Instruction text or image link
                    "instruction_show": "hidden",
                    "hint": "",
                    "hint_show": "hidden",
                    "example": "",
                    "example_show": "hidden"}

        currentChal = 0     # Running counter of the current challenge being processed.

        for row in data_list:
            rownum +=1
            try:
                #TODO: If no challenge ID present, use the last one !Working
                # if not row[0]=='':
                    if(row[0]==''): row[0]=currentChal
                    if int(row[0]) == currentChal+1:
                        challenge_list.insert(currentChal, challenge)
                        challenge = {"title": "",
                                    "subtitle": "",
                                    "instruction": "", 
                                    "instruction_show": "hidden",
                                    "hint": "",
                                    "hint_show": "hidden",
                                    "example": "",
                                    "example_show": "hidden"}
                        currentChal = int(row[0])

                    #     else:
                    type = row[1]
                    value = row[2]
                    extra = row[3].split(",")


                    # Data structure for storing very low level html for formatting
                    # Included AWS links for images, videos
                    html_lines = {"list": "\n\t\t\t\t<li>{TEXT}</li>",
                                "image": "\n\t\t\t\t<img width=\"{WIDTH}\" src=\"{LINK}\">",
                                "video": "\n\t\t\t\t<video controls=\"controls\" width=\"{WIDTH}\" height=\"{HEIGHT}\"><source src=\"{LINK}\"</video>",
                                "button": "\n\t\t<button class = \"rhbutton\" onclick=\" window.open('{LINK}', '_blank'); return false;\">{TEXT}</button>",
                                "project": "\n\t\t\t\t<iframe src=\"{LINK}embed\" allowtransparency=\"true\" width=\"{WIDTH}\" height=\"{HEIGHT}\" frameborder=\"0\" scrolling=\"no\" allowfullscreen></iframe>",
                                "egtitle": "<h2 class = \"rhcenter\">{TEXT}</h2>"
                                }


                    currentContainer = ""
                    if "instruction" in type:
                        challenge["instruction_show"] = ""
                        currentContainer = "instruction"
                        # challenge["instruction"].append(item)
                    elif "hint" in type:
                        challenge["hint_show"] = ""
                        currentContainer = "hint"
                        # challenge["hint"].append(item)
                    elif "example" in type:
                        challenge["example_show"] = ""
                        currentContainer = "example"
                        # challenge["example"].append(item)
                    else:
                        currentContainer = type
                        # challenge[type] = value

                    # Default values for embeds, to be replaced with values fetched from csv
                    IMG_WIDTH = 400
                    VID_WIDTH = 850
                    VID_HEIGHT = 478
                    EMBED_WIDTH = 485
                    EMBED_HEIGHT = 402

                    html = ""
                    # try f strings for formatting. 10/2/2021
                    if "image" in type:
                        actions.append("Updated image link on line " + str(rownum))
                        if extra[0] == "":
                            html = html_lines["image"].format(LINK=bucket+"/"+value, WIDTH=IMG_WIDTH)
                        else:
                            html = html_lines["image"].format(LINK=bucket+"/"+value, WIDTH=extra[0])
                    elif "video" in type:       # Updated bucket link for videos. 17/02/2021
                        actions.append("Updated video link on line " + str(rownum))
                        if extra[0] == "":
                            html = html_lines["video"].format(LINK=bucket+"/"+value, WIDTH=VID_WIDTH, HEIGHT=VID_HEIGHT)
                        else:
                            html = html_lines["video"].format(LINK=bucket+"/"+value, WIDTH=extra[0], HEIGHT=extra[1])
                    elif "project" in type:
                        if not value[-1]=='/':
                            value = value + '/'
                        if extra[0] == "":
                            html = html_lines["project"].format(LINK=value, WIDTH=EMBED_WIDTH, HEIGHT=EMBED_HEIGHT)
                        else:
                            html = html_lines["project"].format(LINK=value, WIDTH=extra[0], HEIGHT=extra[1])
                    elif "button" in type:
                        if ".zip" in extra[0]:
                            newlink = bucket + "/" + extra[0]
                            html = html_lines["button"].format(LINK=newlink, TEXT=value)
                            actions.append("Updated download link in line "+ str(rownum))
                        else:
                            html = html_lines["button"].format(LINK=extra[0], TEXT=value)

                    elif "list" in type:
                        html = html_lines["list"].format(TEXT=value)
                    elif "example_title" in type:
                        html = html_lines["egtitle"].format(TEXT=value)
                    else:
                        html = value

                    challenge[currentContainer] += html
            except:
                print("Error found")
                errorlist.append(rownum)
                csvCorrect = False
                continue
        challenge_list.insert(currentChal, challenge)
        csv_file.close()
    print("OK")
    for act in actions:
        print(act)
except:
    print("ERROR")
if not csvCorrect:
    print("Errors found in CSV file\nOperations unable to complete")
    if len(errorlist)>20:
        print("Check your CSV delimiter (comma or semicolon)")
    else:
        print("Errorlist:")
        for er in errorlist:
            print("  Line " + str(er))
    input("Press enter to continue")
    exit()

# Block to fetch html template 
print("Fetching Template file...")
try:
    template_url = "https://rockethour.s3.af-south-1.amazonaws.com/Javascript%26CSS/HTMLTemplate.html"
    template_path = os.path.join(dir_path, ".RHTemplate.html")
    try:
        # print("Fetching Template File", end='')
        for i in range(3):
            try:
                print("\t\tAttempt "+str(i+1), end="\t")
                urllib.request.urlretrieve(template_url, template_path)
                print("OK")
                break
            except:
                print("Failed")
    except:
        print("Error fetching Template. Please check your network connection")
    file = open(template_path, mode='r')
    template = file.read()
    file.close()
    os.remove(template_path)
except:
    print("Error reading or writing Template")
    input("Press enter to exit")    #lol
    exit()


print("Writing to output files...", end="\t")
try:
    for i in range(len(challenge_list)):
        f = open(os.path.join(dir_path, str(i)+'. '+challenge_list[i]["subtitle"]+".html"), mode='w') #TODO: Change this for consistency between 'challenge 1' in the excel doc and '1. html' in the output
        challenge_template = template.format(**challenge_list[i])
        f.write(challenge_template)
        f.close()
    print("OK")
except:
    print("ERROR")
    print("Encountered an error creating challenge "+ str(i))
    input("Press enter to exit")
    exit()

input("Completed Lesson Creation, Press 'Enter'")
