# 2026-09-24 — Temporal self-entanglement, event time, and the mobile-photon computer

## Status

**PASS — five exact finite/circuit theorems; emergent-spacetime claims remain hypotheses.**

This packet develops the temporal interpretation without identifying three optical time bins
with two simultaneous qutrit tensor factors. It combines the repository's exact Liouville,
Bell-shell, homology, and photonic-control results with process-tensor, Page-Wootters,
modular-flow, quantum-speed-limit, and ancilla-driven-computation ideas.

The central refinement is:

> correlation supplies relational order; a channel supplies update; distinguishability
> supplies elapsed event-time; a state can select a modular clock scale; irreversible
> affinity supplies a preferred arrow.

Those statements are deliberately separated. None alone is promoted to a derivation of
Lorentzian spacetime.
## 1. If every particle in the room were frozen, is time happening?

There are two different questions.

**Internal operational question.** If every physically distinguishable degree of freedom
available to an observer is unchanged — including every clock, record, phase relation, and
memory — then the event-time functional used here assigns zero elapsed internal change.
There are no internal ticks with which to distinguish one putative instant from another.

**Standard spacetime question.** Special/general relativity does not infer from that fact
that the spacetime interval has disappeared. An external clock may assign a nonzero
coordinate/proper-time interval to a stationary subsystem. Moreover, a globally stationary
quantum state can encode nontrivial relational evolution between a clock and a system.

So the defensible claim is not "no change implies time literally ceases to exist." It is:

> without distinguishable relational change, a closed subsystem has no internally
> operational elapsed event-time.

Page-Wootters makes the distinction sharp: global stationarity and internal relational
evolution can coexist.
## 2. A five-layer temporal stack

The packet keeps five structures distinct.

1. **Causal/order structure** — which interventions can precede which others.
2. **Relational clock** — conditioning one subsystem on a clock/reference subsystem.
3. **State update** — the unitary, channel, or process tensor that changes conditional state.
4. **Elapsed event-time** — geometric length accumulated through distinguishable state space.
5. **Arrow/orientation** — irreversible cycle affinity, entropy production, boundary bias,
   or persistent record formation.

A modular flow sits between layers 2 and 5: for a faithful state it supplies a
state-selected internal frequency scale. A tracial state makes that particular modular
generator trivial, but it does not erase every possible relational history.

This repairs the stronger earlier slogan "the Bell state is the timeless now." A better
description is: the tracial Bell vector is a balanced, unoriented temporal bridge for which
the state-selected modular clock is trivial.

## 3. Exact theorem A — coherent temporal memory needs a reference witness

Pass 3717 already implements the qutrit SWAP -> causal break -> SWAP memory comb.
Basis-state retrieval proves operational memory, but it cannot distinguish coherent qutrit
memory from a classical memory that merely stores the label 0,1,2.
The new producer adds a reference qutrit. Starting from the maximally entangled qutrit
Bell state, the ideal coherent memory preserves the final reference-system Bell state.
Its negativity is exactly 1 and its Bell fidelity is 1.

A computational-basis label memory passes all three basis-state retrieval tests but returns
the dephased state (1/3) sum_j |jj><jj|, with negativity 0 and Bell fidelity 1/3.

Therefore preservation of reference entanglement across the causal break is a sufficient
certificate that the memory carried quantum coherence.

For the depolarizing recovered channel

    rho_p = (1-p)|Omega_3><Omega_3| + p I_9/9,

the verifier obtains

    F_Omega = 1 - 8p/9,
    Negativity = max(0,(3-4p)/3).

The recovered one-slot channel becomes entanglement-breaking at p=3/4.

Important boundary: entanglement-breaking does not imply a completely classical memory
resource for a general multi-time process. Higher-order temporal correlations can remain
nonclassical. Reference-entanglement survival is a strong sufficient witness, while its
loss is not a complete process-tensor classification.
Artifact: analysis/w33_20260924_temporal_quantum_memory_witness.py.

## 4. Exact theorem B — the qutrit modular clock is an A2 root clock

For a faithful diagonal qutrit state rho=diag(p0,p1,p2), the finite modular operator acts
on matrix units as

    Delta_rho(E_ij) = (p_i/p_j) E_ij,

so the modular generator has frequencies omega_ij=log(p_j/p_i). There are three zero
diagonal modes and six directed off-diagonal modes. With

    h1 = log(p0/p1),   h2 = log(p1/p2),

the six directed frequencies are exactly

    +/-h1, +/-h2, +/-(h1+h2),

the A2 root pattern evaluated on the two-dimensional log-population vector.

The stronger repo bridge is matrix-exact. Swapping populations 0<->1 and 1<->2 acts on
(h1,h2) by M01=[[-1,0],[1,1]] and M12=[[1,1],[0,-1]]. The repo's BT943 A2
simple reflections are S1=[[-1,1],[0,1]] and S2=[[1,0],[1,-1]].
The producer proves M01^T=S1 and M12^T=S2. Thus the modular log-ratio plane
carries the **contragredient of the exact A2 Weyl representation already present in BT943**.
This is stronger than the previous statement that the six frequency differences merely
look like A2 roots.

At the tracial point p0=p1=p2 all six modular frequencies collapse to zero.

Artifact: analysis/w33_20260924_modular_a2_event_clock.py.

## 5. Exact theorem C — stationary history and nonzero event-time are compatible

The same producer constructs the three-step relational history

    |Psi> = (1/sqrt(3)) sum_n |n>_C tensor X^n|0>_S.

With the forward-shift convention used by the executable,

    (X_C tensor X_S)|Psi> = |Psi>.

The global state is stationary under the paired transformation, while conditioning on the
clock gives |0>, |1>, |2>. This is a finite Page-Wootters history.

For elapsed operational change, define a discrete event-time length by summing Bures angles
between successive conditional states. Three idle updates have length zero. The closed
orthogonal cycle |0> -> |1> -> |2> -> |0> returns to its starting state yet has length

    T_Q = 3 pi / 2.
Elapsed change is therefore neither operation count nor endpoint displacement.

A separate oriented three-cycle with forward/reverse rate ratio 2 has affinity
A_cycle=3 log 2>0, while the equilibrium cycle has affinity zero. This gives an executable
separation:

- reversible cycle: event-time can be positive while arrow coordinate is zero;
- driven cycle: event-time and arrow coordinate can both be positive;
- idle process: event-time is zero.

Quantum-speed-limit theory supplies the complementary rate statement: distinguishability
cannot accumulate arbitrarily quickly for a fixed generator/resource budget. The packet
does not identify Bures length itself with SI seconds.

## 6. Exact theorem D — 27 Bell-shell histories are an equivariant quadratic-action space

Previous repo work proves that the 27 W33 lines disjoint from a chosen Bell line form a
torsor for the elementary group F3^3, with Bell-line parabolic 3^3:S4 and quotient S4.
The temporal draft independently proposed labeling 27 skew contexts by symmetric 2x2
matrices over F3.

The new verifier solves the representation problem instead of matching counts. It constructs
the actual S4 action on the Bell-shell translation kernel and the PGL(2,3)=S4 congruence
action S -> G S G^T on Sym_2(F3).
A GL(3,3) conjugacy exists, with explicit intertwiner

    Q = [[0,1,0],
         [0,0,1],
         [1,0,0]].

So, after choosing an affine torsor origin,

    Bell-shell F3^3 ~= Sym_2(F3)

equivariantly under the actual S4 quotient action.

The symmetric-matrix orbit census is exactly

    27 = 1 zero + 8 rank-one + 6 invertible-det-1 + 12 invertible-det-2.

This promotes the draft's "27 quadratic histories" from a numerical resemblance to a
finite-module theorem.

Artifact: analysis/w33_20260924_bell_shell_quadratic_history_intertwiner.py.

## 7. Exact theorem E — those 27 histories are 27 quadratic Clifford programs

For each symmetric S in Sym_2(F3), define on two-qutrit computational coordinates x

    U_S |x> = omega^((1/2) x^T S x) |x>.
The executable verifies all 27 matrices and all 81 two-qutrit Weyl labels. It proves

    U_S U_T = U_(S+T),

and

    U_S [X(a) Z(b)] U_S^dagger ~ X(a) Z(b + S a),

where ~ means equality up to a global Pauli phase. Thus the induced phase-space action is
the symplectic shear [[I,0],[S,I]].

Therefore the 27 Bell-line-skew contexts are not only possible history contexts: they form
an equivariant atlas of **27 reversible two-qutrit quadratic Clifford phase programs**.

This matters for interpretation. W33 can supply a timeless reversible program geometry
without supplying a thermodynamic arrow. A direction through that geometry must be chosen
by clock conditioning, boundary data, measurement record, or nonequilibrium affinity.

It also creates a direct bridge to the mobile-photon architecture on current master: the
27 quadratic programs sit entirely in its reversible Clifford layer. The non-Clifford
resource still lives in the programmed photonic analyzer, not in these 27 history labels.

Artifact: analysis/w33_20260924_bell_shell_quadratic_clifford_programs.py.

## 8. Exact theorem F — local temporal flatness can hide global phase memory
The repo already knows graph cycle dimension 201, triangle-boundary rank 120, and
H1 dimension 81. The new complex-connection producer does not claim those ranks anew.
It uses them.

On an oriented edge define

    C_xy = (1/2) log(k_xy pi_x / (k_yx pi_y)) + i theta_xy.

Its real part is stochastic/thermodynamic affinity; its imaginary part is coherent phase.
Around a cycle,

    integral C = Sigma_C/2 + i Phi_C.

The producer constructs an exact F3-valued edge cocycle that has zero circulation on
**every one of the 160 filled W33 triangles**, is not a vertex gradient, and has nonzero
period on the graph cycle space. Adding any exact vertex gauge leaves all periods fixed.

Therefore local triangle-flat phase does not imply globally trivial relational phase.
This is the natural H1-dual sector: locally flat, globally holonomic coherent memory.
The number of nonzero coordinates in the particular deterministic cycle basis is
basis-dependent; existence of a non-exact flat class is the invariant statement.

A separate triangle benchmark verifies four logically distinct sectors: flat;
reversible-coherent; irreversible-affinity; and driven-quantum.

Artifact: analysis/w33_20260924_complex_temporal_holonomy.py.
## 9. Universal-computation synthesis: the photon becomes the event/program head

The fixed-interaction universality packet already on current master changes the scalable
meaning of "single photon." One flying photonic qutrit is a mobile ancilla/program head;
stationary qutrit memory nodes carry the tensor-product quantum state.

The fixed interaction is

    E_AR = (F_A^dagger tensor F_R) CZ_AR.

Adaptive three-outcome photon measurement programs arbitrary diagonal phases. Together
with Fourier gates and the same photon's two-memory interaction, this gives local
Clifford+T and entangling CZ on the stationary register. A coherent even-length photon
sweep also compiles multi-memory weighted graph entanglers.

The temporal synthesis is now unusually clean:

1. the photon's route orders candidate interactions;
2. the fixed E_AR supplies reversible state update;
3. the analyzer outcome supplies an event boundary and byproduct label;
4. the memory trajectory supplies event-time through distinguishability;
5. the Pauli-frame record stores classical history;
6. irreversible record erasure or nonequilibrium driving can supply thermodynamic arrow.

This avoids saying that a photon must experience its own proper time. A photon has no
ordinary rest frame.
The architecture can instead use laboratory time, path/phase, time-bin labels, a matter
clock, or a Page-Wootters relational clock.

It also avoids the exponential one-particle-memory trap. Encoding n independent qutrits
only as orthogonal modes of one photon requires at least 3^n modes. The mobile-head model
keeps the carrier local dimension fixed while the memory scales in nodes.

## 10. What the frozen-room thought experiment now means mathematically

Suppose a subsystem follows a constant density operator rho_n=rho for every internal event
label. Then the Bures event-length used here is zero. If every internal clock and record is
also frozen, the subsystem has no operational procedure that distinguishes one internal
instant from another.

But three caveats are essential.

- An external clock may still measure elapsed spacetime time.
- A global stationary state may contain relational clock-system evolution.
- A quantum "frozen room" is not generally a classical configuration with every field
  degree of freedom assigned simultaneously sharp values.

The useful hypothesis is therefore relational, not absolute:

> time-for-a-subsystem is operationally reconstructed from distinguishable ordered
> relations; a preferred future direction requires extra asymmetry or irreversible
> record structure.
To turn that into a fundamental spacetime theory, the project would still have to derive a
continuum causal/Lorentzian geometry and recover proper-time phenomenology rather than
assuming it.

## 11. External anchors

- Page & Wootters, Phys. Rev. D 27, 2885 (1983): dynamics from stationary observables and
  internal clock correlations.
- Gemsheim & Rost, Phys. Rev. Lett. 131, 140202 (2023): system Schrodinger evolution
  derived from a globally stationary interacting state.
- Connes & Rovelli, gr-qc/9406019: thermal-time hypothesis from state-selected modular flow.
- Pollock et al., PRA 97, 012127 (2018) and PRL 120, 040405 (2018): process tensors and
  operational memory under interventions and causal breaks.
- Deffner & Campbell, J. Phys. A 50, 453001 (2017): geometric quantum speed limits based
  on distinguishability.
- Moreva et al., Phys. Rev. D 96, 102005 (2017): experimental Page-Wootters-style
  multitime correlations with a single photon.
- Proctor et al., PRA 95, 052317 (2017): universal ancilla-driven qudit computation from
  a fixed ancilla-register interaction plus adaptive ancilla measurement.
- Appleby, arXiv:0909.5233: finite-field metaplectic/Clifford representation.
- Labib, Quantum 6, 645 (2022): prime-dimensional stabilizer states as quadratic phase
  functions.
- Phys. Rev. Research (2025), Entanglement-breaking channels are a quantum memory
  resource: warning that entanglement-breaking does not imply fully classical multitime
  memory.

## 12. Evidence firewall

**Proved here:** the reference-memory witness, modular/A2 contragredient bridge,
Page-Wootters finite history, Bures event-length examples, Bell-shell/Sym2 intertwiner,
27-element quadratic Clifford program group, and complex phase/affinity separation.

**Prior repo results used:** W33 geometry, Bell-shell F3^3 torsor, BT943 A2 matrices,
201/120/81 chain ranks, and the fixed-interaction mobile-photon universality packet.

**Not proved:** literal past/future photon subsystems, photon proper-time evolution,
Lorentzian spacetime emergence, gravity, cosmological arrow, or a fabricated process-tensor
experiment.

## 13. Artifacts

- analysis/w33_20260924_bell_shell_quadratic_history_intertwiner.py
- analysis/w33_20260924_bell_shell_quadratic_clifford_programs.py
- analysis/w33_20260924_temporal_quantum_memory_witness.py
- analysis/w33_20260924_modular_a2_event_clock.py
- analysis/w33_20260924_complex_temporal_holonomy.py
- tests/test_w33_20260924_temporal_self_entanglement_packet.py
