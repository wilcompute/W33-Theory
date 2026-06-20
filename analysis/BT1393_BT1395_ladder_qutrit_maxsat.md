# BT1393--BT1395 -- Ladder Audit, Reduced Qutrit Simulator, MaxSAT Bound Pathway

## BT1393 -- Q5-Q7 ladder consistency audit

Added:

```text
tools/bt1393_ladder_consistency_audit.py
data/bt1393_ladder_consistency_audit.json
```

Resolutions:

```text
Q7 ceiling vs Q7 completion:
  The earlier Q7 ceiling note is a pre-ladder/W63-extension caution.
  BT1356 certifies a Q7 heptad completion inside the heptad ladder.

Q6 vs Q7 crossing:
  Q6 is the first super-Ramanujan crossing.
  Q7 remains super-Ramanujan and period-closing.

exact_W33_matches = 0:
  This refers to the competitor/falsifier pool, not the W33 reference family.
```

## BT1394 -- Reduced photonic Bell-qutrit demonstrator

Added:

```text
tools/bt1394_reduced_qutrit_demonstrator.py
data/bt1394_reduced_qutrit_demonstrator.json
```

The Bell-qutrit signatures are verified:

```text
V(I) = 1
V(F3) = 1/3
V(X) = 0
V(Z) = 0
```

The route-controlled Clifford transport is unitary and norm-preserving.  The reduced route density matrix is maximally mixed after tracing out the Bell legs, so route coherence requires an interferometric/quantum-erasure readout.

## BT1395 -- S3 MaxSAT bound certificate pathway

Added:

```text
schema/bt1395_s3_maxsat_certificate.schema.json
tools/bt1395_s3_maxsat_bound_pathway.py
data/bt1395_s3_maxsat_bound_pathway.json
```

Current status:

```text
witness score = 210
optimality_status = witness_only
```

The schema supports witness, upper-bound, and optimality certificates.

## Regression

Added:

```text
tests/test_bt1393_bt1395_audit_qutrit_maxsat.py
```
