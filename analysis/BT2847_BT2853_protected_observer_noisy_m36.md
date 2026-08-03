# Passes 2847--2853: Protected Observer, Noisy M36, and Active Support Closure

## Status

`COMPLETE_EXACT_WITH_MODELLED_CHANNEL`. All combinatorial, coding, symmetry, recurrence, and adaptive-observer statements are exact. The asymmetric detector study is deterministic-seed Monte Carlo under explicitly synthetic independent channels. New RTL is source-complete; synthesis and place-and-route remain a separate evidence class until observed.

## Pass 2847 -- exact puncturing of the protected trajectory

The eight shortest six-operation support observers have 64 ordered concatenations. Exactly eight concatenations have full-trajectory minimum distance four. For each of those eight 52-column codes, a binary MILP minimizes the retained columns subject to every pair of the 81 codewords differing in at least four selected positions.

The exact optima are

`[28, 29, 29, 29, 28, 29, 28, 28]`.

The canonical `(0,5)` observer therefore compresses from 52 to **28 taps**, removing 24 bits or 46.15%, while retaining `d_min=4`. HiGHS closes at primal value 28, dual bound 28, and zero MIP gap. This is optimal inside the fixed 52-column trajectory, not globally over every possible diagnostic experiment.

## Pass 2848 -- outside-box affine-square feature code

For any affine Clifford evolution of a ternary frame `x`, a binary support tap is exactly

`support(a.x+b) = (a.x+b)^2` over `F3`.

The 52 raw columns collapse to only **14 distinct affine-square Boolean functions**. Their binary function rank is 14; their ternary quadratic-polynomial span has rank 11. Eight distinct functions can identify all 81 states, but every such eight-function code has distance one.

Allowing independent resampling gives an exact integer repetition problem on the 14 functions. The optimum distance-four payload is **24 samples**: twelve affine-square features, each observed twice. The MILP closes with primal and dual value 24 and zero gap. This is a changed measurement schedule, not a puncture of the historical trajectory.

## Pass 2849 -- exact observer symmetry

The distance-four concatenation digraph on the eight shortest words has automorphism group order **32**. It is two directed `K2,2` components with structure

`(S2 x S2)^2 semidirect S2`.

All eight distance-four edges form one orbit.

The 48 minimum eight-tap fast selectors form a transitive block system. Five columns are mandatory. The remaining eleven split into orbits of sizes 3 and 8; the size-eight orbit decomposes into two four-sets under zero codegree. The full selector-hypergraph automorphism group has order

`6912 = 6 x 1152`

with structure

`S3 x (S4 wreath S2)`.

## Pass 2850 -- asymmetric photonic maximum-likelihood decoding

The canonical 28-bit protected code was decoded under independent false-positive `p01` and false-negative `p10` support-bit channels. Maximum likelihood equals Hamming decoding under symmetric 2% noise, as required. In three deterministic asymmetric models it reduced observed word-error counts by 72.0%, 74.3%, and 76.7% relative to Hamming decoding.

These are modelled channels, not detector measurements. The result proves the decoder implementation and the importance of directional likelihoods; it does not calibrate a laboratory.

## Pass 2851 -- phenomenological noisy M36 boundary

For the exact deep-grade branch, the ideal depolarizing-parameter recurrence is

`R(p)=p(4-p)/(3(p^2-2p+2))`.

Adding output depolarization `g` gives

`T_g(p)=g+(1-g)R(p)`.

The fixed-point polynomial factors as

`(p-1)(3p^2-(2+4g)p+6g)`.

The useful attractor and unstable threshold collide at the saddle node

`g_c=(7-3 sqrt(5))/4 = 0.072949016875...`

and

`p_c=(3-sqrt(5))/2 = 0.381966011250...`.

The exact one-round decoder-noise budget is

`g < p(3p-2)/(2(2p-3))`.

A second symbolic model includes true-accept rejection `r` and maximally mixed false acceptance `f`, producing an explicit rational false-accept bound frozen in the certificate. These are phenomenological operating envelopes, not a circuit-level fault-tolerant threshold.

## Pass 2852 -- outside-box no-reset active observer

Treating support readout as feedback rather than a preset telemetry tape changes the state-identification problem into an adaptive distinguishing experiment. Exact memoized policy search proves:

- worst-case selected operations: **4**;
- uniform mean among minimum-depth policies: **94/27 = 3.481481...**;
- best preset open-loop word: 6 operations.

Thus support is not merely finite-delay telemetry. It is an active sensor whose next Clifford probe can be selected from the observed support history.

## Pass 2853 -- hardware and evidence integration

Two SystemVerilog modules are supplied:

- `w33_pass2848_affine_square_feature_encoder.sv`: the 12-feature, twice-sampled 24-bit code;
- `w33_pass2853_affine_square_nn_decoder.sv`: an 81-candidate sequential nearest-neighbor decoder, with guaranteed correction validity for distance at most one.

The parallel Pass-2796 result remains the measured engine baseline: 43 iCE40 logic cells at 72.40 MHz. The new encoder/decoder require their own observed synthesis and placement certificate and are not assigned those figures by analogy.

## Literature boundary

Adaptive distinguishing sequences are a standard finite-state-machine state-identification object and may be much shorter than preset sequences. Binary asymmetric channels require likelihood rules that distinguish `0->1` from `1->0`. The affine-square and golden saddle-node identities above are repository-specific exact computations; no claim is made that they are imported from those literatures.
