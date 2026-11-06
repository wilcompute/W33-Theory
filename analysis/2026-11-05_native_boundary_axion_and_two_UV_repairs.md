# A native boundary axion and two UV repair attempts

This continuation turns W33 incidence data into a declared particle EFT: complex link scalars, explicit gauge transformations, a bounded scalar potential and a single relative boundary phase. The restricted scalar inventory can pass a leading quality screen after refinement. Two explicit renormalizable extensions then expose the missing protection. This is progress toward a common physical model, not a solved TOE or a viable completed axion theory.

The gauge quiver is internal to a supplied four-dimensional spacetime. It does not derive spacetime, the Higgs scale, gauge couplings or gravity.

## Prior ownership and new use

The following mathematics is already established in this repo and is used as input:

- **BT545-BT547:** the 80-vertex, 160-edge Levi graph; 1,620 oriented apartments; the exact cycle projector `C C^T = 160 Pcycle`, with rank81. Producer: `w33_levi_kirchhoff_cycle_projector.py`; its actual certificate was reread.
- **BT742/744:** the irreducible Steinberg cycle module and apartment spanning. A full-symmetry quadratic potential cannot select one zero mode inside that irreducible81-sector. This is an application of the prior representation result, not a new Schur theorem.
- **Pass5089:** integral apartment generation and torsion-free cycle presentation. **5396-5401:** the all-q tight-frame theorem; its actual certificate was reread.
- **4040/4044:** resistance at Levi distance four is exactly7/10. The full reports were read; this value is not rediscovered here.
- **2026-11-03 sparse apartment Hamiltonian:** a selected cycle basis can preserve the divergence constraint while breaking full symmetry. Its optical Hamiltonian is distinct from the scalar potential constructed here.

Extra-dimensional and deconstructed axions are established mechanisms. [Hor, Nakai, Suzuki and Xu2606.02728, sections3.1 and5.2](https://arxiv.org/abs/2606.02728) provide recent gauge/phase and boundary-breaking context. [Bonnefoy2212.00102](https://arxiv.org/abs/2212.00102) explains why adding heavy mediators requires a fresh quality audit. [Cheung1003.0941](https://arxiv.org/abs/1003.0941) owns the general colored-determinant obstruction used in the preceding packet. Those mechanisms are credited prior art; the calculations below concern this specified native inventory.

## 1. A boundary mode with an explicit positive potential

Put one complex field `Phi_e=(F/sqrt2) exp(i theta_e)` on each oriented Levi edge and gauge the vertex U(1) factors. Gauging all vertices eats79 independent phases and leaves the known81 cycle modes. Instead omit the gauge fields at two distance-four vertices, u=0 and v=4 in the canonical constructor. The remaining78 gauge generators are independent, so there are **82 physical phases**.

For an apartment, let Pplus multiply the link fields whose oriented cycle coefficient is+1, and Pminus multiply those with coefficient-1. Both products transform identically because `B C=0`. Therefore the potential

\[
V=\sum_e\lambda_e(|\Phi_e|^2-F^2/2)^2
 +\sum_A\frac{|P_{A,+}-P_{A,-}|^2}{\Lambda_c^{8s-4}}
\]

is gauge invariant and nonnegative. Here s=1 on the native graph, or s is the uniform edge subdivision factor. Each half-product has4s factors. Equal link magnitudes and flat cycle phases are exactly stationary zero-potential minima. This avoids the unbounded large-field potential that a negative high-degree cross term alone would produce.

The81 cycle modes are lifted locally, leaving one boundary Goldstone. The primitive phase is `psi=phi[v]-phi[u]` on the cycle-flat sheet `theta=B^T phi`; an oriented u-v path has precisely phase psi. Integral apartment generation ensures that this is a primitive2pi phase rather than an unnoticed multiple winding.

Let h be the exact unit-current flow between u and v. The producer obtains it by a rational polynomial inverse of the native Laplacian and checks Kirchhoff's law in every row. With R=7/10, `||h||²=R`, and the unit-phase representative is h/R. Consequently

\[
f_a=F/\sqrt R
\]

if a supplied QCD coupling has anomaly one. This is a kinetic normalization derived from the declared action, not a numerical dimension identified with a mass. The attempted fermion completion below realizes anomaly one only when an additional gauge-allowed mass is set to zero.

## 2. Refinement, shortest paths and the missing gap

Uniformly replace each native edge by s links and s-1 new gauge sites. There are `80+160(s-1)` vertices,160s scalar links, and `78+160(s-1)` gauged interior factors. The cycle rank stays81; the relative phase count stays82. This is subdivision, not the signed2-lift already obstructed in Pass4173.

The boundary resistance becomes `R_s=7s/10`. Every shortest boundary path has4s links, and **four** such paths exist. After cycle locking, all four carry the same primitive phase. For supplied fa=1e11GeV, set `F=fa sqrt(7s/10)` and examine unit coefficients in `-2 Re(product Phi/MP^(4s-4))`, with MP=2.435e18GeV and chi=(0.0756GeV)^4.

| s | Leading degree | Four coherent shortest-path amplitudes / chi | Leading screen |
|---|---|---|---|
|1|4|3.0001e48|Fails|
|2|8|1.6726e19|Fails|
|3|12|2.6555e-10|Fails the phase-uniform1e-10 bound|
|4|16|8.3184e-39|Passes under the stated scalar assumptions|

One s=3 path alone would pass that bound; the path multiplicity changes the screen. The s=4 inventory has **640 link scalars and558 gauged U(1) factors**, with F=1.6733200530681512e11GeV. These additions and the absolute scale are inputs, not predictions or a preserved original D+Q+Q unification fit.

The single-phase screen presumes the other81 modes are locked above QCD. If their cycle interactions are suppressed only by MP, the s=4 cycle mass is approximately **2.1430e-77 times the nominal single-mode QCD mass sqrt(chi)/fa**. They cannot then be integrated out; this comparison is not the full mixed82-mode QCD spectrum. Taking Lambda_c=F in the positive potential instead gives a link-only quadratic gap approximately **0.13975F**. This is a declared lower matching scale requiring mediators, not an automatic consequence of subdivision. Higher operators, arbitrary Wilson coefficients, complete thresholds and cosmology remain uncomputed.

## 3. Colored anomaly-sector attempt: a gauge-allowed closing mass

On a boundary path with L links, introduce L color-fundamental Dirac pairs. For link i, Qi has charge-1 at its head vertex and Qbari has charge+1 at its tail. Endpoint gauges are absent. Every interior site has one color triplet and one color antitriplet with opposite U(1) charges and hypercharges, so all gauge and mixed gravitational anomalies cancel site by site.

The renormalizable terms are `yi Phi_i Qi Qbari` and `Mi Qi Qbar_(i+1)`. With no closing mass, PQ assignments

\[
PQ(\Phi_i)=1/L,\quad PQ(Q_i)=-i/L,\quad PQ(\bar Q_i)=(i-1)/L
\]

preserve those terms and give color anomaly magnitude one. But **mu Q_L Qbar_1 is gauge invariant** because both endpoint fields are neutral. It breaks this PQ symmetry. Setting it to zero requires additional protection or a justified locality assumption.

This extends beyond the particular interior charges. For any added ordinary Abelian protection, keeping all Mi as gauge-neutral constants implies `X(Qbar_(i+1))=-X(Qi)`. Thus

\[
\sum_iX(Q_i+\bar Q_i)=X(Q_L)+X(\bar Q_1).
\]

If other sectors have zero mixed color anomaly, anomaly cancellation forces the closing mass neutral. Colorless additions cannot change it. Extra colored sectors, charged mass spurions or inflow change the hypotheses; no general no-go for deconstructed axions follows.

The mass determinant is `product(yi Phi_i)+(-1)^(L-1) mu product(Mi)`. The producer compares exact cyclic-matrix singular values with an analytic Fourier expansion of the color-triplet Dirac Coleman-Weinberg potential. At L=16, `Mi=mu=F`, and `yi Phi_i/F=exp(i psi/L)/sqrt2`, its first harmonic has amplitude **4.9196073224e-7 F^4**, or **1.18075e43 chi** at the link benchmark. A free complex closing phase shifts this potential. This is an allowed, generically misaligned source, not a prediction of theta for every CP choice. The mu=0 control has phase-independent singular values.

## 4. Renormalizable scalar factorization: an explicit bilinear shortcut

The high-degree positive potential also admits a natural renormalizable factorization. Introduce prefix fields Ak with positive terms `|M A2-Phi1 Phi2|²` and `|M Ak-A_(k-1) Phik|²`, followed by `M²|A_(4s),plus-A_(4s),minus|²`. On the tree constraint sheet, `Ak=product(Phi)/M^(k-1)`, reproducing the desired cycle term with Lambda_c=M.

A direct charge search through canonical apartment prefixes finds two fields representing these native edge pairs:

\[
A:\ (0,41),(13,53),\qquad B:\ (4,53),(13,41).
\]

Their full vertex charges differ only at the two ungauged boundaries. Their interior gauge charges are identical, but their boundary PQ charges differ by one. Both are explicit prefixes of actual apartment half-products, recorded with the parent signed cycles in the certificate.

Consequently **epsilon M²|A-exp(i delta)B|²** is gauge invariant, positive, renormalizable and PQ breaking. Under s-fold subdivision each prefix represents2s links. At s=4, an operator involving16 original link fields is replaced by a canonical **dimension-two** mediator mixing. For M=F, each prefix vev is F/16. Even epsilon=1e-3 gives a potential amplitude far above chi, with no Planck suppression.

This rejects the specified canonical-prefix completion as gauge-only protection. It does not reject every mediator architecture. Auxiliary kinetic terms also change the phase metric: the quoted potential uses the old link F as a benchmark, not a newly matched physical fa or a completed scalar spectrum.

## Reproducibility and scope

Producer: `toe_20261105_native_boundary_axion.py`. It regenerates the native incidence, exact boundary flow, refinement screen, explicit cyclic-fermion loop and scalar-mediator charge witness. Remote Desktop Commander runs the PC calculation while the companion JavaScript independently constructs finite-field points and lines, enumerates octagons, verifies the integer frame identity and solves a grounded Laplacian in server V8. Known mathematics remains credited to its original owners.

The validation JSON records the actual producer/test outcomes and source/input/output hashes. Eighteen new cases cover three actual refined graphs, the positive potential, phase normalization, path multiplicity, site anomalies, the telescoping obstruction, changed closing phases, Fourier quadrature and the scalar shortcut. Seventeen related prior PQ/determinant tests are included. An initial14-case run passed; the final harness checks35 cases. Direct server powers initially overflowed the s=6 Planck denominator; logarithmic evaluation fixed it, and every nonzero amplitude is compared against the PC result.

Additional full-text PDF reading covers pages65-68, bringing cumulative coverage to **1-68 of215**. Complete PDF reading and complete past-week patch review remain unfinished. The native-boundary EFT and both repair attempts leave a protected anomaly sector, mediator selection rules, full RG/threshold matching, cosmology, and a common gravity-matter action open. The concrete next design requirement is to protect the **full field inventory**, rather than extrapolate link path length to particles that were added later.
