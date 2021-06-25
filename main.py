#!/usr/bin/env python3

from src.GameController import GameController

from src.objects.GameObject import GameObject

def main():

    scene_scheme = [
        {
            "type": GameObject,
            "items": [
                { "position":(.0,.0,.0), "scale":(1, 1, 1), "rotate":(.0, 0., 0.0) },
                { "position":(4.5,-2.0,4.5), "scale":(.3, .3, .3), "rotate":(.0, 0., 0.0) },
            ] 
        },
    ]

    # Atualizar glm para 1.1.8
    game = GameController(title="T2 Computer Graphics", width=650, height=650, scheme=scene_scheme)
    game.start()



if __name__ == '__main__':
    main()