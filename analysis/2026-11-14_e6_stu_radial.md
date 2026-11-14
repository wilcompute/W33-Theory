# Physical STU radial path in the E6 charge coordinates

The [nearest-minimum proof](2026-11-14_e6_attractor_gradient.md) concerns the five-dimensional scalar potential on its symmetric space. The ungauged electric STU solution gives an independent spacetime trajectory with the same horizon moduli. The comparison below uses positive charges in the static supersymmetric branch, the scalar origin at spatial infinity, and the three-charge normalization of the repo. [Sabra, General BPS Black Holes in Five Dimensions](https://arxiv.org/abs/hep-th/9708103)

Set tau = 1/r^2, H_i = 1 + q_i tau, and W = (H_1 H_2 H_3)^(1/3). The STU solution has spatial warp W, time warp W^(-2), scalar factors X_i = W/H_i and product X_1 X_2 X_3 = 1. The dressed Pauli coefficients are d_i = q_i X_i. Thus each tends to (q_1 q_2 q_3)^(1/3) at the horizon, which is exactly the unique balancing rescaling found in the nearest-minimum proof.

## Three paths with one endpoint

Write ell_i = log X_i and y_i = q_i/H_i. Then ell' equals mean(y)-y and ell'' equals y squared minus mean(y squared). The determinant with columns (1,ell',ell'') is minus the Vandermonde product of the y_i. The verifier factors it exactly. For distinct charges this is nonzero at every finite tau because q -> q/(1+q tau) is strictly increasing. The path in the flat logarithmic scalar plane is therefore curved. With a repeated charge the trajectory stays on a line and its image is the segment to the minimum. Three equal charges give a constant trajectory.

The potential-gradient direction in this plane is proportional to mean(d squared)-d squared. Because d=W y, this is proportional to mean(y squared)-y squared. The determinant of the two directions with the constant vector is the same Vandermonde up to orientation and a nonzero scalar factor. The radial trajectory therefore also differs from the scalar-potential gradient trajectory for distinct charges, even allowing a reparametrization.

Along the actual radial path, d_i' = -d_i (d_i-mean(d))/W. This gives spectral majorization directly. Order the positive dressed charges a>=b>=c. Their three leading quaternionic eigenvalue sums are a+b+c, 2a, and a+b-c. The scalar function f(s)=(s-mean(d))/W is increasing and its three values sum to zero. The same partial-sum argument as in the scalar-gradient proof applies. The charge cubic stays fixed and the density spectral body is forward invariant for an initially physical charge in this branch.

## Singular charge limits

With one or two nonzero positive charges, write k for their number. As tau grows, W grows as tau^(k/3). The occupied scalar factors have exponent k/3-1, and the empty ones k/3. With the repo trace metric, distance squared from the origin is k(3-k) log(tau)^2 + O(log(tau)). The sphere area scales as tau^((k-3)/2) and the dressed potential as tau^(2(k-3)/3), so both go to zero. The classical finite-area attractor applies to three occupied charges. These singular asymptotics concern the two-derivative solution and leave higher-derivative resolution undetermined.

Replay with py -3 analysis/toe_20261114_e6_stu_radial.py.
