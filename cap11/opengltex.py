from math import radians

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *


SCREEN_SIZE = (800, 600)


def resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width)/height, .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.0, 0.0, 0.0, 0.0)


def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)

    resize(*SCREEN_SIZE)
    init()

    # carrega a textura
    texture_surface = pygame.image.load("sushitex.png")
    # obetem os dados da textura
    textura_data = pygame.image.tostring(texture_surface, 'RGB', True)

    # gera um id de textura
    texture_id = glGenTextures(1)
    # informa a OpenGL que usaremos esse id de textura nas operacoes com textura
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # diz a OpenGL de que modo as imagens devem ser escaladas
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    # informa a OpenGL que os dados estao alinhados nas fronteiras de bytes
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    # obtem as dimensoes da imagem
    width, height = texture_surface.get_rect().size

    # carrega a imagem na OpenGL
    glTexImage2D(GL_TEXTURE_2D,
                 0,
                 3,
                 width,
                 height,
                 0,
                 GL_RGB,
                 GL_UNSIGNED_BYTE,
                 textura_data)

    clock = pygame.time.Clock()

    tex_rotation = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.
        tex_rotation += time_passed_seconds * 360.0 / 8.0

        # limpa a tela (semelhante a fill)
        glClear(GL_COLOR_BUFFER_BIT)

        # limpa a matriz model-view
        glLoadIdentity()

        # define a matriz model-view
        glTranslatef(0.0, 0.0, -600.0)
        glRotate(tex_rotation, 1, 1, 1)

        # desenha um quadrilatero (4 vertices, 4 coordenadas de textura)
        glBegin(GL_QUADS)

        glTexCoord2d(0, 1)
        glVertex3f(-300, 300, 0)

        glTexCoord2d(1, 1)
        glVertex3f(300, 300, 0)

        glTexCoord2d(1, 0)
        glVertex3f(300, -300, 0)

        glTexCoord2d(0, 0)
        glVertex3f(-300, -300, 0)

        glEnd()

        pygame.display.flip()

    glDeleteTextures(texture_id)


if __name__ == '__main__':
    run()