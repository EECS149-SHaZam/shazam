#!/bin/bash

if [[ "$0" != "-bash" ]]; then
    this_dir=$(dirname "$0")
    this_dir="$(pushd "$this_dir" &>/dev/null ; pwd ; popd &>/dev/null)"
    dest_dir="$this_dir/downloaded-packages"
fi

uri="http://downloads.raspberrypi.org/raspbian_latest"


function ensureDest() {
    [[ -d "$dest_dir" ]] ||
        mkdir -v "$dest_dir"
}

function cleanUp() {
    ls "$dest_dir/"*.zip
    echo "`ls "$dest_dir/"*.zip | wc -l | xargs` zipped image(s)"
}

function getUriFilename() {
    header="$(curl -sI "$1" | tr -d '\r')"

    filename="$(echo "$header" | grep -o -E 'filename=.*$')"
    if [[ -n "$filename" ]]; then
        echo "${filename#filename=}"
        return
    fi

    filename="$(echo "$header" | grep -o -E 'Location:.*$')"
    if [[ -n "$filename" ]]; then
        basename "${filename#Location\:}"
        return
    fi

    return 1
}

function ensureDownloaded() {
    pushd "$dest_dir" &>/dev/null
    filename="$(getUriFilename $uri)"
    if [[ $? != 0 ]]; then
        echo "Could not see server!"
        return 1
    fi
    
    # check if we already have a complete latest file
    if [[ -f "$filename" ]]; then
        echo "Found $filename. Verifying structure..."
        if unzip -tq "$filename" &>/dev/null; then 
            echo "$filename is valid!"
        else
            echo "$filename is not complete. Resuming download..."
            echo "Downloading $uri ==> $filename ..."
            # Use -C - to resume the download
            if ! curl -L $uri -C - -o "$filename" ; then
                rm -v "$filename"
                echo "Something was wrong with the download. Please try again."
                return 1
            else
                echo "Finished download!"
            fi
            return
        fi
    else
        echo "Downloading $uri ==> $filename ..."
        # Use -C - to resume the download
        curl -L $uri -o "$filename"
    fi
    popd &>/dev/null
}


if [[ "$0" != "-bash" ]]; then
    ensureDest &&
    ensureDownloaded
    cleanUp
fi
