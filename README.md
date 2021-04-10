# RH-TIM
The Incredible lessonMaker

TIM (The Incredible lessonMaker) is a utility developed for RocketHour (a division of ThinkCamp) to quickly apply a csv file - created from an excel sheet - to an HTML template ("HTMLTemplate.html") for upload to our Learning Management System. 

No installation required! Simply run the script

Currently, version 3.3 is in use. Version 4 is in development, but is more of a complete overhaul of the system to allow for increased functionality (such as including HAPpy, an additional auxilary script). 

The goal for TIM is to provide a decentralised program that will allow all RocketHour lesson developers to easily view, edit, and manage ALL RocketHour lessons. The best methods to do this are yet to be discovered. 
In the future, TIM will migrate to be a centralised program. However, that is not the current scope
Currently, we utilise a combination of a Shared Google Drive to store all documentation,  AWS S3 Bucket (pls no steal) and our LMS to store the Complete HTML files in their final format (css for the HTML is found on the Bucket). TIM is a tool to access the Drive (and its per-lesson folder structure) in order to download lesson files and generate per-challenge or per-lesson (current HAPpy Functionality) HTML files from a central Python App

Drive for Desktop is used at ThinkCamp. This allows a Google Drive to be mapped as a local drive (mounted at G: by default), and prior to API implementation, this is the drive that will be used to manouever files. 

#
FILE CONVENTIONS #
------------------
Within the 'Product' Drive Folder, file structure is as follows:

TRACK/"Checkpoint #"/THREE_WORD_IDENTIFIER

There are 4 tracks:
  Prebeginner     (P)
  Beginner        (B)
  Intermediate    (I)
  Advanced        (A)
Each track will contain between 2 and 6 Checkpoint Periods (4 in a year)
Each Checkpoint Period will be 10 lessons long
Each Lesson will be identified by its unique Three Word Identifier. The assignment of a lesson to a particular slot (eg. Shrinking Sam the Sheep -> Checkpoint 3, lesson 8 -> 3.8) will be handled elsewhere. TIM is only concerned with editing lessons, not the order in which they go.

Within each 'lesson' folder, there will be a series of subfolders as follows:

```-Shrinking Sam the Sheep/
  -assets/     #A folder that stores all images, animations, characters etc. used in the creation of the lesson
  -HTML/       #A folder that stores all generated cards
  -src/        #A folder that stores generated JSON objects for long term storage, as well as the .csv file that is currently in use
    -Shrinking Sam the Sheep.json
    -Shrinking Sam the Sheep.csv
  -Shrinking Sam the Sheep.gsheet   #The Google Sheet that handles card creation
  -old/        #(OPTIONAL) An archive for storing old versions of lessons. There will be a function to grab the current lesson, and pack and dump it here
 ```

 Additionally, for LiveCode Lessons (advanced track) the directory will be include the following:
 
``` -student/   #Folder for storing all files provided to the student
    -Shrinking Sam the Sheep.livecode   #Emtpy/Lesson project file
  -Shrinking Sam the Sheep COMPLETE.livecode #LiveCode Project File
```

#
API KEYS #
----------
TIM currently has no use for API keys, as all work has been done locally. However, Drive and S3 API's are on the Horizon. 
Current plan is to generate a .env file on 'install', and store API keys there. Login process has not been thought out, but will be at some point
