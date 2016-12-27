import pygame
from pygame.locals import *
from random import randint


class Star(object):

    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed


def run():
    pygame.init()
    screen = pygame.display.set_mode((640, 480), FULLSCREEN)
    # screen = pygame.display.set_mode((640, 480), 0, 32)

    stars = []

    # adiciona algumas estrelas no primeiro frame
    for n in range(200):
        x = float(randint(0, 639))
        y = float(randint(0, 479))
        speed = float(randint(10, 300))
        stars.append(Star(x, y, speed))

    clock = pygame.time.Clock()
    white = (255, 255, 255)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                pygame.quit()
                quit()

        # adiciona uma nova estrela
        y = float(randint(0, 479))
        speed = float(randint(10, 300))
        star = Star(640., y, speed)
        stars.append(star)
        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.0

        screen.fill((0, 0, 0))

        # desenha as estrelas
        for star in stars:
            new_x = star.x - time_passed_seconds * star.speed
            pygame.draw.aaline(screen, white, (new_x, star.y), (star.x+1., star.y))
            star.x = new_x

        def on_screen(star):
            return star.x > 0

        # remove as estrelas que nao estejam visiveis
        stars = list(filter(on_screen, stars))
        pygame.display.update()


if __name__ == "__main__":
    run()