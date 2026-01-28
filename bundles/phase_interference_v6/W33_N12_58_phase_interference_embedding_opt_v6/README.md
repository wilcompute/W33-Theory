# W33 ↔ N12_58 phase-aware interference embedding optimization (v6)

This bundle contains a **new improved embedding** (bijection of W33 points 0..39 to N12_58 candidate points)
optimized for a **phase-aware transport + interference objective**.

## Core idea
- Work in W33 = GQ(3,3) with **360 four-center triads**.
- Triad holonomy from C^4 rays yields h ∈ {3,9} (mod 12), corresponding to phase ±i.
- Each 2T cycle step carries delta ∈ {0,2,4,6} (mod 8) and (removed,added) phase-sum subtypes.
- We realize each of the 5 nontrivial 2T cycles as a closed walk in the four-center triad adjacency graph, under the v3 predicate.

## Phase predicate (v3)
- Node constraints:
  - delta=2 ⇒ hol=9
  - delta=6 ⇒ hol=3
- Transition constraints depend on the **previous** edge:
  - delta_prev=0 ⇒ hol(prev)=hol(curr), plus subtype conditions based on removed=add
  - delta_prev=4 ⇒ hol(prev)≠hol(curr), plus a direction constraint for (removed,add)=(6,2)

## Interference model
We evaluate cycles using:
- triad phase factor exp(2πi h/12) ∈ {i,-i}
- delta twist f(0)=-i, f(2)=1, f(4)=1, f(6)=-1
- weight exp(-λ * cover12_indicator), with λ=0.5

The optimizer improved:
- total minimal cover12 cost across 5 cycles: 45
- cover12 count among 360 four-center triads: 286
- global coherence |Σ cycle amps|: 0.43634094602344714

## Files
- w33_to_n12_mapping.csv / n12_to_w33_mapping.csv: the best mapping
- w33_four_center_triads_table.csv: all 360 four-center triads with holonomy and cover statistics
- phase_aware_interference_witness_walks.csv: step-by-step verified closed-walk witnesses for the 5 cycles
- run_summary.json: metrics and predicate definitions
