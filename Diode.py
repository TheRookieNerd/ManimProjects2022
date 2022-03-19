from manim import *
from random import random, uniform
from itertools import cycle

class Atom(VGroup):

    def __init__(self, v, **kwargs):  # valence electrons
        super().__init__(**kwargs)

        self.Z = v
        if v == 3:
            color = GREEN_B
        else:
            color = "#eed9bd"

        nucleus = Circle(radius=0.15, color=color, fill_color=color, fill_opacity=0.5, stroke_width=1)
        if v == 4:
            nucleus.add(Text("Si").scale(0.25))
        else:
            nucleus.add(Text("B").scale(0.25))
        shell_radius = 0.5
        self.add(nucleus)
        directions = [UP, RIGHT, DOWN, LEFT]

        self.electrons = VGroup()
        clouds = VGroup()
        electron_config = {
            "radius": 0.05,
            "fill_opacity": 1,
            "fill_color": BLUE,
            "color": BLUE
        }
        hole_config = {
            "radius": 0.07,
            "fill_opacity": 0,
            "fill_color": RED,
            "color": RED,
            "stroke_width": 1
        }
        clouds_config = {
            "fill_opacity": 0.75,
            "stroke_width": 15
        }

        cycled = cycle(directions)
        next(cycled)

        # def hole_updater(hole, dt):
        def vibrate(elec, dt):
            nc = -nucleus.get_center() + elec.center
            r = np.array([nc[0] + uniform(-0.01, 0.01), nc[1] + uniform(-0.01, 0.01), 0])
            elec.move_to(r)

        def hole_updater(hole):

        for _ in range(4):
            if _ < v:
                nudge = next(cycled)
                elec = Circle(**electron_config).move_to(directions[_] * shell_radius).shift(nudge * 0.125)
                elec.center = elec.get_center()
                elec.add_updater(vibrate)
                self.electrons.add(elec)
                # print(nudge)
                self.add(elec)
                # cloud = Line(nucleus.get_center(), elec.get_center(), color=BLUE, **clouds_config).shift(nucleus.get_radius() * directions[_]).set_opacity(0.25)
                # self.add(cloud)
            else:
                hole = Circle(**hole_config).move_to(directions[_] * shell_radius).shift(UP * 0.125)
                # hole.add(hole_updater)
                self.add(hole)
                # cloud = Line(nucleus.get_center(), hole.get_center(), color=RED, **clouds_config).shift(nucleus.get_radius() * directions[_]).set_opacity(0.25)
                # self.add(cloud)


class Diode(Scene):
    def construct(self):
        shell_radius = 0.5
        shell = Circle(radius=shell_radius, color=GREY, stroke_width=1)

        grid = [np.array([x, y, 0]) for y in range(-2, 3) for x in range(-4, 5)]
        d = 0
        i = 0
        for _ in grid:
            self.add(shell.copy().shift(_))

        for _ in grid:
            if random() > 0.3:
                self.add(Atom(4).shift(_))
                i += 1
            else:
                self.add(Atom(3).shift(_))
                d += 1

        # for _ i
        self.wait(4)
