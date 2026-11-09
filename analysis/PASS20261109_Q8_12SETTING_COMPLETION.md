# Twelve-setting informational completion of the W33/Q8 eight-Bell-MUB meter

**November 9, 2026.** Constructive follow-up to PASS20261109_Q8_FIVE_EXTENSIONS.md. This is a finite quantum-information measurement design, **not** new physical dynamics or a demonstrated optical chip. Producer: analysis/w33_20261109_q8_12setting_completion.py; JSON: data/w33_20261109_q8_12setting_completion.json; tests: tests/test_w33_20261109_q8_12setting_completion.py.

## Why the 8 / 24 Bell contexts cannot determine purity

One Q8 coset contains eight mutually unbiased maximally entangled bases (72 projectors). Their traceless projectors span the **64-dimensional** two-qutrit correlation-operator subspace spanned by H_a tensor H_b, where H_a (a=1..8) are orthonormal traceless Hermitian qutrit generators. Each projective Bell ray has reduced states I3/3; thus all projectors are orthogonal (in Hilbert-Schmidt inner product) to H_a tensor I3 and I3 tensor H_b. Consequently no combination of the three Q8 cosets (24 Bell bases) can recover **any of the 16 local Bloch parameters**. An explicit exact observational ambiguity is rho0=I9/9 (purity 1/9) versus rho1=|0><0| tensor I3/3 (purity 1/3): all 216 Bell outcomes are uniformly 1/9 in both cases. Earlier pure-state linear-entropy inference therefore relies on *external purity trust*.

## A concrete four-product-setting solution

Use the full set of four qutrit MUBs

    B0=I3,
    B1=F3,
    B2=P F3,
    B3=P^2 F3,

where F3[r,s]=omega^(rs)/sqrt(3), omega=e^(2pi i/3), and P=diag(1,1,omega). Their four bases are mutually unbiased (max |overlap|^2 - 1/3 below 5e-13). In each of four extra settings, jointly measure the product basis B_q tensor B_q, recording nine outcomes; marginalize the nine joint probabilities to reconstruct the two qutrit marginal distributions. The standard complete-qutrit-MUB 2-design inversion is

    rho_A = sum_(q=0..3,i=0..2) p_A(q,i) |B_qi><B_qi| - I3,
    rho_B = sum_(q=0..3,i=0..2) p_B(q,i) |B_qi><B_qi| - I3.

Together with T_ab from the first eight Bell bases, the **full 9x9 density operator** is

    rho = I9/9
        + sum_(ab) T_ab H_a tensor H_b
        + (1/3) sum_a tr(rho_A H_a) H_a tensor I3
        + (1/3) sum_b tr(rho_B H_b) I3 tensor H_b.

This explicitly recovers all 64 nonlocal and 16 local coordinates. It provides **12 nine-outcome settings = 108 observed outcome frequencies**. The 80-column full traceless operator design has **rank 80**, and singular-value condition number **sqrt(2)**. Sixty seeded pure/mixed density matrices (ranks 1,2,3,5,9) were reconstructed with max 9x9 error 4.1262e-16 and matching marginal checks.

## Minimality scope

With product projective readout B_A tensor B_B, a single setting yields at most two *independent traceless marginal directions per subsystem*, or four combined. Sixteen local traceless coefficients therefore require **at least four such matched product settings** if no additional marginal information exists and we insist on pure product projective analyzers. We explicitly verify that 1, 2, or 3 of the matched product settings leave the combined measurement rank below 80. This is **not** a universal claim that 12 is the fewest settings possible with arbitrary entangled, non-MUB, adaptive, or informationally overcomplete POVMs. The earlier eight Bell bases are strongly unextendible as MUBs; the four added product bases are not required to be mutually unbiased with the Bell bases.

## Hardware and physical interpretation

The four product analyzers are local 3-mode Fourier/phase measurements on each qutrit encoding, not new 9-mode entangled Bell transforms. They add 36 outcomes and are compatible with separately programmable local DOF measurement. Whether the two qutrit factors are path/time-bin/OAM on a single photon or spatially separated systems must be specified. 12-setting statistical completeness **does not imply** a loophole-free entanglement certification: local detection-efficiency calibration, detector dark counts, cross-talk, source drift and finite-shot confidence bounds are still required. The formula permits unbiased verification of purity only after those uncertainty sources are incorporated. Complete qutrit MUB tomography and finite-dimensional operator reconstruction are standard prior art; the repo-local contribution is the exact low-condition-number completion of the Q8 correlation-only architecture.

Reproduce:

    py -3 analysis/w33_20261109_q8_12setting_completion.py data/w33_20261109_q8_12setting_completion.json
    py -3 -m unittest discover -s tests -p test_w33_20261109_q8_12setting_completion.py -q

Five independent next tests: (1) compare two arbitrary non-Bell projective settings for full rank, testing whether 10 contexts can be informationally complete without MUB extension; (2) derive confidence regions for purity and Schmidt number under calibrated losses; (3) map all 12 settings onto time-bin/OAM optics with actual switching/crossings; (4) construct interacting W33 continuum models with chirality and anomaly controls; (5) obtain the real DES Y6 cosmic shear covariance and refit frozen S9.
