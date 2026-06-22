# BT1438--BT1440: Otto g-2 audit, 13-12-24 bus simulator, and spinor/double-cover gate

## Source paper anchors

Hans Hermann Otto, *Golden Quartic Polynomial and Moebius-Ball Electron*, Journal of Applied Mathematics and Physics 10, 1785--1812 (2022), DOI 10.4236/jamp.2022.105124.

Visible paper anchors used in this packet:

- the abstract gives the rounded claim \(g_e=2.002319\);
- the paper states that the anomalous part of the electron gyromagnetic factor was previously represented by a golden-mean formula, with a series expansion more accurate to the tenth decimal place, but the equation bodies are image-rendered in the SCIRP HTML;
- the paper's core structural object is a 13-times-180-degree twisted double helix whose 12 generated slings are directed to icosahedron vertices;
- the author remarks that a number 24 in the denominator was a strong indicator for the later icosahedral/Moebius-ball construction.

## BT1438 — g-2 audit calculator

The calculator audits the visible rounded claim against the 2023 electron magnetic moment anchor

\[
\frac{g}{2}=1.00115965218059,
\qquad
 g=2.00231930436118.
\]

Otto's visible rounded abstract value is

\[
 g_{\rm Otto,visible}=2.002319.
\]

The absolute residual is

\[
 -3.0436\times 10^{-7}
\]

in \(g\).  This is close at the rounded-display level, but it is not a derivation.  The paper's equations (49) and (50) must be manually transcribed before an Otto-specific formula can be credited.

The calculator also records Schwinger's leading QED baseline for the anomalous part in the \(\Delta g\) convention:

\[
\Delta g_{\rm Schwinger}=\frac{\alpha}{\pi}.
\]

## BT1439 — 13-12-24 Moebius/Fano simulator

The simulator tests the finite bus lift of the paper's explicit construction:

\[
13\text{ half-turns},\qquad 12\text{ slings},\qquad 12\text{ icosahedron vertices}.
\]

The W33 lift is exact:

\[
12(13+1)=168,
\]

where the extra \(+1\) is the closure tick per sling, and

\[
12\cdot 2=24
\]

for two oriented guard apertures per sling.  Therefore

\[
168+24=192.
\]

The icosahedron check verifies 12 vertices, 30 edges, and degree profile \(5^{12}\).  This is the strongest concrete bridge so far: Otto's 13/12 object can be lifted into the exact W33 active/guard bus without changing the counts.

## BT1440 — spinor/double-cover gate

The spinor gate is deliberately strict.  A spinor changes sign under \(2\pi\) and returns under \(4\pi\).  Otto's path has

\[
13\pi = 6.5\text{ turns},
\]

so it has six complete \(2\pi\) blocks plus one leftover half-turn.  That is spinor-relevant, but it is not by itself a closed spin-1/2 proof.

W33 already has a spinor anchor through the Sp(4,R) ~ Spin(2,3) / Dirac-spinor bridge, and it has the finite retwined covariance law

\[
\operatorname{syn}_{H}(e)=\operatorname{syn}_{H'}(Je).
\]

The missing Otto-side object is an explicit closure/chirality identification for the odd 13th half-turn.

## Repo cross-checks

- `w33_paper.tex` already fixes \(\Phi_3=13\), \(k=12\), \(f=24\), \(E=240\), and \(T=160\) from the q=3 parameter closure.
- `W33_TANGLED_POLYHEDRA.py` already emphasizes tangled icosahedra, 12 vertices = k, 30 edges, and the Hurwitz/Klein quartic link \(168=24\cdot7=8\cdot21\).
- `analysis/w33_BREAKTHROUGH_376_dirac_spinor_from_Sp4R.py` already supplies the W33 spinor anchor via Sp(4,R) ~ Spin(2,3).

## Boundary

BT1438--BT1440 do not import the electron model as established physics.  They import only three checkable structures:

1. a numerical audit of the visible \(g_e\) claim;
2. an exact 13-12-24 to 168+24 finite-bus lift;
3. a spinor/double-cover gate that identifies the missing closure condition.
