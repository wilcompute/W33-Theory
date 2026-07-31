# Passes 1521–1525 — frame resolution, module structure, and the harmonic bridge

This packet executes the five continuations opened by the frame-Hoffman theorem. It incorporates the newest parallel-track corrections before drawing any conclusion. In particular, it uses the certified four-cover packing and its residual Algorithm X trace, the 327-orbit saturation frontier, and the full-group Steinberg-extension calculation. None of those inputs is silently upgraded past its stated quantifier.

## Pass 1521 — the global resolution is now a frozen SAT instance

For frame `f` and color `c` introduce `x[f,c]`, giving `540*9=4860` Boolean variables. The clauses are:

* exactly one color on each of 540 frames: `540*(1+C(9,2)) = 19,980`;
* for each of 240 W33 edges and each of nine colors, exactly one of the nine incident frames has that color: `240*9*(1+C(9,2)) = 79,920`;
* nine unit clauses fixing the colors on one edge-clique to quotient the global `S9` color symmetry.

Hence the exact DIMACS instance has

```text
variables  4,860
clauses   99,909
bytes   1,437,956
SHA256  226ea85993ff629207980d8b9f090ff860b298a54c12372277e5d635493a88ab
```

This is logically equivalent to a nine-cover resolution. A local HiGHS branch-and-bound run and the parallel CaDiCaL run were both undecided. Therefore `chi(H)=9` remains open: this pass freezes the decision problem; it does not pretend that a time-limited run is a certificate.

## Pass 1522 — the 315-dimensional obstruction module

The action is rebuilt from symplectic transvections, not imported from a cached character decomposition.

```text
PSp(4,3): order 25,920, frame stabilizer 48, permutation rank 32
PGSp(4,3): order 51,840, frame stabilizer 96, permutation rank 22
```

A generic symmetric element of the complete orbital commutant splits the `H=-4` space into the stable block profile

\[
64\oplus81\oplus20\oplus60\oplus60\oplus15\oplus15.
\]

For `PSp(4,3)`, another orbital has nonzero off-diagonal action between both 60-blocks and between both 15-blocks. Thus these are multiplicity-two isotypic components, not unrelated representations with matching dimensions:

\[
E_{-4}(H)\sim 64\oplus81\oplus20\oplus 60^{\oplus2}
                   \oplus 15_{\mathrm{other}}^{\oplus2}.
\]

The frame stabilizer has point orbits `8,8,24`. All three rectangular orbital maps from the 540-frame module to the 40-point permutation module vanish on `E_-4`. Therefore the repeated 15 is the *other* rational degree-15 constituent, not the 15 occurring in the 40-point module.

After adjoining an anti-symplectic similitude, the two 15-blocks cease to mix, while the 60-blocks continue to mix. Thus the full-group fingerprint is

\[
64\oplus81\oplus20\oplus60^{\oplus2}
       \oplus15_{\mathrm{other}}^+\oplus15_{\mathrm{other}}^-.
\]

The projective action inflates to `Sp(4,3)` with central `-I` acting trivially. The ATLAS page for `U4(2)=PSp(4,3)` independently lists characteristic-zero representations of dimensions 15a, 15b, 20, 60, 64, and 81, and identifies the 81-dimensional modular representation as Steinberg:
https://brauer.maths.qmul.ac.uk/Atlas/v3/clas/U42/

Evidence boundary: the orbital actions, group orders, subdegrees, zero maps, and block dimensions are rebuilt independently. The character labels are a stable commutant fingerprint matched against the ATLAS degree list; a literal GAP character-inner-product certificate is still the cleanest final formalization.

## Pass 1523 — maximum coclique classification, exactly scoped

Every maximum Hoffman coclique is an exact cover, so classifying covers and classifying maximum cocliques are the same problem. The current certified frontier contains 327 complete `PSp(4,3)` orbits with stabilizer-order histogram

```text
order 2: 228 orbits
order 4:  84 orbits
order 8:  15 orbits
```

and therefore certifies

\[
228\frac{25920}{2}+84\frac{25920}{4}+15\frac{25920}{8}
=3,547,800
\]

distinct covers. Both opposite DFS prefixes hit the same 327 orbits, all 327 have a partner disjoint from the canonical cover, and the 13,648 known partners form a graph of clique number three.

What is *not* proved is equally important: both searches are finite prefixes. Agreement under branch reversal is strong saturation evidence, but not global orbit completeness. The four-cover packing is real; the claim that 327 is the complete global orbit census remains open.

## Pass 1524 — the four-packing's affine fiber

Let `x_i` be the four pairwise-disjoint cover indicators and

\[
y_i=x_i-\frac19\mathbf 1.
\]

Their Gram matrix is exact:

\[
\langle y_i,y_i\rangle=\frac{160}{3},\qquad
\langle y_i,y_j\rangle=-\frac{20}{3}\quad(i\ne j).
\]

Any fifth disjoint cover must have the fixed projection

\[
y_{\rm frac}=-\frac15(y_1+y_2+y_3+y_4),
\qquad \|y_{\rm frac}\|^2=\frac{16}{3}.
\]

This is *exactly* the uniform residual `1/5` solution: it equals `-1/9` on the 240 used frames and `4/45` on the remaining 300. Consequently every integral fifth cover would have to be

\[
y_5=y_{\rm frac}+z,
\qquad z\perp\operatorname{span}(y_1,\ldots,y_4),
\qquad \|z\|^2=48,
\]

with residual coordinates `4/5` on 60 selected frames and `-1/5` on the other 240. The frozen 2,332-node Algorithm X trace proves this integral shell empty. This explains the integrality gap geometrically rather than merely reporting it. It is a theorem about this particular four-packing, not every possible packing.

## Pass 1525 — exact frame-to-harmonic Steinberg bridge

Let

\[
P_4=(H-32I)(H-14I)(H-8I)(H-2I)(H+4I),
\]

so `P_4=-17920` on the frame `+4` eigenspace and vanishes on every other frame eigenspace. From seed frame 0 and seed signed edge 4, form the integral Reynolds map `T: Z^540 -> Z^240`; its entries lie in `[-3,3]`. Define

\[
B=T P_4.
\]

The independent verifier proves, over the integers,

```text
rank d1 = 39
rank d2 = 120
rank P4 = 81
rank B  = 81

d1 B   = 0
d2^T B = 0
B H     = 4 B
S(g) B  = B R(g)  for all four generators
```

Therefore

\[
\boxed{E_{+4}(H)\cong \ker d_1\cap\ker d_2^{\mathsf T}}
\]

as `PSp(4,3)`-modules. The right side is the 81-dimensional harmonic signed-edge sector already identified as Steinberg, so the equality is now implemented by a literal integer matrix rather than inferred from dimension 81.

Frozen hashes:

```text
T   5ba0d667317317c4b45897192b6bd28efde5317916d41fcc92e90474775eb874
P4  7f020aaf0da40f0cf589f2610fc7542d7f5815c46b96a65f00e78739f8fe41db
B   02c63b9a3d00eaee1e758e336d6d3f9a20824b0b1d46a01ee0110ada68879f90
```

This closes the proposed 81-sector intertwiner. It remains finite kinematics: it does not create the absent Hodge star or a continuum action.

## External theory check

The equality structure is consistent with the modern decomposition theory of Hoffman colorings, where attaining the spectral bound forces regular/equitable color-class structure. See Abiad–Bosma–van Veluw, *Hoffman colorings of graphs*, arXiv:2407.02544. The external paper supports the general equality framework; all W33-specific spectra, modules, maps, and hashes above are repository computations.
