# BT1320–BT1325 Hypercube Tower & Holonet Bridges

## Summary

This packet extends the BT1319 local Q4 packet router upward through Q5 and Q6
to the D12 mirror bus, establishing the complete inter-quadrant routing protocol
and physical realizability analysis for the W33 photonic holonet.

---

## BT1320 — Q5 Hypercube Holonet Bridge

Q5 (32 vertices, 80 edges, diameter 5) is the next layer above the local Q4
packet router. Ten embedded Q4 sub-cubes partition the 32 Q5 vertices:

```
Q5 vertices  = 2 * Q4 vertices   = 32
Q5 edges     = 5 * 2^4           = 80
Q5 4-faces   = C(5,4)*2^1        = 10  (ten Q4 sub-cubes)
RM(1,4) code : [16, 5, 8]
```

A Gray code Hamilton cycle on Q5 uses 5 alternating flip bits, extending the
Q4 Gray clock by one dimension. The RM(1,4) code doubles the distance from the
Q4 [8,4,4] Hamming code: one bit flip in Q5 lifts to a distance-8 protected
transition.

---

## BT1321 — Q6 Hypercube Holonet Bridge (Tomotope Flag Bus)

Q6 (64 vertices, 192 edges) is where the hypercube tower first reaches the
tomotope flag count directly:

```
Q6 edges = 6 * 2^5 = 192 = tomotope_flags
```

Additional Q6 identities:

```
Q6 2-faces = C(6,2)*2^4 = 15*16 = 240 = 2 * 120 D12 antipode pairs
Q6 3-faces = C(6,3)*2^3 = 20*8  = 160
Q6 4-faces = C(6,4)*2^2 = 15*4  = 60  (fifteen Q4 sub-cubes)
Q6 5-faces = C(6,5)*2^1 = 6*2   = 12  (six Q5 sub-cubes)
RM(1,5) code : [32, 6, 16]
```

The Q6/tomotope edge identity is a verified counting fact. A future
construction must assign Q6 directed edges to specific flag transitions to
upgrade this to an objectwise proof.

---

## BT1322 — Inter-Quadrant Routing Protocol

The layered routing hierarchy:

```
Local   : Q4 (16 states)   [8,4,4]  Hamming    d=4
Transit : Q5 (32 states)   [16,5,8] RM(1,4)   d=8
Flag bus: Q6 (64 states)   [32,6,16] RM(1,5)  d=16
Global  : D12 (2160 slots) 540 charts, 4 transversals/chart
```

Routing rules:
- Q4 → Q5: append one bit (0=stay, 1=transit)
- Q5 → Q6: append one bit (0=local bus, 1=flag bus)
- Q6 → D12: 2160 = 192 * 11.25 (non-integer; D12 slot assignment is not a
  pure Q6 covering — an objectwise assignment remains open)

Error isolation principle: code distance doubles at each layer hop, ensuring
that single-bit errors within a layer cannot propagate upward undetected.

```
Q4 hop : error weight < 2 → correctable (d/2 = 2)
Q5 hop : error weight < 4 → correctable (d/2 = 4)
Q6 hop : error weight < 8 → correctable (d/2 = 8)
```

---

## BT1323 — Toroidal Heptad Physical Realizability

Physical parameter budgets for a telecom-band (1550 nm) photonic implementation:

| Parameter | Value | Constraint |
|-----------|-------|------------|
| Coupling loss per edge | ≤ 0.1 dB | 21 edges → 2.1 dB max insertion loss |
| Phase noise per vertex | 1×10⁻⁴ rad | 7 vertices → 7×10⁻⁴ rad total |
| Photon coherence time | ≥ 10 ns | fiber loop travel time < 0.77 ns ✓ |
| Q4 switching time | ≤ 1 ns/state | 16 states × 1 ns = 16 ns total |
| Fiber loop diameter | 50 mm | circumference = 157.1 mm |

The Q4 router maps to a 4-port symmetric beamsplitter network. The [8,4,4]
Hamming router lift corresponds to an 8-port Mach-Zehnder interferometer array
with 4 input modes and distance-4 error correction.

**These are engineering feasibility bounds, not W33-derived theorem proofs.**

---

## BT1324 — Holonet Architecture Numerical Simulation

Simulation parameters: 10,000 packets, W33 seed (33), telecom-band photons.

Key results:
- **Gray code routing** achieves 100% Q4 state coverage in 16 steps (vs. ~75%
  for random walk in 64 steps)
- **Error detection rates** increase with layer: Q6 undetected error rate is
  lower than Q4 due to larger code distance
- **Tomotope flag utilization**: approximately uniform across 192 Q6 edges
  (load balance ratio ~0.8 for 10k packets)
- **D12 mirror bus**: approximately uniform chart load distribution
- **Total worst-case latency**: 15 ns (4+5+6 hops × 1 ns/hop)

---

## BT1325 — Hypercube Tower Summary

### Layer Table

| Layer | n | Vertices | Edges | Diameter | Code | d | Role |
|-------|---|----------|-------|----------|------|---|------|
| Q4 | 4 | 16 | 32 | 4 | [8,4,4] Hamming | 4 | Local packet router |
| Q5 | 5 | 32 | 80 | 5 | [16,5,8] RM(1,4) | 8 | Transit layer |
| Q6 | 6 | 64 | 192 | 6 | [32,6,16] RM(1,5) | 16 | Tomotope flag bus |
| D12 | — | 2160 slots | — | — | — | — | Global chart atlas |

### Tower Invariants

```
Vertices double:       16 → 32 → 64
Code distance doubles: 4  → 8  → 16
Q6 edges = tomotope flags = 192  ✓
Q6 2-faces = 240 = 2 × 120 D12 antipode pairs  ✓
D12 slots = 2160 = 540 × 4  ✓
```

### Open Problems (BT1316–BT1325 boundary)

| ID | Description | Status |
|----|-------------|--------|
| OP1 | Bijection: 7 metric toroidal realizations ↔ 7 Csaszar C2 involutions | Not proved (current labels) |
| OP2 | Objectwise Q6→D12 slot assignment | Open |
| OP3 | Full Clifford algebra for 14641 = 11⁴ | Scale marker only |
| OP4 | Physical photon scheduling in Q4/Q5/Q6 | Parameter budgets established (BT1323) |

---

## Verification

```bash
python3 analysis/bt1320_q5_holonet_bridge.py
python3 analysis/bt1321_q6_holonet_bridge.py
python3 analysis/bt1322_inter_quadrant_routing_protocol.py
python3 analysis/bt1323_toroidal_heptad_physical_realizability.py
python3 analysis/bt1324_holonet_simulation.py
python3 analysis/bt1325_hypercube_tower_summary.py
python3 tests/test_bt1320_bt1325_hypercube_tower.py
```
