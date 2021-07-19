#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
import glm
import glfw

from src.objects.GameObject2 import GameObject
from src.shaders.LumiShader import LumiShader


class Bakugo(GameObject):
    """
    Implementa o céu utilizando o método Sky Sphere.
    """

    shader_name     = LumiShader
    shader_program  = None
    shader_offsets  = { "pos": 0, "tex": 0, "norm": 0 }
    shader_model    = None # Positions, Textures, Normals and Faces

    object_paths = { "folder": "./assets/bakugo/", "mtl": "bakugo.mtl", "obj": "bakugo.obj" }
    object_materials = []
    object_textures = []
    object_textures_ids = []


    def get_model():
        """Exported function used by Game Controller"""
        return GameObject._get_model_helper(Bakugo)


    def __init__(self, position=(0,0,0), scale=(0,0,0), rotate=(0,0,0)) -> None:
        super().__init__(position, scale, rotate)


    def logic(self, keys={}, buttons={}, objects={}) -> None:
        """
        Interface que permite a criação de lógicas a serem executadas pelo objeto
        a cada iteração do jogo. Recebe os estados dos inputs.
        """
        pass
        