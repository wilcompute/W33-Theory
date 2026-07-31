# Passes 1531–1535 — frame resolution, obstruction modules, and the harmonic bridge

This packet executes the five continuations opened by the frame-Hoffman theorem after reconciling the newest parallel commits. It preserves every active evidence boundary: the global nine-cover resolution is still open, and the 327-orbit cover frontier is not promoted to an exhaustive census.

## Pass 1531 — exact global decision instance

For frame `f` and color `c`, introduce `x[f,c]`. The exact encoding has:

- `540*9 = 4,860` Boolean variables;
- 19,980 clauses imposing exactly one color on each frame;
- 79,920 clauses imposing exactly one frame of each color through every W33 edge;
- nine unit clauses fixing the colors on one edge `K9` to remove global `S9` symmetry.

The resulting DIMACS instance has 99,909 clauses, 1,437,956 bytes, and SHA256

```text
226ea85993ff629207980d8b9f090ff860b298a54c12372277e5d635493a88ab
```

It is equivalent to a nine-cover resolution. A local HiGHS branch-and-bound run and the parallel CaDiCaL run remained undecided, so no SAT or UNSAT claim is made.

## Pass 1532 — the 315-dimensional frame obstruction module

The action is rebuilt from symplectic transvections:

```text
PSp(4,3):  order 25,920, frame stabilizer 48, permutation rank 32
PGSp(4,3): order 51,840, frame stabilizer 96, permutation rank 22
```

The complete orbital commutant gives the stable `H=-4` block profile

\[
64\oplus81\oplus20\oplus60\oplus60\oplus15\oplus15.
\]

For `PSp(4,3)`, orbital operators mix the two 60-blocks and also the two 15-blocks. Hence the isotypic fingerprint is

\[
E_{-4}(H)\sim64\oplus81\oplus20\oplus60^{\oplus2}
\oplus15_{\mathrm{other}}^{\oplus2}.
\]

The frame stabilizer has point orbits `8,8,24`; every one of the three equivariant frame-to-point orbital maps vanishes on `E_-4`. This proves that the repeated 15 is the other rational degree-15 constituent, not the one in the 40-point permutation module.

After adjoining an anti-symplectic similitude, the two 15-blocks cease to mix while the 60-blocks continue to mix:

\[
64\oplus81\oplus20\oplus60^{\oplus2}
\oplus15_{\mathrm{other}}^+\oplus15_{\mathrm{other}}^-.
\]

The projective action inflates to `Sp(4,3)` with central `-I` acting trivially. The ATLAS degree list for `U4(2)=PSp(4,3)` supplies an independent representation-theoretic cross-check. The block extraction remains explicitly labeled a commutant fingerprint pending a literal GAP character-inner-product certificate.

## Pass 1533 — maximum-coclique frontier audit

Every 60-frame maximum Hoffman coclique is an exact cover. The frozen frontier contains 327 complete `PSp(4,3)` orbits with stabilizer-order histogram

```text
order 2: 228
order 4:  84
order 8:  15
```

and therefore certifies

\[
228\frac{25920}{2}+84\frac{25920}{4}+15\frac{25920}{8}=3,547,800
\]

distinct covers. Both opposite DFS prefixes hit the same 327 orbits; all 327 have a disjoint partner; and the 13,648 known partners of the canonical cover form a graph of clique number three. These are exhaustive statements inside the frozen frontier, not proof that the frontier is globally complete.

## Pass 1534 — exact geometry of the blocked four-packing

For the four pairwise-disjoint covers, set `y_i=x_i-(1/9)1`. Then

\[
\langle y_i,y_i\rangle=\frac{160}{3},\qquad
\langle y_i,y_j\rangle=-\frac{20}{3}\quad(i\ne j).
\]

Any fifth disjoint cover has forced projection

\[
y_{\rm frac}=-\frac15(y_1+y_2+y_3+y_4),
\qquad\|y_{\rm frac}\|^2=\frac{16}{3}.
\]

This is exactly the uniform residual weight `1/5`: `-1/9` on the 240 used frames and `4/45` on the remaining 300. Therefore an integral fifth layer would require

\[
y_5=y_{\rm frac}+z,\qquad z\perp\operatorname{span}(y_1,\ldots,y_4),
\qquad\|z\|^2=48.
\]

The frozen 2,332-node Algorithm X trace proves this integral shell empty for this packing. It does not prove every possible four-packing is blocked.

## Pass 1535 — exact frame-to-harmonic Steinberg bridge

Let

\[
P_4=(H-32I)(H-14I)(H-8I)(H-2I)(H+4I),
\]

so `P4=-17920` on `E_4(H)` and zero on every other frame eigenspace. An integral Reynolds map `T:Z^540→Z^240`, with entries in `[-3,3]`, yields `B=TP4`. The verifier proves over the integers

```text
rank d1 = 39       rank d2 = 120
rank P4 = 81       rank B  = 81
d1 B = 0           d2^T B = 0
B H = 4 B          S(g)B = BR(g) for four generators
```

Thus

\[
\boxed{E_{+4}(H)\cong\ker d_1\cap\ker d_2^{\mathsf T}}
\]

as `PSp(4,3)`-modules. The bridge hashes are

```text
T   5ba0d667317317c4b45897192b6bd28efde5317916d41fcc92e90474775eb874
P4  7f020aaf0da40f0cf589f2610fc7542d7f5815c46b96a65f00e78739f8fe41db
B   02c63b9a3d00eaee1e758e336d6d3f9a20824b0b1d46a01ee0110ada68879f90
```

This closes the proposed 81-sector intertwiner by a literal integer map. It remains a finite-module theorem and does not supply a Hodge star or continuum dynamics.

## External anchors

- A. Abiad, W. Bosma, T. van Veluw, *Hoffman colorings of graphs*, arXiv:2407.02544 — general equality/equitable-partition framework.
- ATLAS of Group Representations, `U4(2)` / `S4(3)` — independent degree and Steinberg-module cross-checks.

All W33-specific spectra, modules, affine fibers, matrices, and hashes in this packet are repository computations.
