# Makefile
# Installs dependencies for shazam on a Raspberry Pi running Raspbian
#
# Based on tutorial at
# https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/wiimote/

SHELL=bash

APT_PKGS=bluez \
	python-cwiid \
	python-bluez \
	python-dev \
	python-serial

install: deps
	(cd rs485; make install)

uninstall: clean
	(cd rs485; make uninstall)

deps: apt-pkgs python-pkgs git-repos
	
apt-pkgs: apt-update
	sudo apt-get install $(APT_PKGS)

apt-update:
	sudo apt-get update

python-pkgs:
	sudo easy_install-pypy pip
	
git-repos: 

cwiid:
	git clone git@github.com:chaimleib/cwiid

bt-on:
	sudo hciconfig hci0 piscan

rumble:
	python wiimote/rumble.py

led-counter:
	python wiimote/led_counter.py

clean:
	rm -f *.pyc
	rm -f wiimote/*.pyc
	rm -rf cwiid

.PHONY: deps \
	apt-pkgs \
	apt-update \
	bt-on \
	rumble \
	led-counter \
	clean \
	python-pkgs \
	git-repos

