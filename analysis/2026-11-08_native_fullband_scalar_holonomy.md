# A scalar holonomy potential from the full native 135-link graph

This continuation replaces a previously supplied ingredient with an explicit calculation: one charged complex scalar on the actual native periodic graph generates a stable Wilson-holonomy potential. All27 matter bands are retained. Compactification, scalar inventory, bare mass and microscopic units remain supplied. This is a free-matter contribution at fixed background, not a selected universe or a solved TOE.

## Prior owners

Pass11991 and w33_pass12189_12193_five_bridges.py own the primitive four-period cover,27vertices,135edges and acoustic metric. The October27 native propagation report owns the harmonic electric metric M and an engineered common leading gauge cone. The October28 three-mixed-loop report compresses that magnetic completion; it does not generate a compactification potential.

The October27 acoustic vacuum-density report already computes a full-Fock **spinless fermion thermal** harmonic response. Pass12029 already computes full-native heat-trace variations and independent lifted real-space checks. These are predecessors, rather than this vacuum trace-square-root calculation for a relativistic complex scalar. The November8 five-boundary-bridges source supplies a compact Wilson scalar mass to illustrate a two-vector-plus-one-scalar splitting. The preceding gauge-origin packet528571d775996d14b71f2359e707378f3db659bc derives a continuum Dirac Wilson potential for a separately assumed flat-circle spectrum.

Here the matter Laplacian uses literal native edges and integer voltages. No continuum spectrum or independently supplied quadratic mass is presented as derived from the graph.

Standard method: [Kan–Shiraishi2212.07049, introduction and sectionII](https://arxiv.org/html/2212.07049v2#S2) treats twisted graph Laplacians, heat traces and scalar holonomy potentials on cycle graphs. Only those sections were read; no UV-modified-propagator prescription is adopted. [Ponton–Poppitz0105021](https://arxiv.org/abs/hep-ph/0105021) gives established Casimir/radius-stabilization context; its abstract was consulted here. The repo's October27 massive-field work already owns a supplied-spectrum AdS radius minimum. Stable holonomy does not solve the radius problem.

Result-specific searches covered the results index, analysis py/md, certificates and manuscript tex with stated file-size caps. Standard methods and coincident integers do not establish novelty.

## Declared action and full-band energy

For one charge-one complex scalar, take continuous time, canonical temporal kinetic term, bare mass m>0 and unit nearest-edge hopping:

\[
S_\chi=\int dt\left[\sum_{x,v}(|D_t\chi_{x,v}|^2-m^2|\chi_{x,v}|^2)
-\sum_{e=(a,b)}|e^{ia_{x,e}}\chi_{x+V_e,b}-\chi_{x,a}|^2\right].
\]

The spatial operator is H(k)=D(k)†D(k), where D_ea=-1 and D_eb=exp(i k.V_e). The actual10-regular graph gives H=10I-A. **Assume** L cells compactify the fourth primitive period with total holonomy theta, so k4=(2pi n+theta)/L for n=0,...,L-1.

Per noncompact three-cell the complex-scalar vacuum-energy difference is

\[
\Delta V(\theta)=\int_{\mathrm{BZ}_3}\frac{d^3k}{(2\pi)^3}
\sum_{n=0}^{L-1}\sum_{j=1}^{27}
\left[\sqrt{m^2+\lambda_j(k,(2\pi n+\theta)/L)}
-\sqrt{m^2+\lambda_j(k,2\pi n/L)}\right].
\]

A complex field has two real oscillators, hence coefficient1 rather than1/2. Subtracting theta-independent energy does not explain the cosmological constant. Full-spectrum2pi periodicity follows by compact-momentum relabeling. Integer vertex-cell changes give diagonal-unitary-conjugate Bloch matrices. An independently assembled lifted real-space graph with boundary twist reproduces the complete Bloch spectrum.

## Exact stability and a literal winding witness

The heat kernel expands as exp(-10t)exp(tA). Every oriented walk has positive weight before its holonomy phase. BZ3 integration keeps zero noncompact period, and the compact momentum sum keeps fourth period a multiple of L. Opposite orientations pair with nonnegative coefficients. The trace-square-root proper-time representation yields

\[
\Delta V(\theta)=\sum_{w\ge1}c_w(1-\cos w\theta),\qquad c_w\ge0.
\]

This standard positive-walk argument applies to this operator, not arbitrary fermions, twists or interacting theories.

The certificate walks native edges6+,32-,19-,1-,0+,12+,53+,4-. This eight-edge based walk returns to vertex0 with primitive period(0,0,0,1). Repeating it L times gives one compact winding and zero noncompact period. Thus c1>0: theta=0 modulo2pi is the unique global minimum of this scalar contribution and V_theta_theta(0)>0.

Keeping only the forward/reverse walks based at vertex0 in each compact cell gives

\[
\boxed{V_{\theta\theta}(0)\ge
\frac{L\,\Gamma(r-\frac12)}
{\sqrt{\pi}\,r!\,(10+m^2)^{r-\frac12}}>0,\qquad r=8L.}
\]

All omitted coefficients are nonnegative. The walk is not claimed shortest. This analytic formula is exact; printed logarithmic values use ordinary floating arithmetic.

## Native electric normalization

The prior harmonic Gram is

\[
M=\begin{pmatrix}10&5&-6&0\\5&10&0&-6\\-6&0&12&-6\\0&-6&-6&12\end{pmatrix}
=\begin{pmatrix}A&b\\b^T&12\end{pmatrix}.
\]

Completing the kinetic square gives A^-1 b=(0,-3/5,-1/2) and Schur complement12-b^T A^-1 b=27/5. Redefining the noncompact vector coordinates decouples the scalar kinetic term. With microscopic link coefficient1/g², theta=L A4 and L compact cells,

\[
\boxed{f_\theta^2=\frac{27}{5g^2L}},\qquad
m_\theta^2=\frac{5g^2L}{27}V_{\theta\theta}(0).
\]

The single-scalar mass formula requires the infinite noncompact-volume limit, where constant noncompact connections only shift the BZ integral. On a finite noncompact torus all four holonomies are physical and their potential can mix: a genuine pole spectrum requires the full four-variable Hessian. These are supplied-action lattice-unit normalizations. Neither g,L, physical spacing nor a measured mass is predicted. Under the additional common leading-metric assumption, completing the spatial momentum square gives compact coefficient1/5 and effective radius sqrt(5)L/(2pi). That is a leading-symbol matching statement, not a full-band relativistic identity.

The loop provides a periodic gauge-invariant contribution in place of an independently assigned local theta² term. It does not select the engineered cone, explain dimensional reduction or identify electromagnetism.

## Numerical checks and limits

For X=U†H'U,Y=U†H''U and omega=sqrt(m²+lambda), the implemented curvature is

\[
E''=\sum_a\frac{Y_{aa}}{2\omega_a}
-\sum_{ab}\frac{|X_{ab}|^2}
{2\omega_a\omega_b(\omega_a+\omega_b)}.
\]

This expression stays finite at degeneracies. Independent five-point energy differences check it.

At m=0.8,L=2, the12³-grid curvature is0.000692312 in lattice units; the8³-to12³ relative change is0.0000878. At g=1 its single-holonomy normalized curvature is0.000256412. This is a diagnostic, not an asserted finite-torus pole mass. At m=0.3,L=6, the change is54%, so its12³ value is not a converged infinite-volume result. Additional20³/28³ controls are stored in the certificate.

An unshifted Bloch grid is exactly a finite noncompact torus. Extra winding walks alias infinite-volume coefficients; positivity survives, coefficients change. The same nonnegative-walk expansion gives an analytic one-sided comparison: each finite-torus coefficient is at least its infinite-volume value, hence V_theta_theta_infinite(0)<=V_theta_theta_N(0) and DeltaV_infinite(theta)<=DeltaV_N(theta). If N2 is divisible by N1, the allowed winding set shrinks, so these upper bounds decrease. Independent2-to4 and3-to6 cover controls test that consequence. The analytic relation concerns exact finite-torus quantities; printed floating values have no certified roundoff interval. Adjacent-grid differences remain diagnostics, not rigorous error bars.

The actual independent server uses64-term complex matrix powers in the binomial series for sqrt(19I-A), with m=3,L=2 and a2³ grid. It retains all27 bands without an eigensolver. Its theta=pi difference is0.00003195169677; five-point curvature is approximately0.00001607725. The analytic series-tail bound is2.05e-19 per three-cell; floating roundoff and differencing error are separate and larger.

## Evidence and missing physics

The receipt records22 focused controls, literal winding, exact Schur identity, independent lifted-graph assembly, changed voltage gauge, periodicity, positive-walk lower/upper comparisons, proper-time bound integral and actual server matrix series. The scalar loop is a model calculation, not evidence that this scalar exists.

Three incoming patches were read in full through5200a426cf184ae8fcb22d1f549a17cf89a1205d. Correction239eba0af4e188c2358cd7d6ff0893b25c9f1424 retracts S7's low-redshift-penalty explanation: stored high/mixed covariance blocks carry the penalty. KLT predictive rows remain provisional and width-sensitive. CLASS fits and posterior draws were not rerun here. The preceding native19-test receipt checked finite models and frozen-record integrity, not a successful cosmological forecast.

Full extracted manuscript pages109–112 were read; page110 was reread after output truncation. The unchanged PDF hash is003b75482b6584e20e83a55d9e9ba0a181f93b8dff0f94c1d615039c21213cbb. Personal text coverage is1–112 of215. String-vacuum, flavour and selection-rule claims there were read, not independently re-proved. Full weekly and manuscript reading remain unfinished.

Missing ingredients: complete charged fermion/scalar content, quantum gauge corrections, compactification/spacing selection, radius dynamics, physical chirality, scalar populations, observed cosmology, gravity and vacuum-energy control. Extra fields or twists can move or remove this scalar-only minimum.

Five independent next investigations:

1. Bound finite-volume winding errors analytically.
2. Construct an anomaly-compatible charged Dirac operator on the same native cover.
3. Couple holonomy to a dynamical radius with the complete matter inventory.
4. Solve finite-density evolution for actual mass eigenstates of a common action.
5. Test induced interacting gauge response before identifying a physical photon.
