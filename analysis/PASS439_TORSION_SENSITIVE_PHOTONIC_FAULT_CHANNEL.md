# Pass 439 — Torsion-sensitive photonic fault-channel falsifier

Pass 438 supplies two competing 2-primary templates at order nine:

\[
GF(9):\quad (\mathbb Z/8)^{72}\oplus(\mathbb Z/16)^{288},
\]

\[
\mathbb Z/9:\quad (\mathbb Z/2)^6\oplus(\mathbb Z/8)^{60}\oplus(\mathbb Z/16)^{216}.
\]

The residue-ring defect has one extra torsion period, \(2\), absent from the field model. Pass 439 turns that distinction into a 16-step Ramsey/echo protocol.

## Protocol

For phase step \(n=0,\dots,15\), measure a binary contrast whose ideal expectation is

\[
C(n)=\frac{1}{M}\sum_T m_T\cos\frac{2\pi n}{T},
\]

where \(T\) is a torsion period and \(m_T\) its multiplicity.

The field template is

\[
C_F(n)=\frac{72\cos(2\pi n/8)+288\cos(2\pi n/16)}{360}.
\]

The residue-ring template is

\[
C_R(n)=\frac{6\cos(\pi n)+60\cos(2\pi n/8)+216\cos(2\pi n/16)}{282}.
\]

Their exact discrete Fourier amplitudes are

\[
\widehat C_F(1)=0.8,\qquad \widehat C_F(2)=0.2,\qquad \widehat C_F(8)=0,
\]

and

\[
\widehat C_R(1)=\frac{36}{47},\qquad
\widehat C_R(2)=\frac{10}{47},\qquad
\widehat C_R(8)=\frac{2}{47}.
\]

Thus the ring defect produces a Nyquist component \(2/47\) that the field model cannot generate.

## Classifier

The device trace is fit against both templates after allowing one free visibility scale. The smaller residual selects the model. The emitted telemetry packet contains:

- one model bit;
- the residual margin;
- the Nyquist amplitude;
- visibility and calibration flags.

These fields fit naturally inside the existing distance-three protected telemetry framework from Pass 427.

## Deterministic synthetic census

The witness performs 72 seeded shot-noise scenarios:

- truth model: field or ring;
- visibility: \(0.55,0.70,0.85,1.00\);
- dark-count fraction: \(0,0.01,0.03\);
- phase jitter: \(0,0.10,0.25\);
- \(16{,}384\) shots per phase point.

Result:

\[
\boxed{72/72\text{ correct classifications}.}
\]

The minimum residual margin is

\[
0.016153162338.
\]

Across the entire census, the largest field Nyquist amplitude is

\[
0.006896972656,
\]

while the smallest ring Nyquist amplitude is

\[
0.014190673828.
\]

So even the single Nyquist feature separates the two synthetic populations in this calibration grid; the full residual classifier supplies an additional firewall.

## Laboratory mapping

A tabletop implementation can use a phase-stepped interferometer or time-bin echo sequence:

1. prepare the selected protected fiber superposition;
2. apply \(n\) repeated phase-step operations;
3. interfere with the reference path;
4. record the binary output contrast;
5. compute bins \(1,2,8\) of the 16-point DFT;
6. compare the two fitted templates.

A significant period-2/Nyquist component is evidence for a residue-ring-like conductor defect, such as a collapsed field multiplication table, nilpotent leakage channel, or hardware operation that respects only the additive \(\mathbb Z/9\) structure.

## Boundary

This is a deterministic synthetic falsifier, not a reported experiment. Real visibility, detector imbalance, phase drift, correlated shot noise, and pulse-shape systematics must be calibrated before applying the threshold to hardware.
