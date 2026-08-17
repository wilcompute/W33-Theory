# Passes 6533–6540 — Doily quadratic-evaluation code, dual line reconstruction, and intrinsic \(S_6\) outer automorphism

## Status

**PASS — exact finite binary geometry/coding theorem.** The executable verifier is
`analysis/w33_pass6533_6540_doily_quadratic_evaluation_code.py`; its frozen result is
`data/PART_W33_PASS6533_6540_DOILY_QUADRATIC_EVALUATION_CODE.json`.

This packet closes the highest-value open direction left by S/6501–6532: compute the dual and automorphism group of the complemented-doily-hyperplane \([15,5,6]_2\) code and test whether the full \(Sp(4,2)\) action is intrinsic. It also folds the newer duad/syntheme/ovoid/spread dictionary into one code object.

## Pass 6533 — one canonical evaluation code

Let \(V=\mathbb F_2^4\), with alternating form
\[
B(u,v)=u_1v_2+u_2v_1+u_3v_4+u_4v_3,
\]
and let
\[
q_0(x)=x_1x_2+x_3x_4,
\qquad q_0(u+v)+q_0(u)+q_0(v)=B(u,v).
\]
Evaluate on the 15 nonzero vectors of \(V\):
\[
C=\left\{\big(B(a,x)+tq_0(x)\big)_{x\ne0}:a\in V,\ t\in\mathbb F_2\right\}.
\]
The verifier gives
\[
\boxed{C\text{ is }[15,5,6]_2}
\]
with weight enumerator
\[
\boxed{W_C(y)=1+10y^6+15y^8+6y^{10}}.
\]
The \(t=0\) subcode is the canonical symplectic simplex code
\[
S=\{(B(a,x))_{x\ne0}:a\in V\}\cong[15,4,8]_2,
\]
and
\[
\boxed{C=S+\langle q_0\rangle}.
\]
Thus the five-dimensional object is not a numerical appendage: it is one quadratic coset added to the already-known four-dimensional symplectic simplex.

## Pass 6534 — the dual reconstructs the doily incidence geometry

Exhaustive dual enumeration gives
\[
\boxed{C^\perp\cong[15,10,3]_2}.
\]
Its weight enumerator is
\[
1+15y^3+45y^4+96y^5+160y^6+195y^7+195y^8+160y^9+96y^{10}+45y^{11}+15y^{12}+y^{15}.
\]
There are exactly 15 minimum words. Their supports are exactly the 15 totally isotropic doily lines
\[
\boxed{\{x,y,x+y\}\quad(B(x,y)=0)}.
\]
So the point-line geometry is recoverable from the code alone: coordinates are points; minimum dual supports are lines. This is the decisive strengthening over a weight-enumerator observation.

## Pass 6535 — the three hyperplane species are exactly the three nonzero weight strata

The nonzero words of \(C\) split intrinsically as
\[
\boxed{10\text{ words of weight }6+15\text{ words of weight }8+6\text{ words of weight }10}.
\]
Their zero sets are, respectively,

- 10 nine-point grids (plus-type quadratic hyperplanes), each containing six doily lines;
- 15 seven-point perps, one for each nonzero symplectic linear form;
- 6 five-point ovoids, meeting every doily line once.

Equivalently, the codeword supports are exactly the complements of the 31 geometric hyperplanes. This gives a linear coding coordinatization of the doily Veldkamp point set.

## Pass 6536 — determinant is one distinguished weight-six word

The chosen quadratic word \(q_0\) itself has weight six. In the matrix model \(V\cong M_2(\mathbb F_2)\), its nine zero coordinates are precisely the nonzero singular matrices and its six one-coordinates are the units:
\[
\boxed{15=9_{\det=0}+6_{\det=1}}.
\]
Hence the recent determinant \(9+6\) split is not a separate object. It is one distinguished weight-six / grid-complement word inside \(C\), i.e. one member of the ten plus-type quadratic class.

## Pass 6537 — \(\operatorname{Aut}(C)=Sp(4,2)\cong S_6\) intrinsically

All 720 symplectic matrices act as coordinate permutations preserving \(C\). Conversely, any coordinate automorphism must permute the six weight-ten words. Their five-point zero sets have the stronger property
\[
\boxed{|O_i\cap O_j|=1\quad(i\ne j),}
\]
and their 15 pairwise intersections are all 15 coordinates. Therefore the action on the six weight-ten words is faithful:
\[
\operatorname{Aut}(C)\hookrightarrow S_6,
\qquad |\operatorname{Aut}(C)|\le720.
\]
The 720 symplectic coordinate actions attain this bound, so
\[
\boxed{\operatorname{Aut}(C)=Sp(4,2)\cong S_6.}
\]
This proof needs no separately imported automorphism-group order for the doily.

## Pass 6538 — the exceptional outer automorphism is internal to the code

The 15 minimum dual supports partition into exactly six spreads. Thus the same code canonically produces two six-sets:

1. the six weight-ten words / ovoid zero sets;
2. the six spreads of the 15 minimum dual supports.

For all 720 automorphisms, the verifier compares the two induced cycle types. The exact class correspondence is

| action on ovoid six-set | action on spread six-set | count |
|---|---:|---:|
| \(1\) | \(1\) | 1 |
| \(2\) | \(2^3\) | 15 |
| \(2^2\) | \(2^2\) | 45 |
| \(2^3\) | \(2\) | 15 |
| \(3\) | \(3^2\) | 40 |
| \(3\,2\) | \(6\) | 120 |
| \(3^2\) | \(3\) | 40 |
| \(4\) | \(4\) | 90 |
| \(4\,2\) | \(4\,2\) | 90 |
| \(5\) | \(5\) | 144 |
| \(6\) | \(3\,2\) | 120 |

In particular,
\[
\boxed{2\leftrightarrow2^3,\qquad3\leftrightarrow3^2,\qquad 3\,2\leftrightarrow6,}
\]
which is the exceptional class swap of the nontrivial outer automorphism of \(S_6\). The point is structural: both six-actions are reconstructed from \(C\) itself.

## Pass 6539 — one object now carries the full recent \(S_6\) dictionary

The code unifies the current dictionary without extra choices:
\[
\boxed{6\text{ weight-10 words}\leftrightarrow6\text{ ovoids / letters},}
\]
\[
\boxed{15\text{ weight-8 words}\leftrightarrow15\text{ perps / duads},}
\]
\[
\boxed{10\text{ weight-6 words}\leftrightarrow10\text{ grids / }3+3\text{ partitions}.}
\]
Its dual supplies the 15 synthemes as minimum supports, and the six spread decompositions supply the second six-set needed for the exceptional outer automorphism. The determinant word singles out one of the ten 3+3-partition/grid words.

## Pass 6540 — prior-art and evidence firewall

Saniga, Planat, Pracna, and Havlicek already identified the 31 geometric hyperplanes of the two-qubit doily as the points of its Veldkamp space \(PG(4,2)\), with the familiar 15-perp / 10-grid / 6-ovoid taxonomy (arXiv:0704.0495). Earlier two-qubit ring-line work also identifies the doily with the geometry of the 15 nontrivial two-qubit Pauli classes (e.g. arXiv:quant-ph/0611063). Accordingly, **this packet makes no literature-priority claim for the abstract Veldkamp-space or \(10+15+6\) census**.

The repo-level advance is the explicit quadratic-evaluation realization and executable closure of the chain
\[
\boxed{
C=[15,5,6]
\Longrightarrow
C^\perp_{\min}=\text{doily lines}
\Longrightarrow
\operatorname{Aut}(C)=S_6
\Longrightarrow
\mathrm{Out}(S_6)\text{ from the two intrinsic six-sets}.
}
\]

**Scope boundary.** Everything in this packet is finite binary geometry/coding. It does not establish a canonical map to \(W(3,3)\), CE2, the missing K3 curvature object, a physical Hilbert space, or a continuum/QFT observable. Those identifications remain separate obligations requiring explicit maps and source objects.
