import math

from npchandler import NPCHandler
from background.background import Background
import settings
from physics import *


class ActionHandler:

    def __init__(self, display: pygame.Surface, game_map: Map, player: Character, background: Background):
        self.__display = display
        self.__map = game_map
        self.__player = player

        self.__npc_handler = NPCHandler(self.__display, self.__player, self.__map)
        self.__background = background
        self.__display_size = self.__display.get_size()
        self.sign = lambda x: math.copysign(1, x)
        self.__npc = []
        self.__score = 0

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        self.__player.set_moving(False)
        self.handle_move_cmd()

        self.__npc, self.__score = self.__npc_handler.run()
        for character in [self.__player, *self.__npc]:
            apply_gravity_to_character(character, self.__map, settings.GRAVITY, settings.MAX_VERT_SPEED)
            check_jumping_character_have_landed(character)

        # TODO : vérifier les NPC toujours vivants et les return
        self.check_fallen_characters()

        return self.__npc, self.__score

    # TODO : à voir si on garde
    def display(self):
        self.__npc_handler.display()

    def handle_move_cmd(self):
        keys = pygame.key.get_pressed()
        if not self.__player.is_dead():
            if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            # Changement éventuel du sens des sprites
                self.__player.change_direction(True if keys[pygame.K_RIGHT] else False)
                self.__player.set_moving(True)
                wanted_move_x = settings.PLAYER_SPEED if keys[pygame.K_RIGHT] else -settings.PLAYER_SPEED
                allowed_move_x = check_allowed_mouvement(self.__map, self.__player, wanted_move_x, 0)[0]
                forward = True if keys[pygame.K_RIGHT] else False
                background_translation = \
                    self.sign(allowed_move_x) * (abs(allowed_move_x) // settings.BACKGROUND_TRANSLATION_SPEED_RATIO)

                # Tant que le joueur ne dépasse pas la moitité de la longueur horizontale de l'écran, seuls la map et
                # les npc bouge
                if (self.__player.get_rect().x < self.__display_size[0] // 2
                        if forward else self.__player.get_rect().x > self.__display_size[0] // 2):
                    self.__player.move(pixels_x=allowed_move_x, pixels_y=0)

                # Sinon c'est le joueur ou la map et les npc en fonction de si la limite est atteinte
                else:
                    if not self.__map.has_reached_limit(not forward):
                        self.__map.translate(allowed_move_x)
                        self.__background.translate(- background_translation)
                        for npc in self.__npc:
                            npc.move(pixels_x=-allowed_move_x, pixels_y=0)
                    else:
                        self.__player.move(pixels_x=allowed_move_x, pixels_y=0)

            if keys[pygame.K_LCTRL]:
                # TODO : afficher les impacts
                make_character_shoot_and_handle_damage(self.__player, self.__npc, self.__map)

            if keys[pygame.K_SPACE]:
                make_character_jump(self.__player, settings.JUMP_VERT_SPEED)

    # TODO : permet de kill les entités qui sont tombées par exemple
    def check_fallen_characters(self):
        for character in [self.__player, *self.__npc]:
            if character.get_rect() and character.get_rect().y > self.__map.get_height() + 2 * character.get_rect().h:
                character.kill()



    # TODO : voir comment faire disparaître les morts depuis un certain temps
