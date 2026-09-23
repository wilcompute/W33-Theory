# 2026-09-23 — Cubic image covers the full 54D Fourier-retyped quotient

The nonlinear compiler problem can now be stated in the exact **current H27
address gauge**.

The canonical E6-id cubic labels are first transported by the explicit
27-point gauge conjugacy
\`data/w33_e6id_current_h27_gauge_bridge.json\`.  That bridge sends all 45
canonical cubic triads to the current five-direction H27 coset system and all
nine firewall fibers to the current central spread.  Only after that transport
do we apply the current H27 Schrödinger/Fourier coordinates.

The address module has
\[
\operatorname{Reg}(K)=S_1^{(27)}\oplus S_2^{(27)}\oplus L^{(27)},
\]
where the 27-dimensional \(S_1\) sector is operator-compatible.  The minimal
compiler must therefore retype the complementary 54-dimensional quotient.

For a matter background \(v\), define
\[
D_v(x)=[v,x].
\]
The relevant alignment condition is
\[
\operatorname{rank}(S_1+\operatorname{Im}D_v)=81,
\]
equivalently surjectivity of
\[
\operatorname{Im}D_v\longrightarrow \operatorname{Reg}(K)/S_1.
\]

The 27 current-gauge \(S_1\) matrix coefficients are built from the frozen
qutrit Schrödinger representation and the three external \(C_3\) characters.
Reduction in \(\mathbb Z[\omega]\) at split primes 103 and 109 gives the same
table at both primes:

| background | rank \(D_v\) | rank \(S_1+\mathrm{Im}D_v\) | quotient rank | \(\dim(S_1\cap\mathrm{Im}D_v)\) |
|---|---:|---:|---:|---:|
| root | 20 | 47 | 20 | 0 |
| uniform | 54 | 63 | 36 | 18 |
| linear | 54 | 72 | 45 | 9 |
| quadratic | 78 | 81 | 54 | 24 |

For
\[
v_n=(n+1)^2
\]
in the frozen canonical matter-row ordering, an \(81\times81\) minor remains
nonzero after reduction.  Therefore it was already nonzero over
\(\mathbb Q(\omega)\), and
\[
\operatorname{rank}\!\left(
\operatorname{Im}D_v\to\operatorname{Reg}(K)/S_1
\right)=54.
\]

Thus one explicit cubic background accesses every Fourier direction that the
minimal compiler must retype.  The image is not claimed to equal the chosen
\(S_2\oplus L\) complement; it intersects \(S_1\) in dimension 24 and projects
surjectively onto the quotient.

The rank-54 uniform and linear backgrounds demonstrate why raw Jacobian rank
alone is insufficient: they reach only 36 and 45 quotient directions,
respectively.

Evidence:
- analysis/w33_e6id_current_h27_gauge_bridge.py
- data/w33_e6id_current_h27_gauge_bridge.json
- analysis/w33_e6_cubic_fourier54_alignment.py
- data/w33_e6_cubic_fourier54_alignment.json
