# 2026-10-09 — Five further W33 physics fronts: corrected R-parity gate, 11-state vacuum, optical joint score, T-odd response and native dimensional limits

**Ritz erratum (2026-10-09):** The earlier eleven-state floating reduction used the wrong line-side sign for momentum covariance and derivative, so its quoted `127.595492673` is NOT a correct bound for the named Hamiltonian. The independent exact-Wick corrected bound **`E0 < 127.595507`** is in [the follow-up](2026-10-09_five_more_toe_frontiers.md). Other fronts have distinct tests.

**Ownership and standard of evidence:** This pass extends the already committed Pass11769–11785 current-square quantization and Pass10960 heterotic ledger. It separates exact algebra and reproducible numerics from interpretations requiring additional string/continuum/hardware assumptions. The principal external benchmark is Lebedev et al., *The Heterotic Road to the MSSM with R parity*, arXiv:0708.2691, especially equations E.1a–c, E.5 and model-1 vacua; the E8 root-system graph is an established Weyl representation (Winter and van Luijk, arXiv:1901.06945).

## 1. Spectrum: improved 11-state upper bound, not a computed full Hamiltonian gap

Adding point/line collective He10 modes to the optimized Gaussian plus collective He2/4/6/8 yields an exactly orthonormal 11-state trial space. Matrix elements reduce to the existing eight W33 incidence-pair orbits and four-variable Gaussian moments. The squared-current integrands have total polynomial degree no greater than 24, integrated independently by degree-exact 13-node and 14-node tensor Gauss–Hermite rules in floating arithmetic.

- Former nine-state ground-energy upper bound: `127.595518296517`.
- **New 11-state upper bound:** `E0 <= 127.5954926734291`.
- Improvement: `0.0000256230879`; maximum 13-versus-14 matrix-entry discrepancy: `5.12e-13`.
- First two *compressed Ritz values*: `127.59549267`, `142.61678016`. The difference `15.02128749` **is not the actual excitation gap**.
- All 11 Ritz eigenvalues lie below `232.968`. By the min–max principle, the true compact-resolvent operator has at least 11 eigenstates, **counting multiplicity**, with eigenvalues below this approximate bound. This is an upper spectral counting certificate, not a lower-bound/gap certificate.

Source producer: `analysis/w33_20261009_11state_ritz.py`, generated from the previous nine-state proof by `analysis/w33_20261009_generate_11state_ritz.py`. Nothing here supplies the quantitative lower bound on `E0` or `E_next-E0` requested for the full 78-coordinate Schrödinger operator. The qualitative compact-resolvent/positive-gap theorem belongs to Pass11778 and should not be confused with the Ritz spectrum.

## 2. Heterotic model-1 gauge congruence and a critical scope correction to Pass10960

The previous pass identified **`Z6II_34__SM_20260917_1558`** as the unique surviving model-1 gauge-shift/Wilson-phase candidate under 48 declared sign/shift transformations. Here we constructed the **full 240-root colored graph** of each E8 factor, with edges for root dot product 1, and colored vertices by the phases of `(V,W2,W3)`. A VF2 isomorphism after `(V,W2,W3)->(-V,-W2,+W3)` gave explicit independent 8-by-8 orthogonal Weyl matrices, with every one of the 240 mapped roots verified, and exact E8 lattice offsets for **all three gauge vectors in both E8 factors**. Full root permutations, matrices, and lattice differences are frozen in `data/w33_20261009_e8_explicit_weyl_congruence.json`.

The same original orbifolder spectrum has `tr Q_anomalous=296/3`, matching the independently published model-1 value (paper E.5). These are substantial *gauge-embedding* concordances, not yet proof of physical orbifold equivalence. It remains essential to verify the inversion choices as geometric Z6-II space-group operations, including chirality and selection rules.

**Important: Pass10960's global verbal conclusion overreaches its implemented premise for this candidate.** It requires **every** field named `bd` to carry the chiral down-antiquark value `B-L=-1/3`. The source ledger contains ten `bd` labels, while the explicitly transformed benchmark B-L direction, reconstructed from 24 raw gauge-momentum anchors and rational U1 charges, assigns **six** of them `B-L=2/3` and four `B-L=-1/3`. All three q fields carry +1/3, all three bu fields -1/3 and all three be fields +1. A minimal unsatisfiable-core witness for the overconstrained gate is `-Q(bd_7)+Q(bu_3)+Q(be_3)=0` but the demanded B-L charges yield **1**, an exact inconsistency. This is not a proof that no suitably selected chiral matter families exist.

An **assignment-aware** rational D-flat search selecting the 3 q, 3 bu, 3 be and 4 properly charged bd fields admits a six-singlet nonnegative support:

```
n_1 = n_54 = n_80 = n_82 = 9/37
n_19 = n_56 = 27/74
```

These are relative squared-VEV weights. They give `sum_s a_s Q_s=(-1,0,0,0,0,0,0,0,0)` exactly (FI normalization -1), each is nonabelian-singlet and hypercharge neutral, and there is an admissible continuous B-L charge direction with `3(B-L)=0` on all six. This is an **explicit counterexample to the *amended assignment-aware* D-flat no-go**, not a counterexample to the literal overconstrained all-bd gate's algebra.
The old Pass10960's *raw* calculation may be correct for its own all-labeled-field rule, but that rule cannot establish the advertised exclusion of **every** W33 singlet matter-parity vacuum. The corrected support is verified independently with exact fractions and archived in `data/w33_20261009_corrected_assignment_dflat_certificate.json`, together with the separate unsatisfiable-core certificate.

**Remaining critical barriers:** The full nine-U1 charge lattice admits **zero** order-two characters that are odd on all thirteen selected standard-charge labels and even on the six VEV labels (exhaustive 2^9 check). Under one continuous B-L choice, only 112/176 raw left-chiral fields have integral `3(B-L)`. The resulting unbroken transformation may therefore act with *higher order* on exotic fields; no exact global Z2 matter-parity claim follows. Supersymmetric F-flatness, hidden-sector vevs, physically correct three-family/Higgs assignments and geometric orbifold equivalence are not proved. The certified FI-cancelling D-flat support is **not** yet the published benchmark's actual supersymmetric vacuum. Neither a full proton-decay computation nor MSSM effective couplings have been reproduced.

Raw-file reproducibility: all 15 full orbifolder model embeddings and original source SHA-256 were frozen in the prior pass; this pass additionally freezes 24 gauge-momentum anchors and their source hash, and independently reconstructs published model-1 B-L with rank-7 anchored subspace (two unconstrained U1 directions). The assignment-aware D-flat family has a three-parameter rational kernel after choosing the thirteen standard matter-charge constraints.

## 3. Vacuum symmetry-breaking response — conditional finite-dimensional classification

For the compact-resolvent Hamiltonian and the verified dressed antiunitary T with `T²=+1`, any Hermitian T-odd curvature `C=i[J_e,J_f]` compresses in a T-real orthonormal basis of the attained finite-dimensional ground sector to `P0 C P0=iA`, with `A` a **real skew-symmetric matrix**. Its first-order eigenvalue shifts occur in **+/- pairs**, and any *odd-dimensional* ground sector has at least one first-order zero shift.

If the actual ground sector is one-dimensional, its first-order curvature response is zero; second order is nonpositive and governed by excited-state matrix elements, not by a Kramers theorem. If a degenerate ground sector has nonzero `iA` compression, its lowest eigenvalue can develop a linear cusp `E0(eps)=E0-|eps|s+O(eps²)`. Exact SymPy finite controls yield a doublet `2-|eps|` and a unique-ground two-level model `(7-sqrt(9+4eps²))/2` with second derivative `-2/3`. This is a diagnostic of **ground degeneracy and symmetry-breaking susceptibility**, not an actual W33 ground-sector multiplicity measurement or spontaneous symmetry breaking in a thermodynamic limit.

The previous bound `(1-|eps|)H<=H+eps C<=(1+|eps|)H` for `|eps|<1` ensures form-domain stability and qualitative discreteness. Its numerical gap remains unknown. Source: `analysis/w33_20261009_ground_antiunitary_response.py`.

## 4. A substantially better photonic observable — and quantified loss

The single-edge continuous-variable nonlinear evolution `U(theta)=exp[-i theta (X+a)^2 (P_Y+a)^2]`, with `a=1/sqrt39`, preserves `P_Y` and gives `P_X' = P_X - 2 theta (X+a)(P_Y+a)^2`. For independent vacuum input, the **joint mixed third cumulant** of two commuting homodyne outputs is

```
kappa(P_X,P_Y,P_Y) = -theta/sqrt39,
theta = (39/20)^2 tau.
```

Every multivariate Gaussian state has zero centered mixed third cumulant, including Gaussian photonic circuits. Relative to the prior fourth-cumulant observable `~theta^4`, this third cumulant is **linear in theta** and exploits the simultaneously measurable second optical mode. Exact rational Wick moments and an independent 13-node Gaussian quadrature agree on the influence-function variance.

At `tau=0.05`, no loss or electronics, a **heuristic 5-sigma alternative-asymptotic** score requires ~**16,983** samples, compared with ~**85,260** for the heavy-tailed fourth-cumulant estimator. For equal transmission eta on both channels, independent pure loss scales the signature as `eta^(3/2)`. An independent 11/12-node quadrature with Gaussian electronic variance 0.01 per channel gives **17,556** at eta=1, **26,486** at eta=0.8, **76,735** at eta=0.5 and **951,658** at eta=0.2. These are *not calibrated finite-N hypothesis-test power values*: non-Gaussian gate synthesis, correlated drift, imperfect correlations and actual detector response are open engineering problems. Relevant source code: `w33_20261009_joint_homodyne_cumulant.py` and `w33_20261009_joint_homodyne_loss.py`.

## 5. A second W33-only spacetime attempt — exact failure to select dimension

Instead of externally imposing a lattice Z^d (previous pass), test the canonical **native self-replication** family `G_n = Levi(W33) □ Levi(W33) □ ... □ Levi(W33)` (n Cartesian factors). Its normalized combinatorial heat kernel is exactly `P_n(t)=p_Levi(t/n)^n`; degree-normalization uses the generator `L_n/n`.

For fixed t and `n->infinity`, the single-cell mean eigenvalue is 4, and

```
P_n(t) -> exp(-4t),
spectral dimension d_s(t) = -2t d(log P_n)/dt -> 8t.
```

The limiting "dimension" crosses 3 only at `t=3/8`, with nonzero slope 8—not a stable spatial plateau. At n=1000 the computed values are `d_s(.2)=1.59968`, `d_s(.375)=2.998875`, `d_s(.5)=3.9980` and `d_s(1)=7.9920`. At any fixed n, the true long-time spectral dimension returns to zero because the graph is finite. This rules out **that natural normalized Cartesian-power construction** as a dynamically generated three-dimensional spacetime; it says nothing universal about all W33-based infinite-system limits.

Source: `analysis/w33_20261009_w33_cartesian_power_spectral.py`.

## Reproducibility / remaining physics

Portability: frozen model rows, gauge-weight anchors, explicit two-factor E8 Weyl matrices, rational B-L and D-flat certificates, the new Hermite tower and both homodyne models, with pytest regressions, live under analysis/, data/ and tests/. The original raw WSL files remain untouched. We did not modify Pass10960's producer or source ledger; this scope/firewall note must accompany any later global no-go language.

**Open:** quantitative *full* spectral gap; unique physical ground/radiative stability; complete Z6-II space-group equivalence and F-flat exact matter parity; a physical quartic photonic gate and drift-robust calibrated inference; intrinsic selection of 3+1D Lorentzian gravity rather than a parameterized geometric lift.
