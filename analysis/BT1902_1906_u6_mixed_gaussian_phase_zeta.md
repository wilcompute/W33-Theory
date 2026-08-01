# Passes 1902–1906 — U6, the mixed separator tensor, Gaussian V9, subgroup phases, and twisted Ihara zeta

## Executive result

All five fronts were executed. The packet verifies **33/33** frozen assertions. Passes 1904 and 1906 close completely; Pass 1905 closes the named chain and every cyclic subgroup class; Passes 1902 and 1903 now have exact finite reductions and compiled chunkable workers, with the genuinely enormous final contractions left as explicit proof boundaries.

The parallel audit is incorporated: its false spread-uniformity bound is neither used nor repeated, while its theorem `End_PSp(90)=C` sharpens the phase chain to a canonical choice `±J`.

## Pass 1902 — exact U6 component reduction

The weight-six collision edges by difference-codeword weight are

| weight | edges |
|---:|---:|
| 4 | 204,105,833,100 |
| 6 | 202,385,664,000 |
| 8 | 397,812,076,200 |
| 10 | 507,826,972,800 |
| 12 | 412,008,338,280 |

Thus `E6=1,724,138,884,380`. A weight-12 difference gives disjoint partners, invisible to every coordinate chart. The 44,589,647 weight-12 codewords through a fixed coordinate contribute `20,600,416,914` external-partner incidences with multiplicity. Therefore U6 is not determined by the collision moment. The supplied external-memory worker generates and merges all fixed-chart syndromes, removes weight-0/2/4 shadows, marks external partners in a combinadic bitmap, and counts true singleton components. The heavy run is not represented as complete.

## Pass 1903 — exact mixed separator tensor

The 45 variables are six five-bit fiber blocks plus fifteen residual bits. The 240 parity factors split exactly as

`20 residual + 180 pair + 40 phase`.

Every fiber-block pair supports 12 pair factors and every residual bit appears in 12 pair factors. The 45 absent pair/residual incidences form the Tutte–Coxeter graph; the 180 present incidences form its complement. The residual and phase families are the complete twenty-triple systems on six labels, with each phase triple doubled. A chunkable OpenMP worker contracts any subset of the 156 residual S6 orbits against all `2^30` fiber words into the full `21×181×41=155,841` bin space. The final all-orbit merge remains open.

## Pass 1904 — Gaussian V9 lattice

The paired natural V9 carrier is a rank-nine Gaussian lattice with Hermitian determinant `2^18·5^8`, Smith invariants

`2,10,10,10,20,40,40,40,40`,

minimum norm 24, and exactly 60 minimal vectors. Modulo Gaussian units these give 15 lines whose `|h|=4` graph is `KG(6,2)=SRG(15,6,1,3)`. Its graph automorphism group is S6, while the kernel on the lines is scalar C4. Hence

`U(L)=C4×S6`, of order `2880`.

## Pass 1905 — phase subgroup skeleton

At PSp(4,3), the real 90-sector has commutant C and exactly two invariant complex structures, `±J`. The outer involution in `W(E6)=PSp(4,3):2` sends `J` to `-J`, so no full-Weyl phase survives. Exceptional S6 obstructs J on the full 24, 90, and 114 carriers but preserves the paired V9 structure. On A6 the 90-sector admits noncanonical J again.

The cyclic classification is exact. Among involutions, only the double-transposition class supports J on the 90-sector. Among order-four classes, only cycle type `(4,2)` does. C3 and C5 support it; the natural C6 does not. A GAP worker applies the Frobenius–Schur parity criterion to every remaining noncyclic subgroup class.

## Pass 1906 — C4-twisted Ihara zeta

The 90 Hashimoto states split into C4-character dimensions `26,20,24,20`. The reciprocal factors are

- `χ0`: `(1-4u²)(1-u²)^4(1+2u²)^2(1-2u+2u²)^3(1+2u+2u²)^3`
- `χ1=χ3`: `(1-u²)^4(1+2u²)^2(1-2u+2u²)^2(1+2u+2u²)^2`
- `χ2`: `(1-u²)^4(1+2u²)^4(1-2u+2u²)^2(1+2u+2u²)^2`.

Their product is the full Ihara reciprocal polynomial. Primitive unoriented reduced-cycle counts continue with `N18=14280`, `N20=51984`, `N22=189720`, and `N24=703650`. The natural V9 nonbacktracking channel distributes its 36 dimensions as `12+8+8+8` across the four characters.

## Evidence boundary

The parallel `|class∩K10|≤5` constraint was an unsupported uniformity assumption and is explicitly excluded. None of these five results depends on it. U6, the full mixed histogram, and the all-noncyclic subgroup table are claimed only when their supplied exact workers complete and their outputs are frozen.
