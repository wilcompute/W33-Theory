# 2026-10-09 — Five follow-on TOE attacks: exact spectral-SOS obstruction, raw Z6 catalog audit, current fluctuations, factorial optics, explicit 3D cycle quotient

**Research context.** Read live W33 master at the start of this pass (prior `2d5389fec`), preserved unrelated dirty files and the already-verified Pass11778 compact-resolvent theorem, Pass11786 rational 11-state ground-energy upper bound `E0<127.595507`, Pass11793 full-field order-four parity action, BT1688 irreducible 81-dimensional Levi H1, and the preceding exact all-order eleven-one-outsider heterotic charge sieve. This packet has five original incremental outputs and clear failed/provisional paths.

The subject is a proposed mathematical Hamiltonian and geometry, not an experimentally validated Theory of Everything. Numerical lower bounds, the true full ground-state representation and actual heterotic F-flatness are still open.

## A. Quantum spectral lower gap: an exact no-go for a tempting simple SOS

Try constructing a numerical `H>=c>0` from a scalar linear combination of the 160 incidence currents, via `sum_e J_e² >= (sum_e w_e J_e)²/(sum_e w_e²)`. For `J_e=(V_e q+a)(U_e p+a)`, `a=1/sqrt20`, its quadratic principal symbol is `(V_e q)(U_e p)`. If a weighted sum became a nonzero scalar operator, its quadratic symbol would vanish.

Compute the exact integer Gram of the 160 rank-one symbols `V_e tensor U_e`, with `40V_e,40U_e` integer:

```
K_ef=((40Ve).(40Vf))*((40Ue).(40Uf))
    = 6400 J_160 + 2304000 A_linegraph + 9728000 I_160.
```

The line graph is the line graph of the 4-regular bipartite 80-vertex W33 Levi graph, whose adjacency spectrum is `{4^1,sqrt6^24,0^30,-sqrt6^24,-4^1}`. Hence the full **exact Gram spectrum** is

```
5120000 (multiplicity 81)
14336000 - 2304000 sqrt6 (24)
14336000 (30)
14336000 + 2304000 sqrt6 (24)
24576000 (1).
```

All 160 eigenvalues are positive, with **exact minimum 5,120,000**, and the 160 current quadratic symbols are therefore linearly independent. There is **no nontrivial weighted linear current sum that equals a scalar**; this simple linear-current Cauchy/SOS strategy cannot produce the desired positive scalar gap certificate. It does **not** rule out nonlinear sum-of-squares, explicit coercivity inequalities, harmonic-analysis estimates, or representation-theoretic spectral bounds. In particular it is NOT a lower bound `E0>=5120000`! The number belongs to a *Gram matrix of current symbols*, not the physical spectrum.

Producer `analysis/w33_20261009_linear_current_scalar_SOS_obstruction.py` and exact-identity result JSON. Full numerical lower bound for `H` and the distinct excitation gap **remain unsolved**.

## B. Actual string selection rules: original-file coverage audit rather than ungrounded F-flatness

The 11 previously found gauge-neutral one-outsider monomials are exhaustive **at any degree** for the specified support because the six rational nine-U1 charge vectors are independent. However, gauge neutrality and a `k mod6` twist-sector check are only necessary criteria.

From the user's actual orbifolder WSL model `Z6II_34__SM_20260917_1558`, inspected and SHA-256 fingerprinted three raw catalogs:

- `.dbd` contains 170 C-records; **zero** exact multiset matches to the eleven candidate monomials.
- `.mu` contains 51 C-records; **zero** matches.
- `.ch` contains 369 records, but zero C-records under the same parser.
- The `.sp` spectrum records contain all **17 named fields** appearing among the eleven monomials, with twist-sector labels and charges. The `.w` gauge-weight export has only **24 distinct field names** and **none** of those 17 fields, so it does not supply their internal quantum/fixed-point/oscillator metadata.

**Essential boundary:** The `.dbd` and `.mu` exports are NOT proven to be complete superpotential catalogs; their absent matches cannot be construed as string selection-rule exclusions. Existing `.sp` data alone cannot establish space-group fixed-point selection, H-momentum/R-charge, gamma, oscillator and instanton consistency. Kobayashi et al., *Revisiting Coupling Selection Rules in Heterotic Orbifold Models*, arXiv:1107.2137, explicitly discusses additional rules beyond naive gauge/R/space-group filters. The next necessary step is generating/verifying a full 17-field CFT/fixed-point record before claiming F-flatness.

Producer `analysis/w33_20261009_heterotic_coupling_catalog_probe.py`, with raw-file hashes, coverage and all exact multiset results stored in JSON. This is a **documented data blockade**, not a completed eleven-coupling determination.
## C. Actual W33 curvature: nonzero exact quantum noise in a T-even Gaussian

Use the 160 actual Weyl-ordered W33 currents on the 78 active Schrödinger coordinates, not a toy qubit replacement. For adjacent incidence currents, let `b=U_e.V_f=U_f.V_e`, `X_e=V_e.q+a`, `Y_e=U_e.p+a` and `C_ef=i[J_e,J_f]=b(X_e Y_f-X_f Y_e)`, which is precisely Hermitian because the crossed-ordering constants cancel.

In the normalized centered *isotropic* Gaussian `psi(q)∝exp(-||q||²/2)` on the projected 78 coordinates, `<C_ef>=0`. Its quantum variance requires both ordinary Gaussian Wick contractions and the operator-ordering (Moyal) term:

```
R = Ve Uf^T - Vf Ue^T
Var(C_ef) = b²/4 [||R||F² + tr(R²)]
          + b² a²/2 [||Ve-Vf||² + ||Uf-Ue||²].
```

Exact rational evaluation on all **480** adjacent unordered pairs yields `Var(C_ef)=41/20` for each of the **240 shared-point** and **240 shared-line** pairs, despite zero mean. This proves the operator has nonzero quantum fluctuations in an explicit normalizable finite-energy test state. It is consistent with the full-group twirl selection rule. It does **not** determine the actual ground eigenspace's irreducible group representation, ground multiplicity, first excited gap or susceptibility.

Producer `analysis/w33_20261009_isotropic_curvature_fluctuations.py` with fraction-exact pair-orbit count and variance certificate.

## D. Photonic false-positive discrimination: randomized 2x2 factorial control

Define two independently randomized binary switches per shot: pump sign `S_i∈{±1}` and nonlinear-gate enable `G_i∈{±1}` (on/off); read a two-mode homodyne statistic `W_i=P_X,i(P_Y,i²-v_Y)`. Use factorial interaction score `T=sum G_i S_i W_i`. In expectation this cancels *pump-only* and *gate-only* nuisance terms while preserving a true signal that requires *both* pump sign and the gate. Under the strong **sharp gate-null** that switching G changes no readout, conditional on S and all observed W, independent balanced G makes the finite-N Hoeffding test

```
reject if |T| > sqrt(2 log(2/alpha) sum W_i²)
```

have type-I error ≤alpha even for temporal correlations in W. It does not guarantee type-I error under a *physical-only no-gate* null when gate switching changes electronics or optics.

Seeded simulation at 50,000 shots per replicate, 96 replicates per arm, alpha=1%, AR(1) drift rho=.98, independent electronics and a strong **pump-sign-dependent** spurious response, gave:

- Pump-only artifact with no gate interaction: **0 / 96** rejections.
- Idealized gate-and-pump nonlinear signal: **88 / 96** rejections.
- Detector artifact proportional to gate*sign, with **no actual nonlinear optical gate**: **96 / 96** false physical detections.

The final control is deliberately a **failed causal inference**: a gate*sign artifact remains observationally indistinguishable in this two-factor data alone. A third independent reference or sham-gate/bypass mechanism is needed. No real photonic nonlinear gate, genuine device shot data or guaranteed alternative power is claimed.

Producer `analysis/w33_20261009_factorial_optical_gate_control.py`, parameter/seed JSON.

## E. Symmetry-broken 3D quotient: explicit integral period matrix

The full `PSp(4,3)` action on W33 Levi `H1(G,Z)≈Z^81` is absolutely irreducible over C (existing BT1688 theorem), excluding any full-equivariant rank-three quotient. This pass used the actual **25,920-element** projective symplectic group to compute edge and vertex orbits for marked-point stabilizers. The exact finite-subgroup fixed-rank formula `dim H1^H = #edge orbits - #vertex orbits +1` gives:

| Preserved subgroup | Order | H1-fixed rank |
|---|---:|---:|
| Single-point stabilizer | 648 | 0 |
| Ordered-two-point stabilizer | 54 | 2 |
| Unordered-two-point stabilizer | 108 | 1 |
| Ordered-three-point stabilizer | 27 | **3** |
| Ordered-four-point stabilizer (this chosen tuple) | 27 | **3** |

More than a character census, an independent producer builds a spanning-tree basis of all 81 integral fundamental cycles, the **16 edge orbits** under the order-27 pointwise three-point stabilizer, and three invariant orbit-sum cochains. Their exact integer period matrix has shape **3x81**, full row rank three and a **3x3 minor of determinant +1**. Consequently, there exists an **explicit surjective Z-linear, stabilizer-equivariant** map `H1(G,Z) -> Z^3` with trivial action on the quotient.

This is a serious constructive bridge between W33 symmetry-breaking and an integer three-dimensional quotient. It is NOT a prediction of physical spatial dimension or a dynamical breaking mechanism: the marked three points are externally chosen, and no universal speed, Lorentz signature, background independence or Einstein equations follow.

Producers `analysis/w33_20261009_symmetry_broken_cycle_quotients.py` and `analysis/w33_20261009_triple_point_integral_3D_quotient.py`; output JSON includes 16 orbit sizes, three selected edge orbits, full 3x81 period matrix and exact unimodular minor.

## Scope of completed five-front execution

All five fronts were explored with original code and explicit checks, but two original *physical deliverables* (full lower quantum spectral gap and full worldsheet F-flatness) remain open. The goal of this packet is to make the impossibility/possibility frontiers and the missing data precise while avoiding false universal claims. Next independently valuable tasks: compute operator lower spectral constants; recover full CFT singlet fixed-point phases; project actual ground state onto group irreps; build reference-corrected detector model; dynamically select a marked triple and characterize quotient dispersion.
