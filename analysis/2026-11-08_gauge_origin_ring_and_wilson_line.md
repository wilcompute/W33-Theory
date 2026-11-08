# Gauge-origin repairs: a closed ring and a continuum Wilson line

This packet tests two concrete ways to replace the previous elementary scalar's unprotected Phi^24 term. The closed gauge ring has a computable invariant-operator lattice and physical fermion mass branches; the continuum model has a complete parity-even KK loop and physical varying eigenmasses. Both supply conditional positive examples, with explicit failures of tempting simplifications. Neither supplies a stabilized Standard-Model-plus-gravity vacuum or a solved TOE.

## Prior ownership and evidence

The previous published vector/quality packet is `8f4f7d2aaf0299f7a94a24eee7c89971b174d916`. The November5 native-boundary report already demonstrates that canonical mediators can admit shorter gauge-invariant breaking operators. Its report was reread, and that warning is applied here. The November5 PQ normalization/cutoff report already owns the July2026 Wilson-line literature intake and very small gauge-coupling calculation for a different, micron-size interval; neither the mechanism nor a tiny coupling is new here.

[Arkani-Hamed–Cheng–Creminelli–Randall, hep-th/0301218](https://arxiv.org/html/hep-th/0301218v2) establishes extranatural Wilson-line protection and the closed-quiver normalization. [Bonnefoy–Dudas–Pokorski1804.01112, sections2.1–2.3](https://arxiv.org/html/1804.01112v2) establishes gauge-quiver operator protection and reduced Goldstone periods. [Fernández Navarro2607.08814, selected gauge-origin/quality sections](https://arxiv.org/html/2607.08814v1) provides recent interval context, not the circle model below. Relevant sections were read, not all of the longer papers. The original extranatural paper's short main text was consulted for its normalization, nonlocal potential and quintessence discussion; its inflationary observational claims are not adopted.

The parity-odd issue was checked against [Closset–Del Zotto–Saxena1812.10451, section2.2](https://arxiv.org/html/1812.10451v2): a five-dimensional Dirac fermion has a mass-sign-dependent Chern–Simons shift. Opposite signed masses cancel those shifts; an integer counterterm/regulator convention still needs specifying. The [weak gravity conjecture](https://arxiv.org/abs/hep-th/0601001) motivates diagnostic scales printed below, not a proved cutoff. No microscopic anomaly/gravity completion is claimed.

Repository searches covered py/json/md/tex and the results index, with stated file-size caps. Standard mechanisms are credited; absence from a search is not priority. Additional full extracted PDF text pages105–108 was read after verifying the unchanged Forty Points hash `003b75482b6584e20e83a55d9e9ba0a181f93b8dff0f94c1d615039c21213cbb`. Personal text coverage is now1–108 of215. These pages describe how extra states and moduli can close apparently successful string constructions. Those census claims were read, not independently reproduced. Full PDF and weekly reading remain unfinished.

## 1. Closed-ring action: the physical coupling scale differs from the loop period

Take U1^N on ring vertices, N canonical complex links Phi_i with charge e_i-e_(i+1) and vev F/sqrt2, and N vectorlike Dirac fermions of charge e_i. Site gauge anomalies cancel between each fermion's two left-handed charge conjugates. Use a positive radial potential and retain both allowed nearest-neighbor chiral hoppings. At translation/reflection-symmetric real equal couplings the actual fermion matrix is

\[
\mathcal M=M I+t e^{i\psi/N}S+t e^{-i\psi/N}S^\dagger,
\quad \psi=\sum_i\theta_i,\quad 2t/M=\epsilon<1.
\]

Its positive singular masses are

\[
m_k=M[1+\epsilon\cos(\psi/N+2\pi k/N)].
\]

Gauge covariance and arbitrary nonuniform link phases with fixed total psi were tested directly. This avoids assuming a forward-only hopping while silently omitting its allowed reverse. Coupling equality, CP phases, absolute scales and N are inputs, not selected by W33.

Integrating out gauge directions in the canonical kinetic metric gives

\[
f_{\rm loop}=\left(\sum_iF_i^{-2}\right)^{-1/2}=F/\sqrt N,
\qquad \phi=f_{\rm loop}\psi,
\qquad f_{\rm mass}=Nf_{\rm loop}=\sqrt N F.
\]

The full spectrum is periodic under psi->psi+2pi, which permutes k. An individually occupied eigenbranch can vary on the longer scale f_mass. Conflating this branch scale with the fundamental loop period would incorrectly exclude or endorse parameter choices. Actual matrices up to N=300, a constrained kinetic minimization and independent server arithmetic check the distinction.

The ring retains a massless diagonal U1 vector. Consequently this action cannot automatically inherit the previous packet's heavy-vector-only transport with closed two-vector annihilation channels. Giving that vector a mass, choosing production and checking additional annihilations require a specified extension. No such extension is included in the passing ring scalar inventory.

## 2. Complete scalar monomials, rather than one selected operator

For ring incidence B, Bz=0 over integers implies z_i=z_(i+1), hence z=m(1,...,1). Every phase-dependent scalar monomial is therefore a positive winding power of product(Phi_i), multiplied by arbitrary radial powers product(|Phi_i|^(2k_i)), or its conjugate. The lowest degree is N. This is a complete statement for the specified link-scalar inventory, not for arbitrary added fields.

Let u=F^2/(2Lambda^2), v=u^(N/2), and suppose every dimensionless coefficient of these scalar monomials has magnitude at most1 at cutoff Lambda. At fixed radial vevs, summing absolute curvatures over all windings m>=1 and radial insertions k_i>=0 gives the sufficient bound

\[
\max|V''|\le {2\Lambda^4\over f_{\rm loop}^2}
{1\over(1-u)^N}\,{v(1+v)\over(1-v)^3},\qquad u<1.
\]

The radial factor comes from N geometric series; the winding factor from sum(m^2 v^m). An independently differentiated generating potential and server partial sums verify the expression. It is stronger than checking the first monomial alone, but depends explicitly on the coefficient bound, cutoff and fixed radial vacuum. It does not calculate unknown quantum-gravity coefficients or bound all derivative/fermionic operators.

| N | f_mass/MP | supplied cutoff | log10 leading curvature/H0^2 | log10 all-scalar bound/H0^2 |
|---:|---:|---|---:|---:|
|24|1|MP|103.34|103.56|
|110|1|MP|-4.00|-3.78|
|850|1|MP/sqrt(N)|-7.18|248.69|
|300|0.15|MP/sqrt(9N)|-28.70|-14.79|

Thus a leading-only pass can fail the bounded scalar-tower screen. The species estimate Lambda=MP/sqrt(nu N) is an external sensitivity hypothesis, not an exact gravitational threshold. With cutoffMP and f_mass=MP, the first all-scalar bound below0.01H0^2 occurs at N=109. At f_mass=0.15MP, nu=9 moves that sufficient threshold to272. No passing bound up to N=2000 is asserted as a universal impossibility beyond the scanned range.

For this linear cosine fermion spectrum, cyclic sums cancel phase-dependent Taylor terms below degreeN. Expanding (1+z)^4 log(1+z) yields |c_j|=24/[j(j-1)(j-2)(j-3)(j-4)] for j>=5. Since |d_theta^2 cos^j(theta)|<=j^2 and |c_j|j^2 decreases, the complete one-loop fermion contribution obeys

\[
{\max|V_f''|\over H_0^2}\le
{M^4N^3|c_N|\epsilon^N\over8\pi^2 f_{\rm mass}^2H_0^2(1-\epsilon)}.
\]

This is a conservative all-phase bound for the declared symmetric fermion matrix, not an all-orders proof. Tiny Yukawas, site/radial stability, extra portals and the common gravitational vacuum energy remain unexplained. If complementary path mediators X,Y are added, their charges sum to zero and mu^2 XY is allowed at canonical degree2. Its physical amplitude depends on their vevs and matching scale; degree alone is insufficient. This repeats the November5 full-inventory lesson rather than claiming a new general no-go.

## 3. A continuum alternative with physical KK eigenmasses

On a supplied flat circle of radius R, take a five-dimensional U1 gauge field and a pair of same-charge periodic Dirac fermions with bulk masses +M,-M. The parity-even potential is twice the single-Dirac result. Opposite mass-sign CS shifts cancel; an allowed integer counterterm/regulator convention is chosen for the remaining offset. All global/topological and UV questions are not thereby settled.

With theta=integral(A5 dy), phi=f theta and f=1/(2pi Rg4), physical eigenmasses are

\[
m_n^2=M^2+{(n+q\theta/(2\pi))^2\over R^2},\quad n\in\mathbb Z.
\]

These are genuine Dirac singular masses. Large gauge shifts relabel n; they do not invalidate fixed-mode particle states. The complete single-Dirac parity-even nonlocal loop is

\[
V_{\rm nl}={3\over16\pi^6R^4}\sum_{l\ge1}
{e^{-x_l}(1+x_l+x_l^2/3)\over l^5}\cos(ql\theta),
\quad x_l=2\pi lMR.
\]

It follows from a Schwinger proper-time representation, Gaussian momentum integration and Poisson summation. The theta-independent local divergence is subtracted; the cosmological constant is not computed. Positive proper-time quadrature, closed half-integer Bessel form, polylogarithmic curvature sums and independent server Simpson integration agree. A naive finite KK truncation is not used as a gauge-invariant UV calculation.

## 4. Supplied window, and the population/density boundary

Choose M=16keV, MR=12, q=1 and f=0.01MP. Then R=1.480e-10m, KK spacing=1.333keV and g4=8.715e-24. The parity-paired loop curvature is bounded by3.52e-6H0^2. An initial ground-band n=0 mode at theta=-3.01782 has physical mass16012.81eV and local beta=-MP*dlog(m)/dphi=0.053.

At fixed f=0.01MP, the joint conditions of loop curvature below0.01H0^2 and that local beta on an initial ground band allow 10.76969<MR<12.24321. This is a window for two diagnostics, not an allowed cosmological parameter region. The input mass, coupling, radius and phase are not derived constants.

Three independent limitations are decisive:

* **Population relaxation:** the instantaneous lightest KK band has at most log(m_max/m_min)=0.5log[1+1/(4(MR)^2)]=0.0008673 variation. A fixed branch can vary more but needs a real occupation/conversion history. On the chosen fixed branch, an illustrative displacement0.01MP already changes beta to0.0355; at0.3MP it becomes-0.421. A constant-coupling fit cannot simply be imported.
* **Charged inventory:** one additional tower of bulk mass1.6keV at the same R contributes about10^21.86H0^2 to the parity-even curvature. A massless charged tower gives about10^23.78H0^2. Nonlocal protection requires checking the full charged spectrum, not only the selected heavy field.
* **Finite density:** with one occupied branch and supplied Omega_DM=0.26, n*m(phi) has positive curvature1.368H0^2 at the initial point, even though the vacuum loop is tiny. The phase-dependent loop energy is only1.17e-10 of3MP^2H0^2. Neither late-time scalar evolution nor the observed DE density follows from the vacuum-loop calculation.

Flat Einstein reduction gives M5 about1.08e10GeV; the diagnostic g4 MP is21.22keV, only1.33 times the bulk mass. That is not a large UV separation under that conjectural cutoff estimate. Radius stabilization, magnetic objects, other charged UV fields, boundary sectors and nonlocal gravitational effects remain open. The circle is an assumed geometry, not a derived spacetime or a gravity solution.

## Validation and next physical requirement

The receipt records37 focused tests, both producers, actual N=300 matrix checks and independent server calculations. The prior vector-conversion model's tests are included; its thermal solution is not reused for a different action. Incoming sign-fit and native E6/weighted-walk/Hodge/optical commits are reviewed separately in the intake record; stored likelihoods are not rerun here.

The next necessary object is a common action with a full charged/mediator inventory and a dynamical radius, followed by a population-plus-scalar solution. A scalar quality screen, a physical mass derivative and a small vacuum loop are three distinct checks. This packet makes them explicit and tests them; it does not substitute them for the missing universe.
