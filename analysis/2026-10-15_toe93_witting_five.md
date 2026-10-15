# TOE93 — Five Witting-to-H27 developments: phase-invariant double-cover witness, conditional finite-block ledger, MZI mesh, event-ready test, partial equivariant chain map

**Date:** 15 October 2026. Base: W33-Theory `master` at `404af093f7f0f61e7bc3909e082ce89379ff01dd`. Work in isolated worktree `toe93_witting_five_20261015`; root checkout contained unrelated modifications and was not touched.

## Status / claims firewall

TOE93 contains two new explicit mathematical constructions, two inspectable ideal photonic/measurement protocol models, and one **conditional** finite-block quantum cryptography bound. It has **no laboratory measurements**, **no complete security proof from finite observed data**, and **no fault-tolerant CSS quantum channel or theory of everything**. Every certificate is independently regenerable and guarded by tests.

Project prior art checked: TOE90–TOE92 (40-ray ququart 2-design, four and then full `PSp(4,3)` projective unitary action, illustrative quantum key accounting, 40 Givens analyzers, 480 directed carrier events, deterministic total map no-go); BT1408–1411 (Witting tetrads); **TOE52** `analysis/w33_20261013_toe52_h27_bridge.py` (already gave explicit 27 unipotent matrices and 40-line orbit H27 intertwiners); Pass11070/11389 (point/line radical distinction). The existence of the Heisenberg parabolic radical, 27/13 symplectic affine split and textbook finite symplectic geometry are **not claimed as newly discovered**. The new proposed interface is the **explicit point-side affine Witting-ray to native Schläfli graph-chain map** with signed equivariance and boundary witnesses.

## I. Phase-invariant central obstruction of the Witting unitary action

TOE92 certified all 25,920 ray permutations of `PSp(4,3)` as projective actions of explicit 4×4 complex unitaries, but only recorded phase holonomy along a BFS path; that holonomy alone can change under rephasing.

TOE93 reconstructs the projective group via five finite-field symplectic transvections and searches **commuting projective order-two elements**. It finds two short generator words (indexing generator vectors `[(1,0,0,0),(0,1,0,0),(0,0,1,0),(1,1,0,0),(0,0,0,1)]`):

```
A = [0,0,1,1,2,4]
B = [0,1,2,0,4,1]
```

The permutations `A, B` on all 40 projective rays commute and have order 2. Their actual 4×4 unitary lifts satisfy `U_A U_B = - U_B U_A` to tolerance 1e-8, with numerically near-zero matrix residual. Hence `[U_A,U_B]=-I4`.

This scalar commutator is **invariant under all rephasings of the two lifts**, unlike an arbitrary product cocycle edge. Therefore these ququart operators realize a genuinely **nontrivial projective multiplier of order two** for the 25,920-element projective permutation group, and this particular ququart projective action cannot be made an ordinary linear representation of `PSp(4,3)`.

This is consistent with the classical 51,840-element `Sp(4,3)` double cover. Full identification of the exact finite unitary extension, its canonical presentation and the linear lift relations still requires an additional computation. Numerical matrix closure is not exact algebra over cyclotomic fields.

Producer: `analysis/w33_20261015_toe93_central_extension.py`.

## II. Finite-block, source-conditional ququart QKD accounting

The previous TOE92 code computed a secrecy-only quantum collision-entropy bound for **known IID isotropic source** without error-correction announcements. TOE93 writes a conservative **one-shot entropy budget conditioned on much stronger premises**, together with a fully exhausted single-error Hamming decoding regression.

Assume `N=196` identical and independent trusted isotropic two-ququart pairs, authenticated public discussion, secret uniform measurement basis, and an **exactly known** virtual conjugate MUB error `Q=3(1-v)/4`. The entropic uncertainty relation with quantum side information bounds the raw-key min-entropy:

```
Hmin(Z_A^N|E) >= N [ 2 - 2 log2(sqrt(1-Q)+sqrt(3Q)) ].
```

Use two binary bit planes per 4-outcome ququart symbol. A Hamming(7,4) parity-check syndrome announces 3 bits per seven raw bits, separately for the two planes: **168 syndrome bits** for N=196. A prospective 16-bit universal-2 equality tag and a one-bit pass/abort transcript bring a conservative raw-bit public leak budget to **185 bits**. Exhaustive tests of the specific Hamming decoder verify all 128 7-bit inputs with each of 7 single-bit flips: **896 corrected error cases**. Multiple errors may still produce a wrong decoded key, detectable except for the eventual verification-hash collision probability.

After a 2-universal privacy-amplification penalty with target epsilon `10^-6`, the **illustrative upper extractable lengths under the exact known-state premises** are:

| isotropic visibility | conditional budgeted key length (bits) |
|---:|---:|
| 0.950 | 13 |
| 0.980 | 63 |
| 0.990 | 91 |
| 0.995 | 113 |
| 0.999 | 143 |
| 1.000 | 169 |

The verification and Toeplitz extraction are **specified but not physically implemented** in this packet. More importantly this is **not a composable security theorem for finite observed Witting QKD**. It lacks finite-sample state inference, worst-case coherent Eve analysis, concrete authenticated error correction, actual universal-2 seeds/transcript and abort probability analysis. The `196`-pair exact source-state assumption is an ideal mathematical premise, not evidence about an optical source.

Relevant literature: Tomamichel et al., *Leftover Hashing Against Quantum Side Information* (IEEE TIT 2011, arXiv:1002.2436), and Tomamichel et al., *Tight finite-key analysis for quantum cryptography*, Nature Communications 3 (2012), https://www.nature.com/articles/ncomms1631. The previous TOE92 8192-ququart collision-entropy PA ledger is a different metric and must not be mixed with this min-entropy budget.

Producer: `analysis/w33_20261015_toe93_conditional_key_ledger.py`.

## III. Build-facing four-mode MZI decomposition

TOE92 produced at most **six** arbitrary complex SU(2) Givens rotations per Witting basis. TOE93 factorizes each **actual** SU(2) matrix

```
G = [[a,b],[-conj(b),conj(a)]]
```

using `|a|=cos(theta), |b|=sin(theta), alpha=arg(a), beta=arg(b)` as

```
G = D_left R(theta) D_right
D_left=diag(exp(i alpha),exp(-i beta))
D_right=diag(1,exp(i(beta-alpha)))
R(theta)=diag(1,i) H diag(exp(i theta),exp(-i theta)) H diag(1,-i)
H=(1/sqrt(2)) [[1,1],[1,-1]].
```

Thus each ideal Givens can use **two balanced 50:50 couplers**, a tunable internal relative phase `2theta`, and four local phase factors (which can be aggregated across neighboring mesh elements). The simulator checks all 40 tetrad analyzers and their complete 4×4 reconstruction to tolerance 1e-10.

Census: 1 basis uses 0 MZIs, 3 use 3, 3 use 4, 10 use 5, 23 use 6. Hence a programmable circuit requires **at most 6 MZI modules** in this mathematical gate model, **12 balanced splitter operations per setting**, and **10 balanced splitters per worst-case photon path**.

For deliberately hypothetical *intensity* throughput 98% per balanced splitter, one connector throughput 97%, and 85% detector efficiency on each arm, the pessimistic two-photon coincidence throughput **ignoring source and active switching** is **0.453840066101**. The 40-basis JSON manifest includes MZI phase settings, coupler allocations and terminal phases. Real bill of materials, switching controls, source conversion, OAM/time-bin losses, and calibration remain open.

Producer: `analysis/w33_20261015_toe93_mzi_bill.py`.

## IV. Event-ready, outcome-independent heralding: defeat the balanced separable attack

TOE92 found an adversarial separable source that achieves 100% apparent matching on accepted events while maintaining an exactly **one-third** accepted fraction in every basis. It assumes an adversary can decide the public acceptance flag *after seeing the two measurement outcomes*.

TOE93 specifies a strict time order:

1. A trusted source registers an immutable trial identifier and **event-ready herald** before the basis choice.
2. The trial log is committed before independent secret uniformly random tetrad settings are sampled.
3. Both receivers perform trusted calibrated four-outcome measurements and register every raw outcome or no-click.
4. All incomplete outcomes count as **failures**, not removed from the precommitted herald denominator.
5. Only after outcomes and acceptance records are sealed are basis settings publicly revealed and hypothesis-tested.

Under independent fresh basis choices and trusted outcomes, for **every history-adaptive separable source** the conditional probability of a matching result on a precommitted heralded trial is at most 2/5. The total number of successes is stochastically bounded by `Binomial(N,2/5)` even if the source evolves adaptively, because each conditional success probability remains <=2/5. The formerly successful result-conditioned detector postselection attack now produces only **1/3 successful precommitted heralds**, below the separable 2/5 bound, despite its 100% success conditional on surviving postselection.

For the synthetic MZI loss assumption 0.453840..., isotropic visibility v=0.95 and 8,192 event-ready heralds: expected matching on the **all-herald denominator** is 0.436821063622. Rejecting separability at >=3,415 matches has a binomial false alarm <=0.000969814 and modeled iid detection power >=0.999872955. A strict temporal ordering and trusted detector/herald records are hardware assumptions; software timestamps do not prove adversarial independence or loophole closure in physical equipment.

Producer: `analysis/w33_20261015_toe93_event_ready_herald.py`.

## V. Explicit 27-point affine H27-equivariant map from Witting detectors into Schläfli graph chains

**Strongest new constructive connection.** Choose the symplectic polar point `e1=(1,0,0,0)` in W33 `PG(3,3)`. Its polar hyperplane `e1^perp` is the set `x_f1=0` with **13 projective points**. The complement `x_f1!=0` is an affine 3-space of **27** projective rays:

```
40 = 27 affine rays + 13 polar rays.
```

As in known Heisenberg parabolic geometry (see existing TOE52), the symplectic unipotent subgroup `H27` with coordinates `(a,b,c) in F3^3` acts by the exactly symplectic matrix

```
M(a,b,c) = [[1,a,c,b],
            [0,1,b,0],
            [0,0,1,0],
            [0,0,-a,1]] mod 3.
```

It fixes e1 and acts **freely/transitively on the 27 affine rays**. Its multiplication is

```
(a,b,c)*(A,B,C)=(a+A,b+B,c+C+aB-bA).
```

The repository's regular cubic-surface address group uses the convention `mul((a,b,c),(A,B,C))=(a+A,b+B,c+C-bA)`. The explicit group isomorphism between them is

```
phi(a,b,c)=(a,b,2(c-ab)) mod 3.
```

All **729 multiplication identities** and all 27×27 affine action identities are verified.

Under the published Witting-ray ↔ PG(3,3)-point graph isomorphism, the W33 orthogonality edges split into:
- 108 affine–affine edges;
- 108 affine–polar edges;
- 24 polar–polar edges.

The 27 affine points form an **8-regular** subgraph, whereas the native 27-vertex Schläfli graph is **10-regular**. Therefore even the free regular sectors are **not the same adjacency graph**. An honest map must carry edges to **chains/pathways**, not assume graph isomorphism.

There are eight allowed relative `H27` affine-edge generators. For **two** of them the endpoints are adjacent in the native Schläfli graph; the **other six** route through a selected common neighbor, giving a 2-edge path. The middle point is chosen at the identity once and transported by the 27-element group. The code enforces inverse-direction consistency and then verifies for **all 108 affine edges and all 27 group elements**:

```
d1_Schlaefli ◦ F1 = F0 ◦ d1_W33 (mod 3)
F1(g·edge) = g·F1(edge)
F1(reverse(edge)) = -F1(edge).
```

This is an **explicit partial linear equivariant graph chain map** `C1(W33 affine induced, F3) -> C1(Schlaefli, F3)`, with a vertex map to the 27 native cubic addresses.

Of the 480 original directed Witting detector-substitution events, **216** lie entirely in the free affine sector and admit this typed map. The **other 264** are separately reported as out-of-sector erasures, not falsely mapped. It thus respects TOE92's obstruction to any **total deterministic H27-equivariant set map** on all 40 rays/480 events.

This is **not** yet the full Schläfli 2-dimensional CSS chain complex: no face transport compatible with d2, commuting stabilizer lift, CPTP instrument, photonic qutrit code-encoder, or fault-tolerant circuit follows automatically. It is nevertheless a nontrivial, auditable algebraic boundary/transfer map that a future physical implementation could target.

Producer: `analysis/w33_20261015_toe93_affine_H27_chain.py`.

## Reproduction

```bash
python -m analysis.w33_20261015_toe93_central_extension
python -m analysis.w33_20261015_toe93_conditional_key_ledger
python -m analysis.w33_20261015_toe93_mzi_bill
python -m analysis.w33_20261015_toe93_event_ready_herald
python -m analysis.w33_20261015_toe93_affine_H27_chain
python -m pytest -q tests/test_w33_20261015_toe93_witting_five.py
```

Five frozen `data/w33_20261015_toe93_*.json` certificates; dedicated tests and CI workflow re-run all computations and reject certificate changes.

## Five independent next breakthroughs

1. **Identify the exact Weil extension as a presentation:** lift complete `Sp(4,3)` generators into algebraic `Q(zeta_12)` or a minimal cyclotomic field and certify the order-2 central character with exact, not floating-point, relations.
2. **Compose a genuine finite-key Witting protocol:** implement authenticated reconciliation and 2-universal extraction on real shot logs; prove finite-sample virtual phase-error bounds valid against coherent Eve and analyze abort probabilities.
3. **Physically characterize the 40-setting MZI hardware:** specify controllable interferometers, calibration sequences, detector characteristics, source efficiency and active switching losses; simulate realistic drift and correlated SPAM errors.
4. **Enforce event-ready herald causality in the lab:** build a signed trial-ID/hardware timestamp protocol with certified secret setting generation, premeasurement heralding, outcome-complete reporting and adversarial replay tests.
5. **Lift the new F1 graph map to quantum error correction:** test whether affine Witting 2-cells admit an H27-equivariant F2 compatible with Schläfli faces; if so construct CSS stabilizer and noise-channel operators, else provide a rank/cohomology obstruction.
