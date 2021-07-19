#!/usr/bin/env python3
from src.shaders.Shader import Shader

# Base 3D Object Shader

class LumiShader:

    vertex_code = """
        attribute vec3 position;
        attribute vec2 texture_coord;
        attribute vec3 normals;

        varying vec2 out_texture;
        varying vec3 out_frag_pos;
        varying vec3 out_normals;

        uniform mat4 u_model;
        uniform mat4 u_view;
        uniform mat4 u_projection;

        void main(){ 
            gl_Position  = u_projection * u_view * u_model * vec4(position, 1.0);
            out_texture  = vec2(texture_coord);
            out_frag_pos = vec3(u_model * vec4(position, 1.0));
            out_normals  = normals;
        }
    """

    fragment_code = """
        // Phong Model Parameters
        vec3 light_pos       = vec3(40.0, 40.0, 0.0); 
        vec3 light_intensity = vec3(1.0);
        vec3 viewer_pos      = vec3(0.0, 10.0, 0.0);

        uniform vec3 mtl_ka = vec3(0.3);
        uniform vec3 mtl_kd = vec3(0.8);
        uniform vec3 mtl_ks = vec3(0.9);
        uniform float mtl_ns = 1.0;

        uniform vec4  u_color;
        uniform float u_color_mix;
        
        varying vec3 out_frag_pos;
        varying vec3 out_normals;
        varying vec2 out_texture;
        uniform sampler2D samplerTexture;
        
        void main(){
            // Loading texture
            vec4 texel = texture2D(samplerTexture, out_texture);
            vec4 color = (u_color_mix*vec4(1.0)) + ((1.0-u_color_mix)*texel);

            // Ambient Intensitiy
            vec3 Ia = mtl_ka * light_intensity;

            // Diffuse Reflection Intensitiy
            vec3 N   = normalize(out_normals);
            vec3 L   = normalize(light_pos - out_frag_pos);
            float NL = max(0.0, dot(N,L));
            vec3 Id  =  mtl_kd * NL * light_intensity;

            // Specular Reflection Intensity
            vec3 V = normalize(viewer_pos - out_frag_pos);
            vec3 R = reflect(-L, N);
            float NH = pow(max(0.0, dot(V,R)), mtl_ns);
            vec3 Is = mtl_ks * NH * light_intensity;

            gl_FragColor = vec4(vec3((Ia+Id+Is)*color),1.0); // Phong
            gl_FragColor = vec4(vec3((Ia)*color),1.0); // Ambient
            // gl_FragColor = vec4(vec3((Id)*color),1.0); // Diffuse
            // gl_FragColor = vec4(vec3((Is)*color),1.0); // Specular
        }
    """

    def compile():
        shader_program = Shader(LumiShader.vertex_code, LumiShader.fragment_code)
        shader_program.compile()
        return shader_program