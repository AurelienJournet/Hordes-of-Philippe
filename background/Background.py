from pathlib import Path
from typing import Union

import pygame
import settings


# TODO : pouvoir faire des backgrounds en plusieurs couches
# TODO : pouvoir répéter le backgound

# TODO : documenter le fait que les images doivent être données de la plus éloignée à la plus rapprochée

class Background:

    def __init__(self, image_path: Union[str, list], game: pygame.Surface):
        self.__game = game
        self.__translation = 0
        self.__background_images_set = []

        # Si le paramètre est une chaîne de caractères, il s'agit d'un seul fichier ou d'un dossier
        abs_path = Path(Path(__file__).parent, image_path)
        if isinstance(image_path, str):
            # Si le chemin renseigné est un dossier, on regarde la ou les images dedans
            if abs_path.is_dir():
                for image in Path(abs_path).glob("*"):
                    self.__background_images_set.append({"image": pygame.image.load(image),
                                                         "rect": pygame.image.load(image).get_rect()})
            else:
                self.__background_images_set.append({"image": pygame.image.load(abs_path),
                                                     "rect": pygame.image.load(abs_path).get_rect()})
        
        # Sinon, c'est une liste de chemins d'images dans l'ordre
        elif isinstance(image_path, str):
            self.__background_images_set.append({"image": pygame.image.load(image_path),
                                                 "rect": pygame.image.load(image_path).get_rect()})

        # Scaling des images et ajout des Rect
        for background_image in self.__background_images_set:
            
            # On transforme chaque image en un dictionnaire image + rect associé
            scale_ratio = self.__game.get_height() / background_image["image"].get_height()
            scaled_background_image = pygame.transform.scale(background_image["image"],
                                                             (background_image["image"].get_width() * scale_ratio,
                                                              self.__game.get_height()))
            background_image["image"] = scaled_background_image
            background_image["rect"] = scaled_background_image.get_rect()

    def display(self):

        for background_image in self.__background_images_set:

            # Calcul du nombre minimal d'images nécessaires pour couvrir l'écran
            min_images_nb_to_cover_display = self.__game.get_width() // background_image["image"].get_width() + 2

            if -background_image["rect"].x > background_image["image"].get_width() or \
                    background_image["rect"].x + background_image["image"].get_width() * min_images_nb_to_cover_display < self.__game.get_width():
                background_image["rect"].x += background_image["image"].get_width()

            elif background_image["rect"].x > 0:
                background_image["rect"].x -= background_image["image"].get_width()

            for i in range(min_images_nb_to_cover_display + 1):
                self.__game.blit(background_image["image"],
                                 background_image["rect"].move(background_image["rect"].x + i *
                                                               background_image["image"].get_width(), 0))

            # print(background_image["rect"].x)
            # self.__game.blit(background_image["image"], background_image["rect"])

    def translate(self, pixels):
        i = 0
        for background_image in self.__background_images_set:
            background_image["rect"] = background_image["rect"].move(pixels * i, 0)
            i += 1
