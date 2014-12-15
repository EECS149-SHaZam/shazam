raspi
=====
This directory contains source files and documentation about using the Raspberry Pi as the core of Shazam. In many ways, it supplants the `mbed` directory.

Links
-----
This project would not be possible without the help of web resources. We want to heartily thank and acknowledge the writers of these articles and open source projects.

* Physical computing with Raspberri Pi: [Interfacing with a Wiimote][]
* elinux.org: [Serial port programming][]

Installation
------------

To install the software dependencies on the Raspi, run

```bash
make deps
```

inside the `raspi` directory.

First link
----------
Press 1 and 2 on the Wiimote. Then, run 
    
```bash
make bt-on rumble
```


[Interfacing with a Wiimote]: https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/wiimote/
[Serial port programming]: http://www.elinux.org/Serial_port_programming

