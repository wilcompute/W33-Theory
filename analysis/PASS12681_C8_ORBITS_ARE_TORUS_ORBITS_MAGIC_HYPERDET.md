# Pass 12681: an order-4 code space attains c₈ iff its group lies in a torus rank-3 group (4 of 17 orbits); the two magic values are exact; the three-tangle is not canonical

Claude track. Follows Pass 12680. **Not a theory of everything.**

## 1. Per-orbit minima (`w33_f8_order4_orbit_classification.py`, Pass 12681 section)

For each of the 17 orbits of uncovered order-4 groups, the code computes: the minimum of F on a representative's 16-dimensional code space (best over the four sign choices, 6 starts each), the stabiliser order in H = (SL(2,8) × SL(2,8)) ⋊ Frobenius (|H| = 762,048), and how many of the seven order-4 subgroups of the torus group T lie in the orbit.

| orbit (type, size) | \|Stab_H\| | code-space minimum | census minimisers | T subgroups |
|---|---|---|---|---|
| A, 1,512 | **504** | **c₈** | 9 | 1 |
| B\*, 42,336 | 18 | **c₈** | 7 | 3 |
| B, 84,672 | 9 | **c₈** | 0 | 2 |
| C, 42,336 | 18 | **c₈** | 0 | 1 |
| {1: 136-type}, {1: 140-type} | 8 | 2.7318, **2.7410899854** | 0 | 0 |
| {4: 2}-type, 31,752 | 24 | **2.7410899854** | 0 | 0 |
| {1: 120, 135}-type, 1,512 | 504 | 2.76998 | 0 | 0 |
| {22}-type; B (×2, 84,672 and 42,336) | 14; 9, 18 | 2.80949; **2.81234** (×2) | 0 | 0 |
| B, 84,672 | 9 | 2.84820 | 0 | 0 |
| {14}-types (×2) | 7, 14 | 2.86342, 2.94546 | 0 | 0 |
| {3: 7}-type; C, 14,112 | 14; 54 | **3** (stabiliser value) | 0 | 0 |
| {1: 135}-type, 504 | 1,512 | **7** | 0 | 0 |

> **Result (numerical, all 17 orbits).** Exactly **4** orbits have code spaces attaining c₈, and they are **exactly the orbits containing subgroups of the torus group T** (1 + 3 + 2 + 1 = 7). Every other orbit's minimum is strictly above c₈.
>
> Generic global minimisers (Pass 12674/12679 census) sit only in A and B\*. The orbits B (2 T-subgroups) and C reach c₈ only at the torus points, consistent with the local-rigidity picture of Pass 12675.

The other minima reproduce known critical levels: 2.7410899854 (the root of 13c³ − 265c² + 1447c − 2243, Pass 12672) in two orbits; 2.81234 (Pass 12672) in two; the stabiliser value 3 in two. Orbit A's stabiliser has order **504 = |SL(2,8)|**, an unusually large symmetry for the 16-dimensional code space carrying half the minimisers.

## 2. The two magic values are exact (`w33_f8_torus_eigenstate_magic.py`)

| torus eigenstates | logical stabiliser fidelity | closed form |
|---|---|---|
| r = ±1, ±2, ±4 (primitive ninth roots; c₈, 4.6048, 8.5634) | 0.5099291129236313 | (3 + √3)(γ + γ²)/36 = (3 + √3)·cos²(π/18)/9 |
| r = ±3 (cube roots; c = 37/3) | 0.490562612162345 | **(9 + 5√3)/36** |

The values are identified by pslq at 15 digits, with a spread across lifts of 2×10⁻¹⁵ and small coefficients. The non-primitive value involves only √3, matching cube roots of unity, and the primitive one needs Q(cos 2π/9).

## 3. Black-hole/qubit control: the three-tangle is not canonical (`w33_f8_hyperdet_control.py`)

The STU black-hole dictionary uses the three-qubit Cayley hyperdeterminant, which is invariant under local SL(2)³ only.
- In the fixed effective basis, all 300 minimiser runs give the same 4|Det| = 0.216727, so the problem's own symmetries preserve it there.
- Local gates (H, S) preserve it (400/400), which is the control.
- **Random entangling Clifford changes of the effective factorisation give 66 distinct values** (0.067 to above 0.2).

> The effective three-qubit factorisation is a free choice, so the minimiser carries no canonical three-tangle or STU "entropy". The connection to the magic three-qubit Veldkamp line (Lévay–Planat–Saniga) is at the level of the shared E₇ geometry only (Pass 12678, 12680).

## 4. Status of the other tasks

- **Exact c₈ certificate.** PARI/GP is available (C:/tools/pari/gp.exe). The construction (exact face over Q(γ, i), rounding, exact solve and PSD check) remains a multi-hour build and was not started.
- **Degree 8 on 16-dimensional spaces.** Orbit A's stabiliser of order 504 is the natural symmetry to exploit. It acts by non-monomial Cliffords on the effective space, so using it needs a numerical commutant or isotypic decomposition of the monomial spaces. Not attempted.
