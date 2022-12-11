import pygame

from hud.hud import Hud
from map.map import Map
from character.character import Character
from background.background import Background
from sounds.sounds import Sounds

from actionhandler import ActionHandler
import settings


# TODO : tout documenter
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
        self.__player = Character(self.get_display(), "sprites/mike", "mike", [0, -100], [200, 140], health_points=100,
                                  rate_of_fire=10, attack_points=50)

        # Les NPC sont générés et gérés par le NPC Handler qui les remontent à chaque run
        self.__npc = []
        self.__score = 0
        self.__goal_score = 30
        self.__endgame = False

        self.__background = Background("library/jungle_of_phillipe", self.get_display())
        self.__hud = Hud(self.__display, self.__player)
        self.__action_handler = ActionHandler(self.__display, self.__map, self.__player, self.__background)

        Sounds.play_sound(sound_file_path="library/intro.mp3")
        Sounds.play_sound(sound_file_path="library/fond.mp3", loop=True)

    def get_display(self) -> pygame.Surface:
        return self.__display

    def update(self):
        self.__hud.update_score(self.__score)
        if self.__player.is_dead():
            self.end_game()
        elif self.__score >= self.__goal_score:
            self.end_game()

    def end_game(self):
        if not self.__endgame:
            self.__endgame = True
            self.__hud.end_game()

    def display(self):
        self.__display.fill(settings.BLACK)
        self.__background.display()
        self.__map.display()
        for npc in self.__npc:
            npc.display()
        self.__player.display()
        self.__action_handler.display()
        self.__hud.display()
        pygame.display.flip()
        self.__game_clock.tick(settings.FPS)

    def run(self):
        while True:
            self.display()
            if not self.__endgame:
                self.__npc, self.__score = self.__action_handler.run()
                self.update()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit(0)


if __name__ == '__main__':
    my_game = Game()
    my_game.run()








