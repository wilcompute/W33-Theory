# Pass 12077: dynamics on the clocks chooses E6

Claude track. Replaces the reading withdrawn in 12072.

## Model

The 120 commuting clock involutions act on the 248 as gradings. With rates φ ≥ 0, H(φ) = Σ φ_c (1 − θ_c)/2 is
diagonal, and F_T is concave in φ, so a single clock wins at fixed total rate.

## Results

- **Counting.** Every clock is odd on 112 roots; every root is odd under 56 clocks.
- **Pairs.** There are 3360 Klein pairs (their product is a clock; 72 roots even under both) and 3780 others (64).
  Z₇₂ − Z₆₄ = 8(1 − e^(−1/(2T)))² > 0, so **Klein pairs win at every temperature**.
- **Triples (exhaustive, 280,840).** There are five types. The 1120 Klein triples (40 at one event and 1080 on three
  pairwise non-collinear events) have root pattern (72, 0, 168, 0) and fix **e₆ + u(1)²**.
- **Capacity.** With a cost g Σφ², a single clock gives way **first to a Klein triple**, below every pair, every other
  triple type and the uniform state, on T ∈ [0.05, 3].

## Reading

On the clocks themselves, the first multi-clock condensate keeps the grand-unified e₆ + u(1)².

## Scope

Sets larger than three are not covered. The multistart can stall, so it is a record, not a proof.

Producer: `analysis/w33_pass12077_clock_dynamics_chooses_e6.py`.
