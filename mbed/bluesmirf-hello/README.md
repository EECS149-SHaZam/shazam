bluesmirf-hello
===============

Interface the mbed uC with the Bluesmirf module.

This was created to demonstrate interfacing the FRDM-KL25Z with the [Sparkfun BlueSMiRF Gold](https://www.sparkfun.com/products/12582). Unfortunately for us, I discovered that the board version I had would not interface with a WiiMote, which was my ultimate goal. There are several modes of Bluetooth operation, including serial and HID modes. The BlueSMiRF Gold works with serial, while I need HID mode to connect to the WiiMote. To get this requires a different firmware to be installed on the BlueSMiRF, which is done at the factory. This means that we cannot use the BlueSMiRF with the WiiMote.

(There is another version of this board called the [BlueSMiRF HID](https://www.sparkfun.com/products/10938), which would probably serve my purpose.)

However, the code might be useful for a different project.

Instructions
------------
### Mac
These are based on [Sparkfun's guide](https://learn.sparkfun.com/tutorials/using-the-bluesmirf/example-code-using-command-mode).

1. Load the binary onto the flash.

2. Before resetting, run this in the Terminal:
    
        screen /dev/tty.usbmodem*

3. Hit the reset button. You should see a hello message:
    
        Hello World!
        Bluesmirf 0x1ffff178(0x60) is on tx=0x2010 and rx=0x200c
    
    The Bluesmirf light will blink slowly.

4. Enter Command mode by typing `$$$` without a carriage return. You should see it respond with `CMD`, and the Bluesmirf will blink quickly.

5. Type `D` with a carriage return. This will show the device config.

6. Type `I,` with a carriage return. This will search for nearby BT devices.

7. Copy the BT address (beginning of line until comma). To connect to that address, run
    
        C,<address>
    
    with a carriage return. You will see it respond `TRYING`. If you need to enter a code on the target device, the code was displayed when you typed `D`.

8. If successful, you will see no other output, and be immediately dropped into data mode. The Bluesmirf will blink slowly again.

9. If not successful, you can exit command mode by typing `---` with a carriage return.

