# Exact Fourier-twisted compiler for the two Hesse 36-carriers

The ordinary Payne/Hesse 36 and the maximal compiler-safe 36 are not equivalent
as plain permutation \(SL(2,3)\)-sets. Their mismatch is concentrated on the
order-three class. The orbit data nevertheless exposes a complete linear
repair.

Under
\[
G=SL(2,3),
\]
the ordinary carrier has orbit decomposition
\[
4+4+4+24,
\]
while the safe carrier has
\[
4+4+4+8+8+8.
\]

The three 4-orbits have the same order-six stabilizer on both sides, so those
12 states pair objectwise. The ordinary 24-orbit is the regular \(G\)-set. All
three safe 8-orbits have the same order-three stabilizer \(H\cong C_3\).
Therefore
\[
\boxed{
\operatorname{Reg}(G)
\cong
\operatorname{Ind}_{H}^{G}(1)
\oplus
\operatorname{Ind}_{H}^{G}(\chi)
\oplus
\operatorname{Ind}_{H}^{G}(\chi^2).
}
\]

This is not merely an abstract character identity in the repository. The
certificate constructs the intertwiner explicitly.

Choose the eight right \(H\)-cosets \(rH\). On each coset perform the
three-point Fourier transform
\[
|r,j\rangle
\longmapsto
\sum_{k=0}^{2}\omega^{-jk}|rh^k\rangle,
\qquad j=0,1,2.
\]
Interpret the three safe 8-orbits as the three character sectors
\(1,\chi,\chi^2\). The induced monomial action is then
\[
g|r,j\rangle
=
\omega^{j m(g,r)}
|r',j\rangle,
\qquad
gr=r'h^{m(g,r)}.
\]

The resulting full 36-dimensional compiler has:

- coefficient field \(\mathbf Q(\omega)\);
- exact rank 36;
- 84 nonzero entries;
- 12 one-supported objectwise columns;
- 24 three-supported Fourier columns;
- exact column Gram profile \(1^{12}\oplus3^{24}\);
- all \(24^2\cdot36=20{,}736\) target representation-law checks passed;
- all 24 intertwining identities passed exactly.

After the twist, the target permutation/phase character is
\[
(36,12,3,0,3)
\]
on element orders \(1,2,3,4,6\), exactly the ordinary source character. Before
the twist the order-three trace was 9; the Fourier-character completion changes
it to 3 and leaves the other strata unchanged.

Multiplying the 24 Fourier columns by \(1/\sqrt3\) gives a complex-unitary
normalization. The exact algebraic certificate itself stays over
\(\mathbf Q(\omega)\) and does not need that normalization.

## Compiler reading

The missing ternary layer is now explicit: it is not a new routing geometry.
Twelve states compile by a literal object map. The remaining 24 states are
eight \(C_3\) fibers whose Fourier modes are the three safe character sheets.

This closes the finite \(SL(2,3)\) representation-level compiler problem for
the two 36-state carriers after the stated character twist.

## Boundary

The theorem does not show that E8 dynamics, a heterotic vacuum, or photonic
hardware physically selects this twist. It is an exact finite
representation/compiler theorem and a concrete target for the next physical
selection test.
