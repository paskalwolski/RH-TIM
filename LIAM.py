#LIAM v1
#Lesson Inventory And Management tool (LIAM) for RocketHour
#PROPERTY OF PASKAL - NO TOUCH


import os

class Liam:

    def __init__(self, cwd):
        self.liam_loc = cwd
        print("I now know where I am: {}".format(self.liam_loc))

        self.tracks = ("Pre-Beginner", "Beginner", "Intermediate", "Advanced")
        self.track_ids = ('P', 'B', 'I', 'A')
        self.years = (1)
        self.checkpoints = (1, 2, 3, 4)
    
        self.drive_path = self.find_drive()

        clear()
        print("Setup Complete")


    def main(self):
            self.main_action = self.select_dest_from_menu(("What do you want to do today?", ["Enter Lesson Details", "Explore Lesson Library"]))
            if self.main_action == 0:
                self.specific_lesson()
            elif self.main_action == 1:
                self.explore_library()


    def specific_lesson(self):

        Years = (1)
        track_ids = ('P', 'B', 'I', 'A')

        lesson_code = input("Please Enter the lesson code you wish to work with:\n")


        return


    def explore_library(self):
        try:
            # tracks = ("Pre-Beginner", "Beginner", "Intermediate", "Advanced")
            response = self.select_dest_from_menu(("Select a track by number", self.tracks))
            os.chdir("{}. {}".format(response+1, self.tracks[response]))
            print("Opening {}".format(self.tracks[response]))

            print(os.listdir())

        except FileNotFoundError as e:
            print(e)
            print("An Error occured going through the Google Drive")
        input("Done with Library Exploration")
        return




    def select_dest_from_menu(self, menu_tuple):

        user_prompt, menu_list = menu_tuple

        clear()
        while True:
            # print("Size of Menu: {}".format(len(menu_list))) DEBUG LINE

            # Print index and item of menu
            for i in range(len(menu_list)):
                print("{}. {}".format(i, menu_list[i]))

            user_input =input(user_prompt + "\n\n")
            if user_input=='q':
                raise KeyboardInterrupt
            try:
                # Typecast to int to check for invalid Type input
                user_input = int(user_input)
            except TypeError as e:
                print("Please enter the number of the option you want to select")
                continue
            # Check for invalid int input
            if user_input not in range(len(menu_list)):
                # clear()
                print("Please enter a valid option")
                continue
            break
        return user_input


    def find_drive(self):
        print("Searching for Drive")
        vol_path = 'G:/'

        while True: #outer

            try:
                os.chdir(vol_path)
            except FileNotFoundError as e:
                clear()
                print("No Google Drive found at {}\n".format(vol_path))
                while True: #inner
                    print("\nType \'q\' to exit")
                    vol_path = input("Enter the volume label of your Drive:\n")
                    if not len(vol_path) == 1:
                        print("Please enter a valid, single character volume label")
                        continue    #continue inner
                    if vol_path == 'q':
                        raise KeyboardInterrupt #Only exit point for this function...
                    vol_path = "{}:/".format(vol_path)
                    break   #break inner
                continue    #continue outer
            break   #break outer
        print("Found Drive at {}".format(vol_path))

        # self.drive_path = vol_path  

        try:
            os.chdir(os.path.join(vol_path, "Shared Drives\\Product"))
        except FileNotFoundError:
            print("Error Occured Switching to Product Folder")
        clear()
        print("Setup Complete")

        return vol_path


class Track:

    def __init__(self, track_id, track_name):
        self.track_id = track_id
        self.track_name= track_name

        self.years = self.get_years()
        for year in self.years:
            pass

    def __repr__(self):
        return "Track({}, {})".format(self.track_id, self.track_name)

    def __str__(self):
        return self.track_name



#Util Methods

def clear():
    os.system("cls")

def on_exit():
    print("Exiting...")

    print("Goodbye!")
    exit()


if __name__ == '__main__':
    try:
        os.system("cls")
        print("Welcome to LIAM!")
        liam = Liam(os.getcwd())
        liam.main()
        input("Enter to exit")

        raise KeyboardInterrupt

    except KeyboardInterrupt:
        on_exit()
