from math import radians

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.raw.GL.VERSION.GL_1_0 import glLoadMatrixd

import pygame
from pygame.locals import *

from gameobjects.matrix44 import *
from gameobjects.vector3 import *

SCREEN_SIZE = (800, 600)


def resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width)/height, .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


class Cube(object):
    def __init__(self, position, color):
        self.position = position
        self.color = color

    # informacoes do cubo
    num_faces = 6
    vertices = [(0.0, 0.0, 0.1),
                (1.0, 0.0, 1.0),
                (1.0, 1.0, 1.0),
                (0.0, 1.0, 1.0),
                (0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
                (1.0, 1.0, 0.0),
                (0.0, 1.0, 0.0)]

    normals = [(0.0, 0.0, +1.0),  # frente
               (0.0, 0.0, -1.0),  # tras
               (+1.0, 0.0, 0.0),  # direits
               (-1.0, 0.0, 0.0),  # esquerda
               (0.0, +1.0, 0.0),  # em cima
               (0.0, -1.0, 0.0)]  # embaixo

    vertex_indices = [(0, 1, 2, 3),  # frente
                      (4, 5, 6, 7),  # tras
                      (1, 5, 6, 2),  # direita
                      (0, 4, 7, 3),  # esquerda
                      (3, 2, 6, 7),  # em cima
                      (0, 1, 5, 4)]  # embaixo

    def render(self):
        # define a cor do cubo, aplica a todos os vertices ate a proxima chamada
        glColor(self.color)

        # ajusta todos os vertices para que o cubo esteja em self.position
        vertices = []
        for v in self.vertices:
            vertices.append(tuple(Vector3(v)+ self.position))

        # desenha todas as seis faces do cubo
        glBegin(GL_QUADS)
        for face_no in range(self.num_faces):
            glNormal3dv(self.normals[face_no])
            v1, v2, v3, v4 = self.vertex_indices[face_no]

            glVertex(vertices[v1])
            glVertex(vertices[v2])
            glVertex(vertices[v3])
            glVertex(vertices[v4])

        glEnd()


class Map(object):
    def __init__(self):
        map_surface = pygame.image.load("labirinto.gif")
        map_surface.lock()

        w, h = map_surface.get_size()
        self.cubes = []

        # cria um cubo para todos os pixels diferentes de branco
        for y in range(h):
            for x in range(w):
                r, g, b, a = map_surface.get_at((x, y))

                if (r, g, b) != (255, 255, 255):
                    gl_col = (r/255.0, g/255.0, b/255.0)
                    position = (float(x), 0.0, float(y))
                    cube = Cube(position, gl_col)
                    self.cubes.append(cube)

        map_surface.unlock()
        self.display_list = None

    def render(self):
        if self.display_list is None:
            # cria uma display list
            self.display_list = glGenLists(1)
            glNewList(self.display_list, GL_COMPILE)

            # desenha os cubos
            for cube in self.cubes:
                cube.render()

            # finaliza a display list
            glEndList()
        else:
            # renderiza a display list
            glCallList(self.display_list)


def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)

    resize(*SCREEN_SIZE)


    clock = pygame.time.Clock()

    # este objeto renderiza o mapa
    map = Map()

    # matriz de transformacao da camera
    camera_matrix = Matrix44()
    camera_matrix.translate = (10.0, .6, 10.0)

    # inicializa as velocidades e as direcoes
    rotation_direction = Vector3()
    rotation_speed = radians(90.0)
    movement_direction = Vector3()
    movement_speed = 5.0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == K_UP and event.key == K_ESCAPE:
                pygame.quit()
                quit()

        # limpa a tela e o buffer z
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.0

        pressed = pygame.key.get_pressed()

        # reinicia as direcoes de rotacao e de movimento
        rotation_direction.set(0.0, 0.0, 0.0)
        movement_direction.set(0.0, 0.0, 0.0)

        # modifica os vetores de direcao de acordo com as teclas pressionadas
        if pressed[K_LEFT]:
            rotation_direction.y = +1.0
        elif pressed[K_RIGHT]:
            rotation_direction.y = -1.0

        if pressed[K_UP]:
            rotation_direction.x = -1.0
        elif pressed[K_DOWN]:
            rotation_direction.x = +1.0

        if pressed[K_z]:
            rotation_direction.z = -1.0
        elif pressed[K_x]:
            rotation_direction.z = +1.0

        if pressed[K_q]:
            movement_direction.z = -1.0
        elif pressed[K_a]:
            movement_direction.z = +1.0

        # calcula a matriz de rotacao e multiplica pela matriz da camera
        rotation = rotation_direction * rotation_speed * time_passed_seconds
        rotation_matrix = Matrix44.xyz_rotation(*rotation)
        camera_matrix *= rotation_matrix

        # calcula o movimento e soma à translacao da matriz da camera
        heading = Vector3(camera_matrix.forward)
        movement = heading * movement_direction.z * movement_speed
        camera_matrix.translate += movement * time_passed_seconds

        # carrega a matriz da camera invertida na OpenGL
        glLoadMatrixd(camera_matrix.get_inverse().to_opengl())

        # a luz tambem deve ser transformada
        glLight(GL_LIGHT0, GL_POSITION, (0, 1.5, 1, 0))

        # renderiza o mapa
        map.render()

        # mostra a tela
        pygame.display.flip()

if __name__ == "__main__":
    run()