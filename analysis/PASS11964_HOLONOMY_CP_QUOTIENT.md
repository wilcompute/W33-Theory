# Pass11964: a lower-energy flat connection need not break conjugation

TOE57's finite spinless-fermion model destabilizes trivial holonomy. Its
survey does not identify whether the lower-energy connection and its complex
conjugate belong to different vertex-gauge orbits. This pass supplies that
test and searches the actual three-dimensional compact holonomy torus.

## Exact criterion

On a connected graph, fix a spanning tree. Vertex gauge transformations can
make every tree-link phase zero; each remaining chord phase is a fundamental
Wilson-loop phase. Thus a connection U is gauge equivalent to U* exactly
when every fundamental Wilson loop is real, W=+1 or -1. Necessity follows
from gauge invariance of loop products. Sufficiency follows because in tree
gauge all remaining links are real as well. This criterion allows arbitrary
vertex gauge transformations, without a graph relabeling.

The native three-deck marking in
[TOE38](w33_20261010_toe38_local_maxwell_2complex.py) puts the three unit
voltages on three fundamental chords. Therefore phase vectors phi_i=0 or pi
modulo2pi are conjugation fixed. A nonzero phi is not sufficient for symmetry
breaking. The flux at (pi,pi,pi) is a real sign connection with nontrivial
global Wilson loops and zero selected local plaquette flux.

## Computed finite-model result

Using the same beta=4, mu=0, unit-hopping 80-site spinless fermion model as
[TOE57](w33_20261013_toe57_fermion_holonomy.py):

| Connection | Grand free energy |
|---|---:|
| trivial | -67.98702449745932 |
| three pi twists | -68.80381817641133 |

The three-pi candidate is exactly conjugation fixed. Its analytic spectral
Hessian has positive eigenvalues 0.0994539938, 0.1039174656, 0.1082647551;
the gradient vanishes to numerical precision. An independent centered
finite-difference Hessian agrees within 3.78e-7. The spectral formula uses
the divided difference of the Fermi occupation, with its derivative at
degenerate eigenvalues, rather than differentiating eigenvector labels.

Eight corner starts and24 fixed-seed random starts found no energy below
the three-pi corner beyond 1.5e-14 numerical noise. Several optimizer calls
reported precision-loss failures; those flags remain in the certificate.
This is a multistart survey and positive local-stability check, not a
certified global-minimum theorem. A separate genuinely complex connection
provides a positive control: its nonreal Wilson loops survive arbitrary
vertex gauge transformations.

## Consequence and limits

The fermionic holonomy instability demonstrated by TOE57 admits a strictly
stable, lower-energy conjugation-fixed candidate. It therefore does not by
itself supply the CP-breaking phase required by the flavour constructions.
This result adds a gauge-orbit diagnostic; it does not retract TOE57's
negative curvature or lower-energy samples.

Conjugation of a spinless hopping model is an antiunitary operation. Calling
it physical CP would require a specified spatial-parity action, charge
conjugation on all matter, a chiral field content, and a dynamical vacuum.
Those objects are absent here. The finite compact torus is not a
thermodynamic spontaneous-symmetry-breaking limit. Graph automorphisms
could further identify connections; no such generalized symmetry was
needed to identify this real-sign candidate.

Flux-phase selection is established prior art. [Lieb1994](https://arxiv.org/abs/cond-mat/9410025)
proves results under specific geometric hypotheses; we do not apply its
global theorem to this nonplanar marked W33 graph. The contribution here is
the explicit quotient diagnostic and finite-model stability calculation.

Artifacts: [producer](w33_pass11964_holonomy_cp_quotient.py),
[certificate](../data/w33_pass11964_holonomy_cp_quotient.json),
[regressions](../tests/test_w33_pass11964_holonomy_cp_quotient.py).
