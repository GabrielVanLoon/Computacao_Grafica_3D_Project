#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
import glm
import glfw

from src.objects.GameObject2 import GameObject
from src.shaders.Shader import Shader
from src.shaders.BaseShader import vertex_code, fragment_code

class Yorozu(GameObject):
    """
    Implementa o céu utilizando o método Sky Sphere.
    """

    shader_program  = Shader(vertex_code, fragment_code)
    shader_offsets  = { "pos": 0, "tex": 0, "norm": 0 }
    shader_model    = None # Positions, Textures, Normals and Faces

    object_paths = { "folder": "./assets/yorozu/", "mtl": "yorozu.mtl", "obj": "yorozu.obj" }
    object_materials = []
    object_textures = []
    object_textures_ids = []

    subscribe_keys = [glfw.KEY_J, glfw.KEY_K, glfw.KEY_L, glfw.KEY_I, glfw.KEY_U, glfw.KEY_O, glfw.KEY_UP, glfw.KEY_DOWN]


    def get_model():
        """Exported function used by Game Controller"""
        return GameObject._get_model_helper(Yorozu)


    def __init__(self, position=(0,0,0), scale=(0,0,0), rotate=(0,0,0)) -> None:
        super().__init__(position, scale, rotate)


    def logic(self, keys={}, buttons={}, objects={}) -> None:
        """
        Interface que permite a criação de lógicas a serem executadas pelo objeto
        a cada iteração do jogo. Recebe os estados dos inputs.
        """
        pass 
