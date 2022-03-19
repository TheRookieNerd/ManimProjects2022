from manim import *
from circuits import *
from math import exp, log


class BjtMosCharacteristics(Scene):
    def construct(self):
        mos_axis = Axes(
            x_range=[-1, 5, 1],
            y_range=[-0.001, 0.010, 0.002],
            x_length=7,
            y_length=6,
            x_axis_config={
                "include_tip": False
            },
            y_axis_config={
                "include_tip": False
            }
        ).add_coordinates()

        x_label = MathTex("V_{DS}", color=YELLOW).scale(0.75).next_to(mos_axis.x_axis.get_right(), direction=DR)
        y_label = MathTex("I_D", color=RED).scale(0.75).next_to(mos_axis.y_axis.get_top(), direction=UL)
        axis_labels = VGroup(x_label, y_label)

        self.vgs = 2
        self.kn = 0.0043
        self.vt = 0.5

        def mos_op_func(vds):

            if self.vgs < self.vt:
                return 0
            elif (self.vgs - self.vt) >= vds:
                return self.kn * ((self.vgs - self.vt) * vds - vds**2 / 2)
            else:
                return self.kn * (self.vgs - self.vt)**2 / 2

        def mos_op_locus(vds):
            return self.kn * vds**2 / 2

        idvds = VGroup()
        for vgs in np.arange(0, 3, 0.5):
            self.vgs = vgs

            idvds.add(mos_axis.plot(mos_op_func, x_range=[0, 5], color=RED))
            if self.vgs > 0.5:
                idvds[-1].add(MathTex("V_{GS} =", str(self.vgs)).scale(0.65).next_to(idvds[-1].points[-1]))

        idvds_locus = mos_axis.plot(mos_op_locus, x_range=[0, self.vgs - self.vt + 0.3], color=BLUE, stroke_width=2)

        locus_label_pt = idvds_locus.points[-8]
        measure_lines = VGroup(
            DoubleArrow(np.array([mos_axis.y_axis.get_center()[0] + 0.25, locus_label_pt[1], 0]), locus_label_pt + RIGHT * 0.2).stretch(0.7, 1),
            DoubleArrow(locus_label_pt + LEFT * 0.2, np.array([mos_axis.x_axis.get_right()[0], locus_label_pt[1], 0])).stretch(0.7, 1)
        )
        text = VGroup(
            MathTex("V_{DS}<V_{GS}-V_{th}").next_to(measure_lines[0], direction=UP, buff=0.5).shift(LEFT),
            MathTex("V_{DS}>V_{GS}-V_{th}").next_to(measure_lines[1], direction=UP, buff=0.5).shift(RIGHT),
        ).scale(0.6)

        def mos_ip_func(vgs):
            if vgs < self.vt:
                return 0
            else:
                return self.kn * (vgs - self.vt)**2 / 2

        mos_ip_axis = Axes(
            x_range=[-0.5, 3, 0.5],
            y_range=[-0.001, 0.010, 0.002],
            x_length=7,
            y_length=6,
            x_axis_config={
                "include_tip": False
            },
            y_axis_config={
                "include_tip": False
            }
        ).add_coordinates()

        ip_axis_labels = mos_ip_axis.get_axis_labels(x_label=MathTex("V_{GS}", color=GREEN).scale(0.75), y_label=MathTex("I_D", color=RED).scale(0.75))

        idvgs = mos_ip_axis.plot(mos_ip_func, x_range=[0, 2.75], color=RED)
        vt_text = MathTex("V_t").next_to(mos_ip_axis.c2p(self.vt, 0), direction=UP)
        # ip_condition = MathTex("V_{DS} \\geq V_{GS}-V_{th} ").scale(0.75).next_to(ip_axis.get_bottom(), direction=LEFT, buff=0)
        mos_eqn = VGroup(
            # MathTex("I_D", " = \\dfrac{\\mu C_{ox} W}{L}"),
            MathTex("i_D", " = k_n"),
            MathTex("(", "v_{GS}", "-V_{th})^2 \\over 2")  # s, substrings_to_isolate="V_{GS}"),
        ).arrange_submobjects(buff=0.1)
        mos_eqn.scale(0.8).next_to(idvgs.points[-20], direction=LEFT, buff=0.5)
        mos_eqn[0].set_color_by_tex("i_D", RED)
        mos_eqn[1].set_color_by_tex("v_{GS}", GREEN)

        idvgs_grp = VGroup(mos_ip_axis, idvgs, ip_axis_labels, vt_text, mos_eqn)
        idvds_grp = VGroup(mos_axis, axis_labels, idvds, idvds_locus, measure_lines, text)

        def bjt_ip_func(vbe):
            return 10**-12 * exp(vbe / 0.025)

        bjt_axis = Axes(
            x_range=[-0.1, 0.8, 0.1],
            y_range=[-0.001, 0.010, 0.002],
            x_length=7,
            y_length=6,
            x_axis_config={
                "include_tip": False
            },
            y_axis_config={
                "include_tip": False
            }
        ).add_coordinates()

        bjt_ip_axis_labels = bjt_axis.get_axis_labels(x_label=MathTex("V_{BE}", color=GREEN).scale(0.75), y_label=MathTex("I_C", color=RED).scale(0.75))
        icvbe = bjt_axis.plot(bjt_ip_func, x_range=[0, 0.575, 0.001], color=RED)
        bjt_eqn = MathTex("i_C", "= I_s \\, e^{(", "v_{BE}", "/V_t)}").next_to(icvbe).shift(LEFT * 4.25 + UP * 1.5)
        bjt_eqn.set_color_by_tex("i_C", RED)
        bjt_eqn.set_color_by_tex("v_{BE}", GREEN)
        icvbe_grp = VGroup(bjt_axis, bjt_ip_axis_labels, icvbe, bjt_eqn)

        bjt = BJT().shift(4 * LEFT + 1.5 * DOWN).add_labels()
        mos = MOSFET().shift(3.5 * RIGHT + 1.5 * DOWN).add_labels()
        bjt_text = Text("BJT").next_to(bjt, direction=UP, buff=0.6).scale(0.7)
        mos_text = Text("MOSFET").next_to(mos, direction=UP, buff=1).scale(0.7)
        bjt.add(bjt_text)
        mos.add(mos_text)

        self.play(Create(bjt), Create(mos))

        transconamp = VGroup(
            Tex(r"Voltage", r"\, Controlled", r"\, Current", r"\, Source"),
            Tex(r"Transconductance Amplifier"),
        ).arrange_submobjects(direction=DOWN).scale(1.25).to_edge(UP)

        self.play(
            AnimationGroup(*[GrowFromCenter(t) for t in transconamp[0]], lag_ratio=0.5)
        )
        self.play(Write(transconamp[1]))
        self.wait()

        self.play(bjt.animate.to_edge(UP), FadeOut(mos, transconamp))  # .shift(LEFT * 0.25 + UP), FadeOut(mos, bjt_text))
        mos.to_edge(UP).align_to(bjt, direction=LEFT).shift(LEFT)

        bjt_active_region = VGroup(
            Text("Active Region"),
            Line(LEFT, RIGHT).scale(2.5),
            Text("B-E Junction:  FB"),
            Text("B-C Junction: RB")
        ).scale(0.75).arrange_submobjects(direction=DOWN).next_to(bjt, direction=DOWN, buff=1).shift(LEFT * 0.25)

        for t in bjt_active_region:
            self.play(Write(t))

        bjtamp = BJTAmp().shift(2 * RIGHT)
        # bjt_eqn..next_to(bjtamp[0:9], direction=UL),

        self.play(
            TransformFromCopy(bjt[0:-1], bjtamp[0:9])
        )

        transconamp[1].to_edge(UP)
        transconamp.remove(transconamp[0])

        vcc = bjtamp.elements[-2]
        temp_short = Line(bjtamp.collector(), vcc.get_bottom())
        vcc.add(MathTex("V_{CC}").scale(0.75).next_to(vcc, direction=UR, buff=0))

        ic, vbe = MathTex("i_c", color=RED), MathTex("v_{BE}", color=GREEN).scale(0.75)
        ic_arrow = Arrow(UP, DOWN).scale(0.75).next_to(temp_short, buff=0.5)
        ic.next_to(ic_arrow)
        ic.add(ic_arrow)
        vbe.next_to(bjtamp.elements[1][0], direction=DL, buff=0.1)
        temp_bjt_amp = VGroup(bjtamp.elements[0:4:3], bjtamp.elements[-1], bjtamp[-1], temp_short)
        self.play(
            *[Create(m)
              for m in temp_bjt_amp
              ],
        )

        self.play(Write(vbe))
        self.play(Write(ic))
        self.wait()
        self.play(Wiggle(vbe))
        self.play(Wiggle(ic))
        self.wait()
        self.play(FadeOut(temp_bjt_amp, bjtamp[:9], vbe, ic))
        self.wait()
        self.play(Create(icvbe_grp.to_edge(RIGHT, buff=0.1)[:-1]))
        self.play(Write(icvbe_grp[-1]))
        self.wait()
        self.play(FadeOut(bjt_active_region, icvbe_grp[:-1], bjt, bjt_eqn))

        self.wait()
        # #########

        mos_active_region = VGroup(
            Text("Active Region").scale(0.75),
            Line(LEFT, RIGHT).scale(2),
            MathTex("V_{GS} > V_{th} "),
            MathTex("V_{DS} \\geq V_{GS}-V_{th} "),
        ).arrange_submobjects(direction=DOWN, buff=0.25).next_to(mos, direction=DOWN, buff=.5).shift(LEFT * 0.25)
        self.play(FadeIn(mos))
        self.play(Write(mos_active_region[0:-1]))
        # idvds_grp.to_edge(RIGHT)
        # self.play(FadeIn(idvds_grp[:-2]))
        self.play(Write(mos_active_region[-1]))
        # self.play(FadeIn(idvds_grp[-2:]))

        idvgs_grp.to_edge(RIGHT)
        self.play(
            # FadeOut(idvds_grp),
            Create(idvgs_grp[:-1])
        )
        self.play(Write(idvgs_grp[:-1]))
        self.wait()
        bjt.move_to(LEFT * 3.5)
        bjt_eqn.next_to(bjt, direction=DOWN, buff=0.5)

        self.play(
            FadeOut(idvgs_grp[:-1], mos_active_region),
            *[FadeIn(m) for m in [bjt, bjt_eqn]],
            mos.animate.move_to(RIGHT * 3.5),
            mos_eqn.animate.next_to(RIGHT * 3.5, direction=DOWN, buff=2)
        )
        self.wait()
        # #############################
        voltageamp = Tex(r"Voltage Amplifier").scale(1.25).to_corner(UL)

        self.play(Write(transconamp))
        self.play(FadeOut(mos, mos_eqn))

        for m in [bjtamp, vbe, ic, temp_short]:
            m.shift(LEFT)

        self.play(
            bjt_eqn.animate.next_to(voltageamp, direction=DOWN, buff=0.75),
            FadeOut(bjt[-1]),
            ReplacementTransform(bjt[0:-1], bjtamp[0:9])
        )

        self.play(
            *[Create(m)
              for m in [bjtamp.elements[0:4:3], bjtamp.elements[-1], bjtamp[-1], temp_short]
              ],
            transconamp.animate.to_corner(UL)
        )
        rc = bjtamp.elements[2]
        self.play(Write(vbe))
        self.play(Write(ic))
        self.play(ReplacementTransform(transconamp, voltageamp))
        rc_text = MathTex("R_C").scale(0.75).next_to(rc, direction=LEFT)
        self.play(ReplacementTransform(temp_short, rc), FadeIn(rc_text))
        self.wait()

        icrc = MathTex("i_C\\,R_C", color=BLUE).scale(0.75).next_to(rc)
        plusmin = VGroup(MathTex("+"), MathTex("-")).arrange_submobjects(DOWN, buff=1).move_to(icrc).shift(UP * 0.1)
        self.play(ReplacementTransform(ic[0], icrc), FadeOut(ic_arrow), FadeIn(plusmin))
        self.play(FadeOut(bjtamp.elements[1][-3:]))
        self.wait()

        vce_term = Line(bjtamp.collector(), bjtamp.collector() + 2 * RIGHT)
        op_node = vce_term.points[-1]
        vce_term.add(Dot(op_node))
        vce_gnd = Ground().next_to(vce_term.points[-1], direction=DOWN).align_to(bjtamp.elements[-1], direction=UP)
        vce_gnd.add(Dot(vce_gnd.get_top()))
        vce_text = MathTex("v_C", " = V_{CC} -").scale(0.75).set_color_by_tex("v_C", YELLOW)
        vo_text = MathTex("v_C", " = V_{CC} -", "i_C R_C").set_color_by_tex("v_C", YELLOW).set_color_by_tex("i_C R_C", BLUE).next_to(bjt_eqn, direction=DOWN)

        self.play(
            plusmin[0].animate.next_to(op_node, direction=DOWN, buff=0.5),
            plusmin[-1].animate.next_to(vce_gnd, direction=UP, buff=0.5),
        )
        vce_text.move_to(plusmin).shift(LEFT * 0.5)

        self.play(
            *[FadeIn(m) for m in [vce_term, vce_gnd, vce_text]]
        )
        self.play(icrc.animate.next_to(vce_text, buff=0.1))
        self.play(TransformFromCopy(vce_text, vo_text))
        self.wait()


class SS1(MovingCameraScene):
    def construct(self):
        title = MathTex("v_C", " = V_{CC} - R_C \\,\\, I_s \\, e^{(", "v_{BE}", "/V_t)}").to_corner(UR).scale(0.9)
        title.set_color_by_tex("v_C", YELLOW)
        title.set_color_by_tex("v_{BE}", GREEN)
        self.play(FadeIn(title))

        temp_axis = Axes(
            x_range=[-0.1, 1, 0.25],
            y_range=[-2, 11, 2],
            x_length=10,
            # y_length=14,
            x_axis_config={
                "include_tip": False
            },
            y_axis_config={
                "include_tip": False
            }
        ).add_coordinates().to_edge(LEFT)

        temp_axis_labels = temp_axis.get_axis_labels(x_label=MathTex("v_{BE}", color=GREEN), y_label=MathTex("v_C", color=YELLOW))
        temp_axis.add(temp_axis_labels)
        self.Rc = 1e3

        def diode_func(x):

            vce = 10 - self.Rc * 1e-12 * exp(x / 0.025)
            if vce > 0:
                return vce

            elif vce <= 0:
                return 0

        x_lim = 0.025 * log(10 / (1e-12 * self.Rc))
        diode_eqn_temp = temp_axis.plot(diode_func, x_range=[0, x_lim, 0.001], color=BLUE)

        self.play(Create(temp_axis))
        self.play(Create(diode_eqn_temp))

        marker_pts = [temp_axis.i2gp(0.5, diode_eqn_temp), temp_axis.i2gp(x_lim, diode_eqn_temp)]
        marker_dots = VGroup(*[
            Dot(pt, color=BLUE)
            for pt in marker_pts
        ])
        marker_lines = VGroup(*[
            DashedLine(ORIGIN, UP * 5.5).next_to(pt, direction=UP, buff=0)
            for pt in [temp_axis.c2p(0.5, 0), temp_axis.c2p(x_lim, 0)]
        ])
        marker_text = VGroup(Text("A").scale(0.75).next_to(marker_dots[0], direction=UR, buff=0.1), Text("B").scale(0.75).next_to(marker_dots[1], direction=UR))
        markers = VGroup(marker_dots, marker_lines, marker_text)
        regions = VGroup(*[Tex(t) for t in ["Cutoff", "Active", "Saturation"]])
        regions[0].next_to(marker_lines[0], direction=LEFT, buff=1)
        regions[1].rotate(PI / 2).next_to(marker_lines[0], buff=0.1).add_background_rectangle()
        regions[2].next_to(marker_lines[1], buff=1)

        self.play(FadeIn(marker_dots), FadeIn(marker_text))
        self.play(
            *[Create(m) for m in marker_lines]
        )
        for m in regions:
            self.play(FadeIn(m))
        axis = Axes(
            x_range=[0.35, 0.65, 0.05],
            y_range=[-0.25, 11, 1],
            x_length=10,
            y_length=7,
            x_axis_config={
                "include_tip": False,
            },
            y_axis_config={
                "include_tip": False
            }
        ).add_coordinates()
        axis_labels = axis.get_axis_labels(x_label=MathTex("v_{BE}", color=GREEN), y_label=MathTex("v_C", color=YELLOW))
        axis.add(axis_labels)
        diode_eqn = axis.plot(diode_func, x_range=[0.35, x_lim, 0.0001], color=BLUE)

        self.play(
            ReplacementTransform(temp_axis, axis),
            ReplacementTransform(diode_eqn_temp, diode_eqn),
            FadeOut(regions, marker_lines),
            marker_dots[0].animate.move_to(axis.i2gp(0.5, diode_eqn)),
            marker_dots[1].animate.move_to(axis.i2gp(x_lim, diode_eqn)),
            marker_text[0].animate.next_to(axis.i2gp(0.5, diode_eqn), direction=UR),
            marker_text[1].animate.next_to(axis.i2gp(x_lim, diode_eqn), direction=UR),

        )
        self.wait()

        self.q_point = 0.55  # 0.56
        small_sig_amp = 0.02
        q_point_in_graph = axis.i2gp(self.q_point, diode_eqn)
        q_point_dot = Dot(q_point_in_graph, color=ORANGE)

        dot = q_point_dot.copy()  # .set_color(YELLOW)
        upper_dummy_dot = Dot(axis.i2gp(self.q_point + small_sig_amp, diode_eqn)).scale(0.001)
        lower_dummy_dot = Dot(axis.i2gp(self.q_point - small_sig_amp, diode_eqn)).scale(0.001)
        dots = VGroup(q_point_dot, upper_dummy_dot, lower_dummy_dot)

        self.t, self.x, self.f = 0, 0, 2

        temp_amp = 0.0075

        def q_point_updater(q_point, dt):
            self.t += dt
            self.x = self.q_point + temp_amp * np.sin(self.t)
            q_point.move_to(axis.i2gp(self.x, diode_eqn))

        def upper_dummy_updater(q_point, dt):
            x = self.q_point + small_sig_amp + temp_amp * np.sin(self.t)
            upper_dummy_dot.move_to(axis.i2gp(x, diode_eqn))

        def lower_dummy_updater(q_point, dt):
            x = self.q_point - small_sig_amp + temp_amp * np.sin(self.t)
            lower_dummy_dot.move_to(axis.i2gp(x, diode_eqn))

        def lim_line_updater(line):
            new_line = axis.get_lines_to_point(q_point_dot.get_center())
            line.become(new_line)

        x_lim_nos = [self.q_point, self.q_point + small_sig_amp, self.q_point - small_sig_amp]

        up_lim_line = axis.get_lines_to_point(upper_dummy_dot.get_center()).add_updater(lambda x: x.become(axis.get_lines_to_point(upper_dummy_dot.get_center())))
        low_lim_line = axis.get_lines_to_point(lower_dummy_dot.get_center()).add_updater(lambda x: x.become(axis.get_lines_to_point(lower_dummy_dot.get_center())))
        q_point_lim_line = axis.get_lines_to_point(q_point_dot.get_center()).add_updater(lambda x: x.become(axis.get_lines_to_point(q_point_dot.get_center())))
        lim_lines = VGroup(up_lim_line, low_lim_line, q_point_lim_line)

        temp_grp = VGroup(*[*dots, *lim_lines])

        self.play(*[Create(mobj) for mobj in temp_grp])

        def get_horizontally_moving_tracing(dot, color, stroke_width=3, rate=0.25):
            path = VMobject()
            path.set_stroke(color, stroke_width)
            path.start_new_path(np.array([axis.c2p(self.q_point - small_sig_amp, 0)[0], dot.get_center()[1], 0]))
            path.Vector = Vector

            def update_path(p, dt):
                p.shift(rate * dt * 3 * (LEFT))
                p.add_smooth_curve_to(np.array([axis.c2p(self.q_point - small_sig_amp, 0)[0], dot.get_center()[1], 0]))
            path.add_updater(update_path)
            return path

        def get_vertically_moving_tracing(dot, color, stroke_width=3, rate=0.25):
            path = VMobject()
            path.set_stroke(color, stroke_width)
            path.start_new_path(np.array([dot.get_center()[0], axis.i2gp(self.q_point + small_sig_amp, diode_eqn)[1], 0]))
            # path.start_new_path(dot.get_center())
            path.Vector = Vector

            def update_path(p, dt):
                p.shift(rate * dt * 3 * DOWN)
                p.add_smooth_curve_to(np.array([dot.get_center()[0], axis.i2gp(self.q_point + small_sig_amp, diode_eqn)[1], 0]))
            path.add_updater(update_path)
            return path

        x_mark, y_mark = Dot(color=GREEN), Dot(color=YELLOW)

        def x_mark_updater(x_mark):
            x_mark.move_to(ip_path.points[-1])

        def y_mark_updater(y_mark):
            y_mark.move_to(op_path.points[-1])

        ip_path = get_vertically_moving_tracing(dot, GREEN)
        op_path = get_horizontally_moving_tracing(dot, YELLOW)
        x_mark.add_updater(x_mark_updater)
        y_mark.add_updater(y_mark_updater)

        def dot_updater(dot, dt):
            self.t += 5 * dt
            self.x = self.q_point + small_sig_amp * np.sin(self.t)
            # y = diode_func(x)
            dot.move_to(axis.i2gp(self.x, diode_eqn))

        dot.add_updater(dot_updater)
        self.play(GrowFromCenter(dot), FadeOut(q_point_dot))
        self.add(dot, op_path, ip_path, x_mark, y_mark)
        self.wait(20)


class SS_linear(MovingCameraScene):
    def construct(self):
        # title = MathTex("v_C", " = V_{CC} - R_C \\,\\, I_s \\, e^{(", "v_{BE}", "/V_t)}").to_corner(UR).scale(0.9)
        # title.set_color_by_tex("v_C", YELLOW)
        # title.set_color_by_tex("v_{BE}", GREEN)
        # self.play(FadeIn(title))

        # temp_axis = Axes(
        #     x_range=[-0.1, 1, 0.25],
        #     y_range=[-2, 11, 2],
        #     x_length=10,
        #     # y_length=14,
        #     x_axis_config={
        #         "include_tip": False
        #     },
        #     y_axis_config={
        #         "include_tip": False
        #     }
        # ).add_coordinates().to_edge(LEFT)

        # temp_axis_labels = temp_axis.get_axis_labels(x_label=MathTex("v_{BE}", color=GREEN), y_label=MathTex("v_C", color=YELLOW))
        # temp_axis.add(temp_axis_labels)
        self.Rc = 1e3

        def diode_func(x):

            vce = 10 - self.Rc * 1e-12 * exp(x / 0.025)
            if vce > 0:
                return vce

            elif vce <= 0:
                return 0

        def line_func(x):
            x_lim = 0.025 * log(10 / (1e-12 * self.Rc))
            y1 = diode_func(0.5)
            y2 = diode_func(x_lim)
            line = y1 + (y2 - y1) * (x - 0.5) / (x_lim - 0.5)  # *  + (1 - x) * diode_func(x_lim)
            return line
            # if vce > 0:
            #     return vce

            # elif vce <= 0:
            #     return 0

        x_lim = 0.025 * log(10 / (1e-12 * self.Rc))
        # diode_eqn_temp = temp_axis.plot(diode_func, x_range=[0, x_lim, 0.001], color=BLUE)

        # self.play(Create(temp_axis))
        # self.play(Create(diode_eqn_temp))

        # self.play(FadeIn(marker_dots), FadeIn(marker_text))
        # self.play(
        #     *[Create(m) for m in marker_lines]
        # )
        # for m in regions:
        #     self.play(FadeIn(m))
        axis = Axes(
            x_range=[0.35, 0.65, 0.05],
            y_range=[-0.25, 11, 1],
            x_length=10,
            y_length=7,
            x_axis_config={
                "include_tip": False,
            },
            y_axis_config={
                "include_tip": False
            }
        ).add_coordinates()
        axis_labels = axis.get_axis_labels(x_label=MathTex("v_{BE}", color=GREEN), y_label=MathTex("v_C", color=YELLOW))
        axis.add(axis_labels)
        diode_eqn = axis.plot(diode_func, x_range=[0.35, x_lim, 0.0001], color=BLUE)
        line = axis.plot(line_func, x_range=[0.5, x_lim, 0.0001], color=BLUE)

        self.add(axis)
        self.add(line)

        marker_pts = [axis.i2gp(0.5, diode_eqn), axis.i2gp(x_lim, diode_eqn)]
        marker_dots = VGroup(*[
            Dot(pt, color=BLUE)
            for pt in marker_pts
        ])

        marker_text = VGroup(Text("A").scale(0.75).next_to(marker_dots[0], direction=UR, buff=0.1), Text("B").scale(0.75).next_to(marker_dots[1], direction=UR))
        markers = VGroup(marker_dots, marker_text)

        # marker_dots[0].move_to(axis.i2gp(0.5, diode_eqn)),
        # marker_dots[1].move_to(axis.i2gp(x_lim, diode_eqn)),
        marker_text[0].next_to(axis.i2gp(0.5, diode_eqn), direction=UR),
        marker_text[1].next_to(axis.i2gp(x_lim, diode_eqn), direction=UR),
        self.add(markers)
        self.q_point = 0.55  # 0.56
        small_sig_amp = 0.02
        q_point_in_graph = axis.i2gp(self.q_point, line)
        q_point_dot = Dot(q_point_in_graph, color=ORANGE)

        dot = q_point_dot.copy()  # .set_color(YELLOW)
        upper_dummy_dot = Dot(axis.i2gp(self.q_point + small_sig_amp, line)).scale(0.001)
        lower_dummy_dot = Dot(axis.i2gp(self.q_point - small_sig_amp, line)).scale(0.001)
        dots = VGroup(q_point_dot, upper_dummy_dot, lower_dummy_dot)

        self.t, self.x, self.f = 0, 0, 2

        temp_amp = 0.0075

        def q_point_updater(q_point, dt):
            self.t += dt
            self.x = self.q_point + temp_amp * np.sin(self.t)
            q_point.move_to(axis.i2gp(self.x, line))

        def upper_dummy_updater(q_point, dt):
            x = self.q_point + small_sig_amp + temp_amp * np.sin(self.t)
            upper_dummy_dot.move_to(axis.i2gp(x, line))

        def lower_dummy_updater(q_point, dt):
            x = self.q_point - small_sig_amp + temp_amp * np.sin(self.t)
            lower_dummy_dot.move_to(axis.i2gp(x, line))

        def lim_line_updater(line):
            new_line = axis.get_lines_to_point(q_point_dot.get_center())
            line.become(new_line)

        x_lim_nos = [self.q_point, self.q_point + small_sig_amp, self.q_point - small_sig_amp]

        up_lim_line = axis.get_lines_to_point(upper_dummy_dot.get_center()).add_updater(lambda x: x.become(axis.get_lines_to_point(upper_dummy_dot.get_center())))
        low_lim_line = axis.get_lines_to_point(lower_dummy_dot.get_center()).add_updater(lambda x: x.become(axis.get_lines_to_point(lower_dummy_dot.get_center())))
        q_point_lim_line = axis.get_lines_to_point(q_point_dot.get_center()).add_updater(lambda x: x.become(axis.get_lines_to_point(q_point_dot.get_center())))
        lim_lines = VGroup(up_lim_line, low_lim_line, q_point_lim_line)

        temp_grp = VGroup(*[*dots, *lim_lines])

        self.play(*[Create(mobj) for mobj in temp_grp])

        def get_horizontally_moving_tracing(dot, color, stroke_width=3, rate=0.25):
            path = VMobject()
            path.set_stroke(color, stroke_width)
            path.start_new_path(np.array([axis.c2p(self.q_point - small_sig_amp, 0)[0], dot.get_center()[1], 0]))
            path.Vector = Vector

            def update_path(p, dt):
                p.shift(rate * dt * 3 * (LEFT))
                p.add_smooth_curve_to(np.array([axis.c2p(self.q_point - small_sig_amp, 0)[0], dot.get_center()[1], 0]))
            path.add_updater(update_path)
            return path

        def get_vertically_moving_tracing(dot, color, stroke_width=3, rate=0.25):
            path = VMobject()
            path.set_stroke(color, stroke_width)
            path.start_new_path(np.array([dot.get_center()[0], axis.i2gp(self.q_point + small_sig_amp, line)[1], 0]))
            # path.start_new_path(dot.get_center())
            path.Vector = Vector

            def update_path(p, dt):
                p.shift(rate * dt * 3 * DOWN)
                p.add_smooth_curve_to(np.array([dot.get_center()[0], axis.i2gp(self.q_point + small_sig_amp, line)[1], 0]))
            path.add_updater(update_path)
            return path

        x_mark, y_mark = Dot(color=GREEN), Dot(color=YELLOW)

        def x_mark_updater(x_mark):
            x_mark.move_to(ip_path.points[-1])

        def y_mark_updater(y_mark):
            y_mark.move_to(op_path.points[-1])

        ip_path = get_vertically_moving_tracing(dot, GREEN)
        op_path = get_horizontally_moving_tracing(dot, YELLOW)
        x_mark.add_updater(x_mark_updater)
        y_mark.add_updater(y_mark_updater)

        def dot_updater(dot, dt):
            self.t += 5 * dt
            self.x = self.q_point + small_sig_amp * np.sin(self.t)
            # y = diode_func(x)
            dot.move_to(axis.i2gp(self.x, line))

        dot.add_updater(dot_updater)
        self.play(GrowFromCenter(dot), FadeOut(q_point_dot))
        self.add(dot, op_path, ip_path, x_mark, y_mark)
        self.wait(15)


class SS2(MovingCameraScene):
    def construct(self):
        title = MathTex("v_C", " = V_{CC} - R_C \\,\\, I_s \\, e^{(", "v_{BE}", "/V_t)}").to_corner(UR).scale(0.9)
        title.set_color_by_tex("v_C", YELLOW)
        title.set_color_by_tex("v_{BE}", GREEN)
        self.play(FadeIn(title))

        temp_axis = Axes(
            x_range=[-0.1, 1, 0.25],
            y_range=[-2, 11, 2],
            x_length=10,
            # y_length=14,
            x_axis_config={
                "include_tip": False
            },
            y_axis_config={
                "include_tip": False
            }
        ).add_coordinates().to_edge(LEFT)

        temp_axis_labels = temp_axis.get_axis_labels(x_label=MathTex("v_{BE}", color=GREEN), y_label=MathTex("v_C", color=YELLOW))
        temp_axis.add(temp_axis_labels)
        self.Rc = 1e3

        def diode_func(x):

            vce = 10 - self.Rc * 1e-12 * exp(x / 0.025)
            # vds =
            if vce > 0:
                return vce
            # elif vce <= 0.3 and vce >= 0:
            #     return 1e-10 * vce
            elif vce <= 0:
                return 0

        x_lim = 0.025 * log(10 / (1e-12 * self.Rc))
        diode_eqn_temp = temp_axis.plot(diode_func, x_range=[0, x_lim, 0.001], color=BLUE)

        self.play(Create(temp_axis))
        self.play(Create(diode_eqn_temp))

        marker_pts = [temp_axis.i2gp(0.5, diode_eqn_temp), temp_axis.i2gp(x_lim, diode_eqn_temp)]
        marker_dots = VGroup(*[
            Dot(pt, color=BLUE)
            for pt in marker_pts
        ])
        marker_lines = VGroup(*[
            DashedLine(ORIGIN, UP * 5.5).next_to(pt, direction=UP, buff=0)
            for pt in [temp_axis.c2p(0.5, 0), temp_axis.c2p(x_lim, 0)]
        ])
        marker_text = VGroup(Text("A").scale(0.75).next_to(marker_dots[0], direction=UR, buff=0.1), Text("B").scale(0.75).next_to(marker_dots[1], direction=UR))
        markers = VGroup(marker_dots, marker_lines, marker_text)
        regions = VGroup(*[Tex(t) for t in ["Cutoff", "Active", "Saturation"]])
        regions[0].next_to(marker_lines[0], direction=LEFT, buff=1)
        regions[1].rotate(PI / 2).next_to(marker_lines[0], buff=0.1).add_background_rectangle()
        regions[2].next_to(marker_lines[1], buff=1)

        self.play(FadeIn(marker_dots), FadeIn(marker_text))
        self.play(
            *[Create(m) for m in marker_lines]
        )
        for m in regions:
            self.play(FadeIn(m))
        axis = Axes(
            x_range=[0.35, 0.65, 0.05],
            # x_range=[0, 0.8, 0.1],
            y_range=[-0.25, 11, 1],
            x_length=10,
            y_length=7,
            x_axis_config={
                "include_tip": False,
            },
            y_axis_config={
                "include_tip": False
            }
        ).add_coordinates()
        axis_labels = axis.get_axis_labels(x_label=MathTex("v_{BE}", color=GREEN), y_label=MathTex("v_C", color=YELLOW))
        axis.add(axis_labels)
        diode_eqn = axis.plot(diode_func, x_range=[0.35, x_lim, 0.0001], color=BLUE)

        self.play(
            ReplacementTransform(temp_axis, axis),
            ReplacementTransform(diode_eqn_temp, diode_eqn),
            FadeOut(regions, marker_lines),
            marker_dots[0].animate.move_to(axis.i2gp(0.5, diode_eqn)),
            marker_dots[1].animate.move_to(axis.i2gp(x_lim, diode_eqn)),
            marker_text[0].animate.next_to(axis.i2gp(0.5, diode_eqn), direction=UR),
            marker_text[1].animate.next_to(axis.i2gp(x_lim, diode_eqn), direction=UR),
            # ReplacementTransform(temp_axis_labels, axis_labels),
            # self.camera.frame.animate.shift(DOWN * 4)  # .scale(2),
        )
        self.wait()

        self.q_point = 0.56
        small_sig_amp = 0.002
        q_point_in_graph = axis.i2gp(self.q_point, diode_eqn)
        q_point_dot = Dot(q_point_in_graph, color=ORANGE)

        # self.play(
        # self.camera.frame.animate.move_to(q_point_in_graph + LEFT),
        # axis.x_axis.animate.move_to(np.array([axis.x_axis.get_center()[0], q_point_dot.get_center()[1] - 3, 0]))
        # )  # .scale(2)

        # self.add(axis1, diode_eqn_1)
        # self.play(Transform(axis1, axis2), Transform(diode_eqn_1, diode_eqn_2))
        # self.wait()

        dot = q_point_dot.copy()  # .set_color(YELLOW)
        upper_dummy_dot = Dot(axis.i2gp(self.q_point + small_sig_amp, diode_eqn)).scale(0.001)
        lower_dummy_dot = Dot(axis.i2gp(self.q_point - small_sig_amp, diode_eqn)).scale(0.001)
        dots = VGroup(q_point_dot, upper_dummy_dot, lower_dummy_dot)

        self.t, self.x, self.f = 0, 0, 2
        # rd = 0.025 / diode_func(self.q_point)
        # print(rd)
        # self.op_amp = (diode_func(self.q_point + small_sig_amp) - diode_func(self.q_point - small_sig_amp)) / 2

        temp_amp = 0.0075

        def q_point_updater(q_point, dt):
            self.t += dt
            self.x = self.q_point + temp_amp * np.sin(self.t)
            # y = diode_func(x)
            q_point.move_to(axis.i2gp(self.x, diode_eqn))
            # self.camera.frame.move_to(q_point.get_center() + LEFT)
            # axis.x_axis.move_to(np.array([axis.x_axis.get_center()[0], q_point_dot.get_center()[1] - 3, 0]))

        def upper_dummy_updater(q_point, dt):
            x = self.q_point + small_sig_amp + temp_amp * np.sin(self.t)
            upper_dummy_dot.move_to(axis.i2gp(x, diode_eqn))

        def lower_dummy_updater(q_point, dt):
            x = self.q_point - small_sig_amp + temp_amp * np.sin(self.t)
            lower_dummy_dot.move_to(axis.i2gp(x, diode_eqn))

        def lim_line_updater(line):
            new_line = axis.get_lines_to_point(q_point_dot.get_center())
            line.become(new_line)

        x_lim_nos = [self.q_point, self.q_point + small_sig_amp, self.q_point - small_sig_amp]

        up_lim_line = axis.get_lines_to_point(upper_dummy_dot.get_center()).add_updater(lambda x: x.become(axis.get_lines_to_point(upper_dummy_dot.get_center())))
        low_lim_line = axis.get_lines_to_point(lower_dummy_dot.get_center()).add_updater(lambda x: x.become(axis.get_lines_to_point(lower_dummy_dot.get_center())))
        q_point_lim_line = axis.get_lines_to_point(q_point_dot.get_center()).add_updater(lambda x: x.become(axis.get_lines_to_point(q_point_dot.get_center())))
        lim_lines = VGroup(up_lim_line, low_lim_line, q_point_lim_line)
        tgt_line = Line(LEFT, RIGHT, color=ORANGE, stroke_width=3).put_start_and_end_on(upper_dummy_dot.get_center(), lower_dummy_dot.get_center() + DOWN * 0.000000001)

        def tgt_line_updater(tgt):
            tgt.move_to(q_point_dot)
            x = axis.p2c(q_point_dot.get_center())[0]
            y0 = axis.i2gp(x, diode_eqn)
            y1 = axis.i2gp(x + 1e-12, diode_eqn)
            tgt.put_start_and_end_on(
                axis.i2gp(x, diode_eqn),
                axis.i2gp(x + 1e-12, diode_eqn)
            )
            tgt_line.scale(2e10)
            # tgt.slope = (y1[1] - y0[1]) / 1e-12
            tgt.slope = (diode_func(x + 1e-12) - diode_func(x)) / 1e-12
            # tgt.slope = 1

        slope_text = MathTex("\\dfrac{\\Delta v_c}{\\Delta v_{be}} = ")
        slope_val = DecimalNumber(0).add_updater(lambda x: x.set_value(tgt_line.slope))
        slope_mobj = VGroup(slope_text, slope_val).arrange_submobjects(direction=RIGHT).next_to(q_point_dot, buff=1)

        self.play(Write(slope_text))
        temp_grp = VGroup(*[*dots, *lim_lines, tgt_line, slope_val])

        self.play(*[Create(mobj) for mobj in temp_grp[:-1]])

        q_point_dot.add_updater(q_point_updater)
        upper_dummy_dot.add_updater(upper_dummy_updater)
        lower_dummy_dot.add_updater(lower_dummy_updater)
        tgt_line.add_updater(tgt_line_updater)

        self.add(*temp_grp)
        self.wait(2 * PI)

        for mobj in [*dots, *lim_lines]:
            mobj.clear_updaters()

        self.wait()

        def get_horizontally_moving_tracing(dot, color, stroke_width=3, rate=0.25):
            path = VMobject()
            path.set_stroke(color, stroke_width)
            path.start_new_path(np.array([axis.c2p(self.q_point - small_sig_amp, 0)[0], dot.get_center()[1], 0]))
            path.Vector = Vector

            def update_path(p, dt):
                p.shift(rate * dt * 3 * (LEFT))
                p.add_smooth_curve_to(np.array([axis.c2p(self.q_point - small_sig_amp, 0)[0], dot.get_center()[1], 0]))
            path.add_updater(update_path)
            return path

        def get_vertically_moving_tracing(dot, color, stroke_width=3, rate=0.25):
            path = VMobject()
            path.set_stroke(color, stroke_width)
            path.start_new_path(np.array([dot.get_center()[0], axis.i2gp(self.q_point + small_sig_amp, diode_eqn)[1], 0]))
            # path.start_new_path(dot.get_center())
            path.Vector = Vector

            def update_path(p, dt):
                p.shift(rate * dt * 3 * DOWN)
                # p.add_smooth_curve_to(np.array([dot.get_center()[0], self.q_point - 0.005, 0]))
                p.add_smooth_curve_to(np.array([dot.get_center()[0], axis.i2gp(self.q_point + small_sig_amp, diode_eqn)[1], 0]))
            path.add_updater(update_path)
            return path

        x_mark, y_mark = Dot(color=GREEN), Dot(color=YELLOW)

        def x_mark_updater(x_mark):
            x_mark.move_to(ip_path.points[-1])

        def y_mark_updater(y_mark):
            y_mark.move_to(op_path.points[-1])

        ip_path = get_vertically_moving_tracing(dot, GREEN)
        op_path = get_horizontally_moving_tracing(dot, YELLOW)
        x_mark.add_updater(x_mark_updater)
        y_mark.add_updater(y_mark_updater)

        def dot_updater(dot, dt):
            self.t += 5 * dt
            self.x = self.q_point + small_sig_amp * np.sin(self.t)
            # y = diode_func(x)
            dot.move_to(axis.i2gp(self.x, diode_eqn))

        # op_path = axis.plot(lambda x: self.op_amp * np.sin(self.f * self.q_point * 2 * PI * x / self.q_point) + diode_func(self.q_point), x_range=[0, 1])
        # op_path = axis.plot(, x_range=[0,1])

        # def op_path_updater(op_path):
        #     op_path.become(
        #         axis.plot(lambda x: self.op_amp * np.sin(self.f * self.q_point * 2 * PI * x / self.q_point) + diode_func(self.q_point), x_range=[0, self.x])
        #     )

        dot.add_updater(dot_updater)
        # op_path.add_updater(op_path_updater)
        self.play(GrowFromCenter(dot), FadeOut(q_point_dot))
        self.add(dot, op_path, ip_path, x_mark, y_mark)
        self.wait(20)


class SSExpln(Scene):
    def construct(self):
        ip = MathTex("v_{BE}(t)", "=", " V_{BE}", " +", " v_{be}(t)")
        for i, c in zip(ip[::2], [GREEN, GREEN_A, GREEN_B]):
            i.set_color(c)

        op1 = VGroup(
            MathTex("= I_s \\,e^{v_{BE}/V_t}"),
            MathTex("= I_s \\,e^{(V_{BE}+v_{be})/V_t}"),
            MathTex("= I_s \\quad e^{V_{BE}/V_t}", "\\, e^{v_{be}/V_t}"),
            MathTex("= I_C\\, e^{v_{be}/V_t}"),
            MathTex("= I_C \\, \\bigg( 1 + \\dfrac{v_{be}}{V_t} \\bigg)"),
        ).arrange_submobjects(direction=DOWN)

        for o in op1[1:]:
            o.align_to(op1[0].get_left(), direction=LEFT)

        for o in op1[:-1]:
            if o is not op1[2]:
                o[0][4:].scale(0.75).next_to(o[0][3], direction=UR, buff=0)
            else:
                o[0][4:12].scale(0.75).next_to(o[0][3], direction=UR, buff=0)
                o[1][1:].scale(0.75).next_to(o[1][0], direction=UR, buff=0)

        op1.shift(LEFT * 3 + UP * 0.3)

        IC_box = SurroundingRectangle(op1[2][0][1:12])
        ic = MathTex("i_C ")
        ic.next_to(op1[0], direction=LEFT)

        op2 = VGroup(
            MathTex("= I_C \\, \\bigg( 1 + \\dfrac{v_{be}}{V_t} \\bigg)"),
            MathTex("= I_C + I_C\\dfrac{v_{be}}{V_t}"),
            MathTex("= I_C + ", "\\dfrac{I_C}{V_t}", "\\,v_{be}"),
            MathTex("= I_C + ", "g_m", "\\,v_{be}").set_color_by_tex("g_m", YELLOW)
        ).arrange_submobjects(direction=DOWN)

        op2[0].next_to(ic)

        # gm = MathTex("gm = \\dfrac{I_C}{V_t}", color=YELLOW).move_to(op1[0])

        for o in op2[1:]:
            o.align_to(op1[0].get_left(), direction=LEFT)

        taylor = MathTex("e^{v_{be}/V_t} = 1 + \\dfrac{(v_{be}/V_t)}{1!}", " + \\dfrac{(v_{be}/V_t)^2}{2!} + \\dfrac{(v_{be}/V_t)^3}{3!} + .\\,.\\,.\\,")
        taylor.next_to(op1[-2], direction=DOWN).align_to(op1[-2].get_left(), direction=LEFT).shift(LEFT * 0.2)
        ss_condition = MathTex("v_{be}<<V_t")

        vbe_axis = Axes(
            x_range=[-0.1, 2, 0.5],
            # x_range=[0, 0.8, 0.1],
            y_range=[-0.1, 1, 0.25],
            x_length=5,
            y_length=3,
            x_axis_config={
                "include_tip": False,
            },
            y_axis_config={
                "include_tip": False
            }
        ).to_corner(UR)
        vbe_axis_labels = vbe_axis.get_axis_labels(x_label=MathTex("t", color=WHITE), y_label=MathTex("v_{BE}", color=GREEN))
        vbe_axis.add(vbe_axis_labels)
        x_lim = 1.5
        vbe_plot = vbe_axis.plot(lambda vbe: 0.1 * np.sin(15 * vbe), x_range=[0, x_lim], color=GREEN_B)
        vBE_plot = vbe_axis.plot(lambda vbe: 0.1 * np.sin(15 * vbe) + 0.56, x_range=[0, x_lim], color=GREEN)
        VBE_plot = DashedLine(stroke_width=1, color=GREEN_A).set_width(0.75 * vbe_axis.x_axis.get_width())\
            .move_to(vbe_axis.c2p(2.1 / 2, 0)).align_to(vbe_axis.c2p(0, 0.56), direction=LEFT)
        vbe = VGroup(
            MathTex("V_{BE}", color=GREEN_A).scale(0.7).next_to(vbe_axis.c2p(0, 0.56), direction=LEFT),
            MathTex("v_{be}(t)", color=GREEN_B).next_to(vbe_plot.get_right(), direction=UR),
            MathTex("v_{BE}(t)", color=GREEN).scale(0.7).next_to(vBE_plot.get_right())
        )

        ip.next_to(vbe_axis, direction=LEFT, buff=2)
        self.play(Create(vbe_axis))

        self.play(
            VBE_plot.animate.move_to(vbe_axis.c2p(2.1 / 2, 1.1 / 2)).align_to(vbe_axis.c2p(0, 0.56), direction=LEFT),
            Write(vbe[0]), Write(ip[2])
        )
        self.wait()
        self.play(Create(vbe_plot), Write(vbe[1]), Write(ip[-1]))
        self.wait()
        self.play(ReplacementTransform(vbe_plot, vBE_plot), ReplacementTransform(vbe[1], vbe[-1]), Write(ip[0:2]), Write(ip[3]))
        self.wait()
        self.play(ip.animate.to_corner(UL))
        self.wait()
        self.play(Write(ic))

        for i in range(len(op1[:-2])):
            if i == 0:
                self.play(Write(op1[i]))
            else:
                self.play(TransformFromCopy(op1[i - 1], op1[i]))

        self.play(Create(IC_box))
        line3 = op1[3][0]
        self.play(Write(line3[0]), TransformFromCopy(op1[2][0][1:12], line3[1:3]), FadeOut(IC_box))
        self.wait()
        self.play(TransformFromCopy(op1[2][1], line3[3:]))
        self.wait()
        ss_condition.next_to(taylor, direction=DOWN)
        self.play(Write(taylor))
        self.wait()
        self.play(Write(ss_condition))
        self.wait()
        self.play(FadeOut(taylor[1]))
        self.wait()

        self.play(TransformFromCopy(VGroup(taylor[0], op1[-2]), op1[-1]), FadeOut(taylor[0], ss_condition))
        self.play(FadeOut(op1[:-1]), op1[-1].animate.move_to(op2[0]))
        self.wait()

        self.remove(op1[-1])
        self.add(op2[0])

        for i in range(1, len(op2[1:])):
            self.play(TransformFromCopy(op2[i - 1], op2[i]))
            self.wait()

        self.play(
            FocusOn(op2[-2][1]),
            op2[-2][1].animate.set_color(YELLOW)
        )
        self.play(Write(op2[-1]))
        self.wait()
        self.play(FadeOut(op2[:-1]), op2[-1].animate.next_to(ic))
        self.wait()

        transcon = Tex(r"Transconductance", color=YELLOW).next_to(op2[-1][1], direction=DOWN)
        self.play(Write(transcon))
        self.play(FadeOut(transcon))

        op3 = VGroup(
            MathTex("i_C = I_C +", " \\,i_c"),
        ).next_to(op2[-1], direction=DOWN, buff=0.3).align_to(ic, direction=LEFT)
        op4 = VGroup(
            MathTex("v_C = V_{CC} - i_C R_C"),
            MathTex("v_C = V_{CC} - (I_C + i_c)R_C"),
            MathTex("V_C + v_c", " = V_{CC} - I_C R_C", " - i_c R_C"),
            MathTex("V_C", "= V_{CC} - I_C R_C").set_color_by_tex("V_C", RED_A),
            MathTex("v_c", "= - i_c", "\\,R_C").set_color_by_tex("v_c", RED_B),
            MathTex("v_c", " =- ", "g_m", " v_{be}", "\\,R_C",).set_color_by_tex("g_m", YELLOW).set_color_by_tex("v_{be}", GREEN_B),
        ).arrange_submobjects(direction=DOWN, buff=0.3).next_to(op3, direction=DOWN, buff=0.6)
        for s, c in zip(["v_c", "g_m", "v_{be}"], [RED_B, YELLOW, GREEN_B]):
            op4[-1].set_color_by_tex(s, c)
        # op4[-1][-1].set_color(RED_B)
        for o in op4:
            o.align_to(op3.get_left(), direction=LEFT)

        op4[2][1].align_to(op4[0][0][2].get_left(), direction=LEFT)
        op4[2][0].next_to(op4[2][1], direction=LEFT)
        op4[2][-1].next_to(op4[2][1])
        temp_grp = VGroup(*op4[3:5]).shift(DOWN * 0.5)  # .arrange_submobjects(direction=RIGHT, buff=3).next_to(op4[2], direction=DOWN, buff=0.75)

        vc_axis = Axes(
            x_range=[-0.1, 2, 0.5],
            # x_range=[0, 0.8, 0.1],
            y_range=[-0.1, 1, 0.25],
            x_length=5,
            y_length=3,
            x_axis_config={
                "include_tip": False,
            },
            y_axis_config={
                "include_tip": False
            }
        ).to_corner(DR)
        vc_axis_labels = vc_axis.get_axis_labels(x_label=MathTex("t", color=WHITE), y_label=MathTex("v_{C}", color=RED))
        vc_axis.add(vc_axis_labels)
        x_lim = 1.5
        vc_plot = vc_axis.plot(lambda vc: -0.4 * np.sin(15 * vc), x_range=[0, x_lim], color=RED_B)
        vC_plot = vc_axis.plot(lambda vc: -0.4 * np.sin(15 * vc) + 0.5, x_range=[0, x_lim], color=RED)
        VC_plot = DashedLine(stroke_width=1, color=RED_A).set_width(0.75 * vc_axis.x_axis.get_width())\
            .move_to(vc_axis.c2p(2.1 / 2, 0)).align_to(vc_axis.c2p(0, 0.5), direction=LEFT)
        vc = VGroup(
            MathTex("V_{C}", color=RED_A).scale(0.7).next_to(vc_axis.c2p(0, 0.5), direction=LEFT),
            MathTex("v_{c}(t)", color=RED_B).next_to(vc_plot.get_right(), direction=UR),
            MathTex("v_{C}(t)", color=RED).scale(0.7).next_to(vC_plot.get_right())
        )

        self.play(Write(op3))
        self.wait()
        self.play(Write(op4[0]))
        self.wait()
        for i in range(1, len(op4[1:-1])):
            if i == len(op4[1:-1]) - 1:
                self.play(
                    TransformFromCopy(op4[i - 1][1], op4[i]),
                    Create(vc_axis),
                    VC_plot.animate.move_to(vc_axis.c2p(2.1 / 2, 1.0 / 2)).align_to(vc_axis.c2p(0, 0.5), direction=LEFT),
                    Write(vc[0])
                )
                self.wait()

            else:
                self.play(TransformFromCopy(op4[i - 1], op4[i]))
                self.wait()

        self.play(
            TransformFromCopy(op4[2][-1], op4[4]),
            Create(vc_plot), Write(vc[1]),
        )
        self.wait()

        vC = MathTex("v_C(t)", "=", "V_C", "+", "v_c(t)").next_to(ip, direction=DOWN, buff=0.25)

        for i, c in zip(vC[::2], [RED, RED_A, RED_B]):
            i.set_color(c)
        self.play(
            Write(vC),
            ReplacementTransform(vc_plot, vC_plot), ReplacementTransform(vc[1], vc[-1]),
            FadeOut(ic, op2[-1], op3, op4[:3]),
        )
        self.wait()
        self.play(
            op4[3:-1].animate.next_to(vC, direction=DOWN, buff=0.75)
        )
        self.wait()

        # op4[-2].next_to(op4[-3], direction=DOWN, buff=0.2).align_to(op4[-3].get_left(), direction=LEFT)

        vbe_ssaxis = Axes(
            x_range=[-0.1, 2, 0.5],
            # x_range=[0, 0.8, 0.1],
            y_range=[-0.5, .5, 0.25],
            x_length=5,
            y_length=3,
            x_axis_config={
                "include_tip": False,
            },
            y_axis_config={
                "include_tip": False
            }
        ).to_corner(UR)
        vc_ssaxis = vbe_ssaxis.copy().to_corner(DR)

        vbe_ssaxis_labels = vbe_ssaxis.get_axis_labels(x_label=MathTex("t", color=WHITE), y_label=MathTex("v_{be}", color=GREEN_B))
        vbe_ssaxis.add(vbe_ssaxis_labels)

        vc_ssaxis_labels = vc_ssaxis.get_axis_labels(x_label=MathTex("t", color=WHITE), y_label=MathTex("v_c", color=RED_B))
        vc_ssaxis.add(vc_ssaxis_labels)

        vbe_plot = vbe_ssaxis.plot(lambda vc: 0.2 * np.sin(15 * vc), color=GREEN_B, x_range=[0, x_lim])
        vc_plot = vc_ssaxis.plot(lambda vc: -0.4 * np.sin(15 * vc), color=RED_B, x_range=[0, x_lim])

        fade_grp1 = VGroup(vC[:2], vC[3:], ip[:2], ip[3:]).save_state()
        fade_grp2 = VGroup(vC[:4], ip[:4]).save_state()  # op4[-3]
        temp = VGroup(vBE_plot, vC_plot, vc[-1], vbe[-1])
        for m in temp:
            m.save_state()

        self.play(FadeOut(op4[-3:-1]))
        self.wait()
        self.play(*[
            m.animate.fade(0.8)
            for m in [fade_grp1]
        ],
            FadeOut(temp)
        )
        self.play(Wiggle(VBE_plot), Wiggle(VC_plot))
        self.wait()
        self.play(fade_grp1.animate.restore())
        self.wait()
        self.play(*[
            m.animate.fade(0.8)
            for m in [fade_grp2]
        ],
            *[
            ReplacementTransform(*m)
            for m in [[vbe_axis, vbe_ssaxis], [vc_axis, vc_ssaxis], [vBE_plot, vbe_plot], [vC_plot, vc_plot]]
        ],
            FadeOut(vbe, vc, VC_plot, VBE_plot)
        )
        self.wait()
        # self.play(op4[4].animate.shift(0.25 * DOWN))
        # op4[-1].next_to(op4[-2], direction=DOWN, buff=0.2).align_to(op4[-2].get_left(), direction=LEFT)

        # vgain = VGroup(
        #     MathTex("\\text{Votlage Gain}"),
        #     VGroup(
        #         MathTex("A_v", "=").set_color_by_tex("A_v", color=BLUE),
        #         MathTex("v_c", "\\over", " v_{be} ").set_color_by_tex("v_c", RED_B).set_color_by_tex("v_{be}", GREEN_B),
        #         MathTex("= -", " g_m ", "R_C").set_color_by_tex("g_m", YELLOW),
        #     ).arrange_submobjects(direction=RIGHT)
        # ).arrange_submobjects(direction=DOWN).next_to(op4[-1], direction=DOWN, buff=0.5)

        # self.wait()
        # self.play(Write(op4[-1]))
        # for v in vgain:
        #     self.play(Write(v))
        #     self.wait()

        # self.play(fade_grp2.animate.restore())

        self.wait()


class Conclusion(Scene):
    def construct(self):
        bjtamp = BJTAmp().label_vcc_rc().remove_bjt_labels().shift(UP)
        vs = bjtamp.elements[0]
        vs.scale(0.75, about_point=vs.get_top())
        gnd1 = bjtamp.elements[-1][1]
        gnd1.next_to(vs, direction=DOWN, buff=-0.35)
        signal = Source(ac=True).scale(0.75)
        signal.move_to(vs)

        amp = VGroup(bjtamp, signal).move_to(ORIGIN)

        vbe = VGroup(
            MathTex("V_{BE}", color=GREEN_A).scale(0.9).next_to(vs, direction=LEFT),
            MathTex("v_{be}", color=GREEN_B).scale(0.9).next_to(signal, direction=LEFT)
        )
        vs.add(gnd1)
        c_node = Dot(bjtamp.elements[2].get_bottom(), color=RED)
        vc = VGroup(
            MathTex("V_C", color=RED_A).scale(0.9).next_to(c_node),
            MathTex("+ \\, \\,v_c", color=RED_B).scale(0.9)
        )
        vc[1].next_to(vc[0])

        self.play(Create(bjtamp))
        self.play(Write(vbe[0]))  # , Write(vc[0]))  # , FadeIn(c_node))
        self.play(
            vs.animate.next_to(signal, direction=DOWN, buff=-0.35),
            vbe[0].animate.shift(DOWN),
        )

        self.play(Write(signal))
        self.play(Write(vbe[-1]))  # , Write(vc[-1]))

        self.wait()
        # self.add(amp, vbe)


class Dummy(Scene):
    def construct(self):
        # rev_sat = MathTex("I_s", " = 10^{-12} A")
        # vt = MathTex("V_t", " = 25 mV")
        # vg = VGroup(rev_sat, vt).arrange_submobjects(direction=DOWN)
        # for m in vg:
        #     self.play(Write(m[0]))
        #     self.play(Write(m[1]))
        #     self.wait()
        # mosamp = MOSAmp().label_vdd_rd()
        # mosamp.elements[1][-3:].fade(1)
        # vgs = MathTex("v_{GS}", color=GREEN).scale(0.7).next_to(mosamp.elements[1], direction=DL, buff=0).shift(UR * 0.2)
        # iD = MathTex("i_D R_D", color=BLUE).scale(0.9).next_to(mosamp.elements[2])
        # # vd = MathTex("v_D","=", "V_DD - ")
        # vds_term = Line(mosamp.drain(), mosamp.drain() + 2 * RIGHT)
        # op_node = vds_term.points[-1]
        # vds_term.add(Dot(op_node))
        # vds_gnd = Ground().next_to(vds_term.points[-1], direction=DOWN).align_to(mosamp.elements[-1], direction=UP)
        # vds_gnd.add(Dot(vds_gnd.get_top()))
        # # vds_text = MathTex("v_D", " = V_{DD} -").scale(0.75).set_color_by_tex("v_D", YELLOW)
        # vo_text = MathTex("v_D", " = V_{DD} -", "i_D R_D").scale(0.75).set_color_by_tex("v_D", YELLOW).set_color_by_tex("i_D R_D", BLUE)
        # vo_text.next_to(vds_term.get_right(), direction=DOWN, buff=1.25)
        # plus = MathTex("+").next_to(op_node, direction=DOWN)
        # minus = MathTex("-").next_to(op_node, buff=2.5, direction=DOWN)
        # self.add(mosamp, vds_term, vds_gnd, vo_text, plus, minus, vgs, iD)

        # q_pt_t = Tex("Q-point")
        # q_pt_coord = MathTex("(", "V_{BE}", ",", "V_C", ")").next_to(q_pt_t, direction=DOWN)
        # q_pt_coord[1].set_color(GREEN_A)
        # q_pt_coord[3].set_color(RED_A)
        # self.add(q_pt_coord)
        # self.play(Write(q_pt_t))
        # self.play(Write(q_pt_coord))
        # self.wait()
        # dcan = Text("AC / Small Signal Analysis")
        # self.play(Write(dcan))
        # self.wait()
        mos_eqn = VGroup(
            # MathTex("I_D", " = \\dfrac{\\mu C_{ox} W}{L}"),
            MathTex("i_D", " = k_n"),
            MathTex("(", "v_{GS}", "-V_{th})^2 \\over 2")  # s, substrings_to_isolate="V_{GS}"),
        ).arrange_submobjects(buff=0.1)
        mos_eqn.scale(0.8)
        mos_eqn[0].set_color_by_tex("i_D", RED)
        mos_eqn[1].set_color_by_tex("v_{GS}", GREEN)
        vd = MathTex("v_D", "= V_{DD} -", "i_D R_D")
        vd[0].set_color(YELLOW)
        vd[-1].set_color(BLUE)
        temp = VGroup(mos_eqn, vd).arrange_submobjects(direction=DOWN)
        self.add(temp)
# class SSModelBjt(Scene):
#     def construct(self):
