# Pass 10947 — cubic VM, verified Golay factories, quotient symmetry, and M36 router

Pass 10947 executes the five independent continuations left by Pass 10944.
Its producer is `analysis/w33_pass10947_five_front_execution.py` and its
frozen certificate is `data/w33_pass10947_five_front_execution.json`.
The ternary Golay code and 66-location core remain owned by
`analysis/w33_dark_strange_golay11_ft_lane.py`,
`analysis/2026-09-23_execute_all5_hybrid_lie_golay_calibration.md`, Pass 10943,
and Pass 10944; this packet cites and extends those witnesses.

## 1. The E6 cubic controlled-X now has seven-qutrit VM microcode

Use data modes 0--3 as control, copy ancilla, fixed-one ancilla, and target.
The Pass 10941 Clifford ABI gives

```text
SUM(0->1) = F(1) CZ(0,1) F(1)^-1.
```

After preparing mode 2 in `|1>`, the Pass 10944 identity becomes the exact
program

```text
copy x to mode 1;
X on target mode 3;
signed E6 cubic tick x*x*1 into mode 3;
uncompute mode 1 and restore mode 2 to |0>.
```

All nine control/target cases give `t -> t+1-x^2`, hence zero-controlled X.
The lowering uses ten primitive operations in seven parallel layers: three
Heisenberg X translations, four Fourier operations, two CZ operations, and
one native signed cubic tick. Only the existing P7 edge `(0,1)` is needed; the
data/control bridge is not. This is an exact logical ABI conditional on the
cubic-tick port, not a microscopic four-body pulse construction.

## 2. Exact encoded inputs and the first factory-plus-core threshold curve

Let `C=G11^perp` be the committed five-dimensional self-orthogonal ternary
code. The producer constructs the three disjoint size-243 cosets

```text
C, C+1, C+2,
```

whose union is `Cperp`. They give exact supports for `|0_L>`, `|+_L>`, and
the reflection resource `|R_L>` with logical-coset amplitudes `(1,1,-1)`.
All 7,290 X/Z stabilizer actions and phases are checked objectwise.

Each of the three input blocks uses two complete X/Z syndrome rounds with
verified weight-six cat gadgets and coordinate-local data coupling, accepts
only agreeing zero syndromes, and then performs an eleven-location handoff.
The ledger has 162 locations per input block, 486 across the three factories,
and 66 in the syndrome/injection core: 552 total.

Under the declared accepted-fault support model, only the second-round data
couplings, accepted handoffs, and core locations can be order-three hazards.
There are 279 such locations. All `C(279,3)=3,580,779` hazard triples are
enumerated; exactly

```text
M = 2,576,205
```

touch three distinct code coordinates and are malignant. The former symbolic
`q` is replaced by

```text
P_fail <= M p^3 (1-p)^549 + Pr[Binomial(552,p) >= 4].
```

This conservative bound crosses `P_fail=p` at
`p=0.000531703523611593`. It is a threshold for the explicit independent,
coordinate-local, postselected gadget model. Correlated faults, leakage and a
device-specific cat circuit remain outside that model. Prakash's ternary-Golay
paper owns the Strange-state distillation map (arXiv:2003.02717); Pass 10947
adds the encoded-input and extended-fault ledger.

## 3. The 36+18 quotient has an exact residual centralizer

Pass 10945 proved that the quotient is canonically `18+18+18`; the parabolic
`36+18` is the projector selecting two clock channels against the third. Each
18-dimensional channel has H27 multiplicities

```text
nine distinct linear characters, each once, plus 3 V_(omega^2).
```

Consequently

```text
dim End_H27(Q) = 9*3^2 + 9^2 = 162,
dim End_(H27 x C3)(Q) = 27 + 3*3^2 = 54.
```

On the discrete carrier, `H27 x S3` has order 162. The centralizer of the
rank-36/rank-18 projector is exactly `H27 x S2`, order 54: `S2` swaps the two
positive channels while fixing the opposite channel. These symmetries do not
change the H27 multiplicities, so the original equivariant-rank ceiling 36
survives.

## 4. The M36 interface reduces to a sparse star router

Install three programmable mode switches `(0,3)`, `(1,3)`, `(2,3)` and use
mode 3 as the dump bus. For family `f=0,1,2`, activate only `(f,3)` at MZI
mixing angle `pi/2`; family 3 is the bypass configuration. The first three
rows of the resulting four-mode permutation are exactly the required
three-by-four partial isometry:

```text
W_f W_f^dagger = I3,
W_f^dagger W_f = I4-|f><f|.
```

All 36 M36 rays pass. With three installed switches, the star uses active
counts `(1,1,1,0)`, versus `(3,2,1,0)` for an adjacent deletion chain. Its
worst count one is optimal because every non-bypass family must change the
input routed to the fixed dump.

The star therefore retains the Pass 10944 per-interface targets directly:
active-switch process fidelity at least `0.9966554934`, phase error at most
`0.057864` radians, differential loss at most `0.502881` dB, and leakage at
most `1e-3` (30 dB extinction). A three-stage baseline would need materially
tighter per-switch tolerances. The sparse construction is a specialization of
standard programmable multiport interferometry, not evidence of a fabricated
device (Clements et al., Optica 3 (2016), DOI 10.1364/OPTICA.3.001460).

## 5. The order-108 coloring symmetry has a central-phase anomaly

Let `B <= GL(2,3)` be the order-12 stabilizer of calibration family D. The
M36 coloring stabilizer is

```text
F3^2 : B, order 108.
```

The current signed E6 cubic uses the nonabelian H27 lift of the affine address
plane. Exact enumeration gives the support group

```text
H27 : B, order 324,
```

with three central support lifts above every coloring operation. Every one of
the 324 support permutations has a soluble binary diagonal-sign equation of
rank 21 and nullity six. Thus it has 64 sign repairs, and the full monomial
signed-cubic lift has order

```text
324 * 2^6 = 20,736.
```

The central extension does not split. All nine choices of central gauges for
lifts of the two affine translation generators have the same nonidentity
central commutator. Therefore the order-108 group does not act strictly on the
27 signed cubic coordinates. It acts projectively, and VM selector relabeling
must track both the central qutrit phase and a diagonal sign gauge.

## Scope

The VM word, logical code states, location ledger, quotient commutants, ideal
transfer matrices and cubic group extension are executable finite results.
The packet does not claim a microscopic cubic Hamiltonian, a correlated-noise
threshold, a fabricated router, or measured performance.
