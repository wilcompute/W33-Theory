# Passes 3506–3519 — Cubic dependency projector, minimal ternary datapath, and incidence boundaries

## Status

The executable verifier reports

```text
PASS_7_FRONTS 7ad66eec9cbb1b3f207eb4215a348cb9a63e0be9ab7876e53209dbed3099a13f
```

The packet executes the five live continuations from Passes 3458–3505 and two additional high-risk constructions.  It preserves the live boundaries

\[
\boxed{389\le R_{\rm defect}\le435},
\qquad
\boxed{10\le\chi(H)\le11}.
\]

The new result is not another parameter coincidence.  The first 5,040 failures of strength three form a canonical cubic dependency hypergraph on the 240 filled faces, and its characteristic-three overlap operator constructs the protected 81-dimensional summand by an explicit polynomial idempotent.

---

## 3506–3507 — the first code-sensitive covering deck

Each of the 720 support edges belongs to exactly one filled face.  A non-filled triangle of the 45-point block graph therefore determines three filled faces: the unique filled face containing each of its three edges.

There are exactly

\[
\boxed{5040=2160+2880}
\]

such non-filled triangles, and all 5,040 induced triples of filled faces are distinct.  Let

\[
T\in\{0,1\}^{240\times5040}
\]

be their face–dependency incidence matrix.

The resulting 3-uniform hypergraph is regular:

\[
\boxed{\deg(f)=63\qquad\text{for every filled face }f.}
\]

Two filled faces occur together in either two or four dependency triples.  The complete codegree census is

\[
\boxed{2^{3240},\qquad4^{2160}},
\]

so exactly 5,400 of the \(\binom{240}{2}\) face pairs are supported.

Define the weighted two-section operator

\[
D=TT^{\mathsf T}-63I_{240}.
\]

It is 126-regular.  Its spectrum is

\[
\boxed{
126^1,
\left(18+12\sqrt6\right)^{24},
18^{20},
6^{15},
(-6)^{60},
(-10)^{81},
\left(18-12\sqrt6\right)^{24},
(-18)^{15}.
}
\]

The multiplicity list is

\[
\boxed{1,15,15,20,24,24,60,81},
\]

exactly the ordinary constituent fingerprint of the 240-state face module.  Thus one canonical cubic-dependency operator separates all eight characteristic-zero face constituents, including the two 15-dimensional and two 24-dimensional sectors that dimension counting alone cannot distinguish.

A rational annihilator is

\[
\begin{aligned}
p(x)={}&(x-126)(x-18)(x-6)(x+6)(x+10)(x+18)\\
&\times(x^2-36x-540).
\end{aligned}
\]

The verifier checks the spectral multiplicities and verifies \(p(D)=0\) modulo independent primes 101 and 103.

### Covering consequence

The incidence ranks are

\[
\boxed{
\operatorname{rank}_{\mathbb F_2}T=240,
\quad
\operatorname{rank}_{\mathbb F_3}T=239,
\quad
\operatorname{rank}_{\mathbb F_5}T=240.
}
\]

Characteristic three is therefore exceptional.  The only row dependence is the global one forced by every column having weight three.

This is the first exact higher-order deck that can see the switching code beyond one- and two-coordinate marginals.  It supplies the correct input for a code-sensitive degree-three or Lasserre relaxation.  It does not, by itself, prove \(R\ge390\), so the live interval remains \([389,435]\).

---

## 3508 — characteristic-three projector theorem

Reduce \(D\) modulo three.  The verifier proves the exact polynomial relation

\[
\boxed{D^4=-D^3\pmod3.}
\]

Hence

\[
\boxed{E_{81}:=-D^3}
\]

satisfies

\[
\boxed{E_{81}^2=E_{81}},
\qquad
\boxed{\operatorname{rank}_{\mathbb F_3}E_{81}=81}.
\]

Moreover,

\[
DE_{81}=-E_{81}.
\]

The minimal polynomial of the dependency operator is

\[
\boxed{x^3(x+1)}.
\]

The complementary 159-dimensional generalized-zero space has power ranks

\[
\boxed{44,14,0},
\]

and therefore nilpotent Jordan type

\[
\boxed{
J_3(0)^{14}\oplus J_2(0)^{16}\oplus J_1(0)^{85}.
}
\]

The canonical face antipode provides a second check.  The projector annihilates the full 120-dimensional antipodal-symmetric space and has rank 81 on the antipodal-antisymmetric space:

\[
\boxed{
\operatorname{rank}(E_{81}V_+)=0,
\qquad
\operatorname{rank}(E_{81}V_-)=81.
}
\]

This identifies the previously observed 81-dimensional modular brick by an explicit polynomial projector.  It proves that the brick is a direct summand.  It is still not labelled simple without an independent composition-series or MeatAxe calculation.

---

## 3509–3510 — transported full-\(M_4\) finite-grid screen

The six filled faces over each W33 quotient point are identified with the six transpositions of a tetrahedron.  A deterministic gauge is fixed by choosing the lexicographically least face-group lift from the base fibre to each quotient point.

Each block-graph edge inherits the transposition attached to its unique filled face.  The resulting 180-dimensional Hermitian carrier uses six scalar weights, one per local transposition.

The verifier exhausts

\[
\frac{3^6-1}{2}=\boxed{364}
\]

nonzero projective weight vectors in

\[
\{-1,0,1\}^6/\{\pm1\}.
\]

The best member is the equal-weight vector

\[
(1,1,1,1,1,1),
\]

with

\[
\lambda_{\max}=32,
\qquad
\lambda_{\min}\approx-14.060915270409,
\]

and weighted Hoffman ratio

\[
\boxed{3.275812021095}.
\]

Thus every matrix in this deterministic ternary six-weight grid stays below four and cannot alter the live chromatic lower bound ten.

This closes only the stated finite grid.  It is not an unrestricted optimization over edge-dependent elements of the full \(M_4\) algebra.

---

## 3511–3513 — exact five-operation ternary datapath

Modulo three, all 27 five-channel momentum symbols collapse to

\[
J=
\begin{pmatrix}
2&1&1&0&0\\
2&1&0&1&0\\
2&0&1&1&0\\
0&2&2&0&0\\
0&0&0&0&1
\end{pmatrix},
\qquad
J^3=I.
\]

The cost model counts a binary ternary addition or subtraction as one operation; sign changes and copies are wiring.

An exhaustive breadth-first search through depth four has state counts

\[
\boxed{1,20,310,4560,67245}
\]

and finds no circuit containing all five target output forms.  Therefore four operations are impossible.

Five operations attain the target:

\[
s=b+c,
\qquad
p=d-a,
\]

\[
y_0=s-a,
\quad
y_1=p+b,
\quad y_2=p+c,
\quad y_3=-s,
\quad y_4=e.
\]

Hence

\[
\boxed{\text{minimum binary ternary operation count}=5.}
\]

The packet includes `rtl/w33_mod3_five_channel_min5.v` and an exhaustive testbench covering all

\[
3^5=243
\]

legal input states, literal matrix equivalence, and the three-step identity.

The source theorem is exact.  Icarus and Yosys observations remain remote-workflow evidence until the workflow completes.

---

## 3514–3515 — tomotope cocycle lift obstruction

The prior oriented-tetrahedron surface has 12 coordinates and 16 triangular lines:

\[
\boxed{12_4\,16_3}.
\]

The tomotope also has 12 edges and 16 triangular faces, together with eight cells: four tetrahedra and four hemioctahedra.  Every triangular face is incident to two cells, so an incidence-preserving lift must select eight four-face cells, each using six edges twice, and cover every one of the 16 faces exactly twice.

The verifier exhausts the oriented surface.

There are exactly

\[
\boxed{12}
\]

four-face/six-edge local cell candidates, but there are

\[
\boxed{0}
\]

eight-cell double-cover solutions.

The visible \(S_4\) action together with orientation reversal has order 48, and the obstruction is invariant under this full visible symmetry.

Therefore

\[
\boxed{
\text{the oriented-tetrahedron }12_4\,16_3\text{ surface is not the tomotope edge–face incidence structure.}
}
\]

The shared Reye parameters remain useful, but the missing cell cocycle cannot be supplied by relabelling this particular surface.

This agrees with the original tomotope data: four vertices, twelve edges, sixteen triangles, four tetrahedra, four hemioctahedra, symmetry order 96, and 192 flags.  Parameter equality is not incidence equivalence.

---

# BONKERS 1 — the tempting \(57=1+16+40\) decomposition is impossible

The triangle-free/SRG atlas exposes the numerical identity

\[
57=1+16+40,
\]

suggesting an apex plus a Clebsch graph plus W33 inside a hypothetical

\[
\operatorname{SRG}(57,14,1,4).
\]

Assume the 16-set induces Clebsch, of degree five.  Its external degree sum would be

\[
16(14-5)=144.
\]

Assume the disjoint 40-set induces W33, of degree twelve.  Its external degree sum would be

\[
40(14-12)=80.
\]

The difference is

\[
144-80=64.
\]

All Clebsch–W33 cross edges are counted once from each side, so the difference would have to be supplied entirely by the single apex.  But one apex can change the two incidence sums by at most 16.

Therefore

\[
\boxed{
\operatorname{SRG}(57,14,1,4)
\text{ cannot contain induced Clebsch and W33 pieces on a }1+16+40\text{ partition.}
}
\]

This is an exact degree-sum obstruction.  It makes no assertion about other possible realizations of the already known nonexistent parameter set, and it is unrelated to existence of the degree-57 Moore graph.

---

# BONKERS 2 — W33 plus Clebsch completes the Gewirtz augmentation spectrum

W33 and the Gewirtz graph share nonprincipal eigenvalues \(2\) and \(-4\):

\[
W33:\quad 2^{24},(-4)^{15},
\]

\[
\mathrm{Gewirtz}:\quad2^{35},(-4)^{20}.
\]

The missing multiplicities are therefore

\[
11\text{ copies of }2,
\qquad5\text{ copies of }-4.
\]

The Clebsch graph has spectrum

\[
5^1,1^{10},(-3)^5.
\]

Define

\[
\boxed{p(x)=\frac{-3x^2+18x+17}{16}.}
\]

Then

\[
p(5)=p(1)=2,
\qquad
p(-3)=-4.
\]

Consequently

\[
\operatorname{spec}p(A_{\rm Clebsch})=2^{11},(-4)^5,
\]

and

\[
\boxed{
\operatorname{spec}_{\rm nonprincipal}(A_{W33}\oplus p(A_{\rm Clebsch}))
=
2^{35},(-4)^{20},
}
\]

exactly the Gewirtz augmentation spectrum.

This is a functional-calculus completion, not a graph embedding and not a canonical group-module intertwiner.  Its value is that it turns the earlier W33–Gewirtz shared polynomial and the Clebsch \(D_5\) shell into one explicit spectral construction.

---

## Publication and evidence state

Committed surfaces:

- `analysis/bt3506_3519_chained_breakthrough.py`;
- `data/PART_BT3506_BT3519_CHAINED_BREAKTHROUGH_results.json`;
- `tests/test_bt3506_3519_chained_breakthrough.py`;
- `rtl/w33_mod3_five_channel_min5.v`;
- `rtl/tb_w33_pass3506_3519_min5.v`;
- shared TeX and public-index inserts;
- a focused exact/RTL/synthesis/PDF workflow.

The frozen semantic hash is

```text
7ad66eec9cbb1b3f207eb4215a348cb9a63e0be9ab7876e53209dbed3099a13f
```

No remote Icarus, Yosys, FPGA-area, timing, power, PDF-hash, laboratory, M57, or physical result is claimed before observed workflow evidence exists.
