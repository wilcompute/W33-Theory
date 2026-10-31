# W33 server-only: five quantum-information and gravity fronts (2026-10-31)

**Status:** Five executed, independently simulated finite mathematical models; seven targeted regression tests passed in the server environment. **No user computer accessed.** Producer: \`analysis/w33_20261031_server_five_fronts.py\`; tests: \`tests/test_w33_20261031_server_five_fronts.py\`; certificate: \`data/w33_20261031_server_five_fronts.json\`.

**Provenance and limitations.** Audited the repository at master \`b834d2017f628574ef1d9c009e136b740aaa9cfc\` and its parallel commits. The clique/Levi H1 = Steinberg81 result, 13-native-tick qutrit SWAP, native Jones f4 Strange projector, 40-direction transfer spectrum, and prior Lorentz Ward toy models are all **existing work** and not claimed anew here. This campaign independently rebuilds W(3,3) from F3^4 and tests *additional concrete constructions* and negative controls. Neither numerology nor observed particles, constants, emergent spacetime, or a completed TOE is claimed.

## 1. A 160-rail photonic encoding of W33's known 81-dimensional Steinberg carrier

Construct all 40 points, 40 isotropic four-point lines and **160 incidence flags** of W(3,3). The oriented Levi boundary \`D\` is 80×160 of rank 79. Its nullspace admits an explicit real isometry \`Q: C^81 -> C^160\`, with \`DQ=0\` and \`Q†Q=I81\`. For five actual symplectic transvections, compute 160-flag physical rail permutations \`P_g\`; their encoded action \`R_g=Q†P_gQ\` obeys \`P_gQ=QR_g\`, \`R_g†R_g=I\`, \`R_g^3=I\`, and \`P_g QQ† P_g†=QQ†\` with residual ~1e-14. The five induced 81-dimensional character traces are ~0 and each g fixes 16 physical flags.

**Interpretation:** a concrete ideal one-photon **81-mode logical code embedded in 160 physical modes**, with symmetry actions implemented by passive port relabelings/permutations. The underlying 81D homology/Steinberg fact is old repo work. An optical chip, loss/crosstalk budget, encoder decomposition, or actual physical photon carrier has not been built. This is not the naive 81-label Pauli permutation representation (which the prior branch already ruled out).

## 2. A heralding-error model for the Jones–Wenzl qutrit Strange projector

Existing Jones projector \`f4=|0><0|⊗|S><S|\`, \`|S>=(|1>-|2>)/sqrt2\`, is related to the parity observable \`R|j>=|-j mod3>\` through \`P_-=(I-R)/2=|S><S|\`. The already-supplied ancilla-qubit controlled-parity instrument ideally heralds |S> from |1> with probability 1/2.

**New control:** allow the ancilla readout bit to flip with probability eps *after* ideal nondestructive projection. Conditioned on reporting the minus result for |1>, the actual state is \`(1-eps)|S><S| + eps |E><E|\`, \`|E>=(|1>+|2>)/sqrt2\`; its Strange fidelity is \`1-eps\`, its Wigner minimum for eps in [0,1/2] is \`(2eps-1)/3\` and its mana is \`log((5-4eps)/3)\`. Input |0> is a separate **false herald** control, producing a reported minus result with probability eps. All Wigner phase-point entries are independently evaluated in code. Wigner negativity disappears at eps=1/2, but this is not a fault-tolerance threshold. The QND controlled-R interaction requires an external nonstabilizer-capable physical resource; no free magic or experimental photonic QND implementation has been derived.

## 3. Exact all-120-tick 1D transfer spectrum and full two-site quantum test

Retain 40 Pauli directions and all three spectral outcomes, **120 per site**. Use the explicitly assumed bond \`E_ab=J(3-Tr Pi_aPi_b)-K||[Pi_a,Pi_b]||_F²\` with J=1, K=2. For any fixed tick, relative outcomes partition into 1 identical, 2 distinct same-direction (energy 3J), 36 distinct commuting (energy 2J), 81 noncommuting (energy epsilon=2J-4K/3=-2/3).

Define \`a=exp(-2beta J)\`, \`b=exp(-beta epsilon)\`, \`c=exp(-3beta J)\`. The **entire 120×120 transfer spectrum**, verified numerically at five temperatures, is:
- \`1+2c+36a+81b\` (multiplicity 1);
- \`1+2c+6a-9b\` (multiplicity 24);
- \`1+2c-12a+9b\` (multiplicity 15);
- \`1-c\` (multiplicity 80).

For finite beta the transfer matrix has positive entries and a unique Perron root: this stipulated 1D finite-range clock has **no finite-temperature thermodynamic phase transition**. As a separate quantum check, use **the complete 120-state local Hilbert spaces on two sites** (dimension 14,400), with diagonal pair potential and supplied \`-h(|+><+|_1+|+><+|_2)\` transverse mixing. Matrix-free sparse diagonalization returns positive gaps about 0.03066 at h=0.05 and 0.16521 at h=0.25. A finite-size gap does not prove bulk order, and the spatial lattice/quantum mixing are postulated.

## 4. Exact native Floquet gate exposure and a qutrit noise-channel benchmark

The previous 2D checkerboard exchange drive used a **13-native-tick** synthesis of two-qutrit SWAP. This pass follows *each physical carrier* through all four stages (open L=4,6,8) and records its **actual** number of active SWAP stages t, rather than assigning 52 native ticks to everyone. Under a specified local independent qutrit depolarizing channel with probability p per active native tick, its surviving coefficient is \`eta=(1-p)^(13t)\`, exact entanglement fidelity \`F_e=(1+8eta)/9\`, fixed-pure-input fidelity \`F=(1+2eta)/3\`, and maximally-mixed-input coherent information \`I_c=ln3-S(Choi)\`.

For L=4, p=0.01: mean \`F_e≈0.719\`, worst \`F_e≈0.638\`, and **7/16** carriers retain positive maximally-mixed-input coherent information; at p=0.03 none do. A geometrically chiral routing permutation does not preserve high-quality quantum information by itself. No noisy-channel GNVW index, correlated-error tolerance, or physical gate-loss calibration is claimed. Positive coherent information at one input is a lower bound to single-channel quantum communication capability, not a threshold certificate.

## 5. A 3+1 Lorentz Gauss constraint and explicit scalar-bracket failure

On an assumed **2×2×2 three-dimensional spatial lattice**, use Minkowski \`eta=diag(-1,1,1,1)\` and six \`so(1,3)\` generators (three boosts, three rotations). For canonical vector coordinates x and momenta p at each site define \`G_A=p^T A x\`. Exact Poisson differentiation gives \`{G_A,G_B}=G_[A,B]\` and \`{G_A,H_0}=0\` for a supplied ultralocal \`H_0=.5(p^T eta p+x^T eta x)\`; numerical closure residual <1e-12. **But** \`{H[N],H[M]}=0\` for independent smeared lapses, while a generic discretized spatial-shift target on the same fields is nonzero. This is a **negative control**: the stipulated ultralocal Lorentz-invariant scalar does not reproduce the hypersurface-deformation/ADM bracket needed for GR. No actual Palatini action, curvature constraints, invertible tetrad, refiner, or quantum Einstein dynamics is constructed.

## References and honest interpretation

- Jain and Prakash, *Qutrit and ququint magic states*, Phys. Rev. A 102, 042409 (2020), DOI 10.1103/PhysRevA.102.042409.
- Prakash and Singhal, *Search for high-threshold qutrit magic-state distillation routines*, Phys. Rev. A 113, 042404 (2026), DOI 10.1103/61q5-f754.
- Henderson, Laddha and Tomlin, *Constraint algebra in loop quantum gravity reloaded*, Phys. Rev. D 88, 044028 (2013), DOI 10.1103/PhysRevD.88.044028.
- Prior repo commits \`b834d2017\`, \`7a57f8250\`, \`6343cdf59\`, \`b2f932159\` provide previous physics models, group theory and falsifications. In particular the exceptional q=9 240-point set is **not** certified as E8; a recent independent branch explicitly rejects that over-read.

## Five independent next experiments

1. Synthesize Q as a loss-calibrated 160-port sparse Givens network, measure logical leakage and fault sensitivity.
2. Realize controlled-qutrit parity with a nondestructive optical/hybrid measurement and derive detector false-herald, backaction and resource yield.
3. Scale the full 120-outcome *quantum* clock to a growing local chain via MPO/DMRG; separate true phases from finite two-site gaps.
4. Add coherent two-carrier crosstalk, correlated depolarization, erasure and decoding to the 13-tick active-rail Floquet benchmark.
5. Build a curvature-bearing 3+1 Palatini/tetrad discretization with candidate Gauss, vector, and Hamiltonian constraints and numerically/analytically reject anomalous brackets.
