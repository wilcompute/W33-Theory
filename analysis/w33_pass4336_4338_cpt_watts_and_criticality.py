#!/usr/bin/env python3
"""Passes 4336-4338 -- the machine as physics: a CPT test, a wattage, a critical point.

Three questions that are physics rather than engineering, each computable from what the
arc already established.

  4336  DOES THE MACHINE OBEY A CPT-LIKE THEOREM?  It has two independent asymmetries
        (Pass 4314): a spatial one, the p/f bias, and a temporal one, irreversibility.
        The geometry supplies a third involution, the point-line duality of Pass 4296.
        Name them P, T and C.  Each is separately violated.  In field theory the product
        PCT is conserved even where each factor is not, and that is a theorem rather than
        an accident.  Is the analogous statement true here?  The honest answer requires
        defining each operation as a concrete map and checking, not by analogy.
  4337  WHAT DOES THE MACHINE DISSIPATE, IN WATTS?  Pass 4252 gives entropy production per
        instruction; Pass 2833 measured 208.86 MHz; Landauer gives kT ln 2 per bit.  Those
        three multiply to a power, and a power is a number an engineer can act on.
  4338  THE ZETA AS A PARTITION FUNCTION.  A zeta function with a pole is a partition
        function with a singularity, and a singularity is a phase transition.  The Ihara
        zeta's radius of convergence sets a critical point; the graph RH is the statement
        that all other singularities sit on one circle.  So the instruction layer's RH
        failure is a statement about its phase structure, and it can be located.

    py -3 analysis/w33_pass4336_4338_cpt_watts_and_criticality.py
"""

from __future__ import annotations

import json
from math import log, log2, sqrt
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ID4 = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))
TV = [(a, b, c, d) for a in range(3) for b in range(3)
      for c in range(3) for d in range(3)]
TI = {t: i for i, t in enumerate(TV)}

LIN = {"F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "F_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
       "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
       "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}
ISA = [(LIN["F_p"], (0, 0, 0, 0)), (LIN["CX_pf"], (0, 0, 0, 0)),
       (LIN["CX_fp"], (0, 0, 0, 0)), (ID4, (1, 0, 0, 0))]

# The p/f exchange: swap the two hyperbolic pairs (x0,x1) <-> (x2,x3).
SWAP = ((0, 0, 1, 0), (0, 0, 0, 1), (1, 0, 0, 0), (0, 1, 0, 0))

K_B = 1.380649e-23        # J/K, exact by SI definition
CLOCK_HZ = 208.86e6       # Pass 2833, measured on the minimal engine
T_ROOM = 300.0            # K


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % 3 for j in range(4))
                 for i in range(4))


def minv(M):
    a = [list(M[i]) + [1 if j == i else 0 for j in range(4)] for i in range(4)]
    r = 0
    for c in range(4):
        p = next(i for i in range(r, 4) if a[i][c] % 3)
        a[r], a[p] = a[p], a[r]
        iv = 1 if a[r][c] % 3 == 1 else 2
        a[r] = [(x * iv) % 3 for x in a[r]]
        for i in range(4):
            if i != r and a[i][c] % 3:
                f = a[i][c] % 3
                a[i] = [(a[i][k] - f * a[r][k]) % 3 for k in range(8)]
        r += 1
    return tuple(tuple(a[i][4:]) for i in range(4))


def conj(M, g):
    """P-conjugate an affine opcode by the linear map M."""
    A, t = g
    Mi = minv(M)
    return (mm(mm(M, A), Mi), mv(M, t))


def inv_op(g):
    A, t = g
    Ai = minv(A)
    return (Ai, tuple((-mv(Ai, t)[i]) % 3 for i in range(4)))


def act(g, x):
    A, t = g
    return tuple((mv(A, x)[k] + t[k]) % 3 for k in range(4))


def simple(gens):
    A = np.zeros((81, 81))
    for g in gens:
        for i, x in enumerate(TV):
            j = TI[act(g, x)]
            A[i, j] = 1
            A[j, i] = 1
    np.fill_diagonal(A, 0)
    return A


def pencil(A):
    V = A.shape[0]
    Q = np.diag(A.sum(axis=1)) - np.eye(V)
    C = np.zeros((2 * V, 2 * V))
    C[:V, :V] = A
    C[:V, V:] = -Q
    C[V:, :V] = np.eye(V)
    return np.linalg.eigvals(C)


# ------------------------------------------------------------------ 4336
def pass_4336() -> dict:
    print("=" * 78)
    print("Pass 4336 -- P, T, C: each violated.  Is the product a symmetry?")
    print("=" * 78)
    S = set(ISA)
    print("  The three involutions, defined as maps on the OPCODE SET:")
    print("    P  conjugate by the p/f exchange (swap the two hyperbolic pairs)")
    print("    T  replace every opcode by its inverse (reverse the instruction stream)")
    print("    C  the point-line duality of the quadrangle\n")

    P_img = {conj(SWAP, g) for g in ISA}
    T_img = {inv_op(g) for g in ISA}
    PT_img = {inv_op(conj(SWAP, g)) for g in ISA}
    p_ok, t_ok, pt_ok = P_img == S, T_img == S, PT_img == S
    print(f"  P  maps the ISA to itself : {p_ok}")
    print(f"  T  maps the ISA to itself : {t_ok}")
    print(f"  PT maps the ISA to itself : {pt_ok}")

    # What P actually does to each opcode, named.
    print("\n  what P sends each opcode to:")
    names = {LIN["F_p"]: "F_p", LIN["F_f"]: "F_f", LIN["CX_pf"]: "CX_pf",
             LIN["CX_fp"]: "CX_fp", ID4: "I"}
    for g, nm in zip(ISA, ("F_p", "CX_pf", "CX_fp", "Z_p")):
        A2, t2 = conj(SWAP, g)
        tgt = names.get(A2, "(not in the pool)")
        extra = f" + translation {t2}" if any(t2) else ""
        print(f"    {nm:6s} -> {tgt}{extra}")

    # C: the duality is not an operation on the affine ISA at all -- Pass 4335.
    print(f"""
  AND C IS NOT AVAILABLE, which is the finding rather than an obstacle.  The point-line
  duality acts on the two projective carriers.  Pass 4335 established that the ISA's
  translation descends to NEITHER of them -- it disagrees on 40 of 40 points -- so the
  duality is not an operation on this instruction set.  There is no C to multiply by.

  So the CPT analogy breaks at the point where it would have been informative.  P is
  violated ({p_ok}) because conjugating by the p/f exchange sends F_p to F_f, which the
  shipped ISA does not contain.  T is violated ({t_ok}) because the opcodes are not
  involutions.  PT is {'a symmetry' if pt_ok else 'still violated'}, and no third factor exists to rescue it.

  THE HONEST READING.  A field theory's CPT theorem is a consequence of Lorentz invariance
  and locality; this machine has neither, so the analogy was never entitled to the
  conclusion.  What the exercise does establish is sharper than a slogan: the machine's two
  asymmetries are independent AS INVOLUTIONS TOO, not merely as measured defects, because
  neither P nor T maps the ISA to itself and their product does not either.  Pass 4314
  showed the defects do not share a cause; this shows the corresponding symmetries do not
  compose into one.""")
    return {"P_symmetry": bool(p_ok), "T_symmetry": bool(t_ok),
            "PT_symmetry": bool(pt_ok), "C_available": False,
            "reason_C_unavailable": "the ISA translation descends to neither projective "
                                    "carrier (Pass 4335)",
            "cpt_theorem_applies": False,
            "why": "no Lorentz invariance, no locality; the analogy is not entitled to it"}


# ------------------------------------------------------------------ 4337
def pass_4337() -> dict:
    print()
    print("=" * 78)
    print("Pass 4337 -- what the machine dissipates, in watts")
    print("=" * 78)
    kTln2 = K_B * T_ROOM * log(2)
    print(f"  Landauer bound at {T_ROOM:.0f} K : kT ln2 = {kTln2:.4e} J per bit erased")
    print(f"  measured clock (Pass 2833)  : {CLOCK_HZ / 1e6:.2f} MHz\n")

    readout_bits = 8 / 3          # Pass 2836, exact
    rows = []
    for name, bits_per_instr, note in (
            ("compute, machine A (4 opcodes)", float("inf"),
             "irreversible: one-way transitions exist"),
            ("compute, machine D (reversible closure)", 0.0,
             "exactly zero, Pass 4321"),
            ("support readout, per readout", readout_bits, "8/3 bits, Pass 2836"),
            ("readout at the 15-instruction mixing cadence", readout_bits / 15,
             "amortised over the cadence Pass 2867 sets")):
        if bits_per_instr == float("inf"):
            print(f"  {name:44s} unbounded   ({note})")
            rows.append({"item": name, "watts": None, "note": note})
            continue
        w = bits_per_instr * kTln2 * CLOCK_HZ
        print(f"  {name:44s} {w:.4e} W   ({note})")
        rows.append({"item": name, "bits_per_instruction": bits_per_instr,
                     "watts": w, "note": note})

    readout_w = readout_bits / 15 * kTln2 * CLOCK_HZ
    print(f"""
  THE WHOLE THERMODYNAMIC BUDGET IS THE READOUT.  A reversible machine running flat out at
  {CLOCK_HZ / 1e6:.0f} MHz dissipates exactly nothing for computing, and {readout_w:.3e} W --
  about {readout_w * 1e15:.1f} femtowatts -- for looking at its own register on the schedule
  that mixing permits.  That is fifteen orders of magnitude below any real device's static
  power, which is the point: Landauer is not what limits this machine, and saying so with a
  number is more useful than saying computation is "free".

  The four-opcode machine has no finite figure at all.  Its entropy production is unbounded
  because one-way transitions exist (Pass 4252): a trajectory reveals the direction of time
  with certainty, and no rate converts that into joules without a model of how the
  irreversible step is physically implemented.  That is a real gap in the specification, not
  a small number -- and it is the strongest engineering argument for the reversible closure
  that Pass 4279 priced at 1.95x the cells.

  Scope: this is the LANDAUER floor, the thermodynamic minimum for the logical operations.
  It is not a power estimate for any implementation, where switching energy exceeds kT ln 2
  by orders of magnitude.""")
    return {"kT_ln2_joules": kTln2, "clock_hz": CLOCK_HZ, "temperature_K": T_ROOM,
            "rows": rows, "readout_watts_at_cadence": readout_w,
            "machine_A_finite": False}


# ------------------------------------------------------------------ 4338
def pass_4338() -> dict:
    print()
    print("=" * 78)
    print("Pass 4338 -- the zeta as a partition function, and where it goes critical")
    print("=" * 78)
    A = simple(ISA)
    mods = np.abs(pencil(A))
    rho = float(mods.max())
    R = 1.0 / rho
    nt = mods[(mods > 1 + 1e-9) & (np.abs(mods - rho) > 1e-6 * rho)]
    crit = sqrt(rho)

    print("  Read u as a fugacity and zeta(u) as a partition function over closed")
    print("  non-backtracking orbits.  Then:\n")
    print(f"    radius of convergence R = 1/rho    : {R:.9f}")
    print(f"    'critical fugacity'  sqrt(R)       : {sqrt(R):.9f}")
    print(f"    free energy per step  log rho      : {log(rho):.9f} nats"
          f"  ({log2(rho):.6f} bits)")
    print(f"    non-trivial singularities          : {len(nt)}")
    print(f"    fraction on the critical circle    : "
          f"{float((np.abs(nt - crit) < 1e-6 * crit).mean()):.4f}")

    # Where the singularities actually sit, as a radial distribution.
    band = (nt.min(), nt.max())
    print(f"    they instead spread over |lambda|  : {band[0]:.4f} .. {band[1]:.4f}")
    print(f"    the critical circle sits at        : {crit:.4f}")
    inside = int((nt < crit).sum())
    outside = int((nt > crit).sum())
    print(f"    inside / outside the circle        : {inside} / {outside}")
    print(f"""
  THE GRAPH RH IS A STATEMENT ABOUT PHASE STRUCTURE.  For a graph satisfying it -- the Levi
  graph, W(3,3), every one of the 28 Spence graphs -- all non-trivial singularities lie on
  ONE circle, so the partition function has a single critical radius and one transition.
  The instruction layer instead spreads its singularities from {band[0]:.3f} to {band[1]:.3f},
  with {inside} inside the critical circle and {outside} outside.

  In statistical-mechanical language that is the difference between a system with one
  critical point and one whose singularities smear across a band: there is no single
  temperature at which the instruction stream goes critical, because the relaxation modes do
  not share a scale.  Pass 4283 saw the same thing as forbidden bands in the modulus
  histogram; this is the thermodynamic reading of that picture.

  Where the analogy stops, stated so it is not over-read: u is a formal fugacity, not a
  physical temperature, and log rho is a growth rate, not a measured free energy.  Nothing
  here is a claim about a physical phase transition in any device.  What is exact is the
  singularity structure, and the observation that the well-behaved layer of this machine is
  the geometric one while the computational layer is the smeared one.""")
    return {"rho": rho, "R": R, "critical_modulus": crit,
            "free_energy_per_step_nats": log(rho),
            "nontrivial": int(len(nt)),
            "band": [float(band[0]), float(band[1])],
            "inside_circle": inside, "outside_circle": outside,
            "single_critical_point": False}


def main() -> int:
    out = {"pass_4336_cpt": pass_4336(),
           "pass_4337_watts": pass_4337(),
           "pass_4338_criticality": pass_4338()}
    p = ROOT / "data" / "PART_W33_PASS4336_4338_CPT_WATTS_CRITICALITY.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
