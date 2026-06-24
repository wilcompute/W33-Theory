# BT1693 — Projector-Hardware Claim Status Audit

## Scope

This audit covers

`paper/sections/sec_bt1672_projector_hardware_falsifier.tex`.

It separates claims into four classes:

1. exact;
2. numerical certificate;
3. placeholder engineering;
4. unresolved hardware.

## Count

\[
\begin{array}{c|c}
\text{status} & \text{count} \\
\hline
\text{exact} & 7 \\
\text{numerical certificate} & 2 \\
\text{placeholder engineering} & 3 \\
\text{unresolved hardware} & 3
\end{array}
\]

## Exact claims

1. The minimal monomial projector formulas for
   \(P_{c,6}\), \(P_{c,0}\), \(P_{m,24}\), and \(P_{m,30}\) are exact spectral
   interpolation identities.
2. The raw minimal monomial LCU mass is
   \[
   19/48.
   \]
3. The block-encoding normalization rule
   \[
   \sum_i c_iL^i=\sum_i c_i\Lambda^iH^i
   \]
   is exact for \(H=L/\Lambda\).
4. The centered-signal single-sequence QSVT parity obstruction for endpoint
   selectors is exact.
5. The two-sequence even/odd decompositions for \(P_{c,6}\), \(P_{c,0}\), and
   \(P_{m,30}\) are exact scalar polynomial identities.
6. The \(P_{m,24}\) even quartic has analytic sup norm one on \([-1,1]\).
7. The BT1688 character certificate gives
   \[
   \langle\chi_{H_1},\chi_{H_1}\rangle=1,
   \]
   so the Levi \(H_1\) character is irreducible over \(\mathbb C\) for the
   generated projective symplectic action.

## Numerical certificates

1. The oriented bridge twirl matches
   \[
   (8/81)P_{H_1}
   \]
   to Frobenius error about \(10^{-14}\).  The exact character certificate now
   supports the representation-theoretic conclusion, but the displayed matrix
   equality is still a numerical matrix certificate.
2. The phase-precision thresholds use a first-order sensitivity model and are
   numerical model outputs.

## Placeholder engineering

1. Component-loss SNR values and the 960-case sweep use placeholder component
   values.
2. The BT1687 resource table is a logical Chebyshev-term lowering with placeholder
   SNRs.
3. BT1689 LCU success accounting omits hardware-specific ancilla loss and
   controlled-select imperfections.

## Unresolved hardware

1. Collapsed whole-polynomial QSP phase lists have not been synthesized.
2. A foundry-level switch/delay/analyzer layout has not been assigned.
3. Measured component data and experimental calibration are still missing.

## Audit conclusion

The section is defensible if the text preserves these distinctions.  The exact
algebra and representation claims are strong.  The hardware claims are still a
run-card architecture with placeholders, not a completed experimental result.

## Files

- `analysis/bt1693_projector_hardware_claim_status_audit.py`
