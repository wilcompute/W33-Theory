# Part DCXIV — Tomotope/Toroidal $\mathbb{Z}_2$ Orbit-Quotient Bridge

This part applies Burnside's lemma to the DCXIII swap involution.

---

## 1. Oriented shell quotient

On the oriented shell (`42` elements), the swap has no fixed points, so:

```text
|X/\mathbb{Z}_2| = (|X| + |Fix|)/2 = (42 + 0)/2 = 21.
```

---

## 2. Weighted shell quotient

On the weighted shell (`168` elements), the same holds:

```text
|Y/\mathbb{Z}_2| = (168 + 0)/2 = 84.
```

So the involution halves both shells exactly.

---

## 3. Executable artifact

Script:

```text
scripts/tomotope_toroidal_z2_orbit_quotient_bridge.py
```

Output:

```text
data/tomotope_toroidal_z2_orbit_quotient_bridge.json
```

with fixed-point counts, orbit counts, and Burnside certificates.
