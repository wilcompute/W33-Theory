# Passes 9197–9260 — Eight-front continuation from the rank-24 W(3,3) root shadows

## Status and evidence boundary

This packet executes the five requested continuation fronts from Passes 9173–9196 plus three independent outside-box attacks.  Every promoted finite claim has an executable witness under `analysis/w33_pass9197_...` through `analysis/w33_pass9253_...` and a frozen JSON certificate under `data/PART_W33_PASS...`.

The dedicated GitHub Actions gate is `.github/workflows/pass9197-9260.yml`.  The mathematical claims below do not depend on interpreting any continuum or particle-physics model.  The optical section is explicitly conditional on its stated equal-coupling readout model.

## 1. Passes 9197–9204: the E6^4 root-shadow line has the full W33 line stabilizer

Passes 9173–9184 found that `N(E6^4)` projects its visible roots onto exactly one line of `W(3,3)`.  The new verifier reconstructs the carrier and computes the action on the four-dimensional quotient of two explicit families of lattice automorphisms that centralize the order-nine carrier:

- four independent local order-nine E6 phases;
- all signed monomial automorphisms of the tetracode glue.

The local phases induce a group of order `27`.  The signed tetracode monomial lifts number `48`, and their action on the four visible root-shadow points contains all `24` permutations.  Together the induced matrices generate a group of order

`1296`

inside `Sp(4,3)`.  Projectivizing by `+/- I` gives

`648 = 3^3 * 24`,

with the full `S4` action on the four line points.  This is exactly the projective line stabilizer in `PSp(4,3)`.

**Theorem.**  The exhibited `E6^4` carrier-centralizing subgroup maps onto the entire W33 line stabilizer `3^3:S4`.  The `3^3` part is supplied by local phase differences; the `S4` part permutes the four E6/root-shadow channels.

For `A2^12`, support alone proves that its carrier-centralizer image lies in a conjugate line stabilizer, but this pass does not compute equality.  For `E8^3`, the root shadow is all forty W33 points, so there is no line-support restriction.

## 2. Passes 9205–9212: root-shadow type and umbral image are independent carrier data

The same W33 quotient has three different images in the classical Niemeier automorphism quotients:

| carrier | root shadow | umbral quotient | carrier image |
|---|---|---|---|
| `E8^3` | all 40 points | `S3` | order-3 factor cycle |
| `E6^4` | one line + `A2^12` root kernel | `GL2(3) ~= 2.S4` | identity |
| `A2^12` | one line | `2.M12` | order-3 signed monomial lift over `M12` class `3B` |

For `E8^3`, the local E8 Coxeter part is Weyl and the factor 3-cycle survives.  For `E6^4`, the carrier is diagonal inside `W(E6)^4`, hence dies completely modulo the Weyl group.  For `A2^12`, the local A2 Coxeter twists are Weyl while the signed Golay monomial action survives; its coordinate permutation has cycle shape `3^4`, the ATLAS `M12` class `3B`.

**Conclusion.**  The finite quotient `W(3,3)` does not determine the ultraviolet Niemeier automorphism class.  The pair `(root-shadow type, umbral image)` is a strictly finer carrier invariant.

Classical provenance: Cheng–Duncan–Harvey, *Umbral Moonshine and the Niemeier Lattices*, arXiv:1307.5793; ATLAS of Finite Group Representations, `M12` 12-point action.

## 3. Passes 9213–9220: welding the Niemeier line to the Suzuki selector is an exact no-go

The M12:2 polarization in the exact `2.Suz < Sp(12,3)` module yields `7,371` nondegenerate two-spaces `A < U+`, hence W33 candidates

`W_A = A + xA`.

The new verifier checks every one.  In every candidate:

- `A` is a two-dimensional isotropic subspace, hence a W33 line;
- `xA` is a second isotropic W33 line;
- their cross-pairing has rank two;
- together they span the full nondegenerate four-space `W_A`.

Therefore every candidate already contains a canonical ordered pair of lines.  Identifying the four-point Niemeier root-shadow line with the first polarization line leaves **all 7,371 candidates**.  The exact `C4 x A5` controller from Passes 9101–9108 still has `90` orbits on them.

**No-selection theorem.**  A marked W33 line is not enough to weld a unique Niemeier carrier to a unique Suzuki W33 slice.  Any successful weld needs an additional datum.

The remainder of this packet finds two such additional finite data: orthogonal sign and an `F9` complex structure.

## 4. Passes 9221–9228: the E8 root shadow itself is cyclotomically periodic

Starting from the rank-eight E8 order-three carrier, the verifier applies the three-cycle lift recursively and checks ranks

`8, 24, 72, 216`.

At every rung:

- `L/(I-g)L` remains four-dimensional over `F3`;
- the visible support remains all forty W33 points;
- **every individual E8 factor** maps exactly six roots to each W33 point.

Thus the total root fibre is

`6, 18, 54, 162`

roots per W33 point at ranks `8,24,72,216` respectively.

This strengthens the earlier rank-periodicity theorem: through four exact rungs, the lift preserves not merely the abstract symplectic quotient but the full-support E8 root decoration, changing only a uniform multiplicity.

## 5. Passes 9229–9236: a two-observable finite optical discriminator

A deliberately minimal readout model was tested:

- the forty W33 quotient points are output ports;
- all roots couple with equal weight;
- intensities from roots within a port add incoherently;
- quotient-kernel roots are dark.

Under that model, two dimensionless observables separate all three rank-24 carriers:

1. best-W33-line fraction of the **visible** intensity;
2. dark-root fraction.

The signatures are

`E8^3   -> (0.1, 0)`

`E6^4   -> (1, 0.25)`

`A2^12  -> (1, 0)`.

So `E8^3` is delocalized over all forty ports, `E6^4` is line-localized with one quarter of its roots dark, and `A2^12` is line-localized without a dark root sector.

**Physical boundary.**  This is a falsifiable port-level discriminator conditional on the equal-root-coupling model.  It is not yet an optical Hamiltonian, transfer matrix, or fabrication prescription.

# Three outside-box attacks

## 6. Passes 9237–9244: the two Niemeier glue codes generate a new six-qutrit/F9 phase space

Let `C_G` be the extended ternary Golay `[12,6,6]_3` glue and `C_E` the quotient-selected `E6^4` relative `[12,6,3]_3` glue from Passes 9185–9196.

The verifier proves

`C_G intersect C_E = {0}`

and

`C_G + C_E = F3^12`.

Since both are self-dual/isotropic for the standard dot product, they are **opposite maximal isotropics**.  Their cross-pairing has rank six.  After dualizing that pairing, the decomposition determines:

- a nondegenerate alternating matrix `K` of rank 12 with `K^2=I`;
- both glues Lagrangian for `K`;
- an orthogonal involution `S` exchanging the two Lagrangians and satisfying `S K S^T = -K`;
- a symplectic operator `R = K S` with

`R^2 = -I`, `R^4 = I`.

Because `x^2+1` is irreducible over `F3`, `R` equips the twelve-dimensional `F3` symplectic space with an `F9`-module structure of dimension six.

**Breakthrough.**  The pair of Niemeier glues itself manufactures a six-qutrit phase space and a finite-field complex structure.  This structure is not inserted from the original four-dimensional W33 quotient.

Nomenclature boundary: this is an `F9`/unitary-style structure on a characteristic-three 12-space.  It is distinct from the repository's older characteristic-two modular modules denoted `U6`.

## 7. Passes 9245–9252: the glue exchange converts root creation into distance-six protection

Inside the E6-relative glue, the four projective weight-three extension directions span a code

`[12,4,3]_3`

with weight enumerator

`1 + 8 y^3 + 24 y^6 + 32 y^9 + 16 y^12`.

These four directions are exactly the local `A2^3 -> E6` extension channels that account for the `216` visible non-kernel E6 roots.

Apply the canonical exchange involution `S` from the previous pass.  Their four-dimensional image lies inside the extended ternary Golay code and is

`[12,4,6]_3`,

with exact weight enumerator

`1 + 28 y^6 + 48 y^9 + 4 y^12`.

There is no weight-three word.

**Root-creation/protection exchange.**  The canonical glue exchange maps the dimension-four sector that permits norm-two E6 root extensions to an 81-word Golay sector whose minimum glue weight six forbids those norm-two extensions.

This is a precise code/lattice duality.  Calling the two sides “creation” and “protection” is shorthand for whether the glue admits new norm-two lattice vectors; it is not a dynamical particle-creation statement.

## 8. Passes 9253–9260: Q-(5,3) from the glues is the exact orthogonal-sign twin of Suzuki's Q+(5,3)

The new symplectic form `K` and complex structure `R` induce on the Golay Lagrangian a symmetric form

`C_-(a,b) = K(a,Rb)`.

In the explicit basis the verifier obtains exactly `C_- = I_6` over `F3`.  It is minus type and has `112` singular projective points, hence `Q^-(5,3)`.

Its census of all `11,011` two-spaces is

- degenerate: `3,640`;
- hyperbolic: `4,536`;
- anisotropic: `2,835`;
- nondegenerate total: `7,371`.

Suzuki's plus-type `Q^+(5,3)` selector has

- degenerate: `3,640`;
- hyperbolic: `5,265`;
- anisotropic: `2,106`;
- nondegenerate total: `7,371`.

So the total is exactly unchanged, while the sign change transfers

`729 = 3^6`

cases from hyperbolic to anisotropic type.

This is not special to `q=3`.  Using the standard finite orthogonal-group orders and orbit-stabilizer, the verifier symbolically reduces the odd-q formulas to

`N_nondeg(2-space in O^+(6,q)) = N_nondeg(2-space in O^-(6,q))`

`= q^4 (q^2-q+1)(q^2+q+1)`,

while

`H_+ - H_- = q^6`,

`A_- - A_+ = q^6`.

At `q=3`, `q^6=729`, which also equals the number of words in either ternary `[12,6]` glue code because both have dimension six.

**Twin-selector theorem.**  The Niemeier glue pair and the Suzuki polarization provide opposite orthogonal signs on six-dimensional selector spaces.  They select the same number of W33 four-spaces, so the total `7,371` is sign-blind; the hyperbolic/anisotropic split remembers the sign.

## Cross-track implications

The parallel Hall–Janko/Leech lane now gives an exact 416-element set of Hall–Janko 100-sets in the 20,800 Leech carrier, with every Leech six-space lying in exactly two such 100-sets; the same degree-416 coset geometry is the local neighbor carrier of the Suzuki graph.  That development strengthens the next target: the marked-line weld is known to be insufficient, while this packet supplies two richer marks—orthogonal sign and the `F9` complex structure—that can be tested on the 416/Hall–Janko/Suzuki tower.

## Literature/provenance gate

Classical ingredients, not claimed as repository discoveries:

- Niemeier lattices and their finite automorphism quotients; Cheng, Duncan, Harvey, *Umbral Moonshine and the Niemeier Lattices*, arXiv:1307.5793.
- ATLAS conjugacy classes of `M12`; in the 12-point action class `3B` has cycle shape `3^4`.
- Standard finite orthogonal-group orders and plus/minus quadrics.

Repository discoveries in this packet are the explicit carrier actions, glue-pair constructions, exact cross-comparisons, and their executable certificates.
