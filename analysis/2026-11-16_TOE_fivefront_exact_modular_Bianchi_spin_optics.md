# TOE five-front follow-through: E6 filter symmetry obstruction, a two-mode KK chamber, second-order X8 metric jets, IIB spin topology, and active time-bin routing

**2026-11-16 | `wilcompute/W33-Theory` | starting remote master `35fce06cfb76ae3667f1bb715dad276f9f760f18`.**

**Summary:** Six exact or sharply qualified mathematical computations, two new reproducible JSON certificates and 29 independent cross-front regression tests. We investigated the recent parallel E6 triplet-filter staging and retained its files unchanged. These are not predictions of observed constants or a complete quantum theory of gravity. A physical unequal-flux 11D fluctuation matrix, the full eight-derivative action, the M/IIB differential charge dictionary, and a calibrated photonic apparatus remain open.

## Front 1 — E6: why hypercharge alone cannot protect the triplet-filter zeros

The in-progress local parallel implementation `analysis/toe_20261116_E6_triplet_exchange_filter.py` introduces `F(Phi)=(Phi²-4I)/5` on the up-type Higgs leg of the invariant E6 cubic. At the chosen integer-weight adjoint vacuum, `F(-3)=1` for the light doublet and `F(±2)=0` for dangerous heavy triplet sources. Its exact tree-level exchange certificate includes a surviving **separate heavy gauge-boson baryon-violating current**, so the polynomial is not a complete proton-decay protection mechanism.

Our new independent verifier evaluates every cubic monomial `det A+det B+det C-Tr(ABC)` using the repo's exact E6 integer hypercharge weights. **Each monomial has total Y charge zero**, as gauge invariance requires. Thus a discrete subgroup of Y cannot forbid only the triplet monomials while permitting doublet monomials: they are all invariant under that subgroup. Moreover, by Schur's lemma any extra finite symmetry *commuting with E6* acting on one irreducible 27 acts by a scalar, so it cannot independently split the components of that same representation. Family-dependent symmetries, broken noncommuting symmetries, spurion selections, geometric effects or a more sophisticated UV sector can evade this limited no-go; the claim is specifically about commuting single-27 symmetries and hypercharge alone.

### Exact two-messenger mixing counterexample

The polynomial filter zeros can be spoiled by **additional unfiltered heavy states**. For a toy pair of triplets with holomorphic mass

`M=[[m,mu],[mu,m]]`, up source `J_u=(0,y_u)`, down source `J_d=(y_d,0)`, tree integrating out both pairs gives

`W_eff=-J_u M^{-1}J_d=mu*y_u*y_d/(m²-mu²) = (mu*y_u*y_d/m²)+O(mu³).`

One pair's protected up source is exactly zero, yet a second unfiltered pair and a permitted holomorphic mass mixing reintroduce baryon violation. Mixing among *only zero-up-source states* would **not** do so. This is a concrete failure mode to investigate in the complete E6 messenger sector, not proof of decay in the current chosen superpotential.

### A crucial improvement on the earlier radiative warning

The **perturbative supersymmetric Wilsonian nonrenormalization theorem** does protect a *specified holomorphic superpotential* against perturbative corrections in a supersymmetric scheme, including nonrenormalizable holomorphic interactions. This qualifies the previous blanket warning that the filter coefficients are radiatively unprotected. It does **not** explain the tuned ultraviolet coefficients, prohibit already-allowed independent operators and messenger mixing, guarantee protection from SUSY breaking or nonperturbative dynamics, remove gauge-boson-mediated dimension-six proton decay, or compute physical canonical field rotations and thresholds. Source: Steven Weinberg, *Nonrenormalization Theorems in Nonrenormalizable Theories*, Phys. Rev. Lett. 80 (1998), https://doi.org/10.1103/PhysRevLett.80.3702.

**Falsification target:** enumerate every allowed E6-invariant mass mixing and independent baryon-violating operator in the complete matter/messenger system, compute their full effective mass inverse, and identify a symmetry compatible with all chosen Yukawas and proton limits. The reported `p->anti-nu K+` limit `8.2e33 yr` is cited in the existing report from a Super-Kamiokande presentation (https://www-sk.icrr.u-tokyo.ac.jp/~nakahata_s/kakenhi-kibanS/talk/Nakahata_SuperK_KMI2025_250305.pdf), not predicted by our code.

## Front 2 — Exactly two equal-flux BF-violating Fourier modes on an OPEN modular strip

For the established physical equal-flux, sphere-exchange-odd scalar–three-form KK branch,

`lambda_{m,n}=3pi |m+n*tau|²/Im(tau)`,
`m_-²L²=lambda-2-sqrt(4+16lambda)`,
`m_-²L² < -4  iff  0<lambda<12.`

Write `tau=x+i y` in the standard modular fundamental domain `|x|<=1/2, |tau|>=1`. We prove the following **exact open chamber theorem**:

> For *every* `|x|<=1/2` and `4/pi<y<pi`, the only signed Fourier modes with `lambda<12` are `(m,n)=(+1,0),(-1,0)`.

Proof: If `n!=0`, `lambda>=3pi*n²*y>12` because `y>4/pi`. If `n=0, |m|>=2`, `lambda>=12pi/y>12` because `y<pi`. For `m=±1,n=0`, `lambda=3pi/y<12`, since `y>4/pi>pi/4`. This open strip lies strictly inside the reduced modular region and is not a single exceptional shape. At `tau=i`, exactly four signed `(±1,0),(0,±1)` modes violate BF in this branch. At the hexagonal `tau=(1+i sqrt3)/2`, exactly six do. Our verifier enumerates all allowed wavevectors using rigorous analytic enumeration bounds for a range of shapes and checks the exact strip against many `x,y` points.

**Scientific correction:** The earlier four-mode min–max stability statement is a **square-torus** result, not a universal multiplicity theorem. The prior **shape-uniform existence and nonzero BF deficit theorem** is unaffected: it only guarantees that at least one unstable mode exists. The precise physical unequal-flux mixing and other KK sectors still have to be analyzed; neither a new finite-N threshold nor the full 11D spectral operator is claimed.

## Front 3 — Eight derivatives: nonzero quadratic X8 despite vanishing X8 and its FIRST variation

For `AdS5 x S2 x S2 x T2` at unwarped constant curvature, the curvature two-form matrix has `R^a_b=K_i e^a wedge e^b` in each maximally symmetric block. Hence `R wedge R=0` as a matrix of differential forms, and both `tr R²=tr R⁴=0`. Consequently the **background polynomial and its first curvature variation** vanish for

`P(R)=tr(R^4)-[tr(R²)]²/4` (the M-theory `X8` is proportional to this polynomial).

But an exact degree-four expansion gives the **quadratic coefficient**

`[t²]P(R+tD)=2 tr(R D R D) - [tr(R D)] wedge [tr(R D)].`

We independently verified this polynomial identity by computing `P(R+D)`, `P(R-D)`, `P(R)`, and `P(D)`, including the requisite quartic subtraction. The earlier unrestricted curvature two-form example gave a nonzero coefficient 48 in an eight-form mask. We went further: constructed a curvature perturbation `D_{ab cd}` as the sum of **two Kulkarni–Nomizu products of symmetric tensors**, with independent mixed `AdS5-S2` support, and verified in all 11 tangent directions

- `D_{abcd}=-D_{bacd}=-D_{abdc}`,
- `D_{abcd}=D_{cdab}`,
- `D_{abcd}+D_{acdb}+D_{adbc}=0` (first Bianchi).

This **Bianchi-valid local metric-jet** example produces the exact nonzero quadratic coefficient `-216,e^{01235678}` in our unnormalized Euclidean-frame exterior-algebra convention (bitmask 495). It is locally realizable as a curvature perturbation via an appropriate metric normal-coordinate 2-jet. Independent full polynomial finite-difference evaluation reproduces the coefficient exactly.

**What remains open:** This local metric 2-jet is not constrained to solve the full 11D linearized Einstein–C-field equations, preserve our relevant KK sector or obey global AdS boundary conditions. It does not determine the actual gravitational `C3∧X8` quadratic operator, because `C3_background` is generally not globally defined with nonzero magnetic flux. The other supersymmetric `t8t8R4`, parity-odd and mixed flux terms remain. It is, however, a **sharp obstruction to asserting that Riemann symmetries alone cancel quadratic X8**. See e.g. https://arxiv.org/abs/hep-th/0312069 for global C-field subtleties and higher-derivative literature on `C3∧X8`.

## Front 4 — IIB spin structure count is NOT the same as winding or Killing spinors

Let `Y(p,q)->S²xS²` be the circle bundle with nonzero Euler class `e=p x+q y`, `g=gcd(|p|,|q|)`. The existing integral Gysin verifier yields

`pi1(Y)=Z_g`, `Tor H²(Y)=Tor H⁴(Y)=Z_g` with linking pairing generator `±1/g mod 1`.

There is an additional exact constraint: the circle fiber has a trivial oriented tangent line, so `TY≈pi*T(S²xS²)⊕1` as real bundles. Since `w2(S²xS²)=0`, **every Y(p,q) is spin**. Distinct spin structures form a torsor over

`H¹(Y;Z2)=Hom(pi1(Y),Z2)=Hom(Z_g,Z2)`.

Thus there is **exactly one spin structure for odd g and exactly two for even g**. Meanwhile there are **g flat U(1) characters** `Hom(Z_g,U1)` and g winding classes. Our verifier checks examples such as `Y(6,6)`: 2 spin structures but 6 flat characters, and `Y(7,6)`: one spin structure and no nontrivial fundamental group.

These are different mathematical objects. Even g>2 allowing two spin structures does NOT mean a Killing spinor with the requisite Fourier deck phase descends, and the torsion classes are not yet established as conserved IIB Page charges or physical particle excitations. Computing physical fermionic KK harmonics still requires the Killing-spinor and full spin connection, not only `pi1`.

## Front 5 — A stationary passive network cannot demultiplex three time bins into one simultaneous three-rail quantum state

Represent an incoming photonic qutrit as orthogonal time bins `|r=0,t=0,1,2>`. A three-rail spatial Fourier interferometer requires the three amplitudes **at the same arrival time**. We construct an explicit lossless **24-dimensional permutation unitary** routing the three input bins to `|r=0,1,2,t=4>` on a model of 3 rails × 8 time slots. Such a transformation is mathematically unitary.

However, for a **stationary time-translation-covariant** network `U`, one must have `UT=TU`, where T advances every time slot. On input `|0,0>`, the required routing gives `UT|0,0>=|1,4>` but `TU|0,0>=|0,5>`, orthogonal states. Therefore **a stationary shift-covariant optical network cannot perform this exact time-to-simultaneous-spatial routing**. The implementation needs active time-dependent switching, a programmable synthetic-time processor, storage/feedforward or equivalent nonstationarity. This theorem distinguishes a lossless three-port spatial Fourier chip from the complete time-bin qutrit measurement. Relevant new optical research: *Hardware-Efficient Universal Linear Transformations for Optical Modes in the Synthetic Time Dimension*, PRX Quantum 7, 020305 (April 2026), https://doi.org/10.1103/yvcj-d7pb.

The constructed 24-dimensional permutation is a mathematical schedule **not** hardware. Timing jitter, fast-switch speed, routing insertion loss, mode overlap, detector dead time and memory reset must all be measured. The earlier event-ready four-MUB e-process and calibrated detector/false-herald analysis remain valid mathematical requirements, not a completed apparatus.

## Next falsification targets

1. Derive all allowed E6 heavy-triplet and gauge-current mixings, including Wilsonian holomorphic versus physical canonically normalized amplitudes, gauge-boson exchange, and proton lifetime at all relevant final states.
2. Construct the full gauge-constrained 11D metric–C-field KK operator on finite unequal-flux backgrounds; compute its physical eigenvalues and norms, preserving the exact two-mode modular strip and square-torus four-mode data as limiting checks.
3. Project the complete locally and globally consistent eight-derivative action onto **on-shell** BF-relevant fluctuations; determine if the Bianchi-valid quadratic X8 term survives the actual physical sector.
4. Construct the genuine differential-C-field/physical IIB Page-charge and spinor dictionary; separate winding, flat characters, spin structures and physical Killing-spinor deck lifts.
5. Implement the three-to-three active temporal routing circuit with real measured insertion loss and detector POVMs; run the predeclared four-MUB e-process on actual event-ready hardware data.

## Reproducers

- `analysis/toe_20261116_fivefront_exact_negative_controls.py`
- `analysis/toe_20261116_X8_Bianchi_metricjet_quadratic.py`
- `tests/test_toe_20261116_fivefront_chambers_X8_spin_router.py`
- `data/toe_20261116_fivefront_chambers_X8_symmetry_spin_router.json`
- `data/toe_20261116_X8_metricjet_Bianchi_secondvariation.json`

Run each Python verifier individually and
`python -m unittest discover -s tests -p test_toe_20261116_fivefront_chambers_X8_spin_router.py -v`.

Run earlier 2026-11-16 full six-front and E6-KK-qutrit tests as regression. Preserve the existing parallel-agent staged and untracked files; stage/commit only the five listed reproducibility files plus this report (six files total). These results **do not establish a theory of everything**, a full E6 phenomenological theory, a corrected supergravity vacuum or an observed photonic memory.
