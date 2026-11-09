# Prime-field photonics: five independent frontiers, a continuum no-go, and a one-photon SUM correction

**Date:** November 8, 2026 (US Eastern; CI/Git timestamps may read November 9 UTC).
**Code:** `analysis/w33_20261108_primefield_photon_five_fronts.py`
**Tests:** `tests/test_w33_20261108_primefield_photon_five_fronts.py`
**Results:** `data/w33_20261108_primefield_photon_five_fronts.json`
**Scope:** Mathematical theorems, native E6 tensor replay, finite optical circuit proof, and already committed CLASS/Halofit correction audit. NOT a physical TOE, experimental photon/quantum computer, predictive SM spectrum, or a recalculated DES/KiDS likelihood.

## Research provenance and novelty checks

- The previous finite triangular/square result (PASS20261108_FIVE_PHYSICAL_FALSIFIERS) established the native 27/108/36 graph rank-82 completion and its exact integer spectrum. **Here** the focus is the entire prime-field Bloch family and an analytic continuum-limit obstruction.
- PASS20261108_LORENTZ_CHIRP_ESCAPE already proves Gauss-flat convolution and counts off-null support of its principal logarithm. **Here** the focus is the exact **orthogonal-projection energy cost** of a particular principal-log Fourier chirp. Do not rebrand the Gauss sum as a new discovery.
- Prior E6 work established an 81-state rank-78 alternating tensor and a rank-three bilinear completion. **Here** the focus is a gauge-quotient moduli lower bound and a *continuous unselected determinant phase* within a potential-minimum family.
- Previously the logical qutrit magic-injection report treated SUM as an unsupplied two-qutrit entangling primitive. That characterization is **incomplete** when both logical qutrits are independent labels within **one photon**: their SUM is just a routing permutation. This does not give deterministic entanglement between independent photons, nondestructive ancilla measurement, or efficient large-n universal computing.
- Pass12632 CLASS/Halofit correction, independently committed by another track, withdrew all old post-Pass12629 scalar-field shear results. **Here** the correction is replayed from published numeric inputs and no later survey likelihood is fabricated.

## Front 1 — A new prime-family Maxwell obstruction: mode count and anisotropic soft axis

Use \(\mathbb F_p^3\cong\operatorname{Sym}_2(\mathbb F_p)\) for odd primes, with the **complete projective null set of \(m=p+1\) directions**
\[
d_x=(1,x,x^2),\quad x\in\mathbb F_p;\qquad d_\infty=(0,0,1).
\]
One oriented edge channel is assigned per direction per vertex. In momentum block \(k\in\mathbb F_p^3\), the gauge gradient is \(a_j(k)=\exp(2\pi i k\cdot d_j/p)-1\). Standard oriented squares between pairs of channels give the exact magnetic operator
\[
\boxed{K_{\square}(k)=\|a(k)\|^2I_{p+1}-a(k)a(k)^\dagger.}
\]
At every **nonzero** momentum, the directions span the 3-dimensional space, so \(a(k)\ne0\). Hence the block has **one longitudinal gauge zero** and **\(p\) equal nonzero transverse eigenvalues** \(\lambda(k)=\sum_j|a_j(k)|^2\). There are \(p(p^3-1)\) nonzero-momentum physical edge coordinates and \(p+1\) uniform holonomy coordinates at \(k=0\) for square-only curvature.

For the \(p=3\) native case the square-only curvature has rank 78, leaving **four** global harmonic modes after quotienting gradients. Adding the original 36 oriented triangular cycles, which are the length-three parallel-direction loops, gaps these four and produces the **exact previously verified native spectrum**
\[
0^{26}\oplus 3^4\oplus6^{12}\oplus9^{40}\oplus12^{26}.
\]
The new Fourier-block producer independently reconstructs these multiplicities from the momenta, without using that old matrix eigensolver.

More importantly, for the two fixed coordinate momenta \(k_\parallel=(1,0,0)\), \(k_\perp=(0,1,0)\),
\[
\boxed{\lambda(k_\parallel)=2p[1-\cos(2\pi/p)]\sim4\pi^2/p},
\qquad
\boxed{\lambda(k_\perp)=2p}.
\]
For quadratic momentum \(k=(0,0,1)\), the finite-field quadratic Gauss-sum bound yields \(\lambda\ge2(p-\sqrt p)\). The ratio \(\lambda(k_\perp)/\lambda(k_\parallel)\) **diverges like \(p^2/(2\pi^2)\)**. It is about **48.85 at \(p=31\)**, while the \(p\) extra polarizations also increase with \(p\).

**An independent dimension/signature caveat:** \(\operatorname{Sym}_2(\mathbb F_p)\) has **three** history coordinates, and \(\det S\) is an algebraic analogy of a **2+1 Lorentzian** quadratic form, not an already constructed **3+1 spacetime**. In an actual \(2+1\)-dimensional Maxwell continuum a massless U(1) gauge field has **one** propagating polarization; in \(3+1\) dimensions it has **two**. Thus a claim of two photons must also supply a credible 3+1 embedding or an independent physical polarization bundle. The finite model's \(p\) nonzero-k edge modes do not automatically represent either physical continuum. See D. Tong, *Gauge Theory*, electromagnetic degrees-of-freedom chapter, https://www.damtp.cam.ac.uk/user/tong/gaugetheory/gt.pdf.

This is a **rigorous obstruction for the unprojected equal-square-stiffness prime family under the fixed coordinate identification**: multiplying by one p-dependent stiffness cannot turn all three tested momentum directions into an isotropic dispersion, and gauge invariance alone cannot reduce \(p\) transverse channels to two. Anisotropic renormalization, constraints from a distinct physical field, different embeddings, symmetry breaking, extra masses or genuine geometric rescaling might evade the obstruction. The finite-field limit does not itself specify a physical continuum, Lorentz signature, speed of light, or Maxwell coupling.

## Front 2 — The E6 quartic vacuum still has at least 399 inequivalent flat moduli, and does not pin the determinant phase

Prior input: \(M(\phi)\) is an **81×81 alternating tensor** from the original **1620 signed cubic records**, generically of rank 78. Three independent nonholomorphic complex spurions \(\Xi\in\mathbb C^{81\times3}\) can raise this rank to 81.

The proposed invariant quartic \(V(\Xi)=\lambda\operatorname{Tr}[(\Xi^\dagger\Xi-v^2I_3)^2]\) has vacuum manifold \(V_3(\mathbb C^{81})\), of real dimension
\[
2\cdot81\cdot3-9=477.
\]
An E6 gauge orbit has dimension **at most 78**, because \(\dim E_6=78\). Therefore this isolated potential has **at least**
\[
\boxed{477-78=399}
\]
**gauge-inequivalent real flat directions**; even postulating and gauging an *additional*, independent U(3) flavor group could remove at most nine more, leaving at least **390**.

There is a sharper CP observation. Rotate just the first vacuum column by \(\Xi_1\mapsto e^{i\theta}\Xi_1\). This leaves \(\Xi^\dagger\Xi\) and the quartic potential exactly unchanged. If \(U=\overline\Xi\), the native corank-three determinant identity proves
\[
\boxed{\det(M+UTU^T)\mapsto e^{-2i\theta}\det(M+UTU^T)}
\]
for positive diagonal \(T\), without changing the determinant magnitude. The program reconstructs the actual 81-state matrix and verifies the phase law at \(\theta=\pi/7\). Thus the particular quartic cannot independently determine the mass determinant phase.

**Crucial caveat:** the full GUT may gauge or explicitly lift some directions through other interactions, and rephasing can participate in anomalous field redefinitions. This 81-dimensional determinant is NOT the physical SM \(\arg\det(M_uM_d)\), and the calculation is NOT a strong-CP or anomaly-cancellation solution. The result is a falsifier for this *particular standalone scalar potential*.

## Front 3 — Quantify the off-null cost of an exactly flat Gaussian clock's principal logarithm

For odd primes, the nondegenerate quadratic \(Q(k)=k_0k_2-k_1^2\) gives a phase spectrum \(\exp[-2\pi iQ(k)/p]\); its inverse three-dimensional DFT has exactly constant probabilities \(p^{-3}\). This exact Gauss-flat mechanism is already in the repo.

Pick **one specified generator**, the centered principal logarithm \(H(k)=(2\pi/p)\operatorname{centered}(Q(k))\). Fourier inversion produces real Hermitian translation-invariant hopping amplitudes \(h(v)\). Project onto the strict null-link support \(Q(v)=0\), excluding the diagonal, using the Fourier/Parseval orthogonal projection.

The fraction of the generator's **offdiagonal squared Frobenius energy** on forbidden non-null links is:
- \(p=3\): **0.4074074**;
- \(p=5\): **0.7090909**;
- \(p=7\): **0.8775510**.

Thus at \(p=5\) the minimum **relative offdiagonal Frobenius distance** between *this fixed principal-log generator* and the null-supported convolution subspace is \(\sqrt{0.7090909}\approx0.8421\). This is not merely a binary support check; it is an exact least-squares projection bound for a concrete perfect-mixing clock.

**Do not overgeneralize:** changing the \(2\pi\) spectral branches, choosing another perfect-mixing unitary, allowing noncommuting time-dependent null-local Hamiltonians, adding internal degrees of freedom or using nontranslation-invariant controls is not ruled out. This result advances the locality **cost accounting**, not a global null-local no-go theorem.

## Front 4 — Deterministic single-photon SUM is a *passive mode permutation*; two photons are different

Encode three logical qutrit labels in one photon occupying one of **27 mutually orthogonal modes**, \(|a,b,c\rangle\leftrightarrow\) rail \(9a+3b+c\). The controlled-SUM\(_{a\to b}\) operation
\[
|a,b,c\rangle\mapsto|a,b+a\bmod3,c\rangle
\]
is a permutation of 27 physical mode labels, implementable by ideal passive mode routing. The exact permutation has **nine fixed rails and six 3-cycles**, and a minimal decomposition into **12 arbitrary rail swaps**. This produces Schmidt-rank-three nonseparability between the first two *logical degrees of freedom* of one photon, not an entangled state of two independently located photons.

A ninth-root \(T_9=\mathrm{diag}(1,\zeta_9,\zeta_9^{-1})\) on the first logical qutrit can be implemented directly by phase shifting the **18 nontrivial of 27 rails**; no magic-state injection is *logically necessary* for such a full-mode path architecture. Input computational-basis intensities alone do not reveal this phase, but the producer constructs a Fourier-basis interferometric analyzer with **more than five percentage points** of ideal output-probability contrast on a specified test superposition.

**The actual challenge is scalability and operational independence.** Encoding \(n\) independently addressable qutrit factors into a *single photon's orthogonal modes* requires \(3^n\) modes: already **59,049 modes at n=10**. Reusing three time bins does not create new independent address factors; detection of an ancilla carried by the same photon with ordinary destructive detectors destroys the data photon too. A two-*photon* entangling gate is a fundamentally different device problem. Path/frequency/time hybrid encodings may trade spatial rails for other modes, not evade the dimension count.

**Independent external context:** Imany et al., *High-dimensional optical quantum logic in large operational spaces*, npj Quantum Information 5, 59 (2019), https://www.nature.com/articles/s41534-019-0173-8, demonstrated deterministic two-qudit SUM inside a single photon with >90% computational-basis fidelity and explicitly noted that high-dimensional coding alone is not scalable. See also https://doi.org/10.1140/epjqt/s40507-022-00142-1 for theoretical single-photon controlled gates in OAM/path modes.

This corrects an overly broad prior hardware limitation and sharpens the **mode complexity** limitation rather than falsely claiming a new physical breakthrough.

## Front 5 — Corrected CLASS/Halofit checks without resurrecting withdrawn cosmic-shear evidence

The producer independently reads the already committed **six** patched scalar-field-versus-ΛCDM nonlinear-boost control cells and confirms relative differences below \(3\cdot10^{-6}\). It also checks matched-fluid residuals: approximately **0.040%** for the uncoupled exponential model and **3.9–4.4%** for the coupled fading models. This residual does NOT validate Halofit for interacting dark matter; the nonlinear prescription itself needs physical calibration.

**New parallel Pass12632 addendum 2:** Stock CLASS refuses HMcode with scalar fields, so the other research track patched that path separately. I independently replay the new `analysis/toe_uv/hmcode_check.json` alongside patched Halofit. At \(z=0.01,k=1\,h/\mathrm{Mpc}\), the fading-to-CPL **nonlinear-boost ratios minus one** are about **+1.89% in HMcode** and **+0.62% in Halofit**; HMcode's scalar-field ΛCDM control differs from ordinary ΛCDM by about 0.29% at that cell. Two prescriptions now give small, same-sign boosts, but this is **not** an independent observational likelihood or calibration for coupled dark matter.

The corrected, nuisance-refitted **fixed-background** CPL-minus-fading shear chi-square difference is:
- DES Y3: from **+3.100** prepatch to **−0.644** patched;
- KiDS-Legacy: from **+4.686** to **−0.280**.

The reported values are derived *only* from the repo's corrected `sign_des*.json` certificates, not a fresh analysis of raw imaging/shear catalogues. They do not establish which model is statistically preferred. Prior Pass12629–12631 held-out scalar-field shear, old S7/S8 mechanistic statements and the historical S8 Shapley decomposition **remain withdrawn** pending corrected held-out chains, cross-survey covariance, and a proper coupled-matter nonlinear model. The separate expansion-only constraints require their own validation.

See `analysis/PASS12632_HALOFIT_SCF_BUG.md` and `analysis/toe_uv/hf_matched_fluid.json`.

## Sixth synthesis: the selection problem, not just the coupling problem

These results point to one recurring bottleneck:
1. The full finite null orbit contains **too many potential gauge polarizations**, even though its geometry is elegant.
2. An invariant scalar potential has **far too many vacuum moduli**, even when its cubic mass tensor can become full rank.
3. A flat quantum clock is easy when permitting **nonlocal** phases but loses strict locality.
4. A two-qutrit gate within one photon is easy with **exponentially many modes**, but the scalable hardware problem remains.
5. An apparent cosmological preference can disappear when **the forward model** is corrected.

A credible unification program needs an independent, physically motivated *selection mechanism* that reduces these excess channels while preserving gauge symmetry, anomaly cancellation, causality, locality, calibratable dimensionful constants and experimentally independent predictions. Numerical coincidences or successful finite matrix regressions alone do not supply it.

## Reproduction and five orthogonal follow-ups

Run `py -3 analysis/w33_20261108_primefield_photon_five_fronts.py` and `py -3 -m pytest -q tests/test_w33_20261108_primefield_photon_five_fronts.py`.

1. **Photon:** Propose an explicit covariant dynamical projector, local matter constraint or symmetry-breaking pattern that reduces the p nonzero-k transverse branches to exactly two *with a demonstrable continuum limit*.
2. **E6:** Add allowed E6 cubic/quartic invariants and gauge D-terms, count residual moduli by Jacobian rank, and derive an anomaly-cancelled SM vacuum with a radiatively protected \(\bar\theta\).
3. **Quantum clock:** Optimize over spectral branch vectors and certify exact null-support obstructions using cyclotomic integer linear algebra, not just principal-branch L2 projection.
4. **Photonic:** Build an explicit time/frequency/OAM mode router implementing the 27-rail SUM with realistic phase stability, mode errors and resource scaling; design independent-photon versus single-photon tests that cannot be confused.
5. **Cosmology:** Repeat raw DES/KiDS corrected held-out posterior prediction with covariance, check CLASS/Halofit applicability for coupled dark matter, and preserve preregistered predictions irrespective of the outcome.
