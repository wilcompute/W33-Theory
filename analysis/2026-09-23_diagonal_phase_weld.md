# 2026-09-23 — Diagonal center/external phase weld

The cubic compiler now has a coordinate-native symmetry-changing background in
the **current physical-Clifford H27 gauge**.

The canonical signed E6 cubic does not use the raw Pass1103 H27 coordinates as
the compiler gauge.  The explicit bridge in
\`data/w33_e6id_current_h27_gauge_bridge.json\` first conjugates all 45 canonical
cubic triads to the current five-direction H27 right-coset system while sending
all nine firewall fibers to the current pure-center spread.

Write the current scheduler address as
\[
K=H_{27}\times C_3^{\rm ext},\qquad
h=(a,b,c)=Z^aX^b\omega^c,
\]
with external phase \(p\in\mathbb F_3\).  The pure-central H27 direction has
two lifted external slopes
\[
g_+=((0,0,1),1),\qquad g_-=((0,0,1),2).
\]
The diagonal coordinates
\[
\tau_-=c-p,\qquad \tau_+=c+p\pmod 3
\]
are constant on right cosets of \(g_+\) and \(g_-\), respectively.

For the three-level backgrounds \(v_\pm=1+\tau_\pm\in\{1,2,3\}\), each
amplitude occurs exactly 27 times.  Exact rational Jacobian ranks and
current-gauge Fourier-quotient ranks are:

| background | exact rank \(D_v\) | quotient rank |
|---|---:|---:|
| center only \(1+c\) | 36 | 36 |
| external only \(1+p\) | 54 | 36 |
| diagonal \(1+(c+p)\) | 66 | 54 |
| diagonal \(1+(c-p)\) | 66 | 54 |

The quotient ranks are independently certified at split Eisenstein primes 103
and 109.  For either diagonal weld,
\[
\operatorname{rank}(S_1+\operatorname{Im}D_v)=81,
\]
so
\[
\operatorname{rank}\!\left(
\operatorname{Im}D_v\to\operatorname{Reg}(K)/S_1
\right)=54.
\]

This is the structural point: the center factor alone reaches 36 retyped
directions; the external qutrit factor alone also reaches 36; but correlating
them diagonally reaches **all 54** directions required by the minimal
symmetry-changing compiler.  The diagonal raw rank is 66, leaving a
12-dimensional intersection with the operator-compatible \(S_1\) sector.

The two diagonal choices are the conjugate slope pair already present in the
lifted central cubic geometry.  No dynamical preference between them, physical
VEV, D/F-flat vacuum, or hardware pulse is inferred.

Evidence:
- analysis/w33_e6id_current_h27_gauge_bridge.py
- data/w33_e6id_current_h27_gauge_bridge.json
- analysis/w33_e6_cubic_diagonal_phase_weld.py
- data/w33_e6_cubic_diagonal_phase_weld.json
