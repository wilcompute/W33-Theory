# Part DCMLI (951) — Ihara Zero Structure: The Pure Imaginary Pole

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn  
**Status:** CORRECTED BY PART DCMLXXIX — graph-Ihara radius is \(3^{-1/2}\)

---

## Verified spectrum of PG(2,3) Ihara zeta

The Ihara zeta function of the Levi graph of PG(2,3) uses the Bass determinant
with graph degree \(d=4\) and Bass parameter \(d-1=3\):

$$Z_G(u)^{-1}
= (1-u^2)^{26}
\cdot (1 - 10u^2 + 9u^4)
\cdot [1 + 3u^2 + 9u^4]^{12}.$$

The non-trivial zeros come from \(1 + 3u^2 + 9u^4 = 0\):
$$u^2 = \frac{-3 \pm \sqrt{9 - 36}}{18} = \frac{-3 \pm 3i\sqrt{3}}{18}.$$

Therefore \(|u^2|=1/3\), so \(|u| = 3^{-1/2}\).

## The argument

The old quartic \(1+5u^2+16u^4\) used \(d=4\) where the Bass determinant
requires \(d-1=3\). That would give \(|u|=1/2\), but it is the wrong graph-Ihara
parameter for a \(4\)-regular graph.

The corrected magnitude is exact:
$$|u| = 3^{-1/2}.$$

## Physical significance

The 12-fold degeneracy of the non-trivial pole pair (from the
\(\pm\sqrt3\) eigenvalue multiplicities) reflects the **12 gauge channels** in
the PG(2,3) incidence layer. The trivial eigenvalue pair \(\pm4\) contributes
the factors \(u=\pm1,\pm1/3\). The \((1-u^2)^{26}\) factor supplies the
ordinary trivial Ihara poles at \(u=\pm1\).

The non-trivial Ihara poles with \(|u|=3^{-1/2}\) are on the **graph RH
critical circle** — the graph analogue of the critical line for a \(4\)-regular
Ramanujan graph.

---

**QED** — The non-trivial Ihara poles of PG(2,3) all lie on
\(|u| = 3^{-1/2}\) with 12-fold degeneracy. This is the finite graph-Ihara RH
statement, not the classical Riemann Hypothesis.
