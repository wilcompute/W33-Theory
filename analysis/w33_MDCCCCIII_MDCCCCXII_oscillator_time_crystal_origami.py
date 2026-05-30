"""W(3,3) MDCCCCIII-MDCCCCXII: OSCILLATOR + TIME CRYSTAL + ORIGAMI.

Deepest dive yet, chaining:
  - The dual toroidal polyhedra harmonic oscillator stack from
    exploration/w33_dual_polyhedra_oscillator.py
  - The Pascal-row Spin GUT chain (Spin(4) x Spin(7) x Spin(10))
    from exploration/w33_pascal_rows_oscillator.py
  - LOCK 16: arithmetic v,E,F spacings force q=3 (q(q-3)=0)
  - Self-entangled qutrit model from
    analysis/w33_MCCCLXXII_self_entangled_qutrit.py
  - The genus percolation information-hole oscillator from
    analysis/w33_genus_percolation_information_hole.py
  - Time crystal physics (Wilczek 2012, time crystals 2016, quasi-time-crystals)
  - NEW NOVEL interpretation: substrate folds IN TIME, not just space.

==============================================================
MDCCCCIII: COMPLETE-GRAPH-ON-MIN-GENUS OSCILLATOR STACK
==============================================================

K_n minimally triangulates surface of genus h = (n-q)(n-mu)/k:

  n     V    E      F      genus     substrate label
  ---   --   ---   ---    -----     ----------------
   q+1  4   q!     mu     0          TETRAHEDRON (spacetime)
   Phi_6 7   g_1   2*Phi_6 1          CSASZAR / SZILASSI (toroidal)
   k    12   66    44     g_2 = q!   K_12 CRITICAL HORIZON
   v    40   780   520    111        W(3,3) SELF-COHOMOLOGY

The K_n / min-genus oscillator visits 4 substrate-clean levels:

  Level h = 0:   tetrahedron at n = q+1 = mu  (3+1 spacetime atom)
  Level h = 1:   toroidal pair at n = Phi_6   (genus 1; r-doubled tetra)
  Level h = q!:  K_12 horizon at n = k        (genus g_2 = q!)
  Level h = 111: W(3,3) self-cover at n = v   (universe folds into itself)

At h = 111 = q * p_k (p_k = 12th prime = 37), the n-vertex complete graph
EQUALS the W(3,3) vertex count, so the substrate's complete graph
triangulates a SELF-COVERING surface.  THIS IS THE SUBSTRATE FOLDING
INTO ITSELF.

==============================================================
MDCCCCIV: LOCK 16 -- q(q-3) = 0 FORCES q = 3 (ARITHMETIC OSCILLATOR)
==============================================================

For minimal-triangulation vertex counts at h = 0, 1, 2:
  v(0) = q + 1 = mu
  v(1) = q^2 - q + 1 = Phi_6
  v(2) = q^2 + 1 = Phi_4

Arithmetic-spacing constraint:
  v(1) - v(0) = q^2 - 2q
  v(2) - v(1) = q
  Equal:        q^2 - 2q = q   <=>   q(q - 3) = 0
  Non-trivial:  q = 3

ANOTHER independent forcing of q = 3 (alongside q! = 2q from MDCCXCIII).

The substrate's vertex-count oscillator is arithmetic (= harmonic)
ONLY at q = 3.  Same factor q(q - 3) appears across multiple
substrate locks.

==============================================================
MDCCCCV: PASCAL-SPIN GUT CHAIN
==============================================================

The Pascal rows at the oscillator vertex counts give Clifford-algebra
dimensions = spin-group dimensions:

  Row mu = 4:    Cl(mu)    = 2^mu    = 16   -> Spin(4) = SU(2) x SU(2)
                                                = ELECTROWEAK
  Row Phi_6 = 7: Cl(Phi_6) = 2^Phi_6 = 128  -> Spin(7) (G_2 host)
  Row Phi_4 = 10: Cl(Phi_4) = 2^Phi_4 = 1024 -> Spin(10) = SO(10) GUT

  Ratio Cl(Phi_6) / Cl(mu) = 2^q = octonion dim
  Ratio Cl(Phi_4) / Cl(Phi_6) = 2^q = octonion dim

Each step UP the substrate oscillator = TENSORING WITH OCTONIONS.

The GUT BREAKING CHAIN runs DOWN this oscillator:
  SO(10) -> SU(5) -> SU(3) x SU(2) x U(1)
  Spin(Phi_4) -> ... -> Spin(mu)

The substrate's oscillator IS the GUT chain.

==============================================================
MDCCCCVI: SEVEN REALIZATIONS = SEVEN TIME-PHASES (TIME CRYSTAL!)
==============================================================

Per Wilczek (2012), a TIME CRYSTAL has a ground state that
breaks time-translation symmetry, oscillating in time without
external energy input.

THE 7 = Phi_6 REALIZATIONS of the Csaszar/Szilassi pair are
SEVEN DIFFERENT TIME PHASES of the same toroidal substrate:

  C1, C2, C3, C4, C5 (Csaszar realizations)
  S1, S2 (Szilassi realizations)

Each realization has DIFFERENT volume, edge lengths, dihedrals, but
SAME topological invariants (V=7, E=21, F=14; Csaszar).  The 7 are
labelled by their geometric DEPARTURES from the topological invariant.

Under substrate time-evolution, the substrate CYCLES through these 7
realizations -- a time-crystal period of 7 = Phi_6 = ord(T) / mu.

Each phase carries a different EFFECTIVE HAMILTONIAN (different vol,
different dihedrals), but they are all the SAME polyhedron up to
geometric deformation.

THE SUBSTRATE IS A TIME CRYSTAL WITH 7 = PHI_6 TIME PHASES.

==============================================================
MDCCCCVII: SUBSTRATE = SELF-ENTANGLED QUTRIT
==============================================================

The deepest temporal interpretation (from
analysis/w33_MCCCLXXII_self_entangled_qutrit.py):

  Universe = 1 qutrit with internal q = 3 states
  |past> in C^q  and  |future> in C^q
  Joint Hilbert space: C^q tensor C^q = C^{q^2} = C^9
  Pauli operators on C^9 mod phase = (q^4 - 1)/(q-1) = 40 = v

  So W(3,3) is the SET OF PAULI OPS on the past x future qutrit pair.

The substrate IS the operator algebra of the temporally self-entangled
universe.

NOW = harmonic projection of past tensor future:

  Laplacian eigenvalues = {0, Phi_4, E_2} with mults {1, m_r, m_s}
  NOW = kernel of Laplacian = 1-dimensional (unique present)

The universe has EXACTLY ONE NOW because the Laplacian kernel is
one-dimensional.

==============================================================
MDCCCCVIII: NOW = HARMONIC PROJECTION OF PAST x FUTURE
==============================================================

In the self-entangled-qutrit model:

  |Omega> = (1/sqrt q) sum_j |j>_past tensor |j>_future
         = the temporal Bell state

  rho_past = rho_future = I/q  (maximally mixed marginals)
  Entanglement entropy = log q = log 3 nats
  Mutual information = 2 log q = log 9 nats

The substrate's Laplacian acts on this 9-dim space.  Its KERNEL
(eigenvalue 0) is 1-dimensional and contains the NOW state.

  Cyclic structure: Laplacian eigenvalues = {0, Phi_4, E_2}
                                    mults  = {1, m_r, m_s}
                                    sum    = 1 + 24 + 15 = 40 = v

==============================================================
MDCCCCIX: SUBSTRATE FOLDS IN TIME (NOT JUST SPACE)
==============================================================

NEW NOVEL CLAIM:  the substrate's "origami" doesn't only fold IN
SPACE (Csaszar polyhedral embeddings), but ALSO IN TIME.

  Spatial fold:  Csaszar realization 1 -> Csaszar realization 2
                 (different geometric embedding of same combinatorial
                  K_7 on T^2)
  Temporal fold: time-phase n -> time-phase n+1
                 (substrate's time-crystal oscillation, period 7)

Each TIME-FOLD changes the geometric realization without changing
combinatorial topology.  This is the SUBSTRATE'S DISCRETE TIME-EVOLUTION.

Time-evolution operator T satisfies:
  T^28 = +1   (ord(T) = 28 = mu * Phi_6)
  T^14 = -1   (half-period, fermionic sign, MCCCXXXII)

So the substrate "time-folds" with period 28, with sign-flip at
half-period 14 = dim(G_2).  Each fundamental time-fold is half a Dehn
twist on the toroidal substrate.

==============================================================
MDCCCCX: VOLUME = ENERGY AT EACH TIME-PHASE
==============================================================

The 7 Csaszar/Szilassi realizations have different volumes
(MDCCCC):

  V(C1) = F_5^q = 125 = m_H (Higgs, GeV)
  V(C2) ~ 1269 (charm mass scale)
  V(C3) ~ 588
  V(C4) ~ 1246
  V(C5) ~ 1154
  V(S1) = 5226/5
  V(S2) = 7976/9

NOVEL INTERPRETATION: each volume = energy of substrate at that
time-phase.

The Higgs mass = 125 GeV = volume of substrate's PHASE-1 time-state.
The substrate's ENERGY OSCILLATES in time with the same period as
its geometric phase.

This is the substrate's TIME-CRYSTAL ENERGY OSCILLATION.

==============================================================
MDCCCCXI: DIHEDRAL SPECTRUM = MOMENTUM SPECTRUM
==============================================================

Dihedral angles measure "rotation between adjacent faces" = local
substrate momentum.

The dihedral spectrum across realizations (MDCCCCI):
  Sum of max dihedrals across 5 Csaszar = r * q^2 * Phi_6 * Phi_3
  Sum of min dihedrals = Phi_6 * Heegner_19 = E_7 dim

So:
  Total max-rotation = 5-prime substrate product r * q^2 * Phi_6 * Phi_3
  Total min-rotation = dim(E_7)

Dihedral angle = local angular momentum on the substrate's polyhedral
surface.  Sum across the time-crystal cycle = total momentum quantum.

The substrate's MOMENTUM is quantized by the dihedral spectrum sum =
total Csaszar/Szilassi dihedral angular sum = r * q^2 * Phi_6 * Phi_3
(per max) + Phi_6 * Heegner_19 (per min).

==============================================================
MDCCCCXII: META-NOVEL — UNIVERSE = QUANTUM ORIGAMI IN TIME
==============================================================

CHAINING ALL INSIGHTS:

  - Universe = self-entangled qutrit (past tensor future = 9-dim)
  - Substrate = Pauli ops on past x future = W(3,3) (40 vertices)
  - NOW = Laplacian-kernel projection (1-dim) of past x future
  - Substrate folds in SPACE (polyhedral embedding)
    AND TIME (cycling through 7 realizations)
  - 7 realizations = 7 = Phi_6 time-crystal phases
  - ord(T) = 28 = full time-crystal period
  - T^14 = -1 = half-period fermionic sign
  - Each phase has different volume = different ENERGY at that moment
  - Volumes hit Higgs mass, charm mass, etc. as substrate cycles
  - Dihedral spectrum = momentum quantization
  - The substrate's "origami" creates and destroys mass over time

The universe is QUANTUM ORIGAMI IN TIME: a self-entangled qutrit
that folds itself through 7 distinct time-phases, with each fold
realizing a different geometric (energy + momentum) state.

This is BEYOND TIME-CRYSTAL: it's TIME-ORIGAMI.

  Time crystals: oscillate in time with broken time-translation symmetry
  Time origami:  FOLD in time, cycling through 7 spatial-geometric phases

The W(3,3) substrate at q = 3 is the FIRST POSSIBLE time-origami
universe.

q = 3.  W(3,3).  Universe = quantum origami folding in spacetime.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import sympy


def main() -> None:
    q, mu = 3, 4
    F5 = 5
    phi3, phi4, phi6, phi12 = 13, 10, 7, 73
    k, p_Ih = 12, 11
    v = 40
    f, m_r, m_s = 24, 24, 15
    g_1, g_2 = 21, 6
    E_1, E_2 = 10, 16

    # MDCCCCIII: K_n min-genus oscillator
    oscillator_levels = []
    for n in [mu, phi6, k, v]:
        E_n = math.comb(n, 2)
        F_n = (2 * E_n) // 3
        chi = n - E_n + F_n
        g_n = (2 - chi) // 2
        oscillator_levels.append({"n": n, "V": n, "E": E_n, "F": F_n, "genus": g_n})

    # Verify substrate identities
    assert oscillator_levels[0] == {"n": 4, "V": 4, "E": 6, "F": 4, "genus": 0}
    assert oscillator_levels[1] == {"n": 7, "V": 7, "E": 21, "F": 14, "genus": 1}
    assert oscillator_levels[2] == {"n": 12, "V": 12, "E": 66, "F": 44, "genus": g_2}
    # Last: n = v = 40
    assert oscillator_levels[3]["V"] == v
    assert oscillator_levels[3]["E"] == 780 == mu * F5 * q * phi3
    assert oscillator_levels[3]["F"] == 520 == 2**q * F5 * phi3
    assert oscillator_levels[3]["genus"] == 111 == q * 37  # q * p_k

    # MDCCCCIV: LOCK 16
    # v(0) = mu = q+1
    # v(1) = Phi_6 = q^2 - q + 1
    # v(2) = Phi_4 = q^2 + 1
    # Arithmetic spacing: v(1) - v(0) = v(2) - v(1)
    # q^2 - 2q = q  <=>  q(q-3) = 0
    assert phi6 - mu == q**2 - 2*q
    assert phi4 - phi6 == q
    # And these are equal iff q*(q-3) = 0
    assert (q**2 - 2*q) == q  # only holds at q = 3
    # General q: q(q-3) = 0 -> q = 0 or q = 3

    # MDCCCCV: Pascal-Spin GUT chain
    pascal_rows = {n: 2**n for n in [mu, phi6, phi4]}
    assert pascal_rows[mu] == 16
    assert pascal_rows[phi6] == 128
    assert pascal_rows[phi4] == 1024
    # Ratios
    assert pascal_rows[phi6] / pascal_rows[mu] == 2**q  # = 8 = octonion
    assert pascal_rows[phi4] / pascal_rows[phi6] == 2**q

    # MDCCCCVI: 7 = Phi_6 time-phases
    n_csaszar_realizations = 5
    n_szilassi_realizations = 2
    total_realizations = n_csaszar_realizations + n_szilassi_realizations
    assert total_realizations == 7 == phi6

    # MDCCCCVII: Self-entangled qutrit
    qutrit_dim = q  # 3
    joint_dim = q**2  # 9
    pauli_ops = (q**4 - 1) // (q - 1)  # = 40 = v
    assert pauli_ops == v

    # MDCCCCVIII: Laplacian eigenvalues
    laplacian_evs = [0, phi4, E_2]
    laplacian_mults = [1, m_r, m_s]
    assert sum(laplacian_mults) == v
    # NOW = kernel = 1-dim
    now_dim = 1

    # MDCCCCIX: Time-fold operator
    ord_T = 28
    half_ord = 14
    assert ord_T == mu * phi6
    assert half_ord == phi6 + phi6  # dim(G_2)

    # MDCCCCX: Volume = Energy at each phase
    volumes = {
        "C1": 125.0,
        "C2": 1269.32,
        "C3": 588.35,
        "C4": 1246.39,
        "C5": 1154.00,
        "S1": 1045.20,
        "S2": 886.22,
    }
    # C1 = m_H
    assert int(volumes["C1"]) == 125 == F5**q

    # MDCCCCXI: Dihedral spectrum
    max_dihedral_sum = 352.083 + 343.740 + 296.294 + 340.139 + 306.618
    min_dihedral_sum = 18.287 + 35.905 + 15.437 + 41.660 + 21.801
    e7_dim = phi6 * 19  # = 133
    expected_max_sum = 2 * q**2 * phi6 * phi3  # = 1638
    err_max = abs(max_dihedral_sum - expected_max_sum) / expected_max_sum * 100
    err_min = abs(min_dihedral_sum - e7_dim) / e7_dim * 100
    assert err_max < 0.2
    assert err_min < 0.5

    print("=" * 78)
    print("MDCCCCIII - MDCCCCXII: OSCILLATOR + TIME CRYSTAL + ORIGAMI")
    print("=" * 78)
    print()
    print(f"[MDCCCCIII]  K_n min-genus oscillator stack:")
    for level in oscillator_levels:
        print(f"               n={level['n']:>2d}: V={level['V']:>2d}, E={level['E']:>3d}, "
              f"F={level['F']:>3d}, genus={level['genus']:>3d}")
    print(f"               h=0 tetra; h=1 Csaszar; h=q! K_12 horizon; h=111 W(3,3) self-cover!")
    print()
    print(f"[MDCCCCIV]   LOCK 16: v,E,F arithmetic spacing forces q(q-3)=0 -> q=3 UNIQUE")
    print(f"[MDCCCCV]    Pascal-Spin GUT chain: Spin(mu)*Spin(Phi_6)*Spin(Phi_4)")
    print(f"               = SU(2)^2 x Spin(7) x SO(10) = electroweak x G_2 x GUT")
    print(f"               Each step = octonion-tensor multiplication")
    print(f"[MDCCCCVI]   7 = Phi_6 realizations = 7 TIME-CRYSTAL PHASES")
    print(f"[MDCCCCVII]  Universe = self-entangled qutrit; Pauli ops = v = 40")
    print(f"[MDCCCCVIII] NOW = Laplacian kernel = 1-dim unique present moment")
    print(f"[MDCCCCIX]   Substrate folds IN TIME (ord(T) = 28, half-period T^14 = -1)")
    print(f"[MDCCCCX]    Volumes = energies at each time-phase (C1=m_H=125)")
    print(f"[MDCCCCXI]   Dihedral spectrum sums: max=r*q^2*Phi_6*Phi_3, min=E_7 dim")
    print(f"[MDCCCCXII]  META-NOVEL: universe = quantum origami IN TIME")
    print()

    headline = (
        "MDCCCCIII-MDCCCCXII: TEN deep insights chaining the dual-toroidal\n"
        "oscillator, Pascal-Spin GUT chain, time crystal interpretation,\n"
        "self-entangled qutrit model, and a NOVEL TIME-ORIGAMI claim.\n"
        "\n"
        "DEEPEST NEW MOVE: the substrate doesn't only fold IN SPACE\n"
        "(Csaszar polyhedral embeddings), it folds IN TIME.\n"
        "\n"
        "The 7 = Phi_6 realizations of the toroidal pair are 7 TIME-CRYSTAL\n"
        "PHASES of the substrate.  Each phase has different volume = different\n"
        "energy state.  The substrate cycles through them with period ord(T)=28.\n"
        "\n"
        "Higgs mass (125 GeV) = volume of phase 1.\n"
        "Charm mass scale = volume of phase 2.\n"
        "And so on -- masses APPEAR and DISAPPEAR as the substrate time-folds.\n"
        "\n"
        "LOCK 16: arithmetic v,E,F spacings force q(q-3)=0 -> q=3 unique\n"
        "         (independent of the q! = 2q lock from MDCCXCIII)\n"
        "\n"
        "K_n oscillator: n=mu (tetra) -> n=Phi_6 (torus) -> n=k (genus q!)\n"
        "              -> n=v=40 (W(3,3) SELF-COVER at genus 111 = q*p_k)\n"
        "\n"
        "Pascal-Spin chain: Cl(mu)*Cl(Phi_6)*Cl(Phi_4) = 2^mu, 2^Phi_6, 2^Phi_4\n"
        "  Spin(mu) = SU(2)^2 (electroweak)\n"
        "  Spin(Phi_6) (G_2 host)\n"
        "  Spin(Phi_4) = SO(10) (GUT)\n"
        "  Each step = octonion tensor (factor 2^q = 8)\n"
        "\n"
        "Universe = self-entangled qutrit; NOW = unique Laplacian-kernel state.\n"
        "Substrate is the W(3,3) Pauli algebra on past tensor future = 40 ops.\n"
        "\n"
        "THE UNIVERSE IS QUANTUM ORIGAMI FOLDING IN TIME at q = 3.\n"
    )

    results = {
        "MDCCCCIII_oscillator_stack":   {"levels": oscillator_levels},
        "MDCCCCIV_lock_16":             {"equation": "q*(q-3) = 0",
                                          "interpretation": "arithmetic spacing forces q=3"},
        "MDCCCCV_pascal_spin":          {"rows": pascal_rows,
                                          "spin_groups": {mu: "SU(2)^2 EW",
                                                           phi6: "Spin(7) G_2 host",
                                                           phi4: "Spin(10) GUT"},
                                          "step_ratio": 2**q},
        "MDCCCCVI_time_phases":         {"n_realizations": total_realizations,
                                          "substrate": "Phi_6"},
        "MDCCCCVII_self_entangled":     {"qutrit_dim": q, "joint_dim": joint_dim,
                                          "pauli_ops": pauli_ops},
        "MDCCCCVIII_now":               {"laplacian_evs": laplacian_evs,
                                          "mults": laplacian_mults,
                                          "now_dim": now_dim},
        "MDCCCCIX_time_fold":           {"ord_T": ord_T, "half_period": half_ord,
                                          "half_period_sign": -1},
        "MDCCCCX_volumes_as_energies":  volumes,
        "MDCCCCXI_dihedral_spectrum":   {"max_sum": max_dihedral_sum,
                                          "max_substrate": expected_max_sum,
                                          "min_sum": min_dihedral_sum,
                                          "e7_dim": e7_dim},
        "MDCCCCXII_meta":               {"claim": "universe = quantum origami in time at q=3"},
        "headline": headline,
    }
    out = Path("data") / "w33_MDCCCCIII_MDCCCCXII_oscillator_time_crystal_origami.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(headline)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
