#LIAM v1
#Lesson Inventory And Management tool (LIAM) for RocketHour
#PROPERTY OF PASKAL - NO TOUCH


import os

class Liam:

    def __init__(self, cwd):
        self.liam_loc = cwd
        print("I now know where I am: {}".format(self.liam_loc))
        return

    def main(self):
        try:
            drive_path =self.find_drive()
            try:
                os.chdir(os.path.join(drive_path, "Shared Drives\\Product"))
                clear()
                print("Setup Complete")
                tracks = ("Pre-Beginner", "Beginner", "Intermediate", "Advanced")
                prompt = "Select a track by number"
                self.get_user_input_for_menu(tracks, prompt)
                # os.chdir(os.path.join(self.get_user_input_for_menu(tracks, prompt)



            except FileNotFoundError:
                print("An Error occured going through the Google Drive")
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            print("Exiting...")
            return None
        return


    def get_user_input_for_menu(self, menu_tuple, user_prompt):
        while True:
            print(len(menu_tuple))
            for i in range(len(menu_tuple)):
                print("{}. {}".format(i, menu_tuple[i]))
            user_input = input(user_prompt, end = "\n\n")
            if user_input=='q':
                raise KeyboardInterrupt
            if user_input not in range(len(menu_tuple)):
                clear()
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
        return vol_path


    def clear(self):
        os.system("cls")
    


def clear():
    os.system("cls")

def on_exit():
    print("Goodbye!")

    exit()


if __name__ == '__main__':
    os.system("cls")
    print("Welcome to LIAM!")
    liam = Liam(os.getcwd())
    liam.main()
    input("Enter to exit")
    on_exit()