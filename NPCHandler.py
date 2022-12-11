
from random import random
from typing import Tuple

import settings
from physics import *
from sprites.sprite import Sprite


class NPCHandler:

    def __init__(self, display: pygame.Surface, player: Character, game_map: Map):

        self.__display = display
        self.__npc = []
        self.__player = player
        self.__map = game_map
        self.__score = 0
        # TODO : à mettre à terme dans l'init
        # TODO : mettre également les points d'attaque et les points de vie des NPC créés
        self.__number_of_npc = 1
        self.__sprite_target = Sprite(self.__display, f"sprites/target", virtual_frames_number=60, forced_height=50)

    def run(self) -> Tuple[List[Character], int]:
        self.renew_npc_and_calculate_score()
        for npc in self.__npc:
            npc.set_moving(False)
            # TODo : faire tout ça que si le npc est "à portée" ou si il voit le joueur

            #TODO : faire en sorte de sauter si la postion envisagée est dans le vide (is_position_fall_safe())
            # essayer de s'assurer que l'atterissage est possible
            if not npc.is_dead() and not self.__player.is_dead() and (not npc.is_falling() or npc.is_jumping()):
                has_to_go_down = (self.__player.get_rect().center[1] - npc.get_rect().center[1]) > npc.get_rect().h // 2
                has_to_jump = (npc.get_rect().center[1] - self.__player.get_rect().center[1]) > npc.get_rect().h // 4
                has_to_get_closer = abs(npc.get_rect().center[0] - self.__player.get_rect().center[0]) > (self.__display.get_width() // 2)
                has_to_get_further = abs(npc.get_rect().center[0] - self.__player.get_rect().center[0]) < (self.__display.get_width() // 4)

                is_too_close_from_another_npc = False
                for another_npc in self.__npc:
                    if another_npc != npc and another_npc.is_shooting():
                        if abs(another_npc.get_rect().x - npc.get_rect().x) < npc.get_rect().w // 4:
                            is_too_close_from_another_npc = True
                            break

                if has_to_get_closer or has_to_get_further and not has_to_go_down:
                    direction_move = (npc.get_rect().center[0] - self.__player.get_rect().center[0]) < 0
                    if has_to_get_further:
                        direction_move = not direction_move
                    npc.change_direction(True if direction_move else False)
                    move_x = settings.NPC_SPEED if direction_move else -settings.NPC_SPEED
                    allowed_move_x = check_allowed_mouvement(self.__map, npc, move_x, 0)
                    if allowed_move_x[0] != 0:
                        npc.move(pixels_x=allowed_move_x[0], pixels_y=0)
                        npc.set_moving(True)
                    else:
                        make_character_jump(npc, settings.JUMP_VERT_SPEED)
                elif has_to_jump:
                    make_character_jump(npc, settings.JUMP_VERT_SPEED)
                elif has_to_go_down or is_too_close_from_another_npc:
                    direction_move = npc.is_going_to_the_right()
                    move_x = settings.NPC_SPEED if direction_move else -settings.NPC_SPEED
                    allowed_move_x = check_allowed_mouvement(self.__map, npc, move_x, 0)
                    if allowed_move_x[0] != 0:
                        npc.move(pixels_x=allowed_move_x[0], pixels_y=0)
                        npc.set_moving(True)
                    else:
                        make_character_jump(npc, settings.JUMP_VERT_SPEED)
                else:
                    direction_move = (npc.get_rect().center[0] - self.__player.get_rect().center[0]) < 0
                    npc.change_direction(True if direction_move else False)
                    # TODO : afficher les impacts
                    make_character_shoot_and_handle_damage(npc, [self.__player], self.__map)

        #TODO : faire en sorte que les ennemis attendent un peu avant de tirer (si ils peuvent tirer instantanément
        # c'est trop dur lol)

        return self.__npc, self.__score

    def renew_npc_and_calculate_score(self):

        self.__score = len([npc for npc in self.__npc if npc.is_dead()])
        alive_npcs = len([npc for npc in self.__npc if not npc.is_dead()])
        if not self.__player.is_dead():
            while alive_npcs < self.__number_of_npc:

                position_fall_safe = False
                coord_apparation = [0, 0]
                while not position_fall_safe:
                    coord_apparation = [-self.__map.get_translation() + random() * self.__map.get_width(),
                                        -self.__map.get_height()]
                    position_fall_safe = is_position_fall_safe(self.__map, *coord_apparation)

                self.__npc.append(Character(self.__display, "sprites/phillip", "phillip", coord_apparation,
                                            [200, 140], attack_points=5, rate_of_fire=0.3))
                alive_npcs = len([npc for npc in self.__npc if not npc.is_dead()])

    def display(self):
        for npc in self.__npc:
            if not npc.is_dead():
                # Affichage d'un point rouge pour localiser les ennemis, lorsque qu'ils sont hors de l'écran
                coord_npc = npc.get_rect().center
                coord_player = self.__player.get_rect().center
                try:
                    a = (coord_npc[1] - coord_player[1]) / (coord_npc[0] - coord_player[0])
                except ZeroDivisionError:
                    a = 0
                b = coord_npc[1] - a * coord_npc[0]

                if coord_npc[0] > self.__display.get_width() > coord_player[0]:
                    intersect_x_max = a * self.__display.get_width() + b
                    self.__sprite_target.draw_next_image_with_position(self.__display.get_width() - 50, intersect_x_max)
                elif coord_npc[0] < 0 < coord_player[0]:
                    intersect_x_min = b
                    self.__sprite_target.draw_next_image_with_position(0, intersect_x_min)
