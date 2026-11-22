# 2026-11-22 — Witting H27 polar pencil and Hessian quotient tower

**Exact mathematics, not a physical unification claim.**

## Verified projective geometry

The base is the canonical forty Witting rays in `C^4`, with exact Eisenstein field arithmetic `Q(omega)`, `omega^2+omega+1=0`. Three order-three reflections on indices `5,26,33` fix ray **25** and generate a group `G` of order **648**. The normal closure `N = <<R5 R33^-1>>^G` is the **exponent-three extraspecial Heisenberg group** `H27`, order 27, central/derived subgroup of order three.

In the exact ray action of `N`, the orbit decomposition is

```
[25]                           singleton fixed ray
[1,5,33]                       polar line pencil fiber 1
[8,23,26]                      polar line pencil fiber 2
[11,14,24]                     polar line pencil fiber 3
[28,35,38]                     polar line pencil fiber 4
27 other rays                  regular H27 address orbit
```

The four three-element orbits are the four lines through ray25, punctured at their common center. Exact Hermitian orthogonality checks verify that the 12 fiber rays are precisely the neighbors of 25, the 27 outer rays are precisely its nonneighbors, and *each fiber with the center is a four-clique*. Globally, for every pair of rays, the graph has parameters `SRG(40,12,2,4)`: 240 orthogonal pairs have two common neighbors; 540 nonorthogonal pairs have four. All arithmetic is exact.

Thus:

`40 = 1 + 4*3 + 27`.

The 27-element orbit is *regular under the normal H27*, not merely a coset count or a reported equality of group orders.

## Exact central quotient and four-polar-line symmetry

Let `Z=Z(H27)`, order three. It fixes all **13** rays in the polar neighborhood pointwise. On the 27 outer rays its nonidentity generator has **nine disjoint 3-cycles**. These are exact center-orbits, giving a 9-by-3 decomposition:

```
(0,9,29)    (2,13,37)    (3,17,21)
(4,18,31)   (6,19,20)   (7,30,36)
(10,16,39)  (12,15,22)  (27,32,34)
```

The ambient 648-group acts on the nine central cells through a faithful induced group of order **216**, whose point stabilizer has order **24**. The induced image of `H27` has order **9**, is abelian of exponent three, and acts regularly on the nine cells, hence is isomorphic to `F3^2`. It is normal inside the 216-group. This realizes the *finite affine Hesse phase-space structure* as a quotient of the exact Witting ray action, with central phase sheets visible above its nine cells.

Independently, the ambient 648-group permutes the **four isotropic lines** through 25. The induced four-letter permutation group has order **12** with element-order profile `1^1 2^3 3^8`, so it is `A4`, not `S4`. This provides an explicit four-direction and nine-cell comparison: the same rank-three Hessian reflection subgroup contains a four-direction tetrahedral quotient and a nine-cell affine translation quotient.

These statements are group actions and incidence geometries, **not** a proof of four spacetime dimensions, three families, or a Schrödinger time evolution. The nine-by-three rays are **not** 27 mutually orthogonal quantum states.

## Independent relationship to the earlier repo and literature

`analysis/w33_20261011_witting_displacement_firewall.py` already identified a point stabilizer `G25` of order648 and an H27 transverse module. `analysis/2026-10-15_toe92_witting_five.md` also uses an H27 regular address space, but on cubic-surface objects. No discovery of abstract Hessian or Heisenberg groups is claimed here. The new result is an **explicit canonical-ray-index action with direct polar pencil, central phase quotient and single-tunable-phase optical controllability** (the latter in the companion file `analysis/2026-11-22_witting_h27_one_tunable_phase_control.md`).

Hessian groups: [Magma complex reflection tables](https://docs.magma-maths.org/v2.30-1/LieTheory/ReflectionGroups/create-group-refl-complex.html). For contemporary photonic implementation context, a [2026 programmable silicon-photonic U(4) processor](https://www.nature.com/articles/s41467-026-74936-7) uses MZI networks; our abstract control theorem does **not** establish lower hardware component count or superior efficiency. A [2026 heralded photonic ququart–ququart gate](https://www.nature.com/articles/s41566-026-01846-x) solves a different, heralded two-photon gate problem; it cannot be replaced by the single-photon Lie theorem here.

## Reproduction

`analysis/toe_20261122_witting_h27_polar_pencil.py`
`analysis/toe_20261122_witting_hessian_quotient_tower.py`

and corresponding `tests/test_toe_20261122_witting_h27_polar_pencil.py`, `tests/test_toe_20261122_witting_hessian_quotient_tower.py`.

Frozen results: `data/toe_20261122_witting_h27_polar_pencil.json`, `data/toe_20261122_witting_hessian_quotient_tower.json`. Together with the preceding three proofs, the whole independent five-script stack passed **12 focused server-side tests**. GitHub Actions `.github/workflows/witting-h27-controllability.yml` contains the replay specification. The current remote CI completion state requires separate checking. Windows local checkout was **not synchronized** because Remote Desktop Commander reports its monthly usage ceiling exhausted.

## Physics firewall

No physical clock, graviton, observed gauge boson, chiral fermion or quantum advantage is deduced from these finite counts. Deriving a TOE would require a specified dynamical action, Lorentzian/causal continuum construction, chiral anomaly-free matter, empirical low-energy predictions and reproducible experiments. The exact finite symmetry is a candidate building block, not a replacement for those missing constructions.
