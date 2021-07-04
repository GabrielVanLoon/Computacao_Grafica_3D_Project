#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
import glm

from src.shaders.Shader import Shader
from src.shaders.BaseShader import vertex_code, fragment_code
from src.helpers.loader import load_model_from_file


class GameObject:
    """
    Abstração básica de um objeto que compõe a cena do jogo (Ex: jogador, obstaculo, fundo).
    Possui  os atributos e métodos comuns a todos. Assume a forma de um quadrado se desenhado
    em tela.

    A criação do programa de Shader e declaração dos vértices é feita apenas uma vez por meio
    de atributos e métodos estáticos (pertencentes à classe).
    """

    shader_program  = Shader(vertex_code, fragment_code)
    shader_offsets  = { "pos": 0, "tex": 0, "norm": 0 } 
    shader_model    = None # Positions, Textures, Normals and Faces

    object_model = "./assets/cube/cube.obj"
    object_material = ""
    object_textures = ["./assets/cube/cube.jpg"]
    object_textures_ids = []
    
    
    def get_model():
        """
        Carrega e retorna os vertices, texels e vetores normais de um arquivo .obj e retorna
        os valores para serem usados pelo GameController.
        """
        if GameObject.shader_model == None:
            print("Loading object model: ", GameObject.object_model)
            GameObject.shader_model = load_model_from_file(GameObject.object_model)
        return GameObject.shader_model


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


    def configure_hitbox(self) -> None:
        """
        Permite que certor objetos tenham um objeto hitbox configurado e instânciado
        na propriedade self.object_hitbox.
        """
        pass
    

    def draw(self, view_matrix, projection_matrix):
        """
        Assume que o shader do objeto atual já foi ativado e realiza os desenhos na tela. 
        Aplica a matriz model para posicionar o objeto no mundo segundo os parâmetros 
        de posição, rotação e tamanho do objeto.
        """
        # Prepare the model transformation matrix
        model_matrix = np.array(self._generate_model_matrix(), np.float32)

        # Send MVP Matrix to shader
        GameObject.shader_program.set4fMatrix('u_model', model_matrix)
        GameObject.shader_program.set4fMatrix('u_view', view_matrix)
        GameObject.shader_program.set4fMatrix('u_projection', projection_matrix)
        
        # Active the texture
        GameObject.shader_program.set4Float('u_color', [0.0, 0.0, 0.0, 1.0])
        GameObject.shader_program.setFloat('u_color_mix', 0.0)
        glBindTexture(GL_TEXTURE_2D, GameObject.object_textures_ids[0])

        # Draw object steps
        glDrawArrays(GL_TRIANGLES, self.shader_offsets["pos"], 3*len(self.shader_model['faces']))
    
    
    def logic(self, keys={}, buttons={}, objects={}) -> None:
        """
        Interface que permite a criação de lógicas a serem executadas pelo objeto
        a cada iteração do jogo. Recebe os estados dos inputs.
        """
        pass
