# Part DCCLXVII - Axis-Syndrome Nilpotent / Octahedral Codec Bridge

**Bridge:** `verify_dcclxvii_axis_syndrome_nilpotent_octahedral_bridge.py` - Verified
**Tests:** `tests/test_dcclxvii_axis_syndrome_nilpotent_octahedral_bridge.py`
**Data:** `data/dcclxvii_axis_syndrome_nilpotent_octahedral_bridge.json`

---

## 1. Claim

DCCXVI gave the promoted photonic/QEC local alphabet:

```text
12 = 3 axes * 2 signs * 2 accepted/return roles.
```

DCCL-DCCLXVI gave the octahedral harmonic carrier on the six signed axes:

```text
{+B23, -B23, +B31, -B31, +B12, -B12}.
```

DCLXXXV gave the local holonomy witness:

```text
N = [[0, 1],
     [0, 0]],       N^2 = 0  over F3.
```

This part proves these are the same local machine at three scales:

```text
local codec:        6 signed axes * 2 extension states = 12
photonic fusion:    40 * 12 = 480
KLM primitive:      40 * 24 = 960
matter extension:   0 -> 81 -> 162 -> 81 -> 0.
```

---

## 2. The octahedral runtime carrier

The six signed Clifford axes are exactly the six octahedron vertices. The
octahedron has:

```text
6 vertices,
12 undirected turn edges,
24 directed turn incidences.
```

The DCCXVI local slot is a signed axis plus a two-state extension:

```text
accepted:+B23
return:+B23
accepted:-B23
return:-B23
...
```

So the same local `12` appears in two equivalent ways:

```text
6 signed axes * 2 extension states = 12,
octahedral undirected turn edges = 12.
```

The KLM rail bit resolves each signed-axis/role slot into one of the two
non-opposite target axes. That gives:

```text
12 slots * 2 rail choices = 24 directed octahedral turns.
```

Across the `40` W(3,3) carrier sites:

```text
40 * 12 = 480,
40 * 24 = 960.
```

This is the exact finite meaning of the photonic doubling: the KLM primitive
layer is the directed octahedral incidence cover of the axis-syndrome codec.

---

## 3. The nilpotent extension

Use the reduced two-state F3 extension:

```text
accepted/frame branch
return/syndrome branch
```

with nilpotent increment:

```text
N(return) = accepted,
N(accepted) = 0.
```

In matrix form:

```text
N = [[0, 1],
     [0, 0]].
```

On the 12 local slots this is six copies of the same extension:

```text
I6 tensor N.
```

Therefore:

```text
dimension = 12,
rank = 6,
image = kernel = 6,
N^2 = 0.
```

On the promoted homological matter sector:

```text
I81 tensor N.
```

Therefore:

```text
dimension = 162,
rank = 81,
image = kernel = 81,
N^2 = 0.
```

This is the concrete operator form of:

```text
0 -> 81 -> 162 -> 81 -> 0.
```

---

## 4. Snake eats tail

The return branch is not a second classical selector. It is the nilpotent tail
of the accepted frame branch:

```text
return syndrome -> accepted frame -> 0.
```

That is the QEC ouroboros in finite form. The runtime cycles back into itself,
but because the return operation is square-zero, the correction tail closes
without adding a new classical degree of freedom or killing the `H1=81`
logical sector.

---

## 5. Honest boundary

This part proves a finite runtime/codec/holonomy identity. It does not
construct a universal non-Clifford photonic gate set, solve detector noise, or
prove the curved 4D spectral-action asymptotics.

The new content is the architecture lock:

```text
DCCXVI 12-symbol codec
  = DCCL octahedral signed-axis carrier
  = DCLXXXV square-zero F3 holonomy extension
  => 0 -> 81 -> 162 -> 81 -> 0.
```
