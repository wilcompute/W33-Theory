# W33/Q8 deep five-front research — November 9, 2026

Independent follow-up to the previous Q8 measurement/physics/cosmology passes. This package executes five research tracks plus a constructive optical architecture correction. Every claim below distinguishes **exact mathematics**, **numerical simulation**, and **external/physical measurements**. None is a demonstrated theory of everything, optical chip, physical Bell experiment, or DES model likelihood.

## 1. Calibration-robust full-POVM entanglement certification

Previous pass: the ten-setting 90-outcome self-normalizing full POVM inverse recovers 80 traceless two-qutrit density coefficients theta and ten unmeasured click-survival factors s. Write

    M(E,q) x = -b(E), where M=[A(E),-Q(q)], x=(theta,s),
    A_(bj,k) = Tr[E_bj H_k], b_bj = Tr(E_bj)/9.

The 80 Hermitian H_k are Hilbert-Schmidt orthonormal. Assume for each of the 90 outcomes a trusted Frobenius bound ||E_true−E_cal||_F<=e and accepted click probability error |q_true−q_measured|<=eps. Then Parseval, the trace bound and disjoint blocks in Q imply

    ||Delta M||_2 <= sqrt(90)*e + 3*eps = dM,
    ||Delta b||_2 <= sqrt(90)*e/3 = db.

If sigma_min(M_cal)>dM, the inversion error is bounded:

    ||x_true−x_cal||_2 <=
          (db+dM||x_cal||_2)/(sigma_min(M_cal)−dM) = R.

Realignment preserves the Frobenius norm and ||Z||_nuclear<=3||Z||_F for 9×9 matrices, so

    ||Realign(rho_true)||_nuclear >=
          ||Realign(rho_cal)||_nuclear - 3 R.

A strict lower bound above 1 is therefore a valid conditional separability violation, independent of any purity assumption. This is standard perturbation theory plus CCNR, **not a novel separability theorem**.

In the *synthetic expected-count* Horodecki a=0.236 benchmark with 0.995 intensity transmission on each interacting rail and 0.003 rad phase drift, the true CCNR norm is **1.0030587941**, and sigma_min(M)=**0.1585164914**. The sufficient maxima when the other uncertainty is zero are **e=4.88057e−6 per POVM effect** and **eps=1.70631e−5 per conditional probability**. The latter translates via the simultaneous 95% Hoeffding union bound to **14,062,680,952 accepted shots per setting** with zero calibration error, illustrating severe conservatism. Taking each uncertainty to one quarter of its separate maximum still yields a lower CCNR of **1.0015296**. Random noncommuting instrument-perturbation controls verified the actual state/CCNR errors never exceed the bound; a pure separable control was never falsely certified. These are mathematical/expected-count resources, **not measured statistical power**.

Code: analysis/w33_20261109_q8_full_povm_uncertainty_bound.py
Data: data/w33_20261109_q8_full_povm_uncertainty_bound.json

## 2. An exact optical symmetry obstruction and a constructive 27-element Fourier/permutation analyzer

A tempting restricted extra basis is

    U=(L_A tensor L_B) D (F3 tensor F3)

with arbitrary diagonal nine-mode phase mask D and local unitaries L_A,L_B. This **cannot** complete the original eight Q8 Bell contexts with only two extra settings. Proof: every Fourier input column is (Z_A^m tensor Z_B^n)|+,+>. D commutes with Z_A and Z_B, so output columns form local unitary translates of one fixed state. Their first-qutrit reduced matrices depend on only m and the second-qutrit reduced matrices only n. Each local orbit has three members, with traceless members summing to zero because the nine vectors form a complete orthonormal basis. Consequently its local-Bloch response rank is at most **2+2=4**. Two extra such bases supply at most **8 of the 16 missing local directions**, no matter how the phases are optimized. Independent searches over 900 masks per symmetrical/asymmetrical implementation were rank deficient; the regression suite additionally checks fresh random masks. This is a normal-form limitation, not a general no-go for Fourier optics.

The constructive workaround is to insert **fixed nonlocal nine-rail permutations**:

    U=(F3 tensor I3) D1 P (F3 tensor F3)
    V=(I3 tensor F3) D2 Q (F3 tensor F3).

A deterministic search over 1,800 phase/permutation candidate pairs and a subsequent 1,800 phase-only coordinate steps found a pair with **rank 80/80**, condition number **17.8428176**, and 40 pure/mixed reconstructions at maximum error **1.23e−15**. Two selected fixed permutations require ten adjacent-swap inversions in total. Each additional analyzer uses at most **27 two-mode Givens operations to realize fixed qutrit Fourier blocks**, compared with 36 general tunable Givens operations previously, plus nine programmable diagonal phases and the fixed routing. Summed across both extra programs, the abstract count is 54 Fourier mixing operations +10 routing swaps=64, versus 72 generic operations. **These are per-program synthesis counts, not simultaneously installed physical components**; waveguide crossings, conversion efficiency, phase precision, switch losses and drift may change the choice. The two exact permutations, phases and SHA256 basis digest are frozen in the JSON.

Code: analysis/w33_20261109_q8_structured_fourier_readout.py (limited family)
Code: analysis/w33_20261109_q8_perm_fourier_phases_27.py (full-rank workaround)
Data: matching data/w33_20261109_*.json

## 3. Exact class-AIII Chern obstruction for the naive W33 incidence Dirac

With 40 points, 40 lines and 160 incidence edges, the balanced bipartite Dirac is H=[[0,B],[B†,0]], Gamma=diag(I40,−I40), and {H,Gamma}=0. The unweighted matrix B has rank 25; generic complex edge weights can make B invertible and lift its 30 unprotected zero modes.

For **any** continuous, periodic, invertible square B(theta,phi), write B=U_B |B|. The entire occupied negative-energy subspace of H has the globally defined, smooth, periodic, orthonormal frame

    V_minus(theta,phi) = vstack(−U_B(theta,phi), I40) / sqrt(2).

A globally trivial occupied vector bundle has **first Chern number exactly zero**. This is a standard two-parameter consequence of balanced chiral (Altland–Zirnbauer AIII) symmetry and does not extend to arbitrary symmetry classes or 3D winding invariants. The two twist angles are EXTERNAL parameters, not emergent W33 coordinates.

In a W33 numerical check, random U(1) complex phases produce a full-rank graph hopping matrix. Two weak graph edges are then given independent, fixed-modulus periodic Peierls phase twists; the perturbation strength is bounded so the gap stays open throughout both angles. A 13×13 plaquette Berry-phase calculation returns first Chern **8.67e−20**, sampled minimum gap **0.0665915**, with rigorous lower bound **0.0585307**. This verifies the analytic no-go in a concrete W33 example. It does not exclude a 3D AIII winding, overlap/domain-wall construction, explicit breaking of chiral symmetry, gauge-anomaly-free Standard Model physics, or a different regulator.

Code: analysis/w33_20261109_native_twist_chern_no_go.py
Data: data/w33_20261109_native_twist_chern_no_go.json

## 4. DES Y6: actual covariance/xi± provenance still unavailable, S9 unscored

The current official DES Y6 cosmology page says some cosmological data products are released with more forthcoming: https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/ . The public Y6 posterior-predictive software https://github.com/des-science/y6-ppd-public confirms that its analyses require the actual two-point FITS data-vector, matching covariance, scale-cut INI, theory predictions and chain samples. The repository and conditional LCDM S8 result are not substitutes for the frozen S9 alternate-model full-covariance likelihood.

Fresh direct HTTPS GETs from the authorized Windows research machine returned 200 for the official Y6 release web app, DES papers, main analysis arXiv abstract and public PPD code; the formerly indexed unblinded 3x2pt FITS, key-products directory and notebook returned **404**. The 200 release response is a JavaScript/HTML page, not a verified data vector. No validated full unblinded xi+/xi− FITS with matching covariance was obtained. No patched scalar-field CLASS/Halofit predictions or nuisance refits were run. The frozen S9 preregistration is dated 2026-11-08; its model-specific chi-square remains **UNSCORED**. Using the published conditional LambdaCDM S8=0.789±0.012 to claim an S9 sigma would be scientifically invalid.

Code: analysis/w33_20261109_des_y6_public_provenance_probe.py
Data: data/w33_20261109_des_y6_public_provenance_probe.json

## 5. Single-photon internal Hilbert-space factors do not imply spatial Bell locality

Embed the state (|00>+|11>)/sqrt2 in one photon's C3 tensor C3 **internal degrees of freedom**. With commuting CHSH observables assigned to those formal subsystems, the algebraic CHSH expression equals **2sqrt2=2.82842712**, verified directly. Yet both degrees of freedom are carried by a single photon; this is not a loophole-free spacelike Bell experiment with independently chosen measurement settings at separated parties.

For exactly one photon, disjoint detector regions A and B, vacuum ancillary modes, passive number-preserving optical transformations and ideal photon counters, N_A+N_B=1, hence P(clickA AND clickB)=**0** for any input state. Sixteen random one-photon 18-mode controls confirm the operator no-go. It does NOT rule out single-photon mode entanglement, measurements using local oscillators or shared references, non-passive devices or multiphoton protocols.

A second identifiability falsifier builds rho_ent=W rho_product W† and E_product=W† E_ent W. All **90** observed probabilities for the ten-setting projective instrument agree to **2.8e−17**, yet one state has Schmidt rank 2 and the other rank 1. Unknown globally rotated projective instruments cannot determine the operationally trusted tensor-product entanglement structure from probabilities alone. This is why independent POVM and subsystem calibrations are not optional. Relevant prior art: Sheng, Zhang and Chen, Physical Review Letters 134, 010203 (2025), doi:10.1103/PhysRevLett.134.010203; their nonlocality conversion experiment uses TWO OAM-entangled photons, not the one-photon internal algebra of this check.

Code: analysis/w33_20261109_photon_causal_nonlocality_gate.py
Data: data/w33_20261109_photon_causal_nonlocality_gate.json

## Verification and novelty limits

All six frozen Python producers were executed on the authorized Windows machine with NumPy/SciPy/SymPy. The independent test suite rechecks the perturbation lower bound and injected instrument errors; the local phase-orbit rank limit; Fourier/permutation basis reconstruction and digest; the gapped chiral Chern obstruction; the 2sqrt2 internal CHSH and causal counting; untrusted POVM state ambiguity; and the public DES S9 fail-closed gate.

    py -3 -m unittest discover -s tests -p test_w33_20261109_nextfive_deeper.py -q

The work comprises finite mathematical statements, idealized numerical/synthetic apparatus controls and direct public data-acquisition checks. No new Standard Model particles, realistic quantum source, physical device or cosmology model result is claimed. Published unitary 2-design, CCNR, lattice AIII classification and Bell nonlocality are prior art.

## Top five independent next tests

1. Derive *tight* finite-shot CCNR bounds with an experimentally calibrated uncertainty set for full complex POVM elements, using SDP and exploiting physical PSD state constraints rather than worst-case inverse norms.
2. Map the fixed Fourier/phase/permutation readouts onto specific path/time-bin/OAM hardware with measured waveguide losses, crossings and real source/detector models; compare against generic nine-mode meshes.
3. Test a genuine 3D W33-derived chiral/topological extension with nonzero winding or overlap/domain-wall index, local gauge covariance, Ward identities, anomaly cancellation and continuum scaling selected from the geometry.
4. Obtain the authoritative DES Y6 unblinded xi±/covariance release and run the unchanged preregistered S9 corrected CLASS/Halofit likelihood with matched scale cuts and nuisance fits.
5. Build an operational quantum-network protocol converting single-photon internal mode encoding into independently controlled spatial parties, with appropriate local references, loophole budgets and a distinction between contextuality and Bell nonlocality.
