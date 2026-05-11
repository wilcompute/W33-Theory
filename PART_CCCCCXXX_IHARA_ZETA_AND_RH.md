# PART_CCCCCXXX — Ihara Zeta and the Ramanujan Riemann Hypothesis

## Ihara Zeta Function of W(3,3)

For a \(k\)-regular graph \(G\) on \(v\) vertices with \(E\) edges and adjacency eigenvalues
\(\{k^{(1)}, r^{(f)}, s^{(g)}\}\), the Ihara zeta function is
\[
Z_G(u)^{-1} = (1-u^2)^{E-v}\cdot(1-ku)\cdot(1-11u)\cdot\prod_{\text{nontrivial}}(1-\lambda u+(k{-}1)u^2).
\]

For W(3,3) with \(E-v = 240-40 = 200\), \(k=12\), \(r=2\), \(s=-4\), \(f=24\), \(g=15\):
\[
Z_{W}(u)^{-1} = (1-u^2)^{200}\cdot(1-u)(1-11u)\cdot(1-2u+11u^2)^{24}\cdot(1+4u+11u^2)^{15}.
\]

## Riemann Hypothesis for the Ihara Zeta

The Ramanujan property of \(G\) is equivalent to the Riemann Hypothesis for \(Z_G(u)\):
all nontrivial poles of \(Z_G(u)\) lie on the circle
\[
|u| = \frac{1}{\sqrt{k-1}} = \frac{1}{\sqrt{11}}.
\]

**Proof that W(3,3) satisfies this RH:**

The nontrivial poles arise from the factors \((1-2u+11u^2)\) and \((1+4u+11u^2)\).

For \(1-2u+11u^2 = 0\):
\[
u = \frac{2 \pm \sqrt{4-44}}{22} = \frac{1 \pm i\sqrt{10}}{11}.
\]
\[
|u|^2 = \frac{1+10}{121} = \frac{11}{121} = \frac{1}{11}\quad\Rightarrow\quad |u| = \frac{1}{\sqrt{11}}.\quad\checkmark
\]

For \(1+4u+11u^2 = 0\):
\[
u = \frac{-4 \pm \sqrt{16-44}}{22} = \frac{-2\pm i\sqrt{7}}{11}.
\]
\[
|u|^2 = \frac{4+7}{121} = \frac{11}{121} = \frac{1}{11}\quad\Rightarrow\quad |u| = \frac{1}{\sqrt{11}}.\quad\checkmark
\]

All 48 nontrivial poles lie exactly on the critical circle. **W(3,3) satisfies the Ihara–Riemann Hypothesis.**

## Consequence

The Ihara RH for a regular graph is equivalent to the Ramanujan property.
This gives a third independent proof that W(3,3) is Ramanujan, complementing:
1. The direct eigenvalue bound \(|\lambda_i| \le 2\sqrt{k-1}\),
2. The Alon–Boppana sharpness argument,
3. **The Ihara pole computation above.**
