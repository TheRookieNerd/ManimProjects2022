from manim import *


class Simpsons(MovingCameraScene):
    def func(self, u, v):
        return np.array([u, v, u**2 - v**2 + 2])

    def construct(self):

        title = Tex(r"Runge-Kutta $3^{rd}$ Order - A numerical method for solving ODE").to_edge(UP)
        diff_eqn = MathTex("\\dfrac{dy}{dx}=", "f(x,y) = ", "x^2-y^2").next_to(title, direction=DOWN).shift(LEFT * 4)
        init_text = MathTex("y(0)=0").next_to(diff_eqn, direction=DOWN).align_to(diff_eqn.get_left(), direction=LEFT).add_background_rectangle()
        self.play(Write(title))
        grid = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            background_line_style={
                # "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 1
            },
            faded_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            faded_line_ratio=2
        )
        grid.add_coordinates()
        self.play(Create(grid))
        title.add_background_rectangle()
        self.wait()
        self.play(Create(diff_eqn))
        self.wait()
        self.play(Create(init_text))
        self.wait()

        initial_condition = 0
        main_dot = Dot(ORIGIN, color=WHITE)
        pseudo_dot = Dot(ORIGIN, color=GREEN)

        def func(x, y):
            return x**2 - y**2

        slope_field = VGroup()
        x_rad = 7
        for i in list(range(-x_rad, x_rad + 1, 1)):
            for j in list(range(-x_rad, x_rad + 1, 1)):
                slope_line = Line(ORIGIN, RIGHT, color=YELLOW).scale(.5).rotate(np.arctan(func(i, j)))
                slope_line.move_to(np.array([i, j, 0]))
                slope_field.add(slope_line)

        slope_field.add_to_back()
        self.play(
            FadeOut(title, grid, init_text),
            diff_eqn.animate.move_to(title.get_center())
        )
        eqns = VGroup(
            # MathTex("\\int_{\\small{y_0}}^{\\small{y_0+k}}", " dy =", " \\int_{\\small{x_0}}^{\\small{x_0+h}} ", "f(x,y) dx")
            MathTex(
                "\\int\\limits_{y_0}^{y_0+k} \\kern-0.5em",
                "dy =",
                "\\int\\limits_{x_0}^{x_0+h} \\kern-0.75em",
                "f(x,y) dx"
            ),
            MathTex("k =", "\\int\\limits_{x_0}^{x_0+h} \\kern-0.75em f(x,y) dx")

        ).arrange_submobjects(direction=DOWN, buff=1).next_to(diff_eqn, direction=DOWN, buff=1)

        xbox1 = SurroundingRectangle(eqns[0][2][-2:])
        xbox2 = SurroundingRectangle(eqns[0][2][0:4])

        ybox1 = SurroundingRectangle(eqns[0][0][-2:])
        ybox2 = SurroundingRectangle(eqns[0][0][0:4])

        # self.play(TransformFromCopy(diff_eqn[:-1], VGroup(eqns[0][1], eqns[0][3])))
        # self.play(Write(eqns[0][0]), Write(eqns[0][2]))

        # self.play(Create(xbox1))
        # self.play(ReplacementTransform(xbox1, xbox2))
        # self.play(Uncreate(xbox2))
        # self.wait()

        # self.play(Create(ybox1))
        # self.play(ReplacementTransform(ybox1, ybox2))
        # self.play(Uncreate(ybox2))

        # self.wait()
        # self.play(TransformFromCopy(eqns[0][:2], eqns[1][0]))
        # self.wait()
        # self.play(TransformFromCopy(eqns[0][2:], eqns[1][1]))

        self.add(eqns)
        self.play(
            FadeOut(diff_eqn, eqns[0]),
            eqns[1].animate.to_corner(UL).scale(0.85)
        )

        simp = MathTex("= \\dfrac{h}{3}(f_0 + 4 f_1 + f_2)").scale(0.85).next_to(eqns[1])
        self.play(Write(simp))
        fs = VGroup(
            MathTex("f_0", "(x,", "?\\,\\,)"),
            MathTex("f_1", "(x,", "?\\,\\,)"),
            MathTex("f_2", "(x,", "?\\,\\,)"),
            MathTex("f_0", "(x_0,", "y_0)")
        ).arrange_submobjects(direction=DOWN, buff=1).next_to(simp, direction=DOWN, buff=0.5).scale(0.85)

        self.play(fs[:-1].animate.next_to(eqns[-1], direction=DOWN, buff=1))
        fs[-1].move_to(fs[0])
        # self.play(FadeOut(eqns[-1], fs[1:]))
        # self.play(self.camera.frame.animate.scale(0.65).move_to(UP + RIGHT * 2))
        ax = Axes(
            x_range=[-1, 6, 10],
            x_length=9,
            y_range=[-1, 7, 10],
            x_axis_config={
                "stroke_width": 4
            },
            y_axis_config={
                "stroke_width": 4
            }
        )
        labels = ax.get_axis_labels(x_label="x", y_label="y")

        def func(x):
            return 0.15 * (x)**2 + 2

        graph = ax.plot(func, x_range=[1, 5], color=BLUE)

        # self.add(ax, labels, graph)

        xs, ys, vert_lines, hor_lines = [VGroup() for _ in range(4)]
        for _ in range(1, 7, 2):
            xs.add(Dot(color=RED).move_to(ax.c2p(_, 0)))
            ys.add(Dot(color=GREEN).move_to(ax.c2p(0, func(_))))
            vert_lines.add(ax.get_vertical_line(ax.i2gp(_, graph), color=RED, stroke_width=2))
            hor_lines.add(ax.get_horizontal_line(ax.i2gp(_, graph), color=GREEN, stroke_width=2))

        xsw = VGroup(MathTex("x_0"), MathTex("x_0 + \\frac{h}{2}"), MathTex("x_0+h")).scale(0.75)
        for x, xw in zip(xs, xsw):
            xw.next_to(x, direction=DOWN)

        ysw = VGroup(MathTex("y_0"), MathTex("y_1"), MathTex("y_2")).scale(0.85)
        for y, yw in zip(ys, ysw):
            yw.next_to(y, direction=LEFT)

        axes_group = VGroup(ax, graph, labels, xs, xsw, ys, ysw, vert_lines, hor_lines).shift(DOWN + 0.8 * RIGHT).scale(0.85)

        self.play(Create(ax), Create(labels))
        self.play(
            AnimationGroup(*[FadeIn(x, xw) for x, xw in zip(xs, xsw)], lag_ratio=0.5)
        )
        self.play(FadeIn(ys[0], ysw[0]))
        self.play(VGroup(xs[0].copy(), ys[0].copy()).animate.move_to(fs[0]).scale(0.0001),
                  ReplacementTransform(fs[0], fs[-1]))

        self.play(Create(graph))

        anim_grp = AnimationGroup(lag_ratio=0.5)
        for vert_line, hor_line, y, yw in zip(vert_lines, hor_lines, ys, ysw):
            self.play(Create(vert_line), run_time=0.25)
            if yw != ysw[0]:
                self.play(Create(hor_line.rotate(180 * DEGREES)), FadeIn(yw, y), run_time=0.25)
            else:
                self.play(Create(hor_line.rotate(180 * DEGREES)), run_time=0.25)

        self.play(FadeOut(ys, ysw, graph, vert_lines, hor_lines))
        # self.add(xs, xsw, ys, ysw, vert_lines, hor_lines)

        def get_slope_mobject(pt, m):
            slope_obj = Line(ORIGIN, RIGHT, color=ORANGE, stroke_width=5).scale(.65).rotate(np.arctan(m))
            slope_obj.move_to(pt)
            return slope_obj

        m1, m2 = 0.2, 0.4
        h = 4
        init = ax.i2gp(1, graph)
        m1obj = get_slope_mobject(init, m1)
        self.add(m1obj)
        l1 = Line(init, ax.c2p(3, func(1) + (h / 2) * m1))
        self.add(l1, vert_lines)
