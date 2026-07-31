# Passes 1360–1364 — Selector Gelfand Pair, Terwilliger Algebra, and Schur Defect

## Scope

Passes 1353–1359 identified the 120 selectors
\[
X=\{(L,M):L\text{ a totally isotropic line of }W(3,3),\ M\text{ a perfect matching of }L\}
\]
and proved that their five pair relations form a symmetric four-class association scheme with valencies
\[
1,2,36,27,54.
\]

The present packet computes the global spherical representation and the full local algebra at one selector. It also identifies a sharp four-dimensional boundary between the Terwilliger algebra and the complete orbital algebra of the selector stabilizer.

## Pass 1360 — Exact Gelfand pair

The executable model generates
\[
G=\operatorname{PGSp}(4,3)\cong W(E_6),\qquad |G|=51840,
\]
on the 120 selectors using the 40 symplectic transvections together with one multiplier-\(-1\) similitude.

For a base selector \(x\), the stabilizer is
\[
H=G_x,\qquad |H|=432.
\]
Its five suborbits are exactly the five scheme relations, with sizes
\[
\boxed{1,2,36,27,54}.
\]
The corresponding double-coset sizes are
\[
\boxed{432,\ 864,\ 15552,\ 11664,\ 23328},
\]
which sum to \(51840\).

Because the orbital algebra is the commutative Bose–Mesner algebra from Pass 1355,
\[
\boxed{(G,H)\text{ is a Gelfand pair}.}
\]
The permutation representation \(\mathbb C[X]\) is multiplicity-free with constituent degrees
\[
\boxed{1,\ 15,\ 24,\ 20,\ 60}.
\]

Dividing the first eigenmatrix entries by the relation valencies gives the exact spherical functions:
\[
\Phi=
\begin{pmatrix}
1&1&1&1&1\\
1&1&-1/3&1/9&1/9\\
1&1&1/6&-1/9&-1/9\\
1&-1/2&0&1/3&-1/6\\
1&-1/2&0&-1/9&1/18
\end{pmatrix}.
\]
The Plancherel weights are
\[
\boxed{\frac1{120},\frac18,\frac15,\frac16,\frac12}.
\]

## Pass 1361 — Exact Terwilliger algebra

Let \(A_i\) be the five relation matrices and \(E_i^\ast\) the diagonal shell idempotents at \(x\). Set
\[
A=A_1+2A_2+3A_3+4A_4,
\qquad
D=\sum_{i=0}^{4} iE_i^\ast .
\]
The eigenvalues of \(A\) on the five primitive sectors are
\[
371,\ 11,\ -19,\ -10,\ 2,
\]
so they are distinct; the five diagonal values of \(D\) are also distinct. Hence \(A\) and \(D\) generate the Bose–Mesner and dual diagonal algebras.

The exact word closure stabilizes by word length six and gives
\[
\boxed{\dim_{\mathbb Q}T(x)=79}.
\]
The proof is characteristic-zero: 79 exact integer word matrices are independent, and every right product by \(A\) or \(D\) is solved and verified exactly on all stabilizer orbitals.

The center is computed from exact commutator equations:
\[
\boxed{\dim_{\mathbb Q}Z(T(x))=10}.
\]

Only 53 elementary triple products
\[
E_i^\ast A_j E_k^\ast
\]
are nonzero. Therefore
\[
\boxed{79-53=26}
\]
additional directions are created by multiplication beyond the elementary triple-product span. This is a concrete local obstruction to treating the scheme as triply regular.

## Pass 1362 — Orbital closure and the four-dimensional defect

The order-\(432\) stabilizer \(H\) has
\[
\boxed{83}
\]
orbits on \(X\times X\). Thus its full orbital/coherent algebra has dimension 83, whereas the Terwilliger algebra has dimension 79:
\[
\boxed{T(x)\subsetneq \operatorname{End}_{H}(\mathbb C[X]),\qquad \operatorname{codim}=4.}
\]

The 79 exact Terwilliger word evaluations distinguish all 83 stabilizer orbitals. Consequently the coordinatewise/Schur closure is the entire orbital algebra:
\[
\boxed{\operatorname{SchurCl}(T(x))=\operatorname{End}_{H}(\mathbb C[X]),\qquad \dim=83.}
\]

The defect is completely localized. If \(T_{ac}=E_a^\ast T E_c^\ast\), every shell block already equals the corresponding orbital block except
\[
\boxed{
\begin{aligned}
(a,c)=(2,2):&\quad 8\text{ orbitals versus }\dim T_{22}=6,\\
(a,c)=(4,4):&\quad 16\text{ orbitals versus }\dim T_{44}=14.
\end{aligned}}
\]
Hence
\[
\boxed{4=2+2}
\]
is supported only on the intersecting-line shell and the misaligned-disjoint shell.

## Pass 1363 — Stable split fingerprint in two good characteristics

The exact integral word basis is reduced independently modulo
\[
p=1000003,\qquad p=1000033.
\]
In both characteristics the center has dimension ten, a deterministic generic central element has ten distinct linear factors, and the split simple-block fingerprint is identical:

\[
\boxed{
1,1,1,2,2,3,3,3,4,5
}
\]
for the simple matrix-block sizes.

The corresponding module multiplicities are
\[
\boxed{
3,12,14,1,2,4,4,8,8,1
}
\]
in the sorted block order, with isotypic dimensions
\[
\boxed{
3,12,14,2,4,12,12,24,32,5.
}
\]

Checks:
\[
\sum b_i^2=79,\qquad
\sum b_i m_i=120,\qquad
\sum m_i^2=515.
\]

**Boundary.** This is an exact two-prime split fingerprint. It is not promoted to a rational splitting-field or characteristic-zero Wedderburn theorem without an independent rational central-idempotent calculation.

## Pass 1364 — Manuscript and literature boundary

The result is integrated into both principal manuscripts as a finite representation/transport theorem only. It does not:

- choose a preferred perfect matching in a three-element fiber;
- create a 12-regular \(H_4\)/600-cell adjacency;
- validate Holonet cosmology, Standard-Model, or hardware claims;
- establish literature priority.

The nearest targeted source remains Colangelo–Monzillo–Siciliano, *The association scheme on the set of flags of a finite generalized quadrangle*, Discrete Mathematics 347 (2024), 114054, arXiv:2406.03942. Their object is the 160 incident point-line flags, not the present 120 line-matching selectors. General Terwilliger-algebra literature confirms the standard definition and the importance of dimension/Wedderburn calculations, but the targeted search did not locate this exact bundle. The release therefore claims a repository-new exact construction, not novelty in the literature.

## Reproducibility

```bash
python analysis/w33_pass1360_1364_gelfand_terwilliger.py --check
pytest -q tests/test_w33_pass1360_1364_gelfand_terwilliger.py
python tools/integrate_pass1360_1364.py --check
```

Frozen certificate SHA-256:

```text
501863c5aafb0b32c37f295778243c0e1227b7fd981723f9d51a536e98f8c52a
```
