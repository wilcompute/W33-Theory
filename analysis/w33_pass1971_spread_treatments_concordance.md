# Pass 1971 — concordance of the two spread-obstruction treatments

This file compares `analysis/W33_SPREAD_OBSTRUCTION_NOTE.md`, the independent
Passes-1961--1965 review, and `analysis/W33_SPREAD_OBSTRUCTION_REFEREE_DRAFT.tex`.
It is a claim-by-claim reconciliation, not a third narrative.

## Concordance

| claim | standalone note | referee draft | reconciled status |
|---|---|---|---|
| The frame graph is the union of 240 edge-indexed `K9`s | asserted and counted | proposition | **exact at q=3** |
| The 45 pairs of lines of a spread form an independent set | asserted | theorem | **uniform incidence proof** |
| The 45-frame set is maximal independent | asserted | asserted | **withdrawn: false** |
| Fifteen residual candidate frames exist at q=3 | asserted | asserted | **exact for all 36 spreads** |
| The candidates touch only 20 of 60 residual edges | asserted | asserted | **exact for all 36 spreads** |
| A spread seed cannot be completed to a 60-frame exact cover | asserted | asserted | **exact at q=3** |
| Candidate support obeys the `1/q` law | q=3,5,7 verification | q=3,5,7 verification | **proved for every spread carrying the linewise fixed-point-free involution; otherwise finite-case only** |
| `sigma_S` is induced by `g^2=mu I`, `mu` nonsquare | asserted with q=3,5,7 checks | algebraic construction | **proved for the associated Desarguesian symplectic spread; uniqueness only exact at q=3** |
| `chi(H)=9` | open | open | **open** |
| Spread branching is the best measured single encoding | yes | stated | **current benchmark: 60,909 branches** |
| Orbit cuts remove 96.8866% of one known feasible group orbit | absent from old note | stated | **exact orbit statement, not performance evidence** |
| Combining spread branching with 8 or 40 lex generators improves search | tested later | not yet reflected | **refuted: 451,460 and 512,714 branches** |
| The coexact 90 is the unique Eisenstein phase sector | asserted | asserted | **exact representation-theoretic statement** |
| The internal `C6` is charge or homological flux | withdrawn | withdrawn | **withdrawn** |

## The maximality correction

The repeated phrase “the spread `K10` is a maximal independent set” cannot be
true together with the certified residual-candidate census.  Adjacency in the
frame graph means sharing a matching edge.  The spread frames cover precisely
the 180 off-spread edges.  Each of the 15 candidate frames uses only the 60
on-spread residual edges, and is therefore nonadjacent to every spread frame.
Consequently any candidate can be adjoined to the 45-frame independent set.

The correct theorem is stronger in the direction actually needed and weaker in
maximality language:

> The spread frames form a 45-vertex independent seed.  At q=3 it has exactly
> 15 residual candidate extensions, but those candidates collectively meet only
> 20 of the 60 residual edges.  Forty residual edges lie in no candidate, so no
> choice of 15 candidates can complete the seed to a 60-frame exact cover.

Thus the obstruction is a **support-deficiency/completion obstruction**, not a
maximal-independent-set obstruction.

## Solver reconciliation

The Pass-1966/1967 orbit calculation and the Pass-1961/1962 search benchmark are
compatible once their observables are separated:

- exact orbit volume: `25,920 -> 807` under forty spread-signature cuts;
- actual fixed-search tree: `60,909` branches for spread branching alone,
  `451,460` with eight lex generators, and `512,714` with forty.

Orbit-volume reduction is a valid symmetry certificate.  It is not a monotone
proxy for CP-SAT runtime or branch count.  The referee draft must report both.

## Ownership boundary

The general symplectic-spread and regular-spread framework is standard.  The
repository has not located prior art for the exact q=3 `36/270` multiplier split.
The draft therefore keeps “likely known; reference not located” rather than a
novelty claim.  The Gow/Vinroot character-theory ownership and the in-repository
Pass-355 priority remain unchanged.
