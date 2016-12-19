import pygame
from pygame.locals import *
from sys import exit


background_image_file = 'sushiplate.jpg'

SCREEN_SIZE = (640, 480)
pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
background = pygame.image.load(background_image_file).convert()

FullScreen = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == VIDEORESIZE:
            SCREEN_SIZE = event.size
            screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
            pygame.display.set_caption("Janela redimensionada para " + str(event.size))
            screen_width, screen_height = SCREEN_SIZE

            for y in range(0, screen_height, background.get_height()):
                for x in range(0, screen_width, background.get_width()):
                    screen.blit(background, (x, y))










    pygame.display.update()