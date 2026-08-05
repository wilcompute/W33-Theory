# Pass 3408 addendum — the 720-edge ordinary degree atlas

The minimum-support carrier is reconstructed independently as the 720 non-collinear point pairs of the Hermitian generalized quadrangle

\[
H(3,4)=GQ(4,2).
\]

Unitary transvections generate

\[
PSU(4,2)\cong PSp(4,3),
\qquad |G|=25{,}920,
\]

with deterministic subgroup growth

\[
2,6,12,48,192,25{,}920.
\]

The induced action on the 720 complement edges is transitive. The edge stabilizer has order 36 and its exact subdegrees are

\[
1,2,3,6,9,9,
12^5,
18^{11},
36^{12}.
\]

Thus the orbital rank is

\[
\boxed{34}.
\]

A generic complex element of the exact 34-dimensional commutant has eigenspace dimensions

\[
1,
15,15,
20,20,
24,24,24,
30,30,
45,45,
60,60,
64,
81,81,81.
\]

A generic real symmetric commutant element has dimensions

\[
1,
15,15,
20,20,
24,24,24,
60,60,60,
64,
81,81,81,
90.
\]

The 90-dimensional real sector is the conjugate 45-pair, and one of the three real 60-dimensional sectors is the conjugate 30-pair. Dimension and character norm force the ordinary multiplicity profile

\[
\boxed{
1+15_a+15_b+2\cdot20+3\cdot24+30_a+30_b
+45_a+45_b+2\cdot60+64+3\cdot81.
}
\]

Indeed,

\[
1+30+40+72+60+90+120+64+243=720,
\]

while the multiplicity-square sum is

\[
1+1+1+4+9+1+1+1+1+4+1+9=34.
\]

The construction of the group, edge orbit, stabilizer, subdegrees, orbital relations, and commutant matrices is exact. The isotypic dimensions are recovered from deterministic, widely separated numerical commutant eigenvalues and are independently constrained by the exact dimension and rank equations. The GAP/CTblLib workflow remains as a row-label cross-check, particularly for naming the selected conjugate degree-30 pair.
