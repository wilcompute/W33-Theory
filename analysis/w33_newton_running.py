#!/usr/bin/env python3
"""
Newton's constant runs over the exceptional tower: G is not one number but a curve
G_s = q/(h_s * rank_s) = k/(4 * kissing_s) along the GKP shell ladder A2 < D4 < E8,
weakening as the code climbs shells -- 1/2 -> 1/8 -> 1/80 -- with the matter shell D4
sitting at the physical value G = 1/8 = 1/2^q. The factors between rungs are the
substrate constants mu = 4 and Phi_4 = 10.

w33_gravity_dictionary.py fixed G = k/(4f) = 1/8 = 1/2^q at the D4 matter shell, with
de Sitter entropy = the boundary microstate count = the kissing number f = 24. The
holonet's fault-tolerant layer is the lattice tower A2 < D4 < E8 (Face 5). Putting the
two together: each shell is a horizon with its OWN microstate count (its kissing
number), so Bekenstein-Hawking gives a Newton constant PER SHELL -- a discrete running.

THE RUNNING. Keep the holographic area A = k = 12 fixed (the W(3,3) gauge causal screen
is the same self-similar object at every scale, the "fractal of nested shells"), and let
the de Sitter entropy be the shell's horizon microstate count S_s = kissing(shell). The
exceptional tower has, exactly,
    shell:   rank   Coxeter h   kissing = #roots = h*rank
    A2        2        3            6
    D4        4        6           24
    E8        8       30          240
so Bekenstein-Hawking G_s = A/(4 S_s) = k/(4 * kissing_s) = q/(h_s * rank_s) gives
    G(A2) = 12/24  = 1/2,
    G(D4) = 12/96  = 1/8   = 1/2^q   (the matter shell -- the physical Newton constant),
    G(E8) = 12/960 = 1/80.
Gravity WEAKENS monotonically up the tower, by the substrate factors
    G(A2)/G(D4) = 4 = mu,        G(D4)/G(E8) = 10 = Phi_4.
The closed form G_s = q/(h_s rank_s) is exact on all three rungs.

THE SCALE. The Coxeter number h is the supercycle length = the gauge group's natural
scale (Face: "the supercycle is the gauge group"). Identifying h with an RG scale, the
seed shell A2 (h = 3) is the UV (strong gravity, G = 1/2 -> Planckian) and the full
gauge shell E8 (h = 30) is the IR (weak gravity, G = 1/80); the matter shell D4 (h = 6,
G = 1/8) is where we live. So gravity is strongest in the UV and weakest in the IR --
the opposite ordering to a gauge coupling, as gravity should be (it is irrelevant in the
IR). The discrete beta-trend is G_s ~ 1/(h_s rank_s): both the rank (field count) and
the Coxeter number (scale) grow up the tower, suppressing G.

Honest scope: a discrete 3-point running on the established tower, with the assignments
"area = k (self-similar screen)" and "entropy = kissing number (horizon microstates)"
the substrate's holographic dictionary (the same one that gives G=1/8 at D4); GIVEN it,
G_s = q/(h_s rank_s) is forced arithmetic on all three rungs. It is a model of how G
scales over the shell ladder (the UV/IR identification via h is interpretive), not a
continuum renormalization-group derivation; the absolute Planck scale stays a dynamical
input. What is new: G is a CURVE over the tower, exact closed form, hitting 1/2^q at the
matter shell, weakening by mu then Phi_4.

Verifies the tower data (rank, Coxeter, kissing), the closed form G_s=q/(h rank)=
k/(4 kissing) on every rung, the value 1/8=1/2^q at D4, and the mu, Phi_4 step factors.
"""
from __future__ import annotations

import json
from fractions import Fraction


def main():
    out = {}
    q = 3
    k = q * (q + 1)  # 12 area (gauge causal screen, self-similar)
    mu = 4
    Phi4 = q * q + 1  # 10

    # the exceptional GKP shell tower A2 < D4 < E8
    tower = {
        "A2": {"rank": 2, "coxeter": 3, "kissing": 6},
        "D4": {"rank": 4, "coxeter": 6, "kissing": 24},
        "E8": {"rank": 8, "coxeter": 30, "kissing": 240},
    }
    print("== Newton's constant runs over the tower A2 < D4 < E8 ==")
    print(f"  area A = k = {k} (fixed, self-similar gauge screen); entropy S = kissing")
    print(
        f"  {'shell':5s} {'rank':>4s} {'h':>4s} {'kissing':>8s} {'G=k/4kiss':>12s} "
        f"{'= q/(h*rank)':>14s}"
    )
    rows = {}
    for name, d in tower.items():
        rank, h, kiss = d["rank"], d["coxeter"], d["kissing"]
        # kissing = #roots = h * rank (exact for these)
        assert kiss == h * rank
        G = Fraction(k, 4 * kiss)
        G2 = Fraction(q, h * rank)
        assert G == G2  # closed form G_s = q/(h*rank) = k/(4*kissing)
        rows[name] = G
        print(f"  {name:5s} {rank:4d} {h:4d} {kiss:8d} {str(G):>12s} {str(G2):>14s}")
        out.setdefault("tower", {})[name] = {
            "rank": rank,
            "coxeter": h,
            "kissing": kiss,
            "G": str(G),
            "G_float": round(float(G), 5),
            "closed_form": "q/(h*rank) = k/(4*kissing)",
        }

    # the physical matter shell value
    assert rows["D4"] == Fraction(1, 8) == Fraction(1, 2**q)
    print(
        f"\n[matter shell]  G(D4) = {rows['D4']} = 1/2^q  (the physical Newton constant)"
    )
    out["matter_shell"] = {"shell": "D4", "G": "1/8 = 1/2^q"}

    # the step factors = substrate constants
    step1 = rows["A2"] / rows["D4"]
    step2 = rows["D4"] / rows["E8"]
    print(
        f"\n[step factors]  G(A2)/G(D4) = {step1} = mu = {mu};  "
        f"G(D4)/G(E8) = {step2} = Phi_4 = {Phi4}"
    )
    assert step1 == mu and step2 == Phi4
    out["steps"] = {
        "A2_to_D4": {"factor": int(step1), "is": "mu = 4"},
        "D4_to_E8": {"factor": int(step2), "is": "Phi_4 = 10"},
        "trend": "G weakens monotonically up the tower (UV->IR)",
    }

    # the scale interpretation
    print(
        f"\n[scale]  Coxeter h = supercycle = scale: A2(h=3)=UV strong gravity (G=1/2),"
    )
    print(f"  E8(h=30)=IR weak gravity (G=1/80); D4(h=6, G=1/8) = our matter shell.")
    print(f"  Gravity strongest in UV, weakest in IR -- G_s ~ 1/(h_s * rank_s).")
    out["scale"] = {
        "UV": "A2 (h=3), G=1/2 -> Planckian",
        "matter": "D4 (h=6), G=1/8=1/2^q",
        "IR": "E8 (h=30), G=1/80",
        "trend": "G_s ~ 1/(h_s*rank_s): gravity strong UV, weak IR (irrelevant, as it should be)",
    }

    print(
        "\nRESULT: Newton's constant is a curve, not a constant. Identifying each GKP"
    )
    print(
        "  shell of the tower A2 < D4 < E8 as a horizon with its own microstate count"
    )
    print("  (its kissing number = #roots = h*rank) and keeping the self-similar gauge")
    print(
        "  screen area A = k = 12, Bekenstein-Hawking gives a Newton constant per shell,"
    )
    print(
        "  G_s = k/(4*kissing_s) = q/(h_s*rank_s), exact on all three rungs: 1/2, 1/8,"
    )
    print("  1/80. The matter shell D4 sits at the physical G = 1/8 = 1/2^q; gravity")
    print(
        "  weakens up the tower by mu = 4 then Phi_4 = 10. With the Coxeter number as"
    )
    print(
        "  the scale, the seed A2 is the UV (strong gravity, Planckian) and the full E8"
    )
    print(
        "  gauge shell is the IR (weak gravity) -- gravity is strongest in the UV and"
    )
    print(
        "  irrelevant in the IR, exactly as a gravitational coupling should run. So the"
    )
    print("  substrate predicts not just the value of G but its SCALE DEPENDENCE, a")
    print(
        "  discrete beta-trend G_s ~ 1/(h_s*rank_s) over the exceptional shell ladder."
    )

    out["summary"] = (
        "Newton's constant RUNS over the exceptional tower A2 < D4 < E8: G_s = "
        "k/(4*kissing_s) = q/(h_s*rank_s), a curve not a constant. Treating each GKP "
        "shell as a horizon with its own microstate count (kissing = #roots = h*rank: "
        "6, 24, 240) and keeping the self-similar gauge-screen area A=k=12, "
        "Bekenstein-Hawking gives G(A2)=1/2, G(D4)=1/8=1/2^q (the physical matter-shell "
        "value), G(E8)=1/80 -- exact closed form on all three rungs. Gravity weakens "
        "monotonically up the tower by the substrate factors mu=4 then Phi_4=10. With the "
        "Coxeter number h as scale, A2(h=3)=UV (strong gravity, Planckian), E8(h=30)=IR "
        "(weak gravity), D4(h=6, G=1/8)=our matter shell: gravity strongest in UV, "
        "irrelevant in IR, as it should be (G_s ~ 1/(h_s*rank_s)). Honest: a discrete "
        "3-point running; area=k and entropy=kissing are the holographic dictionary (the "
        "same that gives G=1/8 at D4), the UV/IR-via-h identification is interpretive, "
        "and the absolute Planck scale stays dynamical -- but GIVEN the dictionary, "
        "G_s=q/(h*rank) is forced arithmetic. New: G is a curve, hitting 1/2^q at matter, "
        "weakening by mu then Phi_4."
    )
    out["sources"] = [
        "G=k/(4f)=1/8=1/2^q at D4 (w33_gravity_dictionary.py); GKP shell tower A2<D4<E8 "
        "(Face 5, w33 moonshine ladder); exceptional root/Coxeter data (kissing=#roots="
        "h*rank: A2 6, D4 24, E8 240); Bekenstein-Hawking S=A/4G; de Sitter entropy = "
        "horizon microstate count; 'supercycle is the gauge group' (Coxeter=scale)."
    ]
    with open("data/w33_newton_running.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_newton_running.json")


if __name__ == "__main__":
    main()
