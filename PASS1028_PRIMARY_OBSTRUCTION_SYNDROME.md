# Pass 1028 — Primary obstruction syndrome and residual-carrier theorem

**Certificate:** `analysis/w33_pass1028_primary_obstruction_syndrome.py` →
`data/w33_pass1028_primary_obstruction_syndrome.json` (`18/18`, deterministic,
standard-library Python).

## The theorem

The verified factorization

\[
C_6\cong C_2\times C_3
\]

gives two independent section obstructions: binary sign/chirality and ternary
Eisenstein phase. Restriction to four named subgroup probes realizes the complete
Boolean syndrome square:

| probe | chirality obstruction | phase obstruction | syndrome |
|---|---:|---:|---:|
| \(Z(\mathrm{Sp}(4,3))\cong C_2\) | 1 | 0 | `10` |
| Sylow \(3\) | 0 | 1 | `01` |
| Sylow \(5\) | 0 | 0 | `00` |
| \(\mathrm{Sp}(4,3)\) | 1 | 1 | `11` |

The decoder matrix

\[
\begin{pmatrix}
1&0\\
0&1\\
0&0\\
1&1
\end{pmatrix}
\]

has rank two over \(\mathbb F_2\). Thus the center reads the chirality bit without
phase contamination, the Sylow-3 subgroup reads the phase bit without chirality
contamination, Sylow-5 is a clean negative control, and the whole group is the
both-obstructed positive control.

## The residual-carrier square

The two intermediate quotients must be read by the fibre that remains:

\[
240/C_2=120=40\cdot3,
\]

so the antipodal-pair intermediate carrier retains a residual \(C_3\) phase fibre;
and

\[
240/C_3=80=40\cdot2,
\]

so the omega-triple intermediate carrier retains a residual \(C_2\) chirality
fibre.

The golden selector has

\[
120=40\text{ anchor lines}\times3\text{ phase sheets}.
\]

Therefore it has the correct **carrier signature** for the residual ternary phase
bundle, not for the binary chirality bundle. This is a type-level compatibility
statement, not yet a permutation-action isomorphism.

## Contextuality-orientation firewall

The newest Pass-1021 corollary fixes an additional invariant:

\[
W(3,3)=(36\text{ spreads},0\text{ ovoids}),
\]

while the dual orientation satisfies

\[
Q(4,3)=(0\text{ spreads},36\text{ ovoids}).
\]

E8 lands on the point action, so its residual \(C_3\) carrier lies over the
zero-ovoid, KS-uncolourable orientation. The golden selector is anchored on the
40 lines, so its natural quotient lies on the dual, 36-ovoid orientation.

Thus the two objects share

\[
120=40\cdot3
\]

and the same residual prime, but their natural 40-object quotients have opposite
exact-cover/contextuality invariants. Any genuine bridge must explicitly transport
the point/line block system. Equal degree and equal fibre size are not enough.

The independent binary chirality coordinate missing from the ternary selector is
a natural candidate for an orientation-switch datum, but this pass does not claim
or construct such an equivariant switch.

## Selector layering

The existing failure data now separates cleanly into levels:

\[
120=40\cdot3
\]

is the phase-sheet carrier;

\[
108
\]

is the failed minimal-\(Z\) support decoration on one selected sheet; and

\[
864=108\cdot8
\]

adds the \(D_4\) ordering torsor.

None of these three numbers supplies the missing independent binary sign coordinate.
A device claiming full \(C_6\) holonomy must show both a ternary sheet cycle and an
independent commuting sign inversion, producing six CRT-labelled responses.

## Cohomology firewall

The Pass-341 selector-sign Bockstein is a local, non-globalizable
\(H^2(K,\mathbb F_2)\) class. The primary phase target is a global action-groupoid
\(H^1\) class with \(C_3\) coefficients. They differ in coefficient prime,
cohomological degree, and globalization behavior. They cannot be identified
without an explicit transgression.

## Boundary

This pass proves the complete restriction-syndrome decoder, the residual-carrier
type of the 120-sheet selector, and the exact ovoid-count orientation firewall. It
does **not** prove that the E8 antipodal-pair 120-set and the golden-selector 120-set
are conjugate permutation actions. That remains the separate objectwise degree-120
diagnostic.
