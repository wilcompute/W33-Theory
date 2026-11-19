# A harmonic tilt removes the unwanted mirror critical pair

18 November 2026. Explicit local PW BPS deformation and spectral checks. Three chiral profiles remain, while the unwanted semiclassical mirror pair disappears. This is not a global G2 construction or a derivation of the observed generation number.

## Follow the failure rather than preserve the symmetric ansatz

**d7280e023** proved three charged L2 profiles for a harmonic quartic. The subsequent **6ef448a5d**, `analysis/2026-11-18_PW_instanton_mirror_lift.md`, found an exponentially light extra vectorlike pair at strong localization. Merely counting exact zero modes missed this low-energy issue.

An allowed harmonic deformation addresses that specific problem. Set

    f_a=Re(w^4)/4-|w|^2/2+z^2-a*x, w=x+iy.

The linear term leaves Delta f_a=0. Therefore A=0, phi=H df_a still solve the same commuting PW equations. The deformation changes the supplied background/boundary data; it is not shown to be selected by an action or compatible with an earlier global quotient.

## Exactly three critical points for a=1

The critical equations reduce to

    z=0, y*(y^2-3x^2-1)=0,
    y=0: x^3-x-a=0,
    y!=0: 8x^3+4x+a=0, y=plus/minus sqrt(3x^2+1).

The off-axis cubic is strictly increasing and has one real root, supplying two critical points. The axis cubic has discriminant4-27a^2. For 0<a<2/(3sqrt(3)) there are three axis roots and five total critical points. At a=2/(3sqrt(3)), one index-one point meets the index-two point at x=-1/sqrt(3). Beyond this generic fold only one axis root remains: three total critical points, all index one.

At a=1 the points are approximately

    (1.3247179572,0,0),
    (-0.2266988258, plus/minus1.0743263344,0).

Their Hessian eigenvalues are respectively (-6.264633,2,4.264633) and (-4.616708,2,2.616708). Exact Sturm counts and symbolic reductions in the producer establish the count; numerical root positions do not substitute for completeness. The first coordinate is the standard real root of x^3-x-1. That familiar algebraic constant is not a physical parameter prediction.

This is a perfect local Morse configuration: three degree-one critical states, with no degree-two critical state available for an exponentially weak pairing. The old four-trajectory mass matrix is not transplanted to the deformed background.

## Robustness and the caustic

More generally add -A*x-B*y and write alpha=A+iB. The planar gradient equation is

    conjugate(w)^3-w=alpha.

Its real Jacobian determinant is 1-9|w|^4, so the only critical circle is |w|=1/sqrt(3). Its image is the caustic

    alpha(theta)=exp(-3i theta)/(3sqrt(3))-exp(i theta)/sqrt(3).

After rotating the parameter and target, this is the standard four-cusped astroid:

    alpha(phi+pi/4)=-exp(i*pi/4)*4/(3sqrt(3))
                    *(cos(phi)^3+i*sin(phi)^3).

The connection between harmonic-map zeros, Jacobian critical curves and caustics is established mathematics; see [Khavinson, Lee and Saez, Zeros of harmonic polynomials, critical lemniscates, and caustics](https://link.springer.com/article/10.1186/s40627-018-0012-2). Here the curve is derived directly for the PW gradient rather than proposed as a new caustic theorem.

A simple direction-independent sufficient condition is |alpha|>4/(3sqrt(3)). On the closed critical disk, |conjugate(w)^3-w| cannot exceed that value. Hence no solution lies on or inside the disk. Every solution has one negative and one positive planar Hessian eigenvalue, with positive z eigenvalue. The proper gradient has degree -3, so there are exactly three solutions. Thus the result holds on an open parameter region and allows generic tilts that also break the residual reflection. It does not require the exact real value a=1.

## The three exact L2 zero modes survive the fold

The linear term does not change the infinity argument used in d7280e023. The planar gradient remains proper, with lower bound r^3-r-|alpha| outside a disk and winding -3. Both exp(+q f2) and exp(-q f2) remain nonnormalizable in different angular sectors. Thus the planar even kernel vanishes and the index forces exactly three degree-one modes. The z Gaussian gives

    dim H^k_L2(d+q df_a wedge)=(0,3,0,0), q>0.

This holds on either side of the classical fold, including the degenerate value by the proper-gradient index and even-kernel argument. The kernel does not jump when the critical pair annihilates. What changes is the low positive spectrum and the validity of the five-state semiclassical description. The operator and physical form/chirality dictionary remain those of [Braun et al., sections2.3 and5](https://arxiv.org/html/1812.06072v2).

## Numerical removal of the light pair

The tilted planar top-form Hamiltonian is constructed from the true rectangular exterior map, H2=B^T B. The q parameter is the localization amplitude, with the native E6 charge held fixed.

|q|Untiltted H2 lowest|Tilt a=1 H2 lowest|Tilted H2/q|
|---|---:|---:|---:|
|4|0.5136341|8.8779832|2.21950|
|12|0.02612388|56.0909174|4.67424|
|24|0.0001314785|119.7679816|4.99033|

The scan covers six tilts at each amplitude, including values just below and above the fold. Two alternative-width controls and an N=144 check agree. At q=24 the high-resolution full L2 operator residual is about2.47e-9. As in 6ef448a5d, this captures the entire polynomial operator action, not merely the projected eigensolver residual. These floating-point checks are not interval-certified lower eigenvalue bounds.

The local harmonic-oscillator approximation now gives a positive leading top-form gap coefficient

    min_j 2*(3|w_j|^2-1)=5.23341658...

in lambda_H2/q. This explains the numerical growth, contrasting with the untilted exponentially small value. Standard Witten semiclassical localization supplies the oscillator mechanism; no new universality law is asserted. In the full product problem, the z excitation has value4q and H0=H2+4q. The computed first positive value at a=1,q=24 is therefore consistent with4q=96, rather than the small mirror-pair scale. Its global compactification interpretation remains absent.

## What improves and what does not

The explicit symmetric model's unwanted light mirror pair is avoidable within the same local harmonic PW class. A linear harmonic tilt annihilates the extra critical pair while preserving exactly three charged L2 profiles. This is stronger than merely assigning the pair a nonzero but exponentially small mass.

The tilt breaks C4. The earlier C4 character projection cannot be reused, and a global symmetry/bundle construction must permit the deformation. The quartic degree still supplies the index three; no W33 or dynamical selection of that degree or tilt is derived. The noncompact background still has infinite ordinary kinetic energy and no normalizable constant gauge profiles. The E6 extra-U1 anomalies, rank breaking and zero bare two-family adjoint cubic are unchanged. Compact G2/source gluing, physical gauge and Higgs fields, anomaly inflow and observed Yukawas remain open.

Run `python analysis/toe_20261118_PW_tilt_perfect_Morse.py`. Publication scope is this report, its producer and its JSON. The mirror-lift packet is preserved as the tested reason for changing the background rather than silently discarded.
