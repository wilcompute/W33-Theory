# Sentinel shell matroid: GQ(4,2), 720 weight-12 words, and the 216-circuit S5 orbit

Date: 2026-08-29

**Status: PASS.** Executable:
`analysis/w33_20260829_sentinel_shell_matroid.py`.
Certificate:
`data/PART_W33_20260829_SENTINEL_SHELL_MATROID.json`.

The polarity/sentinel weld identifies the 45 columns of the Hermitian
cross-incidence `B` with all 45 minimum words of the W33 `[40,15,8]_2` code.
This packet asks what the **metric and linear-dependency geometry of those 45
minimum words** remembers.

## 1. The Hamming metric reconstructs GQ(4,2)

Let `b_m` and `b_n` be two distinct minimum words. Their supports are the
eight-point Hermitian neighborhoods attached to carrier labels `m,n`.

The exact integral identity for `B^T B` gives only two possibilities:

- disjoint supports: `|supp(b_m) cap supp(b_n)|=0`;
- intersecting supports: intersection size `2`.

Therefore

\[
d_H(b_m,b_n)=16-2|\operatorname{supp}(b_m)\cap\operatorname{supp}(b_n)|
\]

is either `16` or `12`. Exact comparison with the independently reconstructed
45-point carrier graph gives

\[
\boxed{
m\sim_{GQ(4,2)}n
\iff d_H(b_m,b_n)=16
\iff \operatorname{supp}(b_m)\cap\operatorname{supp}(b_n)=\varnothing.
}
\]

Thus the metric graph at distance 16 on the 45 minimum sentinel words is
exactly `SRG(45,12,3,3)=GQ(4,2)`. Its distance-12 complement has valency 32.

## 2. The complete weight-12 shell is the GQ nonedge set

There are

\[
\frac{45\cdot32}{2}=720
\]

noncollinear carrier pairs. The certificate forms the XOR of each pair and
proves that all 720 results are distinct. Each has weight 12. Since the full
sentinel enumerator has exactly 720 weight-12 words,

\[
\boxed{
\{\text{weight-12 sentinel words}\}
=
\{b_m+b_n:m\not\sim n\},
}
\]

and the pair `(m,n)` is unique.

The 270 collinear pairs likewise give 270 distinct weight-16 words, but they
form only a distinguished suborbit of the much larger weight-16 shell.

## 3. A rank-15 binary matroid of girth five

Regard the 45 columns of `B` as a binary matroid.

- no 1- or 2-dependency exists because the columns are distinct and nonzero;
- no 3-dependency exists because every pair XOR has weight 12 or 16, never 8;
- no 4-dependency exists because all pair XORs are distinct.

Hence the matroid girth is at least five. Exhaustive enumeration of the first
possible shell finds exactly

\[
\boxed{216}
\]

five-subsets with XOR zero. Therefore the matroid has girth exactly five and
exactly 216 five-circuits.

Every such circuit is a five-coclique in `GQ(4,2)`: all ten pairs inside it are
distance 12 / noncollinear pairs. Moreover every one of the 720 GQ nonedges lies
in exactly three of the 216 circuits.

Equivalently, every weight-12 codeword has one two-minimum decomposition and
three complementary three-minimum decompositions.

## 4. The 216 circuits are the PSp(4,3)/S5 orbit

The certificate reconstructs the exact `PSp(4,3)` action on the 45 minimum
words from projective transvections. Four deterministic generators close to

\[
|PSp(4,3)|=25920.
\]

The orbit of one five-circuit is all 216 circuits. Its stabilizer has order

\[
25920/216=120,
\]

and restriction to the five elements of the circuit gives all 120
permutations. Hence

\[
\boxed{
\mathcal C_5\cong PSp(4,3)/S_5,
\qquad |\mathcal C_5|=216,
}
\]

where `C_5` is the set of minimum binary dependencies among the 45 sentinel
minima.

This supplies a new exact source for the project's recurring `216` and `S5`:
they occur intrinsically in the dependency matroid of the Hermitian/sentinel
carrier.

## 5. Boundary: 216 is not automatically the qutrit Clifford group

The project also has the projective one-qutrit Clifford group of order 216.
Nothing here identifies that **group** with this 216-element **coset orbit**.
The equality of cardinalities is potentially suggestive, but an equivariant
bijection or regular Clifford action would require an additional theorem.

The certified statement is exactly the finite one:

\[
45\text{ minima}
\longrightarrow
GQ(4,2)\text{ metric}
\longrightarrow
720\text{ weight-12 words}
\longrightarrow
216\text{ five-circuits}
\cong PSp(4,3)/S_5.
\]
