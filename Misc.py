from manim import *


def four_swirls_function(point):
    x, y = point[:2]
    result = 1 * RIGHT + (x**2 - y**2) * UP
    result *= 0.05
    norm = get_norm(result)
    if norm == 0:
        return result
    # result *= 2 * sigmoid(norm) / norm
    return result


class RK(MovingCameraScene):
    def construct(self):

        title = Tex(r"Runge-Kutta $2^{nd}$ Order - A numerical method for solving ODE").to_edge(UP)
        diff_eqn = MathTex("\\dfrac{dy}{dx}=", "f(x,y) = ", "x^2-y^2").next_to(title, direction=DOWN).shift(LEFT * 4).add_background_rectangle(opacity=0.55)
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

        # coords = MathTex("(0,0)", "(1,0)", "(2,0)")
        # for k, l in zip(coords, [ORIGIN, RIGHT, RIGHT * 2]):
        #     k.move_to(l)

        # samples = VGroup(
        #     *[Line(ORIGIN, RIGHT, color=YELLOW)
        #       .scale(.5)
        #       .rotate(np.arctan(func(*x))).move_to(np.array([x[0], x[1], 0]))
        #       for x in [[0, 0], [1, 0], [2, 0]]
        #       ]
        # )
        # for coord, sample in zip(coords, samples):
        #     self.play(Write(coord))
        #     self.play(
        #         coord.animate.move_to(diff_eqn.get_center()).scale(.01)
        #     )

        #     self.wait(.5)
        #     self.play(TransformFromCopy(diff_eqn[2], sample))
        #     self.wait()

        slope_field.add_to_back()
        self.play(
            Create(slope_field),
            FadeOut(title, diff_eqn),
            grid.animate.fade(.7),
        )
        self.wait(.5)
        self.play(FadeIn(main_dot))
        self.wait()

        step_size = Tex(r"Step Size $h$ =").scale(0.9)
        step = DecimalNumber(1).scale(0.75).next_to(step_size)
        step_text = VGroup(step_size, step).add_background_rectangle()

        x_n = initial_condition
        x_np1 = 0
        y_n = 0
        y_np1 = 0
        h = 1
        yp_n = 0
        yp_np1 = 0
        m1 = func(x_n, y_n)
        m2 = 0
        x_nw, x_np1w, yp_nw, yp_np1w, y_nw, y_np1w, m1w, m2w, mpprod = [
            DecimalNumber(_).scale(0.75)
            for _ in [x_n, x_np1, yp_n, yp_np1, y_n, y_np1, m1, m2, m1 * h]
        ]

        xgrp1 = MathTex("x_{n+1}", " = ", "x_n + h ")
        xgrp2 = VGroup(MathTex("="), x_nw, MathTex("+"), step.copy(), MathTex("="), x_np1w)\
            .arrange_submobjects(direction=RIGHT)

        xgrp = VGroup(xgrp1, xgrp2).arrange_submobjects(direction=DOWN)
        xgrp2.next_to(xgrp1, direction=DOWN).align_to(xgrp1[1].get_left(), direction=LEFT)

        ypgrp1 = MathTex("\\overline{y_{n+1}}", " =", " y_n +  f(x_n, y_n)h ")
        ypgrp2 = VGroup(MathTex("="), yp_nw, MathTex("+"), mpprod, MathTex("="), yp_np1w)\
            .arrange_submobjects(direction=RIGHT)

        ypgrp = VGroup(ypgrp1, ypgrp2).arrange_submobjects(direction=DOWN)
        ypgrp2.next_to(ypgrp1, direction=DOWN, buff=0.5).align_to(ypgrp1[1].get_left(), direction=LEFT)

        ygrp1 = MathTex(
            "y_{n+1}",
            " =",
            " y_n +",
            "\\dfrac{f(x_n,y_n)+f(x_{n+1}, \\overline{y_{n+1}}) }{2}",
            "h"
        )
        ygrp1[-2].scale(0.75)
        ygrp1.arrange_submobjects(direction=RIGHT)

        frac = MathTex("\\dfrac{\\quad\\qquad+\\quad\\qquad}{2}").scale(0.75)
        m1w.next_to(frac[0][0], direction=LEFT)
        m2w.next_to(frac[0][0], direction=RIGHT)
        frac.add(m1w, m2w)
        ygrp2 = VGroup(MathTex("="), y_nw, MathTex("+"), frac, MathTex("="), y_np1w).arrange_submobjects(direction=RIGHT)

        ygrp = VGroup(ygrp1, ygrp2).arrange_submobjects(direction=DOWN)
        ygrp2.next_to(ygrp1, direction=DOWN, buff=0.5).align_to(ygrp1[1].get_left(), direction=LEFT)

        wordings = VGroup(step_text, xgrp, ypgrp, ygrp)\
            .scale(0.75).arrange_submobjects(direction=DOWN, buff=0.75).to_corner(UL).add_background_rectangle()
        for m in wordings[:-1]:
            m.align_to(wordings[-1].get_left(), direction=LEFT)

        # samples.fade(1)
        self.play(
            slope_field.animate.fade(0.7),
            init_text.animate.next_to(ORIGIN + RIGHT * 0.25, direction=UP)
        )
        self.play(FadeIn(wordings[0]))
        self.wait()
        for mob in [step_text, xgrp1, ypgrp1]:
            self.play(Create(mob))
            self.wait()
        # self.add(wordings)

        def get_demo_vect(dot):
            vec = Arrow(ORIGIN, RIGHT,
                        color=RED,
                        # stroke_width=15,
                        max_stroke_width_to_length_ratio=10
                        ).move_to(ORIGIN)
            vec.rotate(
                np.arctan(
                    func(dot.get_center()[0], dot.get_center()[1])
                ),
            ).shift(dot.get_center()).shift(vec.get_vector() / 2)
            return vec

        demo_vect = Arrow(ORIGIN, RIGHT, max_stroke_width_to_length_ratio=10)

        def update_vector(obj):
            obj.become(get_demo_vect(main_dot))

        demo_vect.add_updater(update_vector)

        self.play(FadeIn(demo_vect))
        self.add(demo_vect)
        # self.wait(2)

        path = VMobject(stroke_width=5, color=BLUE)
        path.set_points_as_corners([main_dot.get_center(), main_dot.get_center() + UP * 0.01])
        pseudo_path = VMobject(stroke_width=4, color=GREEN)
        pseudo_path.set_points_as_corners([pseudo_dot.get_center(), pseudo_dot.get_center() + UP * 0.01])

        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([main_dot.get_center()])
            path.become(previous_path)

        path.add_updater(update_path)
        self.add(path)

        def update_pseudo_path(pseudo_path):
            previous_path = pseudo_path.copy()
            previous_path.add_points_as_corners([pseudo_dot.get_center()])
            pseudo_path.become(previous_path)

        pseudo_path.add_updater(update_pseudo_path)
        self.add(pseudo_path)

        intervals = [4, 8, 17]
        widths = [1, .5, .25]

        next_point = ORIGIN
        main_dot.save_state()

        def get_slope_mobject(x, y):
            slope_obj = Line(ORIGIN, RIGHT, color=ORANGE, stroke_width=5).scale(.65).rotate(np.arctan(func(x, y)))
            slope_obj.move_to(np.array([x, y, 0]))
            return slope_obj

        for interval, width in zip(intervals, widths):
            if width == 1:
                self.play(FadeOut(init_text))
            self.play(step.animate.set_value(width))
            for i in range(interval):
                # self.camera.frame.save_state()
                # self.play(self.camera.frame.animate.scale(0.5).move_to(main_dot))

                m1 = func(x_n, y_n)
                m1w.set_value(m1)
                mpprod.set_value(m1 * width).next_to(ypgrp2[2], buff=0.1)
                m1_mobj = get_slope_mobject(x_n, y_n)
                m1w.next_to(frac[0][0], direction=LEFT)
                m2w.next_to(frac[0][0], direction=RIGHT)

                x_nw.set_value(x_n)
                yp_nw.set_value(yp_n)

                x_n += width
                x_np1w.set_value(x_n)

                yp_n = yp_n + m1 * width
                yp_np1w.set_value(yp_n)
                y_nw.set_value(y_n)

                if width == 1:
                    self.play(Write(xgrp2))
                    self.wait()
                    self.play(Write(ypgrp2))

                m2_mobj = get_slope_mobject(x_n, yp_n)
                pseudo_point = np.array([x_n, yp_n, 0])

                self.play(pseudo_dot.animate.move_to(pseudo_point))

                if width == 1:
                    self.play(Create(ygrp1), run_time=2)
                    self.play(Write(ygrp2[:-3]), Write(frac[0]))

                if width != 1:
                    frac.next_to(pseudo_point, direction=DOWN, buff=0.5)
                    m1w.next_to(frac[0][0], direction=LEFT)
                    m2w.next_to(frac[0][0], direction=RIGHT)
                    frac.add(VGroup(MathTex("="), y_np1w).arrange_submobjects(direction=RIGHT).next_to(frac, direction=RIGHT))

                self.play(Create(m1_mobj))
                self.play(Transform(m1_mobj, m1w.copy()))

                m2 = func(x_n, yp_n)
                m2w.set_value(m2)

                self.play(Create(m2_mobj))

                self.play(Transform(m2_mobj, m2w.copy()))

                # self.play(FadeOut(m1_mobj, m2_mobj))

                y_n = y_n + ((m1 + m2) / 2) * h
                y_np1w.set_value(y_n)
                if width != 1:
                    self.play(FadeIn(frac))
                if width == 1:
                    self.play(FadeIn(ygrp2[-2:]))

                # y_nw.set_value(y_n)

                print(x_n, y_n)
                next_point = np.array([x_n, y_n, 0])
                yp_n = y_n
                # if width == 1
                #     self.play(Write(ygrp2))

                # self.wait(1)
                self.play(main_dot.animate.move_to(next_point))

                pseudo_path.suspend_updating()
                self.play(
                    pseudo_dot.animate.move_to(next_point),
                    # FadeOut(pseudo_path)
                )
                self.remove(pseudo_path)
                if i != interval - 1:
                    pseudo_path = VMobject(stroke_width=3, color=GREEN)
                    pseudo_path.set_points_as_corners([pseudo_dot.get_center(), pseudo_dot.get_center() + UP * 0.01])
                    pseudo_path.add_updater(update_pseudo_path)
                    self.add(pseudo_path)

                if width == 1:
                    self.play(FadeOut(xgrp2, ypgrp2, ygrp2))
                if width != 1:
                    self.play(FadeOut(frac), run_time=0.25)
                    frac = MathTex("\\dfrac{\\quad\\qquad+\\quad\\qquad}{2}").scale(0.75 * 0.75)

                self.play(FadeOut(m1_mobj, m2_mobj), run_time=0.25)
                # self.play(self.camera.frame.animate.restore())
            if width == 1:
                self.play(FadeOut(xgrp, ypgrp, ygrp))
                self.remove(wordings[0])
                self.play(step_text.animate.to_corner(UL, buff=1).scale(1.5))
            path.suspend_updating()
            next_point = initial_condition
            self.play(
                main_dot.animate.restore(),
                FadeOut(path, pseudo_dot)
            )
            pseudo_dot.move_to(ORIGIN)
            self.remove(path)
            path = VMobject(stroke_width=5, color=BLUE)
            path.set_points_as_corners([main_dot.get_center(), main_dot.get_center() + UP * 0.01])
            path.add_updater(update_path)
            self.add(path)
            x_n, y_n, yp_n = 0, 0, 0

        self.wait(2)

        # self.play(
        #     FadeOut(*self.mobjects),
        #     run_time=2
        # )
