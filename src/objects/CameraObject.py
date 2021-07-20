#!/usr/bin/env python3
import numpy as np
import glm
import glfw


class CameraObject: 
    """
    Abstração da Camera responsável pela visão do usuário no mundo. Gera a matriz
    View e Projection para serem utilizados pelo Game Controller.
    """


    def __init__(self, window_resolution=(600,600)):
        """
        Start the camera in the default space posicion.
        """
        self.window_resolution = window_resolution

        self.camera_pos   = glm.vec3(0.0, 0.6, +10.0)   # Camera Position
        self.camera_front = glm.vec3(0.0, 0.0,  1.0)   # Look Direction
        self.camera_up    = glm.vec3(0.0, 1.0,  0.0)   # Up Vector (default)
        self.camera_speed = 0.05

        self.proj_fov     = 45.0
        self.proj_aspect  = window_resolution[0]/window_resolution[1]
        self.proj_near    = 0.1
        self.proj_far     = 1000.0

        self.__xlast = None
        self.__ylast = None
        self.__cursor_sensitivity = 0.3
        self.__yaw   = -90.0
        self.__pitch =  0.0

        self.__view_matrix = None
        self.__projection_matrix = None
        self.__time = 0.0

    
    def get_view(self):
        """Compute and return the current view matrix."""
        self.__view_matrix = glm.lookAt(self.camera_pos, self.camera_pos+self.camera_front, self.camera_up)
        return np.array(self.__view_matrix).flatten()

    
    def get_projection(self):
        """Compute and return the current projection matrix."""
        self.__projection_matrix = glm.perspective(glm.radians(self.proj_fov), self.proj_aspect, self.proj_near, self.proj_far)
        return np.array(self.__projection_matrix).flatten()

    
    def logic(self, keys={}, buttons={}, cursor={}, objects={}) -> None:
        """Movement and mouse logics of the camera"""

        old_camera_pos = glm.vec3(self.camera_pos)

        # Moving mouse using Yaw and Pitch
        xpos = cursor.get("xpos", None)
        ypos = cursor.get("ypos", None)

        if self.__xlast == None or self.__ylast == None:
            self.__xlast = xpos
            self.__ylast = ypos
            return None

        xdelta, self.__xlast  =  (xpos-self.__xlast), xpos 
        ydelta, self.__ylast  =  (self.__ylast-ypos), ypos      

        self.__yaw   += xdelta* self.__cursor_sensitivity
        self.__pitch += ydelta* self.__cursor_sensitivity
        self.__pitch =  min(max(self.__pitch, -60.0), 89.0) # [-60, 90] degress range

        front = glm.vec3()
        front.x = np.math.cos(glm.radians(self.__yaw)) * np.math.cos(glm.radians(self.__pitch))
        front.y = np.math.sin(glm.radians(self.__pitch))
        front.z = np.math.sin(glm.radians(self.__yaw)) * np.math.cos(glm.radians(self.__pitch))
        self.camera_front = glm.normalize(front)

        # Move around the world (Naive Implement)
        # self.camera_pos[0] += keys.get(glfw.KEY_A, {"action": 0})["action"] * self.camera_speed
        # self.camera_pos[0] -= keys.get(glfw.KEY_D, {"action": 0})["action"] * self.camera_speed
        # self.camera_pos[2] += keys.get(glfw.KEY_W, {"action": 0})["action"] * self.camera_speed
        # self.camera_pos[2] -= keys.get(glfw.KEY_S, {"action": 0})["action"] * self.camera_speed
        self.camera_pos[1] += keys.get(glfw.KEY_SPACE , {"action": 0})["action"] * self.camera_speed
        self.camera_pos[1] -= keys.get(glfw.KEY_LEFT_SHIFT, {"action": 0})["action"] * self.camera_speed

        # Move around like Minecraft :P 
        # - Y-axis same as naive with shift and space
        # - XZ-axis derived from camera direction without perturb y-axis
        if self.__view_matrix == None: return # Prevent crash in first run

        v_foward  = glm.normalize(glm.vec3(self.camera_front[0], 0.0, self.camera_front[2]))
        v_lateral = glm.normalize(glm.cross(self.camera_front, self.camera_up) * glm.vec3(1., 0., 1.))
        
        self.camera_pos += v_lateral * keys.get(glfw.KEY_D, {"action": 0})["action"] * self.camera_speed
        self.camera_pos -= v_lateral * keys.get(glfw.KEY_A, {"action": 0})["action"] * self.camera_speed
        self.camera_pos += v_foward * keys.get(glfw.KEY_W, {"action": 0})["action"] * self.camera_speed
        self.camera_pos -= v_foward * keys.get(glfw.KEY_S, {"action": 0})["action"] * self.camera_speed

        # Move restrictions
        # print(self.camera_pos)
        # if self.camera_pos[1] > 40.0 or self.camera_pos[1] < 0.5:
        #     self.camera_pos[1] = old_camera_pos[1]
        # if self.camera_pos[0] > 130.0 or self.camera_pos[0] < -130.0:
        #     self.camera_pos[0] = old_camera_pos[0]
        # if self.camera_pos[2] > 130.0 or self.camera_pos[2] < -130.0:
        #     self.camera_pos[2] = old_camera_pos[2]

        # Increase/Decrase camera angle with UP and DOWN Keys
        self.proj_fov -= 0.1 * keys.get(glfw.KEY_LEFT, {"action": 0})["action"]
        self.proj_fov += 0.1 * keys.get(glfw.KEY_RIGHT, {"action": 0})["action"]

        self.proj_fov = self.proj_fov if self.proj_fov < 89.0 else 89.0
        self.proj_fov = self.proj_fov if self.proj_fov > 15.0 else 15.0

        # Make camera rotate around cube (Activity 4)
        # self.camera_pos   = glm.vec3(10.0*np.cos(self.__time), 0.2, 10.0*np.sin(self.__time))
        # self.camera_front = -1.0 * self.camera_pos
        # self.__time      += 0.0005
        # return None