# Passes 3905–3912 — Terwilliger sieve, 398-port mesh, maximal-code strata, Monster audit, and rank-48 overlap

## Frozen status

`PASS_FIVE_FRONTS_THREE_BONKERS_MESH_EXACT_ZERO_PATTERN_RADICAL_PROMOTION_PENDING`

Semantic certificate:

`de94973500dcf4af824eb34779034e15a6a9260902bf114a81524adff45aeb9b`

This packet executes the five fronts published after Passes 3821–3828 and adds three derived constructions. It preserves the authoritative restored website and does not overlap the active Passes 3887–3904 order-192/unmarked-axial packet.

## 1. Complete arithmetic sieve for the Terwilliger Wedderburn degrees

The rank-five holonomy Terwilliger algebra has exact rational dimension 79 and center dimension 10. If it is split semisimple over Q, its ten matrix degrees `n_i` satisfy

`sum_i n_i^2 = 79`.

Exhausting nondecreasing positive integer solutions gives exactly fourteen degree multisets. They are frozen in the certificate. The largest simple block must have degree between four and eight. This is the complete arithmetic sieve, but it does not select the actual multiset: primitive central idempotents or central-rank traces are still required.

## 2. Symmetry-adapted adjacent mesh: 418 to 398

For `H=(2A36-J)/6`, a new port permutation gives 398 nontrivial adjacent Givens eliminations in 69 disjoint-gate layers, with 232 eliminations skipped because their targets vanish numerically at machine precision. The residual diagonal is `diag(1,...,1,-1)`, so one terminal pi phase completes the candidate.

The prior upper bound was 418 rotations in 69 layers. The new deterministic parameter hash is

`66735cf785b6f8228b9966f3d60d8290c00a2978bcde15f0e8790cce8e457da4`.

The maximum skipped residual is `1.67e-16`, the final off-diagonal residual is `3.61e-16`, and the minimum nonzero pivot is approximately `0.2357`, giving a wide numerical separation. Rational-square parameters are recovered for every nontrivial rotation.

This promotes a reproducible 398-gate algebraic candidate, not yet an exact radical identity. The exact-radical replay remains the promotion gate, and global gate/depth optimality is not claimed. The rigorous lower bounds remain 35 gates and six layers.

## 3. Maximal-code strata and exact enumerator law

The deterministic sampler constructs 258 maximal doubly-even `[36,17]` extensions containing the original `[36,6,16]` character code. It performs 5,551,147 exact GF(2) greedy trials and observes all six values

`t=A4 in {0,1,2,3,4,5}`.

For every maximal extension, maximality implies `A4(C-perp)=A4(C)=t`. Combining this with total size and the MacWilliams dual coefficients at weights two and four gives the complete exact weight enumerator:

- `A4=t`;
- `A8=225+11t`;
- `A12=9555-39t`;
- `A16=55755+27t`;
- and symmetry about weight 18.

Thus the entire enumerator is controlled by one integer.

The 258 samples nevertheless produce 184 distinct weight-eight coordinate-degree profiles. Weight enumerators are therefore extremely coarse orbit invariants: even the dominant `t=0` stratum contains many distinct local incidence profiles.

This is a deterministic stratum sample, not an exhaustive classification of the more than 4.632 quintillion `U4(2):2` orbits.

## 4. External Monster gate remains fail closed

No concrete GAP/CTblLib or `mmgroup` result artifact is present. The gate remains `PENDING`. Promotion requires portable `MM` strings, runtime provenance, exact group order, identification of the two internal standard-pair orbits, the 36-axis action, all 135 frame and 120 Norton hashes, the `[36,6]` code weights, the `45+216+270+120` line split, and a content-addressed character-fusion artifact.

No Monster embedding or character fusion is inferred from the abstract finite-group evidence alone.

## 5. Exact rank-48 cross-carrier overlap theorem

The 64-point quadratic-parent action has orbital-algebra rank 15. The 200-ovoid action has rank 19. Their combined 264-object action has rank 48. Hence

`48 = 15 + 19 + 2 <chi64,chi200>`,

so the cross-Hom dimension is exactly seven.

The 64-carrier has three orbits and the 200-carrier has two, so their trivial constituents contribute six. Exactly one nontrivial shared constituent remains. From the published 200-module decomposition, the only dimension-compatible multiplicity-one constituent is the 15-dimensional module; the 81-dimensional constituent cannot occur in a 64-dimensional module.

Therefore the exact shared sector is

`1^3` together with one 15-dimensional irreducible,

and the 64-module has forced form

`1^3 + 15_b + X^2 + Y`,

where `X,Y` do not occur in the 200-carrier and `2 dim(X)+dim(Y)=46`. Their individual dimensions remain open pending a character-table or primitive-idempotent calculation.

## Bonkers I — one integer controls a 131,072-word code

A maximal code contains 131,072 words, yet its full weight enumerator is determined by the single integer `t=A4`. This converts a huge code census into a one-parameter enumerator family.

## Bonkers II — enumerator collapse versus profile explosion

Only six enumerator strata occur in the deterministic sample, while 184 weight-eight coordinate-degree profiles occur. The ratio exposes a new hierarchy of invariants: weight enumerator, coordinate-degree profile, and full group orbit are successively much finer.

## Bonkers III — a seven-dimensional intertwiner bridge

The exact cross-Hom dimension seven decomposes as six trivial channels plus one genuinely 15-dimensional channel. Thus the 64-point quadratic parent and 200-ovoid geometry share precisely one nontrivial representation-theoretic bridge, sharply narrowing any future objectwise fusion or hardware-channel interpretation.

## Evidence boundary

Proved exactly here: the fourteen-case split Wedderburn degree sieve; the maximal-code enumerator law; the deterministic six-stratum/184-profile sample; the cross-Hom dimension seven and forced shared 15-dimensional constituent; and the fail-closed Monster audit.

Promoted only as a reproducible candidate: the 398-rotation, 69-layer adjacent mesh. Not claimed: the actual Terwilliger block multiset, exact-radical mesh identity, global mesh optimality, exhaustive code-orbit classification, serialized Monster embedding, character fusion, hardware/laboratory result, physical interpretation, or remote CI/PDF success.
