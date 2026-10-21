# 2026-10-21 — W33 Levi Ihara factors are two explicit local Hasse–Weil curve factors

**Status: exact local arithmetic theorem; NOT a proof of the classical Riemann Hypothesis.**
**Verifier:** `analysis/w33_20261021_levi_genus2_frobenius.py` (stdlib, reconstructs geometry and counts F3/F9/F27/F81 points).

## Cross-track discovery

The existing repo file `analysis/2026-10-14_toe76_six_fronts_rh_ihara.md` derives the 80-vertex point-line Levi graph Ihara determinant. A different track, `docs/RH_CASEY_W33_NEXT5_SYNTHESIS.md`, matches the *40-vertex* W33 nontrivial Ihara factors to elliptic Frobenius polynomials at prime **11**. Combining these two ideas suggests seeking actual varieties over F3 for the Levi graph's quartic and quadratic factors.

Two explicit smooth curves give the exact answer:

- Genus two: `C/F3: y^2=x^5+1`, with Frobenius numerator `P_C(u)=1+9u^4`.
- Genus one: `E/F3: y^2=x^3-x`, with Frobenius numerator `P_E(u)=1+3u^2`.

Then the **nontrivial** inverse Ihara factor equals

```
D_Levi,nt(u) = P_C(u)^24 P_E(u)^30.
```

The cohomological degree is `24*4+30*2=156`. Unlike a dimension coincidence, both factors are actual Hasse–Weil Frobenius polynomials of explicitly given smooth projective curves over **the same field**.

## Mathematical proof: curves

For the smooth genus-two curve `y^2=x^5+1`, the polynomial is squarefree in characteristic 3 since its derivative is `2x^4` and its value at 0 is 1. The curve has one point at infinity. For `n=1,2,3`, `gcd(5,3^n-1)=1`, so `x -> x^5` permutes the field `F_(3^n)`. Hence

```
#C(F_(3^n)) = 3^n + 1 + sum_x chi(x^5+1)
            = 3^n + 1 + sum_z chi(z+1)
            = 3^n + 1.
```

Thus `#C(F3)=4`, `#C(F9)=10`, `#C(F27)=28`. The first two Frobenius power sums are `t1=t2=0`. The genus-two functional equation gives

```
P_C(u) = 1-t1*u + (t1^2-t2)*u^2/2 - 3*t1*u^3 + 9*u^4
       = 1+9*u^4.
```

It predicts `#C(F81)=118`, independently counted in the verifier.

For `E: y^2=x^3-x`, all three x-values in F3 give y=0, plus infinity; thus `#E(F3)=4` and `a3=3+1-4=0`. The elliptic Frobenius polynomial is `1+3u^2`; higher extension counts are `16,28,64` for F9,F27,F81.

## Mathematical proof: W33 Levi spectrum

W33 has 40 symplectic projective points and 40 isotropic lines. Its 40-by-40 incidence matrix N satisfies `N N^T=A+4I`, with collinearity adjacency spectrum `12^1, 2^24, (-4)^15`.

Therefore the 80-by-80 bipartite Levi adjacency spectrum is `(+4)^1, (-4)^1, (+sqrt(6))^24, (-sqrt(6))^24, 0^30`.

The Levi graph is 4-regular with 160 edges, hence Ihara–Bass gives

```
Z_Levi(u)^-1
  = (1-u^2)^80 det(I - u*A_Levi + 3*u^2*I)
  = (1-u^2)^81 (1-9*u^2) (1+9*u^4)^24 (1+3*u^2)^30.
```

This proves the stated local curve-factor identity.

## Implications and boundaries

1. Both nontrivial curve factors obey the finite-field Weil-RH bound and have reciprocal zeros on `|u|=3^-1/2`. This identifies the graph-RH circle with the Frobenius circles of concrete genus-one and genus-two objects.
2. It complements, but is distinct from, the prime-11 elliptic realization of the 40-vertex W33 graph in the Casey packet. The new Levi packet has *local* rank 156, versus local rank 78 for the W33 collinearity packet.
3. The formal local cohomology carrier is `H^1(C)^24 direct_sum H^1(E)^30` over F3; an equivariant, canonical graph-to-motive map has not been constructed.
4. This does **not** give classical RH. A single local factor at p=3 does not identify Euler factors at other primes, a completed global L-function, or the Riemann Xi function. A finite graph zeta is periodic after `u=3^-s`, unlike classical zeta.
5. New literature audit: `analysis/PASS4447_ZETA_AND_SIGNING_ARE_ONE_SUBJECT.md` correctly interprets signings as Artin–Ihara characters, but the unrestricted Bilu–Linial conjecture is now reported false by Zhiqiang Xu (September 2026, https://arxiv.org/abs/2609.15591); the Ramanujan-base restriction is still open. This does not invalidate W33-specific signing witnesses.

## Follow-on falsifiers

- Search for an **intrinsic** representation intertwiner, not just equality of Frobenius characteristic polynomials.
- Test whether the p=3 and p=11 local packets fit one meaningful all-prime arithmetic correspondence; a raw degree-156 versus degree-78 mismatch is an obstruction to naive identification.
- Compare W33 twisted Artin–Ihara factors under Z2/U(1) signings with actual local sheaf/Frobenius factors, keeping local versus global scopes separate.
- In RH arguments require a full explicit-formula/Weil positivity identity, including archimedean terms; finite graph-RH is not sufficient.

**Priority note:** New exact connection discovered in a cross-track search, not a claim of independent first discovery in the mathematics literature.
