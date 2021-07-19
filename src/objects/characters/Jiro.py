#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
import glm
import glfw

from src.objects.GameObject2 import GameObject
from src.shaders.LumiShader import LumiShader


class Jiro(GameObject):
    """
    Implementa o céu utilizando o método Sky Sphere.
    """

    shader_name     = LumiShader
    shader_program  = None
    shader_offsets  = { "pos": 0, "tex": 0, "norm": 0 }
    shader_model    = None # Positions, Textures, Normals and Faces

    object_paths = { "folder": "./assets/jiro/", "mtl": "jiro.mtl", "obj": "jiro.obj" }
    object_materials = []
    object_textures = []
    object_textures_ids = []

    subscribe_keys = [glfw.KEY_J, glfw.KEY_K, glfw.KEY_L, glfw.KEY_I, glfw.KEY_U, glfw.KEY_O, glfw.KEY_UP, glfw.KEY_DOWN]


    def get_model():
        """Exported function used by Game Controller"""
        return GameObject._get_model_helper(Jiro)


    def __init__(self, position=(0,0,0), scale=(0,0,0), rotate=(0,0,0)) -> None:
        super().__init__(position, scale, rotate)


    def logic(self, keys={}, buttons={}, objects={}) -> None:
        """
        Interface que permite a criação de lógicas a serem executadas pelo objeto
        a cada iteração do jogo. Recebe os estados dos inputs.
        """
        pass 
        # Uncomment to allow Jiro positioning
        # delta_mov = 0.01
        # delta_rot = 0.05
        # self.position[0] += keys.get(glfw.KEY_J, {"action": 0})["action"] * delta_mov
        # self.position[0] -= keys.get(glfw.KEY_L, {"action": 0})["action"] * delta_mov
        # self.position[2] += keys.get(glfw.KEY_I, {"action": 0})["action"] * delta_mov
        # self.position[2] -= keys.get(glfw.KEY_K, {"action": 0})["action"] * delta_mov
        # self.position[1] += keys.get(glfw.KEY_UP, {"action": 0})["action"] * delta_mov
        # self.position[1] -= keys.get(glfw.KEY_DOWN, {"action": 0})["action"] * delta_mov
        # self.rotate[1] += keys.get(glfw.KEY_U, {"action": 0})["action"] * delta_rot
        # self.rotate[1] -= keys.get(glfw.KEY_O, {"action": 0})["action"] * delta_rot
        # self._configure_gl_variables()
        # print("Position", self.position, " --- Rotate: ", self.rotate[1])
