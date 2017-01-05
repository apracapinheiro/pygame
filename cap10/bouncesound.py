import pygame
from pygame.locals import *
from random import randint
from gameobjects.vector2 import Vector2


SCREEN_SIZE = (640, 480)
# Em pixels por segundo
GRAVITY = 300.0

# Aumente esse valor para ter mais batidas, mas nao defina um valor maior que 1
BOUNCINESS = 0.7


def stereo_pan(x_coord, screen_width):
    right_volume = float(x_coord) / screen_width
    left_volume = 1.0 - right_volume

    return (left_volume, right_volume)


class Ball(object):
    def __init__(self, position, speed, image, bounce_sound):
        self.position = Vector2(position)
        self.speed = Vector2(speed)
        self.image = image
        self.bounce_sound = bounce_sound
        self.age = 0.0

    def update(self, time_passed):
        w, h = self.image.get_size()

        screen_width, screen_height = SCREEN_SIZE

        x, y = self.position
        x -= w/2
        y -= h/2

        # A bola bateu?
        bounce = False

        # A bola atingiu a parte inferior da tela?
        if y + h >= screen_height:
            self.speed.y = -self.speed.y * BOUNCINESS
            self.position.y = screen_height - h / 2.0 - 1.0
            bounce = True

        # A bola atingiu a borda esquerda da tela?
        if x <= 0:
            self.speed.x = -self.speed.x * BOUNCINESS
            self.position.x = w / 2.0 + 1
            bounce = True
        # A bola atingiu a borda direita da tela?
        elif x + w >= screen_width:
            self.speed.x = -self.speed.x * BOUNCINESS
            self.position.x = screen_width - w / 2.0 - 1
            bounce = True

        # Cria um movimento baseado em tempo
        self.position += self.speed * time_passed
        # Acrescenta a gravidade
        self.speed.y += time_passed * GRAVITY

        if bounce:
            self.play_bounce_sound()

        self.age += time_passed


    def play_bounce_sound(self):
        channel = self.bounce_sound.play()

        if channel is not None:
            # Obtem os volumes da esquerda e da direita
            left, right = stereo_pan(self.position.x, SCREEN_SIZE[0])
            channel.set_volume(left, right)


    def render(self, surface):
        # desenha o centro do sprite em self.position
        w, h = self.image.get_size()
        x, y = self.position
        x -= w/2
        y -= h/2
        surface.blit(self.image, (x,y))


def run():
    # Inicializa com som estereo de 16 bitas a 44 Khz
    pygame.mixer.pre_init(44100, 16, 2, 1024*4)
    pygame.init()
    pygame.mixer.set_num_channels(8)
    screen = pygame.display.set_mode(SCREEN_SIZE, 0)

    print(pygame.display.get_wm_info())
    hwnd = pygame.display.get_wm_info()["window"]
    x, y = (200, 200)

    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    ball_image = pygame.image.load("ball.png").convert_alpha()
    mouse_image = pygame.image.load("mousecursor.png").convert_alpha()

    # carrega o arquivo com o som
    bounce_sound = pygame.mixer.Sound("bounce.wav")

    balls = []

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == MOUSEBUTTONDOWN:
                # cria uma nova bola na posicao do mouse
                random_speed = (randint(-400, 400), randint(-300, 0))
                new_ball = Ball(event.pos,
                                random_speed,
                                ball_image,
                                bounce_sound)
                balls.append(new_ball)

        time_passed_seconds = clock.tick() / 1000.
        screen.fill((0, 0, 0))
        dead_balls = []

        for ball in balls:
            ball.update(time_passed_seconds)
            ball.render(screen)

            # nao faz nada com as bolas que tenham mais de 10 segundos de vida
            if ball.age > 10.0:
                dead_balls.append(ball)

        # remove quaisquer bolas 'mortas' da lista principal
        for ball in dead_balls:
            balls.remove(ball)

        # desenha o cursos do mouse
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(mouse_image, mouse_pos)

        pygame.display.update()

if __name__ == "__main__":
    run()