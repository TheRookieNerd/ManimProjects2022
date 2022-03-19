from manim import *
import math


class NR1D(MovingCameraScene):
    def measure_line(self, p1, p2):
        stroke = 2
        color = TEAL
        measure = Line(p1, p2, stroke_width=stroke, color=color)
        angle = PI / 2 + measure.get_angle()
        end_line = Line(LEFT, RIGHT, stroke_width=stroke, color=color).scale(0.1).rotate(angle)
        measure.add(
            end_line.move_to(measure.get_start()),
            end_line.copy().move_to(measure.get_end())
        )
        return measure

    def construct(self):
        ax = Axes(
            x_range=[-2.5, 2.5, 0.5],
            y_range=[-1, 10, 1],
            x_length=10,
            y_length=7,
            tips=False,
        ).add_coordinates()
        # self.add(ax)

        title = Text("Newton Raphson Method").scale(2)
        self.play(Write(title))
        self.play(FadeOut(title))
        obj = VGroup(
            Tex(r"Find the value of $x$ for which"),
            MathTex("x^2 =", "2")
        ).arrange_submobjects(direction=RIGHT)
        self.play(Write(obj))
        self.play(obj.animate.shift(UP * 2))

        self.play(Create(ax))
        self.add(obj.add_background_rectangle())

        def fn(x):
            return x**2

        parabola = ax.plot(fn, x_range=(-2.5, 2.5), color=BLUE, stroke_width=2)
        self.play(Create(parabola))
        a = 2  # x**2 = a

        req_y = ax.get_horizontal_line(ax.i2gp(2**0.5, parabola))
        req_x = ax.get_vertical_line(ax.i2gp((a / 1)**0.5, parabola), color=YELLOW).rotate(PI)
        req_x.add(Dot(req_x.get_end()))
        for mob in [req_y, req_x]:
            self.play(Create(mob))
        self.wait()
        qmark = MathTex("?").next_to(ax.c2p(2**0.5, 0), direction=UL, buff=0.1)
        self.play(Write(qmark))
        for mob in [req_y, req_x, qmark]:
            self.play(FadeOut(mob))

        self.play(
            self.camera.frame.animate.scale(0.75).move_to(ax.c2p(2, 2.25)),
            ax.animate.fade(0.7)
        )
        x = 0.5
        x0_num_prev = DecimalNumber(x, color=YELLOW).scale(0.4).next_to(ax.c2p(0.5, 0), direction=UR, buff=0.05)
        self.play(Write(x0_num_prev))
        x0_num = x0_num_prev

        for i in range(4):
            slope = ax.slope_of_tangent(x, parabola)
            c = fn(x) - slope * x
            tgt = ax.plot(lambda x: slope * x + c, x_range=(x - 2, x + 2), color=RED, stroke_width=2)
            # self.add(tgt)
            delx = (a - fn(x)) / slope
            x0 = ax.get_vertical_line(ax.i2gp(x, parabola))
            dely = DecimalNumber(a - tgt.underlying_function(x), num_decimal_places=3, color=GREEN)

            #########
            xw = MathTex("x")
            xw.add(Integer(i).scale(0.4).next_to(xw, direction=DR, buff=0.01))
            xgrp = VGroup(xw, MathTex("="), DecimalNumber(x).scale(0.8)).scale(0.75).arrange_submobjects(buff=0.1)  # .next_to(self.camera.frame.get_corner(UR), direction=DL)

            fxw = MathTex("f(\\,\\,\\,\\,)")
            fxw.add(xw.copy().scale(1.25).next_to(fxw[0][1], buff=0.01))
            fxgrp = VGroup(fxw, MathTex("="), DecimalNumber(fn(x)).scale(0.8)).scale(0.75).arrange_submobjects(buff=0.1)  # .next_to(xgrp, direction=DOWN)

            fdxw = MathTex("f'(\\,\\,\\,\\,)")
            fdxw.add(xw.copy().scale(1.25).next_to(fdxw[0][2], buff=0.01))
            fdxw.add(MathTex("= 2x").next_to(fdxw[-1]))
            fdxgrp = VGroup(fdxw, MathTex("="), DecimalNumber(2 * x).scale(0.8)).scale(0.75).arrange_submobjects(buff=0.1)  # .next_to(xgrp, direction=DOWN)

            # fxfdxgrp = VGroup(fxgrp, fdxgrp).arrange_submobjects(buff=0.5)

            delygrp_word = VGroup(MathTex("\\Delta y =  2 - "), fxw.copy(), MathTex("="), dely.copy().scale(0.8)).scale(0.75).arrange_submobjects(buff=0.1)  # .next_to(fxgrp, direction=DOWN)

            x1w = MathTex("x")
            x1w.add(Integer(i + 1).scale(0.4).next_to(x1w, direction=DR, buff=0.01))
            delxgrp_word = VGroup(
                MathTex("\\Delta x"),
                MathTex(
                    "=",
                    "\\dfrac{1}{f'(\\,\\,\\,\\,)}",
                    "\\Delta y"
                )
            ).scale(0.75).arrange_submobjects(buff=0.1)  # .next_to(fdxgrp, direction=DOWN)

            # x1grp = VGroup(
            #     x1w,
            #     MathTex("="),
            #     xw.copy().scale(1.35),
            #     MathTex(
            #         "+",
            #         "\\dfrac{1}{f'(\\,\\,\\,\\,)}",
            #         "\\big( y - f(\\,\\,\\,\\,) \\big)"
            #     ),
            # ).scale(0.75).arrange_submobjects(buff=0.1)  # .next_to(fdxgrp, direction=DOWN)
            delxgrp_word.add(
                xw.copy().next_to(delxgrp_word[1][1][4], buff=0.01),
                # xw.copy().next_to(x1grp[3][2][4], buff=0.01)
            )
            x1grp = VGroup(
                x1w,
                MathTex("="),
                xw.copy().scale(1.35),
                MathTex(
                    "+",
                    "\\Delta x",
                    "="
                ),
                DecimalNumber(x + delx, color=YELLOW).scale(0.8)

            ).scale(0.75).arrange_submobjects(buff=0.1)  # .next_to(fdxgrp, direction=DOWN)

            wordings = VGroup(xgrp, fxgrp, delygrp_word, fdxgrp, delxgrp_word, x1grp)\
                .arrange_submobjects(direction=DOWN).scale(0.75).next_to(self.camera.frame.get_right(), direction=LEFT, buff=1).add_background_rectangle()
            #########
            self.play(FadeIn(wordings[0]))

            y0 = ax.get_horizontal_line(ax.i2gp(x, parabola)).rotate(PI)
            # self.play(Create(y0))
            xp = x + delx
            tgt_cpy_x_range = sorted((x, xp))
            tgt_cpy = ax.plot(lambda x: slope * (x) + c, x_range=tgt_cpy_x_range, color=RED, stroke_width=2)  # used later

            y1 = ax.get_horizontal_line(ax.i2gp(xp, tgt)).rotate(PI)
            # self.play(Create(y1))

            dely_measure = self.measure_line(ax.c2p(0, a), ax.c2p(0, tgt.underlying_function(x))).shift(LEFT * 0.6)
            delygrp = MathTex("\\Delta y", color=GREEN)\
                .scale(0.5).next_to(dely_measure, direction=LEFT, buff=0.05)

            # self.play(Create(dely_measure), Write(delygrp))

            x1 = ax.get_vertical_line(ax.i2gp(xp, tgt))
            delx_measure = self.measure_line(ax.c2p(x, 0), ax.c2p(xp, 0)).shift(DOWN)

            delxgrp = MathTex("\\Delta x", color=GREEN)\
                .scale(0.5).next_to(delx_measure, direction=UP, buff=0.05)

            x = xp
            # self.add(x1)
            # self.play(Create(x1.rotate(180 * DEGREES)))
            # self.play(Create(delx_measure), Write(delxgrp))

            for l in [
                [xgrp, x0],
                [y0], [fxgrp],
                [dely_measure], [delygrp_word, delygrp],
                [fdxgrp], [tgt],
                [y1],
                [delxgrp_word],

            ]:
                self.play(*[Create(m) for m in l])
                self.wait()

            # print(x, x - delx)

            self.play(TransformFromCopy(dely_measure, tgt_cpy))
            self.play(TransformFromCopy(tgt_cpy, delx_measure))
            for l in [
                [delxgrp], [x1grp], [x1.rotate(180 * DEGREES)]
            ]:
                self.play(*[Create(m) for m in l])
                self.wait()

            x0_num_prev = x0_num
            if i % 2 == 0:
                direction = UL
            else:
                direction = UR
            # if i % 3 == 0 and i != 0:
            #     self.play(self.camera.frame.animate.scale(0.65))
            x0_num = DecimalNumber(x, num_decimal_places=3, color=YELLOW).scale(0.4).next_to(x1.get_end(), direction=direction, buff=0.075)
            x0_marker = Line(UP, DOWN, color=YELLOW, stroke_width=1).scale(0.1).move_to(ax.c2p(x, 0))
            x0_num.add(x0_marker)

            self.play(Write(x0_num))
            self.play(FadeOut(tgt, x1, y1, x0, y0, x0_num_prev, dely_measure, delygrp, delx_measure, delxgrp, wordings, tgt_cpy))


class TwoDApprox(MovingCameraScene):
    def get_transposed_matrix_transformation(self, transposed_matrix):
        transposed_matrix = np.array(transposed_matrix)
        if transposed_matrix.shape == (2, 2):
            new_matrix = np.identity(3)
            new_matrix[: 2, : 2] = transposed_matrix
            transposed_matrix = new_matrix
        elif transposed_matrix.shape != (3, 3):
            raise Exception("Matrix has bad dimensions")
        return lambda point: np.dot(point, transposed_matrix)

    def get_piece_movement(self, pieces):
        start = VGroup(*pieces)
        target = VGroup(*[mob.target for mob in pieces])
        return Transform(start, target, lag_ratio=0)

    def get_vector_movement(self, func):
        for v in self.moving_vectors:
            v.target = Vector(func(v.get_end()), color=v.get_color())
            norm = get_norm(v.target.get_end())
            if norm < 0.1:
                v.target.get_tip().scale_in_place(norm)
            # v.add_updater(lambda x: x.move_to(self.origin_tracker, aligned_edge=v.get_end()))
        return self.get_piece_movement(self.moving_vectors)

    def apply_function(self, nonlin_function, jacobian, added_anims=[], **kwargs):
        if "run_time" not in kwargs:
            kwargs["run_time"] = 3
        anims = [
            ApplyPointwiseFunction(nonlin_function, t_mob)
            for t_mob in self.transformable_mobjects
        ] + [
            self.get_vector_movement(jacobian),
        ] + added_anims
        self.play(*anims, **kwargs)
        # self.add(*[self.moving_vectors])

    def get_local_lines(self, grid):
        zoom_point = self.zoom_point
        x_axis = grid.get_x_axis()
        y_axis = grid.get_y_axis()
        x_lines = VGroup(*[
            Line(x_axis.get_start() + LEFT, x_axis.get_end() + RIGHT, stroke_color=BLUE_D, stroke_width=.02).move_to(zoom_point).shift(i * UP)
            for i in list(np.arange(-.1, .11, .01))
            if i != 0.0
        ])
        y_lines = VGroup(*[
            Line(y_axis.get_start() + DOWN, y_axis.get_end() + UP, stroke_color=BLUE_D, stroke_width=.02).move_to(zoom_point).shift(i * RIGHT)
            for i in list(np.arange(-.1, .11, .01))
            if i != 0.0
        ])
        return x_lines, y_lines

    #----------------------------------------------------------------------------------------------------------------------
    def construct(self):
        self.zoom_point = UR
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
        # grid = NumberPlane()
        self.add(grid)
        x_axis = grid.get_x_axis()
        y_axis = grid.get_y_axis()
        x_lines, y_lines = self.get_local_lines(grid)
        bg_xlines = x_lines.copy().fade(.75)
        bg_ylines = y_lines.copy().fade(.75)
        bg_lines = VGroup(bg_xlines, bg_ylines)
        grid.add_to_back(x_lines, y_lines)
        origin_tracker = self.origin_tracker = Dot(self.zoom_point).scale(.0000000000001)
        grid.add(origin_tracker)

        self.transformable_mobjects = [grid]

        dx_vec, dy_vec = [Arrow(self.zoom_point, self.zoom_point + .01 * RIGHT, color=GREEN_C, stroke_width=3),
                          Arrow(self.zoom_point, self.zoom_point + .01 * UP, color=RED_C, stroke_width=3)]

        dx_vec_ghost, dy_vec_ghost = [dx_vec.copy().fade(0.7).add_updater(lambda x: x.put_start_and_end_on(origin_tracker.get_center(), origin_tracker.get_center() + .01 * RIGHT)),
                                      dy_vec.copy().fade(0.7).add_updater(lambda x: x.put_start_and_end_on(origin_tracker.get_center(), origin_tracker.get_center() + .01 * UP))]

        bg_lines = VGroup(*[Line(x_axis.get_start(), x_axis.get_end(), stroke_color=LIGHT_GREY, stroke_width=.015),
                            Line(y_axis.get_start(), y_axis.get_end(), stroke_color=LIGHT_GREY, stroke_width=.015)]).add_updater(lambda x: x.move_to(origin_tracker.get_center()))
        bg_lines.add_updater(lambda x: x.move_to(origin_tracker.get_center()))
        self.moving_vectors = []  # [Vector(UR, stroke_width=4, max_tip_length_to_length_ratio=0.15)]
        grid.add(dx_vec, dy_vec, *self.moving_vectors)
        # grid.add(Arrow(ORIGIN, UL))
        ghost_grid = grid.copy().fade(1)
        self.add(ghost_grid)
        self.play(Create(grid, lag_ratio=0.1))  # , *[Create(vec) for vec in self.moving_vectors])

        # self.add_to_back(ghost_grid)
        # self.wait(2)
        mat = MathTex("\\begin{bmatrix}f_1\\\\f_2\\end{bmatrix}= \\begin{bmatrix}\\sin x_2 + x_1 \\\\ \\cos(x_1) + x_2\\end{bmatrix}").add_background_rectangle().to_corner(UL)
        jac = MathTex("\\begin{bmatrix}\\small{\\partial f_1 / \\partial x} & \\small{\\partial f_1 / \\partial y}\\\\ \\small{\\partial f_2 / \\partial x} & \\small{\\partial f_2 / \\partial y} \\end{bmatrix}").add_background_rectangle()
        jac_num = MathTex("\\begin{bmatrix}1 & 0.53\\\\ 0.68 & 1 \\end{bmatrix}").add_background_rectangle()

        self.play(Create(mat))
        self.wait(2)
        # self.setup()
        grid.save_state()
        # self.play(Write(mat))
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.animate.apply_function(
                lambda p: p
                + np.array(
                    [
                        0.5 * (np.sin(2 * p[1]) + p[0]),
                        0.5 * (np.cos(2 * p[0]) + p[1]),
                        0,
                    ]
                )
            ),
            run_time=3,
        )
        self.wait(2)
        self.play(grid.animate.restore())
        self.play(FadeOut(mat))
        self.wait()
        self.play(
            self.camera.frame.animate.move_to(self.zoom_point),
            run_time=2
        )
        x_label, y_label, = [
            Tex("$\\partial x$").next_to(dx_vec, direction=UP, buff=.01).scale(.005)
            .add_updater(lambda x:x.next_to(dx_vec_ghost, direction=UP, buff=.0005)),
            Tex("$\\partial y$").next_to(dy_vec, direction=LEFT, buff=.01).scale(.005)
            .add_updater(lambda x:x.next_to(dy_vec_ghost, direction=LEFT, buff=.0005))
        ]
        x_label, y_label = [Tex("$\\partial x$").move_to(self.zoom_point).scale(.1),
                            Tex("$\\partial y$").move_to(self.zoom_point).scale(.1)]
        zoomin = Text("Zooming in 100 times on (1,1)").add_background_rectangle()
        self.play(Create(zoomin))
        self.wait()
        # self.add(zoomin)
        self.play(
            self.camera.frame.animate.scale(.01).move_to(self.zoom_point),
            # self.camera.frame.animate,
            grid.background_lines.animate.fade(1),
            * [FadeIn(mobj) for mobj in [dx_vec_ghost, dy_vec_ghost, bg_lines]],  # x_label, y_label
            FadeOut(zoomin),
            run_time=3
        )
        self.add(bg_lines)
        self.wait()
        # self.play(WiggleOutThenIn(bg_lines))
        self.camera.frame.add_updater(lambda x: x.move_to(origin_tracker))
        self.add(self.camera.frame)
        jac.scale(.01)
        jac_num.scale(.01)
        jac.move_to(self.zoom_point + .025 * UL)
        jac_num.move_to(jac.get_center())

        grid.save_state()
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.animate.apply_function(
                lambda p: p
                + np.array(
                    [
                        np.sin(p[1]),
                        np.sin(p[0]),
                        0,
                    ]
                )
            ),
            run_time=3,
        )
        self.wait(2)

        self.play(grid.animate.restore())

        self.play(FadeIn(jac))
        self.wait()
        self.play(ReplacementTransform(jac, jac_num))
        jac_num.add_updater(lambda x: x.move_to(origin_tracker.get_center() + .025 * UL))
        self.add(jac_num)
        self.wait()

        self.play(
            grid.animate.apply_function(
                lambda p: p
                + np.array(
                    [
                        np.sin(p[1]),
                        np.sin(p[0]),
                        0,
                    ]
                )
            ),
            run_time=3,
        )
        # self.apply_function(
        #     lambda p: p + np.array([
        #         p[0] + np.sin(p[1]),
        #         p[1] + np.cos(p[0]),
        #         0,
        #     ]),
        #     self.get_transposed_matrix_transformation([[1, 1], [1, 1]]),
        # )

        self.wait()


class NR2Dtitle1(Scene):
    def construct(self):
        func = VGroup(
            MathTex("f_1(x_1,x_2) = \\sin x_2 + x_1", "=-1"),
            MathTex("f_2(x_1, x_2)= \\cos x_1 + x_2", "=1")
        ).arrange_submobjects(direction=DOWN).shift(UP)

        func_mat = MathTex("F(X)", " = A").next_to(func, direction=DOWN, buff=0.5)
        self.play(Write(func))

        obj = Tex(r"For what values of $x_1$ and $x_2$ does the system become [-1, 1]").next_to(func_mat, direction=DOWN, buff=0.5)
        self.play(Write(obj))
        self.wait()

        self.play(TransformFromCopy(VGroup(func[0][0], func[1][0]), func_mat[0]))
        self.play(TransformFromCopy(VGroup(func[0][1], func[1][1]), func_mat[1]))
        self.wait()


class NR2Dtitle2(Scene):
    def construct(self):
        func = VGroup(
            MathTex("f_1(x_1,x_2) = \\sin x_2 + x_1"),
            MathTex("f_2(x_1, x_2)= \\cos x_1 + x_2")
        ).arrange_submobjects(direction=DOWN).shift(2 * DOWN + 3 * LEFT)
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
        self.play(Create(grid, lag_ratio=0.1), run_time=2)
        self.wait()

        self.add(grid)
        # self.play(Write(func))
        self.wait()

        func.add_background_rectangle()
        ghost_grid = grid.copy().fade(0.8)
        self.add(ghost_grid)
        grid.save_state()
        grid.prepare_for_nonlinear_transform()

        self.play(
            grid.animate.apply_function(
                lambda p: p
                + np.array(
                    [
                        0.5 * (np.sin(2 * p[1]) + p[0]),
                        0.5 * (np.cos(2 * p[0]) + p[1]),
                        0,
                    ]
                )
            ),
            run_time=3,
        )
        self.wait()

        A = Dot(UL, color=YELLOW)
        A_mat = Matrix([[-1], [1]]).next_to(A, direction=UR).add_background_rectangle()
        Q_mat = Matrix([["?"], ["?"]]).scale(1.5).add_background_rectangle()
        # A.add(A_mat)
        # self.play(Write(A))
        # self.play(Create(A_mat))
        # self.play(FadeOut(A_mat))
        # grid.add(A)
        self.wait()
        # self.play(grid.animate.restore(), FadeOut(A))
        # self.play(Create(Q_mat))
        self.wait()


class NR2D1(Scene):
    def construct(self):
        x1, x2 = 1, 1
        a = [-1, 1]
        # a = [0, 0]
        for i in range(6):
            F = [
                np.sin(x2) + x1,
                np.cos(x1) + x2
            ]

            jac = [
                [1, np.cos(x2)],
                [-np.sin(x1), 1]
            ]

            jacmat = Matrix([
                [1, round(np.cos(x2), 2)],
                [round(-np.sin(x1), 2), 1]
            ])
            # self.add(jacmat)
            jacinv = np.linalg.inv(jac)
            delynum = [[x1 - x2] for x1, x2 in zip(a, F)]

            [[dx1], [dx2]] = np.matmul(jacinv, delynum)

            X_n = Matrix([[round(x1, 2)], [round(x2, 2)]])
            xw = MathTex("X")
            xw.add(Integer(i).scale(0.4).next_to(xw, direction=DR, buff=0.01))
            xgrp = VGroup(
                xw,
                MathTex("="),
                X_n
            ).arrange_submobjects(buff=0.1)

            Fbox = Square().add(MathTex("F(X)"))
            Fxn = MathTex("F(\\,\\,\\,\\,\\,\\,\\,) = ")
            Fxn.add(xw.copy().next_to(Fxn[0][0]))
            find_fx = VGroup(
                xgrp.copy(),
                Arrow(ORIGIN, RIGHT).scale(2),
                Fbox,
                Arrow(ORIGIN, RIGHT).scale(2),
                VGroup(
                    Fxn,
                    Matrix([
                        [round(np.sin(x2) + x1, 2)],
                        [round(np.cos(x1) + x2, 2)]
                    ])
                ).arrange_submobjects(direction=RIGHT)
            ).arrange_submobjects(direction=RIGHT)
            for _ in find_fx:
                self.play(Create(_))

            self.wait(2)
            self.play(FadeOut(find_fx))
            x1 = x1 + dx1
            x2 = x2 + dx2
            print(x1, x2)
            # self.add(nr2d1)

            X_nplus1 = Matrix([[round(x1, 2)], [round(x2, 2)]])

            delyw = MathTex("\\Delta Y")

            dely = Matrix([
                [round(delynum[0][0], 2)],
                [round(delynum[1][0], 2)]]
            ).shift(DOWN * 2.5 + RIGHT * 5)
            # ).arrange_submobjects(buff=0.1).scale(0.75).next_to(ORIGIN).add_background_rectangle()

            jacinvw = MathTex("\\bf J^{-1} \\bf").next_to(delyw, direction=LEFT)
            jacinvmat = Matrix([
                [1, round(np.cos(x2), 2)],
                [round(-np.sin(x1), 2), 1]
            ]).add(MathTex("^{-1}").shift(UP + RIGHT * 1.95)).next_to(dely, direction=LEFT)

            delxw = MathTex("\\Delta X", "=").next_to(jacinvw, direction=LEFT)

            # self.play(FadeOut(dely))
            delx = VGroup(
                Matrix([
                    [round(dx1, 2)],
                    [round(dx2, 2)]
                ]),
                MathTex("=")
            ).arrange_submobjects(buff=0.1).next_to(jacinvmat, direction=LEFT)
            # ).arrange_submobjects(buff=0.1).scale(0.75).next_to(delyvec).add_background_rectangle()
            matgrp = VGroup(delx, jacinvmat, dely).arrange_submobjects(direction=RIGHT).add_background_rectangle()
            matgrpw = VGroup(delxw, jacinvw, delyw).arrange_submobjects(direction=RIGHT, buff=0.25)\
                .next_to(matgrp, direction=UP).add_background_rectangle()  # .align_to(matgrp.get_right(), direction=RIGHT)

            self.play(FadeIn(matgrpw[0], delyw))

            self.add(matgrp[0])

            self.play(Create(dely))
            self.wait(2)

            self.play(Write(jacinvw))

            self.play(Write(jacinvmat))

            self.wait(2)

            self.play(Write(delxw))

            self.play(Create(delx))
            self.wait()

            self.play(*[Transform(_, _[1][0]) for _ in [matgrpw, matgrp]])

            self.play(matgrpw.animate.shift(RIGHT * 3))

            self.play(matgrp.animate.next_to(matgrpw, direction=DOWN))
            self.wait()

            tempmatgrp = VGroup(matgrp, matgrpw).add_background_rectangle()

            self.add(tempmatgrp)

            self.wait()
            xn = VGroup(xw.copy(), MathTex("+")).arrange_submobjects(buff=0.1).next_to(matgrpw, direction=LEFT)
            xngrp = VGroup(xgrp.copy()[-1], MathTex("+")).arrange_submobjects(buff=0.1).next_to(matgrp, direction=LEFT)
            self.play(*[Write(_[0]) for _ in [xn, xngrp]])

            self.play(
                *[Write(_[1]) for _ in [xn, xngrp]]

            )

            x1w = MathTex("X")
            x1w.add(Integer(i + 1).scale(0.4).next_to(x1w, direction=DR, buff=0.01))
            xn1 = VGroup(x1w, MathTex("=")).arrange_submobjects(buff=0.1).next_to(xn, direction=LEFT)
            xn1w = VGroup(Matrix([[round(x1, 2)], [round(x2, 2)]]), MathTex("=")).arrange_submobjects(buff=0.1).next_to(xngrp, direction=LEFT)
            self.play(*[Write(_[0]) for _ in [xn1, xn1w]])
            self.play(*[Write(_[1]) for _ in [xn1, xn1w]])

            iteration_endgrp = VGroup(xn, xngrp, xn1, xn1w, tempmatgrp)
            self.play(FadeOut(iteration_endgrp))


class NR2D2(LinearTransformationScene):
    def __init__(self):
        LinearTransformationScene.__init__(
            self,
            show_basis_vectors=False,
            # show_coordinates=True,
            # leave_ghost_vectors=True,
        )

    def construct(self):
        x1, x2 = 1, 1
        a = [-1, 1]
        # a = [0, 0]
        for i in range(6):

            F = [
                np.sin(x2) + x1,
                np.cos(x1) + x2
            ]

            jac = [
                [1, np.cos(x2)],
                [-np.sin(x1), 1]
            ]

            jacmat = Matrix([
                [1, round(np.cos(x2), 2)],
                [round(-np.sin(x1), 2), 1]
            ])
            # self.add(jacmat)

            jacinv = np.linalg.inv(jac)
            delynum = [[x1 - x2] for x1, x2 in zip(a, F)]

            [[dx1], [dx2]] = np.matmul(jacinv, delynum)

            ############################################################################################################
            xw = MathTex("X")
            xw.add(Integer(i).scale(0.4).next_to(xw, direction=DR, buff=0.01))
            xgrp = VGroup(
                xw,
                MathTex("="),
                Matrix(
                    [
                        [round(x1)],
                        [round(x2)]
                    ]
                ).scale(0.8)
            ).scale(0.75).arrange_submobjects(buff=0.1)  # .next_to(self.camera.frame.get_corner(UR), direction=DL)

            fxw = MathTex("F(\\,\\,\\,\\,\\,)")
            fxw.add(xw.copy().scale(1.25).next_to(fxw[0][1], buff=0.01))
            fxgrp = VGroup(
                fxw,
                MathTex("="),
                Matrix([
                    [round(F[0], 2)],
                    [round(F[1], 2)]
                ]).scale(0.8)).scale(0.75).arrange_submobjects(buff=0.1)  # .next_to(xgrp, direction=DOWN)

            fdxw = MathTex("J(\\,\\,\\,\\,\\,)")
            fdxw.add(xw.copy().scale(1.25).next_to(fdxw[0][1], buff=0.01))
            fdxgrp = VGroup(fdxw, MathTex("="), jacmat.copy().scale(0.8)).scale(0.75).arrange_submobjects(buff=0.1)  # .next_to(xgrp, direction=DOWN)

            fxfdxgrp = VGroup(fxgrp, fdxgrp).arrange_submobjects(buff=0.5)

            delygrp_word = VGroup(
                MathTex("\\Delta Y ="),
                Matrix([
                    [round(a[0], 2)],
                    [round(a[1], 2)]
                ]),
                MathTex("-"),
                Matrix([
                    [round(F[0], 2)],
                    [round(F[1], 2)]
                ]),
                MathTex("="),
                Matrix([
                    [round(delynum[0][0], 2)],
                    [round(delynum[1][0], 2)]
                ]).scale(0.8)
            ).scale(0.75).arrange_submobjects(buff=0.1)  # .next_to(fxgrp, direction=DOWN)

            x1w = MathTex("X")
            x1w.add(Integer(i + 1).scale(0.4).next_to(x1w, direction=DR, buff=0.01))
            delxgrp_word = VGroup(
                MathTex("\\Delta X"),
                MathTex("="),
                jacmat.copy().add(MathTex("^{-1}").scale(1.5).shift(UP + RIGHT * 1.95)),
                MathTex(
                    "\\Delta Y"
                )
            ).scale(0.75).arrange_submobjects(buff=0.1)  # .next_to(fdxgrp, direction=DOWN)

            # x1grp = VGroup(
            #     x1w,
            #     MathTex("="),
            #     xw.copy().scale(1.35),
            #     MathTex(
            #         "+",
            #         "\\dfrac{1}{f'(\\,\\,\\,\\,)}",
            #         "\\big( x2 - f(\\,\\,\\,\\,) \\big)"
            #     ),
            # ).scale(0.75).arrange_submobjects(buff=0.1)  # .next_to(fdxgrp, direction=DOWN)
            # delxgrp_word.add(
            #     xw.copy().next_to(delxgrp_word[1][1][4], buff=0.01),
            # xw.copy().next_to(x1grp[3][2][4], buff=0.01)
            # )
            x1grp = VGroup(
                x1w,
                MathTex("="),
                xw.copy().scale(1.35),
                MathTex(
                    "+",
                    "\\Delta X",
                    "="
                ),
                Matrix([
                    [round(x1 + dx1)],
                    [round(x2 + dx2)]
                ], color=YELLOW
                ).scale(0.8)

            ).scale(0.75).arrange_submobjects(buff=0.1)  # .next_to(fdxgrp, direction=DOWN)

            wordings = VGroup(xgrp, fxfdxgrp, delygrp_word, delxgrp_word, x1grp)\
                .arrange_submobjects(direction=DOWN).scale(0.75).next_to(RIGHT * 4, direction=LEFT).add_background_rectangle()
            # self.add(wordings)
            ############################################################################################################

            self.apply_matrix(jac)
            self.mobjects[1].save_state()
            self.mobjects[1].fade(1)
            self.wait(2)
            for vec, color in zip(
                [a, F, np.matmul(jac, [dx1, dx2])],
                [RED, GREEN, YELLOW]
            ):  # np.matmul(jac, [xp, yp]) [x1 - x2 for x1, x2 in zip(a, F)]
                if color != YELLOW:
                    self.add_vector(vec, color=color)
                else:
                    delyvec = Vector(vec, color=color).shift(np.array([F[0], F[1], 0]))
                    self.play(GrowArrow(delyvec))
                    self.moving_vectors.append(delyvec)

            # def add_label_to_vector(vector, label, direction=LEFT):
            #     label.next_to(vector, direction=direction, buff=0.01)
            #     self.play(Write(label))
            #     vector.add(label)
            #     vector.label = label

            if i == 0:
                temp = VGroup(
                    MathTex("A"),
                    MathTex("-"),
                    MathTex("F(X_0)"),
                    MathTex("="),
                    MathTex("\\Delta Y"),
                ).arrange_submobjects(buff=0.1).shift(DOWN + RIGHT * 2).add_background_rectangle()
                for vector, label in zip(self.moving_vectors, [temp[1], temp[3], temp[-1]]):
                    if label != temp[-1]:
                        self.play(TransformFromCopy(vector, label))
                    else:
                        self.play(Write(temp[2]), Write(temp[4]), TransformFromCopy(vector, label))
                self.wait()
                dely_position = temp[-1].get_center()
            ########################
            delyw = MathTex("\\Delta Y").move_to(dely_position)

            dely = Matrix([
                [round(delynum[0][0], 2)],
                [round(delynum[1][0], 2)]]
            ).scale(0.75).shift(DOWN * 2.5 + RIGHT * 5)
            # ).arrange_submobjects(buff=0.1).scale(0.75).next_to(ORIGIN).add_background_rectangle()

            jacinvw = MathTex("\\bf J^{-1} \\bf").next_to(delyw, direction=LEFT)
            jacinvmat = Matrix([
                [1, round(np.cos(x2), 2)],
                [round(-np.sin(x1), 2), 1]
            ]).add(MathTex("^{-1}").shift(UP + RIGHT * 1.95)).scale(0.75).next_to(dely, direction=LEFT)

            delxw = MathTex("\\Delta X", "=").next_to(jacinvw, direction=LEFT)

            # self.play(FadeOut(dely))
            delx = VGroup(
                Matrix([
                    [round(dx1, 2)],
                    [round(dx2, 2)]
                ]),
                MathTex("=")
            ).arrange_submobjects(buff=0.1).scale(0.75).next_to(jacinvmat, direction=LEFT)
            # ).arrange_submobjects(buff=0.1).scale(0.75).next_to(delyvec).add_background_rectangle()
            matgrp = VGroup(delx, jacinvmat, dely).add_background_rectangle()
            matgrpw = VGroup(delxw, jacinvw, delyw).add_background_rectangle()
            ########################
            if i == 0:
                self.play(FadeOut(temp))

            self.wait()
            self.play(
                self.moving_vectors[-1].animate.shift(-np.array([F[0], F[1], 0])),
            )
            self.play(FadeOut(*self.moving_vectors[-3:-1]))
            for p in [-3, -2]:
                self.moving_vectors.pop(p)
            self.wait()

            self.play(self.mobjects[1].animate.restore())
            self.wait(2)

            self.apply_inverse(jac)
            self.wait(3)

            # self.play(FadeOut(delx))
            # self.play(*[_.animate.align_to(DR * 4, direction=RIGHT) for _ in [matgrpw, matgrp]])
            # tempgrp = VGroup("")
            self.add_vector([x1, x2], color=RED_B)
            self.play(
                delyvec.animate.shift(np.array([x1, x2, 0])),
            )

            x1 = x1 + dx1
            x2 = x2 + dx2
            self.wait()
            self.add_vector([x1, x2], color=TEAL)
            self.play(FadeOut(*self.moving_vectors))
            self.moving_vectors.clear()
            print(x1, x2)
            self.wait()

        self.wait()


class NR2DMisc(Scene):
    def construct(self):
        trap_formula = MathTex(
            "="
            "\\dfrac{\\Delta x}{2}\\,",
            "\\Big[",
            "(y_1+y_n)",
            "+",
            "2\\,(y_2+y_3+...+y_{n-1})",
            "\\Big]",
        ).scale(1)
        self.play(Write(trap_formula))
        self.wait()
