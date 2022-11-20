import sys
import pygame
import settings
import argparse
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', required=True)
    parser.add_argument('-s', '--fps', required=False)
    args = parser.parse_args()

    folder_of_sprite = args.folder
    fps_to_use = int(args.fps) if args.fps else settings.FPS

    pygame.init()
    display_size = [0, 0]
    images_list = []
    for file in Path(folder_of_sprite).glob('*.png'):
        image = pygame.image.load(file.as_posix())
        if image.get_height() > display_size[1]:
            display_size[1] = image.get_height()
        elif image.get_width() > display_size[0]:
            display_size[0] = image.get_width()
        images_list.append({"image": image, "rect": image.get_rect()})

    screen = pygame.display.set_mode(display_size)
    screen.fill(settings.BLACK)
    game_clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN):
                sys.exit()
        for image in images_list:
            screen.blit(image["image"], image["rect"])
            pygame.display.flip()
            game_clock.tick(fps_to_use)
