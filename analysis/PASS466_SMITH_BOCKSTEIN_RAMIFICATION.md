# Pass 466 — Smith/Bockstein ramification theorem

Let \(m_e\) be the number of p-primary Smith elementary divisors of exponent \(e\), and define

\[
\kappa_j=\log_p\left|\ker(M\bmod p^j)\right|.
\]

For every nonsingular square matrix over a DVR, or any finite chain-ring truncation, Pass 466 records the universal identities

\[
\kappa_j=\sum_e m_e\min(e,j),
\]

\[
\kappa_j-\kappa_{j-1}=d_j=\sum_{e\ge j}m_e,
\]

\[
m_j=d_j-d_{j+1}=2\kappa_j-\kappa_{j-1}-\kappa_{j+1}.
\]

Applied to the Pass-448 \(\mathbb Z/9\) Laplacian, the tail dimensions are

\[
629,475,313,233,223,18,18,7,0,
\]

and the kernel-growth staircase is

\[
0,629,1104,1417,1650,1873,1891,1909,1916,1916.
\]

The exponent-six multiplicity is the zero second difference

\[
m_6=2\kappa_6-\kappa_5-\kappa_7=0.
\]

Equivalently, \(d_6=d_7=18\): every class surviving to level six lifts through one additional p-adic level. Then 11 terminate at exponent 7 and 7 at exponent 8.

This plateau is localized exactly at the primitive ninth-cyclotomic ramification index:

\[
\varphi(9)=6,
\]

and

\[
\Phi_9(1+u)=3+9u+18u^2+21u^3+15u^4+6u^5+u^6
\]

is Eisenstein at 3.

The universal extraction theorem and the exact ramification-localized gap are closed. A formula for every multiplicity as a function of \(p\) and chain length remains open.
