from manim import *


class Power(Scene):
    def construct(self):
        a = Axes()
        f = a.get_graph(lambda x: np.sin(x))
        self.add(a, f)
