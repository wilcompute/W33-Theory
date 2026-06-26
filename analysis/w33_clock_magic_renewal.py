#!/usr/bin/env python3
"""
The clock renews the magic: the Boerdijk-Coxeter time quasicrystal -- twist
theta = arccos(-2/3), the q=3 simplex angle -- can never close into a Clifford cycle,
so the non-Clifford (cubic) gate it drives is refreshed every tick and can never be
gauged away in time. This is the temporal partner of the spatial no-ovoid result:
spatially the magic cannot be gauged away (W(3,3) has no ovoid), temporally it cannot
(the clock never recurs). Both are the same q=3.

w33_magic_economy.py showed the magic is structural; this asks what keeps it from
decaying into Clifford. The answer is the clock's aperiodicity.

THE TWIST. The Boerdijk-Coxeter helix (the runtime clock, sec:time) advances by
    theta = arccos(-2/3),  with -2/3 = -(q-1)/q,
the pairwise vertex dot of the regular q-simplex (the tetrahedron = the q=3 simplex).
By NIVEN's theorem the only angles with theta/pi rational and cos(theta) rational have
cos in {0, +-1/2, +-1}; since cos(theta) = -2/3 is none of these, theta/pi is
IRRATIONAL. Hence the stroboscopic phases {n*theta mod 2pi} never repeat and are
Weyl-equidistributed (computed below): the clock is a genuine time quasicrystal.

WHY THIS RENEWS THE MAGIC. A drive can be tracked as a Clifford (gauged into the
stabilizer frame) only if it closes into a finite cycle -- i.e. theta is a rational
multiple of 2pi -- landing repeatedly on the discrete stabilizer phases (multiples of
2pi/q). Because theta/pi is irrational, the drive phase NEVER returns to a stabilizer
value and never closes a cycle: each tick injects a fresh non-Clifford (cubic) rotation.
Equidistribution means the phase spends a definite fraction in every region and is
trapped in none, so the cubic-gate (magic) content is continuously replenished rather
than precessing into a Clifford loop. The clock is the magic-renewal engine.

THE SPACE-TIME PAIR. Spatial: W(3,3) has no ovoid, so no global noncontextual (Clifford)
value assignment -- the magic cannot be gauged away across the rays (independence number
alpha=7=Phi_6 < theta=10=Phi_4, the KS deficit q=3). Temporal: theta/pi irrational, so
no Clifford recurrence -- the magic cannot be gauged away across time. The same q=3
forbids the magic from being removed in either space or time.

Verifies theta=arccos(-2/3)= the q-simplex angle, theta/pi irrational (Niven), the
Weyl equidistribution / low discrepancy of {n*theta}, the three-gap (Steinhaus)
property, and that the phase never hits a stabilizer value exactly.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction as F


def main():
    out = {}
    q = 3
    theta = math.acos(-2 / 3)
    print(
        f"[the twist]  theta = arccos(-2/3) = {theta:.6f} rad; -2/3 = -(q-1)/q = "
        f"{-(q-1)/q} (q-simplex vertex dot)"
    )
    assert abs(math.cos(theta) + 2 / 3) < 1e-12 and -(q - 1) / q == -2 / 3

    # Niven: cos rational and theta/pi rational => cos in {0,+-1/2,+-1}; -2/3 excluded
    niven_rationals = {F(0), F(1, 2), F(-1, 2), F(1), F(-1)}
    cos_is_niven = F(-2, 3) in niven_rationals
    print(f"\n[Niven irrationality]")
    print(f"  cos(theta) = -2/3; in Niven set {{0,+-1/2,+-1}}? {cos_is_niven}")
    print(f"  -> theta/pi is IRRATIONAL (no Clifford recurrence)")
    assert not cos_is_niven
    out["twist"] = {
        "theta": round(theta, 6),
        "cos": "-2/3 = -(q-1)/q",
        "theta_over_pi_irrational": True,
        "by": "Niven",
    }

    # Weyl equidistribution: discrepancy of {n*theta mod 2pi} -> 0
    N = 200000
    frac = [((n * theta) % (2 * math.pi)) / (2 * math.pi) for n in range(1, N + 1)]
    frac.sort()
    # star discrepancy estimate D_N* = max_i |i/N - frac[i]|
    disc = max(max(abs((i + 1) / N - frac[i]), abs(i / N - frac[i])) for i in range(N))
    print(
        f"\n[Weyl equidistribution]  N={N}: star discrepancy D_N* = {disc:.5f} "
        f"(-> 0, equidistributed)"
    )
    assert disc < 0.01
    out["equidistribution"] = {
        "N": N,
        "discrepancy": round(disc, 5),
        "equidistributed": True,
    }

    # three-gap (Steinhaus): at any N the gaps take at most 3 distinct values
    Nsg = 500
    pts = sorted(((n * theta) % (2 * math.pi)) for n in range(1, Nsg + 1))
    gaps = [pts[i + 1] - pts[i] for i in range(len(pts) - 1)]
    gaps.append(2 * math.pi - pts[-1] + pts[0])
    distinct = len({round(g, 9) for g in gaps})
    print(
        f"[three-gap law]  N={Nsg}: distinct gap lengths = {distinct} (<= 3, Steinhaus)"
    )
    assert distinct <= 3
    out["three_gap"] = {"N": Nsg, "distinct_gaps": distinct, "steinhaus": distinct <= 3}

    # the phase never hits a stabilizer value (multiple of 2pi/q) exactly
    stab_angles = [2 * math.pi * k / q for k in range(q)]
    nearest = min(
        abs(((n * theta) % (2 * math.pi)) - a)
        for n in range(1, 2000)
        for a in stab_angles
    )
    print(
        f"\n[no stabilizer recurrence]  min distance of {{n*theta}} to a stabilizer "
        f"angle (2pi k/q) over n<2000: {nearest:.5f} > 0"
    )
    assert nearest > 1e-4
    out["no_stabilizer_recurrence"] = {
        "min_distance": round(nearest, 5),
        "never_exact": True,
    }

    # the space-time pair
    print(f"\n[the space-time pair]")
    print(
        f"  SPATIAL : W(3,3) has no ovoid; alpha=7=Phi_6 < theta=10=Phi_4, KS deficit q=3"
    )
    print(
        f"  TEMPORAL: theta/pi irrational; no Clifford recurrence, magic refreshed each tick"
    )
    print(f"  the same q=3 forbids gauging the magic away in space OR time")
    out["space_time"] = {
        "spatial": "no ovoid; alpha=7=Phi_6 < theta=10=Phi_4; KS deficit q=3",
        "temporal": "theta/pi irrational (Niven); no Clifford recurrence",
        "common": "q=3 forbids removing the magic in space or time",
    }

    print("\nRESULT: the clock is the magic-renewal engine. The Boerdijk-Coxeter twist")
    print("  theta = arccos(-2/3) -- the q=3 simplex angle -- has theta/pi irrational")
    print("  (Niven, since -2/3 is not in {0,+-1/2,+-1}), so the stroboscopic phases")
    print("  never repeat, are Weyl-equidistributed (discrepancy -> 0), obey the")
    print("  Steinhaus three-gap law, and never land exactly on a stabilizer angle. A")
    print("  drive can be gauged into the Clifford frame only if it closes a finite")
    print("  cycle (rational theta/2pi); the irrational q-simplex angle never closes,")
    print(
        "  so each tick injects a fresh cubic (non-Clifford) rotation and the magic is"
    )
    print(
        "  continuously replenished rather than precessing into a Clifford loop. This"
    )
    print(
        "  is the temporal partner of the spatial no-ovoid result: the same q=3 keeps"
    )
    print("  the magic from being gauged away in space (no ovoid) and in time (no")
    print("  recurrence). The time quasicrystal does not just clock the machine -- it")
    print("  fuels it.")

    out["summary"] = (
        "the Boerdijk-Coxeter time quasicrystal RENEWS the magic. Its twist theta="
        "arccos(-2/3) = the q=3 simplex vertex angle has theta/pi IRRATIONAL (Niven: "
        "-2/3 not in {0,+-1/2,+-1}), so the stroboscopic phases never repeat, are "
        "Weyl-equidistributed (star discrepancy ->0 at N=2e5), obey the Steinhaus "
        "three-gap law, and never hit a stabilizer angle 2pi k/q exactly. A drive is "
        "Clifford-trackable only if it closes a finite cycle (rational theta/2pi); the "
        "irrational q-simplex angle never closes, so each tick injects a fresh cubic "
        "(non-Clifford) rotation -- the magic is continuously replenished, never "
        "precessing into a Clifford loop. Temporal partner of the spatial no-ovoid "
        "result: the same q=3 forbids gauging the magic away in space (no ovoid, "
        "alpha=7<theta=10, deficit q=3) and in time (no recurrence). The clock fuels "
        "the machine."
    )
    out["sources"] = [
        "Boerdijk-Coxeter helix clock theta=arccos(-2/3)=-(q-1)/q simplex angle "
        "(sec:time); Niven's theorem (rational cos & rational theta/pi); Weyl "
        "equidistribution; Steinhaus three-gap; qutrit stabilizer phases 2pi k/q; "
        "matter=magic + no ovoid (w33_magic_economy.py, w33_contextuality_simulation.py); "
        "cubic gate = non-Clifford resource (Lloyd-Braunstein, degree-3 E6)."
    ]
    with open("data/w33_clock_magic_renewal.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_clock_magic_renewal.json")


if __name__ == "__main__":
    main()
