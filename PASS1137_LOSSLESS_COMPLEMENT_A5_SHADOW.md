# Pass 1137: Lossless Complement Switch and the \(A_5\) Shadow

## Result

Let \(A\) be the adjacency matrix of the collinearity graph of \(W(3,3)\),
let \(\overline A=J-I-A\) be the noncollinearity adjacency matrix, and put
\(D=A-I\), \(H=D^2\).  Exact GAP 4.12.1 arithmetic proves

\[
 A^2=8I-2A+4J,\qquad
 \boxed{H=13I+4\overline A}.
\]

The off-diagonal support of \(D\) consists of the \(240\) collinear point
pairs.  The off-diagonal support of \(H\) consists of the distinct
\(540\) noncollinear point pairs, tagged `{540:point-nonedge}` in the corpus.
Thus passing from the odd generator \(D\) to the positive generator \(D^2\)
switches exactly from the collinearity relation to its complement.

The switch is lossless:

\[
 \boxed{288D=H^2-98H+385I}.
\]

Consequently

\[
 \mathbb Q[D^2]=\mathbb Q[D],
\]

so the positive generator retains the complete three-channel
Bose--Mesner functional calculus.  GAP independently obtains nullities
\((1,24,15)\) for \(H-121I,H-I,H-25I\) and ranks \((1,24,15)\) for the
three rational projectors of \(D\).

## Why the shift \(A-I\) is canonical

For every strongly regular graph \(\operatorname{SRG}(v,k,\lambda,\mu)\),

\[
 A^2=(k-\mu)I+(\lambda-\mu)A+\mu J.
\]

The half-intersection shift

\[
 D_\lambda=A-\frac{\lambda}{2}I
\]

therefore satisfies the exact identity

\[
 \boxed{
 D_\lambda^2=
 \left(k+\frac{\lambda^2}{4}\right)I+\mu\overline A
 }.
\]

At \((v,k,\lambda,\mu)=(40,12,2,4)\), this is precisely
\(D_\lambda=A-I\) and \(D_\lambda^2=13I+4\overline A\).  The disappearance
of the edge shell is structural, not a numerical coincidence.

## The projective \(A_5\) shadow

The verifier reconstructs the \(240\) doubled-coordinate \(E_8\) roots, all
\(2240\) unordered \(A_2\) root triples, and the \(72\)-root subsystem
orthogonal to the lexicographically first \(A_2\).  Its root reflections
generate

\[
 G=W(E_6)\cong U_4(2){:}2,\qquad |G|=51840.
\]

The action of \(G\) on the \(2240\) triples has orbit sizes

\[
 1,1,27^6,240,270,270,432,432,432.
\]

For each \(432\)-orbit, GAP proves that its stabilizer \(S\) has

\[
 |S|=120,\qquad \operatorname{IdGroup}(S)=[120,34],
\]

so \(S\cong S_5\).  The three stabilizers are conjugate in \(G\).
The derived subgroup

\[
 G'=W(E_6)^+\cong PSp(4,3)\cong U_4(2)
\]

has order \(25920\) and index \(2\).  For every one of the three
stabilizers,

\[
 S\cap G'=S'\cong A_5,\qquad
 |S\cap G'|=60,\qquad
 \operatorname{IdGroup}(S\cap G')=[60,5].
\]

Moreover \(G'\) remains transitive on each \(432\)-orbit and
\(\langle G',S\rangle=G\).  Hence restriction to the derived subgroup
does not split the carrier:

\[
 \boxed{
 \operatorname{Res}^{W(E_6)}_{PSp(4,3)}
 \bigl(W(E_6)/S_5\bigr)
 \cong PSp(4,3)/A_5
 }
\]

as transitive \(PSp(4,3)\)-sets of degree \(432\).  This is the exact
projective \(A_5\) shadow of each \(S_5\)-stabilized \(W(E_6)\) carrier.

## Reproducibility

```text
gap -q analysis/w33_pass1137_lossless_complement_a5_shadow.g
python3 -m pytest -q tests/test_pass1137_gap_lossless_complement_a5_shadow.py
python3 -m json.tool data/w33_pass1137_lossless_complement_a5_shadow.json
```

Artifacts:

- verifier: `analysis/w33_pass1137_lossless_complement_a5_shadow.g`;
- deterministic certificate:
  `data/w33_pass1137_lossless_complement_a5_shadow.json`;
- focused regression:
  `tests/test_pass1137_gap_lossless_complement_a5_shadow.py`.

## Scope

This is an exact theorem about a finite association scheme and finite
permutation groups.  The words “logic switch” describe the complementary
off-diagonal supports of \(D\) and \(D^2\); they do not by themselves assert
a physical Hamiltonian, continuum limit, or hardware implementation.
