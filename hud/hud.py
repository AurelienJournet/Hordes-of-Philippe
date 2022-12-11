
import pygame

import settings
from character.character import Character


class Hud:

    def __init__(self, display: pygame.Surface, player: Character):

        self.__display = display
        self.__score = 0
        self.__player = player
        self.__engame = False

    def update_score(self, score: int):
        self.__score = score

    def display(self):
        font = pygame.font.SysFont(None, 24)
        pv = font.render(f"PV : {self.__player.get_health_points()}", True, settings.GREEN)
        self.__display.blit(pv, (20, 20))

        score = font.render(f"Score : {self.__score}", True, settings.RED)
        self.__display.blit(score, (20, 40))

        if self.__player.is_dead():
            font = pygame.font.SysFont(None, 100)
            img = font.render("té mors", True, settings.RED)
            self.__display.blit(img, (self.__display.get_width()//2, self.__display.get_height()//2))
        elif self.__engame:
            font = pygame.font.SysFont(None, 100)
            img = font.render("victoire", True, settings.RED)
            self.__display.blit(img, (self.__display.get_width() // 2, self.__display.get_height() // 2))

    def end_game(self):
        self.__engame = True