#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
import glm
import glfw

from src.objects.GameObject2 import GameObject
from src.shaders.Shader import Shader
from src.shaders.BaseShader import vertex_code, fragment_code

class Wooden(GameObject):
    """
    Implementa o céu utilizando o método Sky Sphere.
    """

    shader_program  = Shader(vertex_code, fragment_code)
    shader_offsets  = { "pos": 0, "tex": 0, "norm": 0 }
    shader_model    = None # Positions, Textures, Normals and Faces

    object_paths = { "folder": "./assets/wooden/", "mtl": "wooden.mtl", "obj": "wooden.obj" }
    object_materials = []
    object_textures = []
    object_textures_ids = []


    def get_model():
        """Exported function used by Game Controller"""
        return GameObject._get_model_helper(Wooden)


    def __init__(self, position=(0,0,0), scale=(0,0,0), rotate=(0,0,0)) -> None:
        super().__init__(position, scale, rotate)


    def logic(self, keys={}, buttons={}, objects={}) -> None:
        """
        Interface que permite a criação de lógicas a serem executadas pelo objeto
        a cada iteração do jogo. Recebe os estados dos inputs.
        """
        #pass
    # Uncomment to allow Jiro positioning
        delta_mov = 0.01
        delta_rot = 0.05
        self.position[0] += keys.get(glfw.KEY_J, {"action": 0})["action"] * delta_mov
        self.position[0] -= keys.get(glfw.KEY_L, {"action": 0})["action"] * delta_mov
        self.position[2] += keys.get(glfw.KEY_I, {"action": 0})["action"] * delta_mov
        self.position[2] -= keys.get(glfw.KEY_K, {"action": 0})["action"] * delta_mov
        self.position[1] += keys.get(glfw.KEY_UP, {"action": 0})["action"] * delta_mov
        self.position[1] -= keys.get(glfw.KEY_DOWN, {"action": 0})["action"] * delta_mov
        self.rotate[1] += keys.get(glfw.KEY_U, {"action": 0})["action"] * delta_rot
        self.rotate[1] -= keys.get(glfw.KEY_O, {"action": 0})["action"] * delta_rot
        self._configure_gl_variables()
        print("Position", self.position, " --- Rotate: ", self.rotate[1])