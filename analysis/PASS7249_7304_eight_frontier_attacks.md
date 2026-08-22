# Passes 7249–7304 — Eight deep frontier attacks

This packet executes the five open attacks from the previous frontier and adds three deliberately outside-the-box probes. The common rule throughout is fail-closed: a negative canonicity result is recorded as such, and q=9 search evidence is not promoted into an upper bound.

## 1. The 36 doily slices form an exact two-sided spectral design

Let `N` be the 45×36 matrix whose column for a double-six is the indicator of its 15 disjoint tritangents. Let `A36` be the double-six graph and `A45` the tritangent-sharing graph. Exact replay gives

\[
N^TN=12I_{36}+3J_{36}+3A_{36},
\]

\[
NN^T=9I_{45}+3J_{45}+3A_{45}.
\]

Here

\[
A_{36}=\operatorname{SRG}(36,20,10,12),
\qquad
A_{45}=\operatorname{SRG}(45,12,3,3).
\]

Therefore

\[
\operatorname{spec}(N^TN)=180^1\oplus18^{20}\oplus0^{15}.
\]

After centering,

\[
X=N-\frac13J,
\]

we obtain the exact intertwiner

\[
\boxed{2A_{45}X=3XA_{36}}.
\]

The 36 centered columns have squared norm 10 and pairwise inner product 1 or -2 according as the double-sixes are adjacent or nonadjacent in `H36`. All 20 nonzero Gram eigenvalues are 18. Thus `X/sqrt(18)` is a partial isometry between the 20-dimensional primitive eigenspaces `A36:2` and `A45:3`.

## 2. One doily slice reconstructs the full binary spread code under PSp(4,3)

A single double-six has a 36-element orbit under the exact `PSp(4,3)` action already implemented in the repo. The 36 orbit columns are exactly all doily-slice columns, and their binary span has dimension 21:

\[
\boxed{\langle PSp(4,3)\cdot N_D\rangle_{\mathbb F_2}=C_{\rm spread}=[45,21,5]_2.}
\]

Moreover, the overlap relation of those orbit columns reconstructs `H36` itself:

\[
|S_D\cap S_{D'}|=6\iff D\sim D',
\qquad
|S_D\cap S_{D'}|=3\iff D\not\sim D'.
\]

So one local doily section plus the ambient group action is enough to recover the full 45-coordinate code and the double-six graph.

## 3. D4 triality is a genuine canonicity obstruction

Pass7182 found diagonal `D4+D4` glue

\[
\{(0,0),(v,v),(s,s),(c,c)\}.
\]

The normalizer arithmetic is

\[
|W(D_4)|=192,
\]

and for an unordered orthogonal `D4+D4` pair

\[
|\operatorname{Stab}|=2\cdot192^2\cdot6=442368.
\]

Since

\[
|W(E_8)|/442368=1575=3150/2,
\]

the extra factor 6 is exactly the simultaneous triality `S3` acting on the two `D4` factors. It permutes

\[
(v,v),\ (s,s),\ (c,c)
\]

transitively while preserving the diagonal glue.

Hence the requested attempt to assign a **single intrinsic** `v/s/c` label to a doily grid fails canonically:

\[
\boxed{\text{a bare orthogonal }D_4\oplus D_4\text{ coordinate carries an }S_3\text{-torsor, not one distinguished triality class}.}
\]

A triality choice therefore requires additional orientation/basis data.

## 4. The exceptional S6 outer automorphism does not extend through the ambient double-six stabilizer

For one fixed double-six, the exact stabilizers are

\[
|\operatorname{Stab}_{PSp}(D)|=720,
\qquad
|\operatorname{Stab}_{W(E_6)}(D)|=1440.
\]

But both have image of order 720 on the 15-tritangent doily slice. The extra kernel has order 2. Its nontrivial element swaps the two sixers of the double-six in six transpositions, fixes the 15 complementary `c_ij` cubic lines, and commutes with the `S6` stabilizer.

Therefore the extra ambient `C2` is a **central double-six swap**, not the exceptional outer automorphism of `S6`.

The code itself makes this boundary even stronger. Exhausting the binary `[45,21,5]` code yields exactly 27 weight-five words. They are precisely the 27 cubic-line stars: for each cubic line, the five tritangents through it. The intersection graph of these minimum supports is exactly the 27-line cubic-surface meet graph.

Thus the code reconstructs the entire 27-line/45-tritangent incidence geometry from its minimum words. Using the classical fact that the Schläfli/cubic-surface automorphism group has order 51840, this gives

\[
\boxed{\operatorname{Aut}(C_{\rm spread})=W(E_6).}
\]

So there is no hidden larger coordinate-automorphism group in which a local exceptional-`S6` involution could extend while preserving the chosen doily section.

## 5. q=9: the proposed direct doily-code restriction is not canonical

The `[15,5,6]_2` doily code lives on the 15 tritangent coordinates of an `E6`/cubic-surface section. A q=9 partial ovoid lives on points of `W(3,9)`. There is no canonical point-to-tritangent restriction map, so forcing the q=3 doily code directly onto the q=9 witness would be importing an unproved identification.

The correct q=9-native local obstruction is intersection with embedded symplectic `W(3,3)` subgeometries. Any such intersection is a partial ovoid of `W(3,3)` and therefore has size at most 7.

For the frozen 51-point q=9 witness:

- the standard `F3`-fixed `W(3,3)` section meets it in 4 points;
- the eight diagonal-torus sections have intersection histogram
  `0^1 1^1 2^2 3^3 4^1`;
- a deterministic breadth-first scan of 20,000 embedded sections under six non-`F3` symplectic transvections gives

\[
0^{276},\ 1^{2453},\ 2^{7343},\ 3^{7291},\ 4^{2305},\ 5^{322},\ 6^{10}.
\]

No scanned section hits 7. This is search evidence only, not an exhaustive section orbit and not an upper bound for `alpha(W(3,9))`.

## Outside-box A — a ternary shadow code appears

The same doily-slice matrix has a striking characteristic-3 reduction. Since all raw self/intersection numbers are divisible by 3,

\[
N^TN\equiv0\pmod3.
\]

The integer Smith form has nonzero diagonal

\[
\boxed{1^{14}3^7}.
\]

Therefore the ternary column span has dimension 14 and is self-orthogonal. Exhausting all `3^14` words gives

\[
\boxed{[45,14,15]_3}
\]

with weight enumerator

\[
1+72y^{15}+6420y^{18}+19440y^{21}+336060y^{24}+1109420y^{27}
+1781136y^{30}+1215720y^{33}+295170y^{36}+18360y^{39}+1080y^{42}+90y^{45}.
\]

Most strikingly, the 72 minimum words are **exactly**

\[
\boxed{\pm\{\text{36 doily-slice columns}\}}.
\]

The seven 3-primary Smith factors are therefore an actual integral invariant. No physical meaning is assigned to them here.

## Outside-box B — q=9 blocker columns form an exact regular simplex

Let `B` be the 769×51 blocker-incidence matrix of the frozen q=9 witness: rows are outside points, columns are witness points, and `B[v,s]=1` when the outside point is collinear with witness point `s`.

Because the witness is independent in `SRG(820,90,8,10)`, exactly

\[
\boxed{B^TB=80I_{51}+10J_{51}}.
\]

After integer centering,

\[
Y=51B-(B\mathbf1)\mathbf1^T,
\]

we obtain

\[
\boxed{Y^TY=208080I_{51}-4080J_{51}},
\]

with rank 50. Hence the 51 centered blocker columns are the vertices of an exact regular simplex in a 50-dimensional real space.

## Outside-box C — the third blocker moment exposes a 103-edge triad hypergraph

The universal second moment does not distinguish this particular 51-set, so the next layer is the common-center count of witness triads. Every witness triple has either 1 or 10 common neighbors:

\[
\boxed{1^{20722}\oplus10^{103}}.
\]

The 103 ten-center triples form a 3-uniform hypergraph on the 51 witness points. Its binary incidence rank is full:

\[
\boxed{51}.
\]

Its vertex-degree histogram is

\[
3^6,\ 4^4,\ 5^{12},\ 6^{12},\ 7^7,\ 8^6,\ 11^2,\ 12^2,
\]

and among used pairs, 285 occur once and 12 occur twice. This is a genuinely witness-specific third-moment fingerprint that can be fed into future exchange/ILP cuts.

## Claim boundary

All new claims in this packet are finite combinatorial, coding-theoretic, representation-theoretic, or deterministic-search statements. The q=9 optimum remains open; no 52-set is ruled out. The triality result is explicitly a **non-canonicity theorem**. The ternary and Smith-form phenomena are recorded without physical interpretation.
