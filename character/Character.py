from math import sqrt
from pathlib import Path
from typing import Union


import pygame

import settings
from sprites.sprite import Sprite
from sounds.sounds import Sounds


# TODO : mettre le nombre de frames d'invicibilité qq part (le virtual frames sprite_hurt)

# TODO : ajouter un "shooting distance" (à gérer dans le ActionHandler et NPCHandler)
# TODO : ajouter une distance de vue (au delà de laquelle les ennemis ne nous voient pas) + vérifier qu'ils peuvent
#  nous voir


class Character:

    def __init__(self, display: pygame.Surface, sprites_folder: str, sounds_folder: str,
                 map_initial_position: [int, int], gun_position_offset_right: [int, int], rate_of_fire: float = 1.0,
                 health_points: int = 100, attack_points: int = 40, debug_shooting: bool = False):

        # TODO : dossier des sons pour avoir des sons custom pas character
        # TODO : voir pour éventuellement passer le forced_height des sprites en paramètre

        self.__position = map_initial_position
        self.__health_points = health_points
        self.__attack_points = attack_points
        self.__debug_shooting_activated = debug_shooting
        self.__gun_position_offset_right = gun_position_offset_right
        self.__sprites_folder = Path(sprites_folder).absolute().as_posix()
        self.__sounds_folder = sounds_folder

        self.__display = display
        self.__sprite_run = Sprite(self.__display, f"{self.__sprites_folder}/Run", 30, forced_height=130)
        self.__sprite_death = Sprite(self.__display, f"{self.__sprites_folder}/Death", 30, forced_height=130)
        self.__sprite_idle = Sprite(self.__display, f"{self.__sprites_folder}/Idle", 30, forced_height=130)
        self.__sprite_jump = Sprite(self.__display, f"{self.__sprites_folder}/Jump", 30, forced_height=130)
        self.__sprite_fall = Sprite(self.__display, f"{self.__sprites_folder}/Fall", 30, forced_height=130)
        self.__sprite_shoot = Sprite(self.__display, f"{self.__sprites_folder}/Shoot",
                                     int(settings.FPS / rate_of_fire), forced_height=130)
        self.__sprite_hurt = Sprite(self.__display, f"{self.__sprites_folder}/Hurt", 5, forced_height=130)

        self.__player_rect = pygame.Rect(0, 0, 0, 0)
        self.__speed = [0, 0]
        self.__is_dead = False
        self.__is_moving = False
        self.__is_falling = False
        self.__is_jumping = False
        self.__is_double_jumping = False
        self.__is_shooting = False
        self.__is_taking_damage = False
        self.__is_going_to_the_right = True
        self.__max_distance_shooting = sqrt(self.__display.get_height() ** 2 + self.__display.get_width() ** 2)

    def get_speed(self) -> [int, int]:
        return self.__speed

    def set_speed(self, x_speed: int, y_speed: int):
        self.__speed = [x_speed, y_speed]

    def take_damage(self, damage_points: int):
        if not self.__is_taking_damage:
            self.__health_points -= damage_points
            if self.__health_points <= 0:
                self.__health_points = 0
                self.kill()
            else:
                Sounds.play_sound(f"{self.__sounds_folder}/Hurt.mp3")
                self.__is_taking_damage = True

    def get_attack_points(self) -> int:
        return self.__attack_points

    def get_health_points(self) -> int:
        return self.__health_points

    def kill(self):
        if not self.__is_dead:
            self.__is_dead = True
            self.set_moving(False)
            Sounds.play_sound(f"{self.__sounds_folder}/Death.mp3")

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
        if is_jumping and not self.__is_dead:
            Sounds.play_sound(f"{self.__sounds_folder}/Jump.mp3")

    def is_double_jumping(self) -> bool:
        return self.__is_double_jumping

    def set_double_jumping(self, is_double_jumping: bool):
        self.__is_double_jumping = is_double_jumping
        if is_double_jumping and not self.__is_dead:
            Sounds.play_sound(f"{self.__sounds_folder}/Jump.mp3")

    def get_rect(self) -> pygame.Rect:
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
            Sounds.play_sound(f"{self.__sounds_folder}/Shoot.mp3")

    def is_shooting(self) -> bool:
        return self.__is_shooting

    def shoot(self) -> Union[None, tuple]:
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

    def change_direction(self, going_right=True):
        if not going_right == self.__is_going_to_the_right:
            self.__sprite_run.flip_horizontally()
            self.__sprite_idle.flip_horizontally()
            self.__sprite_jump.flip_horizontally()
            self.__sprite_fall.flip_horizontally()
            self.__sprite_shoot.flip_horizontally()
            self.__sprite_hurt.flip_horizontally()
            self.__is_going_to_the_right = going_right

            if not going_right:
                self.__gun_position_offset_right[0] -= self.__player_rect.w
            else:
                self.__gun_position_offset_right[0] += self.__player_rect.w

    def is_going_to_the_right(self) -> bool:
        return self.__is_going_to_the_right

    def display(self):

        # TODO : voir comment ajouter un sprite spécifique de tir quand on court ou saute
        if self.__is_taking_damage:
            if not self.__sprite_hurt.end_of_sprite_reached():
                self.__player_rect = self.__sprite_hurt.draw_next_image_with_position(*self.__position)
            else:
                self.__player_rect = self.__sprite_hurt.draw_next_image_with_position(*self.__position)
                self.__sprite_hurt.reset_sprite()
                self.__is_taking_damage = False
        else:
            if self.__is_dead:
                if not self.__sprite_death.end_of_sprite_reached():
                    self.__player_rect = self.__sprite_death.draw_next_image_with_position(*self.__position)
                else:
                    self.__player_rect = self.__sprite_death.draw_last_image_with_position(*self.__position)
            elif self.is_shooting():
                if self.__debug_shooting_activated:
                    pygame.draw.line(self.__display, settings.RED, *self.calculate_shoot_vector())
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

            else:
                self.__player_rect = self.__sprite_idle.draw_next_image_with_position(*self.__position)
