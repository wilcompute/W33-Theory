# Pass 125 — Two nonconjugate \(W(E_6)\) embeddings

**Status: PASS.** The executable witness
`w33_pass125_two_we6_embeddings.py` passes all 12 checks; its focused test is
`tests/test_pass125_two_we6_embeddings.py`.

## The conflict

Pass 102 claimed that the code-induced \(W(E_6)=\operatorname{Aut}(W(3,3))\)
is transitive on each nonzero quadratic stratum of
\[
C^\perp/C\cong E_8/2E_8\cong\mathbb F_2^8.
\]
Its stated reason—transitivity of the containing orthogonal group—was not a
valid subgroup argument. Pass 117 then constructed an explicit \(W(E_6)\)
inside \(O_8^+(2):2\) whose orbits were not transitive.

Both computed orbit statements are true, but they belong to different
embeddings.

## The missing code action

On the 40 projective points of \(W(3,3)\), five symplectic transvections
together with the multiplier-\(2\) similitude
\[
\operatorname{diag}(2,2,1,1)
\]
generate the projective group
\[
\operatorname{PGSp}(4,3)\cong W(E_6),\qquad |W(E_6)|=51840.
\]
The witness enumerates the generated permutation group rather than inferring
its order. Each generator preserves W33 adjacency and therefore its binary
adjacency code \(C\). Transporting the coordinate permutations through
\(C^\perp/C\) gives a faithful order-\(51840\) action preserving the
plus-type quadratic form.

Its measured orbits are
\[
\{0\},\qquad
\{x\ne0:Q(x)=0\}\ (135),\qquad
\{x:Q(x)=1\}\ (120).
\]
Thus the stabilizers have orders \(51840/135=384\) and
\(51840/120=432\). This supplies the explicit action that Pass 102 lacked.

## The second embedding

Pass 117 fixes pointwise an ordered anisotropic pair in its \(56\)-suborbit.
Its order-\(51840\) subgroup has fingerprints
\[
\begin{aligned}
Q=0,\ x\ne0 &: 27+36+36+36,\\
Q=1 &: 1+1+1+27+27+27+36.
\end{aligned}
\]
These are the \(E_8\to E_6\times A_2\) branching orbits. They are not the
code-induced W33 orbits.

Conjugate subgroups have the same orbit-size multiset in a fixed permutation
action. The two fingerprints differ, so the two \(W(E_6)\) subgroups are
nonconjugate in \(O_8^+(2):2\).

## Result

There are two complementary \(E_6/E_8\) lenses:

- the **W33 code embedding** is rank-three on the 256 glue classes,
  producing \(1+135+120\);
- the **ordered-pair branching embedding** resolves the same classes into
  \(E_6\times A_2\) representation blocks.

The distinction also fixes a recurring group-name error: equality of the
orders of \(\operatorname{Sp}(4,3)\) and \(W(E_6)\) is not an isomorphism.
The faithful 40-point group used here is
\(\operatorname{PGSp}(4,3)\cong W(E_6)\); its index-two subgroup is
\(\operatorname{PSp}(4,3)\).
