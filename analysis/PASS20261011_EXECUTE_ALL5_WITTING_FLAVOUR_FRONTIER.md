# 2026-10-11 — Execute-all-five Witting/flavour frontier

Producer: `analysis/w33_20261011_execute_all5_witting_flavour_frontier.py`
Certificate: `data/w33_20261011_execute_all5_witting_flavour_frontier.json`

This packet executes the five independent targets opened by the Witting-displacement firewall. It begins from the
published Pass 11923 result that the common qutrit Yukawa
\[
Y_u(h)_{ab}=h_{a+b}g_{a-b},\qquad g_+=g_-,
\]
remains charm–up locked at every Delta(54)-symmetric Higgs vacuum and needs a magic/non-stabiliser Higgs to unlock.
The results below do not claim a completed Standard Model or TOE.

## 1. The flavour Higgs and Witting tangent have the same physical H27 module

At the Witting reference ray, Pass 11664 gives the transverse triplet matrices
\[
X=\begin{pmatrix}0&0&1\\1&0&0\\0&1&0\end{pmatrix},
\qquad
Z=\operatorname{diag}(1,\omega,\omega^2),\qquad ZX=\omega XZ .
\]
They are exactly the restrictions of SUM01 and CZ on the physical Witting tangent/mass kernel.

For the Pass 11921 flavour-qutrit Yukawa map
\[
\Phi(h,g)_{ab}=h_{a+b}g_{a-b},
\]
direct substitution gives
\[
\Phi(Xh,g)=X^\dagger\Phi(h,g)X^*,\qquad
\Phi(Zh,g)=Z\Phi(h,g)Z .
\]
Thus, after the displayed class conventions are fixed, the identity map on \(\mathbb C^3\) is a phase-resolved
intertwiner between the flavour-Higgs qutrit and the Witting transverse qutrit for the actual \(H_{27}\) action.
There is a sharp distinction at the larger little group. The tensor-cube fixed spaces are
\[
\dim(3^{\otimes3})^{H_{27}}=3,\qquad
\dim(3^{\otimes3})^{G_{25}}=0,
\]
while \(3\otimes\bar3\) has one invariant for both groups and \(3\otimes3\) has none. Therefore an H27-preserving
qutrit cubic can itself be a source of the larger \(G_{25}\) breaking required by the displacement firewall.

Pass 11900 supplies the projective completion.  Enumerating its charged-class modular image and the Witting
\(G_{25}\) image in the displayed basis, with projective matrices canonically normalised and compared at tolerance 1e-9,
gives two 216-element sets with intersection 216 and both set differences empty.  Thus the computed identity
intertwiner extends from \(H_{27}\) to the entire projective one-qutrit Clifford/Hessian group:
\[
\mathbb P G_{25}=\operatorname{Cliff}_1(3)
\]
as the same matrices in this basis.  The remaining distinction is only the choice of scalar lift/centre.

## 2. The invariant bifurcation is a competing-harmonic problem

The bosonic Coleman–Weinberg selector has an isotropic positive six-real-dimensional tangent Hessian at a Witting ray,
numerically
\[
\kappa_{\rm CW}=7.2110956\ldots .
\]

The earlier displacement firewall already showed that no G32-invariant scalar has a linear projective force there.
The stronger local statement uses the G25 tangent invariant degrees \(6,9,12\). If a homogeneous ambient invariant
\(I_d\) is nonzero at the ray, then after unit normalization
\[
\frac{|I_d(t)|}{|I_d(0)|}
=(1+\|t\|^2)^{-d/2}\,[1+O(t^6)] .
\]
A single complex term \(2\operatorname{Re}(\kappa_d I_d)\), after the physical common 84 phase relaxes, is
\(-2|\kappa_d I_d|\). Its quadratic projective contribution is positive. A lone \(I_{12}\) therefore stabilises,
rather than bifurcates, the Witting ray.
A projective instability can nevertheless be produced by competing phase harmonics. Write
\(A_d=2\operatorname{Re}(\kappa_d I_d(r)e^{id\phi_*})\) at a common-phase stationary point. Locally,
\[
m_\phi^2=-\sum_d d^2 A_d,\qquad
m_T^2=\kappa_{\rm CW}-\sum_d dA_d .
\]
For the explicit dimensionless witness
\[
A_{12}=3,\qquad A_{18}=-\frac32,
\]
one gets
\[
m_\phi^2=54>0,\qquad
m_T^2=7.2110956-9=-1.7889044<0 .
\]
So the minimal invariant route is not “I12 nudges the vacuum”; it is competition between at least two phase harmonics
(or another phase-fixing sector).

The Witting point also has the expected Coleman–Weinberg nonanalyticity. Along a displayed tangent, its 24 zero vector
modes split at leading order as
\[
0^4,\qquad (t^2/3)^{18},\qquad (t^2)^2,
\]
so \(\sum a_i^2=4\) and
\[
F(t)=F(0)+\frac12\kappa_{\rm CW}t^2+4t^4\log(t^2)+O(t^4).
\]
Consequently a Landau analysis at a spinodal must retain the logarithm; an ordinary quartic Taylor fit is invalid.
## 3. The existing E8 cubic is a surjective tangent source — but only through non-Cartan matter

In the heterotic \(T^6/\mathbb Z_3\) realisation, the exact untwisted superpotential is the E8 bracket
\[
W=g\,\epsilon^{ijk}\langle X_i,[X_j,X_k]\rangle,\qquad [x,y]=*(x\wedge y).
\]
At the Witting vacuum \(X_1=v,\ X_2=X_3=0\), the \(X_2\)-\(X_3\) mass matrix has rank 56 and a 28-dimensional kernel.
Removing the modulus leaves the actual massless 27 of Pass 11893.

Project the cubic of two vectors in that 27 onto the three complex Cartan-tangent directions transverse to \(v\):
\[
S_j(y,z)=\langle T_j,*(y\wedge z)\rangle .
\]
The resulting map \(\Lambda^2(27)\to\mathbb C^3\) has rank three, with all three nonzero singular values
\[
2\sqrt6 .
\]
Thus the declared gauge-invariant E8 cubic can source every Witting tangent component.

But three Cartan-tangent legs give zero identically: the Cartan is abelian. Therefore the source needs non-Cartan
backgrounds. In the tested heterotic trinification sector, Pass 11893 identifies this massless 27 as the coloured
\((3,3,3)\). Giving it a background is not an SM-preserving implementation. The source exists algebraically and
gauge-invariantly, but the current heterotic vacuum supplies it in the wrong physical representation.
## 4. CKM/PMNS need local adjoint perturbations, not another scalar anisotropy

Pass 11922 showed that CKM and PMNS are the left and right Schmidt bases of one two-qutrit theta state and that a
scalar modulus anisotropy moves them together. This packet perturbs the frozen best joint point independently by local
qutrit adjoints,
\[
Y\longmapsto U_LYU_R^\dagger,\qquad
U_L=e^{i\epsilon_L\lambda_a},\quad U_R=e^{i\epsilon_R\lambda_b}.
\]

At the frozen Pass 11922 point \(t=1.2877557,\ \beta=0.8087233\):
* baseline CKM proxy distance: \(0.74404\);
* baseline PMNS proxy distance: \(0.49997\);
* one left-adjoint direction lowers CKM distance to about \(0.25281\) while leaving the right marginal unchanged;
* one right-adjoint direction lowers PMNS distance to about \(0.32709\) while leaving the left marginal unchanged;
* applying both keeps both improvements simultaneously;
* the down and charged-lepton singular values are unchanged to \(10^{-16}\).

The missing tangent representation is therefore
\[
(8,1)\oplus(1,8)
\]
under the two local qutrit \(SU(3)\) factors, rather than another scalar \((1,1)\) modulus. This is a representation
target for the compactification/spurion sector, not yet a derived geometric operator. Pass 11923's magic-Higgs theorem
is complementary: a non-stabiliser qutrit is needed in the up sector; here the two-qutrit state additionally needs
independent adjoint marginal rotations. Representation-theoretically the two requirements fit: for a qutrit spurion
\(h\), the traceless bilinear \(hh^\dagger-\|h\|^2\mathbf1/3\) lies in the adjoint because
\(3\otimes\bar3=1\oplus8\). A magic spurion on each W(3,3) qutrit factor therefore has exactly the bilinear
representation content \((8,1)\oplus(1,8)\) required by the marginal test. No coefficient or compactification
mechanism for those bilinears is derived here.

## 5. The heterotic untwisted matter spectrum is locked to the gauge spectrum

Let \(D_x:\mathfrak g_0\to\mathfrak g_1\) be the gauge-orbit derivative
\(D_x(a)=[a,x]\), and let \(M_x:\mathfrak g_1\to\mathfrak g_2\) be the untwisted matter mass map
\(M_x(y)=[x,y]\) in the \(\mathbb Z_3\)-graded presentation
\(E_8=\mathfrak g_0\oplus\mathfrak g_1\oplus\mathfrak g_2\) with
\(\mathfrak g_0=\mathfrak{sl}_9\), \(\mathfrak g_1=\Lambda^3\mathbb C^9\).
On the D-flat Cartan slice \([x^\dagger,x]=0\).  Invariance of the Hermitian/Killing form identifies the adjoints, and
Jacobi gives the exact Laplacian identity
\[
M_x^\dagger M_x-D_xD_x^\dagger
=\operatorname{ad}_{[x^\dagger,x]}\big|_{\mathfrak g_1}=0 .
\]
The code checks the repository's concrete matrix conventions at the Witting and a generic Cartan point with relative
residuals below \(3\times10^{-16}\).  The full antisymmetric-tensor norm used in the vector mass computation is six
times the sorted 3-form coordinate norm. Hence the nonzero spectra obey, throughout this D-flat Cartan slice,
\[
m_{\rm untwisted}^2=\frac16\,e_{\rm vector}.
\]

At a Witting ray the matter operator has 28 zeros and 56 nonzero modes, while the vector operator has 24 zeros and
56 nonzero modes. At a generic Cartan point the matter operator has four zeros and the vector operator none, with
80 matched nonzero eigenvalues.

This collapses the untwisted-matter moduli dependence onto the same spectral selector as the gauge sector, up to
couplings, statistics and additive radial terms. It does not rescue the physical vacuum by itself:
* Pass 11892's exact N=1 chiral-84 + gaugino completion cancels the one-loop flat-direction potential;
* a negative soft scalar mass selects Witting/trinification, a positive one selects the C10 point;
* the declared fermion-dominated regime runs toward a cusp;
* the 27 twisted \(\bar9\) copies are massless at this tree-level Witting vacuum in Pass 11893 and do not yet supply an
  \(x\)-dependent determinant there.
A complete off-shell effective-potential claim still needs a declared gauge, Goldstone/ghost inventory and
renormalisation prescription. Nielsen identities guarantee the appropriate gauge-independence statements at physical
stationary points, not an arbitrary off-shell background potential. The robust repository statement is therefore:
**the bosonic 40-ray selector is a controlled sandbox result; the exact supersymmetric heterotic completion is flat at
one loop, and Witting selection requires a specified SUSY-breaking supertrace imbalance.**

## Synthesis

All five targets point to the same missing dynamical object.

The flavour side says that a realistic up sector needs a magic, Delta(54)-breaking Higgs. The vacuum side says a
symmetric G32 correction cannot nudge a Witting ray, while H27-preserving cubics can break G25. The actual E8 cubic
can source the complete Witting tangent, but in the tested heterotic model it does so through coloured non-Cartan
matter. The mixing side says the shared theta state needs local adjoint perturbations. And the loop side says the
supersymmetric completion erases the bosonic selector unless SUSY breaking is specified.

The sharp next construction problem is therefore not another free parameter scan: find a gauge-safe
Delta(54)/G25-breaking sector whose low-energy qutrit spurion is magic, whose bilinears generate the required local
adjoints, and whose supertrace gives the sign that retains the Witting vacuum.
