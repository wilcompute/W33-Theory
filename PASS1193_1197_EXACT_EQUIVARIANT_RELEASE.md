# Passes 1193–1197 — Exact Equivariant Release

Status: **machine-checkable release candidate**

This packet executes the five outstanding workstreams after the Passes 1188–1192 correction release was materialized and merged.

## Pass 1193 — The exact 432-carrier intersection bridge

For each of the three 432-point A2-triple orbits, the stabilizer in the outer Weyl extension is an `S5` of order 120. Reflection parity cuts it into 60 even and 60 odd elements. The even intersection is perfect, centerless, and has element-order census

\[
1^1\,2^{15}\,3^{20}\,5^{24},
\]

therefore it is `A5`. Hence

\[
\boxed{S_5\cap PSp(4,3)=A_5}
\]

and the same carrier has two exact coset descriptions:

\[
\boxed{W(E_6)/S_5\cong PSp(4,3)/A_5},
\qquad
\frac{51840}{120}=\frac{25920}{60}=432.
\]

## Pass 1194 — Explicit residual central idempotents

The 1952-dimensional residual is

\[
13(1)\oplus16(6)\oplus5(15)\oplus4(15_a)\oplus21(20)
\oplus2(24)\oplus9(30)\oplus4(60_a)\oplus10(64)\oplus90.
\]

For every residual irreducible character, the release records the rational class-sum projector

\[
e_\chi=\frac{\chi(1)}{51840}\sum_C\chi(C)K_C.
\]

The ten character rows are exactly orthonormal. The residual center has dimension 10 and the full commutant has dimension

\[
13^2+16^2+5^2+4^2+21^2+2^2+9^2+4^2+10^2+1^2
=1109.
\]

Boundary: these are canonical central/isotypic projectors. Matrix units inside multiplicity blocks require a noncanonical copy-basis choice.

## Pass 1195 — W(E6)-equivariant Hashimoto packets

The 480-dimensional directed-edge module decomposes as

\[
1+2(15_-)+15_a+20+3(24)+30_-+60_a+2(81_+)+90.
\]

The nonbacktracking operator has five exact equivariant spectral packets:

\[
\begin{array}{c|c|c}
\text{factor}&\text{dimension}&W(E_6)\text{-module}\\ \hline
x-11&1&1\\
x-1&201&30_-+81_++90\\
x+1&200&15_a+20+24+60_a+81_+\\
x^2-2x+11&48&2(24)\\
x^2+4x+11&30&2(15_-)
\end{array}
\]

Thus

\[
\boxed{\chi_B(x)=(x-11)(x-1)^{201}(x+1)^{200}
(x^2-2x+11)^{24}(x^2+4x+11)^{15}}.
\]

## Pass 1196 — Primitive reduced-cycle orbits

Literal primitive oriented cycle classes, modulo cyclic rotation, are enumerated through length six:

\[
\pi_3=320,\qquad \pi_4=3480,\qquad
\pi_5=36288,\qquad \pi_6=302880.
\]

The orbit counts are:

\[
\begin{array}{c|rrrr}
 n&3&4&5&6\\ \hline
PSp(4,3)&1&2&3&18\\
W(E_6)&1&2&2&13
\end{array}
\]

At length five, the two projective orbits of size 5184 fuse under the outer involution into one Weyl orbit of size 10368. At length six, 18 projective orbits fuse to 13 Weyl orbits.

The degree-40 continuation is exact through the five spectral packets and Möbius inversion. It is deliberately not called a literal orbit partition beyond length six.

## Pass 1197 — Collision-proof parallel publication

The namespace registry now contains 74 unique registered pass numbers through Pass 1197. The new guard fails closed unless:

- registered pass ranges are disjoint;
- modern pass-numbered files belong to a registered range;
- Passes 1193–1197 each have one passing canonical certificate;
- the prior Pass-1192 synthesis firewall remains clean;
- the new workflow and pre-commit namespace gate are installed;
- the obsolete `.correction` materializer scaffold remains absent.

## Verification entrypoints

```bash
PYTHONPATH=analysis python analysis/w33_pass1193_s5_a5_coset_bridge.py
PYTHONPATH=analysis python analysis/w33_pass1194_residual_central_idempotents.py
PYTHONPATH=analysis python analysis/w33_pass1195_we6_equivariant_hashimoto.py
PYTHONPATH=analysis python analysis/w33_pass1196_primitive_cycle_orbits.py
PYTHONPATH=. pytest -q tests/test_w33_pass1193_1197.py
PYTHONPATH=analysis python analysis/w33_pass1192_parallel_synthesis_guard.py
PYTHONPATH=analysis python analysis/w33_pass1197_parallel_collision_guard.py --check-only
```

The release workflow is `.github/workflows/pass1193_1197_exact_release.yml`.
