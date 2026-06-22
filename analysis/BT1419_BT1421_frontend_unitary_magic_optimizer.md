# BT1419--BT1421: unitaries, D4 injection algebra, and S3 optimizer frontier

This packet continues the BT1416--BT1418 front-end stack.

## BT1419 — symbolic optical unitary certificate

BT1417 listed the objectwise optical primitive inventory:

\[
21\text{ edge-channel couplers},\quad 42\text{ oriented phase latches},\quad
168\text{ active bins},\quad 24\text{ guard apertures}.
\]

BT1419 promotes the primitive inventory to exact symbolic unitary blocks:

- edge-channel coupler:
  \[
  H_2=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix};
  \]
- oriented latch: \(\operatorname{diag}(1,\pm1)\);
- four-residue demux: \(F_4[j,k]=i^{jk}/2\);
- six-channel star analyzer: \(F_6[j,k]=e^{2\pi ijk/6}/\sqrt6\).

The verifier checks all blocks are unitary, the \(K_7\) star-incidence Gram law is diagonal \(6\) and off-diagonal \(1\), and the primitive stack has a conservative finite mesh-depth bound

\[
1+1+6+15=23.
\]

Boundary: the bound is an abstract beamsplitter/phase-shifter mesh bound, not a foundry waveguide layout.

## BT1420 — finite D4-quartic injection algebra

BT1418 identified the guard band as

\[
2\text{ quartic atoms}\times 4\text{ branches}\times 3\text{ qutrit phases}=24
\]

and the D4 orientation lift as

\[
24\times8=192.
\]

BT1420 builds the finite algebra on

\[
\{0,1\}_{\rm atom}\times \mathbb Z_4^{\rm branch}\times\mathbb Z_3^{\rm phase}.
\]

The D4 group acts on the four branch labels with order profile

\[
1^1,2^5,4^2.
\]

The Clifford frame action is the uniform qutrit phase shift

\[
(branch,phase)\mapsto(branch,phase+1).
\]

The non-Clifford injection action is the branch-controlled shear

\[
J:(branch,phase)\mapsto(branch,phase+branch\bmod3).
\]

The verifier proves \(J^3=1\), \(J\ne1\), and \(J\) is not a product of a D4 branch permutation with a uniform qutrit phase shift. This makes the guard injection effect algebraically visible rather than merely counted.

Boundary: this is a finite resource-state algebra, not a calibrated nonlinear source.

## BT1421 — S3 gauge optimizer/certificate frontier

BT1376/BT1379 left the S3 synchronization bound at an honest frontier:

\[
540 = 210_{\rm identity}+330_{\rm correction}.
\]

BT1421 does not claim global optimality. It packages the exact incumbent, the radius-3 local certificate, and the physical front-end constraints into a solver-ready Max-2CSP frontier.

The incumbent has 40 line labels, root line fixed to identity, and all six S3 labels used. The already-certified radius-3 exclusion removes

\[
\binom{39}{1}(6^1-1)+\binom{39}{2}(6^2-1)+\binom{39}{3}(6^3-1)=1,991,015
\]

candidate relabelings. Therefore any strictly better global gauge must occur at radius at least four.

The complete front-end gives exact aggregate constraints:

\[
210=21\cdot10=42\cdot5,
\]

and

\[
330=168+162.
\]

So the next exact solver target is now clean: prove \(\sum_e y_e\le210\), or produce a witness with at least \(211\) identity residual edges, subject to the same 540 S3 skew-line constraints and root-fixed gauge.

## Verification commands

```bash
python tools/bt1419_symbolic_optical_unitary_certificate.py
python tools/bt1420_d4_quartic_injection_algebra.py
python tools/bt1421_s3_gauge_frontend_optimizer_frontier.py
python -m pytest -q tests/test_bt1419_bt1421_frontier.py
python -m py_compile tools/bt1419_symbolic_optical_unitary_certificate.py tools/bt1420_d4_quartic_injection_algebra.py tools/bt1421_s3_gauge_frontend_optimizer_frontier.py tests/test_bt1419_bt1421_frontier.py
```
