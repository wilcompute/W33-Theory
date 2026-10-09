# Round 18: Five independent pressure tests on the W33 TOE program (9 October 2026)

**Provenance.** Follow-up to Round17 exact interaction traces and no-go theorems on the
public W33-Theory `master` branch. Native model inputs only; one optical
readout test is a deliberately constructed synthetic counterexample, not data from hardware.
Concurrent agents' unrelated paths and untracked files must be preserved.

## 1. Exact **fixed-U** two-boson orbit separation (new theorem)

Let A be the native 80x80 W33 Levi magnetic adjacency, D=dGamma(A) on the
3240-dimensional symmetric two-boson Hilbert space, and P the rank-80 projector
onto normalized same-vertex doublons. H(U)=D+UP and G_n=P D^n P on that
doublon subspace. The exact determinant-lemma/formal-series identity is

```
det(I-tH(U)) = det(I-tD)*det(I-U*t*G(t)),
G(t) = sum(n>=0) G_n*t^n.
R(t)=(I-U*t*G(t))^-1
Tr(H(U)^N)-Tr(D^N)
    = U*sum(j=0..N-1) (j+1)*tr(R[N-1-j]*G_j).
R[0]=I; R[n]=U*sum(j=0..n-1) G_j*R[n-1-j].
```

The update uses only 80x80 matrices. For the incidence bipartition G_odd=0,
halving the effective cost. Native G_n are computed from
`sum_k binom(n,k)(A^k)_{xy}(A^{n-k})_{xy}`.
The three edge phasors are Gaussian-rational
`(15+8i)/17,(4-3i)/5,(5+12i)/13`; reversed edges conjugate them.
Both reductions F_p[i] with p=1000003,1000033 preserve ring identities.
The p=1000033 algebra is a *split commutative algebra*, not a field.
A nonzero difference modulo either valid p proves a nonzero rational value.

**Results:** For each **U=2,8,20** and each prime, **the single 19th
trace moment** `Tr H^19` is pairwise distinct among the five representative
families (and the joint 17th/19th signature also separates). Since the
free moment is shared, its subtraction preserves the distinction.
For example p=1000003:

| U | Delta Tr H^17 across native orbits | Delta Tr H^19 across native orbits |
|---|---|---|
| 2 | 954638,954638,300310,521222,733726 | 224581,101947,437992,695317,712875 |
| 8 | 488901,488901,871598,755243,605256 | 617678,127142,409338,903080,522419 |
| 20 | 917521,917521,374259,583373,708407 | 251678,25341,863100,599661,835529 |

These are **fixed-interaction exact spectral separation certificates**, stronger
than Round17 generic-in-U trace-polynomial inequivalence. Toy 4-cycle direct
orthonormal Fock Hamiltonian verifies the full recurrence, and tests recalculate
the complete native five-orbit signatures. The result is **not** for the
Round16 floating-point phases [0.49,-0.74,1.22]; nor for all real U.

## 2. Graph topology, magnetic loop current, and autonomous chiral *toy* potential

Native W33 Levi point-line incidence has 80 vertices, 160 links, girth 8.
DFS enumerates **81 distinct simple eight-cycles through each link**, hence
exactly 160*81/8=**1620 distinct oriented-unidentified eight-cycles**.
This is a concrete graph-plaquette skeleton; the appearance of 1620 elsewhere
in Holonet counting is a *numerical analogy*, not an established isomorphism.

For the same Gaussian-rational phasors, differentiate a one-body eighth moment
with respect to the phase of the corresponding oriented flag:

`d/dtheta_e Tr A(theta)^8 = 8 Tr(A^7 * dA/dtheta_e).`

The three modular derivatives at p=1000003 equal
`[440117,760936,597906]` for **all five** reps. They are nonzero and become
their additive negatives under simultaneous flux reversal. Therefore these
moments sense chirality/orientation (relative to calibrated edge direction),
but do **not** distinguish the five geometric selector classes. Nonzero
modular values certify nonzero rational derivatives at the stated phasors.

Freezing all but one edge phase and assigning a **frustrated second-harmonic**
positive plaquette energy `+g*sum_{8-cycles touching edge} cos(2*holonomy)`
gives exactly `F(phi)=81g cos(2phi)`. Minima at +/-pi/2, with curvature
324g>0. This is a worked example of how a nonlinear gauge-flux potential
*might* make nonzero flux energetically preferred. **It does not select a
unique handedness**: F(phi)=F(-phi). In any finite T-invariant quantum theory,
a nondegenerate T-invariant ground state has zero expectation of a T-odd
observable. A real physical chirality selection requires physical preparation,
T-breaking, environment, or an appropriate infinite-volume limit.
This toy chooses its potential by hand and freezes most links.

## 3. Actual 176-field heterotic Z6-II cubic prefilter: what cannot be inferred

Using all 176 printed physical fields in the frozen source metadata, use
integer-embedded **all nine** exact U1 charges and count unordered cubic
monomials *with replacement* (a<=b<=c):
- **424** charge-neutral cubic monomials.
- **90** pass the stored exact corrected-R and nonR necessary tests.
- **334** fail those tests despite having zero total nine-charge vector.

Control: `(n_17,n_82,n_81)` passes while its charge-twin substitute
`(n_17,n_82,n_83)` does not, even though both have nine-component
zero charge, identical k/G/translation for n81/n83, and identical
weight list; the corrected-R and oscillator counts differ.

The stored `fields` schema lacks full constructing space-group elements,
oscillator **polarizations**, picture changing, full gamma group action,
worldsheet instanton solutions, and moduli. Therefore **none** of the
90 necessary candidates is a certified nonzero worldsheet cubic Yukawa.
Complete orbifold correlators/F- and D-flatness require the missing input;
inventing amplitudes would invalidate the program. Literature:
Kobayashi et al. arXiv:1107.2137 (Rules 4 and 5) and Parameswaran/Zavala
arXiv:1401.6162 (worldsheet instantons); plus recent refinements to Rule 4
should be examined when a full operator dataset is recovered.

## 4. Quantized-current vacuum: new star-adapted squeezed-Gaussian bound

Prior Round16: all 80 exact classical zero anchors have Poisson rank 8 and
a **scalar-width star-centered Gaussian** minimum
`1521/10 + sqrt(40053)/2 = 252.166228...`.
The quantum physical carrier is 78-dimensional; classical zero currents do
not imply a zero quantum eigenvalue.

Now choose q0,p0 exactly at each star, define a real Gaussian on W
with covariance C=t1|e><e|+t2|f><f|+t0*(P_W-|e><e|-|f><f|),
where e=q0/||q0|| and f is Gram-Schmidt(p0,q0); p covariance is C^-1/2.
The exact Wick expectation of commuting quadrature-product currents
is `sum_e((V_e*q0+a)^2+Var(V_e*q))*((U_e*p0+a)^2+Var(U_e*p))`,
where a=1/sqrt(20).

Six symmetry-separated W33 anchors (points/lines) return equal minima
within numerical tolerance: **229.065358769...**, compared with
252.166228... for the scalar-width star Gaussian (improvement ~23.10).
This is a *real squeezed coherent state* variational **upper** bound,
not a lower spectral bound or proof of the true ground state. It also
remains far above the prior **centered non-star complex-Gaussian**
trial ~128.88739 (and the prior non-Gaussian Ritz improvement).
Thus no evidence yet that a classical zero star wins quantum vacuum selection.
Minimizer is numerical, while each stated positive covariance defines a
legitimate normalized trial state regardless of optimization accuracy.

## 5. Proposed chirality photonics: independent controls still leave a no-go

A triple-randomized synthetic detection design independently reverses
the flux command r, an electronics-only sham e, and the detector assignment
d. If genuine optical current and undesirable leakage on the **same r
control wire** both enter as `beta_opt*r + beta_leak*r`, the regression
matrix with [1,r,r,e,d] has **rank 4 for 5 parameters**. Two entirely
different physical models `(beta_opt,beta_leak)=(.08,0)` and
`(0,.08)` generate *bitwise identical observables under the same noise*.
Detector swapping and electronics-only sham controls alone cannot
distinguish these. Thus the earlier two-sensor DID proposal is
**not self-certifying** against science-only switch-wire leakage.
A blocked-optics test, hardwired isolation, independently calibrated
phase actuation, or separate physical signal path is indispensable.
This is a test of identifiability, **not** an optical experiment.

## Reproduction and boundaries

- `python analysis/w33_20261009_round18_fixedU_resolvent_certificate.py`
- `python analysis/w33_20261009_round18_chirality_plaquette_audit.py`
- `python analysis/w33_20261009_round18_heterotic_cubic_information_bound.py`
- `python analysis/w33_20261009_round18_classical_star_squeezed_trial.py`
- `python analysis/w33_20261009_round18_optical_chirality_identifiability.py`
- `python -m pytest -q tests/test_w33_20261009_round18_five_frontiers.py`

Context and prior-art integrity: the general power of interacting two-particle
walks over noninteracting graph dynamics is prior literature (Gamble et al.,
*Phys Rev A* **81**, 052313 (2010), DOI 10.1103/PhysRevA.81.052313).
The contributions here are explicit native W33 checks and clean boundaries
between exact symbolic results, numerical variational states, synthetic
controls, and currently unknown dynamics. No mechanism deriving Lorentz
symmetry, Einstein equations, SM parameters, or a universal photonic processor
is asserted. The 150-page forty_points paper was audited in Round17; this
work builds on its definitions but does not replace that foundational analysis.
