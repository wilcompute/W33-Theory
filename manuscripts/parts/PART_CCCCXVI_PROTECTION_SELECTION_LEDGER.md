# Part CCCCXVI: Protection / Selection Ledger

**Status:** verified role-assignment layer for the protected photonic architecture.

## Result

The recent architecture stack now has several valid mechanisms, but they do not all do the same job.  CCCCXVI assigns each mechanism to its correct role:

| Mechanism | Role |
|---|---|
| Heralded photonic assembly | retry before logical computation |
| Triangle-flat cyclic covers | valid covers, rejected as distance upgrades because `d=3` survives |
| K4 line-star triples | the `H1=81` matter sector, not disposable stabilizers |
| Q4/Bacon-Shor packets | local `[[1296,81,4]]` subsystem routing hardware |
| Steane/Phi6 lift | active quantum protection: `[[82320,81,>=81]]` |
| Classical selector | commit the `40`-trit record only after protected acceptance |
| E8 Z3 gate | bounded operation gate with `8347` checked bracket terms |

The generated ledger passes `15/15` checks.

## Architectural Decision

The Q4 packet layer is still important, but it is not the current distance-12 proof.  CCCCXV shows:

```text
raw Q4 replacement target = 12
dressed subsystem weight  = 4
```

So the active protection layer remains:

```text
[[82320,81,>=81]]
```

The Q4/Bacon-Shor packet layer remains the native local routing/gauge layer:

```text
[[1296,81,4]]
```

## Boundary

This solves role assignment, not device calibration. It does not simulate optical loss, detector dark counts, decoding latency, or the future column-locked Q4 repair.

Artifacts:

- Script: `exploration/PART_CCCCXVI_PROTECTION_SELECTION_LEDGER.py`
- Results: `PART_CCCCXVI_protection_selection_ledger_results.json`
- Tests: `tests/test_protection_selection_ledger_ccccxvi.py`
