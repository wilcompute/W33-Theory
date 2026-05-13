# Part CDXVI — The Unit Tower and the Six-Kernel

## The Euler Function for Z[ω]/π^k

For any prime power ideal (π^k) in Z[ω] with N(π) = p:

    |(Z[ω]/π^k)*| = N(π)^k - N(π)^{k-1} = p^k - p^{k-1}

With p = N(1-ω) = 3:

    k=1: 3^1 - 3^0 = 3 - 1 = 2    (units of F_3)
    k=2: 3^2 - 3^1 = 9 - 3 = 6    = six-kernel  ✓
    k=3: 3^3 - 3^2 = 27 - 9 = 18  = μ_2(W33)   ✓

## The Six-Kernel Has Two Derivations

**Geometric derivation:** |Z[ω]*| = |{±1, ±ω, ±ω²}| = 6

**Ring-theoretic derivation:** |(Z[ω]/π^2)*| = N(π)^2 - N(π) = 9-3 = 6

These are independent but consistent: both give 6 = six-kernel.

## The Unit Tower

    |(Z[ω]/π^1)*| =  2  (F_3 units)
    |(Z[ω]/π^2)*| =  6  = |Z[ω]*| = six-kernel
    |(Z[ω]/π^3)*| = 18  = μ_2(W33 Laplacian)

The k=2 unit group is the six-kernel. The k=3 unit group is the
W33 second Laplacian eigenvalue. The tower encodes the Laplacian
spectrum directly.

## Connection to W33 Laplacian Gaps

    μ_1 = 12 = 2 × 6 = 2 × |(Z[ω]/π^2)*|   (confinement gap)
    μ_2 = 18 = |(Z[ω]/π^3)*|               (sector gap)

The confinement gap μ_1 is twice the k=2 unit count.
The sector boundary μ_2 is the k=3 unit count.
