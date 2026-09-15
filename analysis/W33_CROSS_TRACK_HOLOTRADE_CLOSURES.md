# Cross-track closures from Holotrade

2026-09-15. Reproduce with `py -3 analysis/w33_cross_track_holotrade_closures.py`. Stored certificate: `analysis/w33_cross_track_holotrade_closures.json`, status PASS.

Four items this corpus recorded as open or untested were settled on the Holotrade track. The Holotrade commits own the results. This packet re-checks their fast cores inside this repository and updates the claims ledger.

| Item | Before | Now | Owner |
|---|---|---|---|
| CSS distance $d=q+1$ (ledger P326) | open, "$d\le q+1$ only" | **theorem, all odd $q$**; minimum words = lines | Holotrade `7c57f8e` |
| $m=6$ Coxeter–Todd rung (ledger P368/369) | open, "handed to GAP track" | **certified**: $K_{12}/2K_{12}$ singular $=1+378+1701$, a proper shadow in $O^+(12,2)$ | Holotrade `a0ed473` |
| Pass 7289: SRG$(126,45,12,18)$ | recorded, untested | **confirmed**; locally GQ$(4,2)$ + double cover of $Q(4,3)$ | Holotrade `a0ed473` |
| Pass 7294: Leech at $d=9$ gives $W(3,3)$ | "the one to look at", untested | **killed**: no $\Phi_9^4$ class in $2.\mathrm{Co}_1$ | Holotrade `e680b23` |

## What is re-checked here

- **CSS.** The parity lemma and the GQ axiom hold at $q=3,5$. At $q=3$, exhaustive search finds that the words of weight $\le4$ are exactly the 40 lines. $C^\perp\subseteq C$ is doubly even with $k=q^2+1$, and a line is a logical, so the distance is exactly $q+1$. The proof for all odd $q$ lives in Holotrade.
- **$K_{12}$** (Pass 369's hexacode construction). The theta series starts $756, 4032, 20412$. The 126 unit classes of minimal vectors, under orthogonality, form SRG$(126,45,12,18)$. $K_{12}/2K_{12}$ splits by minimal norm as $378+2016+1701$.
- **Leech $d=9$.** Every order-9 class of $\mathrm{Co}_0$ has $\mathrm{tr}(g^3)=-3$, but $\Phi_9^4$ needs $-12$. Class 9b solves to $\Phi_9^3\Phi_3^2\Phi_1^2$.

## Also fixed

`scripts/check_claims_ledger.py` read only `w33_paper.tex`. The ledger had moved into `w33_paper_body.tex` behind `\input`, so the checker printed "no ledger found" and exited 1 whatever the certificates said. It now follows `\input`, and the true baseline is green: 236 rows, 273 certificates, 0 failures.

## Where the tower actually goes

Above E8 the Eisenstein/cyclotomic tower does not return to $W(3,3)$. The fixed-point-free rungs of the Leech lattice are:

| Rung | Geometry | Structure |
|---|---|---|
| 3a | $W(11,3)$ | 32760 unit classes, a 90-tight set for $2.\mathrm{Suz}$ |
| 5a | $W(5,5)$ | 15/16-ovoids for $2.J_2$ |
| 7a | $W(3,7)$ | 15/35-tight sets for $2.A_7$ |
| 13a | $PG(1,13)$ | 6/8 split |

These are Feng–Xiang's two-orbit intriguing sets (arXiv:2310.09460). The acting groups are the Suzuki chain.

The $d=3$ rung is the Leech analogue of P1021's 6:1 fibration $E_8\to W(3,3)$. Its fibre is again $\mathbb Z_6$, but the image is a proper tight set rather than all points.

## Boundary

These are finite exact checks. The lattice, group and intriguing-set facts are classical or published, and are cited in the Holotrade certificates. No physics is asserted.
