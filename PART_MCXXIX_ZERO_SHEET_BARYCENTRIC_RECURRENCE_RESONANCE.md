# PART MCXXIX — Zero-Sheet Barycentric Recurrence-Resonance Law

## Statement

On the sampled zero-sheet barycentric ladder

\[
s \in \{0.5,1.0,1.5,2.0,2.5,3.0\}
\]

at split-prime cutoff \(10^5\), the MCXXVIII gap-entropy and gap-concentration
profiles admit a common finite resonance description:

1. entropy and concentration turn at the same sampled point \(s=2\);
2. the discrete Fourier magnitudes are dominated by the DC mode, and the
   strongest nonconstant contribution is the first harmonic;
3. both sequences admit stable order-two least-squares linear recurrences with
   small residuals on the sampled ladder.

This is a **finite sampled theorem**, not an infinite-limit periodicity claim.

## Numerical packet at \(s\)-ladder cutoff \(10^5\)

- shared resonance: \(s=2.0\)
- entropy first-harmonic/DC ratio:
  \[
  0.048906449211440516
  \]
- concentration first-harmonic/DC ratio:
  \[
  0.04764778751835799
  \]
- entropy recurrence coefficients \([a_2,a_1]\) in
  \(E_n \approx a_2 E_{n-2} + a_1 E_{n-1}\):
  \[
  [-0.7930288200175148,\; 1.757925053075776]
  \]
- concentration recurrence coefficients \([a_2,a_1]\) in
  \(C_n \approx a_2 C_{n-2} + a_1 C_{n-1}\):
  \[
  [-0.7838244705015696,\; 1.8194198703813358]
  \]
- entropy max residual: \(0.019827909272768007\)
- concentration max residual: \(0.008619228280685343\)

## Interpretation

MCXXVIII already gave a turning law. MCXXIX adds a **spectral/arithmetic shadow**
of that same finite ladder:

- the DC dominance shows the ladder is governed mainly by a smooth mean profile,
  not by violent oscillation;
- the first harmonic is the strongest nonconstant mode, so the leading departure
  from the mean is a single coarse wave across the six-point ladder;
- the short recurrence fit shows that the ladder has nontrivial finite memory.

So the zero-sheet barycentric dynamics now has:

- direction (MCXXVII),
- turning geometry (MCXXVIII), and
- finite recurrence/spectral resonance structure (MCXXIX).

## Validation

- analysis script:
  `py -3 analysis/w33_zero_sheet_barycentric_recurrence_resonance.py`
- focused test surface:
  `py -3 -m pytest tests/test_w33_cyclotomic.py -k recurrence_resonance -q`
