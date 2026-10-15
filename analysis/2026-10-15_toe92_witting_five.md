# TOE92 — Five Witting communication frontiers: full projective symmetry, quantum finite-block privacy, 40-setting optical mesh, adversarial heralding, and an H27 interface no-go

**15 October 2026.** Research worktree `toe92_witting_five_20261015` based on verified TOE91 `dd82d465eabda691ffee9357e9438d4b725c1c6e`. The main Windows checkout is heavily dirty and was **not altered**. The five investigations were verified against TOE90, TOE91, BT1408–BT1411 and the preexisting finite-field symplectic and H27 geometry literature in the repo.

## Scope statement

Exact group calculations, analytic geometry, Hilbert-space QR decompositions, and explicitly declared synthetic/calibrated quantum-security models below are not a demonstration of experimental entanglement, secure key exchange, measured 4D-photon hardware, or fundamental quantum gravity. No result is presented as a completed theory of everything.

## 1. All 25,920 Witting ray symmetries as a projective four-mode unitary action

The project's 40-ray Witting ↔ PG(3,3) orthogonality-graph bijection already exists in `docs/witting_graph_isomorphism.md`. TOE91 proved projective 4×4 unitary lifts for the four coordinate symplectic transvections. In TOE92, close the group under those four transformations and a **fifth cross-plane transvection** with vector `(1,1,0,0)`. The first four generate only **288** projective permutations; the five together generate **25,920**, exactly the established order of `PSp(4,3)`.

Build a breadth-first spanning tree of every one of the 25,920 distinct 40-ray permutations and assign each a 4×4 complex matrix by multiplying the **explicit TOE91 ququart optical lifts**. Verify every one of the `5×25920=129600` directed generator edges, comparing the generated matrix against the preassigned target **up to scalar phase**:

```
U(generator) U(g) ≈ alpha(generator,g) U(generator*g), |alpha|=1.
```

The maximum full-matrix projective-closure error is below `4×10^-15`; the frozen report rounds the maximum to 0 at ten decimal places. Nontrivial phase agreement provides an **explicit scalar cocycle edge witness** (the first is approximately `exp(2 pi i/3)`), but its exact scalar value **depends on chosen unitary phases and spanning tree**. A nontrivial cocycle edge is NOT by itself a proof of a nontrivial projective cohomology class or an obstruction to some alternative global phase convention. The calculation validates the projective group law for **all** 25,920 ray transformations; it does not find a canonical linear representation of PSp or build a physical 135-qutrit gate.

File: `analysis/w33_20261015_toe92_full_symplectic_4mode.py`, and `data/w33_20261015_toe92_full_symplectic_4mode.json`.

## 2. Finite-block quantum secrecy-only PA against an exactly specified IID purifying Eve

TOE91 calculated the asymptotic `2-S(rho_v)` hashing lower bound for a trusted isotropic 4×4 state `rho_v=v|Phi4><Phi4|+(1-v)I16/16`, and warned that this is not a finite-key proof.

TOE92 constructs Alice's explicit classical-quantum density operator after a projective four-outcome measurement, with Eve holding the canonical purification of exactly the stated IID state. In the spectral basis `rho_AB= sum_k lambda_k |psi_k><psi_k|`, Eve's unnormalized conditional state for outcome `x` has entries

```
(rho_E^x)[k,l] = sqrt(lambda_k lambda_l) <psi_l| (|x><x|_A⊗I_B) |psi_k>.
```

The code calculates the **quantum conditional collision entropy** using the fixed marginal `rho_E`:

```
Gamma = sum_x Tr[(rho_E^(-1/4) rho_E^x rho_E^(-1/4))^2]
H_2(X|E) = -log_2 Gamma.
```

The quantum leftover-hash bound for universal-2 privacy amplification with a uniform public random seed implies for N independent copies

```
security trace distance <= (1/2) sqrt(2^(ell-N H_2)).
ell <= floor(N H_2 - 2 log_2(1/(2 epsilon))) .
```

This formula is the **secrecy-only** bound with NO error-correction transcript. At `N=8192`, `epsilon=1e-8`:

| trusted visibility v | Eve conditional collision entropy bits | secrecy-only extractable bits |
|---:|---:|---:|
| 0.25 | 0.121648580439 | 945 |
| 0.70 | 0.687316481687 | 5,579 |
| 0.80 | 0.909370556114 | 7,398 |
| 0.90 | 1.2225825598 | 9,964 |
| 1.0 | 2.0 | 16,332 |

A comparison with the **asymptotic** Slepian–Wolf communication requirement for Bob, `N*H_4(Q)` where `Q=3(1-v)/4`, gives only an *optimistic budget*, not a finite-key certificate including the public error-correction transcript. Even at `v=.8` the optimistic margin is only roughly 455 bits (before finite-block reconciliation, authentication and parameter estimation). With visibility `v=.25` that budget is massively negative, despite the entanglement witness.

Crucial limitations: the state and independence are **assumed and exactly known**, not estimated from finite measurement data. The hashing certificate is not an end-to-end composably secure and correct Witting QKD protocol, nor a device-independent or general-coherent-Eve bound.

Research reference: **M. Tomamichel, C. Schaffner, A. Smith, R. Renner, “Leftover Hashing Against Quantum Side Information,” IEEE Trans. Inf. Theory 57 (2011), arXiv:1002.2436**, https://arxiv.org/abs/1002.2436.

File: `analysis/w33_20261015_toe92_iid_cq_privacy.py`; JSON certificate.

## 3. Exact 40-basis optical circuit compiler with settingwise loss budget

Use the project's authoritative 40 Witting ququart tetrads. For each setting construct the complete 4×4 analyzer with rows `<ray_i|`. Repeatedly apply an exact complex Givens rotation on two of the four rails to eliminate the below-diagonal matrix entries. After at most `4*3/2=6` two-mode rotations, the residual is diagonal with unit-modulus entries and can be expressed as four output-rail phases. Reverse the recorded transformations to **reconstruct the original 4×4 analyzer**, checked at a residual below `1e-9` for all 40 settings.

An exact setting census of needed two-mode complex rotations:

| mixers per setting | Witting bases |
|---:|---:|
| 0 | 1 |
| 3 | 3 |
| 4 | 3 |
| 5 | 10 |
| 6 | 23 |

The maximum optical *path* traversal depth through mixing operations is **5** for the chosen decomposition. A **shared programmable six-coupler four-mode mesh** can realize each of the 40 numerical circuits provided it can implement all the specified complex two-mode rotations and diagonal output phases. A complex Givens step may require multiple physically calibrated beam splitter/phase-shifter elements; **six computational rotations are not an independently sourced count of physical MZIs or tuners**.

Under an intentionally hypothetical component intensity transmission `T=0.98` per traversed coupler and single-photon detector efficiency `eta_D=.85`, pessimistic per-arm path survival is `eta_D*T^5` and two-arm pair survival ignoring source and switching is approximately **0.5903**. This is no measured hardware result and omits many real loss mechanisms.

File: `analysis/w33_20261015_toe92_optical_givens_mesh.py`; frozen complete 40-circuit manifest.

## 4. A stronger malicious-detector negative result: constant per-basis acceptance is insufficient

TOE91 used the separable product state `|ray0><ray0|⊗|conj(ray0)><conj(ray0)|`. Its honest matched probability is `1` in the four bases containing ray0 and `1/3` in each of the other 36, hence uniform-basis average exactly `2/5`.

First constrain *basis-dependent, outcome-independent* acceptance to `eta_B in [0.94,0.98]`. For THIS product-state adversary, the maximum conditional matching is **exactly**

```
Pmatch = [4*0.98*1 + 36*0.94*(1/3)]/[4*0.98+36*0.94]
```

which is above 40%, even with a narrow efficiency variation. For **arbitrary** separable states, a safe generic bound under **outcome-independent** basis weights is `Pmatch <= (eta_max/eta_min)*0.4`. This generic bound is generally not tight.

Second, allow a malicious pairwise coincidence selector that sees Alice and Bob measurement results first, before issuing its public acceptance flag. It can accept **only matching outcomes** and set the acceptance probability conditioned on matching to `(1/3)/p_B`. Because all `p_B>=1/3`, this is a valid event probability. Then **every one** of the 40 settings has exactly **1/3 accepted trials**, yet **100%** of accepted trials match, using a completely separable source. The per-basis acceptance histogram is perfectly balanced and would not catch the attack.

This negative result depends on a **joint, outcome-informed heralding adversary**; it is impossible under trusted outcome-blind, premeasurement heralding. It proves that *per-basis acceptance-rate equality alone* does not close a fair-sampling loophole. A serious experiment must constrain outcome-conditioned selection and ideally preregister acceptance before the quantum measurement results are available.

File: `analysis/w33_20261015_toe92_herald_h27_nogo.py`; JSON certificate.

## 5. An exact H27-equivariance no-go for naive 40-to-27 or 480-to-270 detector maps

Let H27 denote the Heisenberg group order27 acting **regularly** on the cubic-surface 27 addresses. Its action is consequently **free** on the 270 oriented edges of the 27-vertex Schläfli graph (10 outgoing per vertex). It also acts freely on its 135 unoriented edges: a nonidentity group element of odd order cannot swap an edge's endpoints.

For ANY finite G-set `X` and a free G-set `Y`, if `f:X->Y` is a **total, deterministic, G-equivariant set map**, then stabilizers satisfy `Stab(x) subset Stab(f(x))={e}`. Thus every orbit of X must be free, of size 27, and `27 divides |X|`.

But `40 mod 27 = 13` and `480 mod 27 = 21`. Therefore neither the 40-ray Witting set nor the 480 directed detector-substitution events admits a **total deterministic H27-equivariant map** into the regular 27-address space or into the Schläfli oriented-edge space, regardless of how H27 acts on the source.

Consequently, a **full** H27-symmetric deterministic direct translation of each of the 480 W33 detector events to a single one of the 270 Schläfli directed-edge syndrome labels is impossible. Any free-orbit subset of the source must omit **at least 21 events**; similarly any free-orbit subset of 40 rays omits at least 13 rays. Actual orbit structure can force more omissions.

This is a **typed mathematical obstruction**, **not** a no-go for partial projections, linear equivariant maps between representations, stochastic instruments, ancilla-augmented mappings, broken-symmetry routing, or a real physical qutrit encoding. Such a physical interface must specify state preparation and channel and cannot be inferred from count matching.

File: `analysis/w33_20261015_toe92_herald_h27_nogo.py`; JSON certificate.

## Reproduction and claims ledger

```bash
python -m analysis.w33_20261015_toe92_full_symplectic_4mode
python -m analysis.w33_20261015_toe92_iid_cq_privacy
python -m analysis.w33_20261015_toe92_optical_givens_mesh
python -m analysis.w33_20261015_toe92_herald_h27_nogo
python -m pytest -q tests/test_w33_20261015_toe92_witting_five.py
```

All scripts write deterministically sorted or canonical result certificates to `data/w33_20261015_toe92_*.json`. CI independently regenerates and compares each committed certificate. The residuals of floating-point projective closure/unitary compilation are rounded in certificates after explicit strict tolerance assertions.

## Five independent next research steps

1. **Classify the 4D project's central extension:** solve phase gauges and a group-presentation 2-cocycle problem for all `PSp(4,3)` and its double cover `Sp(4,3)`, to determine a genuinely nontrivial multiplier class rather than just a spanning-tree scalar holonomy.
2. **Finish finite-block composable Witting QKD:** design explicit authenticated error correction and two-universal privacy amplification, obtain finite-sample bounds on `rho_AB` against coherent quantum adversaries and detector loss, and combine secrecy/correctness in an end-to-end theorem.
3. **Build a real optical 40-context demonstrator:** turn the six-Givens mesh into actual MZI/heater/detector devices and measured per-rail loss/SPAM parameters with a reproducible calibration and uncertainty budget.
4. **Close the outcome-conditioned heralding loophole:** implement time-ordering/event-ready acceptance signatures and characterize the worst-case detector model under all observed coincidence marginals.
5. **Find or obstruct a probabilistic or homological W33/H27 interface:** explicitly formulate a completely positive trace-preserving event-to-syndrome instrument with ancillas (or a linear chain-level intertwiner), then test its equivariance and error correction. The total deterministic set-map no-go sets a concrete boundary for what needs to change.
