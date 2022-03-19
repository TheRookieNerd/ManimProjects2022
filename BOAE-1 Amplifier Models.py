from manim import *
from circuits import *
from math import exp, log


class Amplifier(MovingCameraScene):
    def construct(self):
        amp_box = Square(fill_color=BLUE, fill_opacity=0.8).scale(2).add(Tex("Amplifier").scale(1.75))
        terminals = VGroup(
            Line(ORIGIN, 2 * LEFT).next_to(amp_box, buff=0, direction=LEFT),
            Line(ORIGIN, 2 * RIGHT).next_to(amp_box, buff=0)
        )
        terminals.add(
            terminals[0].copy(),
            terminals[1].copy()
        )
        for term, direction in zip(terminals, [UP, UP, DOWN, DOWN]):
            term.shift(1.5 * direction)
            term.add(Dot(term.get_end()))
        amp_box.add(terminals)
        amp_box.add(
            MathTex("f(t)").next_to(amp_box, direction=LEFT, buff=0).scale(1.5),
            MathTex("A \\, f(t)").next_to(amp_box, direction=RIGHT, buff=0).scale(1.5),
        )
        # self.add(amp_box)
        ip_axis = Axes(
            x_range=[-0.1, 5, 2],
            y_range=[-2, 2, 2],
            x_length=4,
            y_length=2,
            x_axis_config={
                "include_tip": False
            },
            y_axis_config={
                "include_tip": False
            }
        ).add_coordinates()
        # self.add(ip_axis, ip_sine)

        op_axis = Axes(
            x_range=[-0.1, 5, 2],
            y_range=[-10, 10, 10],
            x_length=4,
            y_length=2,
            x_axis_config={
                "include_tip": False
            },
            y_axis_config={
                "include_tip": False
            }
        ).add_coordinates()
        # self.add(ip_axis, ip_sine, op_axis, op_sine)

        self.play(FadeIn(amp_box[:-3]))
        self.play(amp_box.animate.scale(0.75).shift(UP))

        ip_axis.to_edge(DL, buff=1)
        ip_sine = ip_axis.plot(lambda x: np.sin(5 * x), x_range=[0, 5], color=GREEN)

        op_axis.to_edge(DR, buff=1)
        op_sine = op_axis.plot(lambda x: 10 * np.sin(5 * x), x_range=[0, 5], color=RED)

        self.play(Create(ip_axis), Create(ip_sine))
        self.play(Create(op_axis))
        self.play(TransformFromCopy(ip_sine, op_sine))
        self.wait()
        self.play(FadeOut(*self.mobjects))

        vcvs = Amp().scale(0.9)
        vs = vcvs.elements[0]
        vs_label = vs.labels[0]
        vs_label.next_to(vs, direction=RIGHT)

        vcvs.to_edge(LEFT, buff=1)
        vcvs[-1].set_fill(opacity=1)
        v_amp_text = Tex("Voltage \\\\ Amplifier").scale(2).move_to(vcvs[-1])

        vo_text = MathTex("A_v\\, v_s").next_to(vcvs)
        plusmin = VGroup(MathTex("+"), MathTex("-")).arrange_submobjects(DOWN, buff=1.75).move_to(vo_text)
        vo_text.add(plusmin)

        self.add(vcvs)
        self.play(Write(v_amp_text))
        self.wait()
        self.play(vcvs[-1].animate.set_fill(opacity=0), FadeOut(v_amp_text), run_time=2)
        self.wait()
        self.play(TransformFromCopy(vs_label, vo_text))
        self.wait()
        self.play(FadeOut(vo_text))
        rs = vcvs.elements[1]

        rin = vcvs.elements[2]
        rin_label = rin.labels[0]

        ro = vcvs.elements[4]
        ro_label = ro.labels[0]

        rl = vcvs.elements[-1]
        self.play(Wiggle(rin, scale_value=1.25))
        self.play(Wiggle(ro, scale_value=1.25))
        self.play(Circumscribe(rs.copy().set_color(YELLOW), time_width=2))
        self.play(Circumscribe(rin.copy().set_color(YELLOW), time_width=2))

        self.wait()
        self.play(Circumscribe(ro.copy().set_color(YELLOW), time_width=2))
        self.play(Circumscribe(rl.copy().set_color(YELLOW), time_width=2))

        self.wait()

        rin_open = VGroup(Dot(rin.get_top()), Dot(rin.get_bottom()))
        ro_short = Line(ro.get_left(), ro.get_right())
        rin_inf = MathTex("R_{in} = \\infty ").move_to(rin_open).scale(0.7).shift(LEFT * 0.6)
        ro_0 = MathTex("R_o = 0").next_to(ro_short, direction=DOWN).scale(0.7)

        self.play(FadeOut(rin, rin_label), FadeIn(rin_open), FadeIn(rin_inf))
        self.play(FadeOut(ro, ro_label), FadeIn(ro_short), FadeIn(ro_0))
        self.wait()
        self.play(FadeIn(vo_text))
        self.wait()

        self.camera.frame.save_state()

        amp_titles = VGroup(*[
            Tex("Current Amplifier(CCCS)"),
            Tex("Transconductance Amplifier(VCCS)"),
            Tex("Transresistance Amplifier(CCVS)")
        ]).scale(1.15)
        for t in amp_titles:
            t.add(Line(LEFT * 6, RIGHT * 6).next_to(t, direction=DOWN))
        amps = VGroup(*[
            Amp(amp_type=a).add(title.to_edge(UP, buff=0))
            for a, title in zip(["CCCS", "VCCS", "CCVS"], amp_titles)
        ]).arrange_submobjects(direction=DOWN, buff=2).next_to(vcvs, direction=DOWN, buff=2)
        self.add(amps)
        cccs = amps[0]

        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.move_to(cccs))

        rin = cccs.elements[2]
        rin_label = rin.labels[0]

        ro = cccs.elements[4]
        ro_label = ro.labels[0]
        rin_short = Line(rin.get_top(), rin.get_bottom())
        ro_open = VGroup(Dot(ro.get_top()), Dot(ro.get_bottom()))
        rin_0 = MathTex("R_{in} = 0 ").next_to(rin_short, direction=LEFT, buff=0).scale(0.7)
        ro_inf = MathTex("R_o = \\infty").move_to(ro_open).scale(0.7)

        self.play(FadeOut(rin, rin_label), FadeIn(rin_short), FadeIn(rin_0))
        self.play(FadeOut(ro, ro_label), FadeIn(ro_open), FadeIn(ro_inf))
        self.wait()

        for amp in amps[1:]:
            self.play(self.camera.frame.animate.move_to(amp))
            self.wait()

        self.play(self.camera.frame.animate.restore())


class CascadedAmps(Scene):
    def construct(self):
        # def amp_box(c, t):
        #     amp_box = Square(fill_color=c, fill_opacity=0.8).scale(2).add(Tex(t).scale(1.75))
        #     terminals = VGroup(
        #         Line(ORIGIN, 2 * LEFT).next_to(amp_box, buff=0, direction=LEFT),
        #         Line(ORIGIN, 2 * RIGHT).next_to(amp_box, buff=0)
        #     )
        #     terminals.add(
        #         terminals[0].copy(),
        #         terminals[1].copy()
        #     )
        #     for term, direction in zip(terminals, [UP, UP, DOWN, DOWN]):
        #         term.shift(1.5 * direction)
        #         term.add(Dot(term.get_end()))
        #     amp_box.add(terminals)
        #     return amp_box.scale(0.6)

        # amps = VGroup(amp_box(RED, "Voltage \\\\ Amp"), amp_box(BLUE, "Voltage \\\\ Amp")).arrange_submobjects(buff=-.1)

        def get_vamp():
            vamp = Amp()
            for i in [0, 3, 5, 8]:
                if i == 8:
                    vamp[i][1:3].fade(1)
                    vamp[i][-1].fade(1)
                else:
                    vamp[i].fade(1)
            ip_term = Line(LEFT, RIGHT)
            ip_term.add(Dot(ip_term.get_left()).scale(1.5))
            vamp.add(
                ip_term.next_to(vamp[4].get_corner(UL), direction=LEFT, buff=0),
                ip_term.copy().next_to(vamp[4].get_corner(DL), direction=LEFT, buff=0)
            )
            vamp.add(VGroup(*[Dot(p).scale(1.5) for p in [vamp[2].get_corner(UR) + DOWN * 0.15, vamp[2].get_corner(DR)]]))
            return vamp

        amps = VGroup(*[get_vamp().scale(0.6) for _ in range(2)]).arrange_submobjects(buff=-2.1)
        amps[0].shift(UP * 0.02).scale(1.025)
        # amps[1].add(VGroup(*[Dot(p).scale(0.6 * 1.5) for p in [amps[1][2].get_corner(UR) + DOWN * 0.085, amps[1][2].get_corner(DR)]]))
        for a, c in zip(amps, [RED, BLUE]):
            a.elements.set_color(c)
            a[8].set_color(c)
        boxes = VGroup(*[
            amps[i][-4].copy().set_fill(color=c, opacity=1)
            for i, c in zip(range(2), [RED, BLUE])
        ])
        for b in boxes:
            b.add(Tex("Voltage \\\\ Amp").scale(1.25).move_to(b))

        temp = VGroup(amps, boxes).move_to(ORIGIN).shift(LEFT * 0.5 + UP * 0.25)
        title = Tex("Cascaded Amplifiers").to_edge(UP)
        # dots = VGroup(*[Dot(p) for p in []])
        # self.add(amps, boxes)
        self.play(Write(title))
        self.play(FadeIn(amps[0]), FadeIn(boxes[0]))
        self.wait()
        self.play(FadeIn(amps[1]), FadeIn(boxes[1]), FadeOut(amps[0][-1]))
        self.wait()
        self.play(FadeOut(boxes[0]))
        self.wait()
        self.play(Flash(amps[0].elements[4]))
        self.wait()

        self.play(FadeOut(boxes[1]))
        self.play(Flash(amps[1].elements[2]))

        self.wait()

        eqn = VGroup(
            MathTex("v_{in}", "=").set_color_by_tex("v_{in}", BLUE),
            MathTex("R_{in}", "\\over", "R_{in}", "+", "R_o").set_color_by_tex("R_{in}", BLUE).set_color_by_tex("R_o", RED),
            MathTex("A\\, v_{in}", color=RED)
        ).arrange_submobjects().next_to(amps, direction=DOWN, buff=0.6).shift(LEFT * 1.25)

        condition = MathTex("R_o", "<<<", " R_{in}").next_to(title, direction=DOWN, buff=0.25)
        condition[2].set_color(BLUE)
        condition[0].set_color(RED)
        # one = MathTex("1\\, \\, \\times").move_to(eqn[1])

        self.play(Write(eqn), run_time=1.5)
        self.wait()
        self.play(Write(condition))
        self.wait()

        for e in eqn:
            e.save_state()
        self.play(eqn[1].animate.fade(1))
        self.play(eqn[-1].animate.next_to(eqn[0]))
        self.wait()

        self.play(FadeOut(condition), eqn[1].animate.restore(), eqn[-1].animate.restore())
        self.wait(2)


class Symbols(Scene):
    def construct(self):
        sym = VGroup(
            MathTex(
                "+", "-", "=",
                "\\times 5",
                "20mV", "100 mV", "500 mV", "5mV", "10mV", "25mV",
                "\\approx"
            ),
            MathTex(
                "10\\Omega", "9 k\\Omega",
                color=RED
            ),
            MathTex(
                "100 k\\Omega", "1 k\\Omega",
                color=BLUE
            ),
            Line(LEFT, RIGHT),
        )
        for s in sym:
            s.arrange_submobjects(buff=0.4)
        sym.arrange_submobjects(direction=DOWN, buff=0.5)
        self.add(sym)

        # bjt = BJT().shift(4 * LEFT + 1.5 * DOWN).add_labels()
        # mos = MOSFET().shift(3.5 * RIGHT + 1.5 * DOWN).add_labels()
        # bjt_text = Text("BJT").next_to(bjt, direction=UP, buff=0.6).scale(0.7)
        # mos_text = Text("MOSFET").next_to(mos, direction=UP, buff=1).scale(0.7)
        # bjt.add(bjt_text)
        # mos.add(mos_text)
        # sym = VGroup(
            # VGroup(
            #     bjt, mos,
            #     Resistor(), Inductor(), Capacitor(), Ground()
            # ),
            # VGroup(
            #     Source(), Source(voi=False), Source(indep=False), Source(indep=False, voi=False),
            # ),
        #     VGroup(
        #         BJTAmp(), MOSAmp()
        #     )
        # )
        # for m in sym:
        #     m.arrange_submobjects()
        # self.add(sym.arrange_submobjects(direction=DOWN))


class Promo(Scene):
    def construct(self):
        amps = VGroup(BJTAmp().label_vcc_rc(), MOSAmp().label_vdd_rd()).arrange_submobjects(buff=1.5)
        # self.add(amps)
        self.play(Create(amps[0].elements[1]), Create(amps[1].elements[1]))
        self.wait()
        self.play(FadeIn(amps[0][9:]), FadeIn(amps[1][10:]), run_time=2)
        self.wait()
