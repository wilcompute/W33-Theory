# Charged spin-two minima and the cubic quiver anomaly in the integral basis

Use the [primitive circle bundle](2026-11-14_cubic_iib_spin.md) \(Y\to S\) over a smooth cubic with \(\mathrm{Ric}_S=6g_S\), unit Reeb one-form \(\eta\), and \(d\eta=2\omega\). The unit Reeb orbits have period \(2\pi/3\). Take the Type IIB \(\mathrm{AdS}_5\times Y\) solution with \(n_5\) five-form flux units. All masses below refer to the classical transverse-traceless spin-two tower. Its internal wave equation is the scalar Laplacian on the unit link. [Spin-two geometric bounds](https://arxiv.org/abs/2104.12773)

## The exact minimum at each nonzero circle charge

Choose the charge sign for which functions satisfying \(\mathcal L_\xi f=3ikf\) for \(k>0\) are sections of \((-K_S)^k\), where \(\xi\) is the unit Reeb vector. Horizontal differentiation is the corresponding line-bundle covariant derivative. The unit circle fibers are totally geodesic, so the Laplacian quadratic form splits into vertical energy \(9k^2\) and the horizontal Bochner Laplacian. The Chern curvature has \(iF=6k\omega\). Its Kähler contraction is \(12k\) because the complex dimension is two. On sections, the Bochner–Kodaira identity therefore gives \(\nabla^*\nabla=2\bar\partial^*\bar\partial+12k\). Charge conjugation handles negative \(k\). [Bochner and Kodaira operators on a positive line bundle](https://arxiv.org/abs/1912.07407)

The lower bound is attained in each nonzero charge sector by the holomorphic sections or their conjugates. The exact minima and their complex multiplicities per charge sign are

\[
m^2_{k,\min}L^2=9k^2+12|k|,\qquad
h_k=\binom{|k|+3}{3}-\binom{|k|}{3}=\frac{3|k|^2+3|k|+2}{2}.
\]

Here the binomial with upper index below three is zero. In particular the lowest charged spin-two level has \(m^2L^2=21\) and four complex modes at each sign. The AdS dimension at a charged minimum is \(\Delta=2+\sqrt{4+m^2L^2}=3|k|+4\), consistent with the holomorphic cone function calculation. Neutral functions are ordinary scalar functions on \(S\). The known Kähler Lichnerowicz threshold is strict on a smooth cubic because its automorphism group is finite, so its first base eigenvalue exceeds 12 in this normalization. The full first positive spin-two squared mass is exactly \(\min\{\lambda_1(S),21\}\) and lies in \((12,21]\). Determining which side of 21 the neutral eigenvalue lies on remains a geometric calculation. [Holomorphic cone modes](https://arxiv.org/abs/hep-th/0603021) · [Kähler first eigenvalue bound](https://www.numdam.org/item/10.5802/aif.2415.pdf)

## Chern–Simons coefficients and a direct quiver trace check

Let \(G_{ij}=-\int_S\gamma_i\wedge\gamma_j\) be the positive \(E_6\) Gram matrix of integral primitive classes. Normalize the RR baryonic wavefunctions as \(\omega_i=\eta\wedge\gamma_i/(2\pi/3)\), with zero Killing vector. Use the superconformal R generator and the geometric anomaly formula of Benvenuti, Pando Zayas and Tachikawa, Eqs. (2.20), (2.22), and (2.23). In those conventions \(k_R=(4\pi/3)\xi\), \(\omega_R=-\pi\eta\wedge\omega/(3\operatorname{Vol}Y)\), and \(c_{IJK}\) is \(n_5^2/2\) times the six-term permutation sum of \(\int_Y\omega_I\wedge\iota_{k_J}\omega_K\). The chosen baryonic generator gives a wrapped line charge \(n_5\int_\ell\gamma_i\) in the quiver normalization. [Geometric triangle anomaly and del Pezzo matching](https://arxiv.org/abs/hep-th/0601054)

For \(Rij\) only the two terms contracting with \(k_R\) survive. The factor from the Reeb period is \((4\pi/3)/(2\pi/3)=2\), so the resulting integral is proportional to \(-G\). Primitivity kills \(RRi\); the entirely baryonic coefficients have no Killing vector. With \(\operatorname{Vol}Y=\pi^3/9\) the full leading symmetric tensor in this basis is

\[
c_{RRR}=8n_5^2,\qquad c_{Rij}=-2n_5^2G_{ij},\qquad c_{RRi}=c_{ijk}=0.
\]

This predicts the known leading \(a=9n_5^2/4\). The cubic del Pezzo quiver phase has nine equal-rank nodes and 27 chiral bifundamentals of scalar R-charge \(2/3\), with charges given by their line pairings with the primitive classes. The verifier reuses the repo's frozen line list and independently sums every charge moment through rank three. The linear and cubic moments vanish, and the quadratic moment is \(6G\). Each chiral fermion has R-charge \(-1/3\), giving the mixed anomaly \(-2n_5^2G\), while the nine neutral gauginos of R-charge one give \(c_{RRR}=(9-27/27)n_5^2\) at leading order. This reproduces the established matching in the marked lattice basis directly from the 27 charges. The coefficients refer to these Abelian currents and carry no claim about extra currents. [Cubic quiver field assignments, Section 3.5](https://arxiv.org/abs/hep-th/0404065)

Replay with `py -3 analysis/toe_20261114_cubic_iib_spectrum_anomalies.py`.
