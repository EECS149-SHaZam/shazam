EECS 149/249A Project Charter, Fall, 2014
=========================================
Project Title: SHaZam the Magic Lamp

Team: Chaim Halbert, Dexter Scobee, Edward Zhao

Project Repo: https://github.com/EECS149-SHaZam/shazam

Revised version, post-GSI meeting

## Project Goal
The goal of this project is to design a lamp that will redirect its light to follow a user’s gaze.


## Project Approach
The magic lamp will consist of a standard adjustable desk lamp with a microcontroller embedded in its base and servo motors connected to its light source. Additionally, the lamp will utilize a WiiMote to track IR LEDs affixed to the user’s face or hat. The WiiMote will communicate relative positioning data to the microcontroller via Bluetooth, which will in turn direct the motors to aim the light source. The controller will behave according to a state-machine that models states such as user-gaze-in-motion or user-gaze-fixed. Potential growth paths for this project include changing the tracking algorithm to be facial-recognition-based and adding additional degrees of freedom to the lamp’s motion.


## Resources
* mbed (provided) + [Bluesmirf](https://www.sparkfun.com/products/10938)? Bluetooth Module (~$25)
* 5V power supplies (2x $10)
* WiiMote (provided)
* [IR LED bar](http://www.monoprice.com/Product?seq=1&format=2&p_id=5669&CAWELAID=1329451925&CAGPSPN=pla&catargetid=320013720000066114&cadevice=c&gclid=Cj0KEQjwiJiiBRDh3Z-ctPfS5MgBEiQAAlkbQimVkChWKF0BtfEzTS-pzF3BSvLTc6MKdP7llvVJQGIaArIo8P8HAQ) ($5)
* [2-axis gimbal](http://www.dx.com/p/boscam-pan-tilt-camera-mount-gimbal-for-hd19-fpv-camera-recorder-w-servo-black-255234#.VEb5eovF-d4) for light ($46)
* LED flashlight (~$10)
* Mounting Hardware (~$10)
* Desk lamp stand (provided)
* Cabling (provided)

Total cost: ~$116


## Schedule
* ~~10/21: Turn in project charter and create repo~~
* ~~10/28: Choice of platform finalized after discussion with GSIs~~
* ~~10/31: Order necessary parts / get from TAs~~
* 11/11: Familiarize ourselves with parts and create relevant state models. **Dev access to mbed** (USB-serial)
* 11/14: Hello world sensor comm (BT) and servo control (PWM)
* 11/18: Mini project update - demonstrate **sensor comm** / **servo**
* 11/21: Begin assembling parts and write code for models. **Interface mbed with Wiimote** (Serial)
* 12/2: **Head-tracking** code
* 12/12: **Final integration**; complete project
* 12/16: Complete demo video, ppt, and prep for presentation
* 12/17: **Final Presentation**
* 12/18: Final Project report adjustments (if necessary)
* 12/19: Turn in **Final Project report**


## Risk and Feasibility
There are several risk factors involved, mainly because of the different parts we plan to interface with each other. We must interface the mbed uC with the Bluesmirf module. Then, we must connect that with the WiiMote. Then, we must interface the mbed with the gimbal's servos. Finally, we must process the IR camera data from the WiiMote to a heading vector. These processes are nontrivial (to us) and we anticipate a significant amount of the time will be spent on calibration and debugging.