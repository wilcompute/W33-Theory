# Pass 1419 — Cross-manuscript claim audit and evidence firewall

## Scope

This audit compares the current opening claims of `w33_paper.tex` and
`photonic_holonet.tex` against the exact finite results through Passes 1416–1418
and against the operational definitions used in the external literature.

The audit is not a stylistic objection.  It asks, claim by claim, whether the
repository contains an executable finite theorem, an engineering specification,
an experimental protocol, or a physical derivation.

## Result

The two manuscripts currently use different evidence standards.

### `w33_paper.tex`

The current abstract is reviewer-safe.  It calls the work an evidence-tiered
research atlas, separates exact finite results from conditional physical
selection arguments, and states explicitly that no current result derives the
Standard Model, measured masses or couplings, spacetime dynamics, or cosmology
from `W(3,3)` without additional assumptions.

### `photonic_holonet.tex`

The current abstract still opens with all of the following stronger assertions:

- a “complete, machine-verified architecture” for a universal computer carried
  by one self-entangled photon;
- “Every architectural layer is a theorem with an executable witness”;
- a matter shell that is “exactly the magic sector,” with “contextual fraction
  `1/10`”;
- a triply forced `q=3`;
- Standard-Model descent, three generations, PMNS and gauge-unification claims;
- inflationary and proton-decay predictions;
- “No fitted parameters appear anywhere.”

Those sentences do not follow from the finite theorem spine presently certified
in the repository.

## Exact finite layer that can be promoted

The following statements are now exact and executable:

1. `W(3,3)` has 40 points, 40 isotropic lines, 240 collinearity edges, and 540
   unordered pairs of disjoint isotropic lines (“frames”).
2. Each frame carries one canonical four-edge cross-matching invariant under its
   full order-48 stabilizer.  The 540 matchings cover every W33 edge exactly nine
   times.
3. The 540-by-240 matching matrix `M` has rational rank 225 and Smith cokernel
   `Z^15 + (Z/2)^30`.
4. With `N` the unsigned point-edge incidence, `d` the oriented incidence, `A`
   the W33 adjacency matrix, and `K` the signed-turn operator,

   `K d^T = d^T (6I-A)`.

   If `P=(A-12I)(A-2I)=96 E_{-4}`, then

   `F = d^T P N / 16`

   is integral, annihilates the matching image, has rational rank 15, and lands
   exactly in `ker(K-10I)`.  It therefore gives an explicit equivariant
   isomorphism

   `coker(M) tensor Q  ->  ker(K-10I)`.
5. Modulo 2, the same bridge has rank 14 and square zero.  It geometrically
   separates the two abstractly isomorphic 14-dimensional composition factors:
   one is the nontrivial reduction of the rational 15-dimensional bridge, while
   the second lies in the 31-dimensional torsion-side kernel.
6. The exact-cover space has at least five stabilizer types

   `C2, C4, C2xC2, D8, C4xC2`.

   Sixteen deterministic `C2` cover orbits plus four further stabilizer types
   certify at least 226,800 distinct covers.  A `C2` cover fixes 12 selected
   frames, so the earlier “cover stabilizers are diagonal” observation is not
   universal.

## Claims that remain engineering specifications, not physical theorems

The following can be retained as explicit design proposals, provided they are
not called experimentally established or physically complete:

- the 540-chart routing atlas;
- packet, cache, and compiler counts;
- recursive `40^n` address scaling;
- sparse analyzer matrices;
- proposed time-bin, OAM, path, and polarization encodings;
- finite Clifford-generation calculations.

A finite gate-group closure proves a property of the abstract control algebra.
It does not by itself prove preparation fidelity, loss tolerance, detector
requirements, fault thresholds, scalable feed-forward, or universal physical
computation by one photon.

## Claims that require an operational experiment before promotion

### Contextual fraction

In the standard resource-theoretic definition, contextual fraction is a number
attached to an empirical probability model and is obtained by a linear program.
It is not automatically the ratio of four unsatisfied rays to forty rays.
Accordingly,

`4/40 = 1/10`

is presently a finite deficit ratio.  To call it an experimental contextual
fraction, the manuscript must specify contexts, outcomes, probabilities, the
noncontextual polytope, the linear program, noise treatment, and the witness
inequality.

### Contextuality as magic

The theorem that contextuality supplies magic applies within a specified
stabilizer/magic-state computational framework.  A contextual finite geometry is
not automatically a distillable magic state, nor does a contextuality count by
itself prove universality.

### Pump Chern number

An integer assigned to an abstract band model becomes an experimental Chern
number only after the Hamiltonian, gap, adiabatic cycle, observable, state
preparation, and robustness window are specified and measured.

## Claims that must remain explicitly conditional

The following are hypotheses or phenomenological correspondences, not outputs of
the exact finite model:

- `q=3` is physically forced;
- `E6` descends to the observed Standard Model in the proposed way;
- three generations, CKM/PMNS values, masses, couplings, and the fine-structure
  constant are derived without fitting;
- inflationary observables and proton lifetime follow from the substrate;
- the finite architecture is literally a model of spacetime or cosmology.

The evidence-tiered language already used by `w33_paper.tex` should govern these
claims in `photonic_holonet.tex` as well.

## Literature anchors checked

- Knill–Laflamme–Milburn, *Nature* 409 (2001): scalable linear-optical quantum
  computation uses beam splitters and phase shifters together with single-photon
  sources and photodetectors; this is a concrete physical resource model, not
  merely finite group closure.
- Howard–Wallman–Veitch–Emerson, *Nature* 510 (2014): contextuality supplies
  magic in a specified fault-tolerant magic-state framework.
- Abramsky–Barbosa–Mansfield, *Physical Review Letters* 119 (2017): contextual
  fraction is defined for empirical probability tables and computed by linear
  programming.
- CTblLib/ATLAS distinguishes `U4(2)=PSp(4,3)`, `U4(2).2`, and
  `2.U4(2)=Sp(4,3)`; equal group orders do not justify conflating their actions.
- Signed-line-graph literature treats the oriented incidence/sign choice as
  structural.  This supports the exact Pass 1416 correction: the K-operator
  uses the signed edge action, whereas the frame matching uses the unsigned edge
  action.

## Promotion decision

Promote the Pass 1416 finite bridge and the Pass 1417/1418 corrections into both
manuscripts through one shared TeX source.  In the Holonet, place the shared
insert immediately after the table of contents so readers encounter the evidence
boundary before the architecture and physics claims.
