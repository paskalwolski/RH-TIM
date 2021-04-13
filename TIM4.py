#Experimental TIM version under development for RocketHour
#Property of Paskal (not really) - DO NOT TOUCH

""" CHANGELOG
6/4/2021: Started work on this version with the intention to experiment with some whacky ideas including
    - More robust Python functions like RegEx, JSON for storage
    - Inclusion of REST API's like Docs for easier access
    - Better file handling - hopefully all through the terminal
"""

#Imports
import os
#import  HAP   #Coming Soon


# class Main():
    # Is this necessary? Might not need to have 'main' class
    # def __init__(self):
    #     #Class Variable Declaration for each instance of the program (Should  only be  1)
    #     self.track = None
    #     self.lesson_name = None
    #     self.lesson_number = None
    #     self.cwd = None
    #     self.menu_options = None

    #     #Class Variable Definition
    #     self.loc = os.getcwd()
    #     return None
    
    #clear command line


track = None

#Main Thread
#######################################

def main():
    clear()
    print("Welcome to TIM4!")
    menu = (("Access Google Drive", find_google_drive), ("Something Else I guess", on_close)) #Rethink this
    menu_action(menu, main)
    
    
    # k = input()
    # if k=='1':
    #     print("Starting Card Creation")
    #     find_google_drive('G:') #Default drive mount point for windows
    # elif k=='2':
    #     print("Doing something else...")
    # else:
    #     clear()
    #     unexpected_action()
    #     main()

    # return None


# Grab input to perform menu_action based on the menu_actions dict
def menu_action(menu, catch):
    #Catch: Object to run on catch. Usually the method from which it is called. 
    for i in range(len(menu)):
        print("{}. {}".format(i+1, menu[i][0]))
        
    print("\n------------------------------\n")
    action = input()
    try:
        clear()
        menu[int(action)-1]()
    except IndexError:
        unexpected_action()
        catch()
    except Exception as e:
        print(e)
        unexpected_action()
        catch()


# Search for Google Drive at G:
# If not found, search for drive name ('Google Drive')
def find_google_drive(volume):
    try:
        os.chdir(volume)
        print("Found Google Drive")
        input()
        return None

    except FileNotFoundError:
        clear()
        print("Google Drive is not mounted at G:")
        print("Running Backup Search")
        check_mount_point()

    return None


# Get User  input to find Google Drive Volume
def check_mount_point():
    mount_point = input("Please enter the Volume Label that Google Drive is mounted at:\n")
    try:
        os.chdir(mount_point +  ':')
        clear()
        print("Found Google Drive")
    except FileNotFoundError:
        clear()
        print("\'" + mount_point + ":\' does not exist")
        menu  =  {
            'text' : "1. Try a new Volume\n2. Exit",
            "menu_options" : {
                '1': check_mount_point,
                '2': on_close
            }
        }
        menu_action(menu,check_mount_point)
        # menu_action = input("1. Try a New Volume\n2. Exit")
        # if menu_action == '1':
        #     self.check_mount_point()
        #     return None
        # elif menu_action == '2':
        #     self.on_close()
        #     return  None
        # else:
        #     self.unexpected_action()
        #     self.check_mount_point()

            
#Utility Functions for use from main method
#######################################

def clear():
    os.system('cls')
    return None


def on_close():
    print("\n\nClosing Session\n\n")
    quit()


def unexpected_action():
    clear()
    print("Your response was not expected\n___________________")


#######################################


#Lesson Class - Instantiate with Current Working Lesson
#######################################
class Lesson:
    def __init__(self,  track, checkpoint,  lesson_name):

        return None



# Running the Code
if __name__=="__main__":
    main()