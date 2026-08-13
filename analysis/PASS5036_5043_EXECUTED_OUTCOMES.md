# Passes 5036-5043 executed outcomes

Status: EXECUTED 2026-08-13. Producers: `analysis/w33_pass5036_5037_apartment_tritangent_hecke.py` and `analysis/w33_pass5038_5043_jacobian_frame_family.py`.

**5036.** The labeled 200x45 cover/tritangent matrix U and 1620x200 apartment/cover matrix Y give Z=YU of rank 25. Row sum 108, column sum 3888, and `Z^T Z = 3132 I - 1044 A_trit + 9540 J`. Squared singular spectrum is `419904^1 + 6264^24 + 0^20`; apartment transport again has image `1+V24` and kills V20.

**5037.** The eight flag-fiber orbitals are the eight C2 Weyl cells with `(length,subdegree)=(0,1),(1,3),(1,3),(2,9),(2,9),(3,27),(3,27),(4,81)`. The raw rank-81 projector coefficients are `81,-27,-27,9,9,-3,-3,1`, namely `(-1)^ell 3^(4-ell)`.

**5038.** The Levi incidence matrix has F2 rank 79. The reduced mod-2 Laplacian of the all-edge subdivision has nullity 81 and its kernel is canonically `ker(B)`. Thus `K(SubLevi)/2K(SubLevi) ~= H1(Levi;F2) ~= F2^81`.

**5039.** The apartment frame reconstructs by `v=(1/160)XX^T v`. Absolute correlations from each apartment are `4^16,3^32,2^96,1^288,0^1187`. Every removal set of size at most 46 is certified safe; the Gershgorin bound is 159. Removing all 81 apartments through one chamber drops rank to 80. An explicit 81-column basis has numerical 2-condition number about 12.6491.

**5040.** The PSp apartment stabilizer is split `V4:C4`, order 16, with center 4 and derived 2; point/line/flag intersections are `C4,V4,C2`. The PGSp stabilizer is split `V4:D8`, order 32, with center 4 and derived 4; point/line/flag intersections are `D8,C2^3,V4`. D8 denotes the square dihedral group of order 8. This order-32 group is not the older extraspecial-plus order-32 subgroup.

**5041.** In 81 fundamental-cycle coordinates, a concrete set of 81 apartment cycles has determinant +/-1. Hence apartment cycles generate the entire integral Levi cycle lattice, not merely its rational span.

**5042.** The binary Levi cycle space is `[160,81,8]_2`. Its complete minimum-weight shell consists of exactly the 1620 apartments.

**5043.** For W(3,q), points and lines each number `(q+1)(q^2+1)`, chambers number `(q+1)^2(q^2+1)`, cycle rank is `q^4`, apartments per chamber are `q^4`, and total apartments are `q^4(q+1)^2(q^2+1)/8`. The kernel is `(-1)^ell q^(4-ell)`. Direct matrix checks pass at q=2 `(45,90,16)` and q=3 `(160,1620,81)`. For odd q, the subdivision mod-2 Jacobian quotient has dimension q^4.

Synthesis: the same protected sector is now connected by a chain map, coherent-algebra idempotent, labeled cubic-surface transport, Jacobian quotient, tight frame, unimodular integral apartment basis, and minimum-word binary shell.
