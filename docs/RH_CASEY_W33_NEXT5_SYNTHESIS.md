# Casey / W(3,3) RH Program: Weil, Prime, Operator, Kernel, and Norm-11 Release

## Executive result

All five requested frontiers were executed as a claim-stratified package.
The strongest new exact result is a **local Hasse--Weil realization** of the
nontrivial W(3,3) Ihara determinant at the prime 11. The two graph factors
are precisely the local Frobenius polynomials of two explicit elliptic curves
over `Q` with good reduction at 11. Their Frobenius trace recurrences are
identical to the W33 Hashimoto sector recurrences at every extension degree.

The Casey reflection-cocycle energy also admits an exact Weil/Laplace/Hardy
positive-kernel formulation. On the classical side, however, the naive
positive prime lift diverges at Casey's boundary `sigma=1`; an explicit-formula
regularization with archimedean cancellation is unavoidable. Two increasingly
flexible prime-indexed W33 operator towers were tested and falsified out of
sample. A de Branges audit further shows that generic Hermite--Biehler
positivity is too weak: even an off-line quartet admits an adaptable HB
polynomial.

No classical RH solution is claimed. The release replaces broad analogies
with exact identities, convergence thresholds, and explicit falsifiers.

## Frontier 1: Weil--cocycle positivity

For an orbit

```text
rho      = 1/2 + delta + i gamma,
rho_star = 1/2 - delta + i gamma,
sigma    = 1/2 + a,  a>|delta|,
```

the repaired Casey current has energy

```text
E(a,delta) = integral_R A(a,delta,y)^2 dy
           = pi delta^2/[a(a^2-delta^2)].
```

The new point is the exact Laplace-space identity

```text
E(a,delta)/pi
 = integral_0^infinity
   [exp(-(a-delta)x)-exp(-(a+delta)x)]^2 dx.
```

Equivalently, let

```text
K(c,d)=1/(c+d),
c_-=a-delta,
c_+=a+delta.
```

Then

```text
E/pi = (1,-1) [[K(c_-,c_-),K(c_-,c_+)],
               [K(c_+,c_-),K(c_+,c_+)]] (1,-1)^T.
```

Thus Casey's corrected torque is a genuine positive Hardy-kernel distance.
For a finite orbit family with nonnegative weights, the total energy is zero
exactly when every orbit has `delta=0`. This is an orbit-level positivity
theorem and an RH-equivalent detector after a convergent classical weighting
is supplied. It is not yet an identification with the full Weil explicit
formula.

Certificate:

```text
data/w33_weil_cocycle_positivity_certificate.json
```

## Frontier 2: prime-weight discovery

Sampling the Laplace profile at `x=log n` and inserting the von Mangoldt weight
gives

```text
P(a,delta)
 = sum_{n>=2} Lambda(n)n^(-2a)(n^delta-n^(-delta))^2.
```

In the absolute-convergence region

```text
a-|delta|>1/2,
```

this equals the exact zeta-log-derivative second difference

```text
P(a,delta)
 = L(2(a-delta))-2L(2a)+L(2(a+delta)),
L(s)=-zeta'(s)/zeta(s).
```

Every summand is nonnegative. For small defect,

```text
P(a,delta)/delta^2 -> 4 L''(2a),
```

so the infinitesimal prime weight is a positive log-prime-square moment.

The decisive obstruction is the boundary. Since `a=sigma-1/2`, convergence
requires

```text
sigma > 1 + |delta|.
```

At Casey's `sigma=1`, every nonzero defect is outside the convergence region.
The naive positive prime sum therefore cannot be the missing classical
identity. A Weil explicit-formula regularization must include the gamma and
endpoint terms whose cancellations are absent from the raw positive sum.

A one-damping prime-indexed W33 tower was also fitted. The damping

```text
s = 2.2180060394173368057...
```

matches the scale-free classical quartic moment ratio, but its sextic ratio is
low by

```text
16.4355245%.
```

This rejects the one-exponent model.

Certificate:

```text
data/w33_prime_weight_discovery_certificate.json
```

## Frontier 3: infinite W33 phase operator

A positive prime-power weighted direct-integral model was defined by

```text
trace weight           = Lambda(n)(log n)^2 n^(-s),
local inverse ordinate = log(n)/theta_j,
```

where `theta_j` are the two exact W33 phase angles. Its moments are

```text
M_2k(s)
 = T_2k d^(2k+2)/ds^(2k+2)[-zeta'(s)/zeta(s)],  s>1.
```

This is a genuine positive infinite trace model. A two-channel mixture at
`s=2` and `s=3` has a positive solution

```text
weight(s=2) = 0.06688249400307233...,
weight(s=3) = 0.93311750599692767...,
scale       = 89.53366597571005...,
amplitude   = 4.471175926554505....
```

These three calibration parameters interpolate the classical `S2`, `S4`, and
`S6` moments exactly. The untouched `S8` moment is the falsifier:

```text
relative S8 error = +47.5186499%.
```

Therefore the positive two-damping tower is not the classical xi operator.
The result is useful because it identifies the minimum additional spectral
freedom required and prevents a three-moment fit from being misreported as a
Hilbert--Polya realization.

Certificate:

```text
data/w33_infinite_phase_operator_certificate.json
```

## Frontier 4: de Branges cocycle kernel

The Casey defect is exactly a Hardy/Cauchy reproducing-kernel norm, but generic
de Branges positivity does not force the line.

For every `delta` and `gamma>0`, define

```text
E_delta,gamma(z)=(z+i gamma)^2-delta^2.
```

Its zeros are in the lower half-plane, and for `y>0`,

```text
|E(x+iy)|^2-|E#(x+iy)|^2
 = 8 gamma y(delta^2+gamma^2+x^2+y^2) > 0.
```

Thus `E_delta,gamma` is Hermite--Biehler even when `delta != 0`. Its real and
imaginary parts have interlacing real zeros for every defect. This supplies a
sharp negative result:

> The existence of an orbit-adapted de Branges space is insufficient for RH.

A successful route must produce **one fixed entire Hermite--Biehler function
canonically tied to xi**, not a separately tuned function for each quartet.
The Hardy-kernel distance remains the correct local detector, while the global
fixed-`E` theorem remains open.

Certificate:

```text
data/w33_debranges_cocycle_kernel_certificate.json
```

## Frontier 5: norm-11 local-to-global bridge

This frontier produced the strongest exact new bridge.

Consider the global elliptic curves

```text
E_2  : y^2 = x^3 + x - 1,
E_-4 : y^2 = x^3 + x + 2.
```

Both have good reduction at 11. Direct point enumeration gives

```text
#E_2(F_11)  = 10,  a_11(E_2)  = 11+1-10 = 2,
#E_-4(F_11) = 16,  a_11(E_-4) = 11+1-16 = -4.
```

Their local Frobenius polynomials are exactly

```text
P_11(E_2,u)  = 1-2u+11u^2,
P_11(E_-4,u) = 1+4u+11u^2.
```

Hence the nontrivial W33 determinant has the exact local Hasse--Weil
factorization

```text
Z_W,nt(u)^(-1)
 = P_11(E_2,u)^24 P_11(E_-4,u)^15.
```

The Frobenius discriminants are

```text
2^2-4*11    = -40  -> Q(sqrt(-10)),
(-4)^2-4*11 = -28  -> Q(sqrt(-7)),
```

precisely the quadratic fields of the exact Ihara pole coordinates. Also,

```text
sqrt(-10) mod 11 = +/-1,
sqrt(-7)  mod 11 = +/-2,
```

so 11 splits in both fields, matching the norm-11 denominator prime ideals.

Most importantly, both graph and elliptic sectors obey the same recurrence:

```text
T_0=2,
T_1=a_11,
T_n=a_11 T_(n-1)-11 T_(n-2).
```

On the graph side, `T_n` is the Hashimoto root power sum. On the elliptic side,

```text
#E(F_(11^n)) = 11^n+1-T_n.
```

Thus the W33 nonbacktracking spectral sectors are exactly two elliptic
Frobenius sectors at the local prime 11, at every extension degree. The local
multiplicities remain `24` and `15`.

This does **not** give a global classical-zeta transfer. The next theorem would
have to explain the multiplicities motivically and assemble compatible local
factors at all primes into one automorphic or trace-formula object.

Certificate:

```text
data/w33_norm11_local_global_certificate.json
```

## Validation

The five executable modules generated five immutable PASS certificates.
Focused regression:

```text
python -m py_compile analysis/*.py scripts/*.py
PYTHONPATH=. pytest -q tests/test_rh_next_five_frontiers.py
6 passed in 0.06s
```

## Combined conclusion

The combined Casey/W33 program now has three exact layers:

1. **Orbit geometry:** a positive Hardy/Weil-type cocycle norm detects every
off-line reflected orbit.
2. **Prime obstruction:** its naive von-Mangoldt lift is a positive second
difference of `-zeta'/zeta`, but diverges on the proposed boundary.
3. **Finite arithmetic realization:** the W33 zero-defect graph determinant is
exactly a multiplicity-weighted product of two elliptic local factors at 11.

The most promising route is therefore no longer an arbitrary manifold
compactification. It is an explicit-formula/automorphic program: derive a
regularized global quadratic form whose local `p=11` component is the exact
W33 elliptic packet and whose archimedean component controls the Casey cocycle
energy.
