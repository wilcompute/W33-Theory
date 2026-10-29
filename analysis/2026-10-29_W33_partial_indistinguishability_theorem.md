# Exact three-photon W33 discrimination with imperfect photon overlap

**October 29, 2026.** The parallel producer analysis/w33_20261029_three_photon_dual_discriminator.py previously established a perfectly indistinguishable three-photon distinction between W33 and its orthogonal cospectral dual. This new verifier proves an analytic **uniform-overlap robustness theorem**; it does not claim physics beyond ordinary quantum optics.

At quarter-cycle the graph-matched interferometer on either SRG(40,12,2,4) has U=[2J-5(I+A)]/15. Each numerator entry is -3 or +2. Three photons entering pairwise-nonadjacent distinct inputs, with pure internal states whose *real pairwise mutual overlaps* equal s in [0,1], have collision-free three-output probability

    P(s)=(c0+c2*s^2+c3*s^3)/15^6.

The coefficients sum products over all ordered S3 permutation pairs, with c0 for equal permutations, c2 for relative transpositions, c3 for relative 3-cycles. No independence/cryptography assumption enters.

W33 has 360 independent input triples with FOUR common neighbors (and 2880 with one); select any three common neighbors as outputs, giving a full 3x3 all-minus-three numerator submatrix. Its coefficients are exactly

    W=(4374,13122,8748).

The dual has 1080 independent input triples with zero common neighbors and 2160 with two: no input triple can have three outputs whose every numerator entry is -3. Exhaustively enumerating **all 512** signed 3x3 patterns and excluding the all-minus-three pattern gives universal per-coefficient maxima

    Dual <= (3564,5832,3888).

Therefore at EVERY s in [0,1], for the W33 witness and any dual independent-input/distinct-output event:

    P_W33(s)-P_dual(s)
       >= [810+7290*s^2+4860*s^3]/11390625 > 0.

The inequality remains positive even for fully distinguishable photons s=0; at that endpoint it uses ordinary graph connectivity, not uniquely boson interference. The bound is coefficientwise and conservative: the maxima can come from different signed patterns, making it valid even when the dual physically realizes fewer than the 511 patterns.

An exact independent replay recomputes all 3240 independent input triples on each geometry, the complete 512 pattern family, the gap polynomials and a concrete input/output witness.

**Scope and limitations:** Ideal graph-matched and calibrated unitary; equal real pairwise overlaps; perfect detection; no propagation loss or dark counts; no claim of experimental observation or deviation from quantum mechanics; no physical TOE constants derived. This is a mathematically grounded *optical graph discriminator*, not a new physical interaction.

Reproduce:
    python analysis/w33_20261029_three_photon_partial_overlap.py
    python -m unittest discover -s tests -p test_w33_20261029_partial_overlap.py -v
