#!/bin/bash


get_any() {
    string="$(playerctl -l)"
    
    if (( $(echo $strnig | wc -l ) == 0 )); then
      player_status="Stopped"
    else
      lines=(${string//\\n/\ })
      player_status="Paused"    
      for line in "${lines[@]}"; do
          player_status="$(playerctl status --player="$line")"
          if [[ $player_status == *"Play"* ]]; then
            player_status="Playing"
            break
          fi
      done
    fi
}


get_variables() {
    if [[ "$player" == "cava" ]]; then
	      player_status="Playing"
        category="active"
    elif [[ "$player" == "any" ]]; then
        get_any
    else
      	player_status="$( playerctl status --player="$player" 2> /dev/null)"
    fi

    # check_music
    if [ "$player_status" = "Playing" ]; then
        check_music="true"
    else
        check_music="false"
    fi

    # check_player
    if [[ $player_status == "P"* ]]; then
        check_player="true"
    else
        check_player="false"
    fi


    pid_count="$(ps aux | grep " $parent_pid " | wc -l)"
}


check_state() {
    get_variables

    while :
    do
      get_variables
      if [ \( "$category" = "off" \) -a \( "$check_player" = "true" \) ] || \
      [ \( "$category" = "inactive" \) -a \( \( "$check_player" = "false" \) -o \( "$check_music" = "true" \) \) ] || \
      [ \( "$category" = "active" \) -a \( \( "$check_player" = "false" \) -o \( "$check_music" = "false" \) \) ] || \
      (( pid_count < 2 ))  ; then
          if (( pid_count < 2 )); then
            pkill -f "$token" &>/dev/null
          fi
            exit
      fi
      sleep 1
    done
}
