# Round 17 — Exact two-boson interaction-trace certificate (2026-10-09)

Scope: exact finite-algebra proof of pairwise inequivalent interacting Hamiltonian families for a rational-phase W33 Levi-graph experiment. Not a preferred vacuum, physical device, or solved TOE.

## Inputs and provenance
- The complete 150-page papers/forty_points/main.pdf was text-extracted (460,446 characters); Sections 2–4, 9–11 frame exact geometry, quantum interpretation, and missing dynamics. The paper explicitly does not claim a complete physical theory.
- Five W33 optimal three-flag selector representatives are from data/w33_20261009_PSp_orbits_isotropic_triplets.json, in native order:
  [0,52,68], [0,52,72], [0,52,70], [0,52,74], [0,52,90].
- Round14 proved exact full-band one-particle Peierls isospectrality; Round16 numerically detected two-boson onsite-interaction orbit splitting with residual certificates. Producer files: analysis/w33_20261009_round16_two_boson_hubbard_orbits.py and analysis/w33_20261009_round16_two_boson_verified_splitting.py.
- Prior art: J. K. Gamble et al., Phys. Rev. A 81, 052313 (2010), DOI 10.1103/PhysRevA.81.052313, interacting two-particle walks discriminate some noninteracting-indistinguishable graph structures. Do not claim novelty for this general effect.

## Exact algebra
For any Hermitian 80x80 single-particle adjacency A, let D=dGamma(A) on Sym^2(C^80), let P be the 80-dimensional onsite doublon projector, and set H(U)=D+UP on the 3240-dimensional symmetric boson Hilbert space. Define

G_n(x,y) = <xx|D^n|yy> = sum(k=0..n) binom(n,k) (A^k)_{xy} (A^{n-k})_{xy}.

Then exact cyclic trace expansion yields

[U] Tr(H(U)^N) = N tr(G_{N-1}),
[U^2] Tr(H(U)^N) = N/2 sum(a=0..N-2) tr(G_a G_{N-2-a}).

The 80x80 formulas replace diagonalization of the 3240x3240 operator. Regression tests compare G_n against direct symmetric-boson matrices and independently enumerate all words containing exactly two P insertions.

The Levi graph is bipartite, with a staggered sign C satisfying CAC=-A. On Sym^2 the involution J=C tensor C obeys JDJ=-D, JPJ=P, and JH(U)J=-H(-U). Hence odd moments contain only odd powers of U.

## Rational phases and finite-field certificate
The selected three oriented Levi flags receive rational unit phases:
z1=(15+8i)/17, z2=(4-3i)/5, z3=(5+12i)/13,
and reverse hops receive their complex conjugates. All entries lie in Q(i).

Map the calculations to F_p[i]=F_p[t]/(t^2+1) at p=1000003 and p=1000033. These are prime and neither divides the denominators. A nonzero modular difference therefore proves a nonzero characteristic-zero rational Gaussian coefficient.

For p=1000003, the five native-orbit coefficient vectors:
- [U]Tr(H^17): 378712, 378712, 771233, 660083, 489862.
- [U]Tr(H^19): 445581, 600249, 263943, 671828, 115030.
- [U^2]Tr(H^18): 519536, 519536, 640932, 475300, 103186.

For p=1000033:
- [U]Tr(H^17): 714549, 714549, 795646, 489917, 20245.
- [U]Tr(H^19): 687939, 842535, 790909, 732697, 823449.
- [U^2]Tr(H^18): 725087, 725087, 801880, 147219, 408949.

The paired (N=17,N=19) signatures are distinct for all five orbits at each prime. Therefore every pair of the five interacting Hamiltonian families has different trace polynomials as functions of U over Q(i). The first detected nonconstant U-linear order was 17. The scan also found identical one-body traces across all five through order 32 over both primes; modular equality alone does not prove exact equality over Q(i) and the full exact isospectrality comes from Round14.

Boundaries: The certificate does not establish five-way separation at EVERY fixed nonzero U, nor exact eigenvalues at the original Round16 floating phase choice. It proves a stronger-than-numerical orbit-sensitive trace invariant under an explicitly externally chosen phase assignment, NOT dynamical selection of the phases or spacetime. High-order physical spectroscopy and an actual nonlinear photonic interaction remain needed.

## Reproduction
From C:/Repos/Theory of Everything:
1. python analysis/w33_20261009_round17_interaction_trace_certificate.py
2. set process environment W33_TRACE_MOD=1000033; rerun the producer
3. python -m pytest -q tests/test_w33_20261009_round17_interaction_trace_certificate.py

The dedicated producer, its two JSONs, test, and report are deliberately isolated from concurrent agent work.
