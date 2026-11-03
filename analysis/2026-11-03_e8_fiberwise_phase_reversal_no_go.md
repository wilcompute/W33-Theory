# 2026-11-03 addendum — global E8 fiberwise phase reversal has a Z2 graph-cohomology obstruction

**Status:** exact E8 integer-root adjacency, 40 Coxeter-hexagon fibers, 540 coupled pairs, and 3,240 triangle witnesses independently checked. This is an explicit **base-fixing reflection no-go**, not a no-go for all W(E8) inversions.

The six-site Pascal boundary and each E8 six-root A2 hexagon have the same C6 graph. The earlier five-front packet constructed an S3-equivariant local identification through the parity-preserving D6 subgroup. The missing step was **global gluing** across all 40 fibers.

Let `d=c^5` be the global sixfold Coxeter shift on the roots, and write root phases in each fiber as `k in Z6`. By the certified Pass7164 E8 lift, every coupled pair of base fibers (a,b) has twelve positive-inner-product root edges, with phase differences precisely

```text
D_ab={s_ab,s_ab+1} mod 6.
```

Ask whether there is a simultaneous **base-fixing** phase reversal of the form

```text
F(f,k)=(f,alpha_f-k)
```

that preserves the 240-root adjacency graph. On an edge with old phase difference `d=k_b-k_a`, the new difference is `alpha_b-alpha_a-d`. Thus this is an automorphism of the cross-fiber edge relation only if

```text
alpha_b-alpha_a = 2*s_ab+1 (mod 6).
```

**Every required difference is odd.** Reducing mod two gives

```text
alpha_b-alpha_a = 1 (mod 2)
```

on every edge of the 40-vertex **complement** W33 graph. These equations have a solution if and only if that graph is bipartite. It is not: it has 3,240 triangles. Any triangle demands `0 = 1+1+1 = 1` (mod 2), a contradiction.

Therefore:

```text
NO graph automorphism can reverse all 40 E8 Coxeter-hexagon phases
while keeping every base W33 fiber fixed and using a phase map k->alpha_f-k.
```

This is the nonzero class of the all-ones edge 1-cochain in graph `H^1(G_complement;F2)`. Gauge changes of fiber origins shift the integer 1-cochain by a coboundary and do not remove its mod-two triangle obstruction.

The fully enumerated oriented triangle holonomy of the required Z6 differences is

```text
mod6 phase 1: 1440 triangles
mod6 phase 3:  360 triangles
mod6 phase 5: 1440 triangles
total:        3240 triangles
```

Each value is odd; none is zero. By contrast **all six uniform rotations** `(f,k)->(f,k+t)` preserve the full 240-root graph. The obstruction is specifically reflection, not cyclic phase transport.

## Important constraints

- This does not exclude the actual known Coxeter inversion in W(E8), or any element that **permutes** the 40 fibers. It only excludes maps that hold the base fixed and reverse all phases by a fiberwise affine reflection.
- It does not derive a physical parity violation, a chiral Standard Model fermion, or CP violation. Those require a specified Lorentzian quantum field theory and chiral matter representations.
- Existing repo prior-art threads include `analysis/w33_pass7163_7170_e8_hexagonal_lift.py` (source graph and Z12 cocycle), `analysis/BT746_absolute_chirality_z12.md`, `analysis/BT1758_BT1760_execution_summary.md`, and `analysis/bt1774_e8_inversion_witness.py`. The contribution here is the **explicit elementary all-ones mod-two cohomology obstruction** to simultaneous base-fixing sixfold phase reversal, not a claim to supersede those results.

## Reproduction

```powershell
python analysis/2026_11_03_e8_fiberwise_phase_reversal_obstruction.py
python -m pytest tests/test_20261103_e8_phase_reversal_obstruction.py -q
```

Results JSON `data/2026_11_03_e8_fiberwise_phase_reversal_obstruction.json`.
