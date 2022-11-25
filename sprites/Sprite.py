import pygame
import settings
from pathlib import Path

import settings


#TODO : ajouter la possibilité de scaler les sprites à la taille désirée

class Sprite:

    def __init__(self, display_screen: pygame.Surface, folder_path: str, virtual_frames_number: int = None,
                 forced_height: int = -1):
        self.__folder_path = folder_path
        self.__display_screen = display_screen
        # Taille maximale du sprite
        self.__display_size = [0, 0]
        self.__image_list = []
        self.__current_image_index = 0
        self.__virtual_frames_number = virtual_frames_number
        self.__virtual_current_image_index = 0

        for file in Path(self.__folder_path).glob('*.png'):
            image = pygame.image.load(file.as_posix())

            image_ratio = image.get_width() / image.get_height()
            if forced_height != -1:
                image = pygame.transform.scale(image, (image_ratio*forced_height, forced_height))

            if image.get_height() > self.__display_size[1]:
                self.__display_size[1] = image.get_height()
            elif image.get_width() > self.__display_size[0]:
                self.__display_size[0] = image.get_width()
            self.__image_list.append({"image": image, "rect": image.get_rect()})

        if self.__virtual_frames_number:
            self.__each_frame_duration = self.__virtual_frames_number // len(self.__image_list) \
                if self.__image_list else 0
        else:
            self.__each_frame_duration = 1

    def flip_horizontally(self):
        for image in self.__image_list:
            image['image'] = pygame.transform.flip(image['image'], True, False)

    def end_of_sprite_reached(self) -> bool:
        if (self.__virtual_frames_number and self.__virtual_current_image_index == self.__virtual_frames_number)\
                or self.__current_image_index == len(self.__image_list) - 1:
            return True
        else:
            return False

    def reset_sprite(self):
        if self.__virtual_frames_number:
            self.__virtual_current_image_index = 0
        self.__current_image_index = 0

    def draw_next_image_with_position(self, x: int, y: int) -> pygame.Rect:

        self.__display_screen.blit(self.__image_list[self.__current_image_index]["image"],
                                   self.__image_list[self.__current_image_index]["rect"].move(x, y))

        self.__virtual_current_image_index += 1
        if self.__virtual_current_image_index > self.__each_frame_duration:
            self.__current_image_index += 1
            self.__virtual_current_image_index = 0

        if self.__current_image_index > len(self.__image_list) - 1:
            self.__current_image_index = 0

        return self.__image_list[self.__current_image_index]["rect"].move(x, y)

    def draw_last_image_with_position(self, x: int, y: int):
        self.__display_screen.blit(self.__image_list[-1]["image"],
                                   self.__image_list[-1]["rect"].move(x, y))

        return self.__image_list[-1]["rect"].move(x, y)

        # dessiner sur le display


