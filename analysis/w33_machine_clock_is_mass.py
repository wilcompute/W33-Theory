#!/usr/bin/env python3
"""Finite Heawood control-clock calculation (legacy filename retained).

The former version of this file over-read a dimensionless graph eigenvalue as a
particle mass and an order coincidence as a traversal of a gauge group.  Pass 320
already isolated the missing scale; Pass 377 now supplies the useful computational
reading.  This revision keeps the exact finite calculation and states only what it
builds:

  (1) The 14-vertex Heawood/Fano incidence graph has a 12-dimensional middle
      spectral shell.  On that shell, J=(L_H-3I)/sqrt(2) is an involution with two
      six-dimensional +/- branches.  J is a reversible *spectral branch switch*,
      not a continuum Hamiltonian, energy, or physical frequency.
  (2) The connected graph has cycle rank 21-14+1=8.  Once a cycle basis is chosen,
      its F2 cycle space is an eight-bit switch register with 2^8 states.  The
      dimension is invariant; the particular eight coordinates are not.
  (3) The executable routing ABI is typed: binary Q3 address toggles lower to a
      BT828 header, then to a Q6 flag address and a LOAD/FLIP/LATCH schedule.  The
      separate F3 coordinates are parity lanes, not ternary Q3 toggle gates.
      Pass 379 shows the header depth step is not a Q6 geometric operation
      through the pinned BT1371 address table.  Pass 380 shows that scheduler
      flag plus phase is the minimal free-C3 lift, with fourteen header orbits
      still requiring an explicit binding table.
  (4) The identities 8 -> 48 -> 24 -> 72 -> 2160 -> 51840 are finite layout and
      counting identities.  The equality 51840=|Sp(4,3)| does not itself supply an
      action, an enumeration of group elements, a mass scale, or a device model.

The output path keeps its historical name for existing links, but its contents are
now explicitly a logic-switch certificate.
"""
from __future__ import annotations

import json
from collections import Counter

import numpy as np

Q, LAM = 3, 2  # q=3, lambda=2


def heawood_adjacency():
    # Fano plane PG(2,2): points 0..6, cyclic lines {i, i+1, i+3} mod 7.
    lines = [tuple(sorted(((i) % 7, (i + 1) % 7, (i + 3) % 7))) for i in range(7)]
    A = np.zeros((14, 14))
    for li, ln in enumerate(lines):
        lv = 7 + li
        for p in ln:
            A[p, lv] = A[lv, p] = 1
    return A, lines


def main():
    out = {
        "schema": "w33.heawood_logic_switch_clock.v2",
        "legacy_filename": "w33_machine_clock_is_mass.py",
    }
    A, lines = heawood_adjacency()
    deg = A.sum(1)
    assert np.all(deg == 3), "Heawood is 3-regular"
    L = np.diag(deg) - A
    ev = np.linalg.eigvalsh(L)
    # round to compare to {0, 3-sqrt2, 3+sqrt2, 6}
    rounded = Counter(round(float(x), 4) for x in ev)
    print(f"[1] Heawood (Fano incidence) Laplacian spectrum:")
    for val, mult in sorted(rounded.items()):
        print(f"    {val:8.4f}  x{mult}")
    s2 = np.sqrt(LAM)
    expected = Counter({0.0: 1, round(Q - s2, 4): 6, round(Q + s2, 4): 6, 6.0: 1})
    assert rounded == expected, (rounded, expected)
    out["heawood_laplacian"] = {str(v): m for v, m in sorted(rounded.items())}

    # Middle shell: a normalized involution is an exact reversible branch switch.
    middle_indices = [
        index for index, value in enumerate(ev) if abs(abs(value - Q) - s2) < 1e-6
    ]
    P = np.linalg.eigh(L)[1][:, middle_indices]
    branch_switch = (P.T @ (L - Q * np.eye(14)) @ P) / s2
    branch_eigenvalues = np.linalg.eigvalsh(branch_switch)
    branch_profile = Counter(round(float(value)) for value in branch_eigenvalues)
    print(
        f"\n[1b] spectral branch switch: {len(middle_indices)} middle-shell modes, "
        "J=(L-3I)/sqrt(2)"
    )
    print(
        f"     J^2=I: {np.allclose(branch_switch @ branch_switch, np.eye(12))}; "
        f"branch profile: {dict(sorted(branch_profile.items()))}"
    )
    assert len(middle_indices) == 12
    assert np.allclose(branch_switch @ branch_switch, np.eye(12), atol=1e-8)
    assert branch_profile == Counter({-1: 6, 1: 6})
    out["spectral_branch_switch"] = {
        "normalized_operator": "J=(L_H-3I)/sqrt(2) on the 12-dimensional middle shell",
        "involution": True,
        "branch_profile": {str(key): value for key, value in sorted(branch_profile.items())},
        "spectral_displacement": s2,
        "scope": "A finite reversible spectral selector; no physical frequency, energy, or mass is asserted.",
    }

    # The Heawood cycle space supplies an eight-bit register only after a basis choice.
    cycle_rank = 21 - 14 + 1
    print(
        f"\n[2] cycle-space switch register: beta_1 = 21-14+1 = {cycle_rank}; "
        f"2^{cycle_rank} = {2**cycle_rank} register states"
    )
    assert cycle_rank == 8
    out["cycle_register"] = {
        "field": "F2",
        "cycle_rank": cycle_rank,
        "state_count": 2**cycle_rank,
        "nonzero_cycle_states": 2**cycle_rank - 1,
        "basis_boundary": "The eight coordinate switches depend on a chosen cycle basis; beta_1=8 does not.",
    }

    # These are typed bookkeeping identities, not a group traversal.
    word, body, epi, frame = 8, 48, 24, 72
    bus, supercycle = 2160, 51840
    h_E8 = 30
    sp43 = 51840
    print(f"\n[3] typed runtime accounting 8 -> 48 -> 24 -> 72 -> 2160 -> 51840:")
    print(
        f"    8-tick word = up to 3 binary Q3 toggles + up to 5 apartment slots; "
        f"72 frame = q^2 * 8 "
        f"= {Q**2*word}"
    )
    print(f"    2160 mirror bus = h(E8) * frame = {h_E8} * {frame} = {h_E8*frame}")
    print(
        f"    51840 runtime count = 720 * 72 = 24 * 30 * 72 = {24*30*72}; "
        f"it happens to equal |Sp(4,3)| = {sp43}"
    )
    assert Q**2 * word == frame == 72
    assert h_E8 * frame == bus == 2160
    assert 720 * frame == 24 * h_E8 * frame == supercycle == sp43 == 51840
    out["typed_control_pipeline"] = {
        "source": "binary Q3 coordinate toggle bank",
        "header": "BT828 mirror/tomotope header flag",
        "address": "BT1374 Q6 edge address",
        "transition": "BT1406/BT1698 LOAD_FLAG -> FLIP_Q6_AXIS -> LATCH_VERTEX",
        "header_geometry_boundary": (
            "Pass 379: flag -> flag+64 mod 192 is not a Q6 line-graph "
            "automorphism through BT1371's pinned address table."
        ),
        "scheduler_binding_boundary": (
            "Pass 380: (tomotope_flag, phase_trit) is the minimal free-C3 "
            "scheduler lift; fourteen of sixteen header-orbit bindings remain "
            "explicit missing compiler data."
        ),
        "boundary": "No state-level toggle-to-Q6 intertwiner or hardware implementation is claimed.",
    }
    out["runtime_accounting"] = {
        "word": word,
        "frame": frame,
        "mirror_bus": bus,
        "supercycle": supercycle,
        "order_matches_Sp43": True,
        "h_E8": h_E8,
        "boundary": "Arithmetic equality to a group order is not an action or a group traversal.",
    }

    print("\nRESULT: the Heawood layer supplies a finite spectral branch switch and")
    print("  an eight-bit cycle-space register. BT828/BT1374/BT1406/BT1698 supply")
    print("  a separately typed binary-toggle -> header -> Q6 -> state-transition")
    print("  pipeline, with explicit header-geometry and scheduler-binding boundaries.")
    print("  The numbers sqrt(2) and 51840 are exact finite invariants and")
    print("  counts; this calculation derives neither a physical mass nor a calibrated")
    print("  oscillator, device, group traversal, or continuum dynamics.")

    out["summary"] = (
        "The Heawood/Fano graph supplies J=(L_H-3I)/sqrt(2), an involutive "
        "six-by-six spectral branch selector on its 12-dimensional middle shell, "
        "and an eight-bit F2 cycle-space register after a basis choice. The "
        "Holonet control ABI is a typed binary-Q3-toggle -> header -> Q6-address "
        "-> LOAD/FLIP/LATCH pipeline. Pass 379 keeps the header clock separate "
        "from Q6 geometry, and Pass 380 identifies the missing fourteen-orbit "
        "binding table. No mass, calibrated frequency, hardware, or group-action "
        "interpretation follows from these finite calculations."
    )
    out["sources"] = [
        "BT1654 Heawood graph calculation; BT1656 cycle-basis boundary; "
        "BT1299/BT1300 runtime ISA; Passes 377-380 finite control boundaries"
    ]
    with open("data/w33_machine_clock_is_mass.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_machine_clock_is_mass.json")


if __name__ == "__main__":
    main()
