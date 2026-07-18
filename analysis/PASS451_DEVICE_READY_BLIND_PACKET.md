# Pass 451 — device-ready blind challenge packet

The Pass 442 rehearsal is promoted into a portable, fail-closed packet with five hash-bound components: frozen protocol and integer transfer calibration; sealed observations containing commitments but no labels; predictions bound to the sealed-challenge digest; reveal bound to the prediction digest; and verifier output.

The classifier uses exact integer/rational arithmetic: a minimum affine-fit residual against fixed-point transferred field and ring templates. The abstention margin is frozen at \(1/100\), with 16 phase steps and 16,384 shots per phase.

Synthetic rehearsal result:

\[
96/96\text{ commitments verified},\qquad
96/96\text{ decisions correct},\qquad
0\text{ abstentions}.
\]

**Hardware replacement rule.** Replace only the transfer calibration and observed counts. The templates, classifier, threshold, commitment format, and primary endpoint must remain unchanged.

**Boundary.** The included calibration and counts are synthetic fixed-point data. No laboratory result is claimed.
