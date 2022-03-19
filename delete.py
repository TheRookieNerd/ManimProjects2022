from manim import *


class Test(Scene):
    def construct(self):
        line = Arrow(ORIGIN, UP)
        line.t = 0
        theta = 0
        p = 10
        f = 1
        phase = 0
        self.add(Text(str(p)).shift(LEFT))
        self.add(Dot())

        def updater(line, dt):
            line.t += dt
            scale_factor = (np.cos((p / 2 * theta - phase * 120 * DEGREES) + (f * line.t - phase * 120 * DEGREES))
                            + np.cos((p / 2 * theta - phase * 120 * DEGREES) - (f * line.t - phase * 120 * DEGREES))) / 2
            nl = Arrow(ORIGIN, UP * scale_factor)
            line.become(nl)

        line.add_updater(updater)
        self.add(line)
        self.wait(4)
