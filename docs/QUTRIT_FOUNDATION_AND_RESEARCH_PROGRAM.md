# Qutrit Foundation And Research Program

This note records the strongest exact mathematical spine currently present in the
repository, separates it from the speculative physics layer, and states the most
credible route for pushing the theory forward.

> Status note: this is a focused internal research note on the qutrit spine. For
> the live public status surfaces, use [docs/index.html#current-synthesis](./index.html#current-synthesis),
> [docs/qutrit_foundation.html](./qutrit_foundation.html), and
> [docs/repo_frontier_audit.html](./repo_frontier_audit.html).

## Context Map

| File | Role in the theory spine |
| --- | --- |
| `docs/index.html` | Live public shell map: exact qutrit kernel first, promoted global closure after that. |
| `docs/qutrit_foundation.html` | Public theorem-boundary page for the exact qutrit/Heisenberg/local-`E6` core. |
| `docs/repo_frontier_audit.html` | Repo-wide evidence map and current exactness boundary. |
| `W36_PAPER.tex` | Public manuscript. Contains later spectral and physics claims, but only a compressed qutrit/phase-space account. |
| `scripts/w33_two_qutrit_pauli.py` | Global theorem: `W(3,3)` is the commutation graph of the `40` projective non-identity two-qutrit Pauli operators. |
| `scripts/w33_heisenberg_qutrit.py` | Local theorem: for every base vertex, the `27` non-neighbors form an `F_3^3` Heisenberg shell and the `12` neighbors split into `4` MUB classes. |
| `scripts/w33_exact_lie_bridge_audit.py` | Conservative audit separating exact local `E6` consequences from later promoted `E8` closure claims. |
| `tests/test_e8_embedding.py` | Locks the two-qutrit Pauli commutation model, the SRG parameters, and the `40` maximal commuting sets into tests. |
| `tests/test_heisenberg_qutrit_structure.py` | Locks the local Heisenberg/MUB shell and its emitted JSON checks into tests. |
| `tests/test_w33_exact_lie_bridge_audit.py` | Locks the local `1296/648` symmetry package and the exact-vs-nonfunctorial boundary on the Lie side. |
| `data/gq33_so10_literature.md` | Literature audit. Confirms the two-qutrit/W(3,3) connection is real and that no direct `SO(10)` or full-GUT derivation is established in the literature. |
| `exploration/ALGEBRA_REVIEW_AND_VOGEL_ROUTE_2026_03_09.md` | Internal strategic note. Already identifies the qutrit and Heisenberg ladder as the main route worth pushing. |

## What Is Exact

### 1. Global two-qutrit Pauli geometry

The cleanest exact statement in the repo is:

- The `40` vertices of `W(3,3)` are the `40` projective non-identity two-qutrit
  Pauli operators `X^a Z^b x X^c Z^d`.
- Two vertices are adjacent if and only if the corresponding Pauli operators
  commute.
- The commutation rule is exactly the vanishing of the standard symplectic form
  on `F_3^4`.
- The graph is therefore the finite symplectic polar space `W(3,3)` viewed as a
  Pauli commutation geometry.

Repository evidence:

- `scripts/w33_two_qutrit_pauli.py` builds the operators explicitly and checks
  matrix commutation against the symplectic form.
- `tests/test_e8_embedding.py` verifies the same model directly.

This is the strongest quantum-mechanical statement in the repo because it is not
numerology: it is an explicit operator model.

### 2. Local Heisenberg and MUB shell

For every base vertex `v0`:

- The `12` neighbors `N12(v0)` split into `4` disjoint triangles.
- Those `4` triangles act as `4` striations, i.e. `4` mutually unbiased basis
  classes for the local qutrit shell.
- The `27` non-neighbors `H27(v0)` admit an `F_3^3` coordinatization with
  `9` fibers of size `3`.
- The derived `27`-vertex graph is the Schlafli graph `SRG(27,16,10,8)`.

Repository evidence:

- `scripts/w33_heisenberg_qutrit.py`
- `tests/test_heisenberg_qutrit_structure.py`

This is the strongest local structural theorem in the repo. It gives a real
finite quantum-information shell around every vertex, not merely a graph count.

### 3. Literature-backed external anchor

The repo's literature audit already reaches the right conclusion:

- Planat-Saniga and related papers support the identification of `W(3,3)` with
  the two-qutrit Pauli commutation geometry.
- The factor group of the two-qutrit Pauli group over its center generates the
  `40`-point symplectic polar space.
- There is no comparable external support for a direct `SO(10)` or full
  Standard-Model derivation from `W(3,3)`.

So the two-qutrit foundation is real. The direct high-energy physics closure is
not yet externally established.

## What Is Strong But Still Internal

The following structures are exact inside the repo, but still need a cleaner
independent mathematical write-up before they should be treated as public
foundations:

- The `GF(2)` chain-complex and homology/code layer.
- The `120/240` lift, quotient closure, and line-sector transport machinery.
- The `H^3` and non-isotropic-line module identifications.
- The various transfer operators and mode decompositions.
- The qutrit CSS code interpretation.

These may well be correct, but they are currently one step less mature than the
Pauli and Heisenberg statements because the latter are already standard finite
quantum geometry, while the former are more repo-specific constructions.

## Which Lie Bridges Are Exact

The strongest Lie-theoretic bridge currently supported by the repo is local and
E6-side, not global and E8-side.

### Exact local E6 bridge

- For each base vertex, the derived `27`-vertex graph on the shell is the
  Schlafli graph `SRG(27,16,10,8)`.
- Classically, this is the `27`-line cubic-surface geometry controlled by the
  Weyl group `W(E6)`.
- The qutrit shell keeps its exact `9+9+9` fiber split, so the E6 seam sits on
  top of a concrete Heisenberg/MUB structure rather than a bare count.
- The tritangent count splits as `45 = 36 + 9`, where the `9` missing pieces are
  exactly the Heisenberg center cosets.

### Exact symplectic symmetry data

- The repo's projective symplectic transvections act transitively on the `40`
  points and `240` edges of `W(3,3)`, giving the exact `25920`-element
  projective symplectic subgroup.
- The full collinearity-graph automorphism group is the order-`51840`
  extension obtained by adjoining an anti-symplectic similitude.
- At a base vertex, the full graph stabilizer has order `1296` and restricts
  faithfully to the local `H27` shell, where it preserves the full `45 = 36 + 9`
  tritangent decomposition.
- The projective symplectic-visible part of that local action is the exact
  order-`648` index-`2` subgroup.
- Thus the strongest exact local symmetry statement is not merely a count:
  it is the transported `1296/648` local symmetry package on the cubic-surface
  `27`-line shell.

### Not yet functorial from the qutrit kernel alone

- `|E(W(3,3))| = 240 = |Phi(E8)|` is a real identity of counts, but it is not
  yet a canonical derivation of the `E8` root system from the qutrit kernel by
  itself.
- The later `248` appearing in spectral expansions is a downstream spectral
  closure statement, not yet a local qutrit theorem.
- So the current honest boundary is:

  - local `E6` bridge: exact,
  - global `E8` closure: suggestive but not yet functorial.

## What Is Not Yet Derived

At present, the repository does not honestly have a derivation of all physics.
The missing ingredients are structural, not cosmetic:

- No canonical Hamiltonian or action principle has been derived from the qutrit
  shell alone.
- No controlled continuum or scaling limit has been established.
- No renormalization procedure turns the finite object into a field theory with
  measured couplings.
- No symmetry-breaking mechanism has been derived from the Pauli/Heisenberg data
  in a way that uniquely produces the Standard Model.
- The arithmetic coincidences involving `E6`, `E8`, moonshine, Yukawa ratios,
  and coupling constants are therefore clues or conjectural bridges, not yet a
  closed derivation.

This does not weaken the exact finite geometry. It only marks the current proof
boundary.

## The Most Credible Research Program

The most disciplined route forward is:

1. Promote the qutrit foundation to the front of the public theory.

   The Pauli commutation model and the local Heisenberg/MUB shell should appear
   before any grand-physics claims. That is the actual kernel.

2. Build the operator algebra before extracting constants.

   The next object should be an exact operator package:

   - observables,
   - commutator and central extension,
   - Clifford/symplectic action,
   - transfer operators,
   - and a canonical Dirac/Hamiltonian candidate.

   Physics cannot be claimed until this layer exists in a closed form.

3. Construct a scaling family.

   If the theory is physical, it should survive in a family such as:

   - `W(3,q)`,
   - higher-rank `W(2n-1,q)`,
   - or regular covers/coarse-grainings of the current quotient geometry.

   Without a family, there is no honest continuum program.

4. Derive observables from invariant operator data only.

   Dimensionless quantities should come from spectral invariants, representation
   data, or transport phases that remain meaningful across the scaling family.
   Constant-matching should be the last step, not the first.

5. Keep the algebraic ladder narrow.

   The current repo note in `exploration/ALGEBRA_REVIEW_AND_VOGEL_ROUTE_2026_03_09.md`
   is directionally correct:

   `H27 (1 qutrit shell) -> W33 (2 qutrit Pauli geometry) -> Heisenberg/Golay lift -> sl(27)`

   That route is much more credible than trying to force a direct jump from graph
   numerology to a complete particle spectrum.

## Working Thesis

The strongest honest thesis supported by the current repository is:

`W(3,3)` is an exact finite quantum-information kernel built from the
two-qutrit Pauli commutation geometry, and its local Heisenberg/MUB shell is
the correct starting point for any future derivation of higher algebraic or
physical structure.

That is already substantial. It is not yet the same thing as a finished theory
of all physics.

## Immediate Next Targets

If the goal is to make real progress rather than add more coincidences, the next
targets should be:

- Write a single clean theorem package for the two-qutrit and Heisenberg core.
- Derive a canonical operator algebra and Hamiltonian candidate from that core.
- Prove which later `E6/E8` bridges are functorial consequences and which are
  only numerical alignments.
- Build a scaling family and track which invariants survive it.

Until that is done, the repo should be understood as containing a genuine finite
geometry kernel plus a large speculative physics superstructure built on top of
it.
