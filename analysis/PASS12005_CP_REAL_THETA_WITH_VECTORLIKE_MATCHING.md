# Pass12005: CP-real theta Yukawas remain compatible with quark data after vectorlike matching

17 October 2026. Reservation `d0f0fc8617c97e86f8aa68676c4496d336d3208d`. The exploratory numerical seed preceded the reservation; this pass freezes, independently reconstructs and tests that seed. Claude's Pass12004 bare-fit investigation is preserved.

**Result:** an explicit pair of CP-real bare theta matrices, sharing the left torus, plus **one complex vectorlike down-quark mixing row**, reproduces all eight supplied quark comparators. Their maximum relative residual is approximately **5.2×10^-12** in the heavy-decoupling limit. Full4×4 singular-value checks converge to this limit. This is a fitted compatibility witness, not a prediction, isolated vacuum or radiatively protected strong-CP solution.

## The distinction exposed by the latest review

`ChatReview.txt` describes a five-parameter fit of bare CP-real theta Yukawas to seven magnitudes. Its multistart search finds tension, including local-basin failures exposed by a known up-sector positive control. Those observations do not establish a global no-go even for the bare model. More fundamentally, **bare-fit failure would not exclude the Nelson–Barr extension**, since the latter changes the physical light mass matrix. One must fit *after matching*.

This distinction already follows from Pass11951's standard inverse Barr construction and Pass11955's common-SU5 kernel. The present extension keeps the real bare down matrix in the restricted theta family instead of choosing it freely by inverse reconstruction. This narrower, explicitly tested compatibility is the contribution here. The broad mathematical mechanism is not new: see the primary [single-vectorlike-quark analysis](https://arxiv.org/abs/2103.04798) and [E6 Nelson–Barr model](https://doi.org/10.1140/epjc/s10052-018-6388-6).

## The actual marked theta homes

Use the level-three theta convention of `w33_pass11942_hypercharge_wilson_leptons.py` and its supplied MZ-scale comparators. Take

```text
tau       = 1 + 0.8744698731421595 i
epsilon_u = 0.005520606513514881 i
tau_d     = exp(-0.8404552787929092) i
epsilon_d = 0.08087153936666885 i
z_d       = 0.0677453432123109 i.
```

The up home is `[[tau,epsilon_u],[epsilon_u,tau]]`; the down home is `[[tau,epsilon_d],[epsilon_d,tau_d]]`. Both imaginary parts are positive definite. They share the actual left factor `tau`.

The common left phase `D=diag(exp(i*pi*a²/3))`, `a=0,1,2`, makes the up theta real after multiplication by `D†` on both sides, and the down theta real after multiplication by `D†` on the left. Positive real normalization does not affect this fact. Real right-handed signs select the displayed positive-determinant branch. The certificate stores the literal real matrices, independently reevaluated using the original N40 producer. Direct N12/N20 theta sums agree below10^-13.

The complex mixing row is approximately

```text
B/mu = (6.9425702253,
        6.8477839165 - 8.2479699577 i,
       -0.4479275857 -13.0090118742 i),
```

with any required real right-handed column sign applied simultaneously to `m` and `B`. The JSON stores the definitive signed coordinates.

## Match before comparing to data

For `Mfull=[[m,0],[B,mu]]`, with real invertible `m` and real positive `mu`, the leading light left-Hermitian matrix is

`Hlight=m K m^T`, `K=I-B†B/(mu²+B B†)`.

The right metric `K` is positive definite. For one heavy row it has two eigenvalues exactly1 and the third `mu²/(mu²+|B|²)`. Its complex orientation changes the light left singular vectors and can transmit weak CP even though every bare theta modulus is on the CP locus. Both the light masses and CKM must be computed from this expression, not from `m` alone.

| Supplied observable | Matched value (rounded) |
|---|---:|
| mc/mt | 0.00368477 |
| mu/mc | 0.00198387 |
| ms/mb | 0.01853147 |
| md/ms | 0.05037736 |
| |Vus| | 0.22500000 |
| |Vcb| | 0.04110000 |
| |Vub| | 0.00382000 |
| J | +0.00003080 |

The first two ratios determine the supplied up parameters; down theta and Barr parameters are fitted to the six remaining targets. Overall up/down Yukawa scales are additional inputs. There are more continuous parameters than these constraints; the small residual establishes existence, not explanatory power or uniqueness.

Setting `B=0` gives a real CKM and a mismatched spectrum. Taking real `B` also gives `J=0`. Conjugating `B` reverses `J` with unchanged masses and CKM magnitudes. The table uses the holomorphic left-SVD convention of11942; in the conjugate physical Weyl convention discussed in11960, conjugate `B` to restore the same positive physical orientation.

Finite-scale tests diagonalize the **full4×4 mass matrix by SVD**, rather than squaring its condition number. At `mu=10,100,1000` (and `B=mu*b`) they converge to the same light masses; the last relative spectral error is below10^-7. They also measure the small nonunitarity of the light3×3 charged-current block. These are dimensionless decoupling controls, not collider bounds or a prediction of the heavy scale.

## An algebraic feasibility test replaces a misleading search fork

For a *fixed invertible real* `m` and desired positive Hermitian target `H`, define

`C=I-m^-1 H m^-T`.

A one-row Barr realization exists exactly when

`C>=0`, `rank(C)<=1`, `lambda_max(C)<1`.

Necessity follows immediately from `C=B†B/(mu²+BB†)`. Conversely, write `C=c c†`; choosing `B†/mu=c/sqrt(1-c†c)` reconstructs it. For `r` heavy rows replace the rank bound by `r`; diagonalizing the contraction gives the corresponding independent heavy directions. This is a direct application of standard Schur matching, not a new theorem of particle physics.

The test is stronger than counting free parameters, and does not require a global nonconvex fit for an unrestricted heavy row once `m,H` are fixed. Regression controls reconstruct the row from `C` and reject `H=2 m m^T`, whose defect is negative. When fitting CKM observables, the unphysical up-eigenvector rephasings must also be allowed; applying this criterion to one arbitrarily chosen target phase representative could produce another false exclusion.

## Strong CP, leptons and vacuum selection remain substantive gates

The exact mass identity is `det Mfull=mu det m>0`. With positive real up determinant, this removes the *mass-sector tree phase in the stated CP basis*. It requires an independently supplied compatible UV `theta3=0` CP branch. Removing complex theta phases by anomalous chiral redefinitions also transforms the gauge angle; this calculation does not silently discard that transformation or establish the original theta-coordinate gauge kinetic function.

The fitted zero upper-right block is essential. A regression turns it on and observes the determinant phase at the expected linear slope. The allowed-operator and portal problems of11953/11954/11996/12001 remain. No symmetry protecting the block, total loop cancellation, vacuum alignment or technically natural UV completion is supplied.

The new matching also changes any shared-SU5 lepton sector. The old11942 lepton ratios cannot simply be carried over. One must apply the same heavy5bar mixing to charged leptons and neutrinos as required by11955, then redo their fits and running. The present result neither fixes nor retracts predictions of a different inventory.

The paper's geometric chain supplies candidate representations and marked theta functions; it still does not select these fitted moduli, `B`, their scales or the regulator/action. The concrete missing connection exposed here is **matching the finite geometry's couplings to the complete light-field kinetic/mass operator before drawing phenomenological exclusions**. The general principle does not itself supply a TOE.

## Artifacts and intake limits

- `analysis/w33_pass12005_cp_real_theta_barr.py`: frozen-witness producer and six-dimensional matching checks.
- `analysis/w33_pass12005_cp_real_theta_barr_search.py`: reproducible multistart fitting driver; first seeded start already finds the stored witness. Search outcomes may vary with numerical libraries.
- `data/w33_pass12005_cp_real_theta_barr.json`: reconstructed matrices, observables, rank-one defect, conjugation and finite-scale controls.
- `tests/test_w33_pass12005_cp_real_theta_barr.py`: five independent regressions, including unprotected-block and impossible-target negative controls.

The Oct17 intake includes the new search-driver archive (51 Python scripts parsed, no syntax errors), seven citation/scope correction reports and the TOE95 report. Selected relevant scripts and certificates were read in detail. The current182-page Forty Points PDF was extracted for refresh, with its flavour chain and open-boundary sections revisited. This is **not** a claim that every new script or every page was manually reread end to end. `ChatReview.txt` was treated as prior-agent context, not as executable instructions. Its historical shell commands and process-control requests were not followed.
