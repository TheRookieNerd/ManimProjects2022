from manim import *


# class IM(Scene):
#     def construct(self):
#         s_f = Line(ORIGIN, 1.5 * RIGHT, color=RED)  # .shift(RIGHT)
#         s_b = Line(ORIGIN, 1.5 * LEFT, color=GREEN)  # .shift(LEFT)

#         rate = 90 * DEGREES

#         always_rotate(s_f, rate=rate, about_point=ORIGIN)
#         always_rotate(s_b, rate=-rate, about_point=ORIGIN)

#         s_r = Line().add_updater(lambda x: x.put_start_and_end_on(ORIGIN + RIGHT * 0.00000001, s_f.get_vector() + s_b.get_vector()))

#         # a_r = Line(RIGHT)
#         # a_f = Line(ORIGIN, UP, color=BLUE)  # .shift(RIGHT)
#         # a_b = Line(ORIGIN, DOWN, color=YELLOW)  # .shift(LEFT)

#         # a_r = Line(color=YELLOW).add_updater(lambda x: x.put_start_and_end_on(ORIGIN + RIGHT * 0.00000001, rotate_vector(s_f.get_vector() - s_b.get_vector(), 30 * DEGREES)))
#         a_r = Line(color=YELLOW).add_updater(lambda x: x.put_start_and_end_on(ORIGIN + RIGHT * 0.00000001, s_f.get_vector() - s_b.get_vector()))

#         # a_f = -s_b
#         # a_f = Line(color=BLUE).add_updater(lambda x: x.put_start_and_end_on(ORIGIN + RIGHT * 0.00000001, -s_b.get_vector()))
#         # always_rotate(a_f, rate=rate, about_point=ORIGIN)
#         # always_rotate(a_b, rate=-rate, about_point=ORIGIN)

#         r = Line(color=BLUE).add_updater(lambda x: x.put_start_and_end_on(ORIGIN + RIGHT * 0.00000001, s_r.get_vector() + a_r.get_vector()))

#         self.add(s_f, s_b, s_r)
#         self.wait(PI)
#         self.add(a_r, r)
#         self.wait(5)

class Stator(VGroup):
    CONFIG = {
    }

    def __init__(self, phases, p, nos, **kwargs):
        """
        phases, poles, no of slots
        """
        super().__init__(**kwargs)
        mech_angle_ps = TAU / nos                                       # mech angle per slot
        elec_angle_ps = p / 2 * mech_angle_ps                           # elec angle per slot
        phase_gap_slots = TAU / phases / elec_angle_ps                  # no of slots b/w phases
        spp = nos / p                                                   # slots per pole
        spph = int(spp / phases)                                        # slots per phase

        st_rad = 3
        st_in_rad = st_rad - 0.5

        self.colors_list = [RED, YELLOW, BLUE]                              # add more colors for more phases
        stator = VGroup(
            Circle(radius=st_in_rad, color=WHITE),
            Circle(radius=st_rad, color=WHITE)
        )
        slot_lines = VGroup(
            *[Line((st_rad - 0.5) * RIGHT, st_rad * RIGHT).rotate(_ * mech_angle_ps, about_point=ORIGIN)
              for _ in range(nos)]
        )
        stator.add(slot_lines)

        self.slots = [rotate_vector(RIGHT * ((st_rad + st_in_rad) / 2), mech_angle_ps / 2)]
        for _ in range(nos - 1):
            self.slots.append(rotate_vector(self.slots[-1], mech_angle_ps))

        wdg_table = []
        for i in range(phases):
            phase_n_slots = []
            for _ in range(p):
                if _ % 2 == 0:
                    direction = True
                else:
                    direction = False

                slot_number = i * phase_gap_slots + _ * spp
                if slot_number > nos - 1:
                    slot_number = slot_number - nos
                phase_n_slots.append((int(slot_number), direction))  # slot number, direction of current
                j = 1
                while j < spph:
                    phase_n_slots.append((phase_n_slots[-1][0] + 1, direction))
                    j += 1
            wdg_table.append(phase_n_slots)

        self.conductors = VGroup()
        for i in range(len(wdg_table)):
            for _ in wdg_table[i]:
                self.conductors.add(self.get_conductor(*_, self.colors_list[i]))
            # self.add(Dot(self.slots[int(_[0])]))
        stator.add(self.conductors)
        # slot_numbers = VGroup()
        # for i, _ in enumerate(self.slots):
        #     slot_numbers.add(Text(str(i)).scale(0.5).next_to(_, direction=_, buff=0.2))
        # self.add(slot_numbers[-1])

        # stator.add(slot_numbers)
        self.add(stator)
        # stator.rotate(mech_angle_ps)

    def get_conductor(self, slot, direction, color):
        def cross():
            return VGroup(Line(UP, DOWN), Line(LEFT, RIGHT)).scale(0.15).rotate(45 * DEGREES)
        circ = Circle(radius=0.15, color=color)
        circ.color = color
        circ.direction = direction
        circ.slot = slot
        circ.time = 0
        circ.t = 0
        circ.i_0 = 1  # variable used in updaters, unique for every conductor ik ik its shit
        circ.s_0 = 1  # same shit
        for i, _ in enumerate(self.colors_list):
            if color == _:
                circ.phase = i
        if direction:
            circ.add(Dot(radius=0.05).move_to(circ))
        else:
            circ.add(cross().scale(0.75).move_to(circ))
        return circ.move_to(self.slots[slot])

    def swap_direction(self, cond):
        d = not cond.direction
        # print("In Swap direction")
        # print(f"old cond: {d}")
        new_cond = self.get_conductor(cond.slot, d, cond.color).move_to(cond)
        # print(f"new cond: {new_cond.direction}")
        # cond.become(new_cond)
        # print(f"cond converted: {cond.direction}")

        return new_cond


class ThreePhaseWinding(Scene):
    CONFIG = {
        "phase_a_color": RED,
        "phase_b_color": YELLOW,
        "phase_c_color": BLUE,
    }

    def construct(self):
        one_phase_stators = VGroup()
        for i, _ in enumerate([RED, YELLOW, BLUE]):
            stat = Stator(1, 2, 2).rotate(i * 120 * DEGREES)
            stat.conductors.set_color(_)
            one_phase_stators.add(stat)
        # one_phase_stators[0] = Stator(1, 2, 2, [RED])
        stator = Stator(3, 2, 6)
        # self.add(stator)
        stator.rotate(TAU / 6)

        self.play(Create(one_phase_stators[0]))
        temp_origin = RIGHT * 3
        self.play(one_phase_stators[0].animate.move_to(temp_origin))
        one_phase_stators[1:].move_to(temp_origin)

        #############################
        nov = 10  # no of vectors
        f = 1     # frequency
        circ_axis = Circle(radius=1.5, stroke_width=1.5, color=GREY)  # .shift(2 * RIGHT)
        # self.add(circ_axis)

        def get_linear_sine(phase, color):
            linear_sine = VGroup()
            for _ in np.linspace(0, 1, nov):
                point_in_air = circ_axis.point_from_proportion(_)
                angle = angle_of_vector(point_in_air)
                arrow = Line(ORIGIN, 0.42 * np.cos(angle - phase * 120 * DEGREES) * 2.2 * UP, color=color, stroke_width=1.5)

                scale_factor = np.linalg.norm(arrow.get_vector()) * 2 / 3
                arrow.add(Triangle(color=color, fill_opacity=1, fill_color=color)
                          .move_to(arrow.get_end()).scale(scale_factor * 0.1).rotate(arrow.get_angle() - PI / 2, about_point=arrow.get_end()))
                linear_sine.add(arrow)

            linear_sine.arrange_submobjects(direction=RIGHT, buff=0.05)
            # linear_sine.remove(linear_sine[-1])
            for _ in linear_sine:
                _.shift(_.get_vector() / 2)

            return linear_sine

        # linear_sine.shift(UP * 3)
        ########################
        linear_sines = VGroup()
        for i, j in zip(range(3), [RED, YELLOW, BLUE]):
            linear_sines.add(get_linear_sine(i, j))
        # linear_sines[0].remove(linear_sines[0][-1])
        axis = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-2, 2],
            x_length=linear_sines[0].get_width() - 0.15,
            y_length=4,
            tips=False
        ).shift(LEFT * 3)

        x_axis_label = Tex("$\\theta$").next_to(axis.get_x_axis().get_right())
        y_axis_label = Tex("B").next_to(axis.get_y_axis().get_top())
        axis.add(x_axis_label, y_axis_label)

        linear_sines[0].align_to(axis.get_y_axis().get_center(), direction=LEFT)

        cos = axis.get_graph(lambda x: np.cos(0.99 * x))

        h_axis = Line(temp_origin, temp_origin + 1.5 * RIGHT)
        radius = Line(temp_origin, temp_origin + 1.5 * RIGHT)
        ldot = Dot(color=RED).move_to(axis.y_axis.get_center())
        cdot = ldot.copy().add_updater(lambda x: x.move_to(radius.get_end()))

        self.a = 0

        def arc_updater(arc):
            # print(radius.get_angle() / DEGREES)
            self.a = radius.get_angle()
            if self.a < 0:
                self.a = TAU + self.a
            na = Arc(radius=0.5, angle=self.a, arc_center=temp_origin)
            # print(a / DEGREES)
            # print()
            arc.become(na)
        arc = Arc(angle=radius.get_angle(), arc_center=temp_origin).move_to(temp_origin).add_updater(arc_updater)

        # def theta_updater(t):
        #     t.become(Tex(str(radius.get_angle())).move_to())
        theta = MathTex("\\theta = ")
        # theta_value = Tex(str(radius.get_angle())).add_updater(theta_updater)
        # theta_value = ValueTracker(0).add_updater(lambda x: x.set_value(radius.get_angle() / DEGREES))
        theta_value = DecimalNumber(0, num_decimal_places=0).add_updater(lambda x: x.next_to(theta)).add_updater(lambda x: x.set_value(self.a / DEGREES))
        deg = MathTex("^{\\circ}").add_updater(lambda x: x.next_to(theta_value, direction=UR, buff=0.02))
        theta_grp = VGroup(theta, theta_value, deg).arrange_submobjects(direction=RIGHT).move_to(UP * 3)

        self.play(Create(h_axis))
        self.add(radius, arc, theta_grp)

        self.play(Create(axis), run_time=2)

        circ_axis_copy = circ_axis.copy().move_to(one_phase_stators[0])

        self.play(
            FadeIn(cdot),
            FadeIn(circ_axis_copy)
        )

        self.play(TransformFromCopy(cdot, ldot))
        self.wait()
        self.play(
            Create(cos),
            Rotate(radius, TAU, about_point=temp_origin),
            ldot.animate.move_to(axis.x_axis.get_end()),
            rate_func=linear, run_time=2
        )

        self.play(FadeOut(theta_grp, radius, arc, h_axis, ldot, cdot))

        B_dc = MathTex("B = B_m\\cos\\theta").next_to(theta_grp, direction=LEFT, buff=1)
        self.play(Write(B_dc))

        self.play(
            AnimationGroup(
                *[Create(linear_sines[0][i]) for i in range(len(linear_sines[0]) - 1)],
                lag_ratio=0.5,
                rate_func=linear
            ),

            run_time=2
        )
        # for _ in [axis, cos, linear_sines[0]]:
        #     self.play(Create(_))

        def get_rad_sine(linear_sine):
            rad_sine = VGroup()
            self.points_in_air = []
            for i, _ in enumerate(np.linspace(0, 1, nov)):
                point_in_air = circ_axis.point_from_proportion(_)
                self.points_in_air.append(point_in_air)
                angle = angle_of_vector(point_in_air) - 90 * DEGREES
                arrow = linear_sine[i].copy().scale(1 / 2.2).rotate(angle).move_to(point_in_air)
                arrow.shift(arrow.get_vector() / 2)
                rad_sine.add(arrow)

            rad_sine.remove(rad_sine[-1])
            return rad_sine
            # linear_sine[i].rotate(angle).move_to(point_in_air)
            # linear_sine[i].shift(linear_sine[i].get_vector() / 2)

        rad_sines = VGroup()
        for i in linear_sines:
            rad_sines.add(get_rad_sine(i))
        for _ in linear_sines:
            _.remove(_[-1])
        # linear_sines[0].remove(linear_sines[0][-1])
        # rad_sines[0].remove(rad_sine[-1])
        rad_sines[0:].shift(temp_origin)
        # y_rad_sine.shift(RIGHT * 4)
        # for _ in [r_ra]
        # self.play(
        # *[_.animate.shift(UP * 2) for _ in [axis, linear_sine]],
        # one_phase_stators[0].animate.move_to(ORIGIN)
        # )
        self.play(
            AnimationGroup(
                *[ReplacementTransform(i, j) for i, j in zip(linear_sines[0], rad_sines[0])],
                lag_ratio=0.25,
                rate_func=linear
            ),
            FadeOut(axis, cos),
            B_dc.animate.next_to(one_phase_stators[0], direction=LEFT, buff=2),
            run_time=2
        )

        B_dc_Y = MathTex("B = B_m \\, \\cos (\\theta - 120^{\\circ})").move_to(B_dc)
        B_dc_B = MathTex("B = B_m \\, \\cos (\\theta - 240^{\\circ})").move_to(B_dc)

        DC_eqns = VGroup(B_dc, B_dc_Y, B_dc_B)
        # one_phase_stators.save_state()
        for _ in range(2):
            self.play(
                # AnimationGroup(
                AnimationGroup(Rotate(one_phase_stators[_], 120 * DEGREES),
                               FadeOut(rad_sines[_]),
                               lag_ratio=0.15
                               ))
            self.play(
                FadeOut(one_phase_stators[_]),
                FadeIn(rad_sines[_ + 1]),
                FadeIn(one_phase_stators[_ + 1]),
                # lag_ratio=1
            )
            # )
            self.remove(one_phase_stators[_])
            self.play(ReplacementTransform(DC_eqns[_], DC_eqns[_ + 1]))

            self.wait()

        self.play(
            *[_.animate.move_to(ORIGIN) for _ in [one_phase_stators[-1], circ_axis_copy]],
            rad_sines[-1].animate.shift(-temp_origin),
            FadeOut(B_dc_B)
        )
        rad_sines[0:-1].shift(-temp_origin)
        self.play(FadeOut(one_phase_stators[-1]), FadeIn(stator))

        self.play(FadeOut(rad_sines[-1]), FadeIn(rad_sines[0]))
        self.wait()
        ##########################################################

        def get_field(phase, color):
            field = VGroup()

            def arrow_updater(arrow, dt):
                # print(dt)
                arrow.t += dt
                # print(arrow.t)
                theta = arrow.get_angle()
                p = 4
                scale_factor = (np.cos((p / 2 * theta - phase * 120 * DEGREES) + (f * arrow.t - phase * 120 * DEGREES))
                                + np.cos((p / 2 * theta - phase * 120 * DEGREES) - (f * arrow.t - phase * 120 * DEGREES))) / 4
                # print(scale_factor)
                new_arrow = Arrow(ORIGIN, scale_factor * RIGHT, color=color).rotate(theta).move_to(arrow.center)
                new_arrow.shift(new_arrow.get_vector() / 2)
                arrow.become(new_arrow)

            for i, _ in enumerate(np.linspace(0, 1, nov)):
                # point_in_air = circ_axis.point_from_proportion(_)
                point_in_air = self.points_in_air[i]
                angle = angle_of_vector(point_in_air)
                arrow = Line(ORIGIN, RIGHT, color=color).rotate(angle).move_to(point_in_air)
                # arrow.shift(arrow.get_vector() / 2)
                # arrow.scale_about_point(np.cos(2 * arrow.get_angle()), point_in_air)
                arrow.t = 0
                arrow.center = point_in_air
                arrow.add_updater(arrow_updater)
                # self.add(arrow)
                field.add(arrow)
            return field

        phase_a = get_field(0, RED)
        phase_b = get_field(1, YELLOW)
        phase_c = get_field(2, BLUE)

        #######################################################
        # rmf as sum of three phases
        rmf = VGroup()

        # self.i = 0

        def rmf_updater(arrow):
            i = arrow.index
            # scale_factor = np.linalg.norm(phase_a[i].get_vector() + phase_b[i].get_vector() + phase_c[i].get_vector())
            new_arrow = Line(ORIGIN, phase_a[i].get_vector() + phase_b[i].get_vector() + phase_c[i].get_vector(), color=WHITE, stroke_width=3).move_to(self.points_in_air[i])
            new_arrow.shift(new_arrow.get_vector() / 2)
            scale_factor = np.linalg.norm(new_arrow.get_vector()) * 2 / 3
            new_arrow.add(Triangle(color=WHITE, fill_opacity=1, fill_color=WHITE)
                          .move_to(new_arrow.get_end()).scale(scale_factor * 0.1).rotate(new_arrow.get_angle() - PI / 2, about_point=new_arrow.get_end()))
            # new_arrow.add(ArrowTip().move_to(new_arrow.get_end()))

            # print(new_arrow.get_angle())
            arrow.become(new_arrow)

        for _ in range(len(phase_a)):
            # self.i = _
            arrow = Line(ORIGIN, RIGHT, color=WHITE)  # .rotate(theta).move_to(point_in_air)
            arrow.index = _
            # print(arrow.index)
            arrow.add_updater(rmf_updater)
            rmf.add(arrow)

        ##############################################################
        # rmf manual

        # rmf = VGroup()

        # def arrow_updater(arrow, dt):
        #     # print(dt)
        #     arrow.t += 0.1
        #     # print(arrow.t)
        #     theta = arrow.get_angle()
        #     p = 2
        #     scale_factor = np.cos(arrow.t + p / 2 * theta)
        #     # print(scale_factor)
        #     new_arrow = Line(ORIGIN, scale_factor * RIGHT, color=WHITE).rotate(theta).move_to(arrow.center)
        #     new_arrow.shift(new_arrow.get_vector() / 2)
        #     arrow.become(new_arrow)

        # for i, _ in enumerate(np.linspace(0, 1, nov)):
        #     # point_in_air = circ_axis.point_from_proportion(_)
        #     point_in_air = self.points_in_air[i]
        #     angle = angle_of_vector(point_in_air)
        #     arrow = Line(ORIGIN, RIGHT, color=WHITE).rotate(angle).move_to(point_in_air)
        #     # arrow.shift(arrow.get_vector() / 2)
        #     # arrow.scale_about_point(np.cos(2 * arrow.get_angle()), point_in_air)
        #     arrow.t = 0
        #     arrow.center = point_in_air
        #     arrow.add_updater(arrow_updater)
        #     # self.add(arrow)
        #     rmf.add(arrow)
        ###########################################

        # self.i_0 = 0
        self.n = 0

        def conductor_updater(c, dt):

            i_1 = np.cos(f * c.time - c.phase * 120 * DEGREES)
            if c.time == 0:
                c.i_0 = i_1

            def get_sign_bit(i):
                sign_bit = 1 if i > 0 else 0
                return sign_bit

            if get_sign_bit(c.i_0) != get_sign_bit(i_1):
                nc = stator.swap_direction(c)
                c.become(nc)
                c.direction = not c.direction
                c.s_0 = 1
                c.t = (c.phase * 120 * DEGREES - 90 * DEGREES) / f

            s = abs(np.cos(f * c.t - c.phase * 120 * DEGREES)) + 0.001

            # if c.t == c.phase * 120 * DEGREES:
            #     c[1].scale(s)
            # else:
            c[1].scale(1 / c.s_0 * s)

            c.i_0 = i_1
            c.s_0 = s
            c.time += dt
            c.t += dt

        for _ in stator.conductors:
            _.add_updater(conductor_updater)
        # stator.conductors[0].add_updater(conductor_updater)
        # stator.conductors[2].add_updater(conductor_updater)
        # stator.swap_direction(_)
        # self.add(stator.conductors, phase_a, phase_b, phase_c)
        # self.play(FadeOut(rad_sines[0]), run_time=0.15)

        # self.wait(10)
        ###########################################

        stator_cross_dots = [_[-1] for _ in stator.conductors]
        blocks = VGroup(*[Circle(radius=0.15, fill_opacity=1, fill_color=BLACK, stroke_width=0.001).move_to(_) for _ in stator_cross_dots])
        # self.add(blocks)

        def opacity_updater_1(phase):
            phase.set_opacity(0)

        def opacity_updater_2(phase):
            phase.set_opacity(1)
        for i, j in zip([phase_a, phase_b, phase_c], [0, 2, 4]):  # , stator_directions]:

            for _ in i:
                _.add_updater(opacity_updater_1)
            self.add(i)

        self.play(FadeOut(rad_sines[0]), run_time=0.15)
        # self.add(phase_a)
        # for i, j in zip([phase_a, phase_b, phase_c], [0, 2, 4]):
        for i, j in zip([phase_b], [2]):

            for k in [i]:  # , stator_directions[j:j + 2]]:
                for _ in k:
                    _.remove_updater(opacity_updater_1)
                    _.add_updater(opacity_updater_2)

        #     self.remove(blocks[j:j + 2].set_opacity(0))

        #     if i is phase_a:
        #         self.play(FadeOut(rad_sines[0]), run_time=0.15)

        #     # self.play(FadeIn(DC_eqns[j % 2], tex[j % 2]))
        #     self.wait(10)
        # self.play(FadeOut(DC_eqns[j % 2], tex[j % 2]))

        # for i, j in zip([phase_a, phase_b, phase_c], [0, 2, 4]):
        #     for k in [i]:  # , stator_directions[j:j + 2]]:
        #         _.remove_updater(opacity_updater_2)
        #         _.add_updater(lambda x: x.set_opacity(0.25))

        def cross():
            return VGroup(Line(UP, DOWN), Line(LEFT, RIGHT)).scale(0.15).rotate(45 * DEGREES)
        self.temp = 0
        rotor = Circle(radius=1.25, color=PURPLE, fill_opacity=0.5, fill_color=GREY)
        rotor.add(Circle(radius=0.1, color=PURPLE).add(cross().scale(0.5)).shift(DOWN)).add(Circle(radius=0.1, color=PURPLE).add(Dot().scale(0.5)).shift(UP))  # .add_updater(lambda x, dt: x.rotate(1 / 2 * PI))

        def rotor_updater(rotor, dt):
            self.temp += dt
            rotor.rotate(f * dt)
        # self.add(rotor)
        rotor.add_updater(rotor_updater)
        # self.add(phase_a)  # , rotor)
        self.wait(4)

        ###########################################

# class RMF(Scene):
#     def construct(self):
#         # circ = Circle(radius=2, stroke_width=1, color=GREY)
#         # self.add(circ)

#         # for _ in np.linspace(0, 1, 50):
#         #     # self.add()
#         #     # print(_)
#         #     point_in_air = circ.point_from_proportion(_)
#         #     angle = angle_of_vector(point_in_air)
#         #     arrow = Arrow(ORIGIN, RIGHT).rotate(angle).move_to(point_in_air)
#         #     # arrow.shift(arrow.get_vector() / 2)
#         #     arrow.scale_about_point(np.sin(2 * arrow.get_angle()), point_in_air)
#         #     self.add(arrow)
#         #     # rotate_vector()
#         self.t = 0

#         def arr_updater(arr, dt):
#             self.t += dt
#             scale_fac = (np.cos(self.t) + np.cos(-self.t)) / 2
#             new_arr = Line(ORIGIN, scale_fac * UP)
#             arr.become(new_arr)

#         arr = Line(ORIGIN, UP)
#         arr.t = 0
#         arr.add_updater(arr_updater)
#         self.add(arr)
#         self.wait(4)


# class Walk(Scene):
#     def construct(self):
#         legs = VGroup(*[Line(ORIGIN, _).add_updater(lambda x, dt:x.rotate(np.sin(4 * dt), about_point=ORIGIN)) for _ in [DR, DL]])

#         self.add(legs)
#         self.wait(3)

# class Equations(Scene):
#     def construct(self):
#         stat = Text("Stator")
#         self.play(Write(stat))
#         self.wait()
        # tex = VGroup(
        #     MathTex("B_r = B_m \\, \\cos \\theta", " \\cos \\omega t"),
        #     MathTex("+"),
        #     MathTex("B_y = B_m \\, \\cos (\\theta - 120^{\\circ})", "\\cos (\\omega t - 120^{\\circ})"),
        #     MathTex("+"),
        #     MathTex("B_b = B_m \\, \\cos (\\theta - 240^{\\circ})", " \\cos (\\omega t - 240^{\\circ})"),
        # ).arrange_submobjects(direction=DOWN)
        # for _ in range(2):
        #     self.play(
        #         Write(tex[0][_])
        #     )
        #     self.wait()
        # self.wait()
        # for _ in range(2):
        #     self.play(
        #         Write(tex[2 * (_ + 1)]),
        #         FadeOut(tex[2 * _])
        #     )
        #     self.wait()

        # self.play(FadeIn(tex[0:-1:2]))
        # self.wait()
        # self.play(FadeIn(tex[1:-1:2]))
        # self.wait()

        # B_res = MathTex("B_{res} = \\dfrac{3}{2} \\, B_m \\, cos(\\theta - \\omega t) ")
        # self.play(Transform(tex, B_res))
        # self.wait()
