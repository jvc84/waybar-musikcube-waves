from subprocess import check_output, Popen, CalledProcessError
from sys import exit
import os

player = "any"


def give_output(command):
    return check_output([command], shell=True)


def check_music_player() -> (bool, bool):
    global player

    if player == "cava":
        return True

    try:
        status = get_status()

        if status == b'Playing\n':
            mus = True
        else:
            mus = False

        if b'P' in status:
            play = True
        else:
            play = False

    except CalledProcessError:
        mus =  False
        play = False

    return mus, play


def get_status():
    global player

    command = ''

    if player == "any":
        command = 'playerctl -l'
    else:
        f'playerctl status --player="{player}"'

    output = give_output(command)

    if player == "any":
        is_playing = b'Paused\n'
        list = str(output)[2:-3].split('\\n')
        for pl in list:
            if give_output(f'playerctl status --player="{pl}"') == b'Playing\n':
                is_playing = b'Playing\n'
                break

        output = is_playing

    return output


def frame_multiplier(frames, repeats):
    more_frames = ''
    for n in range(repeats):
        more_frames += frames

    return more_frames


def run_proc(args, token):
    string_args = ""

    for i in args:
        string_args += ("'" + str(i) + "'" + " ")

    pid = Popen([string_args], shell=True)

    try:
        pid.wait()
    except KeyboardInterrupt:
        pid.kill()

    remaining_pids = str(check_output([f"ps aux | grep {token} " + " | awk '{print $2}'"], shell=True))[
                2:-3].split("\\n")

    for pid in remaining_pids:
        os.system(f"kill -9 {pid}")


def show_help():
    print("""
    Usage:
    
        python /path/to/wayves/wayves.py [--off <OPTION>] [--inactive <OPTION>] [--active <OPTION>] [--player PLAYER]
    
    Animation flags:
    
        -h, --help                   -    displays this help end exit
        -p, --player <PLAYER>        -    player whit activity will be represented by this module    
    (Unnecessary if all other flag have same value. You can get names of active players by command 'playerctl -l')    
        -o, --off  <OPTION>          -    scripts, that shows whe player is down. 'cat' by default
        -i, --inactive   <OPTION>    -    scripts, that shows when player is up, but music is on pause. 'splash' by default
        -a, --active  <OPTION>       -    scripts, that shows whe player is up, and music is playing. 'cava' by default
    
    Options:
    
        cat                 -    ASCII cat animations
        info                -    'no sound'/'sound'
        splash              -    some different animations of 3 bars
        waves               -    scripts of 3 bars moving up and down
        cava[=SECTION]      -    dynamic waves, that depend on sound. Requires cava
                                 available SECTIONS: left, right, all. SECTION=all by default
        empty[=NUM]         -    shows NUM spaces. NUM=0 by default
        flat[=NUM]          -    shows NUM '▁'. NUM=16 by default
        
    Cava config:
        
        In config you can configure number of bars and frame rate (and other stuff)
        Config path         -    $HOME/.config/cava/cava_option_config    
    """)

    exit()
