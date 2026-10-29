# Exact 1,500-trial three-photon W33-versus-dual test

**Date:** 2026-10-29. **Status:** exact ideal quantum-optical calculation, not an actual experiment or a theory-of-everything prediction.

## Why this protocol is better specified

The previous exhaustive [three-photon survey](../analysis/w33_20261029_three_photon_dual_discriminator.py) compared W(3,3) point adjacency to its 40-vertex generalized-quadrangle dual. Each graph has SRG parameters (40,12,2,4), so single-particle spectra are equal and global distinct-output two-photon histograms agree. The complete three-photon survey showed that independent input triples with four common point-graph neighbors admit four unusually probable outcomes, absent from the dual's independent-input class.

An initial illustrative triple (0,1,2) is independent **only in the point graph**, not in the dual under the canonical dual-line ordering. This matters when invoking bounds for independent dual inputs. The fixed protocol below corrects the comparison: **(0,7,9) is independent in both graphs**.

## Fixed modes and rational probabilities

Using the sorted F3^4 projective point order and canonical sorted isotropic-line order defined by the producer:

- Input: (0,7,9)
- Point-graph common neighbors: (4,14,23,32)
- Four designated three-photon output triples: (4,14,23), (4,14,32), (4,23,32), (14,23,32)
- Walk: U = (2J - 5(I+A))/15, at t = pi/2 in dimensionless adjacency-hopping units.
- Each bosonic three-by-three permanent is computed **exactly over the integers**, with three distinct input photons and three distinct output ports.
- Point-graph probability numerators for those four events, common denominator 3375²: [26244,26244,26244,26244].
- Dual-graph probability numerators: [784,1024,784,64].

Thus the aggregate four-event probabilities are exactly

    p_W33  = 144 / 15625      = 0.009216
    p_dual = 2656 / 11390625 ≈ 0.0002331742.

This is a **preselected, port-labeled comparison of two known devices**, not an optimization after observing experimental data. A different arbitrary relabeling of the dual changes the four chosen output probabilities; hardware port mapping must be calibrated before data collection.

## Finite-sample decision certificate

For N=1500 **ideal registered three-photon trials** with independent outcomes, observe the number K of trials whose detection event belongs to the set of four designated output triples. Decide W33 when K >= 4; otherwise decide dual. With the exact binomial CDF and survival function:

- Dual incorrectly labeled W33: P(K >= 4 | dual) = 0.0004705969402.
- W33 incorrectly labeled dual: P(K <= 3 | W33) = 0.0005245337713.

Both are below 0.001 in the ideal hypothesis-test model. The event probabilities are *unconditional over every three-photon output pattern*, including bunched outputs. **Do not reinterpret N=1500 as the number of postselected distinct-output coincidences**: that would require different normalization.

## Physical constraints

Requires a calibrated 40-mode lossless interferometer, reproducible injection of three indistinguishable photons, number-resolving detectors, and pre-committed mode labels. Component loss, distinguishability, mode fabrication errors, detector inefficiency, dark counts, phase drift, and input-state contamination change the probabilities and shot budget. Modeling them requires measured device parameters. This is within standard quantum optics; it does not demonstrate failure of standard quantum mechanics or a fault-tolerant eight-logical-qubit optical code.

**Prior art:** Rudinger et al., *Noninteracting multiparticle quantum random walks applied to the graph isomorphism problem for strongly regular graphs*, Phys. Rev. A 86, 022334 (2012), https://doi.org/10.1103/PhysRevA.86.022334. Multi-particle walks as SRG discriminators are **not** new. The contribution here is a specific exactly enumerated port-labeled three-photon event and rigorous finite-sample error certificate.

Reproduce:

    python analysis/w33_20261029_three_photon_1500_trial_protocol.py
    python -m unittest discover -s tests -p test_w33_20261029_three_photon_shot_budget.py -v

NumPy and SciPy are required. The producer writes its deterministic JSON to data/w33_20261029_three_photon_1500_trial_protocol.json.
