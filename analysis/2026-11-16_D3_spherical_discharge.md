# No finite spherical D3 discharge bounce at the charge-normalized tension

The [M/IIB circle duality calculation](2026-11-16_D9_iib_conifold_dual.md) gave an exact backreacted planar D3 wall, dual to a torus-wrapped M5 changing the horizontal flux. Its tension equals its charge in the reduced action. A finite-radius Euclidean wall has a curved four-sphere worldvolume and sources the breathing mode at the junction. The comparison argument here excludes regular \(O(5)\)-invariant discharge bounces with one asymptotic AdS boundary and a finite stack of concentric walls. The result covers charge-normalized tensions and higher multiples with the same scalar dependence, in the sourceful two-derivative breathing-mode truncation with fixed fiber topology and shells smeared over the internal Einstein five-manifold. [Coleman and De Luccia, gravitational vacuum decay](https://doi.org/10.1103/PhysRevD.21.3305) · [Menet, Tomasiello and Van Hemelryck, M5 discharge](https://arxiv.org/abs/2610.08939)

## Equations and boundary conditions

Use the five-dimensional action in the convention \(R-G(\partial b)^2/2-V_Q(b)\), with \(G=80/3\). The internal logarithmic scale is \(b\). On each side of the wall the five-form density parameter \(Q\) is fixed. In reference units the potential and planar first-order function are
\[
 V_Q=-20e^{-16b/3}+\tfrac12Q^2e^{-40b/3},\qquad
 W_Q=10e^{-8b/3}-Qe^{-20b/3}.
\]
Write \(f_Q=-W_{Q,b}/G=e^{-8b/3}-(Q/4)e^{-20b/3}\). The potential identity \(V_Q=G f_Q^2/2-W_Q^2/3\) implies \(V_{Q,b}/G=f_Q f_{Q,b}+(2/3)W_Q f_Q\). For \(Q>0\), the AdS vacuum value \(b_Q\) is fixed by \(e^{4b_Q}=Q/4\), and its AdS radius is \(L_Q=e^{8b_Q/3}\) in the five-dimensional Einstein frame. On \(b\ge b_Q\), \(V_Q<0\), \(W_Q>0\) and \(f_Q\ge0\). The scalar mass at that vacuum is \(32/L_Q^2\).

Let the Euclidean metric be \(d\xi^2+a(\xi)^2d\Omega_4^2\), with \(A=\log a\) and derivatives toward the exterior. The bulk equations are
\[
 \begin{split}
 A'^2&=a^{-2}+G b'^2/24-V_Q/12,\\
 A''&=-a^{-2}-G b'^2/6,\\
 b''+4A'b'&=V_{Q,b}/G.
 \end{split}
\]
Require a regular center with \(a=0\), \(a'=1\), \(b'=0\), and a single exterior tending to the fixed AdS vacuum at \(Q_+>Q_-\ge0\). Denote exterior minus interior values by square brackets. At a wall of finite radius \(a_s>0\), \(a\) and \(b\) are continuous. Write its tension as \(2\kappa_5^2T=\alpha\Delta Q e^{-20b/3}\), \(\Delta Q=Q_+-Q_->0\). Then \(\alpha=1\) is the classical charge-normalized D3 value. The junctions are
\[
 [A']=-\frac{\alpha\Delta Q}{6}e^{-20b_s/3},\qquad
 [b']=-\frac{\alpha\Delta Q}{4}e^{-20b_s/3}.
\]

## The finite-radius obstruction

For an interior with \(Q_->0\), \(V_{-,b}\) has the sign of \(b-b_-\), where \(b_-=b_{Q_-}\). Starting at or below that vacuum at the regular center gives \(b'\le0\) up to the wall, by \((a^4b')'=a^4V_{-,b}/G\). The wall makes \(b'\) smaller, and the exterior then lies below its own vacuum \(b_+>b_-\) with a negative derivative. It cannot turn back toward \(b_+\), by the same equation. Thus a candidate interior starts above \(b_-\), moves upward, and has \(W_->0\), \(f_->0\). For \(Q_-=0\), \(V_{-,b}>0\) and \(f_->0\) everywhere, so the same upward case follows from any regular center.

For such an interior the scalar slope at finite radius obeys
\[
 0<b'_-< f_-(b).
\]
It starts below \(f_-\). At a hypothetical first upward crossing of \(b'-f_-=0\), the constraint gives \(A'=\sqrt{a^{-2}+W_-^2/36}>W_-/6\). The positive sign is fixed by the regular center and \(V_-<0\). The scalar equation then gives \((b'-f_-)'=-4(A'-W_-/6)f_-<0\) at the crossing, excluding it.

If \(b_s\le b_+\), the scalar junction at \(\alpha\ge1\) gives \(b'_+<f_+(b_s)\le0\), again excluding the required exterior. Therefore a candidate has \(b_s>b_+\). It must stay above \(b_+\) and approach it from above, since crossing below with nonpositive derivative cannot be reversed. Its asymptotic derivative is \(-8(b-b_+)/L_+\), while \(f_+(b)=4(b-b_+)/L_++O((b-b_+)^2)\). The derivative follows from the normalizable solution of the scalar equation with \(m_b^2L_+^2=32\). Thus \(b'+f_+<0\) near infinity. At any putative zero of that sum, \(b'=-f_+\) and
\[
 (b'+f_+)'=4(A'+W_+/6)f_+>0 .
\]
Here \(A'>0\) follows from the exterior asymptotics and \(V_+<0\) throughout this region. A nonnegative value cannot then cross downward to the required negative value. Hence at the exterior wall \(b'_+<-f_+(b_s)\).

Now put \(J=A'-W/6\), evaluated separately on the two sides. The constraint and the two slope inequalities give
\[
 J_-<\sqrt{a_s^{-2}+W_-^2/36}-W_-/6
     <\sqrt{a_s^{-2}+W_+^2/36}-W_+/6<J_+ .
\]
The strict middle inequality follows because \(W_->W_+>0\) at the same \(b_s\), and \(\sqrt{a_s^{-2}+w^2/36}-w/6\) decreases strictly with \(w\) at finite \(a_s\). In contrast, the metric junction requires
\[
 J_+-J_-=(1-\alpha)\Delta Q e^{-20b_s/3}/6\le0 .
\]
This excludes the wall. Both slope comparisons and both junction equations include the scalar response. The proof holds at finite flux jump and radius within the indicated truncation. The planar wall has \(a^{-2}=0\), so the strict middle inequality disappears. Localized branes, other scalar trajectories and corrections that change the action are separate problems.

For a general modified tension function \(\tau(b)=2\kappa_5^2T(b)\) with the same bulk theory and charge jump, the same argument excludes a bounce if \(\tau\ge\Delta Q e^{-20b/3}\) for \(b>b_+\), and \(\tau_{,b}\le-(20/3)\Delta Qe^{-20b/3}\) for \(b\le b_+\). The two inequalities come from distinct junctions. A correction evaluated only at the AdS minimum does not test both of them.

## Concentric walls with monotone charge jumps

Let each successive wall increase \(Q\) toward the exterior and have its own \(\alpha\ge1\). The function \(A'\) decreases in the bulk and across each wall. Since it is eventually positive in the exterior AdS region, it is positive everywhere on a candidate geometry. A center below its local vacuum runs toward lower \(b\), and every charge jump raises the local vacuum and lowers \(b'\). Thus the center either has \(Q=0\) or must start above its vacuum, and in either case \(|b'|<f\) holds immediately off the center.

For \(b\) above the local vacuum, the crossings at \(b'=f\) and \(b'=-f\) both point into the strip \(-f<b'<f\): the corresponding derivatives of \(b'-f\) and \(b'+f\) have signs negative and positive, respectively. The strip also prevents \(b\) from reaching the vacuum in finite radial distance because \(f\) vanishes linearly there. At a wall, the outgoing slope obeys \(b'_+<f_+\) by the scalar jump. If \(b\) were at or below the new vacuum, that slope would be negative and all subsequent jumps would keep it on the wrong side. Hence a candidate remains above the new vacuum. By the radial constraint, the strip is equivalent to \(J<\sqrt{a^{-2}+W^2/36}-W/6\) when \(A'>0\). The junction decreases \(J\) or leaves it fixed, and the right-hand side increases strictly as \(W\) drops at the wall. Thus the strip is preserved across the shell as well. Induction takes the strip to the final exterior. A normalizable trajectory above the exterior vacuum instead has \(b'<-f\) near the boundary, so no such stack can satisfy the boundary conditions.

## Near-planar detuning

To see how the obstruction is approached, allow the same tension dependence with \(\alpha<1\) as a diagnostic deformation. The constraint and radial equations give the exact identity
\[
 J'+4A'J=a^{-2}+2J^2-\frac{G}{12}(b'-f)^2.
\]
The leading curvature response for a regular branch tending to the planar wall is obtained by linearizing in \(a_s^{-2}\). At the wall the exterior approaches \(b_+\), giving \(J_+=a_s^{-2}L_+/2+o(a_s^{-2})\). The interior linear equation integrates to
\[
 J_-=a_s^{-2}\int_{\rm interior}^{\rm wall}e^{2(A-A_s)}\,d\xi+o(a_s^{-2}).
\]
Here the integral uses the planar interior, and the regular-center condition removes a homogeneous \(e^{-4A}\) term in the matched expansion. This expansion assumes a regular branch tending to the planar wall.

For \(q_\pm=Q_\pm/4>0\) put the planar shell at the cone coordinate \(r=1\). Its interior has \(e^{4b}=q_-+(q_+-q_-)r^4\), \(e^{2A}=r^2 e^{4b/3}\) and \(d\xi=e^{8b/3}dr/r\). The integral in the last equation is \([q_-/2+(q_+-q_-)/6]/q_+^{1/3}\). Using \(L_+=q_+^{2/3}\) and the wall jump yields
\[
 1-\alpha=\frac{L_+^2}{2a_s^2}+o(a_s^{-2}).
\]
The leading coefficient is independent of the relative charge jump. This expresses the approach to the planar wall from a subcritical deformation of the tension. The deformation is a test parameter and is not supplied by the classical D3 source.

The scalar junction also fixes the first wall displacement. With \(\delta=(q_+-q_-)/q_+\), the interior slope correction is \(b'_--f_-=-\delta L_+/(5a_s^2)+o(a_s^{-2})\) from the radial constraint. The exterior linear relation is \(b'_+-f_+=-12(b_s-b_+)/L_++o(a_s^{-2})\). Combining them gives
\[
 b_s-b_+=-\frac{\delta L_+^2}{40a_s^2}+o(a_s^{-2}).
\]
Thus the wall approaches the exterior vacuum from below along the detuned branch.

For a smooth branch of stationary, renormalized Euclidean actions \(B(\alpha)\), subtracted against the same exterior vacuum, varying \(\alpha\) at fixed charge and boundary data gives \(dB/d\alpha=\Omega_4\,a_s^4 T_c(b_s)\), where \(T_c(b)=\Delta Qe^{-20b/3}/(2\kappa_5^2)\) and \(\Omega_4\) is the unit four-sphere area. The bulk and implicit wall variations vanish on the equations and junctions. The radius law consequently gives the leading conditional asymptotic \(B(1-\epsilon)\sim\Omega_4 L_+^4 T_c(b_+)/(4\epsilon)\). This concerns the detuned stationary branch. Its fluctuation negative-mode count is not determined here.

The [verifier](toe_20261116_D3_spherical_discharge.py) checks the bulk potential and first-order identities symbolically and independently shoots the detuned scalar and metric equations. The interior uses a regular center expansion and the exterior uses the normalizable AdS falloff. At fixed radius the two shooting amplitudes are chosen to match \(b\) and impose the ratio of the two junctions, after which the required \(\alpha\) is computed. The [certificate](../data/toe_20261116_D3_spherical_discharge.json) gives the residuals and a check with more distant numerical boundaries.
