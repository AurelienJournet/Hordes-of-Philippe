from math import sqrt
from typing import Union

import pygame

import settings
from sprites.Sprite import Sprite
from sounds.Sounds import Sounds


# TODO : faire une classe "Living Entity" dont héritera Player -> pour les sprites mettre un sprite path
# TODO : avec la speed et la position a minima (pour le apply_gravity de ActionHandler)

# TODO : mettre la cadence de tir quelque part (le virtual FPS de Sprite)


class Player:

    def __init__(self, game: pygame.Surface):

        #TODO : pour init un "character" :
        # - dossier des Sprites
        # - position sur la MAP
        # - points de vie
        # - points d'attaque
        # - offset du canon du fusil
        # - debug du shooting

        self.__game = game
        self.__sprite_run = Sprite(self.__game, "sprites/phillipe/Run", 30, forced_height=200)
        self.__sprite_death = Sprite(self.__game, "sprites/phillipe/Death", 30, forced_height=200)
        self.__sprite_idle = Sprite(self.__game, "sprites/phillipe/Idle", 30, forced_height=200)
        self.__sprite_jump = Sprite(self.__game, "sprites/phillipe/Jump", 30, forced_height=200)
        self.__sprite_fall = Sprite(self.__game, "sprites/phillipe/Fall", 30, forced_height=200)
        self.__sprite_shoot = Sprite(self.__game, "sprites/phillipe/Shoot", 10, forced_height=200)

        self.__player_rect = None
        self.__position = [0, 0]
        self.__speed = [0, 0]
        self.__is_dead = False
        self.__is_moving = False
        self.__is_falling = False
        self.__is_jumping = False
        self.__is_shooting = False
        self.__is_going_to_the_right = True

        # A conditionner éventuellement avec un attribut en paramètre (can_double_jump ?)
        self.__is_double_jumping = False

        # TODO : à voir quoi en faire, sion garde
        self.__debug_shooting_activated = True
        self.__gun_position_offset_right = [230, 140]
        self.__max_distance_shooting = sqrt(self.__game.get_height() * self.__game.get_height() +
                                            self.__game.get_width() * self.__game.get_width())

    def get_speed(self) -> [int, int]:
        return self.__speed

    def set_speed(self, x_speed: int, y_speed: int):
        self.__speed = [x_speed, y_speed]

    def kill(self):
        self.__is_dead = True

    def is_dead(self) -> bool:
        return self.__is_dead

    def move(self, pixels_x: int, pixels_y: int):
        self.__position[0] += pixels_x
        self.__position[1] += pixels_y

    def set_moving(self, is_moving: bool):
        self.__is_moving = is_moving

    def is_jumping(self) -> bool:
        return self.__is_jumping

    def set_jumping(self, is_jumping: bool):
        self.__is_jumping = is_jumping
        if is_jumping:
            Sounds.play_sound("library/tg.mp3")

    def is_double_jumping(self) -> bool:
        return self.__is_double_jumping

    def set_double_jumping(self, is_double_jumping: bool):
        self.__is_double_jumping = is_double_jumping
        if is_double_jumping:
            Sounds.play_sound("library/viensici2.mp3")

    def get_player_rect(self) -> pygame.Rect:
        return self.__player_rect

    def set_falling(self, is_falling: bool):
        self.__is_falling = is_falling
        if not is_falling:
            self.__speed[1] = 0

    def is_falling(self) -> bool:
        return self.__is_falling

    def set_shooting(self, is_shooting: bool):
        self.__is_shooting = is_shooting
        if is_shooting:
            Sounds.play_sound("library/panpan.mp3")

    def is_shooting(self) -> bool:
        return self.__is_shooting

    def shoot(self) -> Union[None, tuple]:
        # TODO : lui faire retourner un projectile  (ou pas, selon la cadence)
        # TODO : ça peut être une position et une direction
        if not self.__is_shooting:
            self.set_shooting(True)
            return self.calculate_shoot_vector()
        return

    def stop_shooting(self):
        self.set_shooting(False)

    def calculate_shoot_vector(self) -> tuple:
        start_position = self.__player_rect.x + self.__gun_position_offset_right[0], \
                         self.__player_rect.y + self.__gun_position_offset_right[1]
        shoot_line = self.__max_distance_shooting if self.__is_going_to_the_right else -self.__max_distance_shooting
        end_position = self.__player_rect.x + self.__gun_position_offset_right[0] + shoot_line, \
            self.__player_rect.y + self.__gun_position_offset_right[1]
        return start_position, end_position

    def change_sprites_way(self, going_right=True):
        if not going_right == self.__is_going_to_the_right:
            self.__sprite_run.flip_horizontally()
            self.__sprite_idle.flip_horizontally()
            self.__sprite_jump.flip_horizontally()
            self.__sprite_fall.flip_horizontally()
            self.__sprite_shoot.flip_horizontally()
            self.__is_going_to_the_right = going_right

            if not going_right:
                self.__gun_position_offset_right[0] -= self.__player_rect.w
            else:
                self.__gun_position_offset_right[0] += self.__player_rect.w

    def display(self):

        if self.is_shooting() and self.__debug_shooting_activated:
            pygame.draw.line(self.__game, settings.RED, *self.calculate_shoot_vector())

        if self.is_shooting():
            if not self.__sprite_shoot.end_of_sprite_reached():
                self.__player_rect = self.__sprite_shoot.draw_next_image_with_position(*self.__position)
            else:
                self.__player_rect = self.__sprite_idle.draw_next_image_with_position(*self.__position)
                self.__sprite_shoot.reset_sprite()
                self.stop_shooting()
        elif self.__is_jumping:
            self.__player_rect = self.__sprite_jump.draw_next_image_with_position(*self.__position)
        elif self.__is_falling:
            self.__player_rect = self.__sprite_fall.draw_next_image_with_position(*self.__position)
        elif self.__is_moving:
            self.__player_rect = self.__sprite_run.draw_next_image_with_position(*self.__position)
        elif self.__is_dead:
            if not self.__sprite_death.end_of_sprite_reached():
                self.__player_rect = self.__sprite_death.draw_next_image_with_position(*self.__position)
            else:
                self.__player_rect = self.__sprite_death.draw_last_image_with_position(*self.__position)
        else:
            self.__player_rect = self.__sprite_idle.draw_next_image_with_position(*self.__position)
