from subprocess import check_output, CalledProcessError

player = ""


def get_status():
    global player

    output = str(check_output(
        [f'playerctl status --player="{player}" 2> /dev/null'],
        shell=True))

    return output


def check_music():
    global player

    if player == "cava":
        return True

    try:
        status = get_status()

        if 'Playing' in status:
            return True
        else:
            return False

    except CalledProcessError:
        return False


def check_player():
    global player

    if player == "cava":
        return True

    try:
        status = get_status()

        if 'P' in status:
            return True
        else:
            return False

    except CalledProcessError:
        return False


def frame_multiplier(frames, repeats):
    more_frames = ''
    for n in range(repeats):
        more_frames += frames

    return more_frames


def show_help():
    print("""
          Usage:
              python /path/to/wayves.py [--off <OPTION>] [--inactive <OPTION>] [--active <OPTION>] [--palyer PLAYER]
          
          Animation flags:
              -h, --help                  -    displays this help end exit
              -p, --player <PLAYER>        -    player whit activity will be represented by this module    
          (Unnecessary if all other flag have same value. You can get names of active players by command 'playerctl -l')    
              -o, --off  <OPTION>          -    scripts, that plays whe soundcube is down. 'cat' by default
              -i, --inactive   <OPTION>    -    scripts, that plays when soundcube is up, but music is on pause. 'splash' by default
              -a, --active  <OPTION>       -    scripts, that plays whe soundcube is up, and music is playing. 'cava' by default
          
          OPTIONs:
              cat                 -    ASCII cat animations
              info                -    'no sound'/'sound'
              splash              -    some different animations of 3 bars
              waves               -    scripts of 3 bars moving up and down
              cava[=SECTION]      -    dynamic waves, that depend on sound. Requires cava
                                       available SECTIONS: left, right, all. SECTIONS=all by default
                                       number of bars and framerate can be defined in $XDG_CONFIG_HOME/cava/cava_<OPTION>_config
              empty[=NUM]         -    shows NUM spaces. NUM=0 by default
              flat[=NUM]          -    shows NUM '▁'. NUM=16 by default"""
    )