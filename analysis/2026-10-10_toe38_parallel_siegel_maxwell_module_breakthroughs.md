# TOE Round 38 — parallel-commit synthesis: LOCAL W33 Maxwell two-polarization candidate, modular entanglement firewall, and Lorentz/Weil inequivalence

**Date:** 10 October 2026
**Repository:** wilcompute/W33-Theory
**Evidence protocol:** exact GF(3) ranks and identities where available; double-precision spectral tests at specified k; distinguish proved finite model from a physical theory of everything. No actual photons, electron charge, observed fermions, or Einstein gravity have been derived.

## Parallel commit audit: what was already done and what genuinely changes

Reviewed recent master work in W33 and Holotrade. The decisive current parallel commit is **Passes 11869–11873** (`5e5cdb6d7`), especially `analysis/PASS11869_11873_SIEGEL_LEVEL3_TWO_QUTRITS.md` and `analysis/w33_pass11869_11873_siegel_level3_two_qutrits.py`:
- Level-three genus-two theta functions are nine two-qutrit coordinates; Pauli charges = symplectic Weil 3-torsion `F3^4`; Siegel modular `Sp4(Z)` reduces to Clifford `Sp4(3)`, projective W33 automorphisms `PSp4(3)`.
- Generalized CP `Omega -> -conj Omega` acts by coefficient conjugation, generating the outer arrow/chirality coset `PGSp4(3)=W(E6)`.
- Genus-one Hesse elliptic cubic reproduces modular `j(tau)`; genus-two theta-null states are Coble singular points on the Burkhardt quartic.
- A product state arises at diagonal modulus `Omega12=0` in the chosen level-three frame; Schmidt singulars near there scale as `1:eps:eps²`. **This was already established** by Pass11872; no priority claim on it.
- Parallel Passes 11864–11868 prove finite Lorentz Di matter has zero Weyl helicity, and an isolated Lorentz-invariant charged Majorana condensate has an SM compact-algebra stabilizer, **without a derived condensate potential**.
- Parallel Round37, commits `35689b0df` and `d24c01151` (already published), identifies native chiral-index zero, a 4D orthogonal F3 momentum module with no invariant alternating form, and the failure of naive edge masses or all-to-all cycle projection to preserve BOTH locality and linear dispersion.
- Holotrade independently compiles three K81 carriers with explicit provenance boundaries; there is no warrant to transplant these finite-moduli, photonic or analog lattice results into the trading product.
- A newer **reservation** commit `4259e756b` schedules Passes11874–11878 on fixed modular points, Weil 5+4, mass texture, Clifford magic, and CP, but is NOT a proven result at this report's start. We avoid attributing those reserved findings as established.

## Track A: NEW explicit finite-range plaquette *gauge* completion of W33's 80 edge-flat bands

**Files:** `analysis/w33_20261010_toe38_local_maxwell_2complex.py`; `data/w33_20261010_toe38_local_maxwell_2complex.json`.

Previous linear first-order wave `H=[0,B†;B,0]` on a W33 three-deck cover had 80 exactly zero edge modes in `ker B†`. Those are **divergence-free/transverse cycle directions**, not simply pure-gauge gradients; deleting them as gauge would be physically backward. Round37 found that an onsite mass `mI_edge` moves them off zero but converts E∼|k| into E∼k², while a nonlocal projector preserving E∼|k| is >96% dense.

**New construction:** Use the same 80-site base Levi graph, 160 incidence links and three independent integer deck voltages on chord indices **59,93,139**. There are 1,620 native oriented eight-cycles. Compute their integer winding in Z³ and retain the **1,382 eight-cycles with winding zero**: only these are truly closed length-eight 2-cells in the three-deck infinite cover. Exactly **238** native octagons fail to close locally in that cover and must NOT be inserted as 8-step gauge plaquettes.

At k=0 the signed curl/plaquette boundary matrix has rank **78** (including independent exact GF(3) rank verification, not merely floating rank) inside the Levi graph's 81-dimensional native cycle space. The 3 unfilled cycles are the intended three first-homology/winding directions, not a random missing constraint.

Choose each of the three fundamental winding loops at a common basepoint and add the closed commutator walks `[w_x,w_y]`, `[w_x,w_z]`, `[w_y,w_z]` as **three finite-range plaquette terms** of lengths **32,40,40**. Their cellular boundaries vanish at zero momentum but have nontrivial twist dependence away from zero. The total Fourier plaquette operator `P(k): C^160→C^1385` obeys the exact discrete gauge identity `P(k)B(k)=0` (tested to machine precision in six independent momentum points). There is NO all-to-all 160×160 projector inserted in the action.

The key rank structure:
- At k=0, `rank B=79`, `rank P=78`, leaving exactly **3 harmonic edge modes**.
- At nonzero generic k, `rank B=80`, `rank P=80`, with `ker(B†)` dimension80 but **no exactly flat transverse zero mode** after the plaquette curl energy is applied.
- On the 80-dimensional transverse subspace, the *lowest two* eigenvalues of `P†P` near the x direction are `0.00019047,0.00020519` at k=0.01 and `0.00076186,0.00082073` at k=0.02, while the THIRD eigenvalue is already ~99.59 at small k. Thus these TWO acoustic eigenvalues ∝k², and their wave frequencies `omega=sqrt(lambda)` are **linear in |k|**.
- Along y,z and mixed momenta, ranks and closedness remain valid and there are two low-eigenvalue transverse bands. Differences across directions reveal modest *lattice anisotropy*, so no exact continuum Lorentz symmetry is claimed.

**Interpretation:** This is the most promising *original* cross-track result of this run: a finite-cell, finite-length **Maxwell-like two-polarization propagator** and a precise cellular gauge formulation synthesized from W33's original length-eight geometry plus commutator 2-cells. It resolves the *specific* earlier obstruction to simultaneously local cycle constraints, clearing flat bands, and wave-like dispersion. It DOES NOT establish dynamical photon gauge quantization, Gauss constraints as a physical principle, finite Poincare spinor matter, universal light speed c, an action producing gravity, any coupling value, or experimentally observed Maxwell electrodynamics. Relative plaquette stiffnesses, lattice spacings and physical units remain arbitrary.

**Proposed next proof:** derive the full discrete Maxwell canonical Hamiltonian, gauge quotient, positivity/unitarity, two-polarization continuum cone, isotropy error vs scale and a local finite-depth optical/qutrit implementation of length-8 and 32/40 loops. Verify locality in the infinite covering graph with precise support and coupling.

## Track B: NEW modular-frame-observable firewall + theta moment determinant

**Files:** `analysis/w33_20261010_toe38_theta_moment_modular_frame.py`; `data/w33_20261010_toe38_theta_moment_modular_frame.json`.

For `Omega=[[tau1,eps],[eps,tau2]]` the theta-null coefficient `Theta_ab` expands EXACTLY (for convergent genus-two theta series) as

`Theta(eps)=Σ_{r>=0}(6πi eps)^r/r! u_r(tau1) v_r(tau2)^T`.

Each coefficient is an outer product. The first three distinct moment vectors force the leading determinant term

`det Theta(eps)= (6πi)^3 eps³/2 * det[u0,u1,u2]*det[v0,v1,v2] + O(eps^4).`

For base moduli tau1=0.173+1.07i and tau2=0.286+1.29i, numerical singular exponents are **0.99969,1.99983**, and the determinant asymptotic error drops from 6.29e-4 at |eps|=.024 to 3.93e-5 at |eps|=.006. This PROVES the algebraic *reason* for Pass11872's hierarchy but the observed hierarchy is NOT novel to this pass.

**New physics distinction:** An integral modular shear `Omega12→Omega12+1` acts on the same nine theta coefficients by the **entangling two-qutrit CZ gate**. Take a diagonal Omega with exactly rank-one qutrit tensor coefficients (Schmidt entropy 0). Its shear-equivalent theta-null has **rank three** and Schmidt entropy **0.2452548 nats** in the original marked tensor decomposition, despite representing the same modular-equivalence class of abelian surfaces. This is a *rigorous counterexample* to interpreting unframed Schmidt entropy itself as a modular-invariant physical observable. By contrast generalized CP complex conjugates the coefficients and preserves all Schmidt values.

To build realistic predictions one must construct **modular-invariant quantities**, specify a *physical marking/tensor splitting*, or work with Clifford-orbit/frame-bundle invariant observables. Relative hierarchy by itself is not a fermion Yukawa texture with particle masses, and Pass11874–11878 mass-shape work remains only reserved.

## Track C: NEW incompatibility of the orthogonal finite-Minkowski versus genus-two symplectic 4D modules

**Files:** `analysis/w33_20261010_toe38_minkowski_weil_module_firewall.py`; `data/w33_20261010_toe38_minkowski_weil_module_firewall.json`.

Round37 exhibited `M=S/<c>`, a 4D `F3` quotient of the A6 six-coordinate augmentation representation preserving a **symmetric nondegenerate** Gram `I+J`. Its six-dimensional space of alternating forms has NO A6-invariants: exact finite-field constraint rank **6/6**.

Pass11869 independently identifies the two-qutrit Pauli charge phase space `A[3]=F3^4` with a NONDEGENERATE **alternating** Weil pairing, acted on by the Siegel/Clifford group `Sp4(3)`.

**New theorem (module specific):** There is **no A6-equivariant invertible F3-linear map** from the above orthogonal four-momentum module to *any* four-dimensional A6 representation preserving a nondegenerate alternating form. If T were one, `T^T J T` would pull Weil's J back to a nonzero A6-invariant alternating form on M, contradicting the exact rank6 check. The canonical Weil J itself demonstrably fails four of the Minkowski A6 generator symplectic constraints (8,8,10,10 nonzero defect entries in sample matrices).

The same numerical symbol **F3^4** therefore has two INEQUIVALENT geometric roles: finite orthogonal Minkowski momentum and theta/Pauli symplectic quantum charge. Without extra structure they cannot be identified coordinate-for-coordinate with the same Lorentz A6 action. This is NOT an obstruction to different A6 embeddings in Sp4(3), to tensoring larger representations, or to the abstract spinorial finite Poincare group.

## Three unexecuted outside-the-box research hypotheses motivated by this synthesis

1. **Plaquette-selected light:** Can a positive-definite W33-gauge Hamiltonian make the two modes above dynamically stable, with the third harmonic electric/longitudinal direction removed by a local Gauss law, and couple them to a charged two-qutrit representation? This would be an actual test of electromagnetism rather than a graph count.
2. **Modular frame bundle as physical gauge choice:** The 45 tensor factorizations/tritangent sectors are known from Pass11177/11657 and Round24; impose an equivariant frame-selection dynamics instead of treating a chosen Schmidt decomposition as physical. Seek an invariant CP-odd modular observable whose vacuum depends on the genus-two modulus and isn't merely a basis artifact.
3. **Pauli charges versus Minkowski momenta as dual fibres:** Build a nontrivial *correspondence*, not a false identification, between the orthogonal momentum quotient and symplectic theta charge module through the genus-two moduli or E6 27; find a minimal enlarged representation with both bilinear structures, and compute its consistency and anomaly conditions.

## Verdict and boundaries

The main original advance is a concrete W33 three-deck **local lattice-Maxwell two-polarization candidate** using 1,382 closed native octagons and three 32/40-step commutator plaquettes. The modular-entanglement counterexample and the orthogonal/Weil no-intertwiner theorem are independent new inference-level guardrails. All are algebraic and computational; no observed photon, Standard Model matter, moduli stabilization or full Theory of Everything follows.
