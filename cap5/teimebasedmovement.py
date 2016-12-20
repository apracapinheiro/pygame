import pygame
from pygame.locals import *
from sys import exit


background_image_filename = 'sushiplate.jpg'
sptrite_image_file = 'fugu.png'

pygame.init()

screen = pygame.display.set_mode((640, 480), 0, 32)

background = pygame.image.load(background_image_filename).convert()
sprite = pygame.image.load(sptrite_image_file)

# objeto clock
clock = pygame.time.Clock()

# a coordenada x do sprite
x = 0.

# a velocidade em pixels por segundo
speed = 250


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    screen.blit(background, (0, 0))
    screen.blit(sprite, (x, 100))

    time_passed = clock.tick()
    time_passed_seconds = time_passed / 1000.0

    distance_moved = time_passed_seconds * speed
    x += distance_moved

    # se a imagem ultrapassar a extremidade da tela, mova-a de volta
    if x > 640:
        x -= 640

    pygame.display.update()