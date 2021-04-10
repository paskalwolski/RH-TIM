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
#import  HAP

class Main:
    def __init__(self):
        #Class Variable Declaration for each instance of the program (Should  only be  1)
        self.track = None
        self.lesson_name = None
        self.lesson_number = None
        self.cwd = None
        self.menu_options = None

        #Class Variable Definition
        self.loc = os.getcwd()
        return None
    
    #clear command line
    def clear(self):
        os.system('cls')
        return None

    #Main Thread
    #Also used to restart program on dead end
    def main(self):
        self.clear()
        print("Welcome to TIM4!")
        print("1. Create Lesson Cards\n2. Something else I guess")
        print("\n--------------------------\n")

        #Should use:
        # menu_action(input())
        k = input()
        if k=='1':
            print("Starting Card Creation")
            self.find_google_drive()
        elif k=='2':
            print("Doing something else...")
        else:
            self.clear()
            print("Your response was not one of the expected responses")
            input("Enter to continue")
            self.main()

        return None

    # Grab input to perform menu_action based on the menu_actions dict`
    def menu_action(self, menu, catch):
        print(menu["text"])
        action  = input("Enter the Option Number")
        if action in menu["menu_options"]:
            self.clear()
            print(action)
            menu["menu_options"[action]]() #TODO: Fix  this  line
            return None
        else:
            self.unexpected_action()
            catch()

        return None

    # Search for Google Drive at D:
    # If not found, search for drive name ('Google Drive')
    def find_google_drive(self):
        try:
            os.chdir('K:')
            print("Found Google Drive")
            input()
            return None

        except FileNotFoundError:
            self.clear()
            print("Google Drive is not mounted at G:")
            print("Running Backup Search")
            self.check_mount_point()

        return None
    # Get User  input to find Google Drive Volume
    def check_mount_point(self):
        mount_point = input("Please enter the Volume Label that Google Drive is mounted at:\n")
        try:
            os.chdir(mount_point +  ':')
            self.clear()
            print("Found Google Drive")
        except FileNotFoundError:
            self.clear()
            print("\'" + mount_point + ":\' does not exist")
            menu  =  {
                'text' : "1. Try a new Volume\n2. Exit",
                "menu_options" : {
                    '1': self.check_mount_point,
                    '2': self.on_close
                }
            }
            self.menu_action(menu, self.check_mount_point)
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

                

    # Function declared for cleanup later
    def on_close(self):
        print("\n\nClosing Session\n\n")
        quit()

    def unexpected_action(self):
        self.clear()
        print("Your response was not expected\n___________________")


class Lesson:
    def __init__(self,  track, checkpoint,  lesson_name):

        return None



# Running the Code
if __name__=="__main__":
    main =  Main()
    main.main()
    main.on_close()