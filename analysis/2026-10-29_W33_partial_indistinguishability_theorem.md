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

## Same precommitted ports: exact four-event test and sample-budget extension

To ensure a physically fair comparison, the exact verifier now chooses the same independent triple **(0,7,9)** for both W33 point and orthogonal dual graphs, using the repository's canonical mode order. Its W33 common neighbors are (4,14,23,32). Designate all four 3-element output subsets of these as the success event. They are fixed *before* data collection.

For uniform real pairwise internal-photon overlap s in [0,1], the EXACT aggregate probabilities are

    P_W33(s)=[17496 + 52488*s^2 + 34992*s^3]/11390625
    P_dual(s)=[3376 + 1328*s^2 - 2048*s^3]/11390625

so the fixed-port aggregate gap is

    Delta(s)=[14120 + 51160*s^2 + 37040*s^3]/11390625 > 0.

The dual expression is nonnegative throughout [0,1] despite its negative cubic interference term. The s=1 limit recovers the already-established perfect-indistinguishability protocol with P_W33=0.009216, P_dual=2656/11390625. At s=0, P_W33=0.001536 and P_dual=3376/11390625; this remains a valid graph test, now using classical distinguishable-photon amplitudes.

For independent ideal **registered triple-photon trials**, the script evaluates binomial error probabilities with SciPy, using a deterministic threshold K>=k on the count of successful four-port events. To keep each of the two wrong-classification probabilities strictly below 0.001, minimal integer N under this fixed threshold-test family are:

| Pairwise overlap s | Minimum N | W33 if K>=k |
|---:|---:|---:|
| 0 | 19427 | 15 |
| 0.5 | 6881 | 9 |
| 0.8 | 2437 | 5 |
| 1 | 1413 | 4 |

The verifier explicitly checks both binomial error tails and confirms no integer threshold works with N-1 trials in each row. This is an *ideal* statistical bound, not an account of source brightness, optical transmission, detector inefficiency, timing or device calibration. The N=1500 result from the prior repo applies near the indistinguishable ideal, not at arbitrary s. The source code uses SciPy for this additional numerical statistic; the exact algebraic graph witness does not depend on SciPy.


**October 29 correction:** The previous (s=0) value of (N=20,333), cutoff 16, was only minimal with respect to checking (N-1) at that *particular candidate*, not globally minimal. An independent search found (N=19,427), cutoff 15, with false-negative probability 0.000999712 and false-positive probability 0.000938946. The revised producer checks **every** (1\le N\le19,427) against the minimal false-positive cutoff. This correction changes the ideal distinguishable-photon shot budget; the exact bosonic event probability formulas are unaffected. See `analysis/w33_20261029_three_photon_loss_global_budget.py`.
