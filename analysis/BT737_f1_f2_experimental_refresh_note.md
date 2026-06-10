# BT737 — F1/F2 Experimental Refresh Note

Date: 2026-06-10

This note records the first dated external refresh for the public falsifier dashboard.

## F1 — weak mixing angle

Project formula:

\[
\sin^2\theta_W=\frac{3}{13}=0.2307692308.
\]

External comparison class: effective leptonic weak mixing angle at the Z pole.

Compact refresh values encoded in `data/PART_BT737_F1_F2_EXPERIMENTAL_REFRESH_2026-06-10.json` include:

- CMS Drell--Yan forward-backward asymmetry extraction: \(\sin^2\theta_{\rm eff}^{\ell}=0.23157\pm0.00031\).
- 2025 review/extraction value: \(\sin^2\theta_{\rm eff}^{\ell}=0.23153\pm0.00023\), with SM prediction reported as \(0.23161\pm0.00004\).

Comparison against \(0.23153\pm0.00023\):

\[
0.2307692308-0.23153=-0.0007607692,
\]

about \(3.31\sigma\) using the external uncertainty alone.

Verdict: under the effective-leptonic Z-pole convention, this is **not** an agreement claim. A different scheme or normalization would need to be stated explicitly before F1 is compared again.

## F2 — strong coupling

Project formula:

\[
\alpha_s=\frac{20}{169}=0.1183431953.
\]

External comparison class: \(\alpha_s(m_Z)\) determinations.

Compact refresh values encoded in the JSON include:

- NNPDF 2025 global PDF extraction: \(\alpha_s(m_Z)=0.1194^{+0.0007}_{-0.0014}\).
- FLAG 2024 lattice-review source class for lattice \(\alpha_s\) refresh.
- Older historical world-average cross-check: \(0.1181\pm0.0013\).

Comparison against NNPDF 2025:

\[
0.1183431953-0.1194=-0.0010568047,
\]

which lies inside the quoted asymmetric NNPDF interval. Compared with the older broad world-average cross-check \(0.1181\), the difference is \(+0.0002431953\).

Verdict: F2 is plausibly consistent under an \(\alpha_s(m_Z)\) convention, but a final public claim should refresh directly against the latest PDG QCD review and a current lattice average with identical running convention.

## Dashboard policy

This artifact supports the dashboard policy: repo/internal formula status and external empirical status are separate. F1 is currently a convention-sensitive mismatch under one explicit convention; F2 is close under the standard \(m_Z\) convention but still needs the latest PDG/lattice refresh for a public-facing claim.
