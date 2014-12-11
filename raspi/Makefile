# Makefile
# Installs dependencies for shazam on a Raspberry Pi running Raspbian
#
# Based on tutorial at
# https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/wiimote/

SHELL=bash

APT_PKGS=bluez \
	python-cwiid \
	python-bluez


deps: apt-pkgs
	

apt-pkgs: apt-update
	sudo apt-get install $(APT_PKGS)

apt-update:
	sudo apt-get update

bt-on:
	sudo hciconfig hci0 piscan

rumble:
	python wiimote/rumble.py

led-counter:
	python wiimote/led_counter.py


.PHONY: deps \
	apt-pkgs \
	apt-update \
	bt-on \
	rumble \
	led-counter

