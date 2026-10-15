# TOE89 — Cyclic Tate chain obstruction, 2-torsion Heisenberg transport, complementary CSS extraction, heralded MUB theorem, and Albert multiplication no-go

**15 October 2026.** Five TOE88 directions executed on a fresh isolated worktree of `wilcompute/W33-Theory` at remote master commit `aac4f5c72adabf614fdd9d0143fd2ed317263276`. The dirty primary local checkout was not modified. Exact integer/modular calculations and synthetic quantum-circuit calculations are carefully separated.

**Scope and status:** All five received executable investigations, frozen datasets, and regression tests. We do **not** prove the full conceptual two-orbit ternary polarization coincidence without enumeration, do **not** build a fault-tolerant decoder, and do **not** prove or disprove all conceivable exceptional Albert products. No physical TOE, temporal arrow, or device implementation is claimed.

## 1. Characteristic-three cyclic Tate modules: chain-level theorem and obstruction to a simple proof

Take the native H27 Schläfli code with 27 vertex sites, 135 edge qudits, 45 oriented triangle faces, and **two full 27-square H27 orbits** (99 face checks). For any noncentral order-three element `g`, the 99-face signed permutation module restricted to `C3=<g>` has exactly **three fixed oriented triangle faces** and **32 freely rotating triples of faces**, whose combined orientation sign is +1. Therefore, over F3,

```
C2 | C3   ~=   F3^(3)  +  F3[C3]^(32)
dim Tate^0(C3,C2) = dim Tate^-1(C3,C2) = 3.
C1 | C3 ~= F3[C3]^(45); C0 | C3 ~= F3[C3]^(9).
```

These decompositions were independently checked on all four noncentral projective Pauli directions for all **13 normalizer representatives** of the 468 admissible two-orbit codes. Every class still has matching unique H1/H2 minimizing directions (TOE87-88). Yet **the C2 restriction is identical for all four directions**, so fixed-face counts or the absolute Tate(C2) groups **cannot themselves explain the selected direction**; the induced boundary/connecting maps must matter. Adding a third regular square orbit changes the restriction to `3 trivial + 41 regular` but retains the same Tate(C2) dimension 3, while the exact previously found triple (0,10,1) destroys uniqueness of the H1 direction: `[2,2,2,2]` versus H2 `[13,12,13,13]`. Thus a proposed general theorem based *solely* on C3 cell isotropy is refuted.

This is a **partial structural theorem and a no-go for a naive proof**, **not** a derivation of the full 468-pair selector agreement from a long exact Tate sequence. The next theorem needs the extension/connecting morphisms, not just dimensions.

## 2. Geometric origin of the 24-face Z/2 Bockstein membranes

TOE88 independently constructed two 24-face parity membranes spanning the rank-two Bockstein image in the two torsion classes with Smith factors `[6,6]`. This pass applies *every* H27 generator and verifies all **729** group multiplication equations on the two-dimensional binary Bockstein quotient `image(beta_2) <= H1(F2)`.

The image carries a **nontrivial irreducible two-dimensional F2 representation of a C3 quotient** of H27. Its H27 kernel has order nine, including the center, identifying a Pauli direction:

| Square orbit pair | H27 kernel subgroup | projective (a,b) direction |
|---|---|---|
| (1,31) | `{(a,0,c) : a,c in F3}` | (1,0) |
| (1,36) | `{(a,2a,c) : a,c in F3}` | (1,2) |

In both families, the two-dimensional binary Bockstein image therefore gives an *intrinsic H27 symmetry label* for the 2-primary torsion. This is stronger than simply listing [6,6] Smith factors: the parity obstructions themselves furnish Pauli-module representations.

Limits: the discovered binary subspace is canonical, but the individual 24-face membrane *supports* need not be canonical or minimal. We have **not** classified their full W(E6) orbits, just the regular Heisenberg symmetry acting on their homology images.

## 3. Complementary X and Z checks, ideal flag hooks, and repeated extraction

Add a **27×135** ternary vertex-edge incidence matrix HX to the TOE83 selected **99×135** face-edge boundary HZ. Verify exact orthogonality `HX * HZ^T = 0`. Both logical check families can now be accessed in an explicit qutrit SUM-based Pauli-frame simulator.

- 27 X checks / 270 weighted ancilla-control SUM gates in **10 conflict-free layers**;
- 99 Z checks / 351 weighted data-control SUM gates in **6 conflict-free layers**;
- total 621 SUM interactions per round, plus **126 flag ancillas** and 252 paired pre/post flag SUM interactions if enabled;
- three repeated rounds, 144 seeded shots per flagged/unflagged model, identical random fault seeds, noisy data and ancillas and imperfect syndrome digit readout.

Flag construction: conceptual ideal pre/post SUM of an ancilla with its flag, detecting a nonzero accumulated dangerous ancilla Pauli error (`X` on X-check control or `Z` on Z-check target). These paired flag gates are **idealized and not independently fault-injected or simulated gate-by-gate**. They cannot be claimed as validated fault-tolerant hardware.

The frozen seeded results include a model hook-injection incidence of `106/144 = 73.61%` and, with ideal flags enabled, the same incidence of detected nonzero flag syndromes; the unflagged control has zero flag outcomes. Under this toy model both layouts have the same physical residual-error outcomes because monitoring alone does not correct faults.

Most importantly, the naive per-check temporal Viterbi filter **underperformed** the raw final-syndrome single-site physical correction: `48/144 = 33.33%` exact zero residual versus `33/144 = 22.92%` with the filter. This is a valuable negative control against calling a simple temporal majority/Viterbi rule a real hook-aware CSS spacetime decoder. A correlated, circuit-aware joint decoder and noisy flag syndrome extraction remain open. No logical error rate or threshold has been measured.

## 4. Loss-resistant 4-MUB qutrit witness: strengthen the mathematical bound

TOE87-88 found that leaking the *classical secret input basis label* lets a malicious measure-and-reprepare device spoof high accepted-shot return fidelity. This pass proves a stronger positive statement which corrects earlier overbroad wording:

**If input settings are uniformly random over the complete 12-state qutrit projective 2-design and the instrument does not receive the classical setting label, then any trace-nonincreasing entanglement-breaking CP instrument has accepted-shot mean return fidelity at most 1/2 — even if its own measurement result governs whether it heralds acceptance.**

For a rank-one measure/reprepare instrument `E(rho)=Tr(M rho) sigma`, the uniform 2-design gives exactly

```
F_accepted =
  (Tr M + Tr(M sigma))/(4 Tr M) <= 1/2.
```

Since general EB CP instruments are positive sums of measure/reprepare branches, the inequality survives arbitrary quantum-state-dependent *setting-blind* heralding, not merely constant acceptance. The code verifies the second-moment identity through the existing TOE87 construction and validates the formula on 96 random nontrivial measure/reprepare instruments (sample maximum ≈0.47717). It retains the explicit setting-label side-channel attack with 32.5% acceptance and 84.6% fidelity as the genuine loophole.

Under TOE88's conservative trusted preparation/measurement error envelope and readout/leakage nuisance model, the suggested 1,200-accepted-shot threshold remains 665, with ≤0.001 binomial null-tail and ≈0.99324 synthetic alternative power. That design still requires independently verified calibration, uniform hidden settings and a security analysis of classical leaks/drift before experimental claims.

## 5. Test the binary Albert-algebra candidate at the multiplication level

TOE88 constructed a rank-26 F2[H27]-module isomorphism between H1(F2) of the selected code and the **augmentation kernel** of the regular 27-point permutation representation. This pass tests the obvious product:

```
V = {x in F2^27 : sum_i x_i=0}
P(w) = w - (sum_i w_i)/27 * 1  (in F2, 27=1)
x star y = P(x coordinatewise_times y).
```

This is a natural commutative **H27-equivariant** bilinear product on V. However, it is **not a Jordan algebra as a polynomial identity over extensions of F2**: an explicit pair of elements in V tensor F4 (where F4=F2[t]/(t²+t+1)) has a nonzero defect

```
((x*x)*y)*x  +  (x*x)*(y*x) != 0
```

for the star-product (addition equals subtraction in characteristic 2). Its exact nonzero defect occurs in coordinates **[0,1,2,3,5]** and the certificate freezes x, y and all coefficients. This subtlety is easy to miss: checking only F2-valued vectors yields `x*x=x`, so the Jordan identity falsely appears to hold at every F2-rational point; scalar extension exposes failure.

Separately, the full coordinatewise associative algebra F2^27 admits 27 pairwise orthogonal primitive idempotents, unlike degree/rank-three Albert J3(O). Thus the *naive projected coordinatewise multiplication* does not produce the exceptional Albert structure. This **does not rule out a different H27-compatible exceptional product**; identifying one requires a full bilinear-product ansatz and exceptional Jordan identities.

## Reproducible files

- `analysis/w33_20261015_toe89_cyclic_tate_chain.py`
- `analysis/w33_20261015_toe89_parity_symmetry.py`
- `analysis/w33_20261015_toe89_complementary_css.py`
- `analysis/w33_20261015_toe89_heralded_mub.py`
- `analysis/w33_20261015_toe89_albert_product_obstruction.py`
- Five frozen JSON certificates under `data/w33_20261015_toe89_*.json`.
- `tests/test_w33_20261015_toe89_all_five.py` and `.github/workflows/w33_toe89_all_five.yml`.

Reproduce with `python -m analysis.w33_20261015_toe89_<track>` for each script; then `python -m pytest -q tests/test_w33_20261015_toe89_all_five.py`.

## Five independent next steps

1. **Tate connecting-map selector theorem:** compute the explicit cyclic-Tate connecting morphisms for the 99-face chain complex and prove (or sharply limit) the F3 H1/H2 common-minimizer phenomenon beyond the 13 checked classes.
2. **W(E6) parity membrane transport:** classify the 24-face membrane cosets and their 2D Bockstein image under the *full* cubic-surface Weyl action, including minimal support and which symmetries preserve selected H27 structure.
3. **Real flagged fault-tolerant extraction:** implement noisy pre/post flag gates, measurement-gadget fault propagation, simultaneous check scheduling, and a joint space-time correlated Pauli decoder; report verified logical error rates and compare against simple Viterbi failures.
4. **Optical secret-setting security:** design a physical four-MUB photonic protocol with pre-registration and independently audited basis secrecy, source side channels, detection heralds, loss and leakage using adversarial EB instruments.
5. **Exceptional Jordan product classification:** impose equivariance and the universal Jordan identities on a general H27-invariant bilinear multiplication on the 26D binary augmentation module and determine whether any exceptional Albert-compatible structure survives scalar-extension tests.
