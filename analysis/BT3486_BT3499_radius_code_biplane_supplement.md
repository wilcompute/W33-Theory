# Passes 3486–3499 — radius, amplitude, modular, five-channel, code, biplane, and pointed-Clebsch closure

## Status

The verifier reports

\[
\boxed{\texttt{PASS\_9\_FRONTS}}
\]

with semantic SHA-256

```text
029228ef6f414a6fed7ec3afa6078e566cb3d780b9712b062f1f8a3ebdec06a7
```

The live chromatic boundary remains

\[
\boxed{10\leq\chi(H)\leq11}.
\]

All finite-field ranks, code minima, group actions, Smith invariants, circuit identities, and polynomial certificates below are exact. The finite magnetic-grid ranking is numerical with a large margin; its winning matrix is separately exactified.

---

## 3486 — the minimum-defect radius upper bound drops to 435

The scalar flat space is represented by two coordinates on each of the 240 filled triangles. The scalar coboundary rank is 44, so

\[
\dim H^1=480-44=436.
\]

The 720 projective minimum-support defects span this quotient. A deterministic 1,200-step basis-exchange walk produces a basis together with one extra generator whose fundamental circuit has

\[
\boxed{247}
\]

members: the extra generator plus 246 nonzero basis coordinates.

For a worst-case target having all 436 basis coefficients nonzero in \(\mathbb F_3^5\), the 246 preferred circuit shifts take values among only

\[
3^5-1=242
\]

nonzero coefficient vectors. Hence one nonzero shift cancels at least

\[
\left\lceil\frac{246}{242}\right\rceil=2
\]

basis coordinates while adding one extra defect. Therefore

\[
436-2+1=435,
\]

and the exact interval improves to

\[
\boxed{389\leq D_{H^1}\leq435}.
\]

The 247 support indices and coefficients are frozen in the compressed JSON certificate. The exact radius remains open.

---

## 3487–3488 — first amplitude-bearing five-channel magnetic screen

Fix one filled triangle and distinguish five edge channels:

1. the two phased minimum-defect edges;
2. the omitted triangle edge;
3. the 30 external edges incident with the hinge vertex;
4. the 60 external edges incident with the two endpoint vertices;
5. the remaining 627 edges.

The fifth channel is normalized to one. The verifier exhausts 63,869 denominator-32 amplitude tuples in the stated box. The best tuple is

\[
\boxed{\left(-\frac{21}{32},\frac{43}{32},-\frac{27}{32},-\frac{15}{16},1\right)}
\]

with numerical extremal eigenvalues

\[
\lambda_{\min}\approx-4,
\qquad
\lambda_{\max}\approx31.6098420946,
\]

and ratio

\[
\boxed{8.9024605237<9}.
\]

The winner is exactified by scaling by 32. Its characteristic polynomial has repeated factors

\[
(x+128)^{17}(x-64)^{21}
\]

and residual factor

\[
(x^2+75x-6724)
\]

\[
\times\left(x^5-907x^4-117516x^3+11132294x^2+851966752x-42097821696\right).
\]

Rational root isolation places all seven residual roots strictly between \(-128\) and \(1024\). Thus the unscaled winner has

\[
\lambda_{\min}=-4,
\qquad
\lambda_{\max}<32,
\]

which proves its ratio is strictly below nine.

This closes only the finite dyadic box. It does not optimize the unrestricted real amplitude cone.

---

## 3489 — characteristic-three edge-module filtration

Let \(E\cong\mathbb F_3^{720}\) be the edge permutation module. The 240 oriented face boundaries are disjoint and satisfy

\[
FF^T=0\pmod3,
\]

because every face vector has squared norm three. Consequently the face space is a 240-dimensional totally isotropic subspace of the flat space:

\[
R_{240}\subset Z^1_{480}.
\]

The point coboundary space has dimension 44, lies in \(Z^1\), and intersects the face radical trivially:

\[
B^1_{44}\cap R_{240}=0.
\]

The exact filtration is therefore

\[
0<R_{240}<Z^1_{480}<E_{720},
\]

with

\[
\dim H^1=480-44=436
\]

and the new residual quotient

\[
\boxed{\dim Z^1/(R+B^1)=480-240-44=196}.
\]

No modular irreducible name is assigned to the 196-dimensional quotient without a composition-series computation.

---

## 3490 — executable five-channel ternary-torus engine

The 135-state quotient is decomposed, after symmetric/antisymmetric splitting, as

\[
\boxed{135=27\times5}.
\]

The 27 positions are frequencies in \(\mathbb F_3^3\). Four channels come from the barycentric fibre and one is the hidden antisymmetric channel.

For

\[
c(k)=\begin{cases}2,&k=0,\\-1,&k=1,2,\end{cases}
\]

the four-channel symbol is

\[
c(k_1)K_x+c(k_2)K_y+c(k_3)I_4,
\]

where

\[
K_x=
\begin{pmatrix}
0&2&0&0\\1&1&0&0\\0&0&0&2\\0&0&1&1
\end{pmatrix},
\qquad
K_y=
\begin{pmatrix}
0&0&2&0\\0&0&0&2\\1&0&1&0\\0&1&0&1
\end{pmatrix}.
\]

The fifth symbol is

\[
-c(k_1)-c(k_2)+c(k_3).
\]

All

\[
27\cdot5\cdot5=675
\]

matrix entries are exhausted. The blocks reproduce exactly

\[
10^1,\ 7^6,\ 4^{22},\ 1^{44},\ (-2)^{42},\ (-5)^{20}.
\]

`rtl/w33_five_channel_torus_engine.v` implements the exact symbol-entry contract.

---

## 3491 — the exact five-to-four-to-three geometry chain

The Clebsch/\(D_5\) description begins with five coordinate directions. Choosing one hinge leaves four directions with stabilizer

\[
S_4.
\]

These four directions are identified with the four points of the \(PG(2,3)\) null conic. Their three perfect matchings are

\[
01|23,\qquad02|13,\qquad03|12.
\]

The induced action is

\[
\boxed{S_4/V_4\cong S_3}.
\]

The three matchings simultaneously model:

- the three projective directions of the six \(A_2(\mathbb F_3)\) roots;
- the three Fano/tomotope diagonal gauges `far`, `middle`, and `active`.

Thus the exact objectwise chain is

\[
\boxed{5\xrightarrow{\text{choose hinge}}4\xrightarrow{\text{pair}}3}.
\]

The colored controller stabilizer is \(C_2^3\). Since \(S_4\) contains no elementary abelian subgroup of order eight, a conic action necessarily forgets at least one binary controller direction. This is a useful obstruction, not a physical \(D_5\) or \(\mathrm{Spin}(10)\) claim.

---

## 3492 — minimum equivariant completion of the linear controller code

The existing systematic code is

\[
[13,5,5].
\]

Its 13 parity-column functionals are not invariant under the controller \(S_3\) action. The nonzero dual functionals split into nine controller orbits. Any coordinate-permutation-equivariant completion must use constant multiplicity on each orbit and must dominate the original multiplicities.

Taking the componentwise maximum gives a unique minimum multiset length:

\[
\boxed{28}.
\]

The completed code has parameters

\[
\boxed{[28,5,11]}
\]

and nonzero weight enumerator

\[
3z^{11}+z^{13}+12z^{14}+9z^{15}+3z^{16}+3z^{17}.
\]

Therefore exactly

\[
\boxed{15}
\]

additional coordinates are necessary and sufficient to make this fixed linear encoder coordinate-permutation equivariant. This does not prove global optimality among all possible equivariant codes.

---

## 3493 BONKERS — the Clebsch biplane is a fault locator and a modular involution

Let

\[
B=A_{\rm Clebsch}+I.
\]

The closed neighborhoods form a symmetric \(2-(16,6,2)\) biplane and

\[
BB^T=4I+2J.
\]

The exact arithmetic is

\[
\det B=-196608=-6\cdot2^{15},
\]

with Smith invariants

\[
\boxed{1^6,\ 2^4,\ 4^5,\ 12^1}.
\]

Hence

\[
\operatorname{rank}_{\mathbb F_2}B=6,
\qquad
\operatorname{rank}_{\mathbb F_3}B=15,
\]

while the ranks over \(\mathbb F_5\) and \(\mathbb F_7\) are 16.

The zero syndrome and 16 single-point-error syndromes form a binary code of minimum distance six. Thus the readout can correct two syndrome-bit errors, or any mixed pattern satisfying

\[
2e+s<6.
\]

The 120 double-point faults collapse to only 30 syndromes, so arbitrary two-point location is impossible from this readout alone.

The binary kernel has weight enumerator

\[
60z^4+256z^6+390z^8+256z^{10}+60z^{12}+z^{16}.
\]

Over \(\mathbb F_3\), symmetry gives the stronger identity

\[
\boxed{B^2=I-J}.
\]

The uniform line is the one-dimensional kernel, and \(B\) is an involution on the 15-dimensional augmentation subspace.

---

## 3494 — pointed colored-Clebsch coherent algebra

The valid/guard coloring has stabilizer

\[
C_2^3
\]

of order eight. Its ordered-pair coherent configuration has rank

\[
\boxed{60}.
\]

Pointing one valid-valid axis reduces the stabilizer to order two and refines the ordered-pair rank to

\[
\boxed{160}.
\]

The 40 Clebsch edges split into 11 colored edge orbits. The regular weighted subspace has dimension six.

Every nonzero integer coefficient vector in \([-2,2]^6\) was screened. Among the 15,624 admissible regular combinations, the best exact spectrum is

\[
(-6)^5,\quad2^{10},\quad10^1,
\]

with ratio

\[
\boxed{\frac83}.
\]

Thus this natural pointed \(D_5\)/Clebsch algebra is highly resolving but its primitive small-integer chromatic dual is much weaker than the live lower bound ten. The unrestricted real cone remains open.

---

## 3495 — checkpoint, spare, migration, work, and dilation frontier

The previously certified static and dynamic routers combine into the exact Pareto table:

| checkpoint bits | physical slots | spares | worst migrations | work | dilation | contract |
|---:|---:|---:|---:|---:|---:|---|
| 0 | 32 | 16 | 0 | 34 | 2 | static mirrored availability |
| 4 | 22 | 6 | 6 | 34 | 2 | protected state, exact recompilation |
| 4 | 19 | 3 | 1 | 38 | 3 | one-move degraded routing |
| 4 | 18 | 2 | 1 | 42 | 3 | one-move degraded routing |
| 4 | 17 | 1 | 1 | 46 | 4 | one-move degraded routing |

All 6,884 fixed spare banks of size at most five fail the exact-schedule contract. Exactly 96 six-spare banks succeed. Therefore no exact 21-slot implementation exists in this model.

The four checkpoint bits must retain or reconstruct the current logical state. Without them, remapping cannot recover destroyed uncheckpointed information.

---

## External research boundaries

The Perkel graph literature identifies its 57 vertices with one conjugacy class of \(A_5\) subgroups in \(PSL(2,19)\). The active parallel packet correctly treats its rank-20 similarity to the cover-signature projector as a comparison target, not an identification. The biplane literature independently connects \((16,6,2)\) designs to binary codes and classifies three such designs. These sources motivated arithmetic tests; no external identification was assumed without an objectwise verifier.

## Reproduction

```bash
python bootstrap/pass3486_3499/materialize.py
python analysis/bt3486_3499_radius_code_biplane_supplement.py
pytest -q tests/test_bt3486_3499_radius_code_biplane_supplement.py
iverilog -g2012 -s tb_w33_pass3486_3499 \
  -o /tmp/pass3486_3499 \
  rtl/w33_five_channel_torus_engine.v \
  rtl/w33_equivariant_linear28_encode.v \
  rtl/w33_clebsch_biplane_locator.v \
  rtl/tb_w33_pass3486_3499.v
vvp /tmp/pass3486_3499
```
