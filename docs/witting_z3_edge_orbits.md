# Z3 Edge Labels by Monomial Orbits

We decomposed the 540 non-orth edges into orbits under the **monomial symmetry**
group (order 243). The Z3 edge labels are **not constant** on orbits, but show
structured distributions within each orbit.

## Orbit structure
- **12 total orbits**
- Orbit sizes: **8 orbits of size 27**, **4 orbits of size 81**

This matches 8×27 + 4×81 = 540.

## Label distributions (examples)
```
Orbit 0 size 27: {1:12, 2:14, 0:1}
Orbit 2 size 27: {0:11, 1:8, 2:8}
Orbit 5 size 81: {2:25, 1:33, 0:23}
Orbit 6 size 81: {2:33, 1:25, 0:23}
```

The Z3 labels vary within orbits, but each orbit has a **stable distribution**
pattern. The 27-orbits are highly skewed, while the 81-orbits are closer to
balanced.

Full listing: `docs/witting_z3_edge_orbits.txt`
Script: `tools/witting_z3_edge_orbits.py`
