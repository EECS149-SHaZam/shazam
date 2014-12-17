rs485
=====
For talking with the stepper motors.

Note: RS-485 is voltage-incompatible with RS-232.

Wiring
------

### TTL-to-RS485 converter board

![pinout](http://www.raspberrypi.org/documentation/usage/gpio/images/basic-gpio-layout.png)

Wiring is:

| Pi pin   |Pi function| Converter|
|==========+===========+==========|
| 20       | GND       | GND      |
| 8        | TX        | RX       |
| 10       | RX        | TX       |
| 11       | GPIO17    | RTS      |
| 17       | 3v3       | Vcc      |

Driving the serial link
-----------------------

### System setup

1. Run `make install` to modify the system's configuration files.

2. Then, `sudo reboot`.

### Enable RTS

Run this with `sudo python`:

```python
from RPi import GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, True)
```

Source:

* Third Eye Visions: [Lighting Up An Led Using Your Raspberry Pi and Python][GPIO LED]

### Command the motor

```python
from motor_control import MotorController
mc = MotorController()
mc.send(id=mc.pitchID, inst=mc.INST_WRITE, addr=mc.Address.P_GOAL_POSITION, values=mc.split_int(mc.MIN_PITCH))
mc.send(id=mc.yawId, inst=mc.INST_WRITE, addr=mc.Address.P_GOAL_POSITION, values=mc.split_int(mc.STRAIGHT_YAW))
```

Links
-----
* [USB2Dynamixel][]

[USB2Dynamixel]: http://support.robotis.com/en/software/dynamixel_sdk/usb2dynamixel.htm
[GPIO LED]: http://www.thirdeyevis.com/pi-page-2.php
