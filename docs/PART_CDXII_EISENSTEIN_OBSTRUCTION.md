# Part CDXII — The Eisenstein Obstruction and Ghost Rungs

## The Corrected Ghost Criterion

Among the seven ladder n-indices {1, 2, 3, 4, 7, 8, 9, 10}, exactly
three are NOT A2 lattice norms:

    Ghost indices: {2, 8, 10}  (count = 3 = fermion generations)
    Geometric indices: {1, 3, 4, 7, 9}  (count = 5)

**Theorem CDXII.1 (Eisenstein Obstruction):** A positive integer n is
an A2 lattice norm if and only if every prime p ≡ 2 (mod 3) divides
n to an even power.

The ghost ladder indices are exactly those with an inert prime
(p ≡ 2 mod 3) raised to an **odd** power:

    n= 2 = 2^1     → p=2 (inert, e=1 odd)   → ghost
    n= 8 = 2^3     → p=2 (inert, e=3 odd)   → ghost
    n=10 = 2·5     → p=2,5 (both inert, e=1 odd) → ghost

Geometric indices have NO inert prime to odd power:

    n=1: trivial                    → geometric
    n=3 = 3^1: p=3 ramified, NOT inert → geometric
    n=4 = 2^2: p=2 inert BUT e=2 even → geometric
    n=7 = 7^1: p=7≡1 mod 3, SPLIT     → geometric
    n=9 = 3^2: p=3 ramified, e=2 even → geometric

## Three Obstruction Types ↔ Three Generations

The three ghost indices represent three DISTINCT types of
Eisenstein obstruction:

    Type A (single inert prime, 1st power):  n=2  = 2^1
    Type B (single inert prime, 3rd power):  n=8  = 2^3
    Type C (product of two inert primes):    n=10 = 2·5

These three types are combinatorially exhaustive for ghost indices
≤ 10, and their count |{A,B,C}| = 3 equals the number of fermion
generations. The correspondence:

    Type A (lightest obstruction) ↔ 1st generation (electron)
    Type C (double obstruction)   ↔ 2nd generation (muon)
    Type B (cubic obstruction)    ↔ 3rd generation (tau)

## Split Prime p=7 is Geometric

The prime p=7 appears as n=7 in the ladder (giving rung 192 = |W(D4)|).
Since 7 ≡ 1 (mod 3), it is a SPLIT prime in Z[ω] — it factors as π·π̄
for some Eisenstein prime π. Therefore n=7 is an A2 norm (r_{A2}(7)=12)
and the rung 192 is geometric. This is why |W(D4)| = 192 = 8×24 lands
in the geometric (A2) part of the ladder.
