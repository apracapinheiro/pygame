# alguns imports que serão necessários posteriormente
from OpenGL.GL import *
from OpenGL.GLU import *


import pygame
import os.path


class Material(object):
    def __init__(self):
        self.name = ""
        self.texture_fname = None
        self.textude_id = None


class FaceGroup(object):
    def __init__(self):
        self.tri_indices = []
        self.material_name = ""


class Model3D(object):
    def __init__(self):
        self.vertices = []
        self.tex_coords = []
        self.normals = []
        self.materials = {}
        self.face_groups = []
        # ide da display list para uma renderizacao rapida
        self.display_list_id = None

    def read_obj(self, fname):
        current_face_group = None
        file_in = open(fname)

        for line in file_in:
            # faz o parse do comando e dos dados de cada linha
            words = line.split()
            command = words[0]
            data = words[1:]

            if command == 'mtllib':  # biblioteca de materiais
                model_path = os.path.split(fname)[0]
                mtllib_path = os.path.join(model_path, data[0])
                self.read_mtllib(mtllib_path)
            elif command == 'v':  # vertice
                x, y, z = data
                vertex = (float(x), float(y), float(z))
                self.vertices.append(vertex)
            elif command == 'vt':  # coordenada da textura
                s, t = data
                tex_coord = (float(s), float(t))
                self.tex_coords.append(tex_coord)
            elif command == 'vn':  # normal
                x, y, z = data
                normal = (float(x), float(y), float(z))
                self.normals.append(normal)
            elif command == 'usemtl':  # usar material
                current_face_group = FaceGroup()
                current_face_group.material_name = data[0]
                self.face_groups.append(current_face_group)
            elif command == 'f':
                assert len(data) == 3, "Somente triangulos sao suportados"

                # faz parse dos indices nas trincas
                for word in data:
                    vi, ti, ni = word.split('/')
                    indices = (int(vi) - 1, int(ti) - 1, int(ni) - 1)
                    current_face_group.tri_indices.append(indices)

        for material in self.materials.values():
            model_path = os.path.split(fname)[0]
            texture_path = os.path.join(model_path, material.texture_fname)
            texture_surface = pygame.image.load(texture_path)
            texture_data = pygame.image.tostring(texture_surface, 'RGB', True)

            material.textude_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, material.textude_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            width, height = texture_surface.get_rect().size
            gluBuild2DMipmaps(GL_TEXTURE_2D,
                              3,
                              width,
                              height,
                              GL_RGB,
                              GL_UNSIGNED_BYTE,
                              texture_data)

    def read_mtllib(self, mtl_fname):
        file_mtllib = open(mtl_fname)
        for line in file_mtllib:
            words = line.split()
            command = words[0]
            data = words[1:]

            if command == 'newmtl':
                material = Material()
                material.name = data[0]
                self.materials[data[0]] = material
            elif command == 'map_Kd':
                material.texture_fname = data[0]

    def draw(self):
        vertices = self.vertices
        tex_coords = self.tex_coords
        normals = self.normals

        for face_group in self.face_groups:
            material = self.materials[face_group.material_name]
            glBindTexture(GL_TEXTURE_2D, material.textude_id)

            glBegin(GL_TRIANGLES)
            for vi, ti, ni in face_group.tri_indices:
                glTexCoord2fv(tex_coords[ti])
                glNormal3fv(normals[ni])
                glVertex3fv(vertices[vi])
            glEnd()

    def draw_quick(self):
        if self.display_list_id is None:
            self.display_list_id = glGenLists(1)
            glNewList(self.display_list_id, GL_COMPILE)
            self.draw()
            glEndList()

        glCallList(self.display_list_id)

    def __del__(self):
        # chamada quando o modelo for removido pelo Python
        self.free_resources()

    def free_resources(self):
        # apaga a display list e as texturas
        if self.display_list_id is not None:
            glDeleteLists(self.display_list_id, 1)
            self.display_list_id = None

        # apaga qualquer textura utilizada
        for material in self.materials.values():
            if material.textude_id is not None:
                glDeleteTextures(material.textude_id)

        # limpa todos os materiais
        self.materials.clear()

        # limpa as listas com dados da geometria
        del self.vertices[:]
        del self.tex_coords[:]
        del self.normals[:]
        del self.face_groups[:]
