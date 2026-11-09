# Native magnetic homogenization: an obstruction and a positive invariant completion

The all-short-face action can preserve H27 symmetry and still fail to propagate three transverse gauge polarizations. The October 27 audit already found a rank-106 short-face curl and two physical flat modes at its generic sample, with an exact modular lower bound. This packet computes the effective magnetic tensor behind that obstruction, then constructs a positive finite-loop action which preserves the controller symmetry and matches the scalar acoustic cone at leading order. The matching couplings are supplied; no unique action, physical time or TOE is selected.

## Prior ownership and intake

Baseline is `75f5dc379db52d88a962f25443e5a8c2c9119044`; its [full-edge Gauss report](2026-11-08_native_gauss_and_magnetic_symmetry.md) compares magnetic Hessians at zero external momentum. The [October 27 propagation report](2026-10-27_native_gauge_propagation_completion.md) owns the integral rank, short-face flat-mode obstruction, literal six commutators and engineered metric matching. Pass 11991 owns the primitive four-period cover, integer deck controllers, harmonic cochains and scalar metric. This packet uses those objects rather than asserting a new general Schur, group-averaging or nonbirefringence theorem.

Result-specific searches included exact fraction `29857/5775`, all1287/Schur, short-face area tensor and controller-averaged commutator patterns across analysis Python/Markdown and bounded data JSON, plus the result index and selected prior propagation sources. An initial broad integer search returned too much output; the fraction and file-list searches were then used. No absence-of-hit priority theorem is claimed. No new incoming commit was observed at intake; the publication manifest records final integration state. Earlier weekly and concurrent batches remain incompletely read.

The unchanged 215-page manuscript was read further through full extracted pages 121–126: Wilson-line hierarchy versus symmetric degeneracy, cross-sector/Higgs limitations, entangling and flux routes, corrected dual-flux tilt, flavour qutrit magic, Hesse F-flat locking and a supplied soft-supertrace hierarchy. Cumulative personal text coverage is pages 1–126, with no new visual inspection or independent rerun of those flavour/flux claims. A route mentioned in the manuscript is not a constructed physical vacuum here.

External context: [G. F. Rubilar, *Linear pre-metric electrodynamics and deduction of the light cone*](https://arxiv.org/html/0706.2193v1), abstract, selected introduction and sections 4.1/4.3.2. That work relates constitutive symmetry and closure to a conformal Lorentzian metric in four spacetime dimensions. Our six-component area tensor concerns **four spatial** deck directions and an external Hamiltonian time. Its dimension is not grounds for importing the four-spacetime-dimensional closure theorem or claiming Lorentzian signature. The useful connection is methodological: a propagation cone constrains constitutive couplings beyond discrete symmetry.

## Exact optical elimination of all 1,287 short faces

Write h for the native harmonic edge cochains, M=h.T h, and F(k) for the literal running-position Bloch curl. At k=0 the optical rowspace has rank 105. Expand an acoustic field as A=h x+i t C y at k=t n, where C spans that optical edge space. The order-t flux is

```
i t [F1(n) h x + F0 C y].
```

Minimizing over y projects F1 h onto the orthogonal complement of im(F0 C). The projected coefficient is antisymmetric in n,x, so it acts on the six components n wedge x in pair order (01,02,03,12,13,23).

The resulting exact tensor is

```
chi_short = diag(29857/5775, 0, 0, 0, 0, 0).
```

This is more than a numerical rank observation. Raw derivatives have common denominator 9. Numerical rational candidates for the 105 optical coefficients are accepted only after exact rational verification of the full normal equations A.T(raw-A X)=0 and all antisymmetry identities. Thus X gives the unique least-squares projection and the displayed rational Gram tensor. The common denominator of the accepted optical solution is 935550. Tests also compute the finite-k complex optical minimization independently and compare its limit to this tensor.

Consequently the leading short-face symbol is a single outer product, proportional to (-n1,n0,0,0)(-n1,n0,0,0). It has rank one when (n0,n1) is nonzero and vanishes on the n0=n1=0 plane. This reproduces the pattern of the earlier sampled flat modes in the leading symbol. It does not prove an all-orders generic rank-106 upper bound.

## Why positive reweighting cannot repair the short faces

The integer voltages define a period map from the finite short-face complex X to the four-torus: an edge traces its voltage vector, and each zero-voltage boundary fills with its lifted polygon in the cover. On degree two, the pullbacks of the six coordinate torus area classes are represented by the signed polygon areas. The torus cohomology ring used here is standard; see [Hatcher, §3.2, Example 3.16](https://pi.math.cornell.edu/~hatcher/AT/ATch3.pdf#page=32). The earlier TOE59/60 work discusses topology and cup-product limitations on a different three-period complex, so its missing higher cells are not a numerical input for this degree-two calculation.

Independently of the harmonic derivative, compute the integer twice-area columns by summing p_i d_j-p_j d_i over lifted edges with running position p and signed step d. Their difference from twice the projected derivative is exactly A Y for a checked rational Y, where A=F0 C spans the optical coboundaries. Thus the image of the torus degree-two pullback has rank one in the 1,182-dimensional H²(X;R). Since the four degree-one classes span H¹(X;R), this is also the image of their cup products.

A positive definite face metric changes the inner product used to pick a representative of each quotient class. It cannot change the rank of the map into the quotient by im(F0). Therefore **no positive definite reweighting or mixing of these same short faces can give three leading magnetic polarizations**. This conclusion is stronger than a failure of unit weights. As a numerical control, length weights (1.3,0.7,2.1) change the sole area coefficient to about 10.61188215, while all other components stay below 4.6e-16. New loop support is needed within this magnetic construction.

## A positivity obstruction at the original unit weights

The desired scalar-matched area tensor, with the prior unit electric edge metric, is

```
T = C2(M)/27,
W(n).T T W(n) = [(n.T M n) M - (M n)(M n).T]/27.
```

C2 denotes the second compound matrix. The only nonzero generalized eigenvalue of (chi_short,T) is exactly 29857/5775. For a nonnegative short-face weight alpha, T-alpha chi_short is positive semidefinite precisely for

```
0 <= alpha <= 5775/29857 = 0.193421978095589...
```

The upper endpoint gives a singular complement; strict inequality gives a positive definite one. This is also a physical plane-wave obstruction, not just negativity on an unphysical two-form: n=M^-1 e0 and x=M^-1 e1 generate a decomposable area whose short/target energy ratio is 29857/5775. The exact vectors and area are stored in the result. At unit short-face weights, that polarization already exceeds the target energy. Adding positive loop-flux energy cannot lower it to the specified scalar cone. This statement holds for fixed electric metric and added commutator blocks that vanish at k=0; it does not rule out changing the electric action, the target speed, the face weights, or more general optical couplings.

## A positive finite-loop construction

Choose the explicit weight alpha=1/16 for every short face. Let S be the exact unimodular first-area matrix of the six prior 16-step commutators, and set

```
H = S^-T [T-alpha chi_short] S^-1.
```

All six leading principal minors of H are positive exactly. Map the six commutators through every left-H27 controller, producing 27 blocks of six literal closed zero-integer-voltage walks. Couple the six fluxes inside each block by H/27, then sum all blocks. This is local in the periodic finite-loop sense; it uses cross-couplings between six fluxes, not independent diagonal weights alone. No nonlocal harmonic projector is inserted into the action.

Every mapped first-area matrix Sg obeys Sg.T H Sg=T-alpha chi_short exactly. The total leading tensor is therefore T. The short-face optical gap remains positive, and the extra commutator rows vanish at k=0, so optical corrections cannot change their leading acoustic contribution. The resulting three transverse squared speeds equal n.T M n/27 at leading long wavelength.

The group averaging restores covariance after choosing loops based at one vertex; the microscopic action still depends on the supplied loop paths. Exact integral vertex offsets are constructed for all 27 deck controllers, satisfying the voltage coboundary equations. They determine explicit finite-momentum unitary edge and vertex transformations. Five controller samples at k=(0.17,-0.23,0.31,0.11) give magnetic covariance residuals below 1.4e-15 and gradient covariance residuals below 3e-16 in the prototype. Literal mapped-path closure, exact leading invariance and integer lift checks cover all 27 controllers; the finite-k numerical matrix checks are sampled.

## Numerical evidence and limits

On three rays with t=0.02,0.01,0.005, the three low squared frequencies divided by t² approach the scalar target. For n=(1,2,-1,1), the target is 94/27=3.48148148; the smallest-t values are approximately 3.48126830, 3.48139830 and 3.48157949. The optical modes remain separated. At generic momentum the completion removes the short-only flat modes. The finite-k polarizations still split: matching the leading cone is not an exact full-band dispersion identity.

Actual server-side V8 independently checks the native six-area Cholesky positivity, the rank-one compensation threshold and transverse quadratic identity. This is not a separate native 135-edge Bloch replay. The final frozen validation regenerates the native producer and runs 14 new cases plus four prior propagation cases; its receipt records actual results and unchanged source/input hashes. No hosted CI or interval-certified floating-point claim is made. Repository-wide guard limits remain explicit in the manifest.

This establishes compatibility of positive finite-loop couplings, controller covariance and a prescribed leading cone, together with a precise obstruction for the original unit short-face weights. It does not derive those couplings dynamically. The model is a bare noncompact harmonic U(1) action with four spatial directions and supplied external time. Inhomogeneous scalar-loop response, gauge interactions, physical 3+1 selection, charged chiral matter, radius stabilization, units and observational predictions remain open. The TOE goal remains active.
