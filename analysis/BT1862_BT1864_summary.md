# BT1862-BT1864 summary

Executed the three requested moves after BT1859-BT1861.

## BT1862 — homology / logical-basis computation

Built the combined GF(3) check complex:

```text
symbols = 72
edge symbols = 66
parity symbols = 6
face rows = 44
distance rows = 6
total rows = 50
```

Exact linear algebra:

```text
rank(face rows) = 42
rank(distance rows) = 6
rank(combined rows) = 48
full 72-symbol kernel dimension = 24
payload-only 66-edge kernel dimension = 18
parity/gauge degrees = 6
```

Classical check-code distance:

```text
minimum nonzero syndrome-zero word weight = 4
```

Example:

```text
edge(1,5) + edge(2,5) + 2*edge(5,8) + 2*edge(5,9) = 0 syndrome
```

Interpretation: the 44 face rows upgrade the raw six-row BT1856 distance-2 check compiler to a classical check-code distance of 4.  This is still not a quantum CSS/subsystem distance theorem.

## BT1863 — local TeX splice script

Added a non-destructive local splice script:

```text
tools/apply_bt1857_holonet_patch.py
```

It reads:

```text
papers/BT1347_photonic_holonet_journal.tex
papers/BT1857_holonet_k12_compiler_patch.tex
```

and writes:

```text
papers/BT1347_photonic_holonet_journal_with_BT1857.tex
```

Safety checks:

```text
marker must exist
patch label must not already exist in source
patch label must exist in patch
key begin/end environment counts must balance
no enumitem-only [nosep] option may appear
```

## BT1864 — Rule-110 orbit witness

Ran the BT1861 transition rule on the BT1858 length-30 tape seed.

Run:

```text
length = 30
steps = 120
first full-state repeat = none found
first gap-track repeat = none found
```

Statistics:

```text
ones_min = 9
ones_max = 24
max cyclic transitions = 24
hole track coverage at every sampled step = {0,1,2,3,4,5}
```

Gap checkpoints:

```text
t=0   SLSSLSLSLSSLSLSLSLSSLSLSSLSSLS
t=30  LSLLSLLLSLSLLLLLSLLLSSSSLLLSLL
t=60  LLLSLLLSLLSLLLLLSSSLLLSLLLSSSS
t=90  LLSSSSLLLSLLLSLLSLLLLLSSSLLLSL
t=120 SLLLSLLLSSSSLLLSLLLSLLSLLLLLSS
```

Verdict: the BT1858 seed does not collapse under the BT1861 local rule through 120 steps.  It produces nontrivial symbolic dynamics while keeping the six-hole track active.

## Boundary

BT1862 is exact classical GF(3) linear algebra, BT1863 is a local integration script, and BT1864 is a finite symbolic orbit witness.  None of them proves a protected quantum memory, a fully compiled TeX PDF, or physical universal computation.
