from pathlib import Path

import pygame


class Sounds:

    @staticmethod
    def play_sound(sound_file_path: str, loop: bool = False):

        full_sound_file_path = Path(Path(__file__).parent, sound_file_path).as_posix()
        # Si le son doit être joué en boucle, on utilise forcément le channel 0
        if loop:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(full_sound_file_path), loops=-1)

        # Sinon, on utilise n'importe quel autre canal (on prend le premier non occupé, si il y en a un)
        else:
            for channel_number in range(1, pygame.mixer.get_num_channels()):
                if not pygame.mixer.Channel(channel_number).get_busy():
                    pygame.mixer.Channel(channel_number).play(pygame.mixer.Sound(full_sound_file_path))
                    break
