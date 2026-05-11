# PART_CCCCCXXXIX — Orbifold Quotient and Triangle Group

## Flag Count

A **flag** of the map \(\{3,12\}\) is an incident vertex-edge-face triple. The total number of flags is:
\[
|\mathrm{Flags}| = 2E = 2 \times 240 = 480.
\]
The automorphism group \(\mathrm{PSp}(4,3)\) acts on flags. The stabiliser of each flag has order:
\[
|\mathrm{Stab}(\text{flag})| = \frac{|\mathrm{PSp}(4,3)|}{|\mathrm{Flags}|} = \frac{25920}{480} = 54.
\]

## Orbifold Euler Characteristic

\[
\chi_{\mathrm{orb}}(S_{21}/\mathrm{PSp}(4,3)) = \frac{\chi(S_{21})}{|\mathrm{PSp}(4,3)|} = \frac{-40}{25920} = -\frac{1}{648}.
\]

## Triangle Group Quotient

The quotient \(S_{21}/\mathrm{PSp}(4,3)\) is a Riemann sphere with three cone points of orders \(2, 3, 12\) (corresponding to edge midpoints, face centres, and vertices of the regular map). The orbifold Euler characteristic of the triangle group \((2,3,12)\) is:
\[
\chi_{\Delta} = 1 - \frac{1}{2} - \frac{1}{3} - \frac{1}{12} = \frac{1}{12}.
\]

## The Key Identity

\[
\frac{|\mathrm{PSp}(4,3)|}{|\mathrm{Flags}|} = \frac{\chi(S_{21})}{|\mathrm{PSp}(4,3)| \cdot \chi_{\Delta}} = 54.
\]

Expanded: \(|\mathrm{PSp}(4,3)| \cdot \chi_{\Delta} = 25920/12 = 2160\), and \(\chi(S_{21})/2160 = -40/2160 = -1/54\). Thus the flag stabiliser order 54 = 2 × 27 = 2 × \(q^3\), connecting back to the genus sum identity \(g_1 + g_2 = q^3 = 27\).
