# Passes 1971–1975 — reconciliation, scalable auditing, proof promotion, and bounded engineering

The five fronts close with **45/45** frozen checks.

## 1971 — the two treatments reconciled

The standalone note and referee draft agree after one explicit withdrawal. The
45 spread-pair frames are independent but **not maximal independent**: fifteen
residual candidate frames are individually nonadjacent to the seed. The exact
obstruction is support deficiency—those candidates collectively meet only 20 of
60 residual edges, so 40 residual edges cannot be covered and no 60-frame exact
cover extends the seed.

The exact `25,920 -> 807` group-orbit reduction is retained, while the inference
to solver performance is withdrawn. The actual combined fixed-search trees have
451,460 and 512,714 branches, against 60,909 for spread branching alone.

## 1972 — scalable constraint auditing

`scripts/constraint_audit.py` now has separate scopes:

- complete enumeration only for small terminating models;
- named rejected/surviving feasible-witness certificates;
- exact audits of explicitly supplied finite feasible orbits;
- serialized model-growth assertions.

The full 540-variable solution set is no longer approximated by truncated
enumeration. Witness and orbit audits do not claim a global solution count or a
runtime prediction.

## 1973 — solver stagnation diagnosed

Spread branching remains the best frozen configuration. Combined 8- and
40-generator models require 7.412 and 8.418 times more branches. Their conflict
densities are only 0.1307 and 0.1326 per thousand branches, versus 17.0747 for
spread search. The measured behaviour is a propagation-horizon mismatch:
spread aggregates are committed early while frame-level lex constraints become
informative late.

The recommended architecture is to canonicalise search cubes outside the solver
and retain spread-first branching inside each canonical cube.

## 1974 — the surviving spread proofs

Uniformly, spread pairs form an independent seed and leave
`(q^2+1)q(q+1)/2` internal spread-line edges.

For any spread carrying a fixed-point-free linewise involution `sigma`, residual
candidates are exactly `{A,sigma(A)}`. Therefore:

- candidates: `q(q^2+1)/2`;
- supported residual edges: `(q^2+1)(q+1)/2`;
- support fraction: `1/q`;
- multiplicity: `q`.

A nonsquare similitude `g^2=mu I` constructs the involution for the associated
Desarguesian symplectic spread for every odd `q`. Existence and uniqueness for
every arbitrary symplectic spread remain open; uniqueness is exact at `q=3`.

## 1975 — claim ledger and engineering implications

`analysis/W33_CLAIM_STATUS_LEDGER.md` consolidates 32 claims and their current
status. Charge, homological flux, QCD colour, generation, and neutrino readings
remain withdrawn.

The surviving physics statement is representation-theoretic: the unique
Eisenstein `C6` phase is confined to the coexact 90 under equivariant linear
maps and is inverted by chirality, producing a `D12` phase normalizer.

Five bounded engineering directions are recorded:

1. FPGA/ASIC spread-signature canonicaliser outside the solver;
2. cube-and-conquer with geometric deduplication and group tags;
3. 240-bit exact-cover accelerator;
4. exact/harmonic/coexact three-plane controller architecture;
5. isolated six-phase calibration domain with explicit interfaces.

These are design proposals, not a particle model, a physical device claim, or a
proof of `chi(H)=9`.
