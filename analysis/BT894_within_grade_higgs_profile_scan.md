# BT894 — Within-grade Higgs Profile Scan

BT893 corrected the grade-level Yukawa skeleton:

\[
Y_g[a,b]=1\Longleftrightarrow b\equiv -a-g\pmod 3.
\]

BT894 pushes one layer deeper and proves where the physical CKM/PMNS angles can live.

## Result

Let each allowed grade block carry a \(9\times 9\) within-grade Higgs profile, since

\[
q^2=9.
\]

The global Yukawa matrix on the \(27=3\cdot9\) matter shell has exactly one nonzero \(9\times9\) block in each grade row, determined by the BT893 shifted reflection. Therefore

\[
YY^T
\]

is block diagonal by grade for every choice of within-grade profiles.

Consequently the grade skeleton alone is angle-blind:

\[
Y_{\mathrm{flat}}Y_{\mathrm{flat}}^T=I_{27}.
\]

The physical mixing matrix factors as

\[
V_{\rm CKM}=\bigoplus_{g\in\mathbb Z_3} U_{u,g}^{T}U_{d,g},
\]

after the within-grade blocks are diagonalized.

## Minimal mixer

A one-dimensional internal block cannot mix. The smallest possible nontrivial mixer is a single two-plane rotation inside one \(q^2=9\) grade block.

The verifier uses the rational \(3\)-\(4\)-\(5\) rotation

\[
R=\begin{pmatrix}
3/5&4/5\\
-4/5&3/5
\end{pmatrix}
\]

embedded into the first two coordinates of one \(9\)-dimensional grade block. This preserves the BT893 support skeleton but gives nonzero within-grade mixing:

\[
\|R-\operatorname{diag}(R)\|_F^2=\frac{32}{25}.
\]

So the exact conclusion is:

\[
\boxed{
\text{nonzero CKM/PMNS mixing first appears as noncommutation of within-grade }9\times9\text{ Gram profiles.}
}
\]

This is the precise continuation of BT891--BT893: grade conservation fixes the support; \(S_3\) fixes the reflection geometry; the numerical angles are a residual \(q^2=9\) profile problem.

## Witness

Executable verifier:

```text
analysis/bt894_within_grade_higgs_profile_scan.py
```

Result JSON:

```text
data/PART_BT894_WITHIN_GRADE_HIGGS_PROFILE_SCAN_results.json
```
