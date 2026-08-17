# Passes 7017–7024 — the full-group 27↔40 linear bridge is trivial

## Executive result

The repo already contains explicit, generator-level realizations of the same inner group

\[
G=PSp(4,3),\qquad |G|=25920,
\]

on both carriers of interest:

- the 40 points of `W(3,3)`, a rank-three action with subdegrees `1,12,27`;
- the 27-point Schläfli carrier, independently reconstructed as a rank-three action with subdegrees `1,10,16`.

This is enough to decide the characteristic-zero full-group linear transport problem exactly.

The answer is a no-go:

\[
\boxed{\dim \operatorname{Hom}_{G}(\mathbb C^{27},\mathbb C^{40})=1}.
\]

The unique channel is the trivial constant channel.  Therefore there is **no nonconstant full-`PSp(4,3)`-equivariant linear map** carrying Schläfli 27 data into W33 40-point data, or conversely.

## Pass7017 — the W33 permutation module

The W33 point graph is

\[
SRG(40,12,2,4),
\]

with spectrum

\[
12^1\oplus2^{24}\oplus(-4)^{15}.
\]

Because the action is transitive of rank three, its complex permutation module is multiplicity-free with three irreducible constituents.  Hence

\[
\boxed{\mathbb C^{40}\cong \mathbf1\oplus V_{24}\oplus V_{15}}.
\]

This is a representation-theoretic statement about the finite group action; no physical interpretation of the 15- or 24-dimensional constituents is used here.

## Pass7018 — the Schläfli permutation module

The repo's independently reconstructed PSp action on the 27 Schläfli vertices has subdegrees

\[
1,10,16,
\]

and its degree-16 orbital graph is

\[
SRG(27,16,10,8)
\]

with spectrum

\[
16^1\oplus4^6\oplus(-2)^{20}.
\]

Again rank three makes the permutation representation multiplicity-free, so

\[
\boxed{\mathbb C^{27}\cong\mathbf1\oplus V_6\oplus V_{20}}.
\]

The earlier orthogonal-quotient work additionally supplies an explicit graph isomorphism and generator conjugation between this 27-action and the cubic-surface/Schläfli carrier, so this is not a `27=27` cardinality identification.

## Pass7019 — the Hom-space collapses

The two multiplicity-free constituent sets have dimensions

\[
\{1,24,15\},\qquad \{1,6,20\}.
\]

Their only common irreducible is the trivial constituent.  Schur's lemma therefore gives

\[
\operatorname{Hom}_G(\mathbb C^{27},\mathbb C^{40})
\cong\operatorname{Hom}_G(\mathbf1,\mathbf1)
\cong\mathbb C.
\]

Thus every equivariant matrix is proportional to the all-ones map

\[
x\longmapsto \left(\sum_{i=1}^{27}x_i\right)\mathbf1_{40}.
\]

The reverse Hom-space is the same one-dimensional space.

## Pass7020 — the bridge question is now sharper

This closes a recurring ambiguity in the repo.  The 27 and 40 carriers really do share the same finite simple group, but that fact does **not** imply a useful full-group linear intertwiner.

Any nontrivial 27↔40 bridge must therefore do at least one of the following:

1. restrict from `PSp(4,3)` to a proper subgroup, where constituents can branch and overlap;
2. be nonlinear;
3. pass through a larger/intermediate carrier before projecting;
4. work in a modular characteristic where the semisimple characteristic-zero argument no longer applies.

This turns a vague search for “the 27-to-40 map” into four precise alternative programs.

## Pass7021–7024 — boundary

The theorem is characteristic-zero and full-group.  It does **not** rule out modular maps over `F_2` or `F_3`, subgroup-equivariant transports, correspondences of incidence structures, derived functors, nonlinear maps, or maps through the 45-, 36-, 240-, 366-, or other repo carriers.

It does rule out one especially tempting but previously untested possibility: a nonconstant direct linear intertwiner respecting the whole inner `PSp(4,3)` action.
