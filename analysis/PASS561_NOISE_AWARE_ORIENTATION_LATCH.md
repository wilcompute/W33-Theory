# Pass 561 — noise-aware quartic and orientation readout

The 70 quartic levels have minimum squared separation `3750` across the four real Galois readouts. Sub-Gaussian union bounds give exact shot budgets conditional on the calibrated single-shot noise scale.

For the orientation channel, two architectures are compared:

- direct twelvefold parity, whose contrast is `c^12`;
- repeated per-channel signs followed by a classical parity latch.

The correct compiler policy is adaptive. Under the conservative profile the repeated-channel design uses 564 shots versus 1,295 direct shots. Under nominal and aspirational profiles direct parity wins, using 161 and 42 shots respectively. A fixed claim that either architecture always dominates is false.
