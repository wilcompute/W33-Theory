# Passes 4245–4252 — residual symmetry, GHZ operating point, exact minimum Hodge sensing, routed delay geometry, subgroup lattice, and three outside-box probes

Status: `PASS_EXACT_RESIDUAL_ANCHOR_SYMMETRY_GHZ_RESOURCE_MIN_TWO_HODGE_ROUTE_GEOMETRY_TRIPLE_STRATA_METROLOGY_EXERGY_QUOTIENT_RG`

Exact packet SHA-256: `267198b8b02374007865d5c9a3cb52b72f18fb221e886b296ff9047432e55a1f`.

## Pass 4245 — five-generation residual symmetry target

Pass 4205 proved that five complete standard-charge generations are the largest sector keeping both nonabelian Weyl-only one-loop beta coefficients positive, but full original `PSp(4,3)` covariance is impossible. Pass 4245 asks a weaker, concrete question: if the five generations are represented by five unlabeled anchors in the natural 40-point W33 action, what anchor scaffold has the largest setwise stabilizer?

All `C(40,5)=658008` five-subsets split into 43 `PSp(4,3)` orbits. The unique maximum stabilizer has order 72 and orbit size 360. A representative is `[0,1,4,5,6]`; its induced graph is `K_{1,4}`. The stabilizer fixes the star center, induces `A4` on the four leaves, and has a central pointwise kernel `C6`.

This is an anchor-level subgroup target, not yet a branching theorem for the complete 75-state charged `H145` subspace.

## Pass 4246 — GHZ28 operating strategy

The heap binary tree on payload qubits 0..27 cannot be generated in four physical CNOT rounds when simultaneous gates sharing a parent are forbidden. Exact broadcast dynamic programming gives a minimum of seven matching rounds for its 27 edges, and an explicit seven-round schedule is frozen in the ledger.

At the published Huang et al. dual-rail CNOT operating point (`F_proc=0.981`, erasure probability `0.13`), direct whole-circuit postselection accepts `0.87^27 = 0.0232819751` of runs. If the entire state is restarted after a heralded erasure, the model costs about 1159.7 entangler attempts per accepted GHZ28. An optimistic local-edge retry limit is 31.03 attempts. Even a pessimistic dynamic program in which a failed fusion destroys both prepared input blocks needs only 47.91 expected entangler attempts, with optimal top split 13+15.

Heralded modular fusion therefore attacks yield effectively, but not conditional infidelity: `0.981^27 = 0.59575`. A 90% naïve 27-gate product requires per-entangler conditional fidelity at least 99.6105%.

Hung et al. (arXiv:2604.16292, 2026) provide a complementary fast erasure-detection reference: 384 ns single-shot checks, residual error `6.0e-4` per check, induced dephasing `8e-5`, and erasure error `2.54e-2`. The packet treats those as external experimental inputs, not as a demonstrated GHZ28 protocol.

## Pass 4247 — the true minimum is two global Hodge channels

The ten-channel Pass 4207 result was a conditioning result in one orthonormal projection family, not an information-theoretic minimum.

For seven-sparse arbitrary-real edge errors, one global scalar row beyond the oriented Levi incidence matrix can never suffice. The incidence nullspace contains 2D theta circulation spaces supported on at most 14 edges; every linear map from such a 2D space to one scalar has a nonzero kernel vector. Hence any one-row augmentation has spark at most 14.

Two rows do suffice: the deterministic centered integer rows from Pass 4147 were exhaustively audited on 386,964 simple cycles and 133,920 theta cores, proving stacked spark at least 15. Therefore the exact noiseless minimum is `m_min = 2`.

The two-channel theorem is about injectivity. Ten orthonormal H1 channels remain useful because they provide a chosen finite conditioning margin; 81 H1 channels give the globally conditioned arbitrary-amplitude decoder.

## Pass 4248 — explicit routed delay centerlines

The exact Pass 4148 branch schedule assigns delay `d=8-layer`. Across all 160 point-line routes this reproduces exactly the Pass 4208 histogram and 919 delay-slot units.

Each 5 ps delay slot is represented by a rounded rectangular dogleg with four 90-degree bends of radius 50 micrometres. With slot excess path `L=0.749481145 mm`, the required vertical centerline excursion is `h=[L-(2*pi-4)r]/2=0.31766093982051036 mm`.

The deterministic layout contract uses 0.36 mm lane pitch and 0.12 mm dogleg x-pitch. It leaves 42.339 micrometres centerline gap between a dogleg crest and the next lane baseline, has maximum dogleg span 0.96 mm, maximum excess path 5.99584916 mm, and a 40-lane branch delay tile of 14.4 mm by 0.96 mm before ports/keepouts.

`analysis/w33_pass4248_route_centerline_generator.py` emits all 160 route identities and their cell coordinates from the frozen Pass 4148 schedule. This is a centerline contract, not proprietary foundry DRC.

## Pass 4249 — next rank of the nonlinear stabilizer lattice

The 9,880 three-vertex subsets of W33 form exactly five `PSp(4,3)` orbits: triangle (stabilizer 162), independent-A (72), path P3 (12), independent-B (9), and edge-plus-isolated (6).

The two smallest quotient systems were interval/Krawczyk exhausted. Triangle: selector 24 has 9 roots with full-space Morse indices `20^2 22^2 23^4 24^1`; selector 15 has 3 roots with `14^2 15^1`. Maximally symmetric independent triple: selector 24 has 9 roots with `17^4 18^2 23^2 24^1`; selector 15 has 9 roots with `9^2 13^2 14^4 15^1`.

Together with the already exhaustive point, edge-pair and nonedge-pair strata, this closes another finite layer of the subgroup lattice. Three larger triple quotients and trivial-stabilizer equilibria remain open.

## Pass 4250 — outside box: symmetry-resolved metrology

For phase encoding generated by W33 adjacency `A`, pure-state quantum Fisher information is `F_Q=4 Var(A)`. Since the spectrum is `{12,2,-4}`, the exact global maximum is `F_Q,max=256`, attained by equal weight in the extremal 12 and -4 sectors. A localized vertex probe has `F_Q=48`, giving an exact finite-generator QFI ratio `16/3` before resource/noise accounting.

## Pass 4251 — outside box: Hodge two-temperature exergy

The Levi edge space splits into 81 harmonic-cycle modes and 79 gradient modes. In a classical unit-stiffness Gaussian quadratic model, reversible entropy-conserving equalization from temperatures `T_H,T_G` gives `T_*=T_H^(81/160) T_G^(79/160)` and `W_max=(k_B/2)[81T_H+79T_G-160T_*] >= 0`. For `T_H/T_G=2`, `W_max/(k_B T_G)=6.8717227425`. This is an exact finite Hodge exergy ledger, not a fabricated heat engine.

## Pass 4252 — outside box: exact quotient renormalization chain

Use pointwise stabilizers along `point 0 -> ordered edge (0,1) -> ordered triangle (0,1,2)`. Their orders are 648, 54, 27 and quotient dimensions are 3, 6, 8. With refinement lifts `R63,R86`, direct verification gives `Q6 R63=R63 Q3` and `Q8 R86=R86 Q6`. Every adjacency polynomial therefore intertwines exactly. Because each lift has one `1` per row, componentwise cubing also commutes with lifting, so the project's cubic nonlinear vector field closes exactly along the chain.

## Evidence boundary

All promoted results are finite exact group/orbit, linear-algebra, graph, interval, routing-geometry, resource-model, QFI, Gaussian-thermodynamic, or equitable-partition statements, except the explicitly external experimental operating points used in Pass 4246. No phenomenologically viable gauge theory, fabricated GHZ28 processor, proprietary DRC-clean photonic chip, globally complete 80D nonlinear theorem, measured metrological advantage, physical heat engine, continuum RG, gravity, cosmology, or theory of everything is claimed.
