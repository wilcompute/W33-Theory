# Passes12016–12020: running Majorana matching, a stable flavour target, one-sided soft protection and exact native dispersion

17 October2026. Reservation3a55d9d8484c504c815b6d6f42f5e892c84907bb follows the five targets after12015. **This packet does not establish a complete TOE, selected moduli/flux, radiatively complete strong CP, nonlinear native GR or a global native chiral measure.** Papers are unchanged.

## Intake and prior ownership

GitKraken fetched and reviewed74c69f542, a formula-catalogue update only, and fast-forwarded before reserving12016–12020. Catalogue status labels are automatic indexing, not scientific authority. Read12011–12015 sources/report/certificates,12007 Majorana conventions,12002 native heavy-frame construction,11995 harmonic metric and11594 gravity refinement controls. Read11967's mixed-trace alignment/counterterm obstruction and the11965/11973 mediation context. Current paper/site frontier and RESULTS_INDEX remain reference boundaries.

Result-first searches covered31-term quartic coefficients, one-sided Hermitian soft blocks/resolvent residues, projector-invariant potentials, Weinberg running and native-word measure differentials. General RGE, spectral theory, invariant potentials, gauge mediation, Berry frames and magnetic flavour are prior art. The contributions are the explicit named operators, exact coefficients, conditional constructions and their controls.

##12016 — rematch neutrinos on the charged common-scale branch

Keep all eleven12011 quark/charged-lepton comparisons and its fitted matching scale4.2033160x10^6GeV. Use the same complex Barr mixing A, charged matrix and CP-adapted bare basis. The real bare Majorana matrix is n=LL^T with

```
L=[[exp(p0),0,0],[p2,exp(p1),0],[p3,p4,1]],
p=(0.17949509395694016,-0.4295888152402716,0.9583199350202315,
   -1.0661365699775118,-0.37716229548993896).
```

At the matching scale C=A^T n A. Transform consistently to the charged eigenbasis and evolve its shape to MZ. Remove the universal scalar factor of the Weinberg RGE: it does not affect mixing or mass ratios and is absorbed into the supplied atmospheric splitting normalization. For charged eigenvalues y_i, let P_i=y_i²/(16pi²). Implement **all flavour-dependent two-loop Weinberg terms**, in the notation of Ibarra–Leister–Zhang2411.08011 eq24:

```
qi=-(3/2)Pi-[57gprime²/16-33g2²/16-5T/4]Pi/(16pi²)+(19/4)Pi²,
dCij/dlnmu=(qi+qj+2PiPj)Cij.
```

Gauge/Yukawa backgrounds are still the prior **one-loop SM flow**. This is a specified two-loop C5 shape correction, not a complete two-loop SM/BSM fit. Entrywise integrated evolution is independently checked against the full matrix ODE.

The fitted MZ observables are sin²theta12=.304, sin²theta23=.573, sin²theta13=.02219 and Delta21/Delta31=.0295499800876. The two-loop changes relative to one loop, at the same bare parameters, are approximately(4.40e-9,5.58e-8,-2.63e-11,-1.57e-9). There are now **fifteen supplied fitted comparisons** on this branch. Five real Majorana shapes fit four oscillation constraints: one local shape direction remains, and the displayed masses/J are conditional witnesses rather than predictions. Signed CP comparisons retain the prior holomorphic/Weyl convention caveat.

A finite matching diagnostic rescales the UV-to-SM down Yukawa by1+delta while leaving its internal ratios and mixing unchanged. Jointly refit all eleven charged/quark constraints for each supplied delta:

| universal down threshold delta | fitted matching scale, GeV |
|---|---:|
|-.01|5,884,134.77|
|0|4,203,316.03|
|+.01|3,026,674.88|

These are **actual refits**, not just linear sensitivities. Delta is not a calculated particle threshold coefficient. Its large scale effect demonstrates that a precise-looking matching scale is not a protected natural constant. A full ultraviolet spectrum, finite thresholds and updated experimental inputs still need matching. The new neutrino sector would need another rematch on each threshold-deformed branch.

##12017 — an explicit stable CP-even potential, with supplied target coefficients

Introduce two Hermitian3x3 orientation-flavon fields A,B, eighteen real components, transforming by simultaneous U3 conjugation. Set the auxiliary radial spectra to a=(1,2,4), b=(1,3,7), and set B's orientation to the actual12011 quark mixing orbit in A's eigenbasis. These auxiliary spectra are not physical Yukawa eigenvalues.

Use the Lagrange spectral polynomials

```
Pi(A)=product_(k!=i)(A-a_k I)/product_(k!=i)(a_i-a_k),
Qj(B)=product_(k!=j)(B-b_k I)/product_(k!=j)(b_j-b_k).
```

Take ten real CP-even invariants: TrA^k,TrB^k for k1..3, and TrPi(A)Qj(B) for i,j0,1. Fix their target values c_r at the displayed quark orbit and fixed positive weights w_r. Then

```
V=mu0^4 sum_r w_r² (I_r(A,B)-c_r)²
```

is a nonnegative, simultaneous-conjugation-invariant **degree-eight polynomial**. At its zero, the full18-field Hessian is2J^TJ. Analytic invariant derivatives give rankJ=10, ten positive normal directions and eight symmetry tangents. With the declared row-normalized weights the smallest positive dimensionless Hessian eigenvalue is about1.06963e-7. Direct energy differences, analytic-vs-finite derivatives and a second unitary basis check the result.

The conjugate orbit has exactly the same target invariants and energy: the potential does not explicitly choose a CP sign. The eight zero modes are **symmetry** modes; for global SU3 they are Goldstones. Gauging the family action and assigning physical matter consistently require a separate kinetic/anomaly/loop completion. Local transverse stability does not prove a global census of every zero orbit.

This answers the construction question: a stable observed-orientation target is possible beyond11967's single mixed-trace alignment potential. But its c_r,w_r and radial targets are engineered inputs. It does not explain their values, stabilize the theta moduli, or identify an economical renormalizable UV parent. A finite fit is still not a vacuum-selection principle.

##12018 — a gauge-mediated boundary and a larger exact safe class

A standard post-heavy messenger sector W=X Phi Phibar uses5+bar5 messengers, real X=M+theta²F and no direct matter/CP-sector couplings. Choose M=10^6GeV, F/M=2x10^5GeV, below the supplied Barr matching scale. In the leading small-F/M² approximation, scalar masses arise at two gauge loops and gaugino masses at one. Casimirs distinguish Q from d^c while preserving family degeneracy within each representation. The illustrative Q and d^c soft masses are about1493.28 and1383.97GeV, with gluino mass844.83GeV; a gauge-only leading-log A_d is real, about-279.41GeV. These are supplied messenger/EFT benchmarks, not pole-mass predictions. Finite-x=.2 corrections are not included.

The resulting declared colored one-loop matching vanishes analytically by the previous singular-basis alignment argument. Its small floating residual is numerical cancellation, not a physical theta prediction. Importantly, the SUSY inventory is **not spliced into** the pure-SM running fit; SM–MSSM and heavy thresholds would require a simultaneous rematch.

### One-sided Hermitian flavour mixing is also safe in these channels

A stronger sufficient condition follows directly from the resolvent. In the quark singular basis let RR=diag(r_i), LR=diag(ell_i) be real, with arbitrary Hermitian LL. For real z outside the squark spectrum,

```
[(z-Sq)^-1]_LR = [z-LL-ell(z-RR)^-1ell]^-1 ell(z-RR)^-1.
```

The bracket is Hermitian; its inverse has real diagonal. The remaining factor is real diagonal, so every diagonal LR resolvent entry is real. Its spectral residues, including summed degenerate residues, are real. Therefore **every real spectral loop function has real LR diagonal entries**. Both the determinant-trace quark phase and each species-weighted gluino phase vanish in the specified one-loop self energies. LR need not be proportional to the quark masses. Interchanging L/R gives the partner result.

An independent well-conditioned toy gives combined phase approximately-1.4e-18 for arbitrary complex Hermitian LL. Adding a noncommuting RR perturbation gives-1.6033e-6; CP conjugation reverses it. Tests also use nonproportional real diagonal LR and several independent real spectral functions.

This means a top-Yukawa **LL insertion alone** cannot defeat this safe class. The first attempted finite-difference susceptibility in the hierarchical physical benchmark was cancellation noise; it is explicitly labeled as such in the certificate, not interpreted as a physical derivative. Actual RG evolution can also generate opposite-side and LR terms. The one-sided statement is not an all-orders strong-CP solution: neutral portals, forbidden operators, messenger/heavy thresholds, vacuum shifts and higher loops remain uncomputed.12008 owns the universal special case and12013 the narrower all-spectral sufficient class; standard gauge-mediation/MFV mechanisms are external prior art.

##12019 — exact native continuum symbol through fourth order

Use the actual135 native edges,27 sites and primitive four-period voltages of11991. With unit native weights and capacity M=sqrt(detH)=2/27, expand the Bloch operator B(k)^dag B(k)/M. Fix the acoustic eigenvector's mean to1 and solve successive mean-zero correctors using(L0+11^T/27)^-1. Fredholm solvability gives exact rational eigenvalue coefficients. This is computed on the actual27x27 matrix, not inferred from dimensions.

For k=epsilon p,

```
lambda(epsilon p)=epsilon² q2(p)+epsilon⁴ q4(p)+O(epsilon⁶),
q2=5p0²+5p0p1-6p0p2+5p1²-6p1p3+6p2²-6p2p3+6p3².
```

The odd first and third coefficients vanish exactly. The complete q4 is a31-monomial rational polynomial stored in the certificate and reconstructed symbolically by the producer. For p=(7/10,-3/10,1/5,1/2),

```
q2=61/20,
q4=-119603/3240000.
```

Direct Bloch eigenspectra at a=.16,.08,.04,.02 verify

```
lambda(a p)/a²=q2(p)+a²q4(p)+O(a⁴),
```

with successive errors shrinking by approximately4. A changed unimodular deck marking preserves the full Bloch operator. q4 is not proportional to q2²: its coefficients on e0 and e2 give ratios-1/300 and-11/1944. This is a coordinate-independent failure of full metric isotropy at fourth order; it does not invalidate the leading acoustic metric. The full graph operator stays positive; a truncated derivative expansion is a long-wavelength statement.

This supplies a native flat scalar continuum calculation and its leading anisotropic lattice correction. Curved inhomogeneous homogenization, spin transport, a renormalized Einstein action, refoliation constraints, Lorentz signature and physical Newton/cosmological constants remain open. Setting hbar=c=1 leaves a unselected. The previous conditional27-scalar heat tower cannot substitute for this native operator calculation or for the missing curved proof.

##12020 — an explicit local determinant frame and native current interface

Compose the actual native period words (lengths5,19,4,14) into four SU5 links. Use the standard10+bar5 representation and a one-cell4D Wilson kernel. On the displayed topologically trivial patch build

```
P=(I+sign(gamma5 DW))/2,
F=P E(E^dag P E)^-1/2,
L=iTr(F^dag dF).
```

The fixed reference E is specified by the free onsite chirality. The actual reference overlap has minimum eigenvalue about.28625, so the frame is invertible; an initially imposed>.5 condition was unnecessary and was corrected to the actual positive-invertibility requirement. The frame spans a30-dimensional chiral subspace.

Two native-edge variations give projector curvature

```
iTr P[d_sP,d_tP] approximately0.00203709534.
```

Differentiating the explicit frame connection agrees to below1e-7. Thus10+bar5 continuum anomaly cancellation does **not** make this finite-cutoff measure curvature zero. A nontrivial measure connection is required.

Implement the full ordered product derivative of each native period word, including inverse links. It agrees with independent finite differences and local native gauge transformations. Conditional on an admissible coarse global current Lc, the determinant-line interface is

```
Lnative=Phi*Lc + Lheavy + iTr[(Pfactor-Pplus) T dT^dag],
```

where Phi is the bounded native period-word map, T the bounded cell-tree unitary and Lheavy the26 Kato-trivial optical-sector connections of12002. This names the map and its basis correction. It does not implement Lc or independently establish a global-measure theorem.

The internet/repository audit checks Craig2610.09093v1 sections4,9–10: smooth all-volume locality, representation-faithful admissibility, divergence cancellation and global holonomy are distinct requirements. The present finite patch verifies none of those uniformly over all volumes/topological sectors. The preprint remains an external candidate to audit; its proof is not claimed as ours or independently certified here.

Finally use12015's actual72x3 internal zero-mode isometry K. The map S->K S K^dag embeds a family operator into the internal overlap carrier and intertwines the computed H27 action; the certificate records its numerical error. Tensoring three identical chiral species multiplies the local determinant curvature by3, but does not select flux3 or justify adding that internal torus to native4D spacetime. This is an actual operator interface, not a generation claim from an instanton index.

## Primary external checks

- [Ibarra–Leister–Zhang, two-loop Weinberg RGE](https://arxiv.org/abs/2411.08011), equations20–24: C5 coefficients are prior art; only the stated flavour-dependent terms are used on the one-loop background.
- [Giudice–Rattazzi, gauge mediation](https://arxiv.org/abs/hep-ph/9801271); [Evans et al., SUSY Nelson–Barr](https://arxiv.org/abs/2002.04204): messenger formulae and the importance of soft/threshold conditions are prior art.
- [Craig, candidate global non-Abelian measure](https://arxiv.org/abs/2610.09093), v1: conditional audit target, not an independently validated input theorem.

## Reproduction

Producer `analysis/w33_pass12016_12020_neutrino_vacuum_native_measure.py` reconstructs all five certificates, including the rational31-term quartic. The portable neutrino search starts at the older12007 branch and writes a separate exploratory record. Focused new regressions run together with the prior12011–12015 controls; hosted replay and exact-SHA receipts are reported separately. A common microscopic action selecting all supplied targets and physical scales remains absent.
