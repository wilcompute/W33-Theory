# W33 Bundle Spectral Seed

## Honest status

The repo already established the key obstruction:

- the plain 40-vertex Bose-Mesner algebra of W(3,3) is commutative,
- so W(3,3) by itself is not the Connes internal algebra.

That obstruction remains correct.

The right next step is therefore not to keep forcing `C + H + M3(C)` out of the vertex commutant. The right next step is to move to the exact enriched geometry that the repo already built:

- the 45-point quotient transport graph,
- the native A2 rank-2 local system on the standard transport sector,
- the exact local S3 line matching on transport edges,
- the qutrit / Heisenberg color sector.

## What was added

The new script `exploration/w33_bundle_spectral_seed.py` upgrades the earlier 6x6 toy block into a genuine bundle object over the exact 45-point quotient transport graph.

The local fiber is

`C + H + M3(C)`

represented on

`C + C^2 + C^3`.

Concretely:

1. Scalar block
   - the scalar line is trivial.

2. Shell block
   - the shell sector is carried by the exact A2 local system already proved in the repo.
   - transport edges act by exact Weyl(A2) matrices.
   - conjugating the local quaternion generators by shell transport preserves the quaternion relations, so the shell sector is a genuine quaternionic algebra bundle rather than a single fixed copy of `H`.

3. Color block
   - the color sector is carried by the exact S3 permutation action on the three local line states.
   - this preserves the full `M3(C)` color algebra by conjugation.

## Fiber metric and transport

A positive fiber metric is built as

`diag(1, A2, I3)`

where `A2` is the exact A2 Cartan form and `I3` is the standard color metric.

With respect to this metric:

- every local transport block is metric-unitary,
- reverse transport is the metric adjoint of forward transport,
- the resulting global bundle transport operator is G-self-adjoint.

So the bundle transport is not formal window dressing. It is compatible with a positive inner product on the exact bundle.

## Real even spectral seed

The script then builds a candidate bundle-level real even spectral seed:

- Hilbert space: sections of the 45-point bundle with local fiber `C + C^2 + C^3`,
- grading: `gamma = diag(1, -I2, -I3)` fiberwise,
- real structure: complex conjugation `J`,
- Dirac seed: exact bundle transport operator plus a local on-site seed block.

The script checks that:

- `J^2 = 1`,
- `J` commutes with `gamma`,
- `J` commutes with the real bundle Dirac seed,
- the bundle Dirac seed is G-self-adjoint.

This is not yet the full Connes package, but it is a real bundle-level spectral seed rather than a toy isolated matrix.

## Parallel fixed sector

A useful structural result also drops out immediately.

The common transport-fixed fiber sector has dimensions

- scalar fixed dimension = 1,
- shell fixed dimension = 0,
- color fixed dimension = 1,
- total fixed dimension = 2.

So only two parallel singlets survive globally:

- the scalar singlet,
- the democratic color singlet.

The shell doublet and the nontrivial color sector are genuinely twisted by transport.

That is exactly the kind of geometry-first behavior we wanted: the nontrivial internal sectors live as bundle data, not as globally constant commuting scalars.

## Why this matters

This is the first honest step beyond the vertex obstruction that still stays entirely inside repo-native geometry.

Instead of claiming that the 40-vertex algebra already is `C + H + M3(C)`, the new construction says:

- the correct internal algebraic shape appears fiberwise on the exact enriched transport bundle,
- transport glues those local algebras nontrivially over the 45-point quotient geometry,
- the resulting object already carries a real, metric-compatible spectral seed.

That is a serious upgrade in mathematical honesty and in actual structure.

## What this still does not prove

This new object is still a seed, not the finished spectral triple.

Open items remain:

1. first-order condition,
2. full KO-dimension sign table,
3. the precise algebra of admissible bundle sections,
4. the final finite Dirac operator with the correct physical couplings,
5. the full spectral action.

Those are still hard problems.

## Bottom line

The repo now has:

- the April 9 obstruction on the plain vertex algebra,
- the path-space algebra bridge `C + H + M3(C)` at the local level,
- and now a genuine bundle-level real spectral seed over the exact 45-point quotient transport geometry.

That is the cleanest, most honest route forward yet.
