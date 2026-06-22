# BT1480--BT1482: C3 x V4 grid, E6 claim-DAG merge, and closure ABI v2

## BT1480 — product reading of the strand grid

The 12 closure strands are best modeled as

\[
C_3\times V_4,
\qquad V_4=C_2\times C_2,
\]

rather than as a bare \(C_{12}\) or \(C_3\times C_4\).  The reason is structural:
the branch coordinate is two-bit D4/V4 data and has no distinguished order-4
generator.

The axes are:

- \(C_3\): three Szilassi/Fano channels and qutrit phase axis;
- \(V_4\): four E6 gauge triangles and D4 branch bits.

## BT1481 — E6 firewall claim-DAG merge

The E6 firewall square is now upstream in the claim DAG.  Added exact nodes:

- E6 firewall square: \(36\to72\), \(72+6=78\), \(72+9=81\);
- oriented 72-sector shared by E6 roots and ABI rows;
- H1/CSS 81 closure;
- \(C_3\times V_4\) strand grid.

The claim firewall remains intact: blocked formula/physics claims cannot support
exact finite claims.

## BT1482 — closure ABI v2

The closure ABI is upgraded to v2.  Each packet carries:

- \(C_3\) channel;
- \(V_4\) branch;
- side and orientation bits;
- active column;
- guard columns;
- channel membership;
- triangle membership;
- 72-row sector metadata;
- \(+9\) firewall gap closure metadata;
- claim-DAG dependencies.

The new packet formula is

\[
\mathrm{strand}=4c+b,
\]

with

\[
\mathrm{active}=14\mathrm{strand}+13,
\qquad
\mathrm{guard}=(216+2\mathrm{strand},216+2\mathrm{strand}+1).
\]

## Current synthesis

\[
\boxed{
C_3\times V_4
\quad\Rightarrow\quad
24+48=72
\quad\Rightarrow\quad
72+9=81
}
\]
