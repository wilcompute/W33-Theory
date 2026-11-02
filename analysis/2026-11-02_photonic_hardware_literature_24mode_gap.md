# Hardware feasibility literature cross-check: the 24-mode W33 route POVM

**Date checked:** 2026-11-02. **Boundary:** comparison with published quantum-optical capabilities, not a claim that W33-specific instrumentation exists.

## External, independently published or circulated results

1. **Cui–Wang (2015), metaplectic-anyon universality:** https://doi.org/10.1063/1.4914941 . Their theorem needs braids **supplemented by measurements of total topological charge**. This is crucial because our finite Clifford/braid-image symmetries and the newly constructed 216-outcome POVM are **not** by themselves a demonstrated universal anyonic computer.
2. **Chang et al. (Science Advances, 2026-07-03), high-dimensional entanglement:** https://doi.org/10.1126/sciadv.aee1333 . The experiment reports 5.70 ± 0.07 ebits, local dimension 1,021, certified entanglement dimension 668, using time-frequency characterization. This is evidence for scalable high-dimensional **mode and entanglement resources**, but does not compile the particular 216-effect W33 POVM and should not be quoted as doing so.
3. **Nguyen et al. (preprint, 2026-10-02), opportunistic frequency-bin tomography:** https://arxiv.org/abs/2610.03496 . Reports full state estimation of biphoton combs with total Hilbert dimension up to 100 using adaptive hardware-aware measurements corresponding to 1.9% of conventional setting count. It is not an experimental realization of our 24-dimensional input/216-outcome measurement or 216-preparation ensemble.

## Explicit implementation requirements and falsifiable data

The mathematical encoding requires **at least 24 coherent, independently addressable input modes**, because the abstract measurement's input Hilbert space is C^24. The manuscript's native two-qutrit time×frequency carrier is C^9 and cannot contain C^24 isometrically without adding another independent degree of freedom or accessible modes.

The ideal analysis isometry is a 216×24 matrix `V` with `V^†V=I_24`. A programmable interferometer or equivalent measurement network must preserve its 216 linearly dependent rank-one effects. A five-qutrit-sized 243-dimensional *output label* space is sufficient for a unitary completion and 27 spare outlets. **This count alone does not imply feasible locality, low loss, or a fault-tolerant compiler.**

Preparation-plus-measurement gives the certified outcome spectrum of `analysis/w33_20261102_frame_prepare_measure_channel.py`:

* Identical preparation/measurement label clicks with probability `1/9` (one outcome);
* 20 outputs at probability `4/225` each;
* 95 outputs at `1/225` each;
* 100 outputs at `1/900` each.

The resulting 216×216 channel has exact spectral gap 39/50 and a 15-dimensional nullspace. This is a candidate **diagnostic protocol** for a device implementing the constructed POVM: characterize all 216 conditional output histograms, compare their multiplicity and covariance signatures, and test loss/crosstalk against the exact probability profile. Nothing in these purely mathematical ratios fixes physical detector efficiency or a number of required photons in the presence of real noise.

**Critical experiment:** demonstrate all four calibrated output probabilities and 40-generator covariance on an independently specified optical encoding, with a noise model and confidence intervals. If the measured kernel's 216×216 rank or conditional overlap distribution differs significantly under controlled calibration, the proposed implementation fails even though the finite-geometric theorem remains correct.
