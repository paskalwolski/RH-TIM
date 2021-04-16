# Imports
import csv
import fnmatch
import os
import urllib.request
import time

#ROCKET LAUNCH
#TODO: Sanitize subtitle name for special characters


#Program Details Required

#while true loop uses this to keep the mai() method running
running = True

# Check current directory for csv file, and set that as toOpen
# Only 1 csv file should be present. Otherwise script gets confused.
toOpen = None

#cwd - location the script is running from
dir_path = None

# Lesson information - See 'Lesson Information' block below
lesson_id = None

#Required folders per lesson
req_folders = ("assets", "HTML",  "res", "src", "Student Files")


def main():

    print("What do you want to do today?\n\n")

    k = input("1. Create HTML Cards\n2. Create Lesson Structure here\nq. Quit\n\n")
    if k=='1':
        clear()
        print("Creating HTML Cards")
        check_csv()
        
    elif k=='2':
        clear()
        print("Creating Lesson Structure\n")
        check_lesson()
        print("\n\nReady to Work!")
        input("\'Enter\' to Continue")
        clear()
        return

    elif k=='q':
        clear()
        on_quit()
        return
    else:
        clear()
        print("I wasn't expecting that...\n\n")

        return


def check_lesson():
    for folder in req_folders:
        print("Checking for {}...".format(folder).ljust(50), end='')
        if folder in os.listdir(dir_path):
            print("Found")
        else:
            print("Not Found")
            make_dir(folder)

    return None


def check_csv():
    print("Checking for CSV in src folder...")
    try:
        os.chdir('src')
    except FileNotFoundError:
        k = input("\'src\' folder not found. Do you want to create the lesson structure? y/n\n")
        clear()
        while k not in ('y', 'yes', 'n', 'no'):
            clear()
            print("I wasn't expecting that...")
            k = input("\'src\' folder not found. Do you want to create the lesson structure? y/n\n") #Slightly janky, but I think it works? 


        if k == ('y' or 'yes'):
            print("Creating Lesson Structure...")
            check_lesson()
        elif k == ('n' or 'no'):
            print("You will have to make sure the lesson structure is in place!")
            return

    find_csv("src")
            
        
    
        

def find_csv(path):
    for file in os.listdir(path):
            if fnmatch.fnmatch(file, '*.csv'): 
                set_csv(os.path.join(path, file))
    return False


def set_csv(csv_file):
    print("Setting csv file to {}".format(csv_file))
    toOpen = os.path.join(dir_path, csv_file)
    try:
        #TODO: TEST THIS BLOCK
        lesson_id = str(csv_file).split('-')[0].strip()    #Now you don't need to change the filename
    except:
        lesson_id = str(csv_file)[:-4]  #Drop'.csv' extension to get lessonID
    print("Working with Lesson " + lesson_id)

    return False


def make_dir(folder_name):
    print("\tCreating folder {}...".format(folder_name).ljust(20), end='')
    try:
        os.mkdir(folder_name)
        print("Done")
    except Exception as e:
        log(e)


def find_cwd():
    try:
        clear()
        print("Where am I...")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print("Here!\n")
    except Exception as e:
        log(e)

def create_html():
    challenge_list = []

    # Block to fill in lesson information
    track_id = lesson_id[:2].lower()
    lesson_num = lesson_id[3:].lower()
    bucket = "https://rockethour.s3.af-south-1.amazonaws.com/product_development/{TRACK}/{LESSON}".format(TRACK=track_id, LESSON=lesson_num)


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



## UTILITY METHODS

def clear():
    os.system('cls')
    return None

#LOG WRAPPER - TO BE MADE
def log(e):
    print("Something went wrong...")
    print(e)
    input()
    on_quit()
    pass

def on_quit():
    print("Goodbye")
    running = False
    quit()


if __name__ == '__main__':
    clear()
    find_cwd()
    print("Welcome to TIM v3.4!")
    try:
        while running:
            main()
    except KeyboardInterrupt:
        on_quit()
