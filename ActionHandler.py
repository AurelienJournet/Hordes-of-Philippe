import math
from typing import List

import pygame

from map.Map import Map
from player.Player import Player
from background.Background import Background
import settings
import tools

class ActionHandler:

    def __init__(self, game: pygame.Surface, map: Map, player: Player, background: Background):
        self.__game = game
        self.__map = map
        self.__player = player
        self.__background = background
        self.__game_display_size = self.__game.get_size()
        self.sign = lambda x: math.copysign(1, x)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        self.__player.set_moving(False)
        self.handle_move_cmd()

        # TODO : à généraliser une fois le principe vérifié
        self.apply_gravity_to_player()
        self.check_jumping_player_has_landed()

    @staticmethod
    def is_there_collision(one_rect: pygame.Rect, rect_list: List[pygame.Rect]) -> bool:
        collision = one_rect.collidelist(rect_list)
        if collision != -1:
            return True
        else:
            return False

    def check_allowed_mouvement(self, x_move: int = 0, y_move: int = 0) -> [int, int]:
        player_rect = self.__player.get_player_rect()
        rect_after_move = player_rect.move(x_move, y_move)

        # On teste d'avoir si le mouvement "entier" est réalisable
        if not self.is_there_collision(rect_after_move, self.__map.get_collidable_rects()):
            return [x_move, y_move]
        # Si non, on discrétise le mouvement et on essaie de renvoyer le plus grand possible
        else:
            x_max = 0
            y_max = 0
            for x_test in range(1, x_move):
                rect_after_move = player_rect.move(x_test, y_max)
                if not self.is_there_collision(rect_after_move, self.__map.get_collidable_rects()):
                    x_max = x_test
                else:
                    break
            for y_test in range(1, y_move):
                rect_after_move = player_rect.move(x_max, y_test)
                if not self.is_there_collision(rect_after_move, self.__map.get_collidable_rects()):
                    y_max = y_test
                else:
                    break
            # Retourne le mouvement possible "maximum"
            return [x_max, y_max]

    def handle_move_cmd(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            # Changement éventuel du sens des sprites
            self.__player.change_sprites_way(True if keys[pygame.K_RIGHT] else False)
            if not self.__player.is_dead():
                self.__player.set_moving(True)
                wanted_move_x = settings.PLAYER_SPEED if keys[pygame.K_RIGHT] else -settings.PLAYER_SPEED
                allowed_move_x = self.check_allowed_mouvement(wanted_move_x, 0)[0]
                forward = True if keys[pygame.K_RIGHT] else False
                background_translation = \
                    self.sign(allowed_move_x) * (abs(allowed_move_x) // settings.BACKGROUND_TRANSLATION_SPEED_RATIO)

                # Tant que le joueur ne dépasse pas la moitité de la longueur horizontale de l'écran, seule la map bouge
                if (self.__player.get_player_rect().x < self.__game_display_size[0] // 2
                        if forward else self.__player.get_player_rect().x > self.__game_display_size[0] // 2):
                    self.__player.move(pixels_x=allowed_move_x, pixels_y=0)
                # Sinon c'est le joueur ou la map en fonction de si la limite est atteinte
                else:
                    if not self.__map.has_reached_limit(not forward):
                        self.__map.translate(allowed_move_x)
                        self.__background.translate(- background_translation)
                    else:
                        self.__player.move(pixels_x=allowed_move_x, pixels_y=0)

        if keys[pygame.K_k]:
            self.__player.kill()

        if keys[pygame.K_LCTRL]:
            # TODO : ajouter la gestion des conséquences du tir avec le vecteur retourné par la méthode
            # TODO : afficher les impacts
            shoot_vector = self.__player.shoot()
            if shoot_vector:
                a = tools.does_vector_collide_rects(shoot_vector[0], shoot_vector[1], self.__map.get_collidable_rects())

                print(a)

        if keys[pygame.K_SPACE]:
            self.make_player_jump()

    def make_player_jump(self):

        if not self.__player.is_jumping():
            horiz_speed, vert_speed = self.__player.get_speed()
            self.__player.set_speed(horiz_speed, -settings.JUMP_VERT_SPEED)
            self.__player.set_jumping(True)
        elif self.__player.is_jumping() and not self.__player.is_double_jumping() and self.__player.get_speed()[1] > 0:
            horiz_speed, vert_speed = self.__player.get_speed()
            self.__player.set_speed(horiz_speed, -settings.JUMP_VERT_SPEED)
            self.__player.set_double_jumping(True)

    def apply_gravity_to_player(self):
        # Calcul de la vitesse à partir de l'accélération et de la vitesse max
        horiz_speed, vert_speed = self.__player.get_speed()
        new_vert_speed = vert_speed + settings.GRAVITY
        if new_vert_speed > 0 and new_vert_speed > settings.MAX_VERT_SPEED:
            new_vert_speed = settings.MAX_VERT_SPEED
        elif new_vert_speed < 0 and new_vert_speed < - settings.MAX_VERT_SPEED:
            new_vert_speed = -settings.MAX_VERT_SPEED

        # Application du mouvement induit
        allowed_move_y = self.check_allowed_mouvement(0, new_vert_speed)[1]

        # Si le mouvement autorisé est 0 et que la vitesse est nulle, c'est que l'entité ne tombe plus
        self.__player.set_falling(False if not allowed_move_y and not vert_speed else True)
        if not allowed_move_y:
            new_vert_speed = 0
        self.__player.move(0, allowed_move_y)
        self.__player.set_speed(horiz_speed, new_vert_speed)

    def check_jumping_player_has_landed(self):
        # Si une entité est en cours de saut et qu'elle ne tombe pas, c'est qu'elle a atteri
        # On passe donc le statut is_jumping à False

        #print(self.__player.is_jumping(), self.__player.is_falling())

        if self.__player.is_jumping() and not self.__player.is_falling():
            self.__player.set_jumping(False)
            self.__player.set_double_jumping(False)

    def is_entity_out_of_display(self):
        pass
        # TODO : permet de kill les entités qui sont tombées par exemple

    # TODO : voir comment faire disparaître les morts

