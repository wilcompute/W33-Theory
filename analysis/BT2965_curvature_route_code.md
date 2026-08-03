# Pass 2965 — Curvature-Aware \([45,9,9]_2\) Route Code

## Status

**Complete exact binary gauge-code theorem.**

This pass turns the Pass 2962 parity curvature into an error-detecting and error-correcting route syndrome. The code concerns parity faults of the finite \(S_4\) routing permutations; it does not yet model optical loss, continuous phase drift, or even-permutation faults.

## Chain complex

The ten spread modes form \(K_{10}\).

- Edge-parity faults:
  \[
  e\in C^1(K_{10};\mathbb F_2)\cong\mathbb F_2^{45}.
  \]
- Triangle curvature residuals:
  \[
  s=\delta e\in C^2\cong\mathbb F_2^{120}.
  \]

Let \(H\) be the \(120\times45\) triangle-edge incidence matrix. Comparing the observed triangle parities with the certified Pass 2962 baseline gives exactly
\[
s=He.
\]

## Theorem

The verifier proves
\[
\operatorname{rank}_{\mathbb F_2}H=36,
\qquad
\dim\ker H=45-36=9.
\]

Every vertex switching changes all nine edges incident with that vertex and leaves all triangle curvatures unchanged. The ten singleton cuts have one dependency, so they span a 9-dimensional space contained in \(\ker H\). Dimension equality therefore gives
\[
\boxed{\ker H=\operatorname{Cut}(K_{10}).}
\]

The kernel is the binary cut code
\[
\boxed{[45,9,9]_2}.
\]

Its exact weight enumerator is
\[
1+10z^9+45z^{16}+120z^{21}+210z^{24}+126z^{25}.
\]

Consequences:

- every non-gauge fault of weight at most \(8\) is detected;
- every fault of weight at most \(4\) is correctable modulo vertex gauge;
- the first undetectable patterns have weight \(9\) and are precisely singleton vertex switches;
- every single-edge fault has a unique syndrome of weight \(8\);
- two-edge syndrome weights are
  \[
  14^{360},\qquad16^{630}.
  \]

## Check compression

The 120 triangle checks have rank 36. The verifier emits a deterministic set of 36 independent triangles, so a hardware checker does not need 120 stored syndrome bits.

The 210 tetrahedral face relations satisfy
\[
BH=0,
\]
which is the matrix form of the Bianchi identity
\[
\delta^2=0.
\]

## Decoder

Given certified baseline curvature \(\kappa_0\) and observed curvature \(\kappa_{\rm obs}\), form
\[
s=\kappa_{\rm obs}+\kappa_0.
\]

Decode \(s\) to a minimum-weight edge pattern \(e\). Any two solutions differ by a cut and are therefore gauge-equivalent. For weight at most four, the gauge coset is unique.

## Reproduction

```bash
python analysis/bt2965_curvature_route_code.py
```

Expected completion marker:

```text
PASS 10 / 10 The spread router's parity curvature is an exact [45,9,9]_2 gauge code...
```

## Boundary

The syndrome sees only permutation parity. It does not detect:

- an even \(S_4\) routing error,
- attenuation or mode loss,
- phase drift that stays inside one parity class,
- detector faults not mapped to edge parity,
- or coherent optical errors prior to discretization.

Those require the calibrated channel model reserved for Pass 2963.
