# Passes 5832–5839 — normalizer, binary code, Pauli quadric, all-field Fourier law, and three outside-box closures

This packet starts from the exact `M2(F2)` affine/Fourier model frozen in Passes 5792–5831 and attacks eight independent-looking questions. They collapse to one coherent picture, but the coefficient ring and the carrier must be kept explicit at every step.

## Pass 5832 — the full degree-16 normalizer is exactly 1152

Write

\[
G= M_2(\mathbf F_2)_+\rtimes (GL_2(2)\times GL_2(2)),\qquad |G|=16\cdot6\cdot6=576,
\]

acting on the 16 matrices by `M -> A M B^{-1}+X`. Exhausting all 20,160 elements of `GL4(2)` gives

\[
|N_{GL_4(2)}(GL_2(2)\times GL_2(2))|=72,
\qquad |C_{GL_4(2)}(GL_2(2)\times GL_2(2))|=1.
\]

Matrix transpose belongs to this normalizer but not to the 36-element left/right subgroup, so the quotient is `C2`.

This is also the **full** normalizer in `S16`, not merely the affine normalizer. The translation subgroup `T=C2^4` is `O_2(G)`: the quotient `G/T=S3×S3` has trivial normal 2-core. Hence `T` is characteristic in `G`; every permutation normalizing `G` normalizes the regular translation group `T`, and therefore lies in `N_{S16}(T)=AGL(4,2)`. Thus

\[
\boxed{|N_{S_{16}}(G)|=16\cdot72=1152},\qquad
\boxed{N_{S_{16}}(G)/G\cong C_2},
\]

with the nontrivial coset represented by transpose. This closes the uniqueness question for the factor-swap outer class in this degree-16 carrier.

## Pass 5833 — the Reye kernel’s minimum words are exactly the heavy shell

Build the 12-point carrier `P={(w,x): w!=0}` and the 16 Reye lines `L_M={(w,Mw):w!=0}`. Exhausting all binary words on the 12 points reproduces the characteristic-two Reye kernel

\[
[12,4,6],\qquad W(z)=1+12z^6+3z^8.
\]

The new object-level statement is

\[
\boxed{\text{the 12 weight-6 words are exactly the 12 heavy supports}}
\]

because every minimum word is

\[
c_{\phi,\psi}(w,x)=\phi(x)+\psi(w),\qquad \phi\ne0.
\]

The three weight-8 words are precisely the `phi=0, psi!=0` words, i.e. unions of two complete four-point `w` fibers.

This also lands directly on the Pass5827 Smith data. The saturated `R^T` map has SNF

\[
1,1,1,1,1,2,2,4,4,
\]

so its mod-2 nullity is four and its 2-adic cokernel valuation is six. The four-dimensional binary defect is therefore the integral lift of the same Reye code kernel. By contrast, the saturated heavy map has seven even invariant factors and valuation nine: it is a different characteristic-two collapse and must not be conflated with the Reye code.

The global odd-q CSS family remains separate. At q=5 that family is `[[156,26,6]]_2`; the local Reye code has the same distance 6 but only 12 coordinates, so equality of distance is not an embedding or equivalence.

## Pass 5834 — the two-qubit 9+6 is actually the same quadratic geometry on the Fourier labels

Saniga–Planat–Pracna identify the 15 two-qubit Pauli observables with a 15-point subconfiguration of the projective line over `M2(GF(2))`; their published `9+6` partition separates the nine-point “Mermin” part from a six-point complement (arXiv:quant-ph/0611063).

Transcribing their `C1,...,C15` Pauli labels into binary symplectic coordinates

\[
v=(x_1,z_1,x_2,z_2),
\]

their partition is exactly the zero/one split of

\[
q_{SPP}(v)=x_1z_1+x_2z_2+x_2.
\]

Our nonzero dual Fourier labels are matrices

\[
Y=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
q_M(Y)=\det Y=ad+bc,
\]

whose zero/one split is the nine nonzero rank-one labels versus the six units.

Exhausting all `GL4(2)` maps finds exactly **72** linear isometries `L` satisfying

\[
q_{SPP}(L(Y))=\det Y\quad\text{for all }Y.
\]

One explicit choice sends the matrix-coordinate basis `(a,b,c,d)` to

\[
(XI,\ IZ,\ IY,\ ZI).
\]

It carries rank-one labels exactly to `C7,...,C15`, units exactly to `C1,...,C6`, and preserves the polarized symplectic form on all 105 unordered nonzero-label pairs. Under this map the rank-one 3×3 grid becomes

\[
\begin{pmatrix}
C_{10}&C_{13}&C_7\\
C_{12}&C_{15}&C_9\\
C_{11}&C_{14}&C_8
\end{pmatrix},
\]

with every row and column a commuting triple (operator phases and Mermin product signs are not part of this certificate).

So the previous “same count only” firewall can be sharpened:

> **The 9+6 Fourier rank split and the published two-qubit 9+6 are objectwise isomorphic quadratic/symplectic geometries.**

The carrier firewall remains essential: this is an isomorphism on the **15 nonzero dual Fourier labels** of the 16-line torsor. It does not turn the q=5 cover points into physical qubit states or observables.

## Pass 5835 — the `1+9+6` law is the r=2 member of an all-field rank-orbit theorem

Let `F_r` be any finite field, let `L=M2(F_r)`, and define the evaluation incidence

\[
R[(w,x),M]=1\iff x=Mw,
\qquad w\in F_r^2\setminus\{0\}.
\]

Index additive Fourier characters of `L` by dual matrices `Y`. The labels split by matrix rank:

\[
N_0=1,
\qquad N_1=(r-1)(r+1)^2,
\qquad N_2=r(r-1)^2(r+1)=|GL_2(r)|.
\]

A point Fourier vector with nonzero covector `phi` maps to the line character labelled by `Y=phi^T w^T`. Consequently

\[
\boxed{\operatorname{im}R^T=\mathbf1\oplus\mathcal F_{\mathrm{rank}\,1}},
\qquad
\boxed{\ker R=\mathcal F_{\mathrm{rank}\,2}},
\]

and therefore

\[
\boxed{\operatorname{rank}R=1+(r-1)(r+1)^2}.
\]

The two nonzero squared singular values are

\[
r^2(r^2-1)\quad\text{on the constant mode},
\qquad
r^2(r-1)\quad\text{on rank one}.
\]

The line-heavy disjointness relation generalizes just as cleanly:

\[
D[M,(\phi,\psi)]=1\iff \psi=-\phi M.
\]

The q=2 case is unusually tight: every rank-one matrix has a unique nonzero factorization `phi^T w^T`. For `r>2` each rank-one label has `r-1` such factorizations, producing an extra point-side kernel of dimension

\[
(r-2)(r-1)(r+1)^2.
\]

The producer proves the formulas algebraically and replay-checks the full Fourier eigenvalue census at prime anchors `r=2,3,5,7`; the prime-power extension uses the field trace to obtain a nontrivial additive character.

## Pass 5836 — publication front doors were behind the mathematics

The canonical publication contract names `docs/index.html` as the public index. Its registered local public sections stopped before these matrix packets, even though the theorem inserts were already inherited by the shared manuscript manifest.

This packet therefore adds a resilient materializer and registers the five cards for Passes 5776–5839. The materializer treats `docs/index.html` and root `index.html` independently: it rejects duplicate IDs but does **not** require the two large surfaces to be byte-identical before inserting a card. That avoids the brittle mirror-equality assumption used by some older one-packet materializers.

The new theorem insert is added once to `analysis/W33_CURRENT_FRONTIER_MANIFEST.tex`, so `w33_paper.tex`, `photonic_holonet.tex`, and `holonet_machine_blueprint.tex` inherit it through the shared frontier.

## Pass 5837 — outside-box probe 1: determinant is a self-dual bent chirp

On the additive four-space `M2(F2)`, set

\[
f(Y)=(-1)^{\det Y}.
\]

Exhaustive Walsh transformation with the Frobenius bit-pairing gives the exact pointwise identity

\[
\boxed{\widehat f(Z)=4(-1)^{\det Z}=4f(Z)}.
\]

Hence determinant is a **self-dual bent quadratic function**. The Walsh spectrum is `+4` ten times and `-4` six times. This packages the `10=1+9` singular versus `6` unit split into one Fourier eigenfunction.

This is a finite Boolean/Fourier statement only; no quantum state is inferred from the word “bent” or from the phase-valued encoding.

## Pass 5838 — outside-box probe 2: the mysterious 1152 is the unit-difference rook graph

Make a Cayley graph on additive `M2(F2)` by

\[
M\sim N\iff M-N\text{ is invertible}.
\]

Its six connection directions are exactly the six rank-two/unit Fourier labels. Exact enumeration gives

\[
\operatorname{SRG}(16,6,2,2),
\]

with eight `K4`s arranged into exactly two partitions of four disjoint cliques. Those two parallel classes give intrinsic row/column coordinates, so the graph is the `4×4` rook/lattice graph `L_2(4)` rather than the Shrikhande graph.

Enumerating all row permutations, column permutations and row/column swap gives its full automorphism group

\[
\boxed{\operatorname{Aut}(L_2(4))\cong S_4\wr C_2},\qquad |\operatorname{Aut}|=1152.
\]

The resulting 1,152 permutations are **exactly** the affine normalizer from Pass5832.

This resolves an old in-repo open item. Pass5671 correctly killed the hypothesis that the Reye two-weight code’s Delsarte graph explained the `S4 wr C2`; the source is instead the **unit-difference Cayley graph** on the 16 matrix/line labels.

## Pass 5839 — outside-box probe 3: the Reye code is a punctured simplex code

The binary simplex `[15,4,8]` code is evaluation of the 15 nonzero linear forms/points of `PG(3,2)`. In coordinates `(w,x) in F2^2 ⊕ F2^2`, delete the projective line

\[
\ell_0=\{(0,x):x\ne0\},
\]

which has three points. Restricting all linear forms to the remaining 12 points gives **exactly** the Reye kernel.

Thus

\[
\boxed{C_{\mathrm{Reye}}=\operatorname{puncture}_{\ell_0}(\mathrm{Simplex}[15,4,8])}.
\]

If `phi!=0`, the deleted line contains exactly two ones, so a simplex weight-8 word becomes weight 6; there are 12 such words and they are precisely the heavy blocks. If `phi=0, psi!=0`, the deleted line is all zeros, so the three remaining nonzero words stay at weight 8. This gives a conceptual proof of

\[
1+12z^6+3z^8.
\]

## Reproduction

```bash
python3 analysis/w33_pass5832_5839_normalizer_code_pauli_allq.py
python3 -m pytest -q tests/test_w33_pass5832_5839_normalizer_code_pauli_allq.py
```

Primary two-qubit prior art used for the published 15-point/9+6 boundary: M. Saniga, M. Planat, P. Pracna, *Projective Ring Line Encompassing Two-Qubits*, arXiv:quant-ph/0611063.

## Boundary

Everything proved here is finite algebra, coding theory, Fourier analysis, graph theory, or publication plumbing. The two-qubit result is stronger than a count match but narrower than a physical identification: it is an explicit isomorphism of the **dual Fourier-label quadratic geometry** with the two-qubit Pauli-point geometry. No q=5 cover point is declared a qubit state, and no dynamics, mass, coupling, continuum limit, or experimental prediction follows from this packet alone.
