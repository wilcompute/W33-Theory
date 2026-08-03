# Passes 2946–2952 — exact observer optimum, compiled M36, hybrid OAM, reversible telemetry, and two outside-box closures

## Evidence ladder

- **Exact:** finite-field enumeration, orbit-reduced MILP, symbolic packet obstruction, Clifford/Pauli simulation, code/coset census, reversible permutations, and W33 spread routing.
- **Modelled:** the M36 circuit law assumes stochastic Pauli faults and classical measurement flips.
- **Source-complete:** branch microcode, OAM-router generator, reversible transcript RTL generator, quarter-turn RTL, and joint-rank RTL.
- **Pending observed evidence:** Icarus, Yosys/nextpnr, canonical three-PDF compilation, optical loss/crosstalk, and laboratory detector data.

## Pass 2946 — the global affine-support optimum is exactly fifteen

The full observable family is

\[
 f_{a,b}(x)=\mathbf 1[a\cdot x+b\ne0],
 \qquad x\in\mathbf F_3^4,
\]

with 120 nonconstant observables modulo simultaneous sign.

### Local theorem

On every affine three-flat `AG(3,3)`, length eleven is infeasible at binary distance four. Every length-twelve optimum consists of exactly four complete projective-direction triplets. Both the minimum and maximum possible number of complete triplets close at four.

### Global lower bound

A selected global direction becomes constant on its parallel affine three-flats. The local minimum therefore gives direction multiplicity at most one at length thirteen and at most two at length fourteen.

- **Length 13:** affine transitivity fixes two nonparallel probes. The remaining exact MILP is infeasible.
- **Length 14, all directions distinct:** the stabilizer of two fixed nonparallel probes has three orbits on the third probe—zero offset in their span, nonzero offset in their span, and outside their span. All three exact MILPs are infeasible.
- **Length 14, one doubled direction:** restriction to each parallel three-flat leaves a length-twelve local optimum and hence four complete quotient triplets. A packet has offsets `b_i+c_i s`. Requiring those offsets to equal all of `F_3` for every slice `s` forces

\[
 \sum_i c_i=0,
 \qquad
 \sum_i c_i^2=0.
\]

Over `F_3`, this implies `c_1=c_2=c_3`, which uses one global direction three times and contradicts the multiplicity cap two.

Thus `n >= 15`.

### Matching construction

Take the ternary single-parity-check code

\[
 [5,4,2]_3:
 (x_1,x_2,x_3,x_4,x_1+x_2+x_3+x_4),
\]

and encode each trit by all three affine support offsets. Distinct trits differ in two binary positions, so ternary distance two becomes binary distance four. The resulting fifteen probes have pair-distance histogram

```text
4: 810, 6: 810, 8: 1215, 10: 405.
```

Therefore

\[
 \boxed{n_{\mathrm{affine\ support},d=4}=15.}
\]

## Pass 2947 — the deep-M36 branch is now a circuit

The decoder maps the ordered commuting operators

\[
 IYZY\mapsto -Z_0,
 \qquad
 YZXY\mapsto -Z_1.
\]

Consequently syndrome `(-1,+1)` becomes the ordinary decoded-bit acceptance test `01`. The abstract decoder uses six CNOTs, two Hadamards, and two SWAPs. Decomposing each SWAP into three CNOTs and adding the logical Hadamard gives

```text
12 CNOT + 3 H = 15 primitive Clifford gates,
followed by two direct Z measurements.
```

On two copies of deep M36 ray 5, acceptance probability is exactly `1/2`; after `H` on decoded qubit 3, the output is exactly ray 7.

### Circuit-specific first-order law

The exact census contains 191 fault events:

- `X/Y/Z` after each one-qubit gate;
- every one of the fifteen nonidentity two-qubit Paulis after each CNOT;
- one classical outcome flip at each measurement.

For independent total fault probabilities `q1`, `q2`, and `qm` per one-qubit, two-qubit, and measurement location, respectively,

\[
 p_{\rm out}
 =\frac23 p
 +\frac{140}{81}q_1
 +\frac{2084}{405}q_2
 +\frac49q_m
 +O(p^2,pq,q^2).
\]

This is exact for the stated circuit and stochastic model. It is not a coherent-error, leakage, or hardware threshold.

## Pass 2948 — the hybrid OAM fabric is a 10 by 4 spread chart

An exact spread partitions the forty W33 points into ten disjoint isotropic lines. Assign:

- one OAM mode to each spread line;
- one of four time- or frequency-bin slots to each point on that line.

Then the complete address is `(oam_line, slot)` with `10*4=40` values.

The 240 graph edges decompose exactly as

\[
 10\binom42+\binom{10}{2}4=60+180=240.
\]

Every point has three same-line neighbours and exactly one neighbour on each of the other nine OAM lines. Each ordered pair of lines is therefore one exact four-channel permutation.

### Quantized routing curvature

For every triangle of spread lines, compose its three inter-line matchings. Across all `C(10,3)=120` triangles:

```text
60 holonomies are transpositions, cycle type (2,1,1),
60 holonomies are double transpositions, cycle type (2,2).
```

No identity, 3-cycle, or 4-cycle occurs. Every triangular routing holonomy is an involution. This is an exact finite routing invariant, not a physical Berry-phase measurement.

The architecture is compatible with published path/OAM quantum interfaces and general quantum sorters, while its insertion loss and crosstalk remain open hardware quantities.

## Pass 2949 — reversible observer transcript compression

The canonical eight-tap observer gives 81 distinct bytes. Map each valid byte to the frame rank

\[
 r=27x_p+9z_p+3x_f+z_f\in\{0,\ldots,80\}.
\]

Map the remaining 175 invalid bytes bijectively to outputs `81..255`. This extends the valid map to a full 256-state permutation with an exact inverse. All valid outputs have their high bit known zero, so the retained rank needs seven fixed bits without logically erasing the observer byte.

The eight marginal bit entropies sum to

\[
 7.3463666724\text{ bits},
\]

while their joint entropy is

\[
 \log_2 81=6.3398500029\text{ bits}.
\]

The reversible permutation exposes `1.0065166696` bits of correlation before fixed-width packing. Eventually resetting the rank record still carries the `log2(81)` Landauer floor. The permutation does not make the information disappear.

## Pass 2950 — the outer ternary code is classified

For the isodual code from Pass 2938:

\[
 C=[8,4,4]_3,
\]

with ordinary weight enumerator

\[
 1+22z^4+24z^5+20z^6+8z^7+6z^8.
\]

The exact projective hyperplane spectrum is

\[
 (a_0,a_1,a_2,a_3,a_4)=(3,4,10,12,11),
\]

which is the first of the three published spectrum types for ternary `[8,4,4]_3` codes.

Additional exact invariants:

- covering radius `2`;
- hull dimension `0`, hence the code is LCD;
- coset leader distances `{0:1, 1:16, 2:64}`;
- nine distinct coset weight-enumerator types;
- external distance `5`, so it is not uniformly packed in the wide sense;
- eleven weight-four supports, with point degrees `5` or `6`, so those supports are not a 1-design.

The spectrum type is literature-grounded. No uniqueness claim inside that type is made without an explicit classification theorem.

## Pass 2951 — outside-box: encode/check duality is an order-four mode quarter-turn

The explicit signed coordinate permutation taking `C` to `C^perp` satisfies

\[
 \boxed{D^2=-I,\qquad D^4=I.}
\]

Its coordinate cycles are

```text
(0 1), (2 3), (4 6), (5 7).
```

Thus the eight ternary coordinates can be laid out as four OAM lanes with two time/frequency bins each. One application swaps the bins with calibrated ternary signs, exchanging generator and parity-check roles. Two applications give global ternary inversion. Over the real lift, the eigenvalues are four `+i` and four `-i`.

This is an exact reciprocal wiring equivalence. Optical coherence and phase stability remain experimental requirements.

## Pass 2952 — outside-box: fuse routing and observation before erasure

After distance-four correction, reversibly uncompute the fifteen support probes to the seven-bit frame rank. The hybrid address has forty valid values. Their joint state space has

\[
 81\cdot40=3240
\]

states and rank

\[
 R=40(27x_p+9z_p+3x_f+z_f)+(4\ell+s).
\]

Because

\[
 2^{11}<3240\le2^{12},
\]

the joint state fits in twelve fixed bits. Extending the valid map to the unused states gives an exact 8192-state reversible permutation from the raw `7+6`-bit register.

For the protected physical path:

```text
15 corrected support bits + 6 route bits = 21 raw bits
                                      -> 12 joint rank bits.
```

The fixed-width saving is nine bits. The irreducible entropy is

\[
 \log_2(3240)=11.6617780978\text{ bits}.
\]

If a corrected block has total probability `p` of exactly one support-bit error, the error-location record has minimum entropy

\[
 h_2(p)+p\log_2 15.
\]

Only that sparse record and the final joint rank need eventually be reset; the protection redundancy can be reversibly uncomputed.

## Primary literature boundaries

- Finite-time Landauer bounds add positive protocol-dependent cost above the quasistatic floor, and quantum coherence can add further dissipation: Vu and Saito, *Physical Review Letters* 128, 010602 (2022); Lee et al., *Physical Review Letters* 129, 120603 (2022).
- Reversible compression is directly connected to erasure free energy: Baumeler and Wolf, *Physical Review E* 100, 052115 (2019).
- Path-to-OAM quantum interfaces and general degree-of-freedom sorters support the proposed carrier architecture, but do not certify this W33 device: Fickler et al., *Nature Communications* 5, 4502 (2014); Ionicioiu, *Scientific Reports* 6, 25356 (2016).
- Published ternary-code spectra list three `[8,4,4]_3` spectrum types; the present code realizes `(3,4,10,12,11)`: *Nonexistence of some ternary linear codes*, Discrete Mathematics (2022).

## Reproduction

```bash
python analysis/bt2946_affine_support_optimum.py --case local
python analysis/bt2946_affine_support_optimum.py --case n13
python analysis/bt2946_affine_support_optimum.py --case n14_span_zero
python analysis/bt2946_affine_support_optimum.py --case n14_span_nonzero
python analysis/bt2946_affine_support_optimum.py --case n14_outside_span
python analysis/bt2946_affine_support_optimum.py --case double
python analysis/bt2946_affine_support_optimum.py --case witness
python analysis/bt2946_affine_support_optimum.py --case summary
python analysis/bt2947_m36_compiled_branch.py
python analysis/bt2948_oam_spread_fabric.py
python tools/gen_bt2948_oam_router_rtl.py
python analysis/bt2949_reversible_transcript_codec.py
python analysis/bt2950_ternary_844_classification.py
python analysis/bt2951_isodual_oam_quarter_turn.py
python analysis/bt2952_router_observer_fusion.py
pytest -q tests/test_bt2946_bt2952_seven_front_closure.py
```
