# V15 — Closing H under g1 action, exact n=4 residuals, and an explicit l4 patch proposal

This step answers the question from V14: *if we enlarge H to be closed under the g1 action, does the n=4 residual shrink?*

## 1) Closure under g1 action
- Initial H0 (distinct K3 outputs): **173**
- Closing H0 under the filtered bracket action of g1 adds **75** elements in one iteration (including 8 Cartan), yielding **H = 248** (full E8 basis).

Closure details: `[{'iter': 0, 'added': 75, 'added_cartan': 8, 'added_grade_hist': {'g2': 24, 'g0': 24, 'g1': 19}, 'added_phase_hist_top': [(4, 13), (1, 13), (2, 11), (0, 10), (5, 10)]}, {'iter': 1, 'added': 0}]`

## 2) Exact n=4 residual counts
We recompute the same n=4 residual formula used in V14.

### Projected (V14-style) action onto H0
- residual stats over all g1^4 quads: `{'zero': 1657243, 'nonzero': 6497, 'single': 6497}`
- residual support size: **173** (always within H0)

### Closed action (no projection) with H=248
- residual stats over all g1^4 quads: `{'zero': 1656065, 'nonzero': 7675, 'single': 7675}`
- residual support size: **234**
- coefficient histogram: `{1: 3352, 2: 458, -1: 3378, -2: 438, -3: 29, 3: 18, 4: 1, -4: 1}`
- output grade histogram: `{'g2': 2577, 'g1': 2874, 'g0': 2224}`
- output phase histogram (Z6): top=[(5, 1550), (0, 1512), (4, 1355), (1, 1125), (2, 1102), (3, 1031)]

Support comparison:
- support(n4) ∩ support(K3) size: **173**
- new outputs outside K3 support: **61**

Top residual output basis elements:
- {'basis': 87, 'count': 146, 'grade': 'g2', 'phase_z6': 5, 'i27': 16}
- {'basis': 32, 'count': 131, 'grade': 'g1', 'phase_z6': 0, 'i27': 26}
- {'basis': 60, 'count': 112, 'grade': 'g1', 'phase_z6': 4, 'i27': 18}
- {'basis': 65, 'count': 106, 'grade': 'g2', 'phase_z6': 0, 'i27': 23}
- {'basis': 236, 'count': 104, 'grade': 'g0', 'phase_z6': 5, 'i27': None}
- {'basis': 96, 'count': 96, 'grade': 'g1', 'phase_z6': 0, 'i27': 5}
- {'basis': 88, 'count': 90, 'grade': 'g2', 'phase_z6': 5, 'i27': 4}
- {'basis': 27, 'count': 84, 'grade': 'g2', 'phase_z6': 5, 'i27': 2}
- {'basis': 39, 'count': 84, 'grade': 'g1', 'phase_z6': 4, 'i27': 17}
- {'basis': 210, 'count': 77, 'grade': 'g0', 'phase_z6': 5, 'i27': None}
- {'basis': 66, 'count': 76, 'grade': 'g1', 'phase_z6': 1, 'i27': 12}
- {'basis': 33, 'count': 75, 'grade': 'g1', 'phase_z6': 0, 'i27': 23}

## 3) Systematic patch (l4) proposal
Since the n=4 residual is still sparse and always single-term, we can kill it explicitly by moving to a **3-term L∞**:

- Add degree-2 generators `s_k` for each residual output basis element k (support size 234).
- Define `l1(s_k)=t_k` (so its image is the degree-1 generator mapping to basis element k).
- Define `l4(a,b,c,d) = -residual(a,b,c,d) · s_out` for each of the 7,675 quads with nonzero residual.

This makes the n=4 identity hold **by construction**; the next thing to check is the induced n=5 obstruction (V16).

Full l4 table is included as `l4_residual_quads_full.json`.
