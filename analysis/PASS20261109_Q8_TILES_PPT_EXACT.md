# Exact certificate: eight Q8 MUBs witness PPT bound entanglement

**November 9, 2026.** Additional independent falsifier beyond the five tracks in PASS20261109_Q8_CORRELATION_FIVE.md. Exact verifier: analysis/w33_20261109_q8_tiles_ppt_exact.py; frozen data: data/w33_20261109_q8_tiles_ppt_exact.json; regression tests: tests/test_w33_20261109_q8_tiles_ppt_exact.py. No hardware claim or new bound-entangled-state construction.

## The known Tiles state

Use the standard two-qutrit Tiles unextendible product basis introduced by Bennett, DiVincenzo, Mor, Shor, Smolin and Terhal, Phys. Rev. Lett. 82, 5385 (1999), https://doi.org/10.1103/PhysRevLett.82.5385 . Its five mutually orthonormal product rays are

    |0> tensor (|0>-|1>)/sqrt2
    (|0>-|1>)/sqrt2 tensor |2>
    |2> tensor (|1>-|2>)/sqrt2
    (|1>-|2>)/sqrt2 tensor |0>
    (|0>+|1>+|2>)/sqrt3 tensor (|0>+|1>+|2>)/sqrt3.

Let P be the sum of their five orthogonal rank-one projectors. The complementary state rho=(I9-P)/4 has trace one, rho^2=rho/4 and rank 4. Every projector is a real product, so rho^Gamma=rho exactly: this state is PPT. The original UPB literature proves entanglement of the complementary subspace, but the new correlation-norm calculation below gives a second **independent explicit entanglement witness**.

## The old witness fails; the 64-correlator witness succeeds

For any one of the three W33 Q8 eight-MUB Choi frames, reconstruct the 64-dimensional two-qutrit traceless correlation matrix T. On Tiles, symbolic arithmetic gives

    F8 = ||T||_F^2 = 17/144 = 0.11805555...
    ||T||_* = 0.7022810881801117... > 2/3.

The previous squared-collision mixed-state witness requires F8 > 4/9, so it fails here. The new nuclear-norm witness detects entanglement despite exact positivity of the partial transpose. As a consequence this familiar PPT-entangled benchmark is not distillable by ordinary LOCC. CCNR/realignment and PPT-UPB entanglement tests are established quantum-information methods; the substantive repo-local connection is eight W33 Q8 nine-outcome measurement settings reconstructing a tight correlation frame sufficient to implement this certified test.

## Exact rational dual-norm proof: not a floating-point inference

The verifier constructs all projectors and the 8x8 Gell-Mann correlation matrix in Q(sqrt3) using SymPy exact arithmetic. It uses a fixed 8x8 integer matrix N, frozen in the producer, divided by D=1000000 to define W=N/D. Its symmetric rational Gram G=W.T*W has exact maximum absolute row sum

    max_i sum_j |G_ij| = 500001262203/500000000000 = 1.000002524406.

For C=1001/1000, this is strictly less than C^2=1.002001. The operator norm ||W||_2 is at most sqrt(maxrow) < C. The dual characterization of nuclear norm therefore gives

    ||T||_* >= tr(W.T*T)/C
             = 111431*sqrt(3)/600600 + 4982501/13104000
             = 0.7015797247833404...

To prove the inequality with **rationals alone**, sqrt3>433/250 follows by comparing squared positive rational numbers. Substitution produces the certified strict rational lower bound

    tr(W.T*T)/C > 2528178727/3603600000
                    = 0.7015702983127983... > 2/3,

with strictly positive excess of **125778727/3603600000**. The operator-norm, density, PPT, projector orthogonality and final strict lower-bound tests are exact symbolic assertions; the numerical trace-norm number is for comparison.

The producer then regenerates all three Clifford Q8 frames from the committed design code, reconstructs the same T from just their 72 ideal outcome probabilities, and independently confirms the result at approximately 3e-16 tolerance.

## A difficult physical limit: shot budget for PPT detection

The exact entanglement violation is only approximately 0.0356 in trace-norm units. The detector-interval linear-programming bound from the five-front producer is conservative. On **expected probabilities, not sampled measurements**, with actual efficiencies eta_j=0.63+0.045j, a 95% simultaneous Hoeffding rectangle over 72 outcomes, and efficiency uncertainty intervals, the following illustrative expected-frequency results hold.

| Efficiency calibration half-width | Accepted shots per basis | Worst-case dual lower bound | PPT entanglement certified? |
|---|---:|---:|---|
| 0.01% relative | 1,000,000 | 0.661983 | No |
| 0.01% relative | 10,000,000 | 0.689393 | Yes |
| 0.1% relative | 1,000,000 | 0.660357 | No |
| 0.1% relative | 10,000,000 | 0.687627 | Yes |
| 1% relative | 1,000,000 | 0.641643 | No |
| 1% relative | 10,000,000 | 0.669120 | Yes |

Because each ideal frequency was set to its exact expectation, these are **optimistic design-point certificates**, not observed power or successful shots. At 10 million accepted events in each of eight bases, the total is 80 million accepted preparations before losses. Real fluctuation, crosstalk, source drift or calibration mistakes could defeat the certificate. No actual device is claimed. The benchmark identifies both a genuine capability and a severe experimental resource challenge.

## Reproduction and limitations

    py -3 analysis/w33_20261109_q8_tiles_ppt_exact.py data/w33_20261109_q8_tiles_ppt_exact.json
    py -3 -m unittest discover -s tests -p test_w33_20261109_q8_tiles_ppt_exact.py -q

The *state and general PPT/CCNR paradigm* are known since prior literature; the *W33/Q8 implementation, explicit rational dual certificate and finite-setting resource audit* are the repo-local results. No claim of TOE, new fundamental particles, an actual photonic experiment or original invention of PPT bound entanglement.

Five independent next tests: (1) search for other PPT-entangled families with a larger W33 correlation margin; (2) optimize exact worst-case nuclear norm over detector intervals via SDP; (3) implement the 9-mode analyzer with measured mode-dependent loss; (4) seek genuinely derived continuum dynamics, Ward identities and dimensional selection; (5) finish the held-out DES Y6 full-covariance shear likelihood under frozen S9 without substituting summary S8 posteriors.
