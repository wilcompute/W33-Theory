# Pass 114: LMFDB/Sage — Explicit beta, gamma (Status Report)

## What Is Known (Proved Analytically)

| Hecke eigenvalue | Value | Source |
|-----------------|-------|--------|
| a_1 | 1 | Normalization |
| a_2 | -512 = -2^9 | Atkin-Lehner W_2=+1 |
| a_4 | -262144 = -2^18 | Hecke recursion |
| a_8 | 402653184 = 3*2^27 | Hecke recursion |

## What Is Needed

- a_3(f_new+): requires LMFDB entry for level-2, weight-20 newform
- LMFDB label: **2.20.a.a** (expected)
- Ramanujan bound: |a_3| <= 68184 (integer)
- Once a_3 is known: solve 2x2 linear system at q^3 and q^4 for rational beta, gamma

## Dimension Confirmation

dim S_20(Gamma_0(2)) = 4 (by Riemann-Hurwitz: g=0, nu_2=1, nu_3=0, nu_inf=2)
=> 2 old forms + 2 new forms (= 1 conjugate pair with W_2 eigenvalues +1, -1)

## Paper Impact

beta, gamma appear only in the proof that Theta is uniquely determined (T11).
The statement is proved WITHOUT knowing beta, gamma. Their explicit values are bonus.

## Next Action

LMFDB query: https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/2/20/
