# Passes 2967–2973 — Pareto-optimal information-system closure

## Evidence ladder

- **Exact finite mathematics:** Passes 2968, 2970, 2971, 2972, and 2973.
- **Exact inference/identifiability with synthetic counts:** Pass 2967.
- **Exact logical gate schedule with literature-backed decomposition models:** Pass 2969.
- **Source-complete RTL:** the nine-gate M36 microcode and the reversible Z3×Z4 clock.
- **Still open:** laboratory component calibration, Icarus/Yosys/nextpnr evidence, optical locality cost for arbitrary A40 words, and autonomous physical-clock behavior.

## System-level design decision

There is no scalar notion of “best” that simultaneously minimizes every physical, logical, thermodynamic, and calibration cost. The exact packet instead identifies a strict Pareto architecture:

1. retain the live state as four frame trits, ten spread-line labels, four slots, and one encode/check sector;
2. execute only native affine, symplectic, anti-symplectic, D4, and encode/check operations in the live path;
3. absorb static permutations into wiring and detector labels rather than realizing them as gates;
4. preserve all recoverable information reversibly until storage, export, or reset;
5. keep calibration statistics component-resolved;
6. use nonabelian triangle syndromes for route faults;
7. invoke binary frame-route ranking only at archival/reset boundaries.

This architecture minimizes live Boolean nonlinearity, avoids gratuitous erasure, preserves debuggability, and retains exact correspondence with the finite geometry.

## Pass 2967 — component-resolved Bayesian calibration

A single internally coherent reference run is frozen with counts

```text
launched                         200000
survived                         135000
OAM-correct given survival       131625
slot-correct given OAM-correct   130309
dark trials                     7800000
dark clicks                           78
```

The counts are synthetic and exist to validate the inference pipeline, not to claim a device performance.

Independent Jeffreys posteriors give the following medians and 95% credible intervals:

| Quantity | Median | 95% interval |
|---|---:|---:|
| survival | 0.674995 | 0.672941–0.677056 |
| OAM correct given survival | 0.975000 | 0.974156–0.975828 |
| slot correct given OAM correct | 0.990001 | 0.989453–0.990529 |
| dark probability per detector | 1.002e-5 | 7.966e-6–1.240e-5 |
| detected-click probability | 0.674860 | 0.672809–0.676920 |
| conditional address fidelity | 0.965066 | 0.964080–0.966038 |
| erasure/multiclick probability | 0.325140 | 0.323080–0.327191 |

The aggregate correct/wrong/erasure map has Jacobian rank two for four unknown component parameters. Therefore aggregate output counts cannot separately identify survival, OAM sorting, slot sorting, and dark rate. Component-resolved sufficient statistics are mandatory.

With zero observed errors and a Jeffreys prior, 1,920 trials are required for the one-sided 95% posterior lower bound to exceed 0.999.

Primary experimental literature demonstrates that OAM and time-frequency sorters must be characterized by their own crosstalk/fidelity matrices. Those reported efficiencies are boundary anchors, not values combined into this synthetic stack: Malik et al., QIM 2014, DOI 10.1364/QIM.2014.QW3A.6; Walsh et al., *Optics Letters* 43, 2256 (2018), DOI 10.1364/OL.43.002256; Serino et al., *Optics Express* 33, 5577 (2025), DOI 10.1364/OE.544206.

## Pass 2968 — minimum D4 fault-localization schedules

The ten spread lines form `K10` with 45 inter-line links and 120 triangles.

### Exact single-edge optimum

Each selected triangle covers three edges. If `m` selected triangles assign distinct nonzero binary signatures to all 45 edges, the smallest possible total signature weight is

\[
m+2(45-m)=90-m,
\]

whereas the actual incidence total is `3m`. Consequently `3m >= 90-m`, so `m >= 23`.

An explicit 23-triangle schedule attains the bound. Thus

\[
\boxed{m_{\text{single edge}}=23.}
\]

### Full nonabelian model through two faulty edges

Each faulty edge carries one of the seven nonidentity elements of `D4`. Including the no-fault case gives

\[
1+45\cdot7+\binom{45}{2}7^2=48,826
\]

hypotheses. The complete 120-triangle group-valued syndrome is injective on all 48,826.

The support pattern alone localizes the faulty edge set through weight two:

```text
single edge:          8 affected triangles
adjacent edge pair:  15 affected triangles
disjoint edge pair:  16 affected triangles
```

A verified 29-triangle schedule distinguishes every one- and two-edge D4 hypothesis. Twenty-nine is a construction, not yet a minimum theorem.

## Pass 2969 — reversible backend Pareto frontier

The exact binary joint-rank network has

```text
120 Toffoli + 79 CNOT = 199 gates
logical dependency depth = 94
Toffoli-bearing layers = 86
maximum parallel Toffoli count = 4
```

Backend resource models are:

| Backend | Resource profile |
|---|---|
| exact seven-T Toffoli | 840 T, zero ancilla, T-depth upper bound 258 |
| Selinger T-depth-one blocks | 840 T, T-depth upper bound 86, up to 16 clean ancillas |
| Jones measurement-assisted Toffoli | 480 T plus feed-forward |
| conservative relative-phase compute/uncompute | 612 T |
| temporary-logical-AND candidate | 460 T, pending explicit carry-network validation |
| native mixed-radix live controller | zero Boolean Toffoli for state retention |

The physical decision is therefore not to run the 199-gate converter continuously. The live controller retains `(four trits, ten lines, four slots)` and only converts to the twelve-bit binary rank when a record must be stored, exported, compared with a binary interface, or irreversibly reset.

The decomposition models follow Jones, arXiv:1212.5069; Selinger, arXiv:1210.0974; Maslov, arXiv:1508.03273. Their logical resource counts do not determine hardware latency without a target error-correction stack.

## Pass 2970 — dominating nine-gate M36 branch

The original compiled branch ended with two SWAPs. Both are static wire permutations:

- measured post-SWAP wires `(0,1)` are pre-SWAP wires `(2,3)`;
- output post-SWAP wires `(2,3)` are pre-SWAP wires `(0,1)`.

Move the final logical Hadamard through the relabeling to physical wire 1 and rename detector/output channels. The physical branch becomes

```text
6 CNOT + 3 H = 9 Clifford gates,
followed by Z(q2)=0 and Z(q3)=1.
```

It retains ideal success probability `1/2` and exact ray-7 fidelity.

Relative to the 15-gate branch:

| Quantity | Before | After |
|---|---:|---:|
| CNOT | 12 | 6 |
| total Clifford gates | 15 | 9 |
| enumerated fault events | 191 | 101 |
| two-qubit first-order coefficient | 2084/405 | 956/405 |
| measurement coefficient | 4/9 | 1/3 |
| coherent susceptibility sum | 556/27 | 274/27 |

The optimized first-order law is

\[
p_{\rm out}=\frac23p+\frac{140}{81}q_1+\frac{956}{405}q_2+\frac13q_m+O(2).
\]

This dominates the earlier circuit whenever output and detector labels may be assigned freely.

## Pass 2971 — complete native controller group

The controlled state space is

\[
2\times81\times40=6,480,
\]

where the first factor records encode/check duality.

Generated by four frame translations, the isodual quarter-turn `D`, anti-symplectic reversal `K`, and the D4 slot rotation/reflection, the native permutation group has exact order

\[
\boxed{30,233,088=2^9 3^{10}.}
\]

Its state orbits have sizes

```text
648, 648, 1296, 1296, 1296, 1296.
```

The route-only subgroup has order 192 and six route orbits of sizes

```text
4, 4, 8, 8, 8, 8.
```

Adding one symplectic transvection generates `A40` on the route addresses. This proves universal even address permutation is available from one extra geometric primitive. It does **not** mean every `A40` word is local or low-loss, and `A40` is not being identified with the automorphism group of W33.

Optimal policy: retain the smaller native group for ordinary operation and enable the transvection only when universal address permutation is genuinely required.

## Pass 2972 — outside-box minimal sufficient controller

Treat the controller as a Moore machine with observable output

```text
duality sector, OAM spread line, symplectic phase sigma
```

and the eight native transitions. Exact partition refinement gives

```text
60 -> 1980 -> 5616 -> 6048 -> 6048.
```

Therefore the unique coarsest future-observation-preserving quotient has

\[
\boxed{6,048\text{ states}.}
\]

Its class-size distribution is

```text
5832 singleton classes,
216 classes of size 3.
```

The quotient merges 432 raw states and reduces uniform-source entropy by

\[
0.1\log_2 3=0.1584962501\text{ bits},
\]

but both 6,480 and 6,048 states require thirteen fixed bits. Hence the quotient is valuable for formal verification, cache deduplication, and theorem-level sufficiency—not for the live hardware register. The transparent mixed-radix state is the better physical implementation.

## Pass 2973 — outside-box D12 curvature clock

Let

\[
a=(1,2,0,0),\qquad K a=-a.
\]

Define one logical clock step `C` as frame translation by `a` together with the global order-four D4 slot rotation. Define reversal `R` as frame action by `K` together with D4 reflection. Then

\[
C^{12}=I,\qquad R^2=I,\qquad RCR=C^{-1}.
\]

Thus

\[
\langle C,R\rangle\cong D_{12},\qquad |D_{12}|=24.
\]

Every one of the 6,480 controller states lies on a twelve-cycle:

\[
\boxed{6,480=540\times12.}
\]

A fixed symplectic pilot with `sigma(a,p)=1` supplies a mod-three phase tick, while the route slot supplies a mod-four tick. Their CRT pair labels all twelve phases.

This gives a reversible, geometry-native event counter with built-in time reversal and a route-fault hook through the curvature pilot code. The equality with earlier 540-fiber structures in the repository is a concrete structural conjecture, not yet an objectwise identification.

Falsification boundary: this is not an autonomous time crystal, does not spontaneously break time-translation symmetry, and has no demonstrated energetic protection. It is a logical phase clock whose physical rate must still be supplied by hardware.

## Globally optimal architecture selected by the packet

```text
LIVE STATE
  four ternary frame coordinates
  ten OAM spread-line modes
  four time/frequency slots
  one encode/check sector

LIVE OPERATIONS
  affine translations
  D4 route holonomy and pilot syndromes
  anti-symplectic K
  isodual quarter-turn D
  optional locality-certified symplectic transvection
  nine-gate M36 branch

DIAGNOSTICS
  component-resolved calibration counters
  23-triangle minimum single-fault schedule
  29-triangle verified two-fault schedule
  full D4 syndrome only when escalation is required

BOUNDARY OPERATIONS
  reversible 199-gate binary ranking for archive/export/reset
  eventual erasure only after all correctable redundancy is uncomputed
```

This is the current Pareto optimum supported by the exact repository model. No claim is made that it is globally optimal over every physically realizable photonic platform; laboratory data can move the engineering Pareto frontier.
