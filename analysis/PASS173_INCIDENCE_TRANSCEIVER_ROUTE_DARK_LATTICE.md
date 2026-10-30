# Pass 173 — Incidence Transceiver and the Route-Dark Pentad Lattice

## Result

Let (N) be the (40\times40) line--point incidence matrix of
(W(3,3)), with rows indexed by isotropic lines and columns by points.
Pass 173 closes the integral address/route comparison that the existing
Levi, sentinel, and pentad tracks left open.

The centered incidence operator

\[
T=N-\frac1{10}J
\]

is a rank-(24) point-to-line transceiver.  If (A_P,A_L) are the point
and line concurrence adjacencies and (E_{24}^P,E_{24}^L) their shared
(24)-dimensional spectral projectors, then

\[
TA_P=A_LT,
\qquad
T^{\mathsf T}T=6E_{24}^P,
\qquad
TT^{\mathsf T}=6E_{24}^L.
\]

Thus (T/\sqrt6) is an exact isometry between the shared gauge sectors.
It kills constants and both unmatched (15)-dimensional dark sectors.  It
is an exact algebraic analyzer/decoder, not by itself an optical-device
claim.

## The 480 selectors acquire exact analyzer words

For every Pass-157 selector

\[
x=\mathbf1_{L_+\setminus\{p\}}-
  \mathbf1_{L_-\setminus\{p\}},
\qquad \|x\|^2=6,
\]

the line-channel word (y=Nx=Tx) has the same value distribution

\[
\{-3^1,-1^9,0^{20},1^9,3^1\},
\qquad \|y\|^2=36,
\]

and is decoded exactly by

\[
x=\frac16N^{\mathsf T}y.
\]

For matrices whose rows are the (480) selector and analyzer words,

\[
X^{\mathsf T}X=120E_{24}^P,
\qquad
Y^{\mathsf T}Y=720E_{24}^L.
\]

This is the missing object-level bridge from the (480)-vector
eigenlattice shell to the (40)-channel line analyzer.  It does not
identify that shell with the different (480) Hashimoto-arc (G)-set.

## The address and route dark lattices are arithmetically different

Define

\[
L_{\rm address}=\ker_{\mathbb Z}N,
\qquad
L_{\rm route}=\ker_{\mathbb Z}N^{\mathsf T}.
\]

Both have rank (15), but every finer integral invariant separates them:

| invariant | address/point (L_{\rm address}) | route/line (L_{\rm route}) |
|---|---:|---:|
| Gram determinant | (2^{17}3^{10}) | (2^{11}3^{14}) |
| Gram Smith profile | (2^5,6^9,24) | (1,3^5,6^8,24) |
| minimum norm | (8) | (10) |
| minimal vectors | (90) | (432) |
| projective minima | (45) | (216) |
| binary kernel code | ([40,15,8]) | ([40,15,10]) |
| binary Gram rank | (0) | (6) (hull dimension (9)) |

The determinant and covolume ratios are

\[
\frac{\det L_{\rm route}}{\det L_{\rm address}}
=\frac{81}{64}=\left(\frac98\right)^2,
\qquad
\frac{\operatorname{covol}L_{\rm route}}
     {\operatorname{covol}L_{\rm address}}=\frac98.
\]

The complete weight enumerator of the new route code begins

\[
1+216z^{10}+270z^{12}+1080z^{14}+3375z^{16}
+7920z^{18}+7044z^{20}+\cdots+z^{40}.
\]

Consequently every nonzero integral route-dark pattern has support at
least (10), versus the address threshold (8).

The asymmetry is stronger than distance.  The address code is doubly even
and self-orthogonal, so the Pass-164 quotient
(C_{\rm address}^{\perp}/C_{\rm address}) and its
(O^+(10,2)) quadratic shadow are defined.  The route code has binary
Gram rank (6) and hull dimension (9), hence
(C_{\rm route}\not\subset C_{\rm route}^{\perp}); there is no analogous
full quotient (C_{\rm route}^{\perp}/C_{\rm route}).  Pass 174 sharpens
this boundary: the canonical hull quotient
((C_{\rm route}\cap C_{\rm route}^{\perp})/\langle\mathbf1\rangle) does
exist and is the plus-type (8)-space (E_8/2E_8).  Thus Pass 164's
(10)-space is address-chiral, while the route side recovers the
(8)-space through its hull rather than its full code.

Exact MacWilliams transforms reveal where the two context systems first
become distinguishable:

| dual context code | (A_4) | (A_6) | (A_8) | (A_{10}) |
|---|---:|---:|---:|---:|
| (C_{\rm address}^{\perp}) | 40 | 240 | 5085 | 47824 |
| (C_{\rm route}^{\perp}) | 40 | 240 | 3645 | 54736 |

They agree exactly on the first two nonzero shells and split for the first
time at weight (8).  In the unscaled parity lattices
({z\in\mathbb Z^{40}:z\bmod2\in C}), the address coefficient at
(q^4) is (14640), while the route coefficient is only the coordinate
contribution (3120); the (216) route words of weight (10) then
produce (216\cdot2^{10}=221184) vectors at (q^5).  After the usual
(1/\sqrt2) Construction-A scaling, self-orthogonality makes the address
lattice integral, whereas the route construction is not integral.

## The route minima are exactly the old pentad cores

An exhaustive census finds (13{,}824) five-line partial spreads.  Their
(20)-point covers occur with multiplicities

\[
1^{13{,}392},\qquad 2^{216}.
\]

The (216) double covers pair (432) distinguished pentads.  For each
pair ((P_+,P_-)),

\[
v_{P}=\mathbf1_{P_+}-\mathbf1_{P_-}
\]

lies in (ker_{\mathbb Z}N^{\mathsf T}), has norm (10), and has ten-line
support.  Its two pentads meet in the crown graph
(K_{5,5}) minus a perfect matching.  The five deleted matching edges are
skew-line charts; over all (216) supports they cover each of the (540)
charts exactly twice.

There are (432) such signed vectors.  A live
[PARI/GP `qfminim`](https://pari.math.u-bordeaux.fr/dochtml/html-stable/Vectors__matrices__linear_algebra_and_sets.html#qfminim)
certificate independently proves that the whole lattice has exactly
(432) minimal vectors of norm (10).  Therefore the exhibited vectors
are the complete minimal shell:

\[
\boxed{
\operatorname{Min}(L_{\rm route})
=\{\pm(\mathbf1_{P_+}-\mathbf1_{P_-}):
       P_+\leftrightarrow P_-\text{ is a pentad core}\}.}
\]

Under (PSp(4,3)), the (216) supports form one orbit with stabilizer
order (120\cong|S_5|).  The signed shell splits into two chiral orbits
of (216); no projective symplectic element sends a vector to its
negative.  This identifies the previously known BT844--BT846
(432/216) carrier intrinsically as a lattice shell.

## Self-duality correction

Equal parameters (s=t=3), equal (40+40) counts, and identical strongly
regular spectra do **not** make (W(3,3)) incidence-self-dual.  Its dual is
the parabolic quadrangle (Q(4,3)); the classical symplectic quadrangle is
self-dual in the even-(q) case, not here.  A current finite-geometry
reference records this boundary in its table of classical generalized
quadrangles: [Crnković--Hawtin--Švob, arXiv:2105.05833](https://arxiv.org/abs/2105.05833).

Pass 173 supplies a stronger internal obstruction.  Any incidence
duality would induce a coordinate permutation identifying
(ker_{\mathbb Z}N) with (ker_{\mathbb Z}N^{\mathsf T}), preserving
determinant, Smith form, minimum, kissing number, and binary distance.
Every one of those invariants differs.  The correct architecture is:

- spectrally paired and losslessly connected on the common (24)-sector;
- type-protected and non-swappable on the two (15)-sector kernels;
- address-dark threshold (8), route-dark threshold (10).

## Reproduction

```bash
python analysis/w33_pass173_incidence_transceiver_route_dark_lattice.py
pytest -q tests/test_pass173_incidence_transceiver_route_dark_lattice.py
```

Artifacts:

- `analysis/w33_pass173_incidence_transceiver_route_dark_lattice.py`
- `data/w33_pass173_incidence_transceiver_route_dark_lattice.json`
- `tests/test_pass173_incidence_transceiver_route_dark_lattice.py`

The witness reports `PASS (36/36)`.  The checked certificate uses live
PARI/GP in the present environment and retains a cached expected-value
fallback for environments without `gp`.
