# Passes 1836–1840 — global signature witness, duad compression, weight-five dependency frontier, geometric chirality, and an ATLAS-standard word

## Executive result

This packet executes the five continuation fronts opened after Passes 1826–1830 while respecting the separately reserved Passes 1831–1835 packing/signature track. The frozen aggregate certificate has SHA-256

```text
3df51bf4293867129b62fa65cb6207ff4247e1b36e86da07dd2cf2d51a797063
```

The exact conclusions are:

1. the complete 720-vector nonlinear signature set admits an exact nine-signature capacity witness,
   \[
   t_1+\cdots+t_9=12\mathbf 1,
   \]
   with type multiset \(6T128+3T96\); the parallel Pass 1835 exact lift search then proves this signature orbit has no frame-level lift, so signature feasibility and cover realizability separate sharply;
2. the tempting \(9\times5\) spread compression is false: the sparse octet graph has maximum partial-spread size six, exactly 72 such packings, and every 30-point packing leaves a canonical 15-point \(KG(6,2)\) duad residual;
3. the binary frame code has exactly 9,600 weight-six codewords, and exactly 185,040 weight-five errors are shadowed by a unique weight-one syndrome;
4. four geometrically fingerprinted outer probes recover the four chiral traces on degrees \(15,24,30,81\) through a trace matrix of determinant 80;
5. an ATLAS-standard generator pair \((c,d)\) is constructed in the canonical 40-point action, and the canonical \(2D\) similitude is expressed by an exact length-18 word in \(c,d,d^{-1}\).

The packet does **not** claim a frame-cover resolution, a complete middle-layer weight enumerator, or the exact weight-five decoder coefficient.

## Pass 1836 — a global nonlinear signature witness

The 720 globally realizable signatures are reconstructed intrinsically from the 45-octet graph. For every anchor octet, its 12 nonneighbors split into three four-cells, and the four realized cell patterns are

\[
(0,2,4),\quad(0,3,3),\quad(1,2,3),\quad(2,2,2),
\]

with orbit sizes \(270,135,270,45\). Every vector satisfies

\[
(A_{45}+4I)t=48\mathbf1,
\qquad
\sum_i t_i=60.
\]

An exact integer solve finds nine distinct signatures with

\[
\boxed{t_1+\cdots+t_9=12\mathbf1}.
\]

Their class multiset is

\[
\boxed{6T128+3T96}.
\]

This changes the logical boundary from Pass 1830. The selected four-packing remains obstructed, but the complete nonlinear signature quotient itself is not globally inconsistent. The independently executed parallel Pass 1835 worker searches the corresponding cover-orbit lift and returns exact UNSAT, so this specific \(6T128+3T96\) signature orbit does not lift to nine pairwise disjoint exact covers.

## Pass 1837 — the six-line plus duad compression theorem

Let \(A_{45}\) be \(\operatorname{SRG}(45,32,22,24)\), and let

\[
C=J-I-A_{45}.
\]

Then \(C\) is \(\operatorname{SRG}(45,12,3,3)\). It has exactly 27 maximal five-cliques. The line-disjointness graph has clique number

\[
\boxed{6},
\]

not nine. There are exactly

\[
\boxed{72}
\]

maximum six-line partial spreads, and every five-clique occurs in exactly 16 of them.

Each maximum packing covers 30 coordinates. The residual 15-coordinate induced graph is

\[
\boxed{\operatorname{SRG}(15,6,1,3)\cong KG(6,2)}.
\]

Thus the exact separator is

\[
\boxed{45=6\cdot5+15},
\]

where the residual 15 coordinates are the duads of a six-set. Between any two five-point line fibers, \(C\) is a perfect matching. Between a line fiber and the duad residual, \(C\) is \((3,1)\)-biregular. This is the correct middle-layer compression architecture and directly matches the previously discovered 15-dimensional duad carrier.

Boundary: this replaces the false \(9\times5\) ansatz but does not yet propagate triangle statistics through the entire middle layer.

## Pass 1838 — weight-six dependencies and the weight-five frontier

All

\[
\binom{240}{3}=2,275,280
\]

weight-three errors are grouped by their 45-bit syndrome. The exact multiplicity census is

\[
1^{1,576,000},\;2^{268,560},\;3^{38,880},\;4^{4,360},\;5^{2,592},\;6^{2,160},\;9^{240}.
\]

There are 478,320 equal-syndrome triple pairs. Exactly 96,000 are disjoint. Every weight-six codeword has exactly ten complementary \(3+3\) decompositions, giving

\[
\boxed{A_6=9,600}.
\]

None of these 9,600 codewords contains one of the 540 canonical weight-four frame codewords.

The exact weight-five population is

\[
\binom{240}{5}=6,363,048,048.
\]

From the weight-four and weight-six dependency layers, exactly

\[
\boxed{185,040}
\]

weight-five errors are shadowed by a weight-one error. Every one has exactly one singleton shadow; there are no duplications in this layer.

The collision-edge contribution already forced by \(A_4\) and \(A_6\) is

\[
A_4\,3\binom{236}{3}+A_6\,10\binom{234}{2}.
\]

The complete formula is

\[
E_5=A_4\,3\binom{236}{3}
+A_6\,10\binom{234}{2}
+A_8\,35\cdot232
+A_{10}\,126.
\]

Therefore the exact weight-five decoder coefficient requires the weight-eight and weight-ten dependency atlas plus overlap-degree deduplication. No coefficient or threshold is claimed prematurely.

## Pass 1839 — four geometric probes for four chirality bits

The four chiral modules have degrees

\[
15,\quad24,\quad30,\quad81.
\]

Four explicit outer elements are identified by order and fixed-object counts. Their trace matrix, with columns ordered by these four module degrees, is

\[
T=
\begin{pmatrix}
3&4&2&3\\
-1&0&4&-3\\
-2&1&-1&0\\
1&0&0&-1
\end{pmatrix}.
\]

The rows correspond respectively to outer probes with geometric fingerprints

\[
(2;8,6,16,7),\quad
(4;0,4,6,3),\quad
(6;0,1,3,3),\quad
(8;2,0,0,1),
\]

where the entries after the order are fixed points, lines, frames, and octets.

The determinant is

\[
\boxed{\det T=80}.
\]

Consequently, the four character coordinates are uniquely reconstructible from four geometric measurements. This converts “four independent sign bits” from an abstract rank statement into an explicit geometric probe code. The first row is the canonical \(2D\) column \((3,4,2,3)\).

## Pass 1840 — an ATLAS-standard pair and a word for the canonical \(2D\)

The official ATLAS standard-generator conditions for \(U_4(2):2\) are:

\[
c\in2C,\qquad |d|=9,\qquad |cd|=10.
\]

The verifier constructs such a pair inside the canonical 40-point action and proves

\[
|\langle c,d\rangle|=51,840.
\]

It independently computes

\[
|C_G(c)|=1,440,
\qquad
|C_G(s)|=96,
\]

so \(c\) is the outer class \(2C\), while the canonical multiplier-minus-one similitude \(s\) is \(2D\).

Writing \(D=d^{-1}\), a shortest word in the alphabet \(\{c,d,D\}\) found by exact breadth-first search is

\[
\boxed{
 s=c d c D^2 c d c d^2 c D c D^2 c D^2.
}
\]

Its expanded length is 18, and direct permutation evaluation returns the literal canonical outer element.

The source for the standard-generator conditions is the official ATLAS of Group Representations page for \(U_4(2):2\). The certificate constructs an ATLAS-standard pair satisfying those conditions; it does not claim literal identity with an independently downloaded ATLAS data-file tuple.

## Verification and evidence boundary

The frozen verifier checks all five self-hashes and the aggregate hash. Focused local regression passes 2/2. The exact light workers reconstruct the signature witness, partial-spread compression, chirality matrix, and standard word. The compiled weight-six worker independently regroups all 2,275,280 triples.

Open boundaries:

- classify other nine-signature orbits and determine whether any orbit beyond the refuted \(6T128+3T96\) orbit admits a frame-cover lift;
- propagate both edge and triangle statistics through the \(6\times5+KG(6,2)\) separator;
- enumerate \(A_8\) and \(A_{10}\) and deduplicate the weight-five collision graph;
- fuse the remaining geometric probes to stable ATLAS class labels beyond the canonical \(2C/2D\) pair.
