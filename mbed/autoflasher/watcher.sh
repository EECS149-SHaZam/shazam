#!/bin/bash
# Watches the given directory for new binaries and echoes them 
# if they should be programmed to the mbed board.

# The suffix that the compiler adds to the binary's filename
BOARD_MODEL="KL25Z"

function filter_binaries() {
    local fname="$1"
    
    # check file extension and for suffix indicating BOARD_MODEL
    [[ "$fname" == *$BOARD_MODEL*.bin ]] || return 1
    
    # check that running `file` on it shows raw data, and not binhex file
    [[ "$(file "$fname")" == "${fname}: data" ]] || return 1
    
    echo "$fname"
}

function main() {
    local fname
    fswatch "$@" | while read fname; do
        filter_binaries "$fname"
    done
}

# if not sourcing, run main
if [[ "$0" != "-bash" ]]; then
    main "$@"
fi
    
