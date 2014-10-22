EECS 149/249A Project Charter, Fall, 2014
====================================
Project Title: SHaZam the Magic Lamp

Team: Chaim Halbert, Dexter Scobee, Edward Zhao

Project Repo: https://github.com/EECS149-SHaZam/shazam

## Project Goal
The goal of this project is to design a lamp that will redirect its light to follow a user’s gaze.

## Project Approach
The magic lamp will consist of a standard adjustable desk lamp with a microcontroller embedded in its base and servo motors connected to its light source. Additionally, the lamp will utilize a WiiMote to track IR LEDs affixed to the user’s face or hat. The WiiMote will communicate relative positioning data to the microcontroller via Bluetooth, which will in turn direct the motors to aim the light source. The controller will behave according to a state-machine that models states such as user-gaze-in-motion or user-gaze-fixed. Potential growth paths for this project include changing the tracking algorithm to be facial-recognition-based and adding additional degrees of freedom to the lamp’s motion.


## Resources
* Raspberry Pi ($40) + Alamode shield ($35) – OR – mbed ($13) + Bluetooth Module (~$10)
* 5V power supplies (2x $10)
* WiiMote (Free)
* Bluetooth USB dongle (Free)
* IR LED bar ($5)
* 2-axis gimbal for light ($46 – $65)
* LED flashlight (~$10)
* Mounting Hardware (~$10)
* Desk lamp stand (~$10 / Free)
* Cabling (~Free)
Total cost: ~$124 – $195


## Schedule
10/21: Turn in project charter and create repo
10/28: Choice of platform finalized after discussion with GSIs
10/31: Order necessary parts / get from TAs
11/11: Familiarize ourselves with parts and create relevant state models. **Dev access to Pi** (Ethernet)
11/14: Hello world sensor comm (BT) and servo control (PWM via Arduino)
11/18: Mini project update - demonstrate **sensor comm** / **servo**
11/21: Begin assembling parts and write code for models. **Interface Pi with Alamode** (Serial)
12/2: **Head-tracking** code on Raspberry pi (Python?)
12/12: **Final integration**; complete project
12/16: Complete demo video, ppt, and prep for presentation
12/17: **Final Presentation**
12/18: Final Project report adjustments (if necessary)
12/19: Turn in **Final Project report**


## Risk and Feasibility
There are several risk factors involved, mainly because of the different parts we plan to interface with each other. First, we have to interface the Pi with the Alamode Shield. At the same time, we have to get the Pi to interface with the Wiimote via Bluetooth. After that’s complete, we have to make sure that the Alamode shield can understand serial commands. Of course, we also have to use the Alamode shield to control the Gimbal itself. These processes are nontrivial and we anticipate a significant amount of the time will be spent on calibration and debugging.