# W33 Theory — TOE Round 36: five independently tested physics mechanisms

**Date:** 10 October 2026
**Destination:** `wilcompute/W33-Theory` master
**Question:** Can the new E8 spinorial `so(11)` centralizer simultaneously yield CHIRAL matter, actual Minkowski translations, a selected 3D vacuum, a relativistic local propagator, and a parameter-free coupling?

## Research framing / prior work

This is a direct follow-up to Round35, the exact `c_e8(SL(2,9))=so(11)` theorem and the three-deck W33 cover with a positive 3×3 diffusion tensor. Before conducting these tests, reviewed current W33 git master, `PASS11854_11858_FAMILY_NOGO_CHIRALITY_FIREWALL_BOOTSTRAP.md` and `PASS11859_11863_PARITY_ORBIFOLD_TRIALITY_POSITIVITY.md`, and newest Pass11864–11868 reservations. These parallel works ALREADY found that a purely E8 orbifold automorphism fails to create chirality; established the spinorial Lorentz×central Z3 commutant `su3+so5+u1` of dimension19; identified the central Z3 as SU3 colour triality; computed the non-split F3 Minkowski extension; and proved B−L survives Lorentz-preserving adjoint breaking. None of those earlier discoveries is claimed anew. Our work tests candidate mechanisms beyond and independently checks their boundaries.

Source papers `w33_paper.tex`, `photonic_holonet.tex`, `holonet_machine_blueprint.tex` are LaTeX entrypoints with extensive subordinate source includes. Holotrade remains an independent compiler/product repo with its recent three-K81 carrier and provenance ledgers; no ungrounded claim of physical hardware or validated TOE follows.

## 1. Explicit chiral domain-wall index and SM anomaly firewall

We constructed a one-extra-dimensional finite interface operator `Q` with shape (48,49), acting by `(Qψ)_j=ψ_{j+1}−exp(-m_j)ψ_j`, where `m_j=−0.7` left of the interface and `+0.7` right. The exact recurrence gives a normalisable profile peaked at the interface; the numerical residual is below `6×10^-17` and the smallest nonzero singular value about **0.5110**. The 48 rows are independent; the kernel has dim1 and adjoint kernel0, hence `ind Q=1`. Making the system square on a closed finite chain restores `ind=0`. A single positive-index `SO(10)` spinor `16` has under SU5 `10+5bar+1`, and the SU5 cubic gauge anomaly cancels by `A(10)+A(5bar)=1−1=0`.

Under SM the exact hypercharges of one family sum to `ΣY=ΣY³=0`, `SU3² U1=0`, `SU2² U1=0`, with four SU2 doublets (no mod2 Witten SU2 anomaly). These are standard consistency checks, not novel particle predictions.

**Physical boundary:** This is a **constructed domain wall with a rectangular Hilbert-space imbalance**, NOT an E8 or W33-selected boundary, dynamical bulk, or actual 4D chiral EFT. It does not bypass Pass11859: an inner E8 automorphism alone cannot select a net 16; the chiral index comes from added geometry and boundary conditions. No number of generations or anomaly-cancelling compactification follows.

`analysis/w33_20261010_toe36_chiral_domain_wall.py` → `data/w33_20261010_toe36_chiral_domain_wall.json`.

## 2. Spinorial Lorentz + central translation: explicit adjoint triality-spectrum calculation, not full Poincare

Earlier Pass11857 certified `c_e8(SL2(9)×Z3)=su3⊕so5⊕u1` dimension19. We independently reconstructed the same result in the **known 55-dimensional centralizer** of spinorial SL2(9): represent the order3 element on R11=R6⊕R5 by three simultaneous 120-degree plane rotations on R6, leaving R5 fixed; induce it on `so11=Λ² R11` (55×55). Compute exact dimension classification of eigenvalues at machine precision:

- eigenvalue `1`: **19** generators;
- eigenvalue `ω=e^{2πi/3}`: **18** generators;
- eigenvalue `ω²`: **18** generators.

The fixed Lie algebra is the compact centralizer `u(3)⊕so(5)=su3⊕so5⊕u1`, dimension `9+10=19`. This verifies the earlier E8 centralizer by an independent real-matrix wedge calculation; it does NOT constitute a new finite Poincare embedding.

The crucial caveat: this single **central** order3 element commutes with Lorentz and has only three elements. It is SU3 colour triality in the parallel model, not the 81-element noncentral four-dimensional additive Minkowski translations `F3^4`. Nor is the 19-dimensional, rank-five Lie algebra the rank-four SM gauge algebra. Any claimed full translation and hypercharge coexistence requires distinct actual translation generators and verified conjugation/commutators plus chiral physical matter.

`analysis/w33_20261010_toe36_spinorial_triality_translation_gate.py` → `data/w33_20261010_toe36_spinorial_triality_translation_gate.json`.

## 3. Rank-selected spatial vacuum test: uniform W33 hopping CANNOT choose rank three

Use SAME 80-vertex W33 Levi graph; choose r=1,2,3 independent fundamental graph chord voltages, with connected finite decks `Z3^r` and `N=80·3^r` vertices (240,720,2160). The spectra are explicitly computed by `3^r` Hermitian Bloch 80×80 diagonalizations. Every lifted graph has degree4, so Perron-Frobenius gives **exactly `λmax(A)=4`** and unique uniform eigenvector, hence a uniform free hopping `H=-tA` has one-particle ground `E0=-4t` for **ALL ranks**. For N free bosons, `E=-4Nt`. At a matched boson filling n with onsite repulsion U, a *uniform coherent-state mean-field variational energy* per vertex `e=-2tn+(U/2)n²` also does not distinguish rank.

The computed first nonzero p3 Laplacian eigenvalues agree at `~0.019845` across r=1,2,3 for this sparse three-chord voltage construction. Adding an EXTERNALLY chosen rank cost `κr` gives: `κ>0` selects r=1, `κ<0` selects r=3, `κ=0` all degenerate. This is a rigorous non-selection theorem for the given free hopping functional, and exposes the extra physical assumption required.

**Not shown:** a rank-changing operator, graph-geometry quantum Hilbert space, interacting thermodynamic vacuum, spontaneous dimensionality, causal relativistic metric or Einstein dynamics.

`analysis/w33_20261010_toe36_deck_rank_vacuum_selector.py` → `data/w33_20261010_toe36_deck_rank_vacuum_selector.json`.

## 4. A **local first-order wave operator** on W33's three-deck cover; important flat-band firewall

Starting from the rank3 cover of Round35, define the **160×80 local oriented incidence/gradient operator** `B(k)`, with edge row e=(a→b), `B[e,a]=-1`, `B[e,b]=exp(i k·f_e)`. Define 240×240 local bipartite Hermitian operator

`H(k)= [[0, B(k)†], [B(k), 0]]`.

The matrix identity is checked at multiple independent Bloch vectors:

`H²=diag(B†B,BB†)`, `B†B=L_W33(k)`.

Round35's lowest Laplacian band `λ(k)≈kᵀDk` therefore produces **local wave-like positive/negative branches**

`E±(k)=±sqrt(λ(k))≈±sqrt(kᵀDk)`,

a mathematical z=1, linear massless dispersion (unlike simple `H=-tA` whose band is quadratic). Five small-k directional checks match the acoustic tensor prediction within2%; velocities in lattice units are approximately `0.0778, 0.0798, 0.0810`.

**Fatal naive identification:** `B` is 160×80, so at each generic k the local `H` has **80 EXACT zero-energy flat bands** `ker B†`, and at k=0 it has 82 zero modes (two extra from the Laplacian Goldstone zero). These are edge-cycle / cohomology degrees and require a *physically justified gauge constraint* or different Hamiltonian. The operator has sublattice chiral symmetry but NOT four-dimensional Clifford gamma matrices, identified photon polarization, Fermi statistics, Lorentz boosts, the E8 finite spinorial rep or an emergent universal c. It proves a W33-derived LOCAL square-root construction is possible conditional on pre-imposed rank3 spatial winding.

`analysis/w33_20261010_toe36_incidence_relativistic_walk.py` → `data/w33_20261010_toe36_incidence_relativistic_walk.json`.

## 5. Independent on-shell QED running test of W33's bare fine-structure rational

Graph W33 bare proposal `α_W33^-1=137+40/1111=137.036003600360...`. CODATA 2022 physical Thomson/zero-momentum value `α(0)^-1=137.035999177(21)`, discrepancy `+0.000004423360...` = about210.6 reported standard uncertainties. **Already proved in Round35.**

Question: can standard electron-vacuum-polarization one-loop scale running rescue the exact equality parameter-free? In the **specified ON-SHELL, spacelike, electron-only scheme**, exact one-loop relation is

`α^-1(Q²)=α^-1(0)-(2/π)∫_0^1dx x(1−x)ln(1+(Q²/m_e²)x(1−x))`.

The integrand is nonnegative for real `Q²≥0` and strictly positive for Q>0, so `α^-1(Q)<α^-1(0)` ALWAYS. One can always fit the W33→CODATA difference if the *W33 rational is instead declared* a fictitious zero-momentum boundary value and CODATA numerical alpha treated as if it were measured at arbitrary **Q/m_e≈0.0144378**, or ~**7.38 keV**. That value is *selected retrospectively* by solving one scalar equation, NOT predicted by W33 or the Standard Model. CODATA actually refers to Q=0, so this cannot repair the 210σ Thomson conflict.

No graph-derived photon, electron mass, renormalization scale, QED beta function or boundary condition has been supplied. The exact rational is **mathematical**; fitting it with an invented scale is an additional free parameter, not a physics prediction.

Sources: NIST/CODATA official https://physics.nist.gov/cuu/pdf/RevModPhys.97.025002.pdf and on-shell QED vacuum polarization https://qft.org/gauge-theories-standard-model/quantum-electrodynamics/vacuum-polarization-running-charge/ .

`analysis/w33_20261010_toe36_qed_running_alpha_gate.py` → `data/w33_20261010_toe36_qed_running_alpha_gate.json`.

## Five-front verdict

1. **Chirality**: a legitimate index can isolate one `16` and cancel gauge anomalies, but only with explicitly added boundary geometry. Net chirality is not a finite inner E8 automorphism property.
2. **Translations+hypercharge**: actual independent 55D spinorial triality spectrum corroborates a 19D commutant, but the central Z3 is not the full finite Poincare translation group.
3. **Dimensional vacuum**: pure homogeneous W33 hopping cannot distinguish rank; adding rank-energy preference simply inserts what is meant to be derived.
4. **Relativistic wave**: a local incidence square root yields E~|k|, but 80 exactly zero flat bands and absent spinor/gauge/spacetime dynamics prevent a physical Dirac/photon assertion.
5. **Coupling**: QED running requires an unpredicted scale to match the W33 rational, and CODATA is already a Q=0 quantity.

**No complete experimentally validated TOE, realistic chiral generations, emergent Lorentzian spacetime, Standard Model electrodynamics, or physical quantum computer is established.** Every result has a runnable source, frozen JSON and focused regression test; parallel prior work is explicitly credited.
