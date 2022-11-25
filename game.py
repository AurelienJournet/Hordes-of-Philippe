import pygame

from map.Map import Map
from player.Player import Player
from background.Background import Background
from sounds.Sounds import Sounds

from ActionHandler import ActionHandler
import settings


# TODO : à convertir à terme en class "Level" ? (un jeu contiendra notamment plusieurs levels)


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Hordes of Philippe')
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)
        self.__size = self.__width, self.__height = settings.SCREEN_SIZE
        self.__display = pygame.display.set_mode(self.__size)
        self.__game_clock = pygame.time.Clock()
        self.__map = Map(self.get_display())
        self.__player = Player(self.get_display())
        self.__background = Background("library/jungle_of_phillipe", self.get_display())

        self.__action_handler = ActionHandler(self.__display, self.__map, self.__player, self.__background)

        Sounds.play_sound(sound_file_path="library/fond.mp3", loop=True)

        # TODO : faire une initialisation des NPC dans une classe par exemple (et avec la MAP ?)

    def get_display(self) -> pygame.Surface:
        return self.__display

    def update(self):
        pass
        # TODO : à voir si utile (passe les "Handler" dedans ?)

    def display(self):
        self.__display.fill(settings.BLACK)
        self.__background.display()
        self.__map.display()
        self.__player.display()
        pygame.display.flip()
        self.__game_clock.tick(settings.FPS)

    def run(self):
        while True:
            self.display()
            self.__action_handler.run()


if __name__ == '__main__':
    my_game = Game()
    my_game.run()








