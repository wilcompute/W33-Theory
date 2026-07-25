# Pass 79 -- Code / Edge-Space / Terwilliger / Spence Closure

Pass 78 left four boundaries open on purpose.  Pass 79 closes them with
runnable witnesses while preserving the remaining canonical-geometry boundary.

## 1. Explicit `[[66,8,3]]_3` stabilizer witness

`w33_pass79_full_closure.py` builds a finite qutrit stabilizer code on 66
physical qutrits:

```text
8 copies of the cyclic [[5,1,3]]_3 code
+ 26 frozen single-site Z ancillas
= [[66,8,3]]_3
```

The verifier computes stabilizer rank `58`, so `k = 66 - 58 = 8`, checks all
stabilizer commutators, enumerates every weight-1 and weight-2 qutrit Pauli
error (`137808` cases), and exhibits a commuting non-stabilizer logical of
weight `3`.

Boundary: this proves an explicit finite `[[66,8,3]]_3` stabilizer witness in
the architecture's envelope.  It does **not** claim to be the canonical
genus-6/K12 geometric code.

## 2. Full edge-space character decomposition

`analysis/w33_pass79_edge_terwilliger.g` uses GAP's `Sp(4,3)` matrix group,
passes to the projective `PSp(4,3)` action on 40 points, and derives W33
adjacency as the 12-point suborbit of a point stabilizer.

The directed-edge action has degree `480`, rank `24`, and active constituents:

```text
1, 15^2, 15, 20, 24^3, 30, 45, 45, 60, 81^2
```

Equivalently, as `(degree, multiplicity)`:

```text
(1,1), (15,2), (15,1), (20,1), (24,3),
(30,1), (45,1), (45,1), (60,1), (81,2)
```

The undirected-edge action has degree `240`, rank `10`, and active
constituents:

```text
(1,1), (15,1), (15,1), (20,1), (24,2), (60,1), (81,1)
```

This is the edge-space layer that the point-module `1+15+24` decomposition
could not see.

## 3. Terwilliger/Wedderburn decomposition

GAP computes the point-rooted Terwilliger algebra exactly:

```text
dimension = 16
center dimension = 5
radical dimension = 0
central idempotents = 5
component dimensions = 1, 1, 1, 4, 9
Wedderburn block sizes = 1, 1, 1, 2, 3
```

So the dim-16 fingerprint is now replaced by the block-level statement:

```text
T(x) ~= Q + Q + Q + M_2(Q) + M_3(Q)
```

This matters architecturally: the local processor is not just a 16-dimensional
black box.  It has three scalar control channels, one two-dimensional matrix
channel, and one three-dimensional matrix channel.

## 4. Complete 28-Spence hearing table

The verifier stores and parses McKay's graph6 catalogue
`data/spence_srg_40_12_2_4.g6`, which contains all 28
`SRG(40,12,2,4)` graphs.  Every graph is rechecked for degree `12`,
`lambda=2`, and `mu=4`.

What the invariants hear:

| Invariant | Classes Heard | Residual Twins |
|---|---:|---|
| Adjacency spectrum / Bass Ihara | 1 | all 28 |
| 2-WL rank-3 coloring | 1 | all 28 |
| `K4` count | 11 | multiple |
| Independence / ovoid number | 2 | `alpha=7` vs `alpha=10` |
| Local 12-vertex cycle histogram | 26 | `[20,24]`, `[27,28]` |
| Local histogram + alpha | 27 | `[20,24]` |

The two all-local-`4C3` graphs are graph `27` and graph `28`.  The ovoid
number separates them:

```text
Spence #27: alpha = 10 -> Q(4,3) candidate
Spence #28: alpha = 7  -> W(3,3) candidate
```

Boundary: graph pair `[20,24]` survives the listed invariants.  That pair is a
proper target for the next stronger edge-zeta, automorphism, or canonical
labelling witness.

## Verification

```bash
python3 w33_pass79_full_closure.py
python3 -m py_compile w33_pass79_full_closure.py
/usr/bin/gap -q analysis/w33_pass79_edge_terwilliger.g
python3 -m json.tool w33_pass79_full_closure.json
```

Current status: `PASS`.
