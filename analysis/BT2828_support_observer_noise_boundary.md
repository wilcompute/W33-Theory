# Pass 2828: Support Observer Noise Boundary

The six-cycle support observer is an exact noiseless state identifier, but it is not an error-correcting telemetry code.

For each of the eight shortest injective diagnostic words, take the full seven-snapshot support trajectory, flattened to 28 bits.  Exhaustive pairwise comparison gives

\[
\boxed{d_{\min}=1}
\]

for all eight words.

The numbers of state pairs at Hamming distance one are respectively

\[
\boxed{45,\;36,\;45,\;45,\;45,\;36,\;36,\;36}.
\]

For the canonical word

\[
\mathrm{CX}_{p\to f},F_p,Z_p,F_p,Z_p,\mathrm{CX}_{p\to f},
\]

there are 45 nearest state pairs.  Its 48 minimum eight-tap selectors necessarily also have minimum distance one, because deleting trajectory coordinates cannot increase the distance between a pair that already differs in only one full-trace coordinate.

## Consequence

The Pass 2827 decoder ROM is fail-closed for unused 8-bit patterns, but a valid codeword can be changed into another valid codeword by one support-bit error.  Therefore the current observer supplies:

- exact state identification in the noiseless model;
- no guaranteed detection of one arbitrary telemetry-bit error;
- no correction radius.

A fault-tolerant interface must add at least one of:

1. repeated diagnostic rounds with temporal voting;
2. a longer preset word selected for trajectory distance rather than minimum length;
3. multiple distinct six-cycle words whose joint code has larger distance;
4. an external checksum/parity channel;
5. soft-decision decoding using calibrated detector likelihoods.

This boundary is architectural, not a failure of the exact observer theorem.  State observability and noisy code distance are distinct properties and must remain separate in the manuscripts and blueprint.
