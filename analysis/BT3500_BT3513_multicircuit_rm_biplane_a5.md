# Passes 3500–3513 — multi-circuit, Reed–Muller, compound-biplane, and A5 closure

## Status

The verifier reports:

```text
PASS_7_FRONTS 5a2a10073fa2cc46a4d03e429ca4dff62e84b718f318ed30211749e6c45ddbeb
```

The live boundaries remain

\[
389\le D_{H^1}\le435,
\qquad
10\le\chi(H)\le11.
\]

All circuit relations, code minima, fault-location statements, group constructions, characters, and polynomial bounds below are exact. The continuous amplitude candidate is numerical; its nearby rational witness is independently exactified.

## 3500 — heavier circuit and the one-circuit ceiling

A deterministic 60,000-step basis-exchange walk finds a 260-term fundamental circuit. Its frozen ternary relation has SHA-256

```text
794148d204b3537e6e845c3a3ca88c5e7006dda86f4b2ef0862a671eaae90f1c
```

A rank-436 fundamental circuit has at most 436 basis coordinates. Because the nonzero coefficient alphabet has only `3^5-1=242` values, a one-circuit pigeonhole argument can guarantee at most two cancellations while adding one support. Therefore

\[
436-2+1=435,
\]

and no single-circuit proof can establish an upper bound of 434. A higher-dimensional interacting relation space is required.

For the basis carrying the 260-term circuit, all `C(284,2)=40,186` pairs of nonbasis columns were exhausted. Their rows lie in the four directions of `PG(1,3)`, but no pair uses all four. Maximum union support is 330, with one profile `(114,98,0,118)` and 106 zero rows. This is a basis-specific pilot, not a global two-circuit no-go.

## 3501–3502 — amplitude cone

The five exact edge channels have sizes

\[
2,1,30,60,627.
\]

A fixed-seed five-chart continuous search gives the numerical candidate

\[
(0.4753466204,1.3524592362,0.8588093318,-0.9394201262,1)
\]

with ratio approximately

\[
8.9062301931<9.
\]

The nearby exact tuple

\[
\frac1{256}(122,346,220,-240,256)
\]

has ratio approximately `8.9051779121`. After scaling by 256, the repeated eigenvalues are `-1024` with multiplicity 17 and `512` with multiplicity 21. The residual characteristic factor is

\[
(x^2+602x-429824)
\]

\[
\times(x^5-7258x^4-7532840x^3+5728191424x^2+3489056718848x-1419725213007872).
\]

Rational root isolation proves that all seven residual roots lie strictly in `(-1024,8192)` and that the largest one gives ratio greater than 8.905. Thus the witness satisfies exactly

\[
8.905<h<9.
\]

The unrestricted real-cone optimum remains open.

## 3503–3505 — global binary S3-equivariant code frontier

The 31 nonzero dual functionals split into nine controller orbits of sizes

\[
3,3,1,3,6,3,6,3,3.
\]

All 505,230 orbit-multiplicity vectors of total length at most 40 were exhausted. The minimum lengths for target distances 1 through 20 are

```text
6,6,9,10,13,14,15,16,21,21,24,24,27,28,30,31,36,37,39,40
```

In particular:

| target distance | minimum code |
|---:|---:|
| 5 | [13,5,5] |
| 8 | [16,5,8] |
| 11 | [24,5,11] |
| 14 | [28,5,14] |

This corrects the scope of the previous `[28,5,11]` result: length 28 was minimal only for completing one fixed embedded encoder. Globally, an equivariant `[13,5,5]` already exists, distance eleven needs only length 24, and length 28 reaches distance fourteen.

## 3506 BONKERS — Q4 carries RM(1,4) objectwise

The optimal distance-eight code uses exactly the sixteen columns

\[
\{c\in\mathbb F_2^5:\langle00111,c\rangle=1\}.
\]

This is a four-dimensional affine hyperplane and gives weight enumerator

\[
1+30z^8+z^{16}.
\]

Therefore the code is objectwise

\[
RM(1,4)=[16,5,8].
\]

The sixteen coordinates are the Q4/toroidal-knight controller positions, while the five message bits are one constant and four affine-coordinate coefficients. `rtl/w33_rm14_equivariant_encode.v` implements the exact encoder.

## 3507–3508 — minimum compound double-fault locator

The Clebsch biplane maps 120 double-point faults to thirty base syndromes, each with a collision class of size four. Assigning an `r`-bit point label and augmenting a pair syndrome by the XOR of its two labels gives the exact CSP:

| extra bits | result | nodes |
|---:|---:|---:|
| 1 | UNSAT | 47 |
| 2 | UNSAT | 7,890 |
| 3 | SAT | 22 |

Thus three extra bits are necessary and sufficient. One canonical point-label table is

```text
0,0,0,0,0,1,2,3,0,2,3,4,5,6,1,7
```

The resulting nineteen-bit readout uniquely identifies all

\[
1+16+\binom{16}{2}=137
\]

fault patterns of weight at most two.

The three label bits are cubic functions of the four-bit Clebsch-axis coordinate, with ANF monomial masks

```text
L0: 5,10,11,12,14
L1: 6,9,10
L2: 11,12,14
```

This is a second independently derived degree-three map on the Q4 controller substrate. `rtl/w33_clebsch_double_fault_locator3.v` publishes the exact table.

## 3509–3511 — A5 character firewall

The Perkel graph is reconstructed from the 57 conjugates of an A5 subgroup in `PSL(2,19)`, adjacent when their subgroup intersection has order ten. The graph has 57 vertices, 171 edges, degree six, and spectrum

\[
6^1,((3+\sqrt5)/2)^{18},((3-\sqrt5)/2)^{18},(-3)^{20}.
\]

The root A5 has vertex orbits `1,6,20,30`. The character of the Perkel rank-twenty `-3` sector on element orders `1,2,3,5` is

\[
(20,0,2,0),
\]

with decomposition

\[
1\oplus3\oplus3'\oplus2\cdot4\oplus5.
\]

For an explicit A5 subgroup in the live PSp(4,3) action, the W33 block rank-twenty `-4` sector has character

\[
(20,4,5,0),
\]

with decomposition

\[
3\cdot1\oplus3\cdot4\oplus5.
\]

The modules are therefore not A5-isomorphic, and no A5-equivariant rank-twenty intertwiner exists. The firewall is sharp: the Perkel sector contains both three-dimensional A5 irreducibles, while the W33 sector contains neither.

## Reproduction

```bash
python bootstrap/pass3500_3513/materialize.py
python analysis/bt3500_3513_multicircuit_rm_biplane_a5.py
pytest -q tests/test_bt3500_3513_multicircuit_rm_biplane_a5.py
iverilog -g2012 -s tb_w33_pass3500_3513 -o /tmp/pass3500 \
  rtl/w33_rm14_equivariant_encode.v \
  rtl/w33_clebsch_double_fault_locator3.v \
  rtl/tb_w33_pass3500_3513.v
vvp /tmp/pass3500
```

## Boundaries

No exact covering-radius endpoint, ten-colour closure, unrestricted amplitude optimum, non-equivariant Perkel/W33 identification, observed FPGA result, fresh PDF result, laboratory result, or physical particle/spacetime identification is asserted.
