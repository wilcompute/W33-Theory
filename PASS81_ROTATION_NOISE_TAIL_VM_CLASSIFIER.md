# Pass 81 -- Rotation / Noise / Tail / VM / Classifier

Pass 81 executes the five follow-ups from Pass 80.

## 1. K12 Rotation System

The verifier hardcodes and checks an explicit orientable triangular embedding of
`K12`.

```text
vertices = 12
edges    = 66
faces    = 44 oriented triangles
Euler    = 12 - 66 + 44 = -10
genus    = 6
```

Each of the `132` directed arcs occurs in exactly one oriented triangular face,
and each vertex rotation is one 11-cycle.  The 44 face boundaries span rank
`43`.  The Pass 80 native stabilizer uses rank `47`, so the rotation system is
a comparison object, not a replacement for the full code basis.

## 2. Noisy Syndrome Simulator

The native `[[66,8,3]]_3` code now has a deterministic phenomenological noisy
decoder harness:

```text
data errors: qutrit Pauli error per site with probability p
syndrome errors: each syndrome trit flips with probability q
rounds: 1, 3, 5 repeated extraction rounds
decoder: majority-voted syndrome -> exact single-error lookup
```

The emitted table has `36` rows over `p in {0.0005,0.001,0.002,0.005}`,
`q in {0,0.002,0.01}`, and rounds `{1,3,5}`.  At `p=0.001`, `q=0.01`, the best
row uses 5 rounds and reaches success rate `1.0` in the deterministic sample.

Boundary: this is a repeated phenomenological syndrome model, not a gate-level
threshold proof.

## 3. GAP Hashimoto Tail Decomposition

`analysis/w33_pass81_hashimoto_tail_decomposition.g` builds the actual
`480 x 480` nonbacktracking operator and decomposes its `+1` and `-1`
eigenspaces under `PSp(4,3)`.

```text
lambda = +1 eigenspace: dimension 201 = 30 + 45 + 45 + 81
lambda = -1 eigenspace: dimension 200 = 15 + 20 + 24 + 60 + 81
```

This corrects the naive “two 200-dimensional tails” reading.  The `-1`
eigenspace is a clean 200-dimensional tail; the `+1` tail is fused with the
extra `x=1` Bass root into a 201-dimensional GAP eigenspace.

## 4. Packet VM Terwilliger Channels

`analysis/w33_packet_vm.py` now attaches a concrete Terwilliger local-channel op
to every routed packet row.  The 16-op table is:

```text
3 scalar Q ops
4 M2(Q) relay/cut-plane ops
9 M3(Q) ternary processor ops
```

The packet VM audit saw channel totals:

```text
Q: 80
M2(Q): 98
M3(Q): 251
```

## 5. Progressive Spence Classifier

The staged classifier identifies all 28 `SRG(40,12,2,4)` graphs:

```text
local cycle histogram + alpha: 26 graphs
targeted induced-6 profile:    remaining 2 graphs, [20,24]
total classified:              28 / 28
```

So the architecture now has a minimal “what each invariant hears” classifier:
cheap local invariants almost classify the universe, and one targeted
six-vertex profile resolves the final twin.

## Verification

```bash
python3 w33_pass81_rotation_noise_tail_vm_classifier.py
/usr/bin/gap -q analysis/w33_pass81_hashimoto_tail_decomposition.g
python3 -m py_compile w33_pass81_rotation_noise_tail_vm_classifier.py
python3 -m json.tool w33_pass81_rotation_noise_tail_vm_classifier.json
```

Current status: `PASS`.
