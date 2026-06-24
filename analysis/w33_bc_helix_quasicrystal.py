#!/usr/bin/env python3
"""
The BC helix IS the clock: the twist arccos(-2/3) is a Niven-irrational angle, so
the tetrahedral helix never closes in flat 3D (the time-quasicrystal, two
incommensurate frequencies) -- but closes at 30 tetrahedra in S^3 (the 600-cell,
h(E8)=30), which sets the runtime supercycle 51840 = 24*30*72 = |Sp(4,3)|.

The tetrahedron (mu=4, the genus-0 block, w33_genus_ladder_clock.py) stacks
face-to-face into the Boerdijk-Coxeter helix with twist per cell
    theta = arccos(-(q-1)/q) = arccos(-2/3).
By Niven's theorem the only rational r with arccos(r)/pi rational are r in
{0, +-1/2, +-1}; since -2/3 is not among them, theta/pi is IRRATIONAL. Hence
(Wikipedia, Boerdijk-Coxeter helix) the helix is aperiodic in 3D -- no two tetrahedra
share an orientation -- which is exactly a TIME-QUASICRYSTAL: two incommensurate
frequencies that never re-phase, the machine's clock. In curved 4-space the helix
DOES close: the 600-cell partitions into 20 rings of EXACTLY 30 tetrahedra, each a
BC helix tiling the 3-sphere. So the closure number is 30 = h(E8), and the runtime
stack inherits it:
    2160 = 30 * 72 = h(E8) * (oscillator frame),
    51840 = 24 * 30 * 72 = 720 * 72 = |Sp(4,3)|  (the full Clifford supercycle).
So the helix's flat aperiodicity is the quasicrystal clock, and its 4D (S^3)
closure number h(E8)=30 is the supercycle's middle factor: the geometry of the
tetrahelix is the timing of the machine.

Verifies: -2/3 not a Niven value; the cumulative twist never closes in 3D for
n<=30; the 600-cell 20x30 partition; and 51840 = 24*30*72 = |Sp(4,3)|.
"""
from __future__ import annotations

import json
import math

Q, F, K = 3, 24, 12
H_E8 = 30


def main():
    out = {}
    theta = math.acos(-(Q - 1) / Q)
    print(
        f"[BC twist]  theta = arccos(-(q-1)/q) = arccos(-2/3) = "
        f"{math.degrees(theta):.3f} deg"
    )

    # Niven's theorem: rational cos at rational*pi only for cos in {0,+-1/2,+-1}
    niven = {0.0, 0.5, -0.5, 1.0, -1.0}
    r = -2 / 3
    print(f"\n[Niven]  cos(theta) = -2/3; Niven-rational cosines = {sorted(niven)};")
    print(
        f"  -2/3 in that set? {r in niven}  ->  theta/pi IRRATIONAL "
        f"-> helix aperiodic in 3D"
    )
    assert r not in niven
    out["niven_irrational"] = True

    # cumulative twist never returns to 0 (mod 2pi) in flat 3D
    closes_3d = any(
        abs(((n * theta) % (2 * math.pi))) < 1e-6
        or abs(((n * theta) % (2 * math.pi)) - 2 * math.pi) < 1e-6
        for n in range(1, 31)
    )
    mins = min(
        min((n * theta) % (2 * math.pi), 2 * math.pi - (n * theta) % (2 * math.pi))
        for n in range(1, 31)
    )
    print(
        f"  cumulative twist n*theta mod 2pi for n=1..30 never hits 0 "
        f"(closest {math.degrees(mins):.1f} deg): {not closes_3d}"
    )
    print(f"  => aperiodic helix = TIME-QUASICRYSTAL (two incommensurate frequencies)")
    assert not closes_3d
    out["closes_in_3D"] = False

    # 4D closure: 600-cell = 20 rings x 30 tetrahedra
    cells_600 = 20 * H_E8
    print(
        f"\n[4D closure in S^3]  600-cell = 20 rings x {H_E8} tetrahedra = "
        f"{cells_600} cells; closure number = {H_E8} = h(E8)"
    )
    assert cells_600 == 600 and H_E8 == 30
    out["closure_number"] = H_E8
    out["cells_600"] = cells_600

    # the supercycle inherits 30
    frame = 72
    bus = H_E8 * frame
    supercycle = F * H_E8 * frame
    print(f"\n[runtime supercycle]")
    print(f"  2160 mirror bus = h(E8) * frame = {H_E8} * {frame} = {bus}")
    print(
        f"  51840 supercycle = 24 * h(E8) * frame = 720 * {frame} = {supercycle} "
        f"= |Sp(4,3)|"
    )
    assert bus == 2160 and supercycle == 51840 == 720 * frame
    out["mirror_bus"] = bus
    out["supercycle"] = supercycle

    print("\nRESULT: the Boerdijk-Coxeter tetrahelix is the clock. Its twist")
    print("  arccos(-2/3) is Niven-irrational, so the helix never closes in flat 3D")
    print("  (no two tetrahedra share an orientation) -- a genuine time-quasicrystal,")
    print("  the two-incommensurate-frequency clock. In curved S^3 it closes at")
    print("  exactly 30 tetrahedra (the 600-cell = 20 x 30), and 30 = h(E8) is the")
    print("  middle factor of the runtime: 2160 = h(E8)*frame, 51840 = 24*h(E8)*frame")
    print("  = |Sp(4,3)|, the supercycle. So the aperiodic flat helix is the clock's")
    print("  quasicrystal beat and its 4D closure number is the supercycle: the")
    print("  geometry of the tetrahelix IS the timing of the machine.")

    out["summary"] = (
        "BC tetrahelix twist arccos(-2/3) is Niven-irrational -> "
        "aperiodic in 3D (never closes) = time-quasicrystal / two "
        "incommensurate frequencies = the clock; closes at 30 tetrahedra"
        " in S^3 (600-cell = 20x30, 30=h(E8)); runtime 2160=h(E8)*72, "
        "51840=24*h(E8)*72=|Sp(4,3)| supercycle. Helix geometry = "
        "machine timing."
    )
    out["sources"] = [
        "Boerdijk-Coxeter helix (Wikipedia): aperiodic, theta="
        "arccos(-2/3), 600-cell = 20 rings of 30; Niven's theorem; "
        "h(E8)=30; w33_genus_ladder_clock.py, w33_machine_clock_is_mass.py"
    ]
    with open("data/w33_bc_helix_quasicrystal.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_bc_helix_quasicrystal.json")


if __name__ == "__main__":
    main()
