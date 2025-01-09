from time import sleep
from pathlib import Path
import secrets
import shared
import os

token = secrets.token_urlsafe(8)
animation_token = 'animation_' + token
cava_token = 'cava_' + token

current_directory = str(Path(__file__).parent.resolve())
play_animation = current_directory + '/scripts/play_animation.sh'


class Animation(object):
    def __init__(self, time, frames):
        self.time = time
        self.frames = frames[:-1]

    @staticmethod
    def animate_full(time, frames):
        frames_list = frames.split(',')

        for frame in frames_list:
            os.system(f"echo '{frame}'")
            sleep(time)

    def animation_without_transition(self, category):
        if category == 'full':
            self.animate_full(self.time, self.frames)
        else:
            from shared import run_proc

            my_pid = os.getpid()
            run_me = [play_animation, self.time, self.frames, category, token, shared.player, my_pid]

            run_proc(run_me, token)

