# Passes 3514–3527 — multi-circuit radius, continuous amplitudes, equivariant codes, compound biplane location, and the A5 firewall

## Status

The exact verifier reports

```text
PASS_7_FRONTS 3cc9e9d0889148b749a51fdb0834881f2ff131c9ba25cc8b51a402de280c93b4
```

The live boundaries remain

\[
\boxed{389\le D_{H^1}\le435},
\qquad
\boxed{10\le\chi(H)\le11}.
\]

All circuit relations, finite-field searches, code minima, fault-location claims, group constructions, characters, projectors, and rational-polynomial bounds below are exact. The projective amplitude candidate is numerical; its nearby denominator-256 witness is independently exactified.

---

## 3514 — a heavier minimum-defect circuit and the exact single-circuit ceiling

A deterministic 60,000-step basis-exchange walk in the 436-dimensional scalar cohomology quotient finds a fundamental circuit of weight

\[
\boxed{260}.
\]

Its complete support and ternary coefficients are frozen, and its relation hash is

```text
794148d204b3537e6e845c3a3ca88c5e7006dda86f4b2ef0862a671eaae90f1c
```

This is heavier than the previous 247-term witness, but it exposes a decisive limitation. A rank-436 fundamental circuit has at most 437 total terms and at most 436 basis coordinates. The nonzero coefficient alphabet has size

\[
3^5-1=242.
\]

Therefore the pigeonhole argument can force at most

\[
\left\lceil\frac{436}{242}\right\rceil=2
\]

cancellations while adding one extra support. Consequently every proof using one fundamental circuit has the universal floor

\[
436-2+1=\boxed{435}.
\]

Thus:

\[
\boxed{\text{No one-circuit pigeonhole proof can establish }D_{H^1}\le434.}
\]

The next radius improvement must use several interacting circuits or a higher-dimensional relation subspace.

### Exhaustive two-column pilot

For the basis carrying the 260-term circuit, all

\[
\binom{284}{2}=\boxed{40{,}186}
\]

pairs of nonbasis columns were exhausted. Each coordinate row determines a point of

\[
PG(1,3),
\]

which has four projective directions. No pair realizes all four directions. The largest union support is 330; one representative has direction counts

\[
(114,98,0,118)
\]

and 106 zero rows.

This is a complete census for one exact basis, not a global two-circuit no-go.

---

## 3515–3516 — the real five-channel amplitude cone is numerically near 8.90623

The five exact edge channels have sizes

\[
2,\ 1,\ 30,\ 60,\ 627.
\]

A five-chart continuous numerical search gives the projective candidate

\[
(0.4753466204,\ 1.3524592362,\ 0.8588093318,\ -0.9394201262,\ 1),
\]

with

\[
\lambda_{\min}\approx-4,
\qquad
\lambda_{\max}\approx31.6249207792,
\]

and

\[
\boxed{h\approx8.9062301931<9}.
\]

This numerical candidate is not promoted as a global optimum.

### Exact rational improvement

The nearby denominator-256 tuple

\[
\boxed{\frac1{256}(122,346,220,-240,256)}
\]

has numerical ratio

\[
\boxed{8.9051779121},
\]

strictly improving the earlier denominator-32 witness.

After multiplying the matrix by 256, its characteristic polynomial contains

\[
(x+1024)^{17}(x-512)^{21}
\]

and the residual factor

\[
(x^2+602x-429824)
\]

\[
\times\left(
 x^5-7258x^4-7532840x^3+5728191424x^2
 +3489056718848x-1419725213007872
\right).
\]

Exact rational root isolation places all seven residual roots strictly in

\[
(-1024,8192).
\]

It also places the largest root above a rational value yielding ratio greater than 8.905. Hence the witness satisfies exactly

\[
\boxed{8.905<h<9}.
\]

The unrestricted real-cone optimum remains open.

---

## 3517–3519 — complete binary S3-equivariant dimension-five code frontier through length 40

The 31 nonzero binary linear functionals split under the controller \(S_3\) into nine orbits of sizes

\[
3,3,1,3,6,3,6,3,3.
\]

An equivariant coordinate multiset is therefore specified by nine nonnegative orbit multiplicities. All

\[
\boxed{505{,}230}
\]

multiplicity vectors of total length at most 40 were exhausted exactly.

The minimum length for target distance \(d=1,\ldots,20\) is

\[
6,6,9,10,13,14,15,16,21,21,24,24,27,28,30,31,36,37,39,40.
\]

Important exact points are:

| target distance | minimum length | parameters |
|---:|---:|---:|
| 5 | 13 | \([13,5,5]\) |
| 8 | 16 | \([16,5,8]\) |
| 11 | 24 | \([24,5,11]\) |
| 14 | 28 | \([28,5,14]\) |

This corrects the interpretation of the previous \([28,5,11]\) result. Length 28 was minimal only for completing one fixed embedded \([13,5,5]\) encoder. Globally:

\[
\boxed{\text{an equivariant }[13,5,5]\text{ code already exists},}
\]

and distance eleven requires only length 24.

---

## 3520 BONKERS — the Q4 controller carries RM(1,4) exactly

The optimal distance-eight code uses the sixteen dual columns

\[
\{c\in\mathbb F_2^5:\langle 00111,c\rangle=1\}.
\]

This is an affine four-dimensional hyperplane. Its code has weight enumerator

\[
\boxed{1+30z^8+z^{16}}.
\]

Thus it is objectwise the first-order Reed–Muller code

\[
\boxed{RM(1,4)=[16,5,8]}.
\]

The identification is concrete:

- the sixteen coordinates are the vertices of \(Q_4\), equivalently the \(4\times4\) toroidal-knight controller;
- the five message bits are one constant coefficient plus four affine-coordinate coefficients;
- every nonconstant affine function has weight eight;
- the constant-one word has weight sixteen.

This is not merely a matching weight enumerator: the columns are literally one affine hyperplane in \(\mathbb F_2^5\).

`rtl/w33_rm14_equivariant_encode.v` implements the exact encoder.

---

## 3521–3522 — three additional bits are necessary and sufficient to locate every double fault

The Clebsch biplane maps 120 two-point faults to only 30 base syndromes. Every collision class contains exactly four pairs.

Assign an \(r\)-bit label \(\ell_i\) to each of the sixteen Clebsch points and augment a two-point syndrome by

\[
\ell_i\oplus\ell_j.
\]

A canonical exhaustive CSP gives:

| extra bits | result | search nodes |
|---:|---:|---:|
| 1 | UNSAT | 47 |
| 2 | UNSAT | 7,890 |
| 3 | SAT | 22 |

Therefore

\[
\boxed{3\text{ extra bits are necessary and sufficient}.}
\]

One canonical label table is

\[
(0,0,0,0,0,1,2,3,0,2,3,4,5,6,1,7).
\]

The combined nineteen-bit readout uniquely identifies all

\[
1+16+\binom{16}{2}=\boxed{137}
\]

fault patterns of weight at most two.

### BONKERS cubic controller bridge

Treat the sixteen Clebsch axes as four-bit words. The three locator outputs have algebraic-normal-form monomial masks

\[
\begin{aligned}
L_0 &: 5,10,11,12,14,\\
L_1 &: 6,9,10,\\
L_2 &: 11,12,14.
\end{aligned}
\]

Hence the minimum locator is cubic. This gives a second, independently derived degree-three nonlinear map on the same \(Q_4\) controller substrate, alongside the earlier degree-three signature controller.

`rtl/w33_clebsch_double_fault_locator3.v` publishes the exact map.

The 19-bit locator is injective; it is not claimed to have large minimum distance against additional readout corruption.

---

## 3523–3525 — the Perkel/W33 rank-20 A5 intertwiner is impossible

The Perkel graph is reconstructed from

\[
PSL(2,19),\qquad |PSL(2,19)|=3420.
\]

Its 57 vertices are the conjugates of one \(A_5\) subgroup. Two vertices are adjacent when their subgroup intersection has order ten. This gives

\[
57\text{ vertices},\quad171\text{ edges},\quad k=6,
\]

and spectrum

\[
6^1,
\left(\frac{3+\sqrt5}{2}\right)^{18},
\left(\frac{3-\sqrt5}{2}\right)^{18},
(-3)^{20}.
\]

The root \(A_5\) has vertex orbits

\[
1,6,20,30.
\]

The character of the Perkel \(-3\) rank-20 sector on elements of orders \(1,2,3,5\) is

\[
\chi_{\rm Perkel}=(20,0,2,0).
\]

Its \(A_5\)-decomposition is

\[
\boxed{1\oplus3\oplus3'\oplus2\cdot4\oplus5}.
\]

An explicit \(A_5\le PSp(4,3)\) was then constructed in the live 45-block action. The W33 block \(-4\) rank-20 sector has character

\[
\chi_{W33}=(20,4,5,0)
\]

and decomposition

\[
\boxed{3\cdot1\oplus3\cdot4\oplus5}.
\]

Therefore:

\[
\boxed{\chi_{\rm Perkel}\ne\chi_{W33}},
\]

so the two rank-20 modules are not \(A_5\)-isomorphic and

\[
\boxed{\text{no }A_5\text{-equivariant rank-20 intertwiner exists}.}
\]

The representation-theoretic firewall is especially sharp: the Perkel sector contains both three-dimensional \(A_5\) irreducibles, while the W33 sector contains neither.

This converts the previous rank-20 resemblance from an open comparison target into an exact no-go.

---

## Reproduction

```bash
python analysis/bt3514_3527_multicircuit_rm_biplane_a5.py
pytest -q tests/test_bt3514_3527_multicircuit_rm_biplane_a5.py
iverilog -g2012 -s tb_w33_pass3514_3527 \
  -o /tmp/pass3514_3527 \
  rtl/w33_rm14_equivariant_encode.v \
  rtl/w33_clebsch_double_fault_locator3.v \
  rtl/tb_w33_pass3514_3527.v
vvp /tmp/pass3514_3527
```

## Claim boundaries

No exact covering-radius endpoint, ten-colour closure, unrestricted real-amplitude optimum, non-equivariant Perkel/W33 identification, hardware area/timing result, fresh PDF result, laboratory realization, or particle/spacetime interpretation is asserted.
