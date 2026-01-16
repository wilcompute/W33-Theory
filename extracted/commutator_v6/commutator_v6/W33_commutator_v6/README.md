# W33 four-center transport: commutator phase + flip-pair tie-in (v6)

This bundle computes a *gauge-invariant* phase observable on the W33 (GQ(3,3)) ray realization
and connects it to the N12_58 flip audit's (removed_pairs -> added_pairs) matchings.

## A. The gauge-invariant "2-step commutator phase" (Bargmann 4-cycle)

For a directed move between two adjacent four-center triads:

  T = {a,b,c}  ->  T' = {a,b,d}

(they share exactly two points {a,b} and swap c -> d)

define the Bargmann 4-cycle phase

  Phi(T -> T') = arg( <c|a><a|d><d|b><b|c> )

Quantized to Z12:

  comm_k4_mod12 = k(c,a)+k(a,d)+k(d,b)+k(b,c)  (mod 12)

This is gauge-invariant under |x> -> e^{i theta_x} |x> because it is a closed loop.

### Computed fact (from your C^4 rays)
For *every* directed adjacency move between four-center triads in W33:

  comm_k4_mod12 == 6

i.e. Phi == pi, the commutator phase is exactly -1.

Interpretation: every elementary "triad swap" carries a built-in fermionic (-1) commutator.

See: `w33_four_center_triad_moves_directed.csv` and `commutator_phase_summary.json`.

## B. How this ties to removed_pairs/added_pairs (N12_58 flip audit)

Each N12 flip edge has:
- a 4-support set S = {s0,s1,s2,s3}
- removed_pairs = a perfect matching on S (two disjoint pairs)
- added_pairs   = another perfect matching on S

We canonicalize the three matchings on sorted S as indices:
  0: (s0,s1)(s2,s3)
  1: (s0,s2)(s1,s3)
  2: (s0,s3)(s1,s2)

So each flip edge is a class "rem_idx -> add_idx".

Inside the W33 four-center transport picture, each *nontrivial* step in a witness walk is a move
between two triads in the same K4 component (same outer_quad line of centers). Such a move
is characterized by WHICH of the triad's 3 points gets dropped (drop_idx in sorted order).

Empirically (from the v3 phase-aware witnesses):
- certain (rem_idx -> add_idx, delta) classes are highly predictive of drop_idx.
This gives a direct bridge: the matching-change type tells you which W33 transport port is used.

See:
- `phase_aware_v3_witness_enriched_with_commutator.csv`
- `flipclass_to_dropidx_stats.csv`
- `flipclass_delta_to_dropidx_stats.csv`
- crosstabs.

## Files

- w33_four_center_triads.csv
- w33_four_center_triad_moves_directed.csv
- phase_aware_v3_witness_enriched_with_commutator.csv
- flipclass_to_dropidx_stats.csv
- flipclass_delta_to_dropidx_stats.csv
- crosstab_*.csv
