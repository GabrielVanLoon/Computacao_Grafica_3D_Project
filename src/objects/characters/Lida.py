#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
import glm
import glfw

from src.objects.GameObject2 import GameObject
from src.shaders.BaseShader import BaseShader


class Lida(GameObject):
    """
    Implementa o céu utilizando o método Sky Sphere.
    """

    shader_name     = BaseShader
    shader_program  = None
    shader_offsets  = { "pos": 0, "tex": 0, "norm": 0 }
    shader_model    = None # Positions, Textures, Normals and Faces

    object_paths = { "folder": "./assets/lida/", "mtl": "lida.mtl", "obj": "lida.obj" }
    object_materials = []
    object_textures = []
    object_textures_ids = []

    subscribe_keys = [glfw.KEY_J, glfw.KEY_K, glfw.KEY_L, glfw.KEY_I, glfw.KEY_U, glfw.KEY_O, glfw.KEY_UP, glfw.KEY_DOWN]


    def get_model():
        """Exported function used by Game Controller"""
        return GameObject._get_model_helper(Lida)


    def __init__(self, position=(0,0,0), scale=(0,0,0), rotate=(0,0,0)) -> None:
        super().__init__(position, scale, rotate)

        self.u_time = 0.0
        self.xyz_reference = position


    def logic(self, keys={}, buttons={}, objects={}) -> None:
        """
        Interface que permite a criação de lógicas a serem executadas pelo objeto
        a cada iteração do jogo. Recebe os estados dos inputs.
        """
        self.u_time += 0.0005
        self._gl_rotate[1] += self.u_time

        # self._gl_translate[0] = self.xyz_reference[0] + 7.0*np.cos(self.u_time)
        # self._gl_translate[2] = self.xyz_reference[2] + 7.0*np.sin(self.u_time)
