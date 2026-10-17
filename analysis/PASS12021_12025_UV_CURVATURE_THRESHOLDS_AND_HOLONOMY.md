# Passes12021–12025: mixed soft kernels, a global CP-pair vacuum, curved native recovery, calculated thresholds and closed-loop measure transport

17 October2026. Reservation `6d6a48b4f66c9ad8838593a13c0d1acc04b7ee68`. This executes the five followups after12020. **The full TOE, a parameter-free flavour vacuum, complete radiative strong CP, nonlinear native GR and a global native chiral measure are not established.** No paper is edited.

## Intake and ownership

GitKraken fetched before reservation and again before publication; no incoming science superseded12016–12020 at intake. Read the prior producer/report/certificates,11995 harmonic metric,12009 capacity completion,12002 native heavy-sector construction,11665 auxiliary-parent/Schur warning,11967 flavour alignment obstruction,11978 singlet-soft scope and11225 residual-symmetry exclusion. Revisited the forty-points paper's physics/epilogue frontier: a dynamical principle, a continuum with dynamical curvature and computed numbers remain open.

Result-first searches included the mixed `Im(Eij Fji)` kernel, a36-real-field/28-positive-mode parent, two simultaneous-U3 vacuum orbits, native conformal recovery, calculated SQCD matching and determinant holonomy. Prior11665 already owns the auxiliary-field method in this corpus, on a different38-field Witting parent. Standard mass insertions, unistochastic reconstruction, conformal identities, MSSM thresholds and Kato transport are external prior art. The new content is the stated map, its particular application and its independent controls; these general tools are not claimed as discoveries.

##12021: the first independent two-sided soft insertion, and a leading-source cancellation

Work in the real quark mass basis M=diag(m_i), with a positive baseline squark operator made from real species blocks

```
S0_i=[[l_i,ell_i],[ell_i,r_i]],
Delta_i(z)=(z-l_i)(z-r_i)-ell_i^2.
```

Perturb LL by epsilon E and RR by eta F, with E,F Hermitian. The mixed resolvent is

```
R E R F R + R F R E R,
Im [coeff_(epsilon eta) R_LR,ii]
 = sum_j ell_j Im(Eij Fji)/(Delta_i Delta_j).
```

Proof: the only two paths from Li to Ri through distinct species j have imaginary parts proportional to `u_i w_i` and `-v_i^2`; their difference is `1/Delta_i`. The source also verifies a rational symbolic two-species instance, while regressions check arbitrary complex three-species matrices independently. This extends12018's exact zero on either coordinate axis to a named mixed response.

For the repository convention `B0(x,S)=-integral_0^1 log(t x+(1-t)S) dt` plus a real scheme constant, use the resolvent representation of the logarithm and exchange the convergent integrations:

```
Im coeff_(epsilon eta) B0(x,S)_LR,ii
 = -sum_j ell_j Im(Eij Fji)
   integral_0^infty dq q/[(q+x)Delta_i(-q)Delta_j(-q)].
```

The baseline is positive, so the integral is regular and convergent. Quark determinant and gluino phase weights are then applied with the actual12013 loop convention. On the well-conditioned declared benchmark, their coefficients are respectively `-2.7957811552e-5` and `+1.2014416568e-5`, totaling `-1.5943394984e-5`. Independent finite differences at h=.04,.02,.01,.005 converge quadratically; these are coefficients per supplied perturbations, not a physical theta prediction.

A useful cancellation matters for the radiative reading: if `F=Mdag E M`, then `Eij Fji=m_i m_j |Eij|^2` is real. This leading linked-source channel is zero even though both sides mix. Therefore counting two generated spurions is insufficient; their actual relation matters. Full soft RG, generated LR terms, independent UV spurions, neutral portals and higher loops still need calculation. The dangerous mass-insertion mechanism itself is already in the Nelson–Barr literature.

##12022: a renormalizable parent and exactly two classical vacuum orbits

Introduce four Hermitian3 matrices A,B,X,Y:36 real fields. Use the same target invariants and positive weights as12017, but replace every A² by X and B² by Y. Thus

```
Itilde=(TrA,TrX,TrAX,TrB,TrY,TrBY,
        Tr Ptilde_i(A,X) Qtilde_j(B,Y), i,j=0,1),
Ptilde_i=(X-(a_j+a_k)A+a_j a_k I)/[(a_i-a_j)(a_i-a_k)],
V/f^4=sum_r w_r^2 (Itilde_r-c_r)^2
      +||X-A²||F²+||Y-B²||F².
```

All residuals have degree at most two in these fields; the potential has degree at most four. Physical dimension-one fields are f times the displayed dimensionless matrices. For example the auxiliary term becomes `f²||Xphysical-Aphysical²/f||²`, which is renormalizable. The action is CP-even and invariant under simultaneous U3 conjugation. This is a specified bosonic renormalizable parent, not a completed matter theory.

At zero energy the auxiliary constraints hold exactly. Three power traces fix each simple spectrum by Newton identities. Four projector overlaps then fix the complete3x3 bistochastic matrix of relative eigenvector moduli. Orthogonality of the first two rows is a triangle with nonzero area `|J|/2`: it has exactly two orientations up to row/column phases. The third row is fixed up to phase. Hence **the entire classical zero set consists of exactly two simultaneous-U3 orbits**, exchanged by CP, for this generic target. Both are global minima because every term is nonnegative. Trace-square constraints bound all fields in the zero set. The numerical reconstruction gives J=±3.4935133167e-5 and checks both unitary representatives.

The full residual Jacobian has rank28, giving28 positive Hessian modes and8 symmetry tangents. The smallest positive full eigenvalue is about3.67754e-9 in the declared canonical normalization. Finite auxiliary masses change off-shell behaviour: the relaxed light Hessian is the actual Schur complement, not the frozen-auxiliary one. It has10 positive modes and8 zeros; the smallest positive is about1.06585e-7. Analytic derivatives, energy controls and another unitary basis verify this construction.

**What remains:** c_r,w_r, radial spectra and f are supplied target parameters. Renormalizability does not derive their values, stabilize the theta moduli or prove quantum naturalness. The global SU3 version has8 Goldstones; gauging it and coupling the physical fermions need anomaly, kinetic and loop completion. The finite symmetry-only obstruction11225 is not contradicted.

##12023: an actual inhomogeneous native recovery sequence

Use all135 native edges and27 sites. Solve the harmonic vertex correction chi so `h_e=v_e+chi_j-chi_i` and `H0=sum_e h_e h_e^T/27`. On the cover put vertices at `x=a(n+chi_i)` and supply

```
w_e=exp(2sigma(physical bond midpoint)),
M_i=M0 exp(4sigma(x_i)), M0=2/27.
```

The frozen cell metric is `H(x)=exp(2sigma)H0`, so the capacity-completed metric is `g(x)=exp(2sigma)g0`. A centered bond difference of a smooth test field is `a h_e.grad f+O(a³)`. Riemann sums therefore give the conformal4D Dirichlet energy and mass. Harmonicity minimizes the local frozen cell energy. This proves the stated smooth recovery/consistency expansion; a full liminf, spectral or heat-trace convergence proof is not supplied by that expansion alone.

The actual periodic test uses `sigma=.12cos x+.04sin2x`, `f=sin x+.2cos2x`. At N=16,32,64,128,256, native Rayleigh errors shrink by approximately4, approaching5.46351376217. Keeping the capacity fixed instead approaches approximately5.66476070731, a concrete failure control. An integer relabelling of all27 cell origins preserves the native results.

The exact4D conformal identity on a periodic domain is

```
R=exp(-2sigma)(-6 Delta_g0 sigma-6|grad sigma|g0²),
integral sqrt(g)R=6 integral exp(2sigma) grad sigma.H0.grad sigma.
```

The same native energy applied to sigma reproduces this integrated curvature with second-order refinement, approaching0.0233608323233 per coordinate volume. This is a curved conformal native recovery calculation. Choosing this particular conductance-gradient action is still additional dynamics. In the Euclidean Einstein convention `S=-integral sqrt(g)R/(16piG)`, its conformal sign is negative: a positive native energy does not automatically give the Einstein sign. No general ten-component Einstein action, quantum determinant limit, Lorentz signature, constraints, Newton constant, cosmological constant or selected a follows. Natural units hbar=c=1 leave a and f undetermined.

##12024: replace arbitrary delta by a calculated spectrum contribution

Supply a running input MSSM spectrum at Ms=2TeV: Q=2.5TeV, uR=2.4TeV, dR=2.2TeV, L/eR=2TeV, M1=1.5TeV, M2=1.6TeV, M3=2TeV, mu=1TeV, heavy Higgs2TeV, tanbeta10 and A=0. These are model inputs, not measured pole masses or a solved SUSY/electroweak vacuum.

Run the prior SM below Ms and full three-matrix one-loop MSSM Yukawa equations above it. Convert gprime to the SU5 normalization used by the MSSM equations. Include the calculated leading tanbeta-enhanced SQCD term

```
Delta_g=2alpha_s/(3pi) M3 mu tanbeta I(mQ²,mdR²,M3²),
I(a,b,c)=integral_0^infty q dq/[(q+a)(q+b)(q+c)]>0,
YuMSSM=YuSM/sinbeta,
YdMSSM=YdSM/[cosbeta(1+Delta_g)], YeMSSM=YeSM/cosbeta.
```

The positive-integral definition fixes our loop-function sign convention. Its equal-mass limit is1/(2m²), and scale/symmetric closed-form controls pass. This term is3.5708289865% for the stated positive-mu spectrum. Actual eleven-comparison theta/Barr refits give:

| mu input, GeV | included Delta_g | fitted scale, GeV |
|---:|---:|---:|
|-1000|-.03570829|719,999,476.79|
|0|0|138,321,793.53|
|+1000|+.03570829|30,103,970.50|

The zero-mu row is an algebraic zero-threshold control, not a physical heavy-Higgsino benchmark. The producer independently re-evaluates each fit. A regression evolves the matched texture down through both EFTs and the finite matching map, recovering the original low-scale comparisons.

The changed branch also requires a new Majorana fit. Evolve C5 shape with `q_i=+y_i²/(16pi²)` in the MSSM and `q_i=-3y_i²/(32pi²)` in the SM; universal running and the sin²beta matching factor are absorbed in the supplied atmospheric normalization. Four oscillation comparisons are rematched, retaining fifteen fitted comparisons. These are one-loop shape equations;12016's two-loop SM shape correction is not silently claimed in the new MSSM inventory.

This is **not complete precision MSSM matching**. Finite electroweak/Higgs/top/lepton terms, full nonuniversal self energies, MSbar–DRbar conversions and higher loops remain omitted. The primary threshold paper explicitly shows why the dominant approximation can be inaccurate. A messenger-to-low-scale soft solution, Higgs vacuum, UV unification and coefficient/scale selection remain open.

##12025: implement the local current and check closed-loop reconstruction

On12020's actual native period-word map and one-cell10+bar5 Wilson operator, use the fixed reference E and projector P. The implemented local frame current is

```
L_eta=(i/2)Tr[(E^dag P E)^-1 E^dag [P,delta_eta P] E].
```

Derive deltaP by the exact spectral Frechet divided difference of the projector, with deltaWilson computed through actual ordered native words and differentiated wedge² minors. Independent finite differences check deltaP and the frame-current trace. This computes a current, rather than only the previous two-form curvature.

Vary the same two native edges around the rectangle `s=±.12,t=±.10`. Integrating this current gives0.000114009230221184. Independently approximate Kato transport on the full60-dimensional Hilbert space by polar direct rotations between successive projectors. With8,16,32 segments per side, determinant-phase errors shrink by approximately4, ending at2.78e-9. Unitarity/intertwining errors are below3e-13; reversing the loop reverses its phase. Sampled kernel gap is at least.6935 and the reference Gram eigenvalue at least.2411. Sampling is not a uniform bound over an unspecified domain.

Finite simultaneous-root gauge conjugation obeys `F(Ug)=R(g)F(U)R_E(g)^dag`, with detR_E=1. This is a tested finite-patch equivariance statement. A coarse current would pull back along the bounded native words by the explicitly implemented differential, with the native tree/heavy-sector terms12002 still required for the enlarged regulator.

The loop stays inside one frame patch and is contractible. Noncontractible loops, topological components, all-volume locality, admissibility bounds, and the candidate Craig refinement series are unimplemented. Its equations51–54 distinguish closed-loop integrability from curvature; its AppendixE warns that finite polynomial truncations need not satisfy the exact identities. **A global native measure is still open.**

## Primary external checks

- [Evans et al., SUSY Nelson–Barr](https://arxiv.org/abs/2002.04204), especially the two-sided soft-insertion problem; [Dine et al.](https://arxiv.org/abs/hep-ph/9303296).
- [Dunkl–Życzkowski, unistochastic matrices](https://arxiv.org/abs/0909.0116), section3: modulus reconstruction and the unitarity triangle are prior art.
- [Martin, Supersymmetry Primer](https://arxiv.org/abs/hep-ph/9709356), section6.5; [Anandakrishnan–Bryant–Raby](https://arxiv.org/abs/1411.7035), equations1–9 and the complete-threshold warning.
- [Vassilevich, heat-kernel manual](https://arxiv.org/abs/hep-th/0306138): continuum heat coefficients do not by themselves prove convergence of this native regulator.
- [Craig, candidate lattice chiral measure](https://arxiv.org/html/2610.09093v1), equations51–54, AppendixE. No independent certification of its long global proof is asserted here.

## Reproduction and scope

The single producer `analysis/w33_pass12021_12025_uv_curvature_threshold_holonomy.py` reconstructs all five certificate sections, including threshold/neutrino local fits. It uses no scratch paths. The focused regression file includes inverse EFT matching, analytic-vs-independent derivatives, an alternate native cell drawing, full auxiliary relaxation and closed-loop controls. Hosted replay and exact-source validation are recorded separately. New results refine named parts of a model; one microscopic action selecting the physical vacuum, constants and gravity is still missing.
