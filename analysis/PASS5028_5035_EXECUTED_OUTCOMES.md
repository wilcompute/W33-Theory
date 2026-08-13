# Passes 5028-5035 — executed outcomes

**Status:** EXECUTED on 2026-08-13. The standalone finite verifier is `analysis/w33_pass5028_5035_steinberg_apartments.py`; separate JSON certificates own each result.

**Pass5028.** The 160 flag-covers are the chambers of the W33 C2 building. If `ell` is gallery distance, the integer kernel `R(f,g)=(-1)^ell 3^(4-ell)` takes values `81,-27,9,-3,1` and satisfies `R^2=160R` with zero panel sums. Hence `P_St=R/160` is the rank-81 chamber/Steinberg projector. With Pass5023 this is the existing W33 Hodge H1. Because it depends only on relative chamber position, it lies in the flag-flag corner of the Pass5018 coherent configuration.

**Pass5029.** For the `1620 x 200` apartment/cover incidence matrix `Y`, `rank(Y)=160` and the Gram spectrum is `0^40 + 40^81 + 72^15 + 144^15 + (243-9sqrt409)^24 + (243+9sqrt409)^24 + 1296^1`. Thus the same 81 is the eigenvalue-40 block on the full 200-cover module.

**Pass5030.** The canonical 240-vertex all-edge subdivision has native PGSp orbit profile `40+40+160` and degree profile `4^80+2^160`. It therefore has no PGSp-equivariant identification with a transitive 240-set. This agrees with the older Pass1055 firewall: the unsigned 120-axis E8 bridge is internally equivariant, while the signed 240-endpoint lift is obstructed. No arbitrary set-bijection no-go is claimed.

**Pass5031.** Reduced-Laplacian Smith computation gives `K(Levi)=(Z/4)^6 +(Z/40)^22 +Z/160`. The pendant-cover support graph has the same nontrivial critical group. Full Levi edge subdivision gives `K=(Z/2)^52 +(Z/8)^6 +(Z/80)^22 +Z/320`. Their orders are respectively `2^83 5^23`, `2^83 5^23`, and `2^164 5^23`, matching the corrected Matrix-Tree ledger.

**Pass5032.** The 1620 apartments form one PSp orbit; setwise stabilizers have orders 16 in PSp and 32 in PGSp. Each apartment uses 4 W33 lines, 4 point-covers, 8 flag-covers, 12 total covers, and—using Pass5020—12 line-attached Steiner/K3,3 circuits. Every line, point-cover, and line-attached Steiner circuit lies in 162 apartments; every flag-cover lies in 81. For the apartment/line matrix `B`, `B^T B=156I+21A_line+6J`, with squared singular spectrum `648^1+198^24+72^15`. Pass5018 then gives aggregate apartment/tritangent weight 108 per apartment and 3888 per tritangent; a labeled `1620 x 45` composition is not claimed yet.

**Pass5033.** The cube-complex rational homology representation is `H0=1`, `H1=St_81`, `H2=1+V24+V15`. The H2 statement follows because the 40 cube-boundary spheres are canonically indexed by W33 lines. The virtual Euler representation is `2*1+V24+V15-St_81`, of dimension `-40`.

**Pass5034.** If `X` is the signed `160 x 1620` apartment-cycle matrix, then `rank(X)=81`, every column has norm-squared 8, and exactly `X X^T = R = 160 P_St`. Thus all 1620 apartments form a canonical tight frame for the protected Steinberg/Hodge 81. Every chamber lies in 81 apartments, and pair correlations by gallery distance are `81,-27,9,-3,1`.

**Pass5035.** Three separate 240-object constructions are now explicitly firewalled: the cover subdivision (`40+40+160` native orbits), the signed E8 axis endpoints (Pass1055 signed-lift obstruction), and the 240 individual Steiner trihedra (the earlier cubic-surface verifier records only finite incidence/count resonance). Shared cardinality is not a G-set, graph, or physical identification.

## Synthesis

Pass5023 supplied a chain-level H1 isomorphism. Pass5028 supplies its coherent/Hecke projector, Pass5029 isolates it spectrally on all 200 covers, and Pass5034 supplies an apartment tight frame. The cover/building bridge is therefore represented simultaneously by an explicit chain map, an idempotent, a spectral block, and a frame transform.
