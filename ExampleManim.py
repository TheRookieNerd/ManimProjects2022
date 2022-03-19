from manim import *


class Example(Scene):
    def construct(self):
        sq = Square()
        self.play(Create(sq))
        self.wait()
