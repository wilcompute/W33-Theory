# BT1348 & BT1349 — Summary

## BT1348: GF(3) Error Correction + Holonet Integration

### What it does
Integrates the Pillar-45 GF(3) qutrit QEC primitives with the Photonic Holonet routing layer.

### Key result
The finite shell arithmetic is exactly **1 + 12 + 27 = 40**, but the old
inference from those shell sizes to QEC resource classes was too strong.  The
three-qutrit repetition witness detects X-type shift errors only; a one-site Z
phase is an undetected logical action.  The BT1340 routing map is unitary but
does not preserve that repetition subspace (the tested superposition retains
weight 2/3 in it).  Later ADQC/Pass10941 certificates independently retain
qutrit T as a genuine non-Clifford resource.

### Witnesses (7)
| ID | Claim |
|----|-------|
| W1 | GF(3) arithmetic verified |
| W2 | Qutrit Pauli X, Z are order-3 and satisfy Weyl relation |
| W3 | Three-qutrit repetition basis states are orthogonal |
| W4 | Z-difference checks fix the repetition subspace |
| W5 | Single X shift is detected; single Z phase is not |
| W6 | Routing is unitary but leaves only 2/3 weight in the repetition subspace |
| W7 | Shell arithmetic 1+12+27=40; contextual 36 is a separate count |

---

## BT1349: Multi-Photon Toroidal Q4 Heptad Scaling

### What it does
Extends the single-photon Holonet to a 7-photon cluster state using the Fano plane as the inter-node routing geometry.

### Key result
Because every pair of Fano points lies on one line, point adjacency by
"sharing a Fano line" is **K7**, not a 3-regular graph.  K7 is the
1-skeleton of the seven-vertex Csaszar torus triangulation.  The corrected
witness applies one qutrit CZ to each of the 21 unordered pairs, has adjacency
spectrum **6^1 + (-1)^6** and diameter 1, and still gives Schmidt rank 3 across
all seven single-node cuts.

### Witnesses (6)
| ID | Claim |
|----|-------|
| W1 | Fano plane: 7 lines × 3 pts, every pair shares 1 line |
| W2 | Fano point graph is K7 = Csaszar 1-skeleton, degree 6 |
| W3 | K7 spectrum is {6, -1^6} |
| W4 | 7-photon graph state prepared with all 21 pairwise CZ_3 gates |
| W5 | Schmidt rank 3 across all 7 single-node bipartitions |
| W6 | Diameter = 1 with complete pair routing |

---

## Cumulative witness count

| Proof | Witnesses |
|-------|-----------|
| BT1340 | 5 (routing) |
| BT1341 | 5 (contextuality) |
| BT1342 | 6 (clock) |
| BT1343 | All combined |
| BT1348 | 7 (QEC integration) |
| BT1349 | 6 (multi-photon scaling) |
| **Total** | **29 independent witnesses** |

---

## Run the new witnesses

```bash
python proofs/bt1348_gf3_qec_holonet_integration.py
python proofs/bt1349_multi_photon_toroidal_scaling.py
```
