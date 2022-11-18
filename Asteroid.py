import random
import time

from pygame import Rect

import core
from pygame.math import Vector2



def setup():
    print("setup")
    core.fps = 60
    core.WINDOW_SIZE = [800, 800]
    core.memory("position", Vector2(400, 400))
    core.memory("speed", Vector2(0, -1))
    core.memory("direction", Vector2(0, -1))
    core.memory("projectile", [])
    core.memory("x", random.randint(0, 750))
    core.memory("y", random.randint(0, 750))
    core.memory("l", 50)
    core.memory("h", 50)
    core.memory("target", Rect(core.memory("x"), core.memory("y"), core.memory("l"), core.memory("h")))
    core.memory("score", 0)


def run():
    print("running")
    core.cleanScreen()

    #Déplacement
    core.memory("position", core.memory("position") + core.memory("speed"))

    #Contrôle
    if core.getKeyPressList("z"):
        core.memory("position", core.memory("position") + core.memory("speed")*2)
        a = core.memory("speed").angle_to(core.memory("direction"))
        b = core.memory("direction").cross(core.memory("speed"))

        if abs(a) > 1:
            if b < 0:
                core.memory("speed", core.memory("speed").rotate(3))
            if b > 0:
                core.memory("speed", core.memory("speed").rotate(-3))
     
    if core.getKeyReleaseList("z"):
        core.memory("position", core.memory("position") + core.memory("speed") * 0.6)

    if core.getKeyPressList("d"):
        core.memory("direction", core.memory("direction").rotate(4))

    if core.getKeyPressList("q"):
        core.memory("direction", core.memory("direction").rotate(-4))

    if core.memory("position").x < 0:
        core.memory("position").x = 800

    if core.memory("position").y < 0:
        core.memory("position").y = 800

    if core.memory("position").x > 800:
        core.memory("position").x = 0

    if core.memory("position").y > 800:
        core.memory("position").y = 0

    #Tir
    if core.getKeyPressList("SPACE"):
        if len(core.memory("projectile")) > 0:
            if time.time() - core.memory("projectile")[-1]["startTime"] > 0.2:
                p = core.memory("position")
                v = Vector2(core.memory("speed"))
                v.scale_to_length(core.memory("speed").length() + 10)
                r = 1
                c = (255, 255, 255)
                st = time.time()
                d = {"position": p, "vitesse": v, "color": c, "rayon": r, "startTime": st}
                core.memory("projectile").append(d)
        else :
            p = core.memory("position")
            v = Vector2(core.memory("speed"))
            v.scale_to_length(core.memory("speed").length() + 10)
            r = 1
            c = (255, 255, 255)
            st = time.time()
            d = {"position": p, "vitesse": v, "color": c, "rayon": r, "startTime": st}
            core.memory("projectile").append(d)

    for proj in core.memory("projectile"):
        core.Draw.circle(proj["color"], proj["position"], proj["rayon"])

    #DéplacementTir
    for proj in core.memory("projectile"):
        proj["position"] = proj["position"] + proj["vitesse"]

    #CleanTir
    for proj in core.memory("projectile"):
        if time.time() - proj["startTime"] > 0.8:
            core.memory("projectile").remove(proj)

    #Target
    core.Draw.rect((255,0,255),core.memory("target"))

    for proj in core.memory("projectile"):
        if core.memory("target").collidepoint(proj["position"].x, proj["position"].y):
            core.memory("projectile").remove(proj)
            core.memory("x", random.randint(0, 750))
            core.memory("y", random.randint(0, 750))
            core.memory("l", 50)
            core.memory("h", 50)
            core.memory("target", Rect(core.memory("x"), core.memory("y"), core.memory("l"), core.memory("h")))
            core.Draw.rect((255, 0, 255), core.memory("target"))
            core.memory("score", core.memory("score") + 1)



    core.Draw.text((255,255,255), "score :" + str(core.memory("score")), (20, 20))


    #Position et forme vaisseau
    x = core.memory("direction")
    x = x.rotate(90)
    x.scale_to_length(5)
    P1 = core.memory("position") + x

    y = Vector2(core.memory("direction"))
    y.scale_to_length(20)
    P2 = core.memory("position") + y

    z = core.memory("direction")
    z = z.rotate(-90)
    z.scale_to_length(5)
    P3 = core.memory("position") + z

    core.Draw.polygon((255,0,0), (P1, P2, P3))


core.main(setup, run)
