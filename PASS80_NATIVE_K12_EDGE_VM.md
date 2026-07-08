# Pass 80 -- Native K12 / Edge-Zeta / Spence / VM Closure

Pass 80 executes the five follow-ups from Pass 79.

## 1. Native K12 `[[66,8,3]]_3` code

The new witness replaces the Pass 79 block-plus-ancilla construction with a
K12-native CSS stabilizer code.

```text
physical qutrits = 66 K12 edges
X checks         = 12 oriented K12 vertex-incidence rows, rank 11
Z checks         = 47 independent oriented K12 triangle cycles, rank 47
k                = 66 - 11 - 47 = 8
d                = 3
```

The checker rejects all weight-1 and weight-2 CSS logicals on both sides and
exhibits weight-3 logicals on both sides.  Every one of the 66 K12 edges is
covered by the triangle-cycle check basis.

Boundary: this is native to the K12/h=6 edge carrier.  The selected 47 triangle
cycles are a stabilizer basis, not a claim that all 47 are faces of one
44-face orientable K12 embedding.

## 2. Edge-zeta / Hashimoto factor table

The directed-edge Hashimoto carrier has degree `480`.  The Bass factor table is:

| Source | Hashimoto factor | Degree |
|---|---|---:|
| Bass tail | `(x^2 - 1)^200` | 400 |
| `theta=12` | `x^2 - 12x + 11 = (x-1)(x-11)` | 2 |
| `theta=2` | `(x^2 - 2x + 11)^24` | 48 |
| `theta=-4` | `(x^2 + 4x + 11)^15` | 30 |

Total degree: `400 + 2 + 48 + 30 = 480`.

The GAP-directed edge action from Pass 79 remains attached as the representation
carrier.  Boundary: a finer noncommutative Artin splitting of the
200-dimensional tail remains open.

## 3. Final Spence residual separator

Pass 79 left only Spence pair `[20,24]` unresolved under local cycle histograms,
alpha, and K4 counts.  Pass 80 computes the induced 6-vertex
edge-count/degree-sequence profile for that pair:

```text
C(40,6) = 3838380 subsets per graph
profile bins       = 63
differing bins     = 20
```

Therefore:

```text
local cycle histogram + alpha + targeted induced-6 profile hears all 28 Spence graphs
```

## 4. Terwilliger local VM ISA

The exact Terwilliger Wedderburn decomposition

```text
Q + Q + Q + M2(Q) + M3(Q)
```

compiles into a 16-op local channel ISA:

```text
3 scalar selector/control ops
4 M2 binary relay / cut-plane ops
9 M3 native ternary qutrit processor ops
```

This is the first concrete local-processor reading of the dim-16 algebra.

## 5. Exact syndrome decoder

The native K12 code now has an exact ideal-syndrome lookup decoder for all
single-qutrit Pauli errors:

```text
66 sites * 8 nontrivial qutrit Paulis = 528 syndromes
decoded exactly                       = 528 / 528
```

Boundary: this is an ideal-syndrome decoder, not a noisy circuit-level threshold
simulation.

## Verification

```bash
python3 w33_pass80_native_k12_edge_vm.py
python3 -m py_compile w33_pass80_native_k12_edge_vm.py
python3 -m json.tool w33_pass80_native_k12_edge_vm.json
```

Current status: `PASS`.
