# BT1411 Witting Basis Analyzer Unitaries

BT1410 chooses a Witting tetrad for a delayed-query frame.  BT1411 compiles
that choice into the physical single-photon analyzer.

For a tetrad

```text
B = (r0, r1, r2, r3)
```

define the analyzer matrix `U_B` by making row `j` the conjugate of Witting ray
`r_j`.  Then

```text
U_B |r_j> = |j>
```

so the four detector slots are exactly the four `mirror_slot mod 4` residues
used by the packet ABI.

## Hardware Split

The 40 Witting analyzers are not generic dense `4x4` unitaries.  Their sparsity
is the holonet shell:

```text
1  computational direct-rail analyzer
12 one-direct-rail plus complement-tritter analyzers
27 four-three-rail contextual analyzers
```

Equivalently, the nonzero-entry histogram is:

```text
4 nonzero entries:   1 analyzer
10 nonzero entries: 12 analyzers
12 nonzero entries: 27 analyzers
```

No Witting analyzer uses all 16 entries of a generic dense `4x4` multiport.
The entry alphabet is only:

```text
0, 1, +/-1/sqrt(3), +/-omega/sqrt(3), +/-omega^2/sqrt(3)
```

## Physical Reading

BT1411 says the Witting communication desk is a sparse programmable analyzer
bank:

```text
delayed-query tetrad -> 4-mode analyzer -> detector slot -> mirror_slot mod 4
```

The generic optical fact is that arbitrary finite-dimensional unitaries can be
implemented by beam-splitter and phase-shifter meshes.  The holonet-specific
fact is stronger: the Witting unitaries are a small sparse alphabet ROM, with
one direct-rail family, twelve direct-plus-tritter families, and twenty-seven
contextual three-rail families.

## Boundary

BT1411 is an exact unitary/analyzer certificate.  It does not calibrate a chip,
assign loss budgets, synthesize beam-splitter angles, or prove detector
fidelity.

## Verification

```bash
python tools/bt1411_witting_basis_analyzer_unitaries.py
python tests/test_bt1411_witting_basis_analyzer_unitaries.py
python -m py_compile tools/bt1411_witting_basis_analyzer_unitaries.py tests/test_bt1411_witting_basis_analyzer_unitaries.py
python -m json.tool data/bt1411_witting_basis_analyzer_unitaries.json
```
