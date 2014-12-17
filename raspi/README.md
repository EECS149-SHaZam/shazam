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
make install
```

inside the `raspi` directory.


Hardware setup
--------------

### First link

Plug in a bluetooth dongle, then press 1 and 2 on the Wiimote. Then, run 
    
```bash
make bt-on rumble
```

After the Wiimote is linked, it will start to pulse its rumble pack. Break the program with ctrl-C.

### Motors

 then connect the RS-485 adapter (see the README in the rs485 folder). The RS-485 adapter connects to one of the steppers, which is daisy-chained with a second one.

Running
-------

Run `sudo python statechart.py`.

Other files
-----------

There was some effort to refactor the statechart into a more object-oriented form. This was left unfinished, in `main_statechart.py`, `manual_statechart.py`, `statechart_class.py`, `messages.py`, `wiimote/lights.py`, and `wiimote/buttons.py`.

`main_statechart.py` is the entry point for this alternate version. It is runnable, but it does not send motor commands as of yet.

Raspberry Pi system configuration
=================================

Connecting to the internet
--------------------------

In the lab, it is not possible to use the ethernet connections for the Pi. There are protections on them to prevent this. Instead, I had to use my laptop as a proxy and share its internet connection with the Pi. To do this:

1) Connect the Pi to the laptop with an ethernet cable.

2) Turn on the ssh server on the laptop.

3) Connect to Airbears from the laptop. Airbears2 will not work.

4) Set the laptop's ethernet IP manually to 192.168.2.1, and the mask to 255.255.255.0.

5) Set the pi's IP address:

```bash
sudo ifconfig eth0 192.168.2.2 netmask 255.255.255.0
sudo route add default gw 192.168.2.1 eth0
```

6) Add nameservers to the pi. In `/etc/resolv.conf`, 

```conf
nameserver 8.8.8.8
nameserver 8.8.4.4
```

7) Start an ssh tunnel on the pi:

```bash
ssh -D 8080 username@192.168.2.1
```

8) Configure the pi's proxy settings. In another shell in the pi, execute

```bash
export http_proxy=http://127.0.0.1:8080
export ftp_proxy=ftp://127.0.0.1:8080
```

9) Now, try to ping a nameserver:

```bash
ping google.com
```

    It should work.

Sources:

* fclose.com: [Making ssh proxy][]
* The Ubuntu Documentation: [Network Configuration][]
* Justin Tung: [How to Configure Proxy Settings in Linux][]

Pi NAT for the gateway
----------------------

To connect to the gateway laptop from the Pi without using an IP address:

```bash
sudo echo '192.168.2.1 gateway' >> /etc/hosts
```

Now the pi can refer to the laptop as `gateway` instead of using the IP address.

Source:

* Rackspace.com: [How do I modify my hosts file?][]

Mac NAT for the Pi
------------------

```bash
sudo echo '192.168.2.2 raspberrypi' >> /private/etc/hosts
```

Now, the Mac can refer to the Pi as `raspberrypi` instead of using an IP address.

Source:

* Rackspace.com: [How do I modify my hosts file?][]

Uploading files remotely
------------------------

It was useful to have multiple people working on the pi at once. It was necessary to transfer files, so we used NFS.

First, we do some setup on the Pi. Run:

```bash
sudo apt-get install nfs-kernel-server portmap nfs-common
```

Edit `/etc/exports` to add the home folder to the list of shares:

```conf
/home/pi gateway(rw,async,insecure,anonuid=1000,no_subtree_check,all_squash)
```

Edit `/etc/netconfig` to disable IPv6, which generates errors for us:

```conf
udp        tpi_clts      v     inet     udp     -       -
tcp        tpi_cots_ord  v     inet     tcp     -       -
#udp6       tpi_clts      v     inet6    udp     -       -
#tcp6       tpi_cots_ord  v     inet6    tcp     -       -
rawip      tpi_raw       -     inet      -      -       -
local      tpi_cots_ord  -     loopback  -      -       -
unix       tpi_cots_ord  -     loopback  -      -       -
```

Now, run:
```bash
sudo /etc/init.d/nfs-kernel-server restart
```

Source:

* NixCraft: [Ubuntu Linux NFS Server Installation and Configuration][]

### Connecting from Mac
Using the GUI does not work well with NAT, but the command line tools do. Run:

```bash
mkdir /Volumes/pi
mount -t nfs -o tcp raspberrypi:/home/pi /Volumes/pi
```

Source:

* Michel Jansen: [NFS behind NAT on Mac OS X][]


[Interfacing with a Wiimote]: https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/wiimote/
[Serial port programming]: http://www.elinux.org/Serial_port_programming
[wifi driver]: http://ubuntuforums.org/showthread.php?t=2235778
[Making ssh proxy]: http://www.fclose.com/944/proxy-using-ssh-tunnel/
[Network Configuration]: https://help.ubuntu.com/10.04/serverguide/network-configuration.html
[How to Configure Proxy Settings in Linux]: http://justintung.com/2013/04/25/how-to-configure-proxy-settings-in-linux/
[Ubuntu Linux NFS Server Installation and Configuration]: http://www.cyberciti.biz/faq/how-to-ubuntu-nfs-server-configuration-howto/
[NFS behind NAT on Mac OS X]: http://micheljansen.org/blog/entry/38
[How do I modify my hosts file?]: http://www.rackspace.com/knowledge_center/article/how-do-i-modify-my-hosts-file
