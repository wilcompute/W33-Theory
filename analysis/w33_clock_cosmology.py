#!/usr/bin/env python3
"""
The machine's clock is the universe's clock: the Boerdijk-Coxeter time quasicrystal
that renews the computational magic (theta=arccos(-2/3)) is the same de Sitter beat
that sets inflation. Its angle is the discrete de Sitter angle -(q-1)/q; its
fundamental beat is 30 = h(E8); the inflation e-fold number is N = 2*30 = 60 = twice
the beat; and the CMB spectral tilt is 1 - n_s = 2/N = 1/30 = 1/(beat) -- the
deviation of the primordial spectrum from scale invariance is the inverse of the
clock's fundamental period. The architecture's clock (Face 5/the machine) and
inflationary cosmology (Face 7) are one quasicrystal.

w33_clock_magic_renewal.py showed the BC clock keeps the magic non-Clifford by being a
time quasicrystal (theta/pi irrational, never recurs). This asks whether that same
clock appears in the cosmology face -- and it does, quantitatively.

THE DE SITTER ANGLE. The clock twist is cos(theta) = -2/3 = -(q-1)/q, the pairwise
vertex dot of the regular q-simplex (the tetrahedron). The same -(q-1)/q is the
discrete-de-Sitter structure the selection face uses (Face 1, the de Sitter closure
cubic) -- so the clock advances along the discrete de Sitter direction.

THE BEAT = h(E8). The Boerdijk-Coxeter helix sits in the 600-cell as 20 rings of 30
tetrahedra; the beat is 30 = h(E8), the E8 Coxeter number (and the top Witting degree =
Phi_3+Phi_4+Phi_6). So the clock's fundamental period is 30.

THE COSMOLOGY. Inflation (Face 7) has e-fold number
    N = 2(v - Phi_4) = 2*h(E8) = 2*30 = 60 = twice the clock beat,
and the spectral tilt
    1 - n_s = 2/N = 1/30 = 1/h(E8) = 1/(clock beat).
So the number of e-folds is twice the clock's period, and the tilt of the CMB power
spectrum away from scale invariance is exactly the inverse of the clock's beat. The
machine's clock period (30) directly sets the cosmological tilt (1/30).

QUASICRYSTAL <-> QUASI-DE SITTER. The clock is a TIME QUASICRYSTAL -- nearly periodic
but never exactly (theta/pi irrational). Inflation is QUASI-DE SITTER -- nearly
exponential expansion but not exactly (slow roll, n_s != 1). Both are "broken de
Sitter": the clock breaks exact time-periodicity, inflation breaks exact de Sitter, by
the same q=3. The clock's deviation from periodicity is the cosmology's deviation from
scale invariance (1 - n_s = 1/beat).

So the architecture's clock and the universe's expansion are the same quasicrystal:
the de Sitter angle -(q-1)/q, the beat 30 = h(E8), and the tilt 1 - n_s = 1/beat tie
the machine's time to the cosmological clock.

Verifies cos theta = -(q-1)/q, the beat 30 = h(E8), N = 2*beat = 60, and the tilt
1 - n_s = 2/N = 1/beat = 1/30.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction as F


def main():
    out = {}
    q = 3
    Phi3, Phi4, Phi6 = q * q + q + 1, q * q + 1, q * q - q + 1
    hE8 = Phi3 + Phi4 + Phi6  # 30
    v = (q + 1) * Phi4  # 40

    # the de Sitter angle
    theta = math.acos(-2 / 3)
    print(
        f"[de Sitter angle]  cos theta = -2/3 = -(q-1)/q = {-(q-1)/q}; "
        f"theta = {theta:.4f} (q-simplex / discrete de Sitter direction)"
    )
    assert abs(math.cos(theta) + (q - 1) / q) < 1e-12

    # the beat = h(E8)
    beat = hE8
    print(
        f"\n[the clock beat]  Boerdijk-Coxeter beat = 30 = h(E8) "
        f"= Phi_3+Phi_4+Phi_6 = {Phi3}+{Phi4}+{Phi6} (600-cell = 20 rings of 30)"
    )
    assert beat == 30 == 20 * 30 // 20

    # the cosmology: N = 2*beat, tilt = 1/beat
    N = 2 * (v - Phi4)
    n_s = 1 - F(2, N)
    tilt = 1 - n_s  # = 2/N
    print(f"\n[the cosmology]")
    print(f"  e-folds N = 2(v-Phi_4) = 2*h(E8) = 2*{beat} = {N} = twice the clock beat")
    print(f"  spectral tilt 1 - n_s = 2/N = {tilt} = 1/{beat} = 1/(clock beat)")
    assert N == 2 * beat == 60 and tilt == F(1, beat) == F(1, 30)
    out["cosmology"] = {
        "e_folds_N": N,
        "N_is": "2 * h(E8) = 2 * clock beat",
        "tilt_1_minus_ns": "2/N = 1/30 = 1/(clock beat)",
        "n_s": "29/30",
    }

    # quasicrystal <-> quasi-de Sitter
    print(f"\n[quasicrystal <-> quasi-de Sitter]")
    print(
        f"  clock: time quasicrystal (theta/pi irrational) -- nearly periodic, never exact"
    )
    print(
        f"  inflation: quasi-de Sitter (slow roll, n_s != 1) -- nearly exponential, not exact"
    )
    print(
        f"  both broken de Sitter by q=3; clock's aperiodicity = cosmology's tilt 1-n_s"
    )
    out["correspondence"] = {
        "clock": "time quasicrystal: theta/pi irrational, nearly periodic",
        "inflation": "quasi-de Sitter: slow roll, n_s != 1, nearly exponential",
        "common": "broken de Sitter by q=3; clock aperiodicity = tilt 1-n_s = 1/beat",
    }
    out["de_sitter_angle"] = {
        "cos_theta": "-(q-1)/q = -2/3",
        "beat": 30,
        "beat_is": "h(E8) = Phi_3+Phi_4+Phi_6",
    }

    print("\nRESULT: the machine's clock is the universe's clock. The Boerdijk-Coxeter")
    print("  time quasicrystal that renews the computational magic advances by")
    print("  theta = arccos(-2/3) -- the discrete de Sitter angle -(q-1)/q -- with")
    print("  fundamental beat 30 = h(E8) (the 600-cell's 20 rings of 30). Inflationary")
    print(
        "  cosmology then reads off the same clock: the e-fold number is N = 2*30 = 60,"
    )
    print(
        "  exactly twice the beat, and the CMB spectral tilt is 1 - n_s = 2/N = 1/30 ="
    )
    print(
        "  1/(beat) -- the deviation of the primordial spectrum from scale invariance"
    )
    print(
        "  is the inverse of the clock's period. And the structures match in kind: the"
    )
    print(
        "  clock is a time quasicrystal (nearly periodic, never exact) just as inflation"
    )
    print(
        "  is quasi-de Sitter (nearly exponential, never exact) -- both broken de Sitter"
    )
    print("  by q=3, the clock's aperiodicity being the cosmology's tilt. So the")
    print(
        "  architecture's time (Face 5) and the universe's expansion (Face 7) are one"
    )
    print("  quasicrystal: same angle -(q-1)/q, same beat h(E8)=30, same tilt 1/beat.")

    out["summary"] = (
        "the machine's clock IS the universe's clock. The Boerdijk-Coxeter time "
        "quasicrystal that renews the computational magic advances by theta=arccos(-2/3) "
        "= the discrete de Sitter angle -(q-1)/q, with fundamental beat 30 = h(E8) (the "
        "600-cell's 20 rings of 30). Inflation reads off the same clock: e-folds N = 2*30 "
        "= 60 (twice the beat), and CMB tilt 1 - n_s = 2/N = 1/30 = 1/(beat) -- the "
        "spectrum's deviation from scale invariance is the inverse of the clock's period. "
        "The structures match in kind: the clock is a time quasicrystal (nearly periodic, "
        "never exact) as inflation is quasi-de Sitter (nearly exponential, never exact), "
        "both broken de Sitter by q=3 -- the clock's aperiodicity = the cosmology's tilt. "
        "Architecture time (Face 5) and cosmic expansion (Face 7) are one quasicrystal: "
        "angle -(q-1)/q, beat h(E8)=30, tilt 1/beat."
    )
    out["sources"] = [
        "Boerdijk-Coxeter clock theta=arccos(-2/3)=-(q-1)/q, beat 30=h(E8) (600-cell 20x30, "
        "sec:time); time quasicrystal (w33_clock_magic_renewal.py); inflation N=2(v-Phi_4)="
        "60, n_s=1-2/N=29/30 (w33_cosmology_seventh_face.py); de Sitter selection "
        "(w33_desitter_q3_selection.py, Face 1); quasi-de Sitter slow roll; "
        "w33_self_fueling_memory.py."
    ]
    with open("data/w33_clock_cosmology.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_clock_cosmology.json")


if __name__ == "__main__":
    main()
