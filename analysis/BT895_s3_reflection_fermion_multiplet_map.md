# BT895 — \(S_3\) Reflection / Fermion Multiplet Map

BT893 identified the three Higgs-grade Yukawa skeletons as the three reflections of

\[
D_3\cong S_3.
\]

BT895 welds that to the BT879 flavor decomposition of the \(27\)-point matter shell.

## Character input

The \(S_3\) flavor action has class character

\[
\chi_{27}(e)=27,
\qquad
\chi_{27}(\text{reflection})=3,
\qquad
\chi_{27}(\text{3-cycle})=0.
\]

Using the \(S_3\) character table

\[
\begin{array}{c|ccc}
& e & \text{reflection} & \text{3-cycle}\\
\hline
\mathbf 1&1&1&1\\
\mathbf {1'}&1&-1&1\\
\mathbf 2&2&0&-1
\end{array}
\]

one gets

\[
\langle\chi_{27},\mathbf 1\rangle=6,
\qquad
\langle\chi_{27},\mathbf {1'}\rangle=3,
\qquad
\langle\chi_{27},\mathbf 2\rangle=9.
\]

Therefore

\[
\boxed{
\mathbb C[27]=6\cdot\mathbf 1\oplus3\cdot\mathbf {1'}\oplus9\cdot\mathbf 2.
}
\]

## Weld to BT893 and BT894

The three BT893 matrices

\[
Y_0,\quad Y_1,\quad Y_2
\]

are exactly the three reflection axes. Their pairwise products are the two nontrivial \(3\)-cycles.

Thus the Yukawa support axes are not an external add-on: they are the transposition/reflection class of the same flavor \(S_3\) that decomposes the \(27\)-matter shell.

The key payoff is the multiplicity

\[
\boxed{9=q^2.}
\]

The nine standard doublets are precisely the representation-theoretic home of the BT894 within-grade profile layer. In other words:

\[
\boxed{
\text{BT894's }9\text{-dimensional internal Higgs profile layer is the }9\cdot\mathbf 2\text{ sector of flavor }S_3.
}
\]

This is the cleanest version of the CKM boundary:

- BT891/BT893 fixes the \(S_3\) reflection support skeleton.
- BT895 identifies that skeleton inside the exact matter-shell character decomposition.
- BT894 localizes the numerical mixing angles to the \(q^2=9\) standard-doublet multiplicity layer.

## Witness

Executable verifier:

```text
analysis/bt895_s3_reflection_fermion_multiplet_map.py
```

Result JSON:

```text
data/PART_BT895_S3_REFLECTION_FERMION_MULTIPLET_MAP_results.json
```
