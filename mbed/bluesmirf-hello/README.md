bluesmirf-hello
===============

Interface the mbed uC with the Bluesmirf module.

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

