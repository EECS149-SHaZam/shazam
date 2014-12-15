raspi
=====
This directory contains source files and documentation about using the Raspberry Pi as the core of Shazam. In many ways, it supplants the `mbed` directory.

Links
-----
This project would not be possible without the help of web resources. We want to heartily thank and acknowledge the writers of these articles and open source projects.

* Physical computing with Raspberri Pi: [Interfacing with a Wiimote][]
* elinux.org: [Serial port programming][]
* Netgear A6100 [wifi driver][]

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

Raspberry Pi system configuration
=================================
Connecting to the internet
--------------------------
In the lab, it is not possible to use the ethernet connections for the Pi. There are protections on them to prevent this. Instead, I had to use my laptop as a proxy and share its internet connection with the Pi. To do this:

1) Connect the Pi to the laptop with an ethernet cable.
2) Turn on the ssh server on the laptop.
3) Set the laptop's ethernet IP manually to 192.168.2.1.
4) Set the pi's IP address:

```bash
sudo ifconfig eth0 192.168.2.2 netmask 255.255.255.0
sudo route add default gw 192.168.2.1 eth0
```

5) Add nameservers to the pi. In `/etc/resolv.conf`, 

```conf
nameserver 8.8.8.8
nameserver 8.8.4.4
```

6) Start an ssh tunnel on the pi:

```bash
ssh -D 8080 username@192.168.2.1
```

7) Configure the pi's proxy settings. In another shell in the pi, execute

```bash
export http_proxy=http://127.0.0.1:8080
export ftp_proxy=ftp://127.0.0.1:8080
```

8) Now, try to ping a nameserver:

```bash
ping google.com
```

    It should work.

Sources:
* fclose.com: [Making ssh proxy][]
* The Ubuntu Documentation: [Network Configuration][]
* Justin Tung: [How to Configure Proxy Settings in Linux][]

Uploading files remotely
------------------------
It was useful to have multiple people working on the pi at once. It was necessary to transfer files, so we used NFS. The instructions are in NixCraft's [Ubuntu Linux NFS Server installation and Configuration][].


[Interfacing with a Wiimote]: https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/wiimote/
[Serial port programming]: http://www.elinux.org/Serial_port_programming
[wifi driver]: http://ubuntuforums.org/showthread.php?t=2235778
[Making ssh proxy]: http://www.fclose.com/944/proxy-using-ssh-tunnel/
[Network Configuration]: https://help.ubuntu.com/10.04/serverguide/network-configuration.html
[How to Configure Proxy Settings in Linux]: http://justintung.com/2013/04/25/how-to-configure-proxy-settings-in-linux/
[Ubuntu Linux NFS Server installation and Configuration]: http://www.cyberciti.biz/faq/how-to-ubuntu-nfs-server-configuration-howto/
