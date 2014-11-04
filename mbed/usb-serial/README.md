usb-serial
==========
This is a fork of the usb-serial template provided by the mbed online IDE. 

I modified it, because gnu screen (which I use on my Mac) does not play nicely with just `\n` characters, and to my great disappointment, I can't find an option to make it treat unix linefeeds appropriately.

Accessing the serial device
---------------------------
I've only tried this on a Mac. First, plug in the mbed board. Then, find the device file using

```
ls /dev/tty.usbmodem*
```

The `*` is important.

Then, run screen on it:

```
screen DEVICE_FILE
```

When you are done, hit `Ctrl-a`, `k`, `y` in sequence to close screen. If you don't do this and break off the serial connection, weird things can happen to your terminal window.

