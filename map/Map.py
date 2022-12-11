import json
from typing import List

import pygame
from pathlib import Path
import settings

# TODO : pouvoir intégrer des objets qui provoquent des dommages

class Map:

    def __init__(self, game: pygame.Surface):
        self.__game = game
        self.__map_definition = ""
        self.load_map_definition()

        self.__element_height = int(self.__game.get_height() / len(self.__map_definition))
        self.__element_width = int(self.__game.get_width() / settings.G_HORIZ_ELEMENTS_TO_DISPLAY)
        self.__textures_definition = None
        self.load_textures_definition()
        self.__translation = 0
        self.__collidable_rects = []
        self.__right_limit_reached = False

    def load_map_definition(self):
        read_map = Path(Path(__file__).parent, "map_definition.txt").read_text()
        self.__map_definition = read_map.split("\n")

        # Vérification que la map est bien complète
        if not all([len(self.__map_definition[0].split(",")) == len(line.split(","))
                    for line in self.__map_definition]):
            raise Exception("Définition de la map incorrection : nombre d'éléments incohérent sur une ou plusieurs "
                            "lignes")

    def get_width(self) -> int:
        return len(self.__map_definition[-1].split(",")) * self.__element_width

    def get_height(self) -> int:
        return len(self.__map_definition) * self.__element_height

    def get_translation(self) -> int:
        return self.__translation

    def load_textures_definition(self):

        read_texture_mapping = Path(Path(__file__).parent, "textures/texture_mapping.json").read_text()

        self.__textures_definition = json.loads(read_texture_mapping)
        for key in self.__textures_definition["map"]:
            self.__textures_definition["map"][key] = pygame.transform.scale(pygame.image.load(Path(Path(__file__).parent,
                                                                          self.__textures_definition["map"][key])),
                                                                          (self.__element_width, self.__element_height))

    def translate(self, pixels):

        new_translation = self.__translation + pixels
        allowed_translation_right = self.get_width() - self.__game.get_width()

        if pixels > 0 and not self.__right_limit_reached:
            if new_translation > allowed_translation_right:
                self.__translation = allowed_translation_right
                self.__right_limit_reached = True
            else:
                self.__translation = new_translation

        elif pixels < 0:
            self.__right_limit_reached = False
            if new_translation > 0:
                self.__translation = new_translation
            else:
                self.__translation = 0

    def has_reached_limit(self, left):
        if left:
            to_return = True if self.__translation == 0 else False
        else:
            to_return = self.__right_limit_reached
        return to_return

    def get_collidable_rects(self) -> List[pygame.Rect]:
        return self.__collidable_rects

    def display(self):
        # On n'affiche que n unités horizontales de la MAP, on doit donc calculer la taille des élément
        self.__collidable_rects = []

        # for i in range(int(settings.G_HORIZ_ELEMENTS_TO_DISPLAY + (self.__translation / self.__element_width)) + 1):
        for i in range(len(self.__map_definition[0].split(","))):
            for j in range(len(self.__map_definition)):

                to_draw = self.__map_definition[j].split(",")[i]
                if to_draw != "0" and to_draw in self.__textures_definition["map"]:
                    rect = pygame.Rect(self.__element_width * i - self.__translation, self.__element_height * j,
                                       self.__element_width, self.__element_height)
                    self.__game.blit(self.__textures_definition["map"][to_draw],
                                                   (self.__element_width * i - self.__translation,
                                                    self.__element_height * j))
                    if to_draw not in self.__textures_definition["non_collidable"]:
                        self.__collidable_rects.append(rect)
