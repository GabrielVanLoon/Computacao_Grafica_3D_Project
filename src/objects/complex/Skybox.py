#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
import glm

from src.objects.GameObject import GameObject
from src.shaders.Shader import Shader
from src.shaders.BaseShader import vertex_code, fragment_code
from src.helpers.loader import load_model_from_file

class Skybox(GameObject):
    """
    Implementa o céu utilizando o método Sky Sphere.
    """

    shader_program  = Shader(vertex_code, fragment_code)
    shader_offsets  = { "pos": 0, "tex": 0, "norm": 0 }
    shader_model    = None # Positions, Textures, Normals and Faces

    object_model = "./assets/sky/sky.obj"
    object_material = ""
    object_textures = ["./assets/sky/animecloud.png"]
    object_textures_ids = []


    def get_model():
        """
        Carrega e retorna os vertices, texels e vetores normais de um arquivo .obj e retorna
        os valores para serem usados pelo GameController.
        """
        if Skybox.shader_model == None:
            print("Loading object model: ", Skybox.object_model)
            Skybox.shader_model = load_model_from_file(Skybox.object_model)
        return Skybox.shader_model


    def __init__(self, position=(0,0,0), scale=(0,0,0), rotate=(0,0,0)) -> None:
        super().__init__(position, scale, rotate)


    def draw(self, view_matrix, projection_matrix):
        """
        Assume que o shader do objeto atual já foi ativado e realiza os desenhos na tela. 
        Aplica a matriz model para posicionar o objeto no mundo segundo os parâmetros 
        de posição, rotação e tamanho do objeto.
        """
        # Prepare the model transformation matrix
        model_matrix = np.array(self._generate_model_matrix(), np.float32)

        # Send MVP Matrix to shader
        Skybox.shader_program.set4fMatrix('u_model', model_matrix)
        Skybox.shader_program.set4fMatrix('u_view', view_matrix)
        Skybox.shader_program.set4fMatrix('u_projection', projection_matrix)
        
        # Active the texture
        Skybox.shader_program.set4Float('u_color', [0.0, 0.0, 0.0, 1.0])
        Skybox.shader_program.setFloat('u_color_mix', 0.0)
        glBindTexture(GL_TEXTURE_2D, Skybox.object_textures_ids[0])

        # Draw object steps
        glDrawArrays(GL_TRIANGLES, self.shader_offsets["pos"], 3*len(self.shader_model['faces']))
    

    def logic(self, keys={}, buttons={}, objects={}) -> None:
        """
        Interface que permite a criação de lógicas a serem executadas pelo objeto
        a cada iteração do jogo. Recebe os estados dos inputs.
        """
        pass