# Independently motivated physical selection of a 3+2 vacuum: exact SU(5) adjoint theorem, dynamical rank-two projector, supersymmetric degeneracy and E6 invariant obstruction

**17 November 2026 | `wilcompute/W33-Theory`, independent physics research, Python/SymPy/SciPy/NumPy on TheHeavyCrown.** The W33 ten-context mapping was an INPUT motivating a question, not the mathematical source of the mechanism in this report. All new selector calculations use established adjoint-Higgs invariant theory, elementary spectral variational principles, rigid supersymmetry and global/gauge symmetry distinction.

**Answer:** A physical `3+2` alignment can emerge dynamically from an ordinary positive `Tr Phi^4` shape term in a bosonic `SU(5)` adjoint potential, or more interestingly from a gauge-invariant interaction `epsilon Tr(Phi Q)` with an INDEPENDENT dynamical rank-two projector `Q`. Neither amounts to a finished `E6` theory. The stronger algebraic obstruction is that the **full E6 adjoint has neither an independent cubic nor an independent quartic invariant**: the convenient pure-adjoint SU5 shape term cannot be inserted into E6 as a standalone renormalizable invariant.

## 1. Exact global minimization, no SU(5) vacuum ansatz assumed

Take a traceless Hermitian `5x5` adjoint `Phi`. Diagonalization by SU(5) and the fixed-norm constraints `sum x_i=0, sum x_i²=1` reduce shape selection to `Q=sum x_i^4`. The global inequality is

`7/30 <= Tr(Phi^4)/(Tr Phi²)^2 <= 13/20.`

We independently prove this EXACTLY using Lagrange multipliers, not sampling. Every stationary eigenvalue satisfies `4 x_i³ - 2 lambda_L x_i -mu_L=0`, so at most three distinct roots occur. For three roots, the absent cubic coefficient means they sum to zero; together with trace and positive multiplicity constraints this forces a zero root with opposite nonzero roots. The only three-root partition patterns of five are `3+1+1` (quartic ratio `1/2`) and `2+2+1` (ratio `1/4`). For two roots of multiplicities `k,5-k`, the quartic ratio is `((5-k)^3+k^3)/(25 k(5-k))`, i.e. `13/20` for `1+4` and `7/30` for `2+3`. The compact unit sphere ensures that these exhaust global extrema.

Thus global minima have normalized eigenvalues `(2,2,2,-3,-3)/sqrt30` or their negatives, up to permutation. On the fixed-norm traceless eigenvalue sphere the quadratic shape Hessian at the representative has strictly positive eigenvalues `2/3` (two directions splitting the 3-degenerate eigenvalues) and `8/3` (one splitting the 2-degenerate eigenvalues). Broken SU5 gauge directions are separately Goldstone/eaten directions, NOT included in this three-dimensional diagonal Hessian.

For the *nonsupersymmetric* renormalizable potential

`V(Phi)=-m² Tr Phi² +lambda(Tr Phi²)²+kappa Tr Phi⁴`,

the explicit region `m²>0,kappa>0,lambda+(7/30)kappa>0` yields the `3+2` vacuum as a global minimum. Its squared norm is `r²=m²/[2(lambda+(7/30)kappa)]` and energy `-m^4/[4(lambda+(7/30)kappa)]`. At `(m²,lambda,kappa)=(1,.35,.75)`, `V_SM=-0.476190476...`; `V_SU4=-0.298507...`, energy gap `0.177683...`. All 60 independently seeded multistart numerical runs with BFGS and precision-loss fallback agreed with the exact minimum. Conventional SU(5) adjoint-Higgs physics already contains this mechanism (see [Scholarpedia Grand unification](https://www.scholarpedia.org/article/Grand_unification), and [OUP Grand unification §14.2](https://academic.oup.com/book/57152/chapter/457412641)). What is original here is an independently executable exact certificate plus the attempts to embed, stress-test and improve selection.

The centralizer is `S(U3×U2)`, Lie dimension 12, yielding 12 heavy adjoint gauge-boson directions out of SU5's 24. This is a statement about symmetry breaking, **not** proton decay or observed fermion mass hierarchies.

## 2. Is "one of ten" even a physical question?

An A5 action on two-subsets of five objects is transitive: all ten weak pairs have stabilizer order 6. Their Johnson graph is `J(5,2)` (spectrum `6^1,1^4,(-2)^5`) and the complementary graph is Petersen (spectrum `3^1,1^5,(-2)^4`). The calculations cross-check the parallel repo's special-context counts, but the following conclusion comes from ordinary gauge theory.

If the five labels are directions of **gauged SU5**, all ten placements of fixed-sign `(2,2,2,-3,-3)` are related by SU5 conjugation. EVEN odd permutation matrices can be compensated by a diagonal determinant-minus-one factor that commutes with the diagonal VEV, so they have an SU5 representative. Therefore the ten placements are **one physical gauge orbit**, not ten distinguishable vacua. No extra physical symmetry breaker is needed merely to decide which named pair is "weak." Gauge invariants and relative alignment with other fields matter. Elitzur's theorem precisely warns against treating gauge-noninvariant order parameters as physical observables (original [Elitzur 1975](https://doi.org/10.1103/PhysRevD.12.3978)).

If A5/S5 is truly a **global physical** permutation symmetry, then these are ten physically distinct degenerate minima of each sign. A macroscopic transition may spontaneously choose one, but exact spontaneous breaking generically permits domains and interfaces, not a mathematically predetermined global label. The even potential also has a `Phi -> -Phi` Z2 that yields **two SU5-gauge-inequivalent sign orbits**. A cubic adjoint interaction can break that Z2 explicitly. Actual SU5 domain walls from an exact/approximate sign symmetry are discussed in [Vachaspati, Domain walls in SU(5)](https://doi.org/10.1103/PhysRevD.62.123506). Distinguish local gauge redundancy, global symmetry breaking, and true relative order parameters.

## 3. New independent mechanism: a dynamical rank-two projector selects the 3+2 shape even with kappa=0

Introduce a second **Hermitian adjoint-plus-singlet matrix field** `Q` with an effective constraint `Q²=Q,TrQ=2`. It transforms under SU5 by the same conjugation law as `Phi`. A positive *pinning* potential such as

`V_Q = nu Tr[(Q²-Q)²]+chi(Tr Q-2)²`, `nu,chi>0`,

has the manifold of rank-two Hermitian projectors as its zero-energy minima. **When the portal below is added with finite pinning, Q can deviate from an exact projector; the analytic theorem concerns the constrained/strong-pinning limit.** Q is an additional dynamical adjoint-plus-singlet field, not two fundamental SU5 fields with VEVs that would independently give weak gauge bosons masses.

Couple them by the gauge-invariant portal

`V_align=+epsilon Tr(Phi Q)`, `epsilon>0`.

At **fixed** `TrPhi²=r²`, trace-free `Phi`, the Cauchy–Schwarz inequality gives an exact global minimum over `Phi` for *any* fixed rank-two projector:

`Tr(Phi Q)=Tr(Phi (Q-2I/5)) >= -r ||Q-2I/5||_F=-r sqrt(6/5)`,

with UNIQUE minimizing matrix

`Phi_min=-r (Q-2I/5)/sqrt(6/5).`

Thus the normalized eigenvalues are automatically `(2,2,2,-3,-3)/sqrt(30)` and `TrPhi4/(TrPhi2)^2=7/30`, WITHOUT any independent `TrPhi4` coefficient. If radial potential is `-m² r²+lambda r⁴`, the full reduced energy is `-m²r²+lambda r⁴-epsilon r sqrt(6/5)`. For `(m²,lambda,epsilon)=(1,.35,.2)` the unique positive radial stationary norm is `r=1.2466366438141965` and it is the global radial minimum. The minimal potential also **selects the relative sign** of Phi against Q. Rotating one weak eigenvector into one colour eigenvector costs exactly `(5epsilon r/sqrt30)*sin²(theta)`, establishing a positive relative-orientation stiffness. The formula is the [Ky Fan variational principle](https://www.sciencedirect.com/science/article/am/pii/S002437952200372X) specialized to the trace pairing of a rank-two projector.

This is a legitimate **two-field constrained effective-theory selector**, not a derivation of the rank-two field from the E6 repo. The central unresolved dynamical question becomes where the rank-two projector's pinning potential and field representation originate. It selects the shape and **relative** orientation, never an absolute physically distinguished pair of SU5 gauge labels. The computed correction to opposite-sign configuration's optimally readjusted projector is a nonzero energy penalty. Numerical tests include 120 random Hermitian traceless matrices and continuous SU5-plane rotations.

## 4. Rigid supersymmetry blocks a naive import of the bosonic result

The standard renormalizable N=1 SU5 adjoint chiral superpotential

`W=(m/2) TrSigma²+(y/3)TrSigma³`

has traceless F-equation `F_i=m x_i+y(x_i²-TrSigma²/5)=0`. Every eigenvalue solves the same quadratic, so at most two distinct eigenvalues occur. Exact algebra identifies THREE inequivalent Hermitian D-flat F-flat orbits:

- `Sigma=0`;
- `Sigma=(m/y) diag(2,2,2,-3,-3)`, `TrSigma²=30m²/y²`, `W=5m³/y²`;
- `Sigma=(m/(3y)) diag(-4,1,1,1,1)`, `TrSigma²=(20/9)m²/y²`, `W=(10/27)m³/y²`.

ALL have `V_F+V_D=0` in **rigid supersymmetry**, so merely writing this conventional cubic superpotential permits the desired vacuum but DOES NOT select it by energy. A small phenomenological soft term `-epsilon TrSigma²` favors the 3+2 branch over 4+1 at **first order** by `delta(V_SM-V_SU4)=-(250/9)epsilon m²/y²`; full deformed global minimization and tachyon tests remain necessary. Supergravity adds Kähler-dependent covariant F-terms and vacuum energy, so `-3|W|²` by itself is not a consistent selector. A published SU5 adjoint SUSY benchmark is described in [Shirai SUSY SU5 notes](https://indico.desy.de/event/11392/attachments/3791/4359/Shirai.pdf); radiative SUSY-breaking alignment mechanisms exist in [arXiv:1202.2845](https://arxiv.org/abs/1202.2845).

## 5. Crucial E6 obstruction: no pure-adjoint cubic OR independent quartic shape invariant

A conventional SU5 adjoint cubic is NOT an E6-invariant cubic of a single 78. Indeed the primitive E6 Weyl-invariant degrees are **`2,5,6,8,9,12`**, excluding both 3 and 4 (see [Harvard Elkies Lie groups notes](https://people.math.harvard.edu/~elkies/M222.23/index.html)). We independently verified the stronger algebraic claim in the repo's own 27×27 cubic realization:

- Form the 45 nonzero monomials of `I3(A,B,C)=detA+detB+detC-Tr(ABC)`. Their 45×27 diagonal cubic-invariance incidence matrix has kernel dimension **6**, the E6 Cartan rank.
- For an ARBITRARY symbolic `H=sum_{i=0}^5 t_i H_i` in this kernel, SymPy expands the full power-sum polynomials and proves **identically** `Tr27(H³)=0` and `Tr27(H⁴)=[Tr27(H²)]²/12`.
- The fifth-order trace is **NOT identically zero**. For the actual integer-weight hypercharge direction in the W33 repo the moments are `(TrY²,TrY³,TrY⁴,TrY⁵)=(180,0,2700,-4320)`. Independent generic samples also satisfy the cubic and quartic identities.

By the Cartan/Weyl restriction theorem, these identities obstruct a degree-three or independent degree-four **single-E6-adjoint** invariant. A shape-sensitive `SU5` quartic must be generated by other fields or effective interactions AFTER a prior breaking of E6, or through higher-degree invariants, not by a renormalizable E6 pure-adjoint quartic. Note that E6 **does** have the well-known cubic invariant of its `27` **matter/Higgs** representation; that is not the same as a cubic invariant of the **adjoint 78**. The prior E6 degree-five calculation also warned that a naive fifth-order term generally shifts the desired vacuum's F-equations. We have NOT derived the required E6 completion.

## 6. Other four independent physical falsifiers executed in the same packet

These scripts were built alongside the independent vacuum study:

- **A5/W33 orbit + KK Rayleigh:** reproduced the ten-context transitive action with stabilizer order 6 and exact Johnson/Petersen graphs. Strengthened KK stability by the **projected** Courant–Fischer theorem: if a k-dimensional *physical, gauge-admissible* subspace has negative BF quadratic form, no bound on off-block mixing is required to retain at least k negative physical modes. Demonstrated with arbitrary 2/4-dimensional blocks and offdiagonal mixing up to 100. Still lacks the actual unequal-flux 11D constrained quadratic operator.
- **Integral flux topology:** computed complete cohomology ker/im quotients of the artificial degree-four differential `d_G(alpha)=G4 cup alpha` on `S2×S2×T2`. For `(Nxy,Nxt,Nyt)=(5,6,6)`, degree-five torsion is `Z5×Z5` but the gcd-controlled torsion in degrees four/six is absent. This is **NOT an established M-theory Page-charge group or physical AHSS differential**.
- **Quadratic X8 selection:** for externally reflection-even, homogeneous metric scalar perturbations on `AdS5×M6`, only external degree even can occur in the Pontryagin eight-form, while a local internal `C3_background` requires external/internal `(5,3)` to wedge nontrivially. This locally excludes the considered contribution under the stated reflection symmetry, **not** all on-shell 11D modes or the full supersymmetric R4+G4 corrections.
- **Four-MUB qutrit hardware:** proved uniform setting choice is minimax among matched-outcome four-MUB witnesses: product states in the most likely basis enforce a separable threshold at least `1/3+(2/3)max_b w_b>=1/2`; uniform settings achieve exactly 1/2 by the 4-MUB 2-design identity. Derived loss/visibility feasibility floors and the condition under which a *nondestructive, pre-setting local success herald* preserves the separable null. **No physical memory, herald or optical experiment was constructed.**

## Falsifiable next-stage program

**(1) Gauge vs global test.** Identify whether the "ten contexts" represent physical global states or only SU5/Weyl gauge placements. Write down gauge-invariant relational observables coupling vacuum orientation to the matter/Higgs spectrum. No domain-wall prediction follows from gauge permutations alone.

**(2) E6 genuine selector.** Embed an independent adjoint-plus-singlet projector or another rank-two condensate using actual E6 representations and an F/D-flat, radiatively consistent sector. Account for the absence of pure-adjoint cubic/quartic E6 invariants and the previously identified fifth-degree F-term obstruction.

**(3) Proton test.** Recompute all gauge-mediated and Higgs-mediated dangerous operators, their flavor structure, and triplet masses after introducing the second dynamical field. A gauge-invariant alignment potential is not automatically proton-safe.

**(4) Eleven-dimensional test.** Derive the gauge-constrained unequal-flux metric–C3 projected quadratic form on the 2-mode modular strip and determine whether the on-shell higher-derivative X8/R4 terms affect its BF defect. No numerical KK eigenmass is derived here.

**(5) Experimental selector test.** Analyze the rank-two portal's scalar and gauge excitation spectrum, coupling scales, first/second-order phase transition, and any discrete global-sector domain walls. For the separate photonic direction, require realistic quantum nondemolition herald efficiency, not an assumed ideal flag.

## Reproducibility

Run:

```shell
python analysis/toe_20261117_E6_A5_KK_projected_minmax.py
python analysis/toe_20261117_M5_X8_qutrit_minimax.py
python analysis/toe_20261117_SU5_adjoint_vacuum_selection.py
python analysis/toe_20261117_SUSY_SU5_Fflat_vacuum_competition.py
python analysis/toe_20261117_rank2_projector_dynamic_portal.py
python analysis/toe_20261117_E6_adjoint_invariant_shape_obstruction.py
python -m unittest discover -s tests -p test_toe_20261117_SU5_dynamic_context_and_fivefront.py -v
```

Each verifier writes its own uniquely named deterministic JSON certificate under `data/`. Run prior targeted regression suites and preserve other agents' existing dirty, staged and untracked work. Commit **only** the six owned Python programs, six JSON certificates, this report and the focused tests.

**No Theory of Everything, observed SU5/E6 vacuum, realistic E6 supersymmetric model, established Page-charge duality, corrected 11D spectrum or quantum memory hardware has been produced.**
