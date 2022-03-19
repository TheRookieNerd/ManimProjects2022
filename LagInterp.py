from manim import *
from functools import partial


class LagInterp(MovingCameraScene):
    def construct(self):
        title = Tex(r"Lagrange Interpolation").scale(1.5)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        # self.camera.frame.scale(1.5)
        ax = Axes(
            x_range=[-1, 7, 1],
            y_range=[-18, 10, 2],
            y_length=14,
            x_axis_config={
                "include_tip": False
            },
            y_axis_config={
                "include_tip": False
            }
        ).add_coordinates().shift(DOWN * 4 + LEFT * 0.75)
        # ax = NumberPlane().add_coordinates()
        self.play(Create(ax))
        self.wait()
        colors_list = [YELLOW, GREEN, BLUE, PINK]

        ip_pts = [
            (0, 3), (1, 5), (3.5, 1), (5, 3)
        ]
        scale_fac = 0.65
        eqns1 = VGroup(
            MathTex("f(x) =").scale(1 / scale_fac),
            MathTex("3\\,\\dfrac{(x-1)(x-3.5)(x-5)}{(0-1)(0-3.5)(0-5)}", color=colors_list[0]),
            MathTex("+"),
            MathTex("5\\,\\dfrac{(x-0)(x-3.5)(x-5)}{(1-0)(1-3.5)(1-5)}", color=colors_list[1]),
            MathTex("+"),
        ).scale(scale_fac).arrange_submobjects(direction=RIGHT).to_edge(UP, buff=1)
        eqns2 = VGroup(
            MathTex("1\\,\\dfrac{(x-0)(x-1)(x-5)}{(3.5-0)(3.5-1)(3.5-5)}", color=colors_list[2]),
            MathTex("+"),
            MathTex("3\\,\\dfrac{(x-0)(x-1)(x-3.5)}{(5-0)(5-1)(5-3.5)}", color=colors_list[3])
        ).scale(scale_fac).arrange_submobjects(direction=RIGHT).next_to(eqns1[3], direction=DOWN)
        f1 = MathTex("f_1 = ").scale(0.75).next_to(eqns1[1], direction=LEFT, buff=0.1)
        eqns = VGroup(eqns1, eqns2).add_background_rectangle()

        pts = [ax.c2p(pt[0], pt[1]) for pt in ip_pts]
        # pts = [RIGHT * pt[0] + UP * pt[1] for pt in [
        #     (0, 2), (1, 1), (1.5, 4), (3, 0.5)
        # ]]
        dots = VGroup()

        for pt, c in zip(pts, colors_list):
            dot = Dot(pt, color=c).scale(0.75)
            dot.add(Circle(radius=0.1, stroke_width=1, color=c).move_to(dot))
            dots.add(dot)

        def demolagfn1(x):
            nr = 1
            for pt2 in ip_pts:
                if not np.array_equal(ip_pts[0], pt2):
                    nr *= x - pt2[0]
            return nr

        def demolagfn2(x):
            nr, dr = 1, 1
            for pt2 in ip_pts:
                if not np.array_equal(ip_pts[0], pt2):
                    nr *= x - pt2[0]
                    dr *= ip_pts[0][0] - pt2[0]
            return (nr / dr)

        def nthlagfn(x, pt):
            nr, dr = 1, 1
            for pt2 in ip_pts:
                if not np.array_equal(pt, pt2):
                    nr *= x - pt2[0]
                    dr *= pt[0] - pt2[0]
            return pt[1] * (nr / dr)

        functions = {f'fn{i}': partial(nthlagfn, pt=k) for i, k in enumerate(ip_pts)}
        l_plots = VGroup()
        for i, c in enumerate(colors_list):
            l_plots.add(ax.plot(functions[f"fn{i}"], x_range=[-0.1, 5.5], color=c))

        def lagfn(x):
            # self.ls=[]
            l = 0
            for pt in ip_pts:
                nr, dr = 1, 1
                for pt2 in ip_pts:
                    if not np.array_equal(pt, pt2):
                        nr *= x - pt2[0]
                        dr *= pt[0] - pt2[0]

                l += pt[1] * (nr / dr)
            return l

        rev_colors_list = colors_list[-1::-1]
        interp = ax.plot(lagfn, x_range=[-0.5, 5.5]).set_color(color=rev_colors_list)

        scale_fac = 0.2
        l_plots_cpy = VGroup()
        for i, l in enumerate(l_plots.copy()):
            l_plots_cpy.add(l)
            if i != 3:
                l_plots_cpy.add(MathTex("+").scale(3))

        l_plots_cpy.add(MathTex("=").scale(3), interp.copy())
        l_plots_cpy.arrange_submobjects(buff=0.75).to_edge(UP).scale(scale_fac).shift(RIGHT * 0.25)
        # self.add(l_plots_cpy)

        coords = VGroup(*[MathTex(pt) for pt in ip_pts])
        vert_lines = VGroup(*[ax.get_vertical_line(ax.c2p(pt[0], pt[1]), color=WHITE, stroke_width=3).rotate(180 * DEGREES) for pt in ip_pts[1:]])
        circ = VGroup(*[Circle(radius=0.1, stroke_width=2, color=WHITE).move_to(vert_lines[_].get_end()) for _ in range(3)])

        for dot, coord in zip(dots, coords):
            coord.next_to(dot)
            self.play(FadeIn(dot), Write(coord))
        self.wait()
        self.play(FadeOut(coords, title))

        l_plots.save_state()
        for i, l in enumerate(l_plots):
            self.play(
                Create(l),
                run_time=2
            )
            self.wait()
            if i == 0:
                ddots = VGroup(*[Dot(vert_lines[_].get_end()).scale(0.1) for _ in range(3)])
                self.play(*[Flash(ddot) for ddot in ddots])
            self.play(l.animate.fade(0.8))

        self.play(*[ReplacementTransform(i, j) for i, j in zip(l_plots, l_plots_cpy[0:-2:2])])
        self.play(FadeIn(l_plots_cpy[1::2], l_plots_cpy[-1]))
        self.wait()
        self.play(FadeOut(l_plots_cpy))
        l_plots.restore()

        demo_fn1 = ax.plot(demolagfn1, color=YELLOW_C)
        demo_fn2 = ax.plot(demolagfn2, color=YELLOW_D)
        self.camera.frame.save_state()

        self.play(Create(demo_fn1), Write(f1), Write(eqns1[1][0][1:18]), run_time=2)

        self.play(self.camera.frame.animate.shift(DOWN * 9))
        intercept = ax.i2gp(0, demo_fn1)
        c = DecimalNumber(demolagfn1(0)).next_to(intercept)
        self.play(Write(c))

        self.play(
            self.camera.frame.animate.restore(),
            c.animate.next_to(eqns1[1][0][18], direction=DOWN, buff=0.1).scale(0.65).set_color(YELLOW),
            Write(eqns1[1][0][18]),
            ReplacementTransform(demo_fn1, demo_fn2),
            run_time=3
        )
        temp = VGroup(
            MathTex("1").scale(0.75).next_to(ax.c2p(0, 1), direction=LEFT, buff=0.2),
            MathTex("3").scale(0.75).next_to(ax.c2p(0, 3), direction=LEFT, buff=0.2)
        )
        self.play(FadeIn(temp[0]))
        self.play(Flash(temp[0]))
        self.wait()
        self.play(ReplacementTransform(c, eqns1[1][0][19:]))
        self.wait()

        self.play(
            ReplacementTransform(demo_fn2, l_plots[0]),
            Write(eqns1[1][0][0]),
            ReplacementTransform(temp[0], temp[1]),
            run_time=2
        )

        self.wait()
        self.play(
            ShowPassingFlash(
                l_plots[0].copy().set_color(RED),
                run_time=2,
                time_width=0.5
            )
        )
        self.play(FadeOut(temp[1]))

        for l, c in zip(vert_lines, circ):
            self.play(Create(l), Create(c), run_time=0.5)
        self.wait()
        self.play(FadeOut(circ, vert_lines))
        self.wait()

        self.play(l_plots[0].animate.fade(0.95), FadeOut(f1))
        for l, eqn in zip(l_plots[1:], [eqns1[-2], eqns2[0], eqns2[-1]]):
            self.play(
                Create(l),
                Write(eqn),
                run_time=2
            )
            self.wait()
            self.play(l.animate.fade(0.8))
        # self.add(l_plots[1:], interp)
        # l_plots.fade(0.8)
        self.play(
            Create(interp),
            *[Write(mob) for mob in [eqns1[0], eqns1[2], eqns1[-1], eqns2[1]]]
        )
        self.wait()
        self.play(*[FadeOut(mobj) for mobj in self.mobjects])
