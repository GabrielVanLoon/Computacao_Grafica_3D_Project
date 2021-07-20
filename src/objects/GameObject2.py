#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
import glm

from src.objects.GameObject import GameObject
from src.shaders.Shader import Shader
from src.shaders.LumiShader import LumiShader
from src.helpers.loader import load_materials_from_file
from src.helpers.loader import get_textures_from_materials
from src.helpers.loader import load_model_from_file_and_mtl

class GameObject:
    """
    Abstração básica de um objeto que compõe a cena do jogo (Ex: jogador, obstaculo, fundo).
    Possui  os atributos e métodos comuns a todos. Assume a forma de um quadrado se desenhado
    em tela.

    A criação do programa de Shader e declaração dos vértices é feita apenas uma vez por meio
    de atributos e métodos estáticos (pertencentes à classe).
    """

    shader_name     = LumiShader
    shader_program  = None
    shader_offsets  = { "pos": 0, "tex": 0, "norm": 0 }
    shader_model    = None # Positions, Textures, Normals and Faces

    object_paths = { "folder": "./assets/sky/", "mtl": "sky.mtl", "obj": "sky.obj" } 
    object_materials = []
    object_textures = []
    object_textures_ids = []

    def _get_model_helper(ClassName):
        """
        Carrega os arquivos .obj e .mtl necessários para iniciar as variáveis de object_* que
        serão usadas pelo Game Controller. Também prepara as intruções a serem usadas nos Draws.
        """
        # Loading textures and illuminance values from .mtl
        ClassName.object_materials = load_materials_from_file(ClassName.object_paths["folder"] + ClassName.object_paths["mtl"])
        ClassName.object_textures = get_textures_from_materials(ClassName.object_materials, preffix_path=ClassName.object_paths["folder"])

        if ClassName.shader_model == None:
            print("Loading object model: ", ClassName.object_paths["folder"] + ClassName.object_paths["obj"])
            ClassName.shader_model = load_model_from_file_and_mtl(ClassName.object_paths["folder"] + ClassName.object_paths["obj"], ClassName.object_materials)
        return ClassName.shader_model


    def get_model():
        """Exported function used by Game Controller"""
        return GameObject._get_model_helper(GameObject)


    def __init__(self, position=(0,0,0), scale=(0,0,0), rotate=(0,0,0)) -> None:
        """
        Cria um objeto básico com as configurações de posicionamento informadas. a conversão
        da posição em pixels para coordenadas relativas é feita automaticamente.

        Parameters:
        -----------
        position: tripla de inteiros
            Representa a posição em pixels do objeto na janela
        scale: tripla de floats
            Representa o tamanho (width, height and depth) em pixels do objeto na janela
        rotate: tripla inteiro ou flutuante
            Representa o grau de rotação do objeto no eixo (x,y,z)
        """
        self.position = [position[0], position[1], position[2]]                 
        self.scale    = [scale[0], scale[1], scale[2]]
        self.rotate   = [rotate[0], rotate[1], rotate[2]]

        self._gl_scale     = [1.0, 1.0, 1.0]
        self._gl_rotate    = [0.0, 0.0, 0.0]
        self._gl_translate = [0.0, 0.0, 0.0]

        self._configure_gl_variables()


    def _configure_gl_variables(self):
        """
        Atualiza as variáveis utilizadas para renderização (__gl_*) baseado nos valores
        das variáveis públicas.
        """
        self._gl_translate = self.position
        self._gl_rotate    = self.rotate
        self._gl_scale     = self.scale
        return None


    def _generate_model_matrix(self, scale_first=False) -> list:
        """
        Calcula e retorna a matrix model para realizar as transformações no objeto
        """
        # Translate * Scale * Rotate
        model_matrix = glm.mat4(1.0)
        model_matrix = glm.rotate(model_matrix, glm.radians(self._gl_rotate[0]), glm.vec3(1.0, 0.0, 0.0))
        model_matrix = glm.rotate(model_matrix, glm.radians(self._gl_rotate[1]), glm.vec3(0.0, 1.0, 0.0))
        model_matrix = glm.rotate(model_matrix, glm.radians(self._gl_rotate[2]), glm.vec3(0.0, 0.0, 1.0))
        model_matrix = glm.scale(model_matrix, glm.vec3(self._gl_scale))
        model_matrix = glm.translate(model_matrix, glm.vec3(self._gl_translate)) 
        model_matrix = np.array(model_matrix).flatten()
        return  model_matrix


    def draw(self, view_matrix, projection_matrix):
        """
        Assume que o shader do objeto atual já foi ativado e realiza os desenhos na tela. 
        Aplica a matriz model para posicionar o objeto no mundo segundo os parâmetros 
        de posição, rotação e tamanho do objeto.
        """
        # Prepare the model transformation matrix
        model_matrix = np.array(self._generate_model_matrix(), np.float32)

        # Send MVP Matrix to shader
        self.__class__.shader_program.set4fMatrix('u_model', model_matrix)
        # self.__class__.shader_program.set4fMatrix('u_view', view_matrix)
        # self.__class__.shader_program.set4fMatrix('u_projection', projection_matrix)
        
        # Luminance (Phong Model) Configurations
        # self.__class__.shader_program.set3Float('light_pos', luminance['light_position'])
        # self.__class__.shader_program.set3Float('light_intensity', luminance['light_intensity'])
        # self.__class__.shader_program.set3Float('viewer_pos', luminance['viewer_position'])
            
        for draw in self.__class__.shader_model["draws"]:
            
            # Nothing to draw
            if draw["faces"] == 0 : continue
            
            # Config. Material Parameters
            self.__class__.shader_program.set3Float('mtl_ka', self.__class__.object_materials[draw["mat"]]["Ka"])
            self.__class__.shader_program.set3Float('mtl_kd', self.__class__.object_materials[draw["mat"]]["Kd"])
            self.__class__.shader_program.set3Float('mtl_ks', self.__class__.object_materials[draw["mat"]]["Ks"])
            self.__class__.shader_program.setFloat( 'mtl_ns', self.__class__.object_materials[draw["mat"]]["Ns"])

            # If is a texture material, active the texture and draw objects
            if draw["txt_index"] != None:
                self.__class__.shader_program.setFloat('u_color_mix', 0.0)
                glBindTexture(GL_TEXTURE_2D, self.__class__.object_textures_ids[draw["txt_index"]])
                glDrawArrays(GL_TRIANGLES, self.shader_offsets["pos"] + 3*draw["offset"], 3*draw["faces"])
            
            # Else draw white color solid objects :)
            else:
                self.__class__.shader_program.setFloat('u_color_mix', 1.0)
                glDrawArrays(GL_TRIANGLES, self.shader_offsets["pos"] + 3*draw["offset"], 3*draw["faces"])


    def logic(self, keys={}, buttons={}, objects={}) -> None:
        """
        Interface que permite a criação de lógicas a serem executadas pelo objeto
        a cada iteração do jogo. Recebe os estados dos inputs.
        """
        pass