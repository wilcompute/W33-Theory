# Passes 9029–9040 — Rank-24 W(3,3) Root-Shadow Trichotomy

## Status

**Machine-verified.** The executable witness is
`analysis/w33_pass9029_9040_root_shadow_trichotomy.py`; the frozen result is
`data/PART_W33_PASS9029_9040_ROOT_SHADOW_TRICHOTOMY.json`.

This pass starts only after the Pass 8989–9012 exhaustive theorem that exactly three rank-24
Niemeier lattices carry the required pure `Phi_9^4` order-nine action producing
`L/(I-X)L ~= F_3^4` with a nondegenerate alternating form:

- `E8^3` — the three-factor lift;
- `E6^4` — the diagonal sporadic carrier;
- `A2^12` — the Golay-twisted `3^4` carrier.

The new question is not whether they produce W(3,3), but what their **root systems do under
the quotient map**.

## 1. A2^12 is now independently executable

Pass 8989–9012 froze the classification and a summary certificate. This pass closes the
reproducibility gap by rebuilding the third carrier from scratch.

The verifier constructs the extended ternary Golay code with parameters

`[12,6,6]_3`,

checks its 729 words and exact weight enumerator

`1 + 264 y^6 + 440 y^9 + 24 y^12`,

and verifies self-duality. It then checks the explicit signed monomial automorphism

```text
perm  = [5,2,4,11,1,7,3,0,9,10,8,6]
signs = [2,2,2,1,1,2,1,1,1,2,2,1]  (2 = -1 mod 3)
cycles = (7 0 5)(4 1 2)(8 9 10)(11 6 3)
```

as an order-three automorphism of the Golay code.

Using the standard `A2` fundamental-weight glue, the script reconstructs `N(A2^12)` as an
index `3^6=729` overlattice of `A2^12`, and verifies an integral even unimodular Gram matrix.
One `A2` Coxeter twist is inserted in each component 3-cycle. The resulting integral lattice
automorphism satisfies

`X^9 = I`, `X^3 != I`, `Phi_9(X)=0`, `det(I-X)=81`,

and for `P=3(I-X)^(-1)` and `F=P^T G`,

`F+F^T = 3G`.

Modulo 3 the induced alternating form has rank four, recovering W(3,3).

## 2. The root-shadow theorem

Let

`pi_X : roots(N) -> P(L/(I-X)L)`

be the projectivized quotient map, with zero retained separately. The three carriers have
**different exact root shadows**:

| carrier | roots | quotient-zero roots | visible W33 points | roots / visible point | geometry of visible support |
|---|---:|---:|---:|---:|---|
| `E8^3` | 720 | 0 | 40 | 18 | all of W(3,3) |
| `E6^4` | 288 | 72 | 4 | 54 | one W33 line |
| `A2^12` | 72 | 0 | 4 | 18 | one W33 line |

For the two four-point supports the verifier checks both conditions for an actual projective
line: their vector span has dimension two over `F_3`, and every pair is symplectically
orthogonal. Since a W(3,3) line has four points, the support is exactly one line.

For `E8^3`, all 40 projective points occur. The induced collinearity graph is rebuilt and
checked as `SRG(40,12,2,4)`. More strongly, **each individual E8 factor** already hits all 40
points with six roots per point; the three-factor lift merely triples the fibre from 6 to 18.
This recovers the earlier E8 -> W33 Eisenstein six-to-one fibration inside the new rank-24
carrier.

## 3. The E6 kernel is the root system of the third carrier

The sharpest new cross-carrier connection is inside `E6^4`.

Each E6 component contributes:

- 18 roots mapping to zero;
- 54 roots mapping to one nonzero projective point.

The 18 quotient-zero roots are not an arbitrary subset. The verifier checks reflection closure
and the orthogonality decomposition and obtains three connected six-root components:

`18 = 6 + 6 + 6`,

hence exactly

`A2^3`.

Across all four E6 components,

`4 A2^3 = A2^12`.

Therefore the quotient-zero **root system** of the `E6^4` carrier is precisely the root-system
type of the third rank-24 carrier:

`kernel_roots(E6^4 -> W33) = A2^12`.

This is deliberately not promoted to an equality of Niemeier lattices. `N(E6^4)` and
`N(A2^12)` are different even unimodular overlattices; the theorem is about the root subsystem
inside the first.

## 4. Root-pair interpretation

After identifying `alpha` and `-alpha`, the visible fibres have sizes

- `E8^3`: 9 root pairs per W33 point, on all 40 points;
- `E6^4`: 27 root pairs per visible point, on four collinear points;
- `A2^12`: 9 root pairs per visible point, on four collinear points.

The `27` in the E6 carrier is exact rather than numerological: each E6 component has 54 visible
roots, i.e. 27 opposite pairs, after its `A2^3` kernel is removed.

## 5. External context checked

The calculation is internal, but its ingredients were cross-checked against the standard
literature:

- Cheng–Duncan–Harvey, *Umbral Moonshine and the Niemeier Lattices* (2014), defines the
  Niemeier/umbral quotient `G^X = Aut(N^X)/W(X)` and treats all 23 rootful rank-24 Niemeier
  lattices (arXiv:1307.5793).
- Standard coding descriptions identify `N(A2^12)` with ternary-Golay glue and the extended
  ternary Golay code as self-dual `[12,6,6]_3`.
- Standard Niemeier constructions identify `N(E6^4)` as the inverse image of a self-dual
  ternary length-four glue code in `(E6^*/E6)^4`.

The web/literature check did **not** turn up this three-carrier W33 root-shadow comparison or
the `E6^4` quotient-kernel `A2^12` observation. The repository verifier is therefore the
current evidence for those statements.

## 6. Interpretation boundary

A useful mathematical reading is that the same four-dimensional symplectic quotient has three
inequivalent rank-24 **root decorations**:

1. a full 40-point E8 decoration;
2. a line-supported E6 decoration with a hidden `A2^12` root kernel;
3. a pure line-supported `A2^12` decoration.

Calling these different “UV completions” of the same finite “IR” geometry is an analogy, not a
physics theorem. No Standard-Model, continuum, or dynamical claim follows from this pass.

## Next pressure point

The natural next exact discriminator is the Niemeier automorphism quotient. The three carrier
automorphisms have visibly different origins:

- `E8^3`: a nontrivial 3-cycle of the E8 factors;
- `E6^4`: a diagonal element already inside `W(E6)^4`;
- `A2^12`: a signed `3^4` monomial Golay automorphism, with Coxeter twists lying in the root
  Weyl group.

That should distinguish the same three carriers at the umbral quotient level and can be checked
without importing any phenomenological assumptions.
