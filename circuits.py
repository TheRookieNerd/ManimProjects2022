from manim import *


class TheveninEq(Source):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        self.ro = Impedance().next_to(self, UR, buff=0.825).shift(LEFT * 0.75)

        self.wires = VGroup(*[Wire(*pts)
                              for pts in [
            [self.get_top(), self.ro.get_left()],
            [self.ro.get_right(), self.ro.get_right() + RIGHT],
            [self.get_bottom(), np.array([(self.ro.get_right() + RIGHT)[0], self.get_bottom()[1] - 1, 0])]
        ]
        ])

        self.add(self.ro, self.wires)

        # term1 = Circle(color=WHITE, stroke_width=1).scale(0.1).next_to(self.wires[1], buff=0)
        # term2 = term1.copy().next_to(self.get_corner(DR), buff=0)
        # self.nodes = VGroup(term1, term2)
        # self.add(self.nodes)
        self.elements = VGroup(self[0], self.ro)

    def upper_node(self):
        return self.wires[1].get_right()

    def lower_node(self):
        return self.wires[-1].get_corner(DR)


class NortonEq(Source):
    def __init__(self, *args, **kwargs):
        super().__init__(voi=False, **kwargs)

        self.ro = Impedance().rotate(PI / 2).next_to(self, buff=1)
        self.wires = VGroup(*[Wire(*pts)
                              for pts in [
                             [self.get_top(), self.ro.get_top() + UP],
                             [self.ro.get_top() + UP, self.ro.get_top()],
                             [self.get_bottom(), self.ro.get_bottom() + DOWN],
                             [self.ro.get_bottom() + DOWN, self.ro.get_bottom()],
        ]
        ])
        self.wires.add(*[Wire(*pts)
                         for pts in [
                        [self.ro.get_top() + UP, self.ro.get_top() + UP + RIGHT],
                        [self.ro.get_bottom() + DOWN, self.ro.get_bottom() + DOWN + RIGHT]
        ]
        ])

        self.add(self.ro, self.wires)
        self.elements = VGroup(self[0], self.ro)

    def upper_node(self):
        return self.wires[-2].get_right()

    def lower_node(self):
        return self.wires[-1].get_corner(DR)


class Amp(VGroup):
    def __init__(self, amp_type="VCVS", *args, **kwargs):
        super().__init__(**kwargs)

        def add_label(comp, label, dir):
            comp.labels.append(label)
            label.next_to(comp, direction=dir)

        if amp_type == "VCVS" or amp_type == "CCVS":
            eq_ckt = TheveninEq(indep=False)
        else:
            eq_ckt = NortonEq(indep=False)

        rin, rl = [Impedance().rotate(PI / 2) for _ in range(2)]
        rin.next_to(eq_ckt, direction=LEFT, buff=3)
        rl.next_to(eq_ckt, direction=RIGHT, buff=0.75)
        if amp_type == "VCVS" or amp_type == "VCCS":
            vs = TheveninEq(ac=True).next_to(rin, direction=LEFT, buff=0.5)
        else:
            vs = NortonEq(ac=True).next_to(rin, direction=LEFT, buff=1)

        ip_wires = VGroup(*[
            Wire(*pts)
            for pts in [
                [rin.get_top(), vs.upper_node()],
                [rin.get_bottom(), vs.lower_node()]
            ]
        ])

        op_wires = VGroup(*[
            Wire(*pts)
            for pts in [
                [rl.get_top(), eq_ckt.upper_node()],
                [rl.get_bottom(), eq_ckt.lower_node()]
            ]
        ])

        ip_grp = VGroup(vs, rin, ip_wires)
        op_grp = VGroup(eq_ckt, rl, op_wires).align_to(ip_grp.get_bottom(), direction=DOWN)
        ip_corner = ip_wires[-1].get_corner(DR)
        op_corner = eq_ckt.wires[2].get_corner(DL)
        common_wire = Wire(ip_corner, op_corner)
        gnd = Ground().next_to(common_wire.get_center(), buff=0, direction=DOWN)

        self.elements = VGroup(*vs.elements, rin, *eq_ckt.elements, rl)

        for elem in self.elements:
            elem.labels = []

        labels = VGroup(*[MathTex(tex) for tex in ["R_{in}", "R_{L}"]])
        for comp, ip_label, direction in zip([rin, rl], labels, [LEFT, LEFT]):
            add_label(comp, ip_label, direction)

        if amp_type == "CCCS" or amp_type == "VCCS":
            add_label(eq_ckt.elements[0], MathTex("A\\, i_{in}"), LEFT)
            add_label(eq_ckt.ro, MathTex("R_{o}"), LEFT)
        else:
            add_label(eq_ckt.elements[0], MathTex("A\\, v_{in}"), LEFT)
            add_label(eq_ckt.ro, MathTex("R_{o}"), DOWN)

        if amp_type == "VCVS" or amp_type == "VCCS":
            add_label(vs.ro, MathTex("R_{s}"), DOWN)
            add_label(vs[0], MathTex("v_s"), LEFT)
            add_label(rin, MathTex("v_{in}"), RIGHT)
            plusmin = VGroup(MathTex("+"), MathTex("-")).arrange_submobjects(DOWN, buff=1.75).next_to(rin, buff=0.1)
            labels.add(plusmin)

        else:
            add_label(vs.ro, MathTex("R_{s}"), LEFT)
            add_label(vs[0], MathTex("i_s"), LEFT)
            add_label(rin, MathTex("i_{in}"), RIGHT)
            arrow = Arrow(UP, DOWN, max_tip_length_to_length_ratio=0.15).scale(0.5).next_to(rin, buff=0.1)
            labels.add(arrow)
            rin.labels[-1].next_to(arrow, direction=UR, buff=0.1)

        for elem in self.elements:
            labels.add(*elem.labels)

        box = SurroundingRectangle(
            VGroup(rin, eq_ckt, common_wire, gnd, rin.labels[0]),
            fill_color=BLACK, fill_opacity=0, buff=0.35,
            stroke_color=WHITE, stroke_width=1
        ).stretch(0.9, 0).shift(0.6 * LEFT)

        self.add(vs, rin, eq_ckt, rl, ip_wires, op_wires, common_wire, gnd, labels, box)
        self.move_to(ORIGIN)

    # def remove(self, mobj):
    #     # print("hi")
    #     self.remove(mobj)
    #     return self


class BJTAmp(BJT):
    def __init__(self, amp_type="BJT", *args, **kwargs):
        super().__init__(**kwargs)
        self.add_labels()
        # self.bjt = self
        rc = Resistor().rotate(PI / 2).next_to(self.collector(), direction=UP)
        gnds = VGroup(*[Ground() for _ in range(2)])
        gnds[0].next_to(self.emitter(), direction=DOWN, buff=1)

        vcc = Triangle(stroke_color=WHITE).scale(0.25).stretch(1.25, 0).next_to(rc, direction=UP, buff=0)
        vs = Source().next_to(self.base(), direction=LEFT, buff=1).align_to(self.base(), direction=UP)
        gnds[1].next_to(vs, direction=DOWN, buff=0)
        gnds[0].align_to(gnds[1], direction=UP)
        wires = VGroup(*[Wire(*pts)
                         for pts in [
            [self.collector(), rc.get_bottom()],
            [vs.get_top(), self.base()],
            [self.emitter(), gnds[0].get_top()]
        ]
        ])

        self.add(rc, gnds, vs, vcc, wires)
        self.elements = VGroup(vs, self[0:9], rc, vcc, gnds)
        self.move_to(ORIGIN)

    def label_vcc_rc(self):
        rc = self.elements[2]
        from manim import MathTex
        rc_text = MathTex("R_C").scale(0.75).next_to(rc, direction=LEFT)

        vcc = self.elements[-2]
        vcc_text = MathTex("V_{CC}").scale(0.75).next_to(vcc, direction=UR, buff=0)
        self.add(rc_text, vcc_text)

        return self

    def remove_bjt_labels(self):
        self.elements[1][-3:].fade(1)
        return self


class MOSAmp(MOSFET):
    def __init__(self, amp_type="BJT", *args, **kwargs):
        super().__init__(**kwargs)
        self.add_labels()
        # self.bjt = self
        rd = Resistor().rotate(PI / 2).next_to(self.drain(), direction=UP)
        gnds = VGroup(*[Ground() for _ in range(2)])
        gnds[0].next_to(self.source(), direction=DOWN, buff=1)

        vcc = Triangle(stroke_color=WHITE).scale(0.25).stretch(1.25, 0).next_to(rd, direction=UP, buff=0)
        vs = Source().next_to(self.gate(), direction=LEFT, buff=1).align_to(self.gate(), direction=UP)
        gnds[1].next_to(vs, direction=DOWN, buff=0)
        gnds[0].align_to(gnds[1], direction=UP)
        wires = VGroup(*[Wire(*pts)
                         for pts in [
            [self.drain(), rd.get_bottom()],
            [vs.get_top(), self.gate()],
            [self.source(), gnds[0].get_top()]
        ]
        ])

        self.add(rd, gnds, vs, vcc, wires)
        self.elements = VGroup(vs, self[0:10], rd, vcc, gnds)
        self.move_to(ORIGIN)

    def label_vdd_rd(self):
        rf = self.elements[2]
        from manim import MathTex
        rc_text = MathTex("R_D").scale(0.75).next_to(rf, direction=LEFT)

        vdd = self.elements[-2]
        vcc_text = MathTex("V_{DD}").scale(0.75).next_to(vdd, direction=UR, buff=0)
        self.add(rc_text, vcc_text)

        return self

    def remove_mos_labels(self):
        self.elements[1][-3:].fade(1)
        return self
