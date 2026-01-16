# TOE Core Finish (v23)

This bundle is the **finished, choice-free kernel** extracted from your computed W33 → 90-scheme → Q45 rung.

It proves an exact field law linking:
- intrinsic **triad type** in GQ(4,2),
- the canonical **Z₂ voltage curvature**,
- and the **fiber holonomy** of the natural (sheet×port) bundle.

## Objects

### Base geometry
- **Q**: the 45-node quotient graph (degree 32). Its complement is the point graph of **GQ(4,2)**.
- **H**: the collinearity graph from the 27 lines (degree 12).

A triangle in Q is a **triad**: a triple of points pairwise noncollinear in H.

### Z₂ field
Each edge (u,v) in Q has a canonical voltage w(u,v)∈Z₂.  
Triangle curvature is the parity:
  π(u,v,w)=w(u,v)⊕w(v,w)⊕w(w,u).

### Port transport and the correct fiber
Each directed edge has an S₃ transport that depends on the *start sheet* s∈Z₂.

The correct fiber at each vertex is:
  F_q = Z₂ × {0,1,2}
(sheet × port), i.e. 6 states.

Transport along u→v acts on (s,p) by:
- s' = s ⊕ w(u,v)
- p' = g_{u→v}^{(s)}(p)

So each edge induces a permutation in S₆.

## Curvature observable (gauge invariant)
For each Q-triangle (u,v,w), define the fiber holonomy:
  H(u,v,w) = T_{w→u} ∘ T_{v→w} ∘ T_{u→v} ∈ S₆

Its **cycle type** (partition of 6) is conjugacy-invariant ⇒ gauge-invariant.

## Intrinsic triad type via centers
Define:
  centers(u,v,w) = | N_H(u) ∩ N_H(v) ∩ N_H(w) |
This takes values in {0,1,3} for GQ(4,2) triads.

## Theorem (computed, exact)
The triad type, Z₂ curvature, and fiber holonomy cycle type are in perfect 1–1 correspondence:

| centers(u,v,w) | Z₂ parity π | fiber holonomy cycle type in S₆ | count |
|---:|---:|---:|---:|
| 0 (acentric) | 0 | (3,1,1,1) | 2880 |
| 1 (unicentric) | 1 | (2,2,2) | 2160 |
| 3 (tricentric) | 0 | identity (1,1,1,1,1,1) | 240 |

No other behaviors occur.

### Operational interpretation
- tricentric: **flat** (identity holonomy)
- acentric: **pure C₃ rotor** on exactly one sheet (3-cycle on ports; other sheet fixed)
- unicentric: **sheet exchange** with a port permutation τ (three disjoint 2-cycles pairing the sheets)

This is the discrete analog of:
- base space,
- Z₂ spin/voltage field,
- a nonabelian connection on a fiber bundle,
- and a gauge-invariant curvature observable.

## Files
- `Q_triangles_with_centers_Z2_S3_fiber6.csv`
  Full 5280-triangle table: centers, Z₂ parity, S₃ holonomy (start sheet 0), S₆ holonomy and its derived invariants.

- `Q_vertex_tau_profile.csv`
  For each vertex q, distribution of τ on incident unicentric triangles (a local “potential landscape” on Q).

- `toe_core_theorem.json`
  Machine-readable statement of the theorem and counts.

- `recompute_v23.py`
  Minimal recomputation script (expects the two input zips in the same folder).

## Why this “finishes it”
This is the first rung in your stack that is:
- fully explicit,
- computed from your actual artifacts,
- section-free (no ad-hoc closure),
- and stated as a true field law.

Everything else (N12/W33 transport, commutator phases, ±i holonomy) plugs into this as **dynamics** over this fixed kinematic scaffold.
