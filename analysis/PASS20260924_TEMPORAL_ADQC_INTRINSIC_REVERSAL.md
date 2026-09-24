# 24 September 2026 — temporal ADQC, intrinsic reversal, and cyclotomic universality

## Status

This packet separates universal qutrit computation, temporal self-entanglement,
operational elapsed change, thermodynamic arrow, and the finite W33 control
geometry.

Strongest exact results:

- a fixed-interaction ancilla-driven qutrit compiler is universal on a
  stationary qutrit register;
- the 27 Bell-shell contexts are equivariantly the quadratic phase space
  Sym_2(F3), not merely count-matched to it;
- reference entanglement upgrades SWAP-break-SWAP from memory to quantum memory;
- the modular qutrit clock carries the same A2 Weyl representation as BT943;
- qutrit transpose / Liouville left-right exchange intrinsically produces the
  BT172 outer-involution class;
- the proposed 26-class F4 fold and the global 90=9+81 module split both fail;
- the finite 27-history atlas is Clifford, while universality enters through a
  basis-dependent mu_9 analyzer program.


## 1. Universal computation: move the photon, not the whole register

The scalable replacement for the old exactly-one-photon register is a flying
photonic qutrit used as an ancilla/program head. Long-lived qutrit memories hold
the scalable quantum state.

With E_AR=(F_A^dagger tensor F_R)CZ_AR, one fixed ancilla state and a programmed
three-outcome analyzer implement

    K_m=(1/sqrt(3)) X^(-m) F R(theta).

The outcomes are equiprobable and the Pauli byproduct is tracked classically.
The same fixed interaction used on two memories gives

    K_m=(1/sqrt(3))(X^m tensor I)(F tensor F)CZ.

A basis-dependent ninth-root qutrit T phase is obtained by analyzer programming.
This does not make fault tolerance free: the non-Clifford analyzer is the
physical resource that must be protected.

A single particle carrying n independent qutrits only as orthogonal modes needs
at least 3^n modes. The photon is therefore a mobile head/bus, not scalable
memory.


## 2. The 27 histories are an actual S4 module

BT858/BT860 already proved that the 27 W33 lines skew to a Bell line form an
affine torsor for F3^3, with line-parabolic quotient S4.

The new verifier constructs that actual quotient representation and compares it
with the PGL(2,3)=S4 congruence action on Sym_2(F3). An explicit GL(3,3)
conjugator exists:

    Q = [[0,1,0],
         [0,0,1],
         [1,0,0]].

Consequently the Bell-shell contexts admit equivariant symmetric-matrix labels.
Their rank/discriminant census is exactly

    27 = 1 + 8 + 6 + 12.

After choosing a torsor origin this is an affine quadratic-action atlas rather
than a numerical analogy.

## 3. Quantum temporal memory is stronger than state retrieval

BT3717's SWAP-break-SWAP comb proves operational memory, but a classical trit
memory passes all computational-basis retrieval tests.


The reference-entanglement upgrade separates the resources exactly:

- coherent qutrit memory: negativity 1, Bell fidelity 1;
- classical label memory: negativity 0, Bell fidelity 1/3;
- depolarizing memory: N(p)=max(0,(3-4p)/3), F(p)=1-8p/9.

The coherent temporal link becomes entanglement-breaking at p=3/4.

The operational statement is sharp: retrieval after a causal break proves
memory; preservation of reference entanglement proves quantum memory.

## 4. The modular qutrit clock is exactly A2

For a faithful qutrit state diag(p0,p1,p2), the matrix units E_ij have modular
frequencies log(p_j/p_i). The six off-diagonal modes therefore carry

    +/-h1, +/-h2, +/-(h1+h2),

the six A2 roots evaluated on the two log-population ratios.

More strongly, the two elementary population swaps act on the log-ratio plane
by matrices whose transposes are exactly BT943's two A2 simple reflections.
The modular clock is therefore the contragredient of an A2 Weyl plane already
present in the repository.


At the tracial point all six modular frequencies vanish. Yet a globally
stationary three-step Page-Wootters history has nonzero conditional evolution
and closed-path Bures length 3*pi/2. Relational change and thermodynamic arrow
are therefore distinct.

## 5. Intrinsic temporal reversal closes BT172

In one-qutrit Liouville coordinates the two-sided Weyl action is labelled by
(u,v), with form [u,u']-[v,v']. Temporal left/right reversal is

    S(u,v)=(v,u).

Set s=u+v and d=2J(u-v). The explicit basis change H:(u,v)->(s,d) obeys

    H^T J_W33 H = J_L,
    H S H^-1 = diag(I2,-I2).

The second matrix is exactly the anti-symplectic W33 similitude used by the full
order-51840 automorphism group. Transport through the intrinsic center-quad
45-point quotient gives cycle shape 1^7 2^19 and is PSp-conjugate to BT171/172.

The eight fixed W33 rays split into two four-point Lagrangian lines. The + line
pulls back to u=v, so Phi_(u,u)(A)=P_u A P_u^dagger is the unitary CPTP
diagonal. The second line is the reversal mirror sector.


This replaces the earlier temporal-reversal analogy by an intrinsic operator
construction. The pointwise BT169 labeling remains a quotient gauge, so the
correct claim is equality of the outer conjugacy class rather than canonical
equality of stored permutation arrays.

## 6. Two tempting bridges fail

First, the unique common degree-90 W(E6) constituent is irreducible. Even after
restriction to the local order-1296 qutrit stabilizer it decomposes as

    90 = 4+6+6+8+8+12+12+16+18,

not 9+81. The 9+81 state/action picture is useful grading, not an invariant
module decomposition.

Second, the 26 orbit classes of temporal reversal do not carry a W(F4)
centralizer. The full centralizer has order 96; its faithful action on the 26
classes has order 48, orbit sizes 1,3,4,6,12, and the element-order fingerprint
of C2 x S4. The F4 route is rejected.

## 7. W33 is the Clifford history plane

For S in Sym_2(F3), the quadratic phase U_S on F3^2 obeys

    U_S U_T = U_(S+T),   U_S^3 = I.

All 27 gates normalize the two-qutrit Pauli group.


By contrast qutrit T=diag(1,zeta9,zeta9^-1) is non-Clifford and satisfies
T^3=Z. The relevant phase lift is basis-dependent mu_9, not a scalar ninth root.
This agrees with the repository's earlier no-go for the scalar A8^3 Z9 center.

The finite W33 history geometry is therefore the exact Clifford/control
skeleton. Universality enters through a cyclotomic analyzer program beyond that
finite skeleton.

## 8. Computation separates change from arrow

For every tested input density matrix, one ADQC local gate produces the uniform
record distribution (1/3,1/3,1/3), while Pauli-frame correction restores the
same deterministic unitary channel.

One ideal adaptive step therefore creates ln(3) nats = log2(3) bits of branch
record even though the corrected logical evolution is reversible. Resetting a
symmetric trit register at 300 K has Landauer floor

    k_B T ln(3) = 4.55039387321201e-21 J.

This is a machine-level realization of the conceptual separation: logical state
update can be reversible; historical record formation and reset can carry the
irreversible arrow.


For the frozen-room thought experiment: if all internal relational observables
truly remain unchanged, the room's operational state-space event length is
zero. An external coordinate parameter can still label that stationary state,
and a globally stationary history can still contain relational change in
correlations. "No updates" and "no physical time whatsoever" are therefore not
equivalent claims.

## Reproduction

Primary producers:

- analysis/w33_20260924_single_photon_adqc_qutrit_universality.py
- analysis/w33_20260924_bell_shell_quadratic_history_intertwiner.py
- analysis/w33_20260924_temporal_quantum_memory_witness.py
- analysis/w33_20260924_modular_a2_event_clock.py
- analysis/w33_20260924_intrinsic_transpose_outer.py
- analysis/w33_20260924_liouville_swap_cp_outer_bridge.py
- analysis/w33_20260924_temporal_f4_fold_probe.py
- analysis/w33_20260924_adqc_record_arrow.py
- analysis/w33_20260924_bell_shell_clifford_cyclotomic_lift.py

Focused regressions are in tests/test_w33_20260924_single_photon_adqc_qutrit_universality.py
and tests/test_w33_20260924_temporal_adqc_breakthroughs.py.
