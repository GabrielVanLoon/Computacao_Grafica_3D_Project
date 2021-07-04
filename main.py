#!/usr/bin/env python3

from src.GameController import GameController

from src.objects.GameObject import GameObject

from src.objects.scenario.Skybox import Skybox
from src.objects.scenario.Classroom import Classroom
from src.objects.scenario.Ichuraku import Ichiraku
from src.objects.scenario.Academy import Academy

from src.objects.characters.Uraraka import Uraraka
from src.objects.characters.Bakugo import Bakugo
from src.objects.characters.AllMight import AllMight
from src.objects.characters.Jiro import Jiro
from src.objects.characters.Midoryia import Midoryia

def main():

    scene_scheme = [
        {
            "type": GameObject,
            "items": [
                { "position":(.0,+1.0,.0), "scale":(1, 1, 1), "rotate":(.0, 0., 0.0) },
            ]
        },

        # Characters Objects
        {
            "type": Uraraka,
            "items": [
                { "position":(0.0,0.0,0.0), "scale":(1, 1, 1), "rotate":(0.0, 0.0, 0.0) },
            ]
        },
        {
            "type": Bakugo,
            "items": [
                { "position":(1.0,0.0,0.0), "scale":(1, 1, 1), "rotate":(0.0, 0.0, 0.0) },
            ]
        },
        {
            "type": AllMight,
            "items": [
                { "position":(2.0,0.0,0.0), "scale":(1, 1, 1), "rotate":(0.0, 0.0, 0.0) },
            ]
        },
        {
            "type": Jiro,
            "items": [
                { "position":(3.0,0.0,0.0), "scale":(1, 1, 1), "rotate":(0.0, 0.0, 0.0) },
            ]
        },
        {
            "type": Midoryia,
            "items": [
                { "position":(-1.0,0.0,0.0), "scale":(1, 1, 1), "rotate":(0.0, 0.0, 0.0) },
            ]
        },

        # Scenario Objects
        # {
        #     "type": Classroom,
        #     "items": [
        #         { "position":(0.0,-1.0,0.0), "scale":(.5, .5, .5), "rotate":(0.0, 0.0, 0.0) },
        #     ]
        # },
        {
            "type": Academy,
            "items": [
                { "position":(-20.0,-0.7,0.0), "scale":(5., 5., 5.), "rotate":(0.0, 90.0, 0.0) },
            ]
        },
        {
            "type": Ichiraku,
            "items": [
                { "position":(-5.0,0.0,-5.0), "scale":(1., 1., 1.), "rotate":(0.0, 90.0, 0.0) },
            ]
        },
        {
            "type": Skybox,
            "items": [
                { "position":(0.0,0.0,0.0), "scale":(1, 1, 1), "rotate":(0.0, 0.0, 0.0) },
            ]
        },
    ]

    # Atualizar glm para 1.1.8
    game = GameController(title="T2 Computer Graphics", width=1050, height=650, scheme=scene_scheme)
    game.start()



if __name__ == '__main__':
    main()