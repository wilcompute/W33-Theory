# Pass 449 — q=5 cubic-section spectrum and Smith taxonomy

Pass 447 proves that the full \(q=5\) section space has 20,592 automorphism orbits, so orbit enumeration is not a useful compression. This pass instead exhausts the canonical lowest nonlinear family

\[
c(a,b)=\alpha a^3+\beta a^2b+\gamma ab^2+\delta b^3,
\qquad (\alpha,\beta,\gamma,\delta)\in\mathbb F_5^4.
\]

All \(625\) forms collapse to exactly five spectrum-and-Smith classes, indexed by binary-cubic factorization type:

| Type | Count | Critical group invariant factors |
|---|---:|---|
| zero or triple root | 25 | \(5^{29},20^{20},120^7,600^{10},3000^{23}\) |
| double plus simple root | 120 | \(5^{16},25^{23},125^{20},11375^{17},56875^3\) |
| linear times irreducible quadratic | 240 | \(5^{38},25^9,125^3,500^{10},4099800500^{10}\) |
| irreducible cubic | 160 | \(5^{27},25^{11},125^{12},375^{10},218305875^{10}\) |
| three distinct roots | 80 | \(5^{38},25^9,125^3,375^{10},5410646625^{10}\) |

The sharpest surprise is the 25-member flat packet: the zero section and all 24 nonzero pure cubes have the same adjacency spectrum **and the same complete critical group** as the flat graph. Cubic curvature can therefore be spectrally and integrally invisible on this packet.

Every class is certified by exhaustive factorization counting, a combined degree-10 Weil polynomial, an exact 125-vertex characteristic polynomial, Matrix--Tree factorization, p-adic Smith elimination, and invariant-factor welding.

**Boundary.** This is exhaustive for homogeneous binary cubics, not for all \(5^{12}\) inverse-closed sections.
