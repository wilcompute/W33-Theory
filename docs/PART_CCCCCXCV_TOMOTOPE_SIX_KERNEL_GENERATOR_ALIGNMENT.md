# Part CCCCCXCV — Tomotope Six-Kernel Generator Alignment

Part CCCCCXCIV fixed a six-slot dictionary abstractly. This part makes the six-slot kernel action executable from the published tomotope edge generators.

---

## 1. Input data

Use the published maniplex generator maps `p0..p3` on 12 edge labels from:

```text
data/maniplex_tables/tomotope_permutation_summary.json
```

with partial maps completed by identity on missing labels.

---

## 2. Symmetry-derived six-slot pairing

On 12 labels, enumerate all perfect-match involutions (fixed-point-free involutions):

```text
count = 12! / (2^6 * 6!) = 10395.
```

Keep only involutions `tau` commuting with every published generator:

```text
tau * p_i = p_i * tau,  for i in {0,1,2,3}.
```

Choose a canonical such `tau` (lexicographically minimal image list). Its six 2-cycles define kernel slots:

```text
k1..k6  <->  six unordered edge-pairs.
```

---

## 3. Induced generator action on slots

Because `tau` commutes with each generator, every `p_i` maps each 2-cycle pair to another 2-cycle pair, so each `p_i` induces a permutation on six slots.

This yields a concrete action:

```text
p_i^slot in S6.
```

So the six-kernel is no longer only a counting statement (`k^6`), but also a generator-level finite action extracted from the tomotope edge model.

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_six_kernel_generator_alignment.py
```

Output JSON:

```text
data/tomotope_six_kernel_generator_alignment.json
```

containing:

1. canonical commuting involution,
2. six slot-pairs,
3. induced slot actions of `p0..p3`,
4. summary counts and validity checks.

---

## 5. Synthesis

This part provides the missing executable bridge:

```text
12-edge tomotope generator action
   -> symmetry-compatible 6-pair quotient
   -> induced S6 slot action
   -> concrete six-kernel transport model.
```

That is exactly the refinement promised at the end of CCCCCXCIV: the six-kernel dictionary now carries real generator dynamics, not just static label matching.
