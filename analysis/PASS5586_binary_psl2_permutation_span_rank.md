# Pass 5586 — all-odd binary rank of the PSL₂ projectivity-frame design

## Theorem

For every odd prime power \(q\), let \(M_q\) be the incidence matrix of the projectivity-graph design identified in Passes 5580–5585: rows are one \(\mathrm{PGL}_2(q)/\mathrm{PSL}_2(q)\) coset of projectivities of \(\mathbf P^1(q)\), columns are the \((q+1)^2\) cells of \(\mathbf P^1(q)	imes\mathbf P^1(q)\), and a row contains \((x,y)\) exactly when \(y=g(x)\). Then

\[
oxed{\operatorname{rank}_{\mathbf F_2}M_q=rac{(q+1)^2}{2}.}
\]

This closes the binary pattern that Pass 5585 deliberately left conjectural.

## Why the incidence rank is an image-algebra dimension

Vectorize each \((q+1)	imes(q+1)\) permutation matrix. The rows of \(M_q\) are precisely the vectorized permutation matrices \(ho(hg)\) for a fixed \(h\in\mathrm{PGL}_2(q)\) and \(g\in G=\mathrm{PSL}_2(q)\). Multiplication by the invertible matrix \(ho(h)\) does not change span dimension. Hence

\[
\operatorname{rank}_2M_q
=\dim_{\mathbf F_2}\operatorname{span}_{\mathbf F_2}\{ho(g):g\in G\}.
\]

Call this image algebra \(\mathcal A\).

## Published modular input

Zavarnitsine's 2013 paper on the natural projective-line permutation module proves that the all-one line \(I\) is the unique minimal submodule and that the quotient has a unique maximal submodule whose middle factor splits over \(\overline{\mathbf F}_2\) into the two nontrivial absolutely irreducible principal-2-block modules \(U_+\oplus U_-\).

Revin–Zavarnitsine (2021) makes the dimensions and fields of definition explicit. If

\[
a=rac{q-1}{2},
\]

then after scalar extension to \(k=\overline{\mathbf F}_2\) the natural \((q+1)\)-dimensional permutation module has Loewy layers

\[
oxed{\mathbf1\mid(U_+\oplus U_-)\mid\mathbf1,\qquad \dim U_+=\dim U_-=a.}
\]

For \(q\equiv\pm1\pmod8\), the two \(a\)-dimensional constituents are already absolutely irreducible over \(\mathbf F_2\). For \(q\equiv\pm3\pmod8\), the \((q-1)\)-dimensional middle module is irreducible over \(\mathbf F_2\) but splits into the two \(a\)-dimensional constituents after extending to \(\mathbf F_4\).

## Image-algebra dimension

Extend scalars to \(k\); dimension does not change. Let \(J=\operatorname{rad}(\mathcal A\otimes k)\).

Because the permutation module is faithful for its image algebra and its simple composition types are exactly \(\mathbf1,U_+,U_-\),

\[
(\mathcal A\otimes k)/J\cong k\oplus M_a(k)\oplus M_a(k),
\]

so

\[
\dim((\mathcal A\otimes k)/J)=1+2a^2.
\]

The Loewy filtration gives the radical upper bound. An element of \(J\):

- kills the one-dimensional socle;
- maps the \(2a\)-dimensional middle layer into the socle;
- maps the one-dimensional top into middle plus socle.

Therefore

\[
\dim J\le 2a+(2a+1)=4a+1.
\]

For the reverse bound, both \(U_+\) and \(U_-\) occur in \(\operatorname{rad}V/\operatorname{rad}^2V\). Thus the two distinct Pierce components of \(J/J^2\) from the trivial top into \(U_+\) and \(U_-\) are nonzero. Each nonzero component is a module for \(M_a(k)\), so each contributes at least \(a\) dimensions. The permutation-matrix algebra is stable under transpose, and transpose preserves its Jacobson radical, giving the two reverse Pierce components and another \(a+a\) dimensions. Finally the Loewy length is three, so \(J^2V=\operatorname{soc}V
e0\), hence \(J^2
e0\). Therefore

\[
\dim J\ge4a+1.
\]

The bounds coincide:

\[
oxed{\dim J=4a+1.}
\]

Consequently

\[
egin{aligned}
\dim\mathcal A
&=1+2a^2+4a+1\\
&=2(a+1)^2\\
&=oxed{rac{(q+1)^2}{2}}.
\end{aligned}
\]

## Replayed anchors

The executable prime-field verifier from Pass 5580 gives

\[
q=3,5,7,11,13
\quad\mapsto\quad
8,18,32,72,98,
\]

exactly as the theorem requires. The proof itself is all-odd-prime-power; the finite replay is regression evidence, not the argument.

## Prior-art boundary

There are two different prior-art layers here, and both matter.

1. In characteristic zero, Guralnick–Perkinson's work on permutation polytopes already implies that a 2-transitive group of degree \(q+1\) has maximal permutation-polytope affine dimension \(q^2\), equivalent to a \(q^2+1\)-dimensional linear span. Thus the Pass 5582 characteristic-zero rank is best viewed as an explicit rook-complement spectral derivation for this particular incidence design, not as an isolated new dimension phenomenon.
2. The characteristic-two theorem uses the published modular Loewy structure above. I did not find, in the literature search performed for this pass, a source stating the resulting permutation-matrix span dimension \((q+1)^2/2\) in this exact form. That absence is not a novelty claim; it is only a search result.

## Evidence firewall

This theorem is **not** the still-distinct all-odd \(W(3,q)\) footprint-rank statement discussed in Passes 5358/5376. The older characteristic-two firewall remains valid: one cannot reduce the characteristic-zero splitting \(\mathbb C[\mathbf P^1]=\mathbf1\oplus\mathrm{St}\) modulo two. Pass 5586 succeeds precisely because it uses the nonsplit modular Loewy series instead.

Nothing here supplies a \(q>3\) polytope realization or a physics identification.
