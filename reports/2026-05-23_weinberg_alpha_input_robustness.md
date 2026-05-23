# 2026-05-23 - Weinberg Alpha-Input Robustness After External Check

## External audit result

A web check found that the earlier value

```text
alpha_hat(MZ)^(-1) = 127.930
```

is not the cleanest externally defensible value for the effective electromagnetic coupling at the Z pole.

Standard evaluations of the running QED coupling at the Z mass more commonly quote values around

```text
alpha^{-1}(MZ^2) ≈ 128.94 - 128.96.
```

For example, Keshavarzi, Nomura, and Teubner quote

```text
alpha^{-1}(MZ^2) = 128.946 ± 0.015.
```

PDG Live gives the effective leptonic weak mixing angle average as roughly

```text
sin^2(theta_eff^lept) = 0.23148 ± 0.00012/0.00013
```

depending on the live page snapshot.

## Robustness check

The tested W33 expression is

```text
sin2_eff = 3/13 + 1/(11 * alpha_inverse).
```

The script checks multiple alpha input conventions:

```text
127.930
128.936
128.946
128.962
```

All predictions remain within one PDG-scale uncertainty of 0.23148 when using uncertainty 0.00012.

## Meaning

This is important because it prevents the result from depending on a fragile or cherry-picked input convention.

The defensible paper claim should be:

```text
3/13 is the finite-geometric generator.
11 is the W33 Hashimoto transport denominator.
The alpha input must be scheme-specified.
Across standard Z-pole alpha conventions, the corrected value remains within the experimental effective-angle band.
```

## Recommendation for the paper

Do not present one alpha input as uniquely forced yet.

Instead write:

```text
Using standard Z-pole alpha(MZ^2) evaluations near alpha^{-1}=128.94--128.96 gives
sin^2(theta_eff) = 0.23147..., within the PDG effective leptonic average.
```

Then add:

```text
The remaining task is to derive the correct alpha scheme from the W33 transport effective action.
```

## New code

- `analysis/w33_weinberg_alpha_input_robustness.py`

When run, it writes:

- `data/w33_weinberg_alpha_input_robustness.json`
