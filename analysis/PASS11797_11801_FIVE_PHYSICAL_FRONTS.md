# Passes11797–11801: global parity, a fixed-vacuum mass obstruction, and actual dynamics

All five follow-ups to Pass11796 were executed. The strongest outcome is constructive global gauge parity **together with an exact obstruction to a clean MSSM spectrum on the current13-field support**. These are compatible: a D-flat Higgs branch with an unbroken parity can still have unacceptable mass ranks. No completed TOE, F-flat string vacuum, physical mass scale, numerical lower spectral gap or Einstein dynamics is claimed.

## Inputs, prior ownership and replay

- Pass11796 owns the13-field D-flat support, full rank11 gauge Higgs Gram and the primitive binary character. Pass11793 owns the integral charge lattice and candidate family/Higgs basis.
- Pass10974 owns the corrected non-prime-plane `R1+6*theta-gamma` charge. The current work uses it; the older uncorrected selection was already withdrawn.
- Pass11518, in `w33_pass11516_11520_local_geometry_quantum.py`, owns the two-hop rank-six metric repair. Pass11389 owns the actual parabolic line-cover geometry. Pass11769 owns the current Hamiltonian, Pass11786 its rational interval tools, and Pass11778 the compact-spectrum result.
- Parallel commits `cdfebaf1f` and `02119075f` arrived during this run and were read with their scripts and certificates. Their October9 round4/round5 reports own the bilinear-only gradient obstruction, conditional no-oscillator quadratic veto, symmetry-resolved24/15 Ritz bounds, pointwise global step-five transport bracket theorem, sham optical controls and160-triple hopping model. The present full model metadata resolves their stated worldsheet-data gap; corrected actual R charges forbid all six pure-support bilinears and move the leading necessary superpotential to degree8. The meson-gradient reduction here applies to the full W, beyond their bilinear-only case. Their global bracket theorem is useful for a future coercive spectral bound; their finite selector gap remains a different Hamiltonian. No parallel file is overwritten.
- The original benchmark model `Z6II_34__SM_20260917_1558.model` was reopened in orbifolder1.2.1. The compressed input freezes **all176 fields,328 left-chiral weight states, nine16-dimensional U(1) embeddings, eight shift/Wilson vectors, fixed points, oscillator counts, R and gamma data**. Every embedding dot every weight reproduces its rational charge exactly. The earlier24-anchor limitation is removed for this calculation.

Producer: `analysis/w33_pass11797_11801_five_physical_fronts.py`. Certificate: `data/w33_pass11797_11801_five_physical_fronts.json`. The independently checked named-coupling snapshot is `data/w33_pass11797_corrected_named_coupling_checks.json`. Tests: `tests/test_w33_pass11797_11801_five_physical_fronts.py`.

Reproduce the five mathematical producers and independent controls:

```sh
OPENBLAS_NUM_THREADS=1 python3 analysis/w33_pass11797_11801_five_physical_fronts.py
OPENBLAS_NUM_THREADS=1 python3 -m pytest --noconftest --ignore-glob='tests/test_*.py' -q \
  tests/test_w33_pass11797_11801_five_physical_fronts.py \
  tests/test_w33_pass11796_parity_complete_abelian_higgs.py \
  tests/test_w33_pass11794_hidden_center_vacuum.py
```

The optional original-program probe is rebuilt with `python3 analysis/w33_pass11797_build_probe.py --orb "$HOME/orb"`. It requires the external orbifolder build and GSL/readline dependencies. Pass a model, a text file of space-separated exact field names (one request per line), and `gamma-corrected` to the resulting probe. Only exact, unique labels bypass the original combinatorial sector enumeration; ambiguous labels fall back to it. Two degree-eight and all six finite queries were checked against the unaccelerated recursion. Original gauge and constructing-element/conjugacy-class space-group filters are retained. The R adapter changes a private cached R contribution; actual oscillators/geometry remain available in the original sectors. **Orbifolder's random placeholder coupling strengths are ignored.** Hosted replay regenerates the five mathematical fronts from frozen model/probe inputs; it does not rebuild the external CFT program.

## 11797: actual selection and a sharp F-term question

The13-column charge matrix has rank8 and a5-dimensional kernel. Every kernel vector has zero entries on the FI core `n17,n47,n50,n80,n82`. Thus **no pure-support holomorphic neutral monomial can contain any of these five fields, at any order**.

The invariant ring is

\[
\mathbb C[x,y,M_{11},M_{12},M_{21},M_{22}],\qquad
x=n_9n_{54},\ y=n_{37}n_{38},\ M=A^T\epsilon B,
\]

with hidden-doublet flavors `A=(n35,n39)`, `B=(n36,n40)`. The charged baryon product is `det(M)`, rather than a seventh independent neutral generator. Corrected R charges are `R(x)=(2,-1,0)` and `R(y)=R(Mij)=(7,0,-1)`. Necessary superpotential selection is

\[
a=1\pmod3,\qquad b=3\pmod6,
\]

where `a` counts x and `b` counts y/mesons, with an even cross-meson count from the fixed-point parity. The first possible term is **degree8, `W8=x P3(y,M)`**. Its19 invariant terms comprise16 distinct elementary-field multisets. All19 submitted requests pass the actual named gauge/space-group filters and gamma-corrected R rule. This establishes selection, not19 independent physical amplitudes or nonzero values.

At the declared orientation, `A` and `B` are invertible and `M=diag(t,-t)`. Exact differentiation gives

\[
F_A=\epsilon B(\partial_M W)^T,\qquad
F_B=-\epsilon A\partial_M W.
\]

Consequently **all four doublet F terms vanish exactly when the complete meson gradient vanishes**; the two nonzero singlet pairs also require `Wx=Wy=0`. A generic nonsingular leading cubic has no nonzero critical point. Actual coefficients and higher orders decide whether this branch has a solution.

There is an additional sharper outsider question. Gauge charges uniquely force the FI factors of any `n81`-linear term to be `n17*n82`. All orders therefore have

\[
F_{81}=n_{17}n_{82}\,[\lambda+G(x^3,y,M)].
\]

The multiplier has x degree0 mod3 and total y/meson degree0 mod6, with the same even cross-meson parity. Its first nonconstant correction is `x^3`, six additional elementary VEV powers. The cubic `n81*n17*n82` passes the original gauge/space-group filter and corrected R rule. For its G2 plane the actual oscillator counts give1 holomorphic and4 antiholomorphic left oscillators, with twist sum2 and only antiholomorphic instantons: the necessary Rule5 inequality **1<=4 passes**. A nonzero cubic amplitude would obstruct F-flatness sufficiently near the neutral-invariant origin. **Its amplitude, remaining fixed-point/lattice-sum conditions and cancellation possibilities are still open.**

## 11798: the parity has a global E8 cocharacter

Using the original nine U(1) embedding vectors and the HNF charge basis constructs the exact vector

\[
t=(0,6,0,0,7,-9,13,5;\ -20,0,0,0,118,-4,118,2).
\]

Both halves belong to E8: they are integral with even coordinate sum. `t/2` does not belong to E8×E8, so the gauge-torus element `g(P)=exp(i*pi*t.P)` is nontrivial of order2. Its action reproduces the chosen binary parity on **all328 massless weight states**, not just one anchor per field.

Pairing t with the eight original shifts/Wilson vectors gives

\[
(8,0,0,0,107,107,0,285).
\]

These are integers. E8 self-duality then makes `t.P` integral for **every** string momentum coset `P=l+kV+sum ni Wi`, proving `g²=1` beyond the finite massless ledger. The reconstructed U(1) covector has anomalous-coordinate coefficient exactly0. Its continuous gravitational and cubic traces on the full chiral spectrum are0. This removes the universal-anomalous-axion shift in the supplied basis; **model-dependent/blow-up axion charge matrices and nonperturbative consistency remain unsupplied**.

## 11799: the current support cannot lift every colored exotic

An augmented17-row charge lattice includes all nine gauge charges, four non-R selection charges, three corrected R charges and the hidden SU2 center. Lattice non-membership gives exact all-order annihilator certificates. Membership alone permits signed powers and is insufficient for a mass term.

The crucial stronger check is holomorphy: the five FI-core exponents are uniquely fixed for every external operator. A negative or nonintegral fixed exponent excludes the coupling **at every perturbative holomorphic order**, regardless of arbitrarily many neutral insertions.

In the actual7×10 colored mass matrix, the four rows

\[
\{d_1,d_3,d_6,d_7\}
\]

have possible neighbors only

\[
\{bd_1,bd_7\}.
\]

Hall deficiency is2, giving **rank<=5 of7 at all orders**. At least two triplets cannot pair, leaving at least two extra colored vector pairs beyond the three chiral anti-triplet families. This is a fixed-support obstruction, independent of unknown coefficients. The declared `Hu=bl1` up-Yukawa mask has only its(1,1) entry possible, so **up rank<=1 at all orders**. These conclusions require changing the support, Higgs identification or mechanism before a realistic spectrum is possible.

The remaining fractionally charged visible sectors are also obstructed: the `bx/x`2×2 colored matrix (hypercharges ±1/6) has **rank0 at every order**, and the `v/bv`14×14 half-charged singlet matrix has **rank<=8**. At least two fractional-color pairs and six half-charged pairs remain unlifted. Exact charge-core exclusions and necessary discrete masks are frozen for every entry; exhaustive Hall checks independently verify both bounds. These are elementary holomorphic mass blocks before electroweak breaking, not a complete component-level weak-doublet or effective meromorphic mass model.

The six finite necessary requests (three degree-five colored entries, the cubic top entry, and two outsider terms) all pass the actual named gauge/space-group/corrected-R check. They do not overturn the all-order exclusions.

The direct polynomial Weinberg3×3 mask is zero. Among all29 odd SM/hidden singlets as unassigned right-handed-neutrino candidates, the Dirac mask has structural rank<=2 and its `l4` row is zero; the Majorana mask has structural rank29. These are necessary masks, **not physical neutrino masses**. Integrating out heavy states can create meromorphic effective coefficients; absence of a polynomial Weinberg operator is not by itself a no-go for that mechanism. No seesaw inverse or physical neutrino identification was assumed.

An additional all-order search tests **every43 even SM-neutral elementary fields outside the support**, using exact one-variable real-cone inequalities rather than an insertion cutoff. Only `n69,n74`, both hidden SU4 fundamentals, relax the up-mask beyond rank1. As sole new hidden-SU4 charged flavors, neither admits a positive-degree holomorphic invariant: the epsilon contraction of four identical commuting vectors is zero. The current support has no other SU4 charge. Thus **no single elementary addition repairs the declared up rank**. The result points to coordinated hidden flavors or a different Higgs basis; it does not settle those alternatives.

## 11800: a full infinite-Hilbert-space spectral residual

For the original160-current Hamiltonian and the named Gaussian, the exact action is

\[
J_e^2\psi/\psi=(X+a)^2[(fX+a+iZ)^2+2m/t].
\]

All25600 ordered edge pairs fall into six exact integer covariance classes. Rational outward-rounded Wick moments through degree8 enclose `||H psi||²` and the variance. An independent five-node, four-variable Gaussian quadrature checks a separate covariance implementation and also recovers the mean energy.

The trial energy is about128.8873914, `||H psi||²` about17715.6557965, and

\[
\operatorname{dist}(E,\operatorname{spec}H)\le\sigma,
\qquad \sigma<33.221923.
\]

The exact rational upper endpoint is stored in the certificate; its approximate value is33.22192243984417. This residual includes the entire Hilbert space, not a finite Ritz projection. Its large size exposes how much spectral error remains. **It does not identify the ground state or certify a numerical lower gap.** A complementary excited-state bound or coercive certificate is still needed; newer parallel variational upper bounds remain separate valid inputs.

## 11801: native matter stress and the microscopic metric fibers

All480 distinct native two-hop channels, including156 with zero harmonic displacement, satisfy at every Bloch momentum

\[
L_2(k)=8L(k)-L(k)^2.
\]

The identity is independently tested at zero and nonzero momentum. Uniform two-hop conductance kappa leaves the harmonic drawing unchanged and multiplies the acoustic tensor by `1+8*kappa`. At kappa=1/8 this gives **K=(27/1600)I** in the declared graph units.

The640-channel response has rank6. An exact six-channel right inverse realizes every small symmetric tensor perturbation in the explicit coordinate order `(Kxx,Kyy,Kzz,Kxy,Kxz,Kyz)` while preserving positive weights for sufficiently small changes. Rank-six repair itself belongs to Pass11518; this packet names the full uniform Bloch operator and conductance-to-matter map.

A response-null conductance change can affect the energy of a microscopic vertex-localized scalar, while its affine acoustic energy change vanishes. Therefore **microscopic metric fibers cannot be silently identified with gauge redundancy**. For affine `phi=p.x`, `deltaE=40*p^T deltaK p`.

The actual scalar graph Hamiltonian, with kinetic densities rho and spring weights w, has exact cell conservation. Sharing half each spring between endpoints gives outward flux

\[
I_{ab}=\frac{w_{ab}}2(\phi_a-\phi_b)(\dot\phi_a+\dot\phi_b),
\qquad\dot E_a=-\sum_b I_{ab}.
\]

Its acoustic action has an explicit zero-shift metric map

\[
N=(\det K/\rho)^{1/4},\qquad
h=(\rho\det K)^{1/2}K^{-1},
\qquad \rho=\sqrt{\det h}/N,\quad K=N\sqrt{\det h}\,h^{-1}.
\]

A second, non-diagonal positive-definite realization checks these identities. This builds a minimally coupled scalar and its matter response. **Einstein-Hilbert dynamics, gravitational constraints, selected spatial parabolic, physical scales and the cosmological constant have not been derived.**

## Newly arrived round6 integration and validation

Parallel `f2a813f3b` was read in full, including all five producers, tests and six certificates. Its frozen11-field excerpt matches the corresponding entries of this packet's full metadata exactly. It independently confirms the actual corrected-R bilinear veto and outsider cubic selection. Its new global coefficient bound `sum_e(V_e.q+a)^2 >= 8+(4-sqrt(6))*||q||²` complements the prior global transport bracket theorem, while remaining short of an operator-level lower bound. He2+He4 sector upper bounds and finite coupled-selector/calibration models retain their stated domains. These are parallel-owned results; none of their files is changed here.

Final local combined new/prior/round4/round5 controls: **45 tests PASS47.12s**. The full intake harness reports no rediscovery collisions, no forced arithmetic and clean intake across the five scientific files; a final explicit guard after fractional-exotic extension also reports no collisions. Dedicated hosted replay covers frozen branch controls, all five mathematical producers and independent regenerated checks.

## External checks used

The original program and selection-rule literature were consulted before interpreting the probes:

- [Orbifolder program,1110.5229](https://arxiv.org/abs/1110.5229).
- [Coupling selection and corrected Rule5,1107.2137](https://arxiv.org/abs/1107.2137), particularly the corrected version3: oscillator inequalities depend on which classical instantons exist.
- [Non-prime-plane gamma phases and Rule6,1301.2322](https://arxiv.org/abs/1301.2322). The gamma contribution and additional worldsheet rules cannot be replaced by raw point-group charge conservation; Rule6 is not an independent restriction for Z6-II.

The useful next physical branch is constrained by the new mass/Higgs obstruction, rather than by a missing count or an unsupported interpretation of a dimensionless eigenvalue.
