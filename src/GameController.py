#!/usr/bin/env python3
import glfw
import numpy as np
from OpenGL.GL import *
from PIL import Image
import glm

from src.objects.GameObject import GameObject
from src.objects.CameraObject import CameraObject

class GameController:
    """
    Classe principal que engloba todos os estados, objetos, controle de janela,
    inputs de usuário e loop principal da lógica do jogo.
    """


    def __init__(self, title="Computer Graphics 101", width=600, height=600, enable3D=False, scheme = []) -> None:
        """
        Set the program window configurations and other important variables
        """
        self.__glfw_window = False
        self.__glfw_title  = title
        self.__glfw_resolution  = (width, height)
        self.__glfw_enable3D = enable3D
        self.scheme = scheme
        self.__configure_window()
        
        self.__objects = []
        self.__vertices = []
        self.__textures = []
        self.__normals = []
        self.__buffer = None
        self.__solid_objects = []

        self.__glfw_keys = {}
        self.__glfw_observe_keys = [glfw.KEY_R, glfw.KEY_C, glfw.KEY_ESCAPE,
            glfw.KEY_A, glfw.KEY_D, glfw.KEY_W, glfw.KEY_S, glfw.KEY_LEFT_SHIFT, glfw.KEY_SPACE]
        self.__glfw_buttons = {}
        self.__glfw_cursor  = {"posx":  width//2, "posy": height//2}

        self.__camera = None

        self.__configure_vertexes_and_keys()
        self.__configure_objects()
        self.__configure_buffer()
        self.__configure_textures()


    def __configure_window(self) -> None:
        """
        Internal function with the GLFW window and context configurations
        """
        glfw.init()
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
        self.__glfw_window = glfw.create_window(self.__glfw_resolution[0], self.__glfw_resolution[1], self.__glfw_title, None, None)
        glfw.make_context_current(self.__glfw_window)

        # Register handlers
        glfw.set_key_callback(self.__glfw_window, self.__key_event_handler)
        glfw.set_mouse_button_callback(self.__glfw_window, self.__mouse_event_handler)
        glfw.set_cursor_pos_callback(self.__glfw_window, self.__cursor_event_handler)

        # Compile shaders of objects used in scene scheme
        for object in self.scheme:
            object["type"].shader_program.compile()


    def __configure_vertexes_and_keys(self) -> None:
        """
        Configure vertex configurations and subscribed keys
        """
        for object in self.scheme:
            # Update Object offset and save vertices in program buffer
            object["type"].shader_offsets["pos"] = len(self.__vertices)
            object["type"].shader_offsets["tex"] = len(self.__textures)
            object["type"].shader_offsets["norm"] = len(self.__normals)
            
            # Load model and append positions, textures and normals in arrays
            object_model = object["type"].get_model()
            
            for face in object_model['faces']:
                for vertice_id in face[0]:
                    self.__vertices.append(object_model['vertices'][vertice_id-1])
                for texture_id in face[1]:
                    self.__textures.append(object_model['texture'][texture_id-1])
                for normal_id in face[2]:
                    self.__normals .append(object_model['normals'][normal_id-1])

            # Configure observed keys
            if hasattr(object["type"], "subscribe_keys"):
                self.__glfw_observe_keys += object["type"].subscribe_keys


    def __configure_objects(self) -> None:
        """
        Start/Restart all objects used in the game
        """
        self.__objects = []
        self.__solid_objects = []

        # Create the Camera Object and set mouse position
        self.__camera = CameraObject(self.__glfw_resolution)

        for object in self.scheme:
            # Create all desired object items
            items = []
            for item in object["items"]:
                items.append(object["type"](position=item["position"], scale=item["scale"], rotate=item["rotate"]))

            # Append created items to objects
            self.__objects.append({"type": object["type"], "items": items })


    def __configure_buffer(self) -> None:
        """
        Instantiate a buffer in GPU and send the vertex data.
        """
        self.__vertices = np.array(self.__vertices, dtype=np.float32)
        self.__textures = np.array(self.__textures, dtype=np.float32)
        self.__normals  = np.array(self.__normals, dtype=np.float32)

        self.__buffer = glGenBuffers(3)

        glBindBuffer(GL_ARRAY_BUFFER, self.__buffer[0])
        glBufferData(GL_ARRAY_BUFFER, self.__vertices.nbytes, self.__vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, self.__buffer[1])
        glBufferData(GL_ARRAY_BUFFER, self.__textures.nbytes, self.__textures, GL_STATIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, self.__buffer[2])
        glBufferData(GL_ARRAY_BUFFER, self.__normals.nbytes, self.__normals, GL_STATIC_DRAW)


    def __configure_textures(self) -> None:
        """
        Instantiate and initialize all textures used by te objects
        """

        # Calc. the sum number of textures needed and generate them
        qtd_textures = 0
        for object in self.scheme:
            qtd_textures += len(object["type"].object_textures)

        # If no textures to create then exits
        if qtd_textures == 0:
            return 

        # Init all the textures
        texture_id = 1
        glGenTextures(qtd_textures)
        for object in self.scheme:
            for texture in object["type"].object_textures:
                # Texture Settings
                glBindTexture(GL_TEXTURE_2D, texture_id)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);	
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                # Load image and generate midmap
                image = Image.open(texture)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1))
                glGenerateMipmap(GL_TEXTURE_2D)
                # Set id and increment
                object["type"].object_textures_ids.append(texture_id)
                texture_id += 1


    def __key_event_handler(self, window, key, scancode, action, mods):
        """
        Manipula os eventos de teclados lidos pelo GLFW e salva as mudanças de estado 
        apenas das teclas de interesse para economizar memória não necessária
        """
        if key in self.__glfw_observe_keys:
            self.__glfw_keys[key] = { "action": action, "code": scancode, "mods": mods }


    def __mouse_event_handler(self, window, button, action, mods):
        """
        Manipula os eventos de mouse que, como são menores, não necessita de uma
        seleção tão aguçada de quais estados salvar
        """
        self.__glfw_buttons[button] = { "action": action, "mods": mods }


    def __cursor_event_handler(self, window, xpos, ypos):
        """Manipulação do cursor para controle da mira"""
        self.__glfw_cursor = {"xpos": xpos, "ypos": ypos }
    

    def start(self) -> None:
        """
        Start the game logic and graphic loop. Runs until the player close the window.
        """
        glfw.show_window(self.__glfw_window)
        glfw.set_cursor_pos(self.__glfw_window, self.__glfw_resolution[0]//2, self.__glfw_resolution[1]//2)
        glfw.set_input_mode(self.__glfw_window, glfw.CURSOR, glfw.CURSOR_DISABLED); 
        
        # Enable 3D mode
        glEnable(GL_DEPTH_TEST)

        # Enable color transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        while not glfw.window_should_close(self.__glfw_window):
            glfw.poll_events() 
            
            # Reset the screen with the white color
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
            glClearColor(1.0, 1.0, 1.0, 1.0)

            # If key R pressed restart the game, C resets the cursor
            if self.__glfw_keys.get(glfw.KEY_R, {"action": 0})["action"]:
                self.__configure_objects()
                glfw.set_cursor_pos(self.__glfw_window, self.__glfw_resolution[0]//2, self.__glfw_resolution[1]//2)
            
            # If C is pressed disable cursor, ESC return to normal
            if self.__glfw_keys.get(glfw.KEY_C, {"action": 0})["action"]:
                glfw.set_input_mode(self.__glfw_window, glfw.CURSOR, glfw.CURSOR_DISABLED); 
            elif self.__glfw_keys.get(glfw.KEY_ESCAPE, {"action": 0})["action"]:
                glfw.set_input_mode(self.__glfw_window, glfw.CURSOR, glfw.CURSOR_NORMAL)

            # Execute objects logics, if object is solid pass all solid objects to 
            # be used in the collision logics calculation
            self.__camera.logic(self.__glfw_keys,self.__glfw_buttons, self.__glfw_cursor)
            
            for object_group in reversed(self.__objects):
                for item in object_group["items"]:
                    item.logic(keys=self.__glfw_keys, buttons=self.__glfw_buttons)

            # Compute Camera view and projection matrix to be passed to objects draws
            view_matrix = self.__camera.get_view()
            projection_matrix = self.__camera.get_projection()

            # Foreach object group active the shader and draw items
            # Obs: Reversed because first groups have priority.
            for object_group in reversed(self.__objects):
                object_group["type"].shader_program.use(buffers=self.__buffer)
                for item in object_group["items"]:
                    item.draw(view_matrix=view_matrix, projection_matrix=projection_matrix)

            glfw.swap_buffers(self.__glfw_window)
        glfw.terminate()


if __name__ == '__main__':
    game = GameController(title="Testing Game Controller", width=1200, height=600, enable3D=False)
    game.start()