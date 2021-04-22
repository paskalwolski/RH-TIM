#LIAM v1
#Lesson Inventory And Management tool (LIAM) for RocketHour
#PROPERTY OF PASKAL - NO TOUCH


import os

class Liam:

    def __init__(self, cwd):
        self.liam_loc = cwd
        print("I now know where I am: {}".format(self.liam_loc))

        self.tracks = ("Pre-Beginner", "Beginner", "Intermediate", "Advanced")
        self.drive_path = self.find_drive()

        os.chdir(os.path.join(self.drive_path, "Shared Drives\\Product"))
        clear()
        print("Setup Complete")

    def main(self):
            
            self.main_action = self.select_dest_from_menu(("What do you want to do today?", ["Enter Lesson Details", "Explore Lesson Library"]))
            if main_action is "Enter Lesson Details":
                self.specific_lesson()
            elif main_action == 1:
                self.explore_tracks()

    def explore_tracks(self):

        try:
            # tracks = ("Pre-Beginner", "Beginner", "Intermediate", "Advanced")
            response = self.select_dest_from_menu(("Select a track by number", self.tracks))

            for i in range(len(self.tracks)):
                if response in self.tracks[i]:
                    os.chdir(self.tracks[i])

        except FileNotFoundError as e:
            print(e)
            print("An Error occured going through the Google Drive")

        return


    def select_dest_from_menu(self, menu_tuple):

        user_prompt, menu_list = menu_tuple

        clear()
        while True:
            print("Size of Menu: {}".format(len(menu_list)))
            for i in range(len(menu_list)):
                print("{}. {}".format(i, menu_list[i]))

            user_input =input(user_prompt + "\n\n")
            if user_input=='q':
                raise KeyboardInterrupt
            try:
                user_input = int(user_input)
            except TypeError as e:
                print("Please enter a valid option")
                continue

            # except user_input not in range(len(menu_tuple)):
            #     print("")

            if user_input not in range(len(menu_list)):
                # clear()
                print("Please enter a valid option")
                continue
            break
        return menu_list[user_input]


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
        try:
            os.chdir(os.path.join(self.drive_path, "Shared Drives\\Product"))
        except FileNotFoundError:
            print("Error Occured Switching to Product Folder")
        clear()
        print("Setup Complete")

        return


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
