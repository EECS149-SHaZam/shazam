autoflasher
===========
Currently not working.

Watches the user's Downloads directory for new binaries compatible with the FRDM-KL25Z.

When such a binary arrives, copies it to the /Volumes/MBED/, thus programming the board. It then waits for the MBED device to unmount and mount again before trying to flash a new binary.

Dependencies
------------
Uses `fswatch`, which can be installed via [brew]:

```
brew install fswatch
```

Hacking
-------
There are two parts in autoflasher:

1. `watcher.sh DOWNLOADS_DIR` - watches `DOWNLOADS_DIR` for new binaries and echoes them. Tries to filter invalid files.
2. `flasher.sh` - copies filenames specified on stdin to /Volumes/MBED.

Currently, `watcher.sh` works, but not `flasher.sh`. It appears that `cp` from the shell does not cause the SDA to flash the main uC, although dragging and dropping does. The status light flashes to indicate USB traffic as usual, but I don't see the flashes afterwards indicating SDA serial traffic to the Cortex M0.

[brew]: http://brew.sh

