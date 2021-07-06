#!/usr/bin/env python3

from src.GameController import GameController

from src.objects.GameObject import GameObject

from src.objects.scenario.Skybox import Skybox
from src.objects.scenario.Classroom import Classroom
from src.objects.scenario.Ichuraku import Ichiraku
from src.objects.scenario.Academy import Academy
from src.objects.scenario.Grass import Grass

from src.objects.characters.Uraraka import Uraraka
from src.objects.characters.Bakugo import Bakugo
from src.objects.characters.AllMight import AllMight
from src.objects.characters.Jiro import Jiro
from src.objects.characters.Midoryia import Midoryia
from src.objects.characters.Kaminari import Kaminari
from src.objects.characters.Yorozu import Yorozu
from src.objects.characters.Mineta import Mineta
from src.objects.characters.Lida import Lida
from src.objects.characters.Totoro import Totoro
from src.objects.characters.Monokuma import Monokuma
from src.objects.characters.Evelynn import Evelynn


def main():


    scene_scheme = [
        # {
        #     "type": GameObject,
        #     "items": [{ "position":(0.0, 0.0, 0.0), "scale":(1, 1, 1), "rotate":(0.0, 0.0, 0.0) },]
        # },

        # Characters Objects
        {
            "type": Uraraka,
            "items": [ { "position":(4.86,3.53,-0.7), "scale":(1, 1, 1), "rotate":(0.0, -69.5, 0.0) },]
        },
        {
            "type": Bakugo,
            "items": [{ "position":(9.08,-0.12,47.83), "scale":(1, 1, 1), "rotate":(0.0, 0.0, 0.0) },]
        },
        {
            "type": AllMight,
            "items": [{ "position":(-5.26,4.28,-2.28), "scale":(1, 1, 1), "rotate":(0.0, 89.60, 0.0) },]
        },
        {
            "type": Jiro,
            "items": [ { "position":(2.76,0.31,1.76), "scale":(1, 1, 1), "rotate":(0.0, -93.34, 0.0) }, ]
        },
        {
            "type": Midoryia,
            "items": [{ "position":(-5.52,-0.16,-53.17), "scale":(1, 1, 1), "rotate":(0.0, -175.85, 0.0) },]
        },
        {
            "type": Kaminari,
            "items": [{ "position":(-6.78,0.055,-0.78), "scale":(1, 1, 1), "rotate":(0.0, 79.80, 0.0) },]
        },
        {
            "type": Yorozu,
            "items": [{ "position":(-3.69, 0.06,-3.33), "scale":(1, 1, 1), "rotate":(0.0, 78.15, 0.0) },]
        },
        {
            "type": Mineta,
            "items": [{ "position":(0.0, 0.0, 7.0), "scale":(1, 1, 1), "rotate":(0.0, 0.0, 0.0) },]
        },
        {
            "type": Lida,
            "items": [{ "position":(-18.0, 0.0, 0.0), "scale":(1, 1, 1), "rotate":(0.0, 0.0, 0.0) },]
        },
        {
            "type": Totoro,
            "items": [{ "position":(-2.47, 0.0, -1.56), "scale":(20, 20, 20), "rotate":(0.0, 105.2, 0.0) },]
        },
        {
            "type": Monokuma,
            "items": [{ "position":(49.86, 0.0, -45.33), "scale":(1, 1, 1), "rotate":(0.0, -96.3, 0.0) },]
        },
        {
            "type": Evelynn,
            "items": [{ "position":(-28.7, 0.0, -106.44), "scale":(1, 1, 1), "rotate":(0.0, -193.65, 0.0) },]
        },



        # Scenario Objects
        # {
        #     "type": Classroom,
        #     "items": [{ "position":(0.0,-1.0,0.0), "scale":(.5, .5, .5), "rotate":(0.0, 0.0, 0.0) },]
        # },
        {
            "type": Academy,
            "items": [{ "position":(-15.0,-0.7,0.0), "scale":(5., 5., 5.), "rotate":(0.0, 90.0, 0.0) }, ]
        },
        {
            "type": Ichiraku,
            "items": [{ "position":(-5.0,0.0,-5.0), "scale":(1., 1., 1.), "rotate":(0.0, 90.0, 0.0) }, ]
        },
        {
            "type": Grass,
            "items": [{ "position":(0.0,-0.2,-5.0), "scale":(1., 1., 1.), "rotate":(0.0, 0.0, 0.0) },]
        },
        {
            "type": Skybox,
            "items": [{ "position":(0.0,0.0,0.0), "scale":(1, 1, 1), "rotate":(0.0, 0.0, 0.0) },]
        },
    ]

    # Atualizar glm para 1.1.8
    game = GameController(title="T2 Computer Graphics", width=1050, height=650, scheme=scene_scheme)
    game.start()



if __name__ == '__main__':
    main()