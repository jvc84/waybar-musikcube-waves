#!/bin/bash

MYDIR=$(dirname "$(realpath "$0")")

source "$MYDIR/headers.sh"

# Args
time=${1}
frames=${2}
category=${3}
token=${4}
player=${5}
parent_pid=${6}


# Variables
readarray -td, frames_arr <<< "$frames"

# Functions
animation() {
    for i in  "${!frames_arr[@]}"
    do
        echo "${frames_arr[i]//[$'\n']}"
        sleep "$time"
    done
    pkill -f "$token" &> /dev/null
}

# Main
animation & check_state
