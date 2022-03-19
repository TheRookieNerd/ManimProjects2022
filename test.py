from manim import *


def wire(pts):
    return VMobject().set_points_as_corners(pts)


def get_slot():
    return VMobject().set_points_as_corners([0.15 * _ for _ in [LEFT, UL, UR, RIGHT]])


def prep_line_for_trans(l):
    l = Line().set_points_as_corners([
        np.array([x, 1, 0]) for x in np.linspace(l.get_left()[0], l.get_right()[0], 100)
    ])
    return l


class WrapLines(Scene):
    def construct(self):
        left_corner = PI
        l = Line(RIGHT).set_points_as_corners([np.array([x, 1, 0]) for x in np.linspace(-left_corner, left_corner, 100)])

        def get_slotted_line(l, s):
            #l == line mobject, s==slots
            alpha_0 = (l.get_length() / s) / l.get_length()
            alpha = alpha_0
            ln = VGroup()

            slots = VGroup()
            for _ in range(s):
                slot_pos = l.point_from_proportion(alpha)
                slot = get_slot().move_to(slot_pos).align_to(slot_pos, direction=DOWN)
                slots.add(slot)
                l.add(slot)
                alpha += alpha_0

            ln.add(
                Line(RIGHT).set_points_as_corners([
                    np.array([x, 1, 0]) for x in np.linspace(-left_corner, slots[0].points[0][0], 25)
                ])
            )
            for _ in range(len(slots) - 1):
                ln.add(
                    Line(RIGHT).set_points_as_corners([
                        np.array([x, 1, 0]) for x in np.linspace(slots[_].points[-1][0], slots[_ + 1].points[0][0], 25)
                    ])
                )
            return VGroup(ln, slots)

        l = get_slotted_line(l, 2)
        stator = VGroup(l)
        outer_rim = Line().match_width(l)
        outer_rim = prep_line_for_trans(outer_rim).next_to(l, direction=UP, buff=0.65)
        stator_conductors = VGroup(*[Circle(radius=0.025, fill_opacity=1, fill_color=YELLOW, color=YELLOW).move_to(s) for s in l[1]])

        stator.add(outer_rim, stator_conductors)

        width_of_l = np.linalg.norm(l.get_left() - l.get_right())

        # def get_high_res_square(s):
        #     hor_line = Line(RIGHT).set_points_as_corners([np.array([x, 0, 0]) for x in np.linspace(-s / 2, s / 2, 25)]).shift(UP)
        #     ver_line = Line(RIGHT).set_points_as_corners([np.array([0, y, 0]) for y in np.linspace(-s / 2, s / 2, 25)]).align_to(hor_line, direction=UL)
        #     return VGroup(
        #         hor_line,
        #         ver_line,
        #         hor_line.copy().align_to(ver_line, direction=DL),
        #         ver_line.copy().align_to(hor_line, direction=UR)
        #     )

        def get_field_line(s):
            # hor_line = Line(RIGHT).set_points_as_corners([np.array([x, 0, 0]) for x in np.linspace(-s / 2, s / 2, 25)]).shift(UP)
            # ver_line = Line(RIGHT).set_points_as_corners([np.array([0, y, 0]) for y in np.linspace(-s / 2, 0, 25)]).align_to(hor_line, direction=UL)
            # ver_line_2 = ver_line.copy().align_to(hor_line, direction=UR)
            rr = RoundedRectangle(height=1.5, width=3, corner_radius=0.75)
            arc = ArcBetweenPoints(rr.get_bottom() + LEFT * 0.5, rr.get_bottom() + RIGHT * 0.5)
            # return VGroup(hor_line, ver_line, ver_line_2, arc)
            return VGroup(rr, arc)

        # scale_list = [0.2]
        # for _ in range(4):
        #     scale_list.append(scale_list[-1] + scale_list[0])
        # for sc in stator_conductors:

        #     # field_lines = VGroup(*[RoundedRectangle(height=1.5, width=3, corner_radius=0.75).scale(_) for _ in scale_list]).move_to(sc)
        #     # field_lines = VGroup(*[get_field_line(2).scale(_) for _ in scale_list]).move_to(sc)
        #     field_lines = VGroup(*[Circle(radius=0.75).scale(_) for _ in scale_list]).move_to(sc)
        #     # field_lines = VGroup(*[get_high_res_square(_).move_to(sc) for _ in scale_list])

        #     # field_lines = VGroup(*[RoundedRectangle(height=0.5, width=0.5, color=RED).scale(_) for _ in np.linspace(1, 2, 4)]).move_to(sc)
        #     sc.add(field_lines)

        rotor = Line().match_width(l).shift(0.5 * UP)
        rotor = prep_line_for_trans(rotor).next_to(l, direction=DOWN, buff=0.25)
        stator.add(rotor)
        self.add(stator)
        # self.add(RoundedRectangle(height=1.5, width=1.5))

        def line_to_circle(pt):
            x = pt[0]
            y = pt[1]
            return np.array([
                -y * np.cos(2 * PI * x / width_of_l),
                y * np.sin(2 * PI * x / width_of_l),
                0
            ])

        stator.save_state()
        self.play(
            #     ApplyPointwiseFunction(
            #         lambda p: line_to_circle(p), field_lines
            #     ),
            ApplyPointwiseFunction(
                lambda p: line_to_circle(p), stator
            )
        )

        def get_field_line(d, s):
            # hor_line = Line(RIGHT).set_points_as_corners([np.array([x, 0, 0]) for x in np.linspace(-s / 2, s / 2, 25)]).shift(UP)
            # ver_line = Line(RIGHT).set_points_as_corners([np.array([0, y, 0]) for y in np.linspace(-s / 2, 0, 25)]).align_to(hor_line, direction=UL)
            # ver_line_2 = ver_line.copy().align_to(hor_line, direction=UR)
            # rr = RoundedRectangle(height=1.5, width=3, corner_radius=0.75)
            # arc = ArcBetweenPoints(rr.get_bottom() + LEFT * 0.5, rr.get_bottom() + RIGHT * 0.5)
            field_line = Triangle(stroke_width=1).make_smooth().scale(0.75).stretch(1.75, 0).stretch(0.9, 1).scale(s)
            if d:
                field_line.rotate(90 * DEGREES)
            else:
                field_line.rotate(-88 * DEGREES)
            # return VGroup(hor_line, ver_line, ver_line_2, arc)
            return VGroup(field_line)

        scale_list = [0.2]
        for _ in range(5):
            scale_list.append(scale_list[-1] + scale_list[0])
        for i, sc in enumerate(stator_conductors):

            # field_lines = VGroup(*[RoundedRectangle(height=1.5, width=3, corner_radius=0.75).scale(_) for _ in scale_list]).move_to(sc)
            # field_lines = VGroup(*[get_field_line(2).scale(_) for _ in scale_list]).move_to(sc)
            # field_lines = VGroup(*[Circle(radius=0.75).scale(_) for _ in scale_list]).move_to(sc)
            # field_lines = VGroup(*[get_high_res_square(_).move_to(sc) for _ in scale_list])
            if i == 0:
                d = True
            else:
                d = False
            field_lines = VGroup(*[get_field_line(d, _) for _ in scale_list]).move_to(sc)

            # field_lines = VGroup(*[RoundedRectangle(height=0.5, width=0.5, color=RED).scale(_) for _ in np.linspace(1, 2, 4)]).move_to(sc)
            sc.add(field_lines)

        # demo_dot = Dot()
        # axis = Axis()
        # stator.restore()
        # self.play(stator.animate.restore())
