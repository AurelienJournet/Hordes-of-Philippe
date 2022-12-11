from typing import List, Union

import pygame

import tools
from character.character import Character
from map.map import Map


def is_there_collision(one_rect: pygame.Rect, rect_list: List[pygame.Rect]) -> bool:
    collision = one_rect.collidelist(rect_list)
    if collision != -1:
        return True
    else:
        return False


def check_allowed_mouvement(game_map: Map, character: Character, x_move: int = 0, y_move: int = 0) -> [int, int]:

    character_rect = character.get_rect()
    rect_after_move = character_rect.move(x_move, y_move)
    collidable_rects = game_map.get_collidable_rects()

    # On teste d'avoir si le mouvement "entier" est réalisable
    if not is_there_collision(rect_after_move, game_map.get_collidable_rects()):
        return [x_move, y_move]
    # Si non, on discrétise le mouvement et on essaie de renvoyer le plus grand possible
    else:
        x_max = 0
        y_max = 0
        for x_test in range(1, x_move):
            rect_after_move = character_rect.move(x_test, y_max)
            if not is_there_collision(rect_after_move, collidable_rects):
                x_max = x_test
            else:
                break
        for y_test in range(1, y_move):
            rect_after_move = character_rect.move(x_max, y_test)
            if not is_there_collision(rect_after_move, collidable_rects):
                y_max = y_test
            else:
                break
        # Retourne le mouvement possible "maximum"
        return [x_max, y_max]


def apply_gravity_to_character(character: Character, game_map: Map, gravity_value: int, max_vertical_speed: int):

    # Calcul de la vitesse à partir de l'accélération et de la vitesse max
    horiz_speed, vert_speed = character.get_speed()
    new_vert_speed = vert_speed + gravity_value
    if new_vert_speed > 0 and new_vert_speed > max_vertical_speed:
        new_vert_speed = max_vertical_speed
    elif new_vert_speed < 0 and new_vert_speed < -max_vertical_speed:
        new_vert_speed = -max_vertical_speed

    # Application du mouvement induit
    allowed_move_y = check_allowed_mouvement(game_map, character, 0, new_vert_speed)[1]

    # Si le mouvement autorisé est 0 et que la vitesse est nulle, c'est que l'entité ne tombe plus
    character.set_falling(False if not allowed_move_y and not vert_speed else True)
    if not allowed_move_y:
        new_vert_speed = 0
    # Pour éviter que les personnages ne tombent indéfiniment hors de la map
    if character.get_rect().y > game_map.get_height() * 2:
        new_vert_speed = 0
        allowed_move_y = 0
    character.move(0, allowed_move_y)
    character.set_speed(horiz_speed, new_vert_speed)


def make_character_jump(character: Character, jump_vertical_speed: int):

    if not character.is_jumping():
        horiz_speed, vert_speed = character.get_speed()
        character.set_speed(horiz_speed, -jump_vertical_speed)
        character.set_jumping(True)

    elif character.is_jumping() and not character.is_double_jumping() and character.get_speed()[1] > 0:
        horiz_speed, vert_speed = character.get_speed()
        character.set_speed(horiz_speed, -jump_vertical_speed)
        character.set_double_jumping(True)


def check_jumping_character_have_landed(character: Character):
    # Si une entité est en cours de saut et qu'elle ne tombe pas, c'est qu'elle a atteri
    # On passe donc le statut is_jumping à False

    if character.is_jumping() and not character.is_falling():
        character.set_jumping(False)
        character.set_double_jumping(False)


def make_character_shoot_and_handle_damage(shooter: Character, possible_targets: List[Character], game_map: Map):
    shoot_vector = shooter.shoot()
    damage_to_apply = shooter.get_attack_points()
    if shoot_vector:
        # 1 : on vérifie si il y a eu collision avec un rect du décor, on récupère la distance min
        shoot_distance_to_map_obj = tools.does_vector_collide_rects(shoot_vector[0], shoot_vector[1],
                                                                    game_map.get_collidable_rects())

        for target in possible_targets:
            shoot_distance_to_npc = tools.does_vector_collide_rects(shoot_vector[0], shoot_vector[1],
                                                                    [target.get_rect()])

            if shoot_distance_to_npc != -1:
                if shoot_distance_to_map_obj == -1 or shoot_distance_to_npc < shoot_distance_to_map_obj:
                    target.take_damage(damage_to_apply)


def is_position_fall_safe(game_map: Map, x: int, y: int) -> bool:
    # Permet de s'assurer qu'en un point les personnages ne meurent pas si on les "lache"
    # On vérifie simplement que sur une droite verticale passant par le point de lacher, il y a intersection avec
    # un rectangle collisionnable de la map

    collision = tools.does_vector_collide_rects((x, y), (x, game_map.get_height()),game_map.get_collidable_rects())
    return True if collision != -1 else False
