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


class EulerODE(MovingCameraScene):
    CONFIG = {
        "dot_kwargs": {
            "radius": .035,
            "color": BLUE,
            "fill_opacity": .75,
        },
        "vectorfield_kwargs": {
            # "x_min": -2,
            # "x_max": 2,
            # "y_min": -2,
            # "y_max": 2,
            # #"delta_x": .25,
            # #"delta_y": .25,
            # # "length_func": lambda norm: .45 * sigmoid(norm),
            # #"opacity": 1.0,
        },
        "grid_kwargs": {
            "axis_config": {
                "stroke_color": WHITE,
                "stroke_width": 1,
                "include_ticks": False,
                "include_tip": False,
                "line_to_number_buff": SMALL_BUFF,
                "label_direction": DR,
                "number_scale_val": 0.5,
            },
            "y_axis_config": {
                "label_direction": DR,
            },
            "background_line_style": {
                "stroke_color": BLUE_D,
                "stroke_width": 2,
                "stroke_opacity": 1,
            },
            # Defaults to a faded version of line_config
            "faded_line_style": None,
            "x_line_frequency": 1,
            "y_line_frequency": 1,
            "faded_line_ratio": 1,
            "make_smooth_after_applying_functions": True,
        },
        "number_line_kwargs": {
            "color": LIGHT_GREY,
            "x_min": -10,
            "x_max": 10,
            "unit_size": 1,
            "include_ticks": True,
            "tick_size": 0.1,
            "tick_frequency": 1,
            # Defaults to value near x_min s.t. 0 is a tick
            # TODO, rename this
            "leftmost_tick": None,
            # Change name
            "numbers_with_elongated_ticks": [0],
            "include_numbers": False,
            "numbers_to_show": None,
            "longer_tick_multiple": 2,
            "number_at_center": 0,
            "number_scale_val": 0.75,
            "label_direction": DOWN,
            "line_to_number_buff": MED_SMALL_BUFF,
            "include_tip": False,
            "tip_width": 0.25,
            "tip_height": 0.25,
            "decimal_number_config": {
                "num_decimal_places": 0,
            },
            "exclude_zero_from_default_numbers": False,
        }

    }

    def construct(self):

        title = Text("Euler's Method - A numerical method for solving ODE").scale(0.75).to_edge(UP)
        diff_eqn = MathTex("\\dfrac{dy}{dx}=", "x^2-y^2").next_to(title, direction=DOWN).shift(LEFT * 4).add_background_rectangle(opacity=0.55)
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
        self.wait()
        self.play(Create(diff_eqn))
        self.wait()
        self.play(Create(init_text))
        self.wait()

        # field = VectorField(four_swirls_function)
        # self.add(field)
        initial_condition = 0  # * 3
        demo_dot = Dot(initial_condition, color=WHITE)
        # demo_vect = field.get_vector(point=[demo_dot.get_center()[0], demo_dot.get_center()[1]])

        def get_demo_vect():
            # return field.get_vector(point=[demo_dot.get_center()[0], demo_dot.get_center()[1]])
            vec = Arrow(ORIGIN, RIGHT,
                        color=RED,
                        stroke_width=15
                        ).scale(1.5).move_to(ORIGIN)
            vec.rotate(
                np.arctan(
                    func(demo_dot.get_center()[0], demo_dot.get_center()[1])
                ),
            ).shift(demo_dot.get_center()).shift(vec.get_vector() / 2)
            return vec

        demo_vect = Arrow(ORIGIN, RIGHT)

        def func(x, y):
            return x**2 - y**2

        # def get_vector(x, y, func):
        #     vec = Arrow(ORIGIN, RIGHT).rotate(np.arctan2(func(x, y)))
        #     vec.shift(np.array([x, y, 0]))

        slope_field = VGroup()
        x_rad = 7
        for i in list(range(-x_rad, x_rad + 1, 1)):
            for j in list(range(-x_rad, x_rad + 1, 1)):
                slope_line = Line(ORIGIN, RIGHT, color=YELLOW).scale(.5).rotate(np.arctan(func(i, j)))
                slope_line.move_to(np.array([i, j, 0]))
                slope_field.add(slope_line)

        coords = MathTex("(0,0)", "(1,0)", "(2,0)")
        for k, l in zip(coords, [ORIGIN, RIGHT, RIGHT * 2]):
            k.move_to(l)

        samples = VGroup(
            *[Line(ORIGIN, RIGHT, color=YELLOW)
              .scale(.5)
              .rotate(np.arctan(func(*x))).move_to(np.array([x[0], x[1], 0]))
              for x in [[0, 0], [1, 0], [2, 0]]
              ]
        )
        for coord, sample in zip(coords, samples):
            self.play(Write(coord))
            self.play(
                coord.animate.move_to(diff_eqn.get_center()).scale(.01)
            )
            # self.play(
            #     coord.animate
            # )
            self.wait(.5)
            self.play(TransformFromCopy(diff_eqn[2], sample))
            self.wait()

        slope_field.add_to_back()  # [title, diff_eqn, init_text, demo_dot, demo_vect])
        self.play(
            Create(slope_field),
            FadeOut(title, diff_eqn),
            grid.animate.fade(.7),
        )
        self.wait(.5)
        # self.play(Create(init_text))
        self.play(Create(demo_dot), Create(demo_vect))
        self.wait()
        # self.play(FadeOut(init_text))

        step_size = Tex(r"Step Size $h$ =").scale(0.9)
        step = DecimalNumber(1).scale(0.75).next_to(step_size)
        step_text = VGroup(step_size, step).add_background_rectangle()

        x_n = initial_condition
        x_np1 = 0
        y_n = 0
        y_np1 = 0

        m = func(x_n, y_n)

        x_nw, x_np1w, y_nw, y_np1w, mw = [DecimalNumber(_).scale(0.75) for _ in [x_n, x_np1, y_n, y_np1, m]]

        xgrp1 = MathTex("x_{n+1}", " = ", "x_n + h ")
        xgrp2 = VGroup(MathTex("="), x_nw, MathTex("+"), step.copy(), MathTex("="), x_np1w)\
            .arrange_submobjects(direction=RIGHT)

        xgrp = VGroup(xgrp1, xgrp2).arrange_submobjects(direction=DOWN)
        xgrp2.next_to(xgrp1, direction=DOWN).align_to(xgrp1[1].get_left(), direction=LEFT)

        ygrp1 = MathTex("y_{n+1}", " =", " y_n + h \\times \\dfrac{dy}{dt}\\Bigr\\rvert_{x = x_n} ")
        ygrp2 = VGroup(MathTex("="), y_nw, MathTex("+"), mw, MathTex("\\,\\,="), y_np1w)\
            .arrange_submobjects(direction=RIGHT)

        ygrp = VGroup(ygrp1, ygrp2).arrange_submobjects(direction=DOWN)
        ygrp2.next_to(ygrp1, direction=DOWN).align_to(ygrp1[1].get_left(), direction=LEFT)
        wordings = VGroup(step_text, xgrp, ygrp).scale(0.75).arrange_submobjects(direction=DOWN, buff=0.5).to_corner(UL).add_background_rectangle()
        step_text.align_to(xgrp1.get_left(), direction=LEFT)
        # wordings.align_submobjects(wordings[0], direction=LEFT)

        self.play(init_text.animate.next_to(ORIGIN, direction=UP))
        self.play(FadeIn(wordings[0]))
        self.wait()
        for mob in [step_text, xgrp1, ygrp1]:
            self.play(Create(mob))
            self.wait()
        # self.play(Create(step_text))
        # self.add(wordings)

        def update_vector(obj):
            obj.become(get_demo_vect())

        demo_vect.add_updater(update_vector)

        # self.play(FadeIn(demo_dot), FadeIn(demo_vect))
        self.add(demo_vect)
        # self.wait(2)

        path = VMobject(stroke_width=5, color=BLUE)
        path.set_points_as_corners([demo_dot.get_center(), demo_dot.get_center() + UP * 0.01])

        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([demo_dot.get_center()])
            path.become(previous_path)
        path.add_updater(update_path)
        self.add(path)

        intervals = [5, 1]  # , 17]
        widths = [1, .5]  # .25]

        next_point = ORIGIN
        demo_dot.save_state()

        for interval, width in zip(intervals, widths):
            if width == 1:
                self.play(FadeOut(init_text))
            self.play(step.animate.set_value(width))
            for i in range(interval):
                self.play(ApplyMethod(demo_dot.move_to, next_point))
                if width == 1 and i != 0:
                    self.play(FadeOut(xgrp2, ygrp2))

                m = func(x_n, y_n)
                mw.set_value(m * width)

                x_nw.set_value(x_n)
                y_nw.set_value(y_n)

                x_n += width
                x_np1w.set_value(x_n)

                y_n = y_n + m * width
                y_np1w.set_value(y_n)
                next_point = np.array([x_n, y_n, 0])

                if width == 1:
                    self.play(Write(xgrp2))
                    self.play(Write(ygrp2))

                    self.wait(1)

            if width == 1:
                self.play(FadeOut(xgrp, ygrp, wordings[0]))
                self.play(step_text.animate.to_corner(UL, buff=1).scale(1.5))
            path.suspend_updating()
            next_point = initial_condition
            self.play(
                demo_dot.animate.restore(),
                FadeOut(path)
            )
            self.remove(path)
            path = VMobject(stroke_width=5, color=BLUE)
            path.set_points_as_corners([demo_dot.get_center(), demo_dot.get_center() + UP * 0.01])
            path.add_updater(update_path)
            self.add(path)
            x_n, y_n = 0, 0

        self.wait(2)

        # self.play(
        #     FadeOut(*self.mobjects),
        #     run_time=2
        # )
