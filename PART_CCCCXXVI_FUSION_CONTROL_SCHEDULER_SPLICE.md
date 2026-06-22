# Part CCCCXXVI: Fusion-Control Scheduler Splice

**Status:** verified runtime splice between the CCCCVI protected photonic scheduler and the CCCCXXV theta/U(5) stabilizer completion.

## Result

Part CCCCVI gives the eight-tick runtime scheduler:

```text
projective carrier
-> heralded fusion assembly
-> KLM primitive budget
-> CSS resource validation
-> deterministic MBQC feed-forward
-> Steane/Phi6 protection
-> classical selector commit
-> E8 Z3 operation gate
```

Part CCCCXXV refines the CSS validation tick by splitting the W33 edge carrier:

```text
105 + 135 = 240
```

The `105` side is the five-block Csaszar theta packet. The `135` side is the transport complement.

## Probabilistic Budget

The runtime's probabilistic layer now splits cleanly across the same carrier:

```text
p_fusion = 1/2
2 * 105 + 2 * 135 = 210 + 270 = 480
```

and

```text
p_KLM = 1/4
4 * 105 + 4 * 135 = 420 + 540 = 960
```

So the older scheduler's `480` fusion-attempt budget and `960` KLM primitive budget are not just global counts. They decompose into theta and transport budgets with the same `7/16` and `9/16` shares.

## CSS Refinement

The CCCCVI CSS tick stated:

```text
39 X-rank + 120 Z-rank + 81 logical = 240
```

CCCCXXV resolves the `120` term:

```text
95 + 25 = 120
```

Therefore the refined CSS runtime identity is:

```text
95 + 25 + 39 + 81 = 240
```

This gives the exact split:

- `95`: local Csaszar toric checks
- `25`: `U(5)` input-mode completion
- `39`: W33 vertex-star checks
- `81`: H1 logical matter tail

## Deterministic And Classical Locks

The splice leaves the deterministic and classical contracts unchanged:

```text
deterministic Pauli frame = H1 = 81
classical selector = 40 trits
2^63 < 3^40 < 2^64
```

The "snake eats its tail" reading is now precise at the runtime level: the scheduler starts with an `81`-state projective/Pauli frame and ends by feeding the protected `H1=81` matter sector into the E8 Z3 operation gate, while the classical selector remains the `40`-trit W33 vertex record.

## External Anchor

The finite splice is aligned with the current photonic fault-tolerance literature:

- KLM establishes universal linear-optical computation from single photons, beam splitters, phase shifters, detectors, and feed-forward.
- RHG one-way computation links cluster states to surface-code/topological error correction.
- FBQC treats nondeterministic photonic fusions as errors handled by the QEC protocol rather than as a deterministic-gate assumption.

## Boundary

This is a finite scheduler splice and budget refinement. It does not simulate optical loss thresholds, detector dark counts, switch latency, biological chemistry, or empirical particle/gravity fits.

Artifacts:

- Script: `exploration/PART_CCCCXXVI_FUSION_CONTROL_SCHEDULER_SPLICE.py`
- Results: `PART_CCCCXXVI_fusion_control_scheduler_splice_results.json`
- Tests: `tests/test_fusion_control_scheduler_splice_ccccxxvi.py`
