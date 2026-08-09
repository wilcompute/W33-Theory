# Part CCIV — Tropical Geometry Bridge for W(3,3)

## Theorem (Tropical Geometry Bridge)

*All tropical geometry invariants listed below are derived from the
zero-parameter W(3,3) collinearity graph SRG(40, 12, 2, 4) with no free
parameters.*

---

### W(3,3) Atoms

| Symbol | Value | Meaning |
|--------|-------|---------|
| Q      | 3     | Field order |
| V      | 40    | Vertices |
| K      | 12    | Valency |
| λ      | 2     | Common neighbourhood (adjacent pair) |
| μ      | 4     | Common neighbourhood (non-adjacent pair) |
| Φ₃     | 13    | Collinearity classes / lines |
| EDGES  | 240   | Edge count |

Eigenvalue spectrum of the adjacency matrix:
λ ∈ {12 (×1), 2 (×27), −4 (×12)}

---

### Bridge 1 — Tropical Genus

The W(3,3) collinearity graph, viewed as a tropical curve (metric graph),
has first Betti number

$$b_1 = \text{EDGES} - V + 1 = 240 - 40 + 1 = \boxed{201}$$

The tropical genus g = b₁ = 201 counts the independent cycles of the
spanning tree complement.

---

### Bridge 2 — Tropical Grassmannian Dimension

The tropical Grassmannian Gr_trop(k, n) parametrises tropical k-planes in
tropical n-space. For the natural (Q, V) pair of W(3,3):

$$\dim \operatorname{Gr}_{\mathrm{trop}}(Q, V)
  = Q \cdot (V - Q)
  = 3 \cdot 37 = \boxed{111}$$

---

### Bridge 3 — Tropical Rank (Perfect Matching)

The tropical rank of the adjacency matrix equals the size of a maximum
matching. For SRG(40, 12, 2, 4), which is regular and even-order, a
perfect matching exists:

$$\tau_{\mathrm{trop}} = V / 2 = \boxed{20}$$

---

### Bridge 4 — K-Polygon Lattice Points ↔ Φ₃

A tropical K-gon (convex lattice polygon with K sides) has K + 1 lattice
points on the boundary segment:

$$K + 1 = 12 + 1 = 13 = \Phi_3$$

The collinearity class count Φ₃ = 13 equals the lattice point count of the
tropical K-polygon — a direct combinatorial identification.

---

### Bridge 5 — Tropical Satake Parameters

The tropical Satake parameters of a local L-function are integer shadows
of classical Satake parameters, obtained via floor(log_p(|αᵢ|)).  Using
base Q = 3:

| Eigenvalue λ | |λ| | floor(log₃|λ|) |
|---|---|---|
| 12 | 12 | **2** |
|  2 |  2 | **0** |
| −4 |  4 | **1** |

The three Satake parameters {0, 1, 2} are all distinct and exhausted.

---

### Bridge 6 — Tropical Fan / Spanning Tree Count

By the Kirchhoff Matrix-Tree theorem, using the Laplacian eigenvalues
ν_i = K − λ_i  →  {0 (×1), 10 (×27), 16 (×12)}:

$$\kappa = \frac{1}{V} \prod_{\nu_i \neq 0} \nu_i
         = \frac{10^{27} \cdot 16^{12}}{40}$$

$$\log_{10} \kappa \approx 39.847$$

The tropical fan has approximately $10^{39.85}$ maximal cones, one per
spanning tree.

---

### Bridge 7 — Min-Plus Spectral Radius

For a K-regular graph, the spectral radius under the tropical (min, +)
semiring equals the degree:

$$\rho_{\mathrm{trop}} = K = \boxed{12}$$

---

### Bridge 8 — Dual Tropical Cell Complex Dimension

The dual cell complex of a tropical K-regular curve has cells of maximal
dimension

$$\dim_{\mathrm{dual}} = K - 1 = \boxed{11}$$

---

### Summary Table

| Tropical Invariant | Formula | Value | W(3,3) atom |
|--------------------|---------|-------|-------------|
| Euler characteristic | V − EDGES | −200 | V, EDGES |
| Betti number b₁ / Genus | EDGES − V + 1 | **201** | V, EDGES |
| Gr_trop(Q,V) dimension | Q(V−Q) | **111** | Q, V |
| Tropical rank | V/2 | **20** | V |
| K-polygon lattice pts | K+1 | **13 = Φ₃** | K, Φ₃ |
| Satake {12→2, 2→0, −4→1} | floor(log_Q\|λ\|) | {2,0,1} | Q, eigenvalues |
| log₁₀(spanning trees) | Kirchhoff | **≈39.847** | V, K, eigenvalues |
| Min-plus spectral radius | K | **12** | K |
| Dual cell dim | K−1 | **11** | K |
| Tropical proj dim | V−1 | 39 | V |
| Tropical lines | Φ₃ | **13** | Φ₃ |
| Newton degree | K | **12** | K |

---

### Proof Sketch

Each bridge relies only on the SRG parameter tuple (V, K, λ, μ) = (40, 12, 2, 4)
and the derived constants Q, Φ₃, EDGES — no fitting parameters, no
continuous adjustments.  The tropical Satake computation uses the fact
that the adjacency eigenvalues are integer, so the floor is exact.

Computational verification: all invariants are automatically checked by
`_verify_invariants()` in `exploration/PART_CCIV_TROPICAL_GEOMETRY_BRIDGE.py`;
the full regression suite (71 tests) lives in
`tests/test_tropical_geometry_bridge_cciv.py`.
