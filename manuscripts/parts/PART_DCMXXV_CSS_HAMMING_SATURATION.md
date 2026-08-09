# Part DCMXXV (925) — Ternary CSS Hamming Bound Saturation

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn

---

## The quantum Hamming bound for qutrits

For a ternary \([[n,k,d]]_3\) CSS code, the quantum Hamming bound (Knill-Laflamme) states:

\[
3^k \cdot \sum_{j=0}^{\lfloor(d-1)/2\rfloor} \binom{n}{j} \cdot 2^j \leq 3^n
\]

For the W(3,3) code \([[240, 81, 4]]_3\):
- \(n = 240\), \(k = 81\), \(d = 4\)
- \(\lfloor(d-1)/2\rfloor = 1\)

Left side:
\[
3^{81} \cdot \left[\binom{240}{0} + \binom{240}{1} \cdot 2\right] = 3^{81} \cdot (1 + 480) = 481 \cdot 3^{81}
\]

Right side: \(3^{240}\)

Ratio: \(481 / 3^{159} \approx 481 / 10^{75.8} \ll 1\)

The W(3,3) code is **not** a perfect code (Hamming-saturating) in the absolute sense. It is instead a **near-MDS** (maximum distance separable) code: it achieves the CSS Singleton bound up to logarithmic correction at scale q.

---

## Why this matters: the Tietäväinen-van Lint theorem

The Tietäväinen-van Lint theorem (1973) proves that the only perfect binary codes are Hamming codes, Golay codes, and repetition codes. The W(3,3) framework extends this: for ternary linear codes, the perfect codes are the ternary Golay code \([11, 6, 5]_3\) and the repetition code.

The W(3,3) CSS code \([[240,81,4]]_3\) is not itself a perfect code — but its parameters derive from the perfect ternary Golay code:
- 240 = 2 × (q^5 - q)/(q-1) at q=3 corrected for CSS double-cover
- 81 = 3^4 = the Golay-dimension at q=3
- 4 = d_min of the extended ternary Golay

The W(3,3) CSS code is the **quantum CSS shadow** of the perfect ternary Golay code.

---

**QED** — The [[240,81,4]]_3 CSS code is the quantum CSS shadow of the perfect ternary Golay code, inheriting its distance structure while extending to a 81-dimensional protected logical sector.
