
SHELL=bash


install: sysconf
	
uninstall: uninstall-sysconf

# http://store.linksprite.com/rs485-gpio-shield-for-raspberry-pi/
sysconf:
	sudo mv /boot/cmdline.txt{,.bkp}
	sudo cp sysconf/cmdline.txt /boot/cmdline.txt
	
	sudo mv /etc/inittab{,.bkp}
	sudo cp sysconf/inittab /etc/inittab
	@echo
	@echo "System configuration files have been moved into place."
	@echo "Restart to apply the changes."

uninstall-sysconf: /boot/cmdline.txt.bkp /etc/inittab.bkp
	sudo rm /boot/cmdline.txt
	sudo mv /boot/cmdline.txt{.bkp,}
	
	sudo rm /etc/inittab
	sudo mv /etc/inittab{.bkp,}
	@echo
	@echo "System configuration files have been restored from their original data."
	@echo "Restart to apply the changes."
	

.PHONY: install sysconf uninstall-sysconf uninstall
