# Pass 10948 — clock-tetracode negacyclic / reciprocal-factor hyperbolic bridge

Pass 10946 proved that the frozen tetracode is exactly the evaluation code of linear clock functions on the four oriented rays of P1(F3). This pass puts that exact code into a polynomial clock gauge and welds it to a cyclotomic mechanism that already existed elsewhere in the repo but had never been connected to the clock code.

## Exact theorem

Let

```text
C = {(a,b,a+b,b-a) : a,b in F3}.
```

In its frozen Pass 10946 orientation, C is **not** invariant under the standard negacyclic shift

```text
N(c0,c1,c2,c3)=(-c3,c0,c1,c2).
```

But there are two one-ray orientation flips:
- flip coordinate 2: `diag(1,-1,1,1)`;
- flip coordinate 4: `diag(1,1,1,-1)`.

They give exactly the two principal ideals

```text
C+ = (x^2+x-1),
C- = (x^2-x-1)
```

inside

```text
R = F3[x]/(x^4+1),
x^4+1 = (x^2+x-1)(x^2-x-1).
```

The factors are irreducible and reciprocal over F3. On either sector the negacyclic shift obeys

```text
N^4=-I,   N^8=I,
```

and has exact order 8.
## Hyperbolic-pair closure

Both C+ and C- are [4,2,3]_3 tetracodes. Each is totally isotropic for the standard F3 dot product, hence self-dual. They are transverse:

```text
C+ ∩ C- = {0},
dim(C+ + C-) = 4.
```

In polynomial bases `(g+,Ng+)` and `(g-,Ng-)`, their cross-pairing matrix is

```text
[[1,1],
 [2,1]]
```

with determinant 2 mod 3, so the cross-pairing is nondegenerate. Cyclotomic inversion `p(x) -> p(x^-1)`, with `x^-1=-x^3`, exchanges C+ and C-.

This is the exact rank-one version of the reciprocal-prime split already verified in Pass 9961–9984: there, the same factorization of Phi_8 mod 3 produces two conjugate F9 spaces with zero restricted form and nondegenerate cross-pairing. The new result is that the four-ray clock tetracode is built from the same mechanism.
## Signed-permutation census

The full signed coordinate group has order

```text
4! * 2^4 = 384.
```

The tetracode has monomial stabilizer order 48, so its orbit contains exactly eight distinct code images. Exhaustive enumeration gives:

```text
8 distinct signed-permutation images,
2 distinct negacyclic images,
48 gauges per image,
96 signed gauges yielding a negacyclic presentation.
```

So negacyclicity is neither automatic nor arbitrary. It selects exactly one quarter of the signed coordinate gauges and exactly two of the eight code images.

## E8 and literature cross-check
The existing repo E8 glue certificate already proves `240 = 4*6 + 8*27` from the standard tetracode. Pass 10948 adds the missing polynomial/cyclotomic presentation.

An external 2018 construction by Watanabe, Belfiore, de Carvalho and Vieira Filho (International Journal of Applied Mathematics 31(1), DOI 10.12732/ijam.v31i1.6) explicitly identifies the tetracode as the negacyclic ideal `(x^2+x-1)` in `F3[x]/(x^4+1)` and uses it in a cyclotomic E8 construction. Its displayed generator rows agree with the C+ basis here up to an irrelevant row sign.

A very recent paper by Ian Teixeira, arXiv:2609.27148 (submitted 2026-09-22), develops A2-frame lattice constructions with one-generator negacyclic glue and recovers Coxeter–Todd through an index-8 overlattice in the l=3 case. That paper is **not** being identified with this clock tetracode theorem. It is a strong next-direction signal because the repo already contains the Coxeter–Todd/hexacode rung, while searches found no existing repo bridge from the clock tetracode to negacyclic glue.

## Boundary

This is finite coding theory and cyclotomic algebra. The order-8 shift is a reversible algebraic clock on the code. It is not a thermodynamic arrow, a Page–Wootters clock by itself, or evidence that the optical register is literally entangled with a physical future. Those physical identifications require the separate process/open-system layer.

Producer: `analysis/w33_pass10948_clock_tetracode_negacyclic_hyperbolic_bridge.py`

Certificate: `data/w33_pass10948_clock_tetracode_negacyclic_hyperbolic_bridge.json`

Regression: `tests/test_w33_pass10948_clock_tetracode_negacyclic_hyperbolic_bridge.py`
