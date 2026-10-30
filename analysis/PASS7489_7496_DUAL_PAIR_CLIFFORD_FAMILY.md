# Passes 7489–7496 — dual-pair α separation, Clifford L/R boundary, the W33 family

**Certificate (PASS, deterministic, pure Python/NumPy):**
`analysis/w33_pass7489_7496_dual_pair_clifford_family.py` →
`data/w33_pass7489_7496_dual_pair_clifford_family.json`

## S1 — the α correction, made definitive

Both cospectral mates of SRG(40,12,2,4) were built and their independence numbers
computed exactly:

- $\alpha(W(3,3)) = 7$ (no ovoid; $q$ odd)
- $\alpha(Q(4,3)) = 10$ (ovoid exists)

The "α = 10" in `analysis/w33_lovasz_independence_clique.py` and the closure package
(T201/T229) is true only of the **dual** $Q(4,3)$. For $W(3,3)$, $\alpha = 7$ and 10 is
merely the Lovász theta bound $-vs/(k-s) = 160/16$. The "α = 10 = superstring critical
dimension" claim inherits the conflation and should be re-audited.

## S3 — the Clifford L/R boundary (MDCLXXXI), pinned

The 36 Clifford L/R cross-pairs form a 6×6 grid (6 L-families × 6 R-families); the
natural scheme is the rook graph **SRG(36,10,4,2)**, spectrum $\{10^1, 4^{10}, -2^{25}\}$
— entirely different from the spread scheme **SRG(36,15,6,6)** $\{15^1, 3^{15}, -3^{20}\}$.
Count-equal (36), scheme-different: the MDCLXXXI boundary is confirmed with both schemes
written explicitly.

## S4 — the family of W(3,3)s is real

- $\rho$ and $\rho^2$ give the **same** 40 Eisenstein lines (the $\{J, J^2\}$ pairing).
- A Weyl-conjugate of $\rho$ gives a **different** 40-line set (0 shared $A_2$s).

The family is real. The full count (4480 fixed-point-free order-3 elements → 2240
copies) is the other lane's Springer/$G_{32}$-centralizer computation; this pass
confirms the underlying pairing and non-triviality structurally.

## Honest boundary

- **S2 (third 1440):** Brosowsky's $20 \times 72 = \binom{6}{3} \times 72$ is a count,
  not an asserted group action; note $1440 = |\mathrm{Aut}(S_6)|$. Not folded in.
- **S5 ($\alpha(W(3,9))$):** still open. The perp-$E_6$ identification (a point is an
  $E_6 \times A_2$ maximal subgroup) is a structural lever, not a solution.
