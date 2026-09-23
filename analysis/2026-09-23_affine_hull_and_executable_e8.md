# Affine hull, quantum-distance obstruction, and executable E8 transport

The parent ramified code is already certified in
`analysis/w33_ramified_hesse_cubic_holonomy_bridge.py` and
`analysis/w33_affine_holonomy_vm_code_architecture.py`:

G = [2 A | I_12 tensor (1,1,1)], with A the line-point incidence of AG(2,3).

The extension `analysis/w33_affine_holonomy_hull.py` independently reconstructs
these affine lines and checks them against the parent certificate. Its exact
Gram matrix is (J_4-I_4) tensor J_3 over F_3. For a coefficient vector c,
write s_d for its sum on the three lines in direction d. Then c is in the
radical exactly when all four s_d agree. Eight within-direction differences
and one equal-direction-sum vector give a basis of the nine-dimensional hull.

Exhausting all 19,683 hull words proves **[45,9,12]_3**. Its 24 minimum words
are exactly the signed differences of two parallel-line generators. The
nondegenerate quotient has dimension three and Gram matrix with zero diagonal
and ones off diagonal. Its four projective isotropic points are
(1,0,0), (0,1,0), (0,0,1), (1,1,1): the four direction classes.

The punctured [21,12,4]_3 encoder has dual **[21,9,5]_3**, with exactly 18
minimum words, the signed point-star parity checks. This is an exact local
check structure for a classical VM register, without a latency claim.

A useful negative result follows. Using the self-orthogonal hull as both CSS
check spaces gives **[[45,27,2]]_3**, not a single-error-correcting quantum
memory. Every hull column is nonzero, excluding dual weight one. A difference
inside a private triple is a dual weight-two word and cannot lie in the hull,
whose distance is twelve. This proves the quantum distance is exactly two.

The Hesse incidence geometry is classical; see Artebani and Dolgachev,
[The Hesse pencil of plane cubic curves](https://arxiv.org/abs/math/0611590).
Affine-plane incidence hulls have prior literature, including Ghinelli,
de Resmini and Key, *Minimum words of codes from affine planes*,
[DOI 10.1007/s00022-008-2096-y](https://doi.org/10.1007/s00022-008-2096-y).
The present certificate concerns the private-triple lift. We do not claim
newness for Hesse geometry or the parent [45,12,6] parameters, already audited
against [Saif–Alhomaidhi](https://doi.org/10.3390/math14112019).

## Integration corrections that make the algebra computable

The incoming full E8 Chevalley transport supplied a valid change-of-basis
recipe but no callable hybrid bracket. The v2 implementation now supplies
`to_source`, `from_source`, `source_bracket`, and `bracket` on sparse exact
vectors over Q(omega). It serializes the neutral source indices, matter
permutations and signs. All 248 basis vectors roundtrip in both directions;
all six grade products have nonzero source-table regression witnesses.
The complete source Jacobi sweep checks 2,511,496 triples. Invertible transport
then preserves Jacobi. This is a finite algebra computation, not a derivation
of a spacetime action, masses, couplings, or scattering amplitudes.

The neutral basis is explicitly h1..h8 followed by source grade-zero root
vectors. The matter basis uses the canonical signed current-H27 label chart.
Equality with a separately frozen negated-root atlas is not assumed.

The incoming anti-linear charge-conjugation scaffold had a phase error:
C Z_FI C^-1 = Z_FI, because grade swapping and complex conjugation each invert
the phase. Coefficient conjugation alone gives the inverse. The producer,
certificate, regression, report and paper insert now use the commutation law.
