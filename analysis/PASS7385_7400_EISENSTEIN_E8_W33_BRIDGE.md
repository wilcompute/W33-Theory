# Passes 7385–7400 — the Eisenstein E8 → W(3,3) bridge, explicit and corrected

**Certificates (all PASS, deterministic, pure Python/NumPy):**
- `analysis/w33_pass7385_7392_eisenstein_e8_to_w33.py` → `data/w33_pass7385_7392_eisenstein_e8_to_w33.json`
- `analysis/w33_pass7393_7400_e8_w33_followups.py` → `data/w33_pass7393_7400_e8_w33_followups.json`

---

## Main theorem (every step machine-verified)

The 240 roots of $E_8$ become the 40 points of $W(3,3)$ as follows.

1. **Eisenstein structure.** $\rho = c^{10}$, where $c$ is an $E_8$ Coxeter element
   (order 30), is a fixed-point-free order-3 lattice automorphism with
   $1+\rho+\rho^2 = 0$ and characteristic polynomial $\Phi_3^4 = (x^2+x+1)^4$.
   It is multiplication by $\omega$ for a $\mathbb{Z}[\omega]$-module structure on $E_8$.
2. **40 Eisenstein lines.** The 240 roots split into exactly **40** orbits under the
   unit group $\langle -1, \rho\rangle \cong \mathbb{Z}_6$ (the Eisenstein units).
3. **Collinearity = orthogonality.** Two lines are collinear iff their $\rho$-invariant
   real 2-planes are orthogonal. The resulting graph is **SRG(40,12,2,4)** with
   spectrum $\{12^1, 2^{24}, -4^{15}\}$.
4. **It is genuinely $W(3,3)$.** The 40 four-cliques satisfy the $GQ(3,3)$ axioms
   (40 lines, 4 points/line, 4 lines/point, unique-line axiom), and the independence
   number is $\alpha = 7$ — selecting $W(3,3)$ over the dual $Q(4,3)$ (which has
   ovoids, $\alpha = 10$).
5. **Explicit $F_3^4$ coordinatization.** A $\mathbb{Z}[\omega]$-basis reduces mod
   $\pi = (1-\omega)$ to 40 distinct points of $PG(3,3)$, with an explicit
   non-degenerate symplectic form $J$ over $\mathbb{F}_3$ ($\det J = 1$) such that
   collinearity $\iff$ symplectic orthogonality.

This independently verifies the GAP-only Pass1020/1021 fibration certificate and adds
the explicit adjacency rule, the explicit $\rho$, and the $F_3$ coordinatization.

## Correction to PART_CCCCCXCIX

The latest-commit claim that the spectral descent "determines the W33 vertex count
(33) = 27+6" is **false**:

- $W33 = W(3,3)$ has **40** vertices, not 33.
- The iterated local-subgraph chain of the $E_8$ root graph is the Gosset–Elte chain
  $$240 \to 56 \to 27 \to 16 \to 10 \to 6$$
  ($E_8$ root graph, Gosset $3_{21}$, Schläfli $2_{21}$, Clebsch $1_{21}$, $T(5)$,
  triangular prism). It never contains 40 or 33.
- The bridge is a lattice ring-reduction $E_8 \to \mathbb{Z}[\omega] \to \mathbb{F}_3$,
  **not** a graph covering: $\operatorname{spec}(W33) = \{12, 2, -4\}$ does not embed in
  $\operatorname{spec}(\text{root graph}) = \{56, 28, 8, -2, -4\}$ (12 and 2 are absent),
  so no spectral-descent / equitable-partition argument can produce W33 from the root graph.

The "33" appears to be cross-contamination from the concurrent $\alpha(W(3,7)) = 33$
ovoid frontier. The antipodal quotient of the root graph is SRG(120,56,28,24)
(spectrum $\{56^1, 8^{35}, -4^{84}\}$), also not W33.

## Follow-ups (Passes 7393–7400)

- **S2 — Reconciliation of the two 240-decompositions.** Each Eisenstein line is an
  $A_2$ root hexagon ($v \cdot \rho v = -1$): 3 antipodal axes × 2 endpoints. Hence
  $40 \times 6 = 40 \times (3 \text{ axes}) \times (2 \text{ endpoints})$, so the
  Eisenstein fibration and the Pass1041 axis-glue $40 \times 3 \times 2$ fibration are
  the **same** fibration.
- **S3 — D4 subsystems.** $E_8$ has $3150$ $D_4$ subsystems
  ($240 \text{ roots} \times 2520 \text{ diagrams} / |W(D_4)| = 192$). Exactly **90** are
  $\rho$-invariant (unions of 4 Eisenstein lines) — precisely the 90 "C6-supported" D4s
  of Pass7353–7360. The 40 GQ lines (24 roots each) are **not** $D_4$ subsystems: the
  W33 line structure and the D4 triality structure are complementary 24-root decompositions.
- **S4 — Closure-package correction.** T201/T229 list $\alpha(W33) = 10$; the exact value
  is $\alpha = 7$ (Pass7187, this session). 10 is only the Lovász theta bound
  $-vs/(k-s) = 160/16$, not the independence number. Downstream Shannon-capacity claims
  inheriting $\alpha = 10$ should be re-audited.
- **S5 — Shared smallest eigenvalue $-4$.** Eigenspace dimensions: W33 $= 15$
  ($=$ doily $W(2,2)$ points), $E_8$ root graph $= 84$, antipodal SRG(120,56,28,24) $= 84$.
  Since $84/15$ is non-integral and the Eisenstein quotient is non-spectral, the $-4$
  sharing is structural (both are $-4$ geometric graphs), not a spectral reduction.
