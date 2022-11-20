from pathlib import Path

import pygame


class Sounds:

    def __init__(self):
        pass

    @staticmethod
    def play_sound(sound_file_path: str, loop: bool = False):
        pygame.mixer.music.load(Path(Path(__file__).parent, sound_file_path).as_posix())
        pygame.mixer.music.play(loops=-1 if loop else 1)

    # TODO : gérer les superpositions de son (ne marche pas actuellement)




