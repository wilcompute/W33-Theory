# Pass 443 — section-sensitive Smith classification

All 81 inverse-closed sections of the `q=3` Heisenberg quotient are classified
exactly.

For offsets `(c0,c1,c2,c3)` on the four antipodal coset pairs, define

\[
\delta(c)=(c_2-c_0-c_1,\;c_3-2c_0-c_1)\in\mathbb F_3^2.
\]

## Flat orbit

`delta=0` gives exactly 9 sections. They form one `Aut(H_3)` orbit and have

\[
\chi_A(x)=(x-8)(x-2)^{12}(x+1)^8(x+4)^6.
\]

Their critical group is

\[
(\mathbb Z/3)^4\oplus(\mathbb Z/6)^4\oplus
\mathbb Z/18\oplus\mathbb Z/54\oplus(\mathbb Z/216)^6.
\]

## Curved orbit

`delta!=0` gives the remaining 72 sections. They form the second and only other
`Aut(H_3)` orbit and have

\[
\chi_A(x)=(x-8)(x+1)^{14}(x^2-x-11)^6.
\]

Their critical group is

\[
\mathbb Z/3\oplus(\mathbb Z/9)^4\oplus(\mathbb Z/27)^3
\oplus(\mathbb Z/135)^5\oplus\mathbb Z/405.
\]

The curved spanning-tree order is `3^37 5^6`; the flat order is `2^24 3^31`.
Thus curl changes the rational spectrum and integral torsion simultaneously.
At `q=3` there is no third class and no cospectral-but-Smith-distinct section.
