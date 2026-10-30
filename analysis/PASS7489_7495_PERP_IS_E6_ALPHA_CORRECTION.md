# Passes 7489–7495 — perp-is-E6 (coordinate verification) + the α = 10 → 7 correction

**Certificate (PASS, deterministic, pure Python/NumPy):**
`analysis/w33_pass7489_7495_perp_is_e6_alpha_correction.py` →
`data/w33_pass7489_7495_perp_is_e6_alpha_correction.json`

## Perp-is-E6, independently verified with explicit coordinates

Cross-checks Pass7253–7260 (other lane) using the explicit Eisenstein bridge of
Pass7385–7392. For **all 40 points, no exceptions**:

- The roots of $E_8$ orthogonal to a point's $A_2$ line number exactly **72**, span
  rank 6, and are closed under reflection — an $E_6$ root subsystem.
- That $E_6$ is exactly the union of the $A_2$s of the **12 collinear** points
  ($12 \times 6 = 72$).
- The 240-split is a statement about the quadrangle:
  $$6 \text{ (own } A_2) + 72 \text{ (12 collinear)} + 162 \text{ (27 non-collinear)} = 240.$$
- A point's own $A_2$ (6) plus its perp $E_6$ (72) $= 78$ roots $=$ the
  $E_6 \times A_2$ **maximal subgroup** of $E_8$; the 162 non-collinear roots are the
  mixed $(27,3) \oplus (\bar 27, \bar 3)$ part.

## Correction: α = 10 → 7

$\alpha(W33) = 7$ exactly (Pass4797, Pass7106–7113, and the Eisenstein bridge agree);
the Lovász theta is only the upper bound $-vs/(k-s) = 160/16 = 10$. The "α = 10" still
present in `analysis/w33_lovasz_independence_clique.py` and the closure package
(T201/T229) conflates the independence number with its Lovász bound — and the
"α = 10 = superstring critical dimension" claim built on it should be re-audited.

## Note on the 36 spreads ↔ 36 double-sixes

My independent computation this session confirmed both are SRG(36,15,6,6) and
isomorphic, with both transitive $G$-sets for $G = P\Omega(5,3) \cong PSp(4,3)$
(order 25920) with $S_6$ stabilizer (720). This is an **independent confirmation**, not
a new result: the explicit isomorphism witness is already MCCCXCIV (2026-05-28), and
Pass7245–7252 re-derived it. The $G$-set framing (shared simple group, $S_6$
stabilizer) is the only incremental note; priority is MCCCXCIII/MCCCXCIV.
