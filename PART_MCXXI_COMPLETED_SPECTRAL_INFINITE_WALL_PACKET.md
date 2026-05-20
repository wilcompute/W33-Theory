# Part MCXXI: Completed Spectral Infinite Wall Packet

**Date:** 2026-05-19  
**Series:** W(3,3) Theory of Everything  
**Status:** VERIFIED INFINITE-CUTOFF WALL ACTION / ORDER / HESSIAN / STIFFNESS ENCLOSURES

---

## Why this part exists

MCXV showed that the positive-real completed spectral branch reaches a finite wall packet at
$\lambda=6$ for every finite cutoff. MCXIX then showed that this wall packet carries its own local
boundary effective theory, and MCXX proved that the canonical interior packet at $\lambda=4$ transfers
exactly to it across the interval $[4,6]$.

The next natural question is global: does the wall packet itself survive the split-prime cutoff limit,
or is it only a finite-cutoff boundary convenience?

---

## The theorem

Fix finite real $s>0$ and a split-prime cutoff $X\ge 7$. At the wall scale $\lambda=6$, the finite-cutoff
completed spectral action, order parameter, and Hessian,
\[
\mathcal F_X(s;6),\qquad \mathcal M_X(s;6),\qquad \chi_X(s;6),
\]
increase monotonically with $X$ and converge to finite infinite-cutoff wall values
\[
\mathcal F_\infty(s;6),\qquad \mathcal M_\infty(s;6),\qquad \chi_\infty(s;6).
\]
Moreover, with
\[
X_*=\max\{X,7\},
\]
one has the explicit wall-tail bounds
\[
0<\mathcal F_\infty(s;6)-\mathcal F_X(s;6)
\le
\frac{12}{X_*}+\frac{72}{(1-(6/X_*)^2)X_*^2},
\]
\[
0<\mathcal M_\infty(s;6)-\mathcal M_X(s;6)
\le
\frac{2}{X_*}+\frac{36}{(1-(6/X_*)^2)X_*^2},
\]
\[
0<\chi_\infty(s;6)-\chi_X(s;6)
\le
\frac{12}{(1-(6/X_*)^2)^2 X_*^2}.
\]
Therefore the infinite-cutoff wall stiffness
\[
\Sigma_\infty(s;6)=\chi_\infty(s;6)^{-1}
\]
admits the reciprocal enclosure
\[
\frac{1}{\chi_X(s;6)+H_X^{\mathrm{wall}}}
\le
\Sigma_\infty(s;6)
\le
\frac{1}{\chi_X(s;6)},
\]
where
\[
H_X^{\mathrm{wall}}=\frac{12}{(1-(6/X_*)^2)^2 X_*^2}.
\]
Finally, the wall Legendre dual also survives with the certified absolute error bound
\[
\left|\Gamma_\infty(s;6)-\Gamma_X(s;6)\right|
\le
6\,T_X^{\mathrm{wall}}+B_X^{\mathrm{wall}},
\]
where the right-hand side uses the order and action wall-tail bounds above.

---

## Reading

This upgrades the wall packet from a finite-cutoff endpoint to a genuine infinite-cutoff boundary object.
The zero-sheet $6$-cycle no longer lands merely on a finite packet that happens to exist cutoff by cutoff;
it lands on a thermodynamic packet that survives the whole split-prime completion.

So the zero-sheet boundary is now controlled at three levels simultaneously:

1. it is finite at every cutoff (MCXV),
2. it has its own local effective theory (MCXIX), and now
3. it survives to infinite cutoff with explicit thermodynamic error bars (MCXXI).

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_completed_spectral_infinite_wall_packet.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_completed_spectral_infinite_wall_packet.json`
- Result: `PART_MCXXI_completed_spectral_infinite_wall_packet_results.json`
