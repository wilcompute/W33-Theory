# TOE65 — All-five physics pass, native rational flux falsifier, and topology correction

**Date:** 2026-10-13. **Repository:** wilcompute/W33-Theory. **Starting point:** TOE64 `bc582d83545d5e2d7998ceb153a111a044458d05`, plus the later independent formula-index commit. **Work discipline:** separate clean worktree; no overwrite of uncommitted master changes; exact claims distinguished from numerical evidence and physical interpretations.

## Executive finding: an actual W33 counterexample and a necessary retraction

1. **CERTIFIED counterexample:** For actual native W33 edge-product amplitudes in `[1-245/1000,1+245/1000]`, a 160-bit assignment of endpoint values makes the exact Hessian of the *leading* beta^7 flat-holonomy potential at `(pi,pi,pi)` have a negative Rayleigh quotient. Thus three-pi is NOT always a local minimizer under 24.5% independent link disorder. TOE64's proof remains valid *through* 14.875640159%; the universal worst-case threshold is bracketed by `0.14875640159021247 <= e* < 0.245`. The explicit rational 160-edge pattern, 3-vector, integer polynomial, and exact integer witness are frozen in `data/w33_20261013_toe65_exact_edge_disorder_bracket.json`.

2. **RETRACTION of BT1643:** The triangular W33 clique two-skeleton has Euler characteristic -40, but **is not a genus-21 surface**. Each of the 40 vertex links consists of four *disconnected* triangles, not a single circle. Its GF(2) Betti numbers are `[1,81,40]`; the full tetrahedral complex has `[1,81,0,0]`. Both follow from the exact 40 tetrahedral K4 blocks glued at W33 points and the connected 40+40 point-line incidence graph with 160 edges, whose circuit rank is 81. The old `BT1643_css_boundary_genus21.py` banner and printouts now explicitly retract the surface/genus-21 toric-code interpretation but retain the historical arithmetic. This does not overturn the separate tested CSS `[[240,81,3]]_3` construction; it removes an unproved **surface-code interpretation** claimed in BT1643.

## Front 1: all-beta continuous flat U(1)^3 flux falsification campaign

`analysis/w33_20261013_toe65_thermal_continuous_falsifier.py` computes the complete native 80x80 Hermitian free-fermion hopping spectrum at five regimes (beta=.25,.5,2,8 and zero-temperature) with 256 seeded Sobol holonomy points, eight local BFGS starts per regime, and explicit conjugation cross-checks. Among these finite tests, no lower free-energy state than three-pi was found. In particular at beta=2, `F(pi)-F(0)~-0.2744521663`; at beta=8, `~-1.2834768922`; at zero-temperature, `~-1.8020262751`.

**OPEN:** no global all-beta continuous determinant theorem; no integration over the gauge field. These tests are not a continuum-QFT prediction. E. Lieb's 1994 flux-phase theorem has *planar/periodicity* hypotheses that must not be transplanted wholesale to the W33 three-deck geometry (Phys Rev Lett 73, 2158, DOI 10.1103/PhysRevLett.73.2158). Goller and Porta (J Stat Phys 193:60, 2026, DOI 10.1007/s10955-026-03617-y) cover a different 2D dynamical Z2 model with zero electric coupling.

## Front 2: authentic 4D chirality prerequisite and positive topology control

The TOE38 native octagonal two-complex has verified mod-2 cellular Betti profile `(1,3,1304)` (`V=80,E=160,F=1382`, ranks `d1=79,d2=78`); the independent producer recomputes `d2` from all actual octagon boundary rows rather than trusting a summary. Over `F2`, Kunneth gives

```
b(X x S1)  = (1,4,1307,1304),           b4=0,
b(X x T2)  = (1,5,1311,2611,1304),     b4=1304.
```

Thus the time-only product lacks 4-cells/top fourth homology, while the naive double-circle product is not a connected closed 4-manifold: such a manifold has `dim H4(-;F2)=1`, not 1304. This does **not** rule out a replacement/refinement or attached higher cells.

An independent non-W33 4-torus cohomological **positive control** has `c1=m dx1^dx2+n dx3^dx4`, `(1/2)int c1^2=mn=1` at `m=n=1`. It confirms which additional topology would support nontrivial gauge topology, but it is not a W33 overlap-Dirac index, a 4D field configuration, or an anomaly-free Weyl Standard Model. Relevant rigorous backdrop: Lüscher's admissible overlap gauge field program and subsequent lattice-family index analyses (e.g. DOI 10.1016/S0550-3213(02)00567-9 and Phys Rev D73, 014503).

## Front 3: spatial geometry and the 19-new-edge obstruction

With unchanged 80 native vertices, 160 native links, degree4 and selected octagonal faces, a closed 3D cellulation with **simple** vertex links has 8F face corners but capacity at most 480. Closed Euler with nonempty 3-cells requires `F>=81`, hence a 168-corner deficit.

Allow `e` **new simple edges connecting existing vertices**, and let `s_v` be added degree. Corner capacity becomes `480+8e+sum_v C(s_v,2)`, while Euler requires at least `648+8e`. Therefore `sum_v C(s_v,2)>=168`; pairs of new distinct edges can meet at most once, so `C(e,2)>=168`, requiring `e>=19`. Nineteen is **necessary, not sufficient**. The proof does not cover new vertices, shorter faces, multigraph local links or other CW constructions.

More severe: the historical 40-point *triangular* clique skeleton also fails the surface local-link condition (independent theorem above). This explains why arithmetic `g=21` was not enough to create spatial geometry.

## Front 4: dynamical Gauss–matter truncation convergence

The independent `analysis/w33_20261013_toe65_three_loop_cutoff_grid.py` extends the original native 14-site/16-link three-loop Gauss-exact Hamiltonian in both neutral and static charged sectors. New configurations:

| Fock depth | flux L | basis dimension / sector | neutral E | charged E | neutral Fock-boundary weight | neutral flux-boundary weight |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 2,125 | -1.115600 | -0.810418 | .42038 | .00887 |
| 2 | 3 | 38,759 | -2.262535 | -1.939401 | .20405 | .000104 |
| 3 | 2 | 52,125 | -2.776032 | -2.436503 | .09035 | .02003 |

Twelve cross-comparisons verify variational energy monotonicity under nesting of the two independent cutoffs, both charge sectors. Every eigensolver residual is below 1e-5. Under the code's convention, electric `g^2*n^2/2>=0` and each magnetic `beta/g^2(1-Re U)>=0`, while the fermion hopping operator norm is bounded by `16*kappa` and staggered on-site contribution by `6*m`. Thus `E_full_patch >= -16(0.7)-6(0.3)=-13` gives a **rigorous but loose** lower bound. Finite Galerkin energies are upper bounds **for each individual sector**; their differences are not rigorous charge-gap bounds. The Fock-depth sensitivity persists and the full model is not solved.

Compare Ciavarella et al., `Truncation uncertainties for accurate quantum simulations of lattice gauge theories`, arXiv:2508.00061 (2025, revised 2026), on quantitative electric-basis truncation errors. Their estimates are not automatically valid for this W33 patch.

## Front 5: exact native disorder-bracket theorem

Unlike TOE63/64's independent Fourier-coefficient interval relaxations, the new explicit simple-cycle script reconstructs **all 238 noncontractible length-eight simple cycles as 238x160 edge-incidence vectors**. For each weighted native cycle `c`, the contribution to the Hessian at pi is `sgn_c prod_{e in c}w_e * winding(c)*winding(c)^T`.

It is **multi-affine in each edge magnitude**. Since `lambda_min` is concave along any one edge coordinate, its minimum over the compact box is achieved at a vertex: it suffices in principle to search `2^160` binary corner assignments to locate the worst local-stability Hessian. This reduction is exact, **not** a claim that all corners have been enumerated.

An optimizer supplied one such candidate at 30% deviation. Rounded to actual rational weights `7/10` and `13/10`, the binary native edge assignment has exact negative integer Rayleigh. For the fixed assignment, reuse the same high/low bits at continuously varying epsilon. The integer test direction is `q=(12,710,-704)`; the Rayleigh polynomial is

```
P(e) = sum_{j=0}^8 A_j(1+e)^j(1-e)^(8-j),
A = [0,6048,34489848,24498148,17516456,-521140,0,0,-5998188].
```

Its numerical first root on this fixed direction is `e≈0.24467014432769635`. Crucially, **exact arithmetic at rational `e=245/1000`** gives

```
1000^8 * P(245/1000)
= -119579006159618433637710937500 < 0.
```

This proves a **native W33 edge-product** negative Hessian Rayleigh and therefore three-pi is not even a local minimum of the leading beta^7 flat-holonomy potential for these permitted positive edges. A separate regression reconstructs this exact polynomial and cross-checks the actual native weighted **80x80 trace-H^8** phase difference against the 238 cycle sum.

Hence the universal disorder guarantee remains rigorously established for `e<=0.14875640159021247...`, and necessarily fails by `e=0.245`. The true minimax tolerance **inside that interval remains OPEN**, as does every-beta/disorder gauge dynamics.

## Reproducibility and status discipline

Producer scripts:
- `analysis/w33_20261013_toe65_surface_topology_correction.py`
- `analysis/w33_20261013_toe65_spacetime_admission_gates.py`
- `analysis/w33_20261013_toe65_thermal_continuous_falsifier.py`
- `analysis/w33_20261013_toe65_three_loop_cutoff_grid.py`
- `analysis/w33_20261013_toe65_edge_product_adversary.py`
- `analysis/w33_20261013_toe65_exact_edge_disorder_bracket.py`

Six matching `data/w33_20261013_toe65_*.json` certificates; dedicated `tests/test_w33_20261013_toe65_five_fronts.py` cross-checks the native integer witness, topology, truncation, finite beta search, and 80x80 weighted spectral moment. Historical `BT1643_css_boundary_genus21.py` corrected. The distinction between `CERTIFIED`, `NUMERICAL`, `CONDITIONAL`, `RETRACTED`, and `OPEN` is retained.

**The Theory of Everything is not solved.** A physical 3+1-manifold, nonzero native overlap index, anomaly-free Weyl measure, controlled gauge–matter thermodynamic limit, first-class gravity, and measured parameter-free predictions remain missing.
