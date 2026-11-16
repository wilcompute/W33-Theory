# Modular statistics of the winding instability

The [circle-bundle winding census](2026-11-16_circle_bundle_ring_winding_staircase.md) counts the unstable winding labels at fixed torus shape. Here the torus shape varies over the modular surface, with its normalized invariant area measure. This gives exact count and depth statistics for the [equal-flux M/IIB family](2026-11-16_D9_iib_conifold_dual.md). The measure is a geometric comparison of shapes at fixed flux. It does not prescribe a cosmological population, a modulus potential, or a weighting by quantum vacua.

Write \(N=|N_1|=|N_2|\), \(N_0=|N_0^{\rm flux}|\), \(\tau=x+iy\), and use the reduced domain \(|x|\le1/2,\ x^2+y^2\ge1\). Let \(c=3\pi N_0/N\) and \(R=12/c=4N/(\pi N_0)\). A nonzero signed integer label \(v=(m,n)\) contributes one unstable real Fourier degree in the paired count when its squared lattice norm
\[
 Q_\tau(v)=|m+n\tau|^2/y
\]
satisfies \(Q_\tau(v)<R\). The opposite labels together count two real sine and cosine coefficients. Denote the resulting count by \(U\). In the reduced domain \(y\) is the modular height, and the shortest squared norm is \(1/y\).

## A finite mean and an infinite second moment

For an integrable radial test function \(f(Q_\tau)\), unfold the primitive lattice directions up to sign from the fundamental domain to the parabolic strip. Their mean sum is \((3/\pi)\int_0^\infty f(1/y)\,dy/y^2=(3/\pi)\int_0^\infty f(q)\,dq\). Summing integer multiples of each primitive direction and restoring both signs multiplies this by \(2\zeta(2)\). Thus
\[
 \mathbb E_\tau\sum_{v\ne0} f(Q_\tau(v))=\pi\int_0^\infty f(q)\,dq,
 \qquad \mathbb E_\tau U=\pi R=4N/N_0 .
\]
This is the radial two-dimensional Siegel mean in the present normalization. It is exact for every positive flux ratio, with no large-ratio limit. [Siegel, mean value theorem in geometry of numbers](https://www.jstor.org/stable/1969027)

In the cusp \(y\ge\max(1,R)\), any vector with \(n\ne0\) has squared norm at least \(y\) and cannot contribute. The remaining count is twice the number of positive integers \(j<\sqrt{Ry}\). The part of the reduced domain with \(y\le\max(1,R)\) has a uniform finite count bound. For example \(|n|\le\sqrt{R/(\sqrt3/2)}\) and \(|m+nx|\le\sqrt{R\max(1,R)}\) bound the number of integer candidates. Consequently for all sufficiently large integers \(j\),
\[
 \Pr(U\ge2j)=\frac{3R}{\pi j^2}.
\]
Indeed the event is then precisely the cusp above \(j^2/R\), up to its measure-zero boundary. In particular the second moment diverges even though the mean is finite. If the count is capped at \(A\), then
\[
 \mathbb E[\min(U,A)^2]=\frac{24R}{\pi}\log A+O(1).
\]
If the shape is instead restricted to height \(y\le Y\), the unnormalized truncated second moment grows as \((12R/\pi)\log Y+O(1)\). Both statements follow directly from the cusp formula, so the divergent variance can be tracked under a specified geometric cutoff.

For \(0<R\le1\) the cusp calculation gives the **entire** law. A nonempty count requires \(y>1/R\ge1\), where only the single primitive direction contributes. Thus
\[
 \Pr(U=0)=1-\frac{3R}{\pi},\qquad
 \Pr(U=2j)=\frac{3R}{\pi}\left(\frac1{j^2}-\frac1{(j+1)^2}\right)
 \quad(j\ge1).
\]
Conditional on instability, exactly one pair occurs with probability \(3/4\), and the mean signed count is \(\pi^2/3\). These conditional statistics are independent of the flux ratio in this range. Arbitrarily large counts arise only on very elongated shapes.

At any \(R\), at least one mode is unstable precisely when \(y>1/R\). Integrating the portion of the fundamental domain above that horizontal line gives
\[
\Pr(U>0)=\frac3\pi\left[2\arcsin a+(1-2a)R\right],
\qquad a=\min\!\left(\tfrac12,\sqrt{\max(0,1-R^{-2})}\right).
\]
For \(R\le1\) this reduces to \(3R/\pi\); for \(R\ge2/\sqrt3\) it is one. Between those values the threshold line meets the circular boundary of the reduced domain, so the measure is no longer linear in the flux ratio.

## The depth of the strongest instability

In the [sphere-exchange-odd mass block](2026-11-16_D9_mtheory_uplift.md), set \(\lambda=cQ_\tau\) and define the BF depth \(\nu=\sqrt{-4-m_-^2L^2}\) for unstable modes. The positive range ends at \(3/2\). The condition \(\nu>b\) for \(0\le b<3/2\) is an annulus
\[
 \lambda_-(b)<\lambda<\lambda_+(b),\qquad
 \lambda_\pm(b)=6-b^2\pm2\sqrt{9-4b^2}.
\]
Applying the unfolded mean gives the expected number of such signed labels as
\[
 \mathbb E U_b=\frac{4N}{3N_0}\sqrt{9-4b^2}.
\]
For example integrating the depth tail gives \(\mathbb E\sum\nu=3\pi N/(2N_0)\) and \(\mathbb E\sum\nu^2=6N/N_0\). These means weight each mode separately.

For \(R\le1\) an exact conditional law for the **largest** \(\nu\) follows from the separation between lattice multiples. Given that there is at least one pair, \(w=1/(Ry)\) is uniform on \((0,1)\), and the allowed eigenvalues have the form \(\lambda_j=12j^2w\). The annulus selects intervals
\[
 \frac{\lambda_-}{12j^2}<w<\frac{\lambda_+}{12j^2}.
\]
Adjacent intervals overlap for the first time at
\[
 J=\left\lceil\frac1{\sqrt{\lambda_+/\lambda_-}-1}\right\rceil
 \qquad (0<b<3/2).
\]
The intervals with \(j<J\) are disjoint, and those with \(j\ge J\) give a connected interval from zero to \(\lambda_+/(12J^2)\), apart from irrelevant boundary points. Therefore
\[
 \Pr(\max\nu>b\mid U>0)
   =\frac{\lambda_+-\lambda_-}{12}\sum_{j=1}^{J-1}\frac1{j^2}
      +\frac{\lambda_+}{12J^2}.
\]
The endpoints are one at \(b=0\) and zero at \(b=3/2\). A shape sufficiently far into the cusp has many winding labels, including multiples with eigenvalues near \(\lambda=15/4\), so its maximum approaches the continuous depth \(3/2\). The shortest mode alone would miss this effect, because its eigenvalue tends to zero and its depth tends to zero too.

One field-theory use of this depth variable is the radial behavior under a cutoff in the Poincaré chart. At zero boundary momentum the two scalar solutions are \(z^{2\pm i\nu}\); a real linear combination has adjacent radial nodes separated by a scale factor \(e^{\pi/\nu}\). This factor approaches \(e^{2\pi/3}\) for the deepest mode. The depth statistics above therefore also give the geometric distribution of these radial separations. The calculation concerns the linear equation. An actual double-trace flow or condensate scale requires a boundary condition and a nonlinear completion. [Kaplan, Lee, Son and Stephanov, logarithmic scaling below the BF bound](https://arxiv.org/abs/0905.4752)

The [verifier](toe_20261116_winding_modular_statistics.py) reuses the parallel lattice enumerator and checks the cusp counts, the logarithmic second-moment coefficient, and the deepest-mode law against an independent modular integral on an inverse-height grid. The [certificate](../data/toe_20261116_winding_modular_statistics.json) records the sample thresholds and probabilities.
