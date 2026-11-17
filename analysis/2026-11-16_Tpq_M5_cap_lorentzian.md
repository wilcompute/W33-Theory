# Lorentzian growth of the capped M5 flux domain

The [finite-amplitude cap](2026-11-16_Tpq_M5_finite_stripe.md) is an \(S^5\times S^1\) M5 probe wrapping the spectator torus circle. Its continuation into Lorentzian AdS has an exact trajectory in the other torus coordinate. On each of the three tested warped backgrounds the fronts meet around that circle before the first AdS refocusing, at both the equal-action circumference and the round radial threshold. This gives the probe evolution up to contact. A final flux state requires the dynamics when the fronts interact. [Coleman and De Luccia, continuation through the light cone](https://doi.org/10.1103/PhysRevD.21.3305) · [Wrapped M5 discharge](https://arxiv.org/abs/2610.08939)

## Continue through the tip

Use lengths and times in local AdS units at the warp minimum. Let \(z\) measure proper distance along the cycle where the cap localizes, let \(c=4/\alpha\), and write \(P_{\rm cap}\) for the Euclidean cap width. The two Euclidean graphs from their tips \(z_{\pm,0}=\pm P_{\rm cap}/2\) have
\[
 z_\pm(r)=z_{\pm,0}\mp\int_0^r
   \frac{c V_E(s)}{\sqrt{\sinh^8s-c^2 V_E(s)^2}}\,ds,
 \qquad V_E(r)=\int_0^r\sinh^4v\,dv .
\]
They are even analytic functions of \(r\) near the tips, with displacement \(cr^2/10+O(r^4)\). Continuing an angle on the external \(S^4\) gives the real exterior \(\mathrm{AdS}_5\) metric \(dr^2+\sinh^2r\,ds_{\mathrm{dS}_4}^2\). For example, in the AdS embedding coordinates its radial invariant is \(X_{-1}=\cosh r>1\). For the future interior take \(r=i\tau\), with \(X_{-1}=\cos\tau\), \(X_0=\sin\tau\cosh\chi\), and \(\vec X=\sin\tau\sinh\chi\,\widehat n\). The metric there is
\[
 ds^2_{\rm AdS}=-d\tau^2+\sin^2\tau\,ds_{H^4}^2,\qquad 0<\tau<\pi .
\]
The exterior and interior trajectories agree smoothly by analyticity in \(r^2\) near the light cone. The upper and lower tips continue as
\[
 z_\pm(\tau)=z_{\pm,0}\pm d(\tau),\qquad
 d(\tau)=\int_0^\tau \frac{c V_L(s)}{\sqrt{\sin^8s+c^2 V_L(s)^2}}\,ds,
 \qquad V_L(\tau)=\frac{3\tau}{8}-\frac{\sin 2\tau}{4}+\frac{\sin 4\tau}{32}.
\]
Here \(V_E(i\tau)=iV_L(\tau)\); the sign reverses the Euclidean narrowing. An independent Lorentzian derivation uses the probe Lagrangian per unit hyperbolic volume, up to a positive overall factor,
\[
 L_\pm=-\sin^4\tau\sqrt{1-\dot z_\pm^2}\mp c V_L\dot z_\pm.
\]
The sign of the electric term differs on the two sheets. The conserved momentum vanishes by the regular initial behavior \(\dot z_\pm=\pm c\tau/5+O(\tau^3)\), giving the same velocities. Each front is timelike for \(0<\tau<\pi\), with speed tending to one at the first open-chart refocusing. The transverse position remains stationary for this ansatz, and the magnetic four-form still pulls back to zero.

## First contact on the torus

For \(L_\parallel>P_{\rm cap}\) the expanding domain covers a proper longitudinal interval of length \(P_{\rm cap}+2d(\tau)\) until contact. Its first contact with its periodic image in the future open chart satisfies
\[
 L_\parallel=P_{\rm cap}+2d(\tau_{\rm hit}).
\]
The function \(d\) is strictly increasing, so a unique contact occurs before refocusing precisely when \(P_{\rm cap}<L_\parallel<P_{\rm cap}+2d(\pi)\). The exterior part of the cap cannot meet an image earlier, since its longitudinal width decreases outward from the light cone. On the center geodesic, \(\tau\) equals global AdS time measured from nucleation in the chosen units. The relative Lorentz factor of the colliding probe fronts in the one common comoving frame is \((1+\dot d^{\,2})/(1-\dot d^{\,2})\).

| Chern pair | \(\tau_{\rm hit}\) at equal actions | Front speed at equal actions | \(\tau_{\rm hit}\) at round threshold |
| --- | ---: | ---: | ---: |
| \((7,8)\) | \(0.945616\) | \(0.676395\) | \(0.986061\) |
| \((8,9)\) | \(0.943472\) | \(0.675629\) | \(0.986517\) |
| \((38,43)\) | \(0.956221\) | \(0.680010\) | \(0.963280\) |

All these times precede \(\pi\). Since contact time is increasing in circumference, every circumference between the equal-action crossing and the round threshold also meets before refocusing in these examples. The equal-action relative Lorentz factors are about \(2.68\)–\(2.72\).

The two sheets are oppositely oriented boundaries of one lower-flux interval. Integrating the magnetic source equation over the horizontal four-cycle shows that crossing them changes its flux period by opposite units, consistent with periodicity. When the sheets meet, the probe continuation ceases to determine the flux evolution. A transition to a homogeneous lower-flux state would require resolving the collision, including the dynamical form fields and conserved Page data. The calculation also does not follow a noncolliding pair beyond the first AdS caustic.

Reproduce the [certificate](../data/toe_20261116_Tpq_M5_cap_lorentzian.json) with `py -3 -B analysis/toe_20261116_Tpq_M5_cap_lorentzian.py`. It checks the analytic continuation of the hyperbolic primitive, the Lorentzian momentum relation, and the contact condition at both circumferences.
