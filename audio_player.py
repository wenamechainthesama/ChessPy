from pygame import mixer
from os.path import abspath, dirname


class Sound:
    move = "move-self.mp3"
    capture = "capture.mp3"
    castle = "castle.mp3"
    check = "move-check.mp3"
    promote = "promote.mp3"


class AudioPlayer:
    def __init__(self):
        self.sounds_path = str(abspath(dirname(__file__))) + "/sounds"
        mixer.init()

    def play(self, sound_filename):
        sound = mixer.Sound(self.sounds_path+ "/" + sound_filename)
        sound.play()
