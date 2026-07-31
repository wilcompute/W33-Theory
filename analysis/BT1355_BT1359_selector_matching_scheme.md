# Passes 1355–1359 — Selector-Matching Association Scheme

## Scope

Pass 1353 identified the 120-element selector orbit as

\[
\{(L,M): L \text{ a totally isotropic line of } W(3,3),\ M \text{ a perfect matching of the four points of }L\}.
\]

There are 40 isotropic lines and three perfect matchings per line. The present packet determines the complete pair-relation algebra on this set. It closes the manuscript's previously named transport-algebra gap while preserving the existing no-go boundary: the four selector orbitals do **not** manufacture a 12-regular 600-cell/H4 adjacency.

## Pass 1355 — Exact four-class scheme

For selectors \(x=(L,M)\) and \(y=(L',M')\), define:

1. \(R_0\): \(x=y\).
2. \(R_1\): \(L=L'\), but \(M\ne M'\).
3. \(R_2\): \(L\ne L'\) and \(L\cap L'\ne\varnothing\).
4. \(R_3\): \(L,L'\) are disjoint and the unique generalized-quadrangle transversal bijection \(L\to L'\) carries \(M\) to \(M'\).
5. \(R_4\): \(L,L'\) are disjoint and the transported matching differs from \(M'\).

The five relation matrices partition \(X\times X\), are symmetric, and close under multiplication with constant intersection numbers. Hence they form a commutative symmetric association scheme of order 120 and class 4. Its valencies are

\[
\boxed{1,2,36,27,54}.
\]

## Pass 1356 — Bose–Mesner eigenmatrices

With relation ordering \((R_0,R_1,R_2,R_3,R_4)\),

\[
P=\begin{pmatrix}
1&2&36&27&54\\
1&2&-12&3&6\\
1&2&6&-3&-6\\
1&-1&0&9&-9\\
1&-1&0&-3&3
\end{pmatrix},
\]

with primitive multiplicities

\[
\boxed{1,15,24,20,60}.
\]

The second eigenmatrix is

\[
Q=\begin{pmatrix}
1&15&24&20&60\\
1&15&24&-10&-30\\
1&-5&4&0&0\\
1&5/3&-8/3&20/3&-20/3\\
1&5/3&-8/3&-10/3&10/3
\end{pmatrix},\qquad PQ=QP=120I_5.
\]

The verifier checks the algebra-character equations entrywise against the exact intersection tensor; these matrices are not numerical fits.

## Pass 1357 — Imprimitivity and fusion rigidity

The relation \(R_0\cup R_1\) gives 40 fibers of size three. The quotient is exactly the line-intersection graph of \(W(3,3)\), hence \(\operatorname{SRG}(40,12,2,4)\). The fiber-constant primitive ranks are \(1+15+24=40\); the fiber-zero ranks are \(20+60=80\).

All 15 set partitions of the four nonidentity relations were checked. Apart from the full scheme, the only fusions are

\[
\{R_3\cup R_4\},\qquad \{R_2\cup R_3\cup R_4\},\qquad \{R_1\cup R_2\cup R_3\cup R_4\}.
\]

Thus the aligned/misaligned split on disjoint lines is rigid: it can only be forgotten wholesale. The full scheme is neither P-polynomial nor Q-polynomial in any ordering.

## Pass 1358 — S3 transport holonomy and automorphism kernel

The graph on the 40 isotropic lines in which two lines are adjacent when disjoint is connected and 27-regular, with 540 edges. Each edge transports the three perfect matchings by a permutation in \(S_3\). Cycle transports generate the whole group:

\[
\boxed{\operatorname{Hol}=S_3}.
\]

The centralizer of this holonomy inside \(S_3\) is trivial. Therefore a scheme automorphism inducing the identity on the 40-line quotient cannot perform any hidden independent fiber permutation. Combining this kernel theorem with the verified full automorphism group of the \(W(3,3)\) line graph yields

\[
\boxed{\operatorname{Aut}(\mathcal X)\cong \operatorname{PGSp}(4,3)\cong W(E_6),\quad |\operatorname{Aut}(\mathcal X)|=51840.}
\]

This is the precise line-dependent \(S_3\) connection requested by the earlier selector analysis.

## Pass 1359 — Manuscript and literature boundary

The theorem insert is written for both `w33_paper.tex` and `photonic_holonet.tex`, with an idempotent integrator and focused regression tests. In the Holonet it is stated only as a finite routing/transport theorem. It is not evidence for cosmology, Standard-Model parameter claims, or a laboratory implementation.

A targeted literature search found two nearby but different constructions:

- Colangelo–Monzillo–Siciliano study the association scheme on the **160 incident point-line flags** of a finite generalized quadrangle and classify its fusions (Discrete Mathematics 347 (2024), 114054, DOI 10.1016/j.disc.2024.114054).
- Srinivasan studies the classical perfect-matching association scheme on all perfect matchings of a complete graph (Algebraic Combinatorics 3 (2020), 559–591, DOI 10.5802/alco.104).

Neither source, in the targeted search, describes this 120-object bundle of three matchings over each of the 40 isotropic lines of \(W(3,3)\). This packet therefore claims a repository-new exact construction, **not** priority or literature novelty.

## Reproducibility

```bash
python analysis/w33_pass1355_1359_selector_matching_scheme.py --check
pytest -q tests/test_w33_pass1355_1359_selector_matching_scheme.py
python tools/integrate_pass1355_1359.py --check
```

Frozen certificate SHA-256:

```text
4efac1631cc6991861a927e04297c4a072b9a2d4e49953642b9113c7e22f87f0
```
