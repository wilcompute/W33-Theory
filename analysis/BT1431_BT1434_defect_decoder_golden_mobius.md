# BT1431--BT1434: defect-conditioned search, retwined decoder, Holonet build closure, and golden quartic / Moebius-ball bridge

## BT1431 — defect-conditioned S3 branch search

BT1431 closes the first exact branch layer after the BT1428 211 obstruction.  The incumbent remains

\[
210\text{ identity edges},\qquad 330\text{ corrections}.
\]

BT1376 already proves that every root-fixed S3 relabeling at radius 1, 2, or 3 has identity score at most 205.  Therefore a 211 witness must satisfy two conditions at once:

1. choose one of the 330 raw nonidentity correction slots as a split packet defect;
2. live at radius at least 4 from the current 40-line S3 incumbent.

Thus the exact first open branch key is:

\[
(\text{defect target},\ \text{four or more changed lines},\ \text{new S3 labels}).
\]

This is not yet the global Max-2CSP solve; it is the exact reduced branch contract.

## BT1432 — retwined decoder runtime simulation

BT1432 links the symbolic pulse scheduler to actual CSS decoder coordinates.  It samples eight active coordinates and all 24 guard-tail coordinates, with qutrit error values 1 and 2.  For each sampled error \(e\), it verifies

\[
\operatorname{syn}_{H}(e)=\operatorname{syn}_{H'}(Je)
\]

for both \(X\)- and \(Z\)-check matrices, where

\[
H_X'=H_XJ^{-1},\qquad H_Z'=H_ZJ^{-1}.
\]

Active coordinates remain fixed under the guard shear.  Guard-tail coordinates move exactly when the D4 branch-phase shear is nontrivial.  This turns the BT1425 algebra into an executable runtime decoding check.

## BT1433 — Holonet build closure manifest

BT1433 adds a local build closure manifest.  The connector pass does not safely run the full LaTeX/PDF/render inspection loop, but the repository now contains:

- the BT1430 Fano-bus TeX insert;
- the idempotent splicer;
- the exact local build commands;
- the inspection checklist for the new figure and inserted laws.

The intended local build loop is:

```bash
python tools/integrate_bt1430_fano_bus_holonet.py
latexmk -pdf -interaction=nonstopmode photonic_holonet.tex
python /home/oai/skills/pdfs/scripts/render_pdf.py photonic_holonet.pdf --out_dir /mnt/data/_renders/holonet --dpi 200
```

## BT1434 — golden quartic / Moebius-ball bridge

I did not find a reliable public hit for the exact title `Golden Quartic Polynomial and Moebius-Ball Electron` during this pass.  So the bridge is stated as a testable concept bundle, not as a claimed summary of an inaccessible paper.

The bridge has three exact layers.

### 1. Golden quartic arithmetic

The canonical quartic secant model

\[
Q(x)=x^4-x^2+\frac{5}{36}
\]

has inner roots

\[
\pm\frac{1}{\sqrt6}
\]

and outer roots

\[
\pm\sqrt{\frac56}.
\]

The shell ratio is

\[
\frac{\sqrt{5/6}}{1/\sqrt6}=\sqrt5,
\]

and the outer/inner secant ratio is

\[
\frac{\sqrt5+1}{\sqrt5-1}=\phi^2.
\]

So any true golden-quartic bridge should preserve the same \(\sqrt5,\phi,\phi^2\) spine.

### 2. Moebius-ball covariance

The recent Moebius-ball literature is about covariance: transforms of the ball preserve or characterize analytic/geometric structures such as invariant Laplacians, Dirichlet inner products, reproducing kernels, or quaternionic ball metrics.

### 3. W33 retwined finite analogue

The W33 analogue is not continuous hyperbolic analysis; it is finite frame covariance.  The retwined CSS law says that a transformation is legal only when the state/error frame and stabilizer/check frame are transformed together:

\[
e\mapsto Je,
\qquad
H_X\mapsto H_XJ^{-1},
\qquad
H_Z\mapsto H_ZJ^{-1}.
\]

That is the discrete version of Moebius covariance.  In our front end, the active/guard split is

\[
168+24=192,
\]

with the 24-aperture guard rail carrying the non-Clifford D4 shear.

## Boundary

This packet does not derive an electron model.  It isolates the exact mathematical tests that an electron-as-Moebius-ball model must pass before being imported into the W33/Holonet stack.
