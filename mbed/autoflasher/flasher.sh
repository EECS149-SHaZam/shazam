#!/bin/bash
# Watches stdin for filenames to flash and copies them to DST_DRIVE.

# The name of the destination "flash drive"
DST_DRIVE="/Volumes/MBED"

# Interval to check for DST_DRIVE during reboot
INTERVAL=0.5

function check_vars() {
    if ! [[ -d "$DST_DRIVE" ]]; then
        (
            echo "The DST_DRIVE does not exist:"
            echo "  ${DST_DRIVE}"
            echo "Please modify $0."
        ) >/dev/stderr
        return 1
    fi
}

function flashit() {
    local fname="$1"
    if cp "$fname" "$DST_DRIVE"; then
        echo "Uploaded: $fname"
    else
        echo "Failed to upload: $fname" > /dev/stderr
        return 1
    fi
}

function wait_reboot() {
    wait_unmount && wait_remount || echo "Failed to reboot" > /dev/stderr
    echo "Press the reset button on the microcontroller to start the program."
}

function wait_unmount() {
    while [[ -d "$DST_DRIVE" ]]; do
        sleep "$INTERVAL"
    done
    echo "Unmounted. Waiting for remount..."
}

function wait_remount() {
    while ! [[ -d "$DST_DRIVE" ]]; do
        sleep "$INTERVAL"
    done
    echo "Mounted. Reboot complete."
}

function main() {
    local fname
    check_vars || return 1
    while read fname; do
        flashit "$fname" && wait_reboot || exit 1
    done
}

# if not sourcing, pass arguments to main
if [[ "$0" != "-bash" ]]; then
    main "$@"
fi
