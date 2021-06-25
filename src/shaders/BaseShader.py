#!/usr/bin/env python3

# Base 3D Object Shader

vertex_code = """
    attribute vec3 position;
    attribute vec2 texture_coord;
    attribute vec3 normals;

    varying vec2 out_texture;
    varying vec3 out_fragPos;
    varying vec3 out_normals;

    uniform mat4 u_model;
    uniform mat4 u_view;
    uniform mat4 u_projection;

    void main(){ 
        gl_Position = u_projection * u_view * u_model * vec4(position, 1.0);
        out_texture = vec2(texture_coord);
        out_fragPos = vec3(u_model * vec4(position, 1.0));
        out_normals  = vec3(u_model * vec4(normals, 1.0));
    }
"""

fragment_code = """
    uniform vec4  u_color;
    uniform float u_color_mix;

    varying vec2 out_texture;
    uniform sampler2D samplerTexture;
    
    void main(){
        vec4 texture = texture2D(samplerTexture, out_texture);
        gl_FragColor = (u_color_mix * u_color) + ((1.0-u_color_mix)*texture) + vec4(1.0, 0.0, 0.0, 1.0);
    }
"""