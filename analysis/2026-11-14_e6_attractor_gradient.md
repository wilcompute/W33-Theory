# The nearest E6 attractor minimum and its exact gradient flow

The [torus proof](2026-11-14_e6_attractor_torus.md) found an explicit route to a global minimum of the charge norm. For the Riemannian negative gradient of that norm on the scalar symmetric space, the same diagonal plane is invariant. It also contains the unique nearest minimum to the scalar origin. These statements concern the scalar potential as a function on the symmetric space. The spacetime radial equations include additional data and are a separate problem. [Real moment map and norm minimization](https://archive.intlpress.com/site/pub/files/_fulltext/journals/mrl/2001/0008/0006/MRL-2001-0008-0006-a008.pdf)

## A fixed subspace of the 42 scalar directions

Use the left quotient K\G with K compact and potential V(Kg)=||gQ||^2. Give the symmetric tangent space at the origin the Frobenius trace metric in the 27 representation. This induces the invariant symmetric-space metric up to a constant. Compact rotation of the charge puts Q on the diagonal three-Pauli triad. There are twelve skew packet generators that kill all three vectors of this triad. Their connected subgroup H fixes the charge. Right multiplication by H acts by isometries, fixing the origin and preserving V.

The exact commutator constraints for H on the 42 symmetric generators have rank 40 modulo 101, so their real rank is at least 40. Two independent real diagonal solutions are supplied by projecting the three coordinate diagonals onto the six-dimensional cubic-preserving diagonal algebra. Their span is therefore the full fixed tangent plane. The exponential at the origin of the simply connected nonpositively curved symmetric space is a diffeomorphism. Its equivariance makes the fixed locus of H exactly the exponential of that plane. Hence the gradient trajectory starting at the origin stays there.

## Flow equation and endpoint

On the three coordinates the compressed Frobenius projector is (I - 11^T/3)/3. If x_i are the squares of the three running charge coefficients, the full negative gradient therefore gives

    dx_i/dt = -(4/3) x_i (x_i - mean(x)).

For nonzero cubic the product of the x_i is constant and positive. Their sum decreases with derivative -(4/3) sum_i (x_i-mean(x))^2. The bounded sum and fixed positive product keep the solution in a compact positive region. Every limit point is balanced, so all three entries converge to |N|^(2/3). Their coefficient signs stay fixed. Thus the endpoint charge has the same top quaternionic line for N>0 and bottom line for N<0 as the constructive torus path. With an empty coefficient, the sum tends to zero by the same Lyapunov argument on the nonnegative orthant. The executable checks the exact projector and fixed-plane rank, then integrates independent examples. Its clock is the symmetric-space gradient time.

## Nearest point among all minima

On any geodesic K exp(tS)g, the potential is ||exp(tS)gQ||^2. The generator S is symmetric, so the potential is a positive sum of real exponentials and is convex. The global minimizer set for N nonzero is consequently a nonempty closed geodesically convex set. Its nearest point to the origin exists and is unique by the metric projection theorem for Hadamard spaces. The H isometries preserve the minimizer set and the origin. The nearest point is therefore H-fixed and must lie in the two-dimensional plane above. The plane maps isomorphically to the sum-zero triad weights, and the three balancing rescalings with product one specify a single point. That point is the nearest scalar minimum. The gradient trajectory need not itself be the geodesic to that endpoint. [Convex analysis on Hadamard manifolds](https://doi.org/10.1287/moor.2025.0939)

## A proof of the parallel majorization observation

[Pass 12667](PASS12667_ATTRACTOR_FLOW_IS_A_PHYSICAL_MIXING_PATH.md) reported that the charge spectrum of a physical state majorizes the balanced endpoint for positive cubic. The stronger statement holds along both paths, in both cubic signs.

For a nonzero cubic, a sign change in two coefficients permutes the four spectral characters. A common negation exchanges the cubic signs and preserves the majorization order, since the eigenvalue sum is fixed. It suffices to study positive magnitudes a>=b>=c>0. They stay ordered by uniqueness and permutation symmetry of the gradient equation. Their three leading eigenvalue sums are a+b+c, 2a, and a+b-c. On the gradient flow the derivatives of the magnitudes are -a*f(a), -b*f(b), -c*f(c), with f(s)=(2/3)(s squared minus the mean of the squares). This f is increasing and f(a)+f(b)+f(c)=0. Therefore a*f(a)+b*f(b)+c*f(c)>=0 by the rearrangement inequality. Also f(a)>=0 and f(c)<=0. These three facts make all three leading sums nonincreasing, including the derivative of a+b-c, which differs from the derivative of a+b+c by 2c*f(c)<=0.

Along the geodesic to the balanced point, each magnitude is its initial value raised to power (1-t) times the geometric mean raised to power t. For t<1 the same derivative proof uses f(s)=log(s/geometric mean)/(1-t), another increasing function with zero sum. Continuity gives the endpoint. Repeating each quaternionic eigenvalue twice and adding the identity preserves the majorization relation. Thus the normalized density spectrum becomes more mixed along either path, and an initially physical charge remains physical. This is a spectral statement about the represented state, with no assertion of one universal linear quantum channel that implements the flow.

Replay with py -3 analysis/toe_20261114_e6_attractor_gradient.py.
