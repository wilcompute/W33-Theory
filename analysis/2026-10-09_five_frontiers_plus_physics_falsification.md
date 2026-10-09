# 2026-10-09 — Five main fronts plus two extra TOE falsification tests

**Scope and provenance.** Checked W33 Theory GitHub master at `5534df1bc` and the already dirty authorized desktop checkout before starting; left parallel-agent files alone. Read latest Pass11794/11795/11796, the existing Pass11389 native FCC graph cover, Pass11778 compact-resolvent theorem, Pass11786 rational Wick spectra, and Pass11793 full-field charge character; checked the original 176-field heterotic ledger and the prior nontrivial-current optical and geometric certificates. These new results are mathematical/model calculations, **not** physical verification of a TOE, a graviton, photonic gate, or a fully consistent MSSM string vacuum.

## 1. Attempting a quantitative Hamiltonian gap: 74 classical flat directions

We revisited `H=sum_{160} (V_e.q+a)^2(U_e.p+a)^2`, `a=1/sqrt20`, and the existing Pass11769 **common zero** of its classical principal symbol. With exact integer coordinates (q0,p0), every current factor product vanishes. At any such zero the classical Hessian equals twice the Jacobian Gram of the 160 current bilinear symbols. In the 156-dimensional classical constrained phase space `W_q⊕W_p`, take

```
q0 = a*(39,-1 (39 times),0 (40 times))
p0 = a/39*(-39,1 (39 times),0 (40 times)).
```

Using integer-scaled incidence matrices, the current linearization reduces, up to an overall positive factor, to

```
[J_q | J_p] = [Y_e * (40 V_e) | 39 X_e * (40 U_e)]
X_e=(40 V_e).q_integer+40, Y_e=(40 U_e).p_integer+1560,
X_e*Y_e=0 for all e.
```

Exactly four X factors are nonzero, so J_p has rank≤4, and all J_q rows lie in the rank-78 two-sided augmentation space. A modular Gaussian-elimination certificate over F_32003 gives **rank(J_q)=78** and **rank(J_p)=4**; supports of the two blocks occupy disjoint edge rows at the common classical zero, and therefore the *exact rational* rank is **82** and the Hessian has **74 flat directions**.

**Meaning:** A purely quadratic harmonic approximation centered on this classical zero cannot confine all 156 phase directions. The quartic/higher terms and CCR-driven subelliptic uncertainty are indispensable to any quantitative lower bound or actual excitation gap. This does not challenge the separately proved positive-but-unquantified spectral gap of the full Schrödinger Hamiltonian. It is an original structural **obstruction to the naive harmonic lower-gap tactic**, not a numerical full-H lower energy bound.

Producer: `analysis/w33_20261009_classical_zero_hessian_rank.py`, data certificate of modular ranks and analytical upper bounds. Earlier independently verified 160-current principal symbol Gram was full rank; this new Hessian rank is for their **evaluation at one common classical zero**, not a contradiction.

## 2. New Pass11796 13-field classical D-flat branch: six quadratic F-term hazards

The parallel Pass11796 source owns a 176-field full-lattice **order-two** candidate matter symmetry and exact 13-field D-flat VEV support, including four hidden SU(2) doublets of two flavors. Its full gauge mass Gram has rank11/12 and leaves exactly hypercharge in the Abelian+hidden-SU2 sector. This supersedes the older six-singlet candidate for a physical MSSM-like Higgs analysis. F-flatness and full orbifold equivalence remain open.

Enumerated all support-only gauge-invariant monomials through degree4, and monomials involving exactly one outside field and up to three support fields, using the complete nine rational U1 charges, the necessary Z6 twist-sector sum, full-field parity, and nonzero hidden-SU2 invariant contractions. Supports carrying any other nonabelian charge with no available conjugating field are rejected. This is a **necessary-filter**, not a computed CFT superpotential.

In degree2 there are **six gauge-, sector- and nonabelian-eligible support bilinears**:

```
n9*n54, n37*n38,
epsilon(n35,n36), epsilon(n35,n40),
epsilon(n39,n36), epsilon(n39,n40).
```

The four hidden-doublet couplings assemble into a complex 2x2 mass matrix M, pairing A=(n35,n39) with B=(n36,n40). On the Pass11796 D-flat orientation, A1 and A2 span both hidden colors and so do B1 and B2. With `W2=sum_{i,j} M_ij epsilon(A_i,B_j)`, the entire set of hidden-doublet F_A vanishes **if and only if M=0**, because its independent derivative matrix has determinant **-1**, and the two singlet-pair bilinears similarly require zero coefficients in the **bilinear-only** theory.

**Physical boundary:** Additional cubic/quartic/higher-order superpotential terms may cancel these derivatives, or the coefficients might be forbidden by full Z6-II space-group, R/H-momentum, instanton or gamma rules. Gauge neutrality and point-group sum do **not** establish generation. The source field export is incomplete, so we do not claim a string-vacuum exclusion.

Producers: `analysis/w33_20261009_new_higgs_13vev_F_filter.py`, `analysis/w33_20261009_doublet_quadratic_F_obstruction.py`. Reference for selection-rule completeness: Kobayashi, Parameswaran, Ramos-Sánchez, Zavala, *Revisiting Coupling Selection Rules in Heterotic Orbifold Models*, arXiv:1107.2137.
## 3. Nontrivial ground/excitation symmetry: explicit 24/15 He2 trial sectors

The corrected eleven-state Wick/Ritz producer used point- and line-symmetric collective even Hermite states. Those trial states belong to the **trivial** PSp(4,3) symmetry sector; no variational energy difference between them could determine ground-sector multiplicity or spontaneous symmetry breaking.

Constructed the actual 40-point and 40-line He2 fluctuation spaces. Each PSp permutation representation has exact decomposition `1+24+15`. For same-side He2 Gaussian overlaps, the graph-scheme Gram is `I + A/9 + (J-I-A)/81`; its constituent Gram eigenvalues are `8/3` (trivial), `32/27` (24-dimensional), and `16/27` (15-dimensional). The 40x40 incidence matrix `N` has singular values 4 (once), sqrt6 (24), and 0 (15). Therefore the nontrivial **24-type** mixes two point/line modes in a Hermitian 2x2 block, while each **15-type** is a 1x1 block.

Recomputed all real/complex expectation matrix blocks directly from the **sign-corrected** 78-coordinate current-squared action, using the already checked eight-incidence-orbit Gaussian integral, and compared exact-degree 13/14 Gauss–Hermite quadrature (max energy difference below 4e-13):

- 24-dimensional constituent (two eigenvalues): **142.7193362242** and **145.1724550873**;
- 15-dimensional point and line constituents: **143.6110807403**, twice.

These are Rayleigh-Ritz **upper bounds within nontrivial invariant sectors**, not the full spectrum, an actual first excitation or a numerical lower gap. They establish that the earlier 11-state trial space was blind to symmetry-breaking sectors and give concrete inputs for an eventual sector-resolved spectral exclusion/ordering.

Producer `analysis/w33_20261009_nontrivial_he2_ritz.py`, JSON floats and raw orbital blocks.

## 4. Three independently randomized optical controls: genuine third-order contrast

Earlier two-factor randomization `S` (pump sign), `G` (gate on/off) could reject pump-sign-only detector artifacts, but a `S*G` detector response without nonlinear photons still faked the gate. Now add an independently randomized binary optical-route switch `R` (interaction arm or bypass). Form the **three-way interaction contrast** `T=sum_i S_i G_i R_i Px_i(Py_i²-vy)`.

For a modeled quartic interaction present only when both gate and route are active, and Gaussian vacuum input, the mean of **4T/N** is the original minus-theta/sqrt39 nonlinear witness. Instrument artifacts proportional only to S or SG vanish in this three-way mean if statistically independent of randomized R. Under the *sharp route-null* that varying R does not affect any measured outcomes, Hoeffding supplies exact finite-N type-I control against arbitrary temporal drift, conditional on the readouts and other randomizations.

Independent synthetic AR(1) Gaussian drift rho=.98, Gaussian electronic noise and strong S/G-linked readout backgrounds; N=90,000 shots, 72 replicates in each arm, alpha=.01 gave:

| Synthetic data arm | rejections |
|---|---:|
| Detector background independent of route | 0/72 |
| Modeled quartic nonlinear interaction | 51/72 |
| Spurious detector effect proportional to S*G*R, no optical gate | 72/72 |

The reconstructed mean of 4T/N in the true-interaction simulations was -0.03168 vs analytic -theta/sqrt39≈-0.03044. The third control resolves the prior *SG-only* artifact but not the genuine **SGR detector confound**. Distinguishing that requires a physically validated sham/bypass path and diagnostics; adding a formal random switch alone cannot solve identification in the presence of corresponding instrument interactions. These counts are seeded toy simulation statistics, not actual laboratory efficacy.

Producer `analysis/w33_20261009_three_control_photonic_causal.py`, data parameters and results.

## 5. Exhaustive point-triple orbit and symmetry-breaking selector

Reused the established BT1688 full 25,920-element literal PSp(4,3) permutation group (not previously asserted novel) and the 40-point symplectic W33 model. Classified all **9880 unordered triples** under that group into **five** orbits:

| representative | size | commuting pairs | contained in a line | pointwise stabilizer | dim H1 fixed |
|---|---:|---:|---|---:|---:|
| (0,1,2) | 160 | 3 | yes | 27 | 3 |
| (0,4,5) | 360 | 0 | no | 24 | 3 |
| (0,1,4) | 2160 | 2 | no | 6 | 15 |
| (0,4,8) | 2880 | 0 | no | 3 | 27 |
| (0,1,22) | 4320 | 1 | no | 3 | 27 |

The exact fixed-cycle formula `dim H1^K=#edge orbits(K)-#vertex orbits(K)+1` is independently checked for pointwise/setwise stabilizers on each representative. Thus **two** types of point-triples (160 and 360) have exactly three invariant cycle directions; the other three types select 15 or 27.

As a **sixth, outside-the-box explicit toy dynamics**, construct the fully PSp-invariant classical selector energy on any triple T,

```
E(T)=3 - # of symplectically commuting point pairs in T.
```

Its exhaustive integer energy level distribution is:

```
E=0:160   E=1:2160   E=2:4320   E=3:3240.
```

This toy Hamiltonian chooses the **160 collinear triples** as its degenerate minima, each possessing the order-27 pointwise stabilizer and rank-three fixed-cycle directions. The toy energy gap to the other orbit classes is 1 in arbitrarily chosen units. It **does not uniquely select a triple or derive spatial propagation**; the 160fold degeneracy is mandated by full symmetry, and any physical spatial metric/FCC dispersion must be taken from or extended beyond the already prior-owned Pass11389 native cover. It is an explicit test of how finite symmetry breaking might select a rank-three period mechanism, not 3+1 Einstein gravity.

Producer `analysis/w33_20261009_all_triple_orbit_breaking.py`, JSON all five orbits, group orders, full edge/vertex orbit sizes and toy energy histogram. Comparison: Pass11389 owns the primitive FCC rank-three graph cover and acoustic metric; these results do not supersede it.

## Validation and independent next steps

The new focused tests rerun the original scripts and verify certificate claims rather than only checking the stored JSON. Full-H numerical lower energy/gap, true quantum ground irrep, F-flatness and true worldsheet coupling coefficients, real optical hardware and intrinsic Lorentzian gravity **remain unproved**. The new tests, JSON, scripts and this report are committed together; unrelated parallel dirty files are not staged.

Top five distinct future fronts: (1) explicit subelliptic/control-distance quantitative spectral lower bound; (2) full CFT worldsheet record and derivative constraints for the six bilinear and higher-order candidate F terms; (3) 24/15 sector expansion with certified rational interval enclosures and true ground-state representation; (4) calibrated sham photonic route that disentangles SGR instrument interactions from optical propagation; (5) rigorous 160-vacuum toy selector dynamics with tunnel splitting, thermodynamic limit, and induced FCC acoustic geometry rather than choosing a triple by fiat.
