# A superconformal fixed-point obstruction for the canonical W33 cubic sector

With the canonical W33 chiral inventory, the one-loop coefficients for the (E_6) and family gauge couplings are −21 and −66 in the convention `β(g)=−b0 g³/(16π²)+…`. Both couplings grow toward the ultraviolet near the free theory. An interacting four-dimensional unitary N=1 fixed point with both gauge couplings, the signed cubic, and the rank-two mixed adjoint coupling also faces an exact obstruction. The trial central charge has no local maximum, even after the usual correction for chiral operators becoming free at the unitarity bound. The calculation assumes the stated elementary fields and allows accidental symmetries from free generators of their polynomial chiral ring. An emergent interacting sector with its own accidental currents or a different superpotential support would require a different calculation. [Canonical matter and couplings](2026-11-09_canonical_sm_flatness.md) · [Asymptotic safety in supersymmetric theories](https://arxiv.org/abs/1508.07411)

## The exact two-variable problem

The basic Dirac indices divided by two give Dynkin indices `(9,27/2)` for each of the five bifundamental fields, `(12,0)` for the adjoint A and `(0,15/2)` for the spectator S. The gauge adjoints have indices 12 and 3. Let `r=R(A)` and let `Σ` sum the five bifundamental R charges. Vanishing mixed R-gauge anomalies give `3Σ+4r=15` and `9Σ+5R(S)=48`. At the fixed point under test, retain the signed alternating cubic and the two singular directions of the mixed adjoint coupling. In their species basis the superpotential requires `R(X2)+R(X+)+R(X−)=2`, `R(Z0)+R(X2)+r=2` and `R(Z1)+R(X+)+r=2`. The rank-two coupling admits a basis with these pairings, and the alternating cubic transforms by the determinant of the X basis change. Its normalization has no effect on the charge equations. [Index ledger](2026-11-12_parent_theta_lattice.md) · [Canonical singular directions](2026-11-12_theta_rephasing.md)

Set `x=1/2−r/3` and `z=3/2−2r/3`. The full trial charges in this basis are

```text
X2   X+   X−        Z0   Z1   A   S
x+t  x−t  1+2r/3    z−t  z+t  r   (3+12r)/5
```

The anomaly expression `a=(3/32)(3 Tr R_f³−Tr R_f)` uses R charges of Weyl fermions and multiplicities `(81,81,81,81,81,78,10)` plus 86 gauginos. On `t=0` its derivative in the r direction is `9(27936r²−22212r+6301)/1600`, positive on the whole real line. The full t derivative is `−2187rt/8`. At r=0 and t≠0 the Hessian has a nonzero off-diagonal entry and zero tt entry, so such points cannot be local maxima. [Intriligator and Wecht’s a-maximization theorem](https://arxiv.org/abs/hep-th/0304128)

## Free chiral generators cannot supply the missing maximum

For a generator of trial charge q below 2/3, replace its trial contribution by that of a free chiral multiplet. The correction `a_ch(2/3)−a_ch(q)` is convex as a function of q on the active interval and extends convexly by zero above the bound. Consequently the Hessian of the uncorrected trial function must be negative semidefinite at a corrected local maximum. Its two diagonal entries and determinant imply

```text
0 ≤ r ≤ L = 617/1552
t² ≤ (776/675) r (L−r).
```

The replay proves `|t|<11/50`, both Z charges greater than one, and all X charges greater than 1/5 throughout this ellipse. The faithful gauge center requires the number of X fields minus the number of Z fields in a singlet to be divisible by three. A monomial containing Z is already above the bound. With only X fields among the bifundamentals, six or more X fields exceed the bound. Three X fields alone can form only the alternating species cubic, which has charge two. Adding A to a three-X invariant gives at least `3/2−3|t|>2/3`. Adding S to a three-X invariant gives more than 2/3 as well. A single S without X or Z carries family charge and cannot form an invariant with adjoints alone. Two or more S fields exceed the bound. These arguments apply to polynomial representatives before imposing the F-term relations, which can only remove classes from this list. [Signed cubic uniqueness](2026-11-08_exact_signed_cubic_and_three_copy_vacuum.md)

The only possible free generators in the ellipse are therefore among the six primitive adjoint invariants of degrees 2, 5, 6, 8, 9 and 12. Products of free generators have their induced R charge. Their corrections are independent of t, so a local maximum must have t=0, including at the r=0 endpoint by the Hessian condition. For fixed r the largest subtraction from the positive r derivative occurs when every primitive with `dr<2/3` contributes. The derivative is quadratic between consecutive crossings. Checking each interval's endpoints and any interior stationary point gives a minimum of `6309/1600>0` across the entire allowed interval. The obstruction survives if some primitives are absent from the quantum chiral ring. [Free-field correction](https://arxiv.org/abs/hep-th/0308071) · [Adjoint invariant degrees](https://jolt.centre-mersenne.org/item/10.5802/jolt.1068.pdf)

## Turning off the alternating cubic

Keep both gauge couplings and the rank-two mixed adjoint term and set the alternating cubic to zero. This releases the two paired charge splittings independently. Each pair has mean `1−r/2`, with splittings u and v, while X− and S retain the charges shown above by the gauge equations. The trial central charge is its value on `u=v=0` minus `2187r(u²+v²)/32`. The same convexity argument restricts a candidate maximum to `0≤r≤1684/3329` and `u²+v²≤(3329/1350)r(1684/3329−r)`. All four paired charges exceed 2/5 there. A gauge invariant with matter outside the adjoint requires at least two such non-adjoint factors, each of charge greater than 2/5. Again only the primitive adjoint generators can contribute corrections. The splitting derivatives force `u=v=0` and the exact minimum corrected r derivative on this interval is `705465/26632>0`. Thus this enlarged trial space also has no local maximum.

## Checks when retaining spectator interactions

At the canonical coefficient ratios in the canonical kinetic chart, the nonzero S² mass sextic ties X+ to X− via the (M00^2) contraction and ties X2 to X+ via (M00 M02). These statements follow from the separate nonzero multidegrees in the two contractions. The gauge and cubic constraints then give `r=−1/2` and `t=0`. The sextic has charge `2R(S)+2(2−r)=19/5`, which is inconsistent with the required charge two. This check uses neither a-maximization nor the free-generator correction.

For the separate spectator-odd quartic, the (X0^3) tensor contains the (X+^3) and (X-^3) components because both projections of X0 are nonzero. Keeping the quartic at a fixed point imposes equal charges for X+ and X− and `R(S)+3R(X+)=2`. The gauge and cubic constraints then force `r=−4/11`. The quadratic adjoint invariant has a trial charge below the unitarity bound at that value. This is a necessary accidentals test for the quartic branch. The quartic breaks the flavor rotation used in the reduced theory, so the two-variable no-maximum proof applies only to the reduced cubic sector. [Spectator interactions and vacuum-preserving quartic](2026-11-12_theta_rephasing.md)

The next ultraviolet question is whether a fixed point with a rank-zero or rank-one mixed term, one vanishing gauge coupling, or additional interactions can generate the canonical action through its relevant deformations. Supersymmetric product-group examples with controlled UV fixed points provide a comparison class. [Bond and Litim’s product-group examples](https://arxiv.org/abs/1709.06953)

Run `python analysis/toe_20261112_canonical_uv_fixed_point.py` from the repository root. [Exact replay data](../data/toe_20261112_canonical_uv_fixed_point.json)
