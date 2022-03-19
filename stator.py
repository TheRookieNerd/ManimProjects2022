from manim import *


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
        stator = VGroup(
            Circle(radius=st_in_rad, color=WHITE),
            Circle(radius=st_rad, color=WHITE)
        )
        slot_lines = VGroup(
            *[Line((st_rad - 0.5) * RIGHT, st_rad * RIGHT).rotate(_ * mech_angle_ps, about_point=ORIGIN)
              for _ in range(nos)]
        )
        stator.add(slot_lines)

        slots = [rotate_vector(RIGHT * ((st_rad + st_in_rad) / 2), mech_angle_ps / 2)]
        for _ in range(nos - 1):
            slots.append(rotate_vector(slots[-1], mech_angle_ps))

        def cross():
            return VGroup(Line(UP, DOWN), Line(LEFT, RIGHT)).scale(0.15).rotate(45 * DEGREES)

        def get_conductor(slot, direction, color):
            # print(slot)
            circ = Circle(radius=0.15, color=color)
            if direction:
                circ.add(cross().scale(0.75).move_to(circ))
            else:
                circ.add(Dot(radius=0.05).move_to(circ))

            return circ.move_to(slots[slot])

        wdg_table = []
        # pseudo_spp = spp - 1
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

        for i, j in zip(range(len(wdg_table)), [RED, YELLOW, BLUE]):
            for _ in wdg_table[i]:
                stator.add(get_conductor(*_, j))
            # self.add(Dot(slots[int(_[0])]))

        slot_numbers = VGroup()
        for i, _ in enumerate(slots):
            slot_numbers.add(Text(str(i)).scale(0.5).next_to(_, direction=_, buff=0.2))
            # self.add(slot_numbers[-1])

        stator.add(slot_numbers)
        self.add(stator)
        # stator.rotate(mech_angle_ps)


class Test(Scene):
    def construct(self):
        sq = Square()
        sq.t = 0
        sq.p = 0.001

        def pulsate(sq, dt):

            sq.t += dt
            s = abs(np.cos(sq.t) + 0.001)
            if sq.t == 0:
                sq.scale(s)
            else:
                sq.scale(1 / sq.p * s)

            sq.p = s

        self.add(sq.copy().next_to(sq))
        sq.add_updater(pulsate)

        self.add(sq)
        self.wait(4)
