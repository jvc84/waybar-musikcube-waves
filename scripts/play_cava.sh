#!/bin/bash

MYDIR=$(dirname "$(realpath "$0")")

source "$MYDIR/headers.sh"

# Args
cava_position=${1}
category=${2}
token=${3}
player=${4}
parent_pid=${5}

# Variables
cache_path="$HOME/.cache/wayves"
cached_config="$cache_path/cava_option_config_$token"
config_path="$HOME/.config/cava"
config_file="$config_path/cava_option_config"

# Functions
cache_config() {
     cp "$config_file" "$cached_config" 2> /dev/null 
}

# Main
mkdir -p "$config_path" &> /dev/null
mkdir -p "$cache_path" &> /dev/null

cache_config ||
(cp "$PARENTDIR/assets/cava/cava_option_config" "$config_file" &> /dev/null && cache_config) ||
(echo "Cannot cache cava config!" && exit 1)


if [ "$cava_position" = "all" ]; then
    cut_cava="s/$//"
else
    bars=$(grep -E "bars=|bars =" "$cached_config" | cut -f2 -d "=" | cut -f2 -d " " | head -n1)
    bars=$(echo "scale=0; $bars / 2" | bc)

    # shellcheck disable=SC2183
    printf -v bars_string  "%*s" "$bars"

    dots=${bars_string// /.}

    if [ "$cava_position" = "left" ]; then
        cut_cava="s/$dots$//"

    elif [ "$cava_position" = "right" ]; then
        cut_cava="s/^$dots//"
    fi
fi


setsid cava -p "$cached_config" | sed -u "s/;//g;s/0/▁/g;s/1/▂/g;s/2/▃/g;s/3/▄/g;s/4/▅/g;s/5/▆/g;s/6/▇/g;s/7/█/g;" | sed -u "$cut_cava" & 
check_state 
