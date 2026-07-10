# Five Levi Frontiers — Execution Report

**Status: PASS.** The packet executes the five follow-on programs from the Levi duality-defect theorem in one reproducible witness:

- `analysis/w33_levi_five_frontiers.py`
- `data/PART_2026_07_10_LEVI_FIVE_FRONTIERS_results.json`
- `tests/test_w33_levi_five_frontiers.py`
- `analysis/PART_2026_07_10_LEVI_FIVE_FRONTIERS_insert.tex`

## 1. Odd-order Jordan census

The symplectic quadrangles `W(q)` were rebuilt over `F_3`, `F_5`, `F_7`, and the genuine extension field

\[
\operatorname{GF}(9)=\mathbf F_3[w]/(w^2+1).
\]

For the point-line incidence matrix `M` and Levi operator

\[
D=\begin{pmatrix}0&M\\M^T&0\end{pmatrix},
\]

the deep scan gives:

| q | n | rank M | rank A_point | rank A_line | ranks D,D²,D³,D⁴ | Jordan type |
|---:|---:|---:|---:|---:|---|---|
| 3 | 40 | 25 | 16 | 10 | 50,26,2,0 | `J4^2 + J3^22 + J1^6` |
| 5 | 156 | 91 | 66 | 26 | 182,92,2,0 | `J4^2 + J3^88 + J1^40` |
| 7 | 400 | 225 | 176 | 50 | 450,226,2,0 | `J4^2 + J3^222 + J1^126` |
| 9 | 820 | 451 | 370 | 82 | 902,452,2,0 | `J4^2 + J3^448 + J1^288` |

The values fit the exact closed forms

\[
\operatorname{rank}_2 M=\frac{q(q+1)^2+2}{2},
\quad
\operatorname{rank}_2 A_P=\frac{q(q^2+1)}2+1,
\quad
\operatorname{rank}_2 A_L=q^2+1,
\]

and therefore

\[
D\sim J_4^{\oplus2}
\oplus J_3^{\oplus (q^3+2q^2+q-4)/2}
\oplus J_1^{\oplus q(q-1)^2/2},
\]

with no `J2` blocks. The rank formulas are computationally verified at the four stated orders; they are not promoted here as a literature-level all-odd-q proof.

One part *is* proved for every odd `q` directly from the generalized-quadrangle axiom:

\[
\boxed{D^3=\begin{pmatrix}0&J\\J&0\end{pmatrix},\qquad D^4=0.}
\]

For `p` incident with `L`, exactly `q` other lines through `p` meet `L`; for `p` off `L`, exactly one line through `p` meets `L`. Both counts are odd. Multiplication once more vanishes because every point and line has `q+1` incidences, which is even.

## 2. Integral/discriminant lift

At `q=3`, the two square-zero adjacency differentials have exact sequences

\[
0\to\operatorname{im}A_P\;(16)
\to\ker A_P\;(24)
\to H_P\;(8)\to0,
\]

\[
0\to\operatorname{im}A_L\;(10)
\to\ker A_L\;(30)
\to H_L\;(20)\to0.
\]

The point code has weight enumerator

\[
1+45x^8+1120x^{12}+15570x^{16}+32064x^{20}+\cdots+x^{40},
\]

and the line code has

\[
1+40x^{12}+135x^{16}+672x^{20}+\cdots+x^{40}.
\]

Both are doubly even and self-orthogonal, so

\[
q([x])=\frac{\operatorname{wt}(x)}2\pmod2
\]

is well-defined on `C^perp/C`. Exact symplectic reduction gives Arf invariant zero on both halves:

\[
H_P\cong O_8^+(2)=E_8/2E_8,
\qquad
H_L\cong O_{20}^+(2).
\]

The nonzero isotropic counts are `135` and `524799`. Their direct sum is a rank-28 plus-type discriminant carrier `O_28^+(2)`. This supplies the requested integral-code-lattice explanation of the earlier `8+20=28` split.

## 3. Rank-two terminal selector

The rank-two image is no longer anonymous:

\[
\operatorname{im}D^3
=\langle u_P,u_L\rangle,
\]

where `u_P` is the all-point parity vector and `u_L` the all-line parity vector. Its three nonzero states are

\[
u_P,
\qquad u_L,
\qquad u_P+u_L.
\]

Thus the abstract terminal action is

\[
\operatorname{GL}(2,2)\cong S_3,
\]

permuting point, line, and mirror-sum rails. The two length-four Jordan chains are exactly the two typed parity channels sought by the selector program.

## 4. Typed address/route packet ABI

A packet now carries

```text
(type bit, homology syndrome, 40-bit payload)
```

with an 8-bit syndrome for point/address packets and a 20-bit syndrome for line/route packets.

A legal mirror conversion is

```text
point -> M^T(point) -> line boundary, target syndrome 0
line  -> M(line)    -> point boundary, target syndrome 0
```

for every canonical homology generator. A raw retag without applying the incidence map is rejected on all `8+20=28` canonical generators by the target differential.

The common kernel of the two differentials has dimension 15. Exhaustive enumeration of its `32768` vectors gives:

- `32640`: nonzero syndrome in both namespaces;
- `126`: point-boundary but line-nontrivial;
- `2`: boundary in both namespaces.

Therefore payload validity alone does not erase type: the type bit and syndrome namespace are mathematically necessary.

## 5. Centralizer and middleware bridge

For the q=3 Jordan partition

\[
4^2 3^{22}1^6,
\]

the conjugate partition is `(30,24,24,2)`. The nilpotent centralizer in `GL(80,2)` has order

\[
2^{2056}
\prod_{j=1}^{6}(1-2^{-j})
\prod_{j=1}^{22}(1-2^{-j})
\prod_{j=1}^{2}(1-2^{-j}),
\]

a 618-digit integer, fully emitted in the JSON certificate.

The quotient acting on the two length-four chains is exactly

\[
\operatorname{GL}(2,2)=S_3.
\]

Adjoining the independent phase/inversion bit gives

\[
S_3\times C_2\cong D_{12},
\]

with element-order profile

\[
\{1:1,\;2:7,\;3:2,\;6:2\},
\]

exactly the committed BT856 mirror-bus slot-stabilizer profile. The count bridges are now structural:

\[
8\cdot6=48,
\qquad
8\cdot12=96,
\qquad
24\cdot45\cdot48=51840,
\qquad
25920/12=2160.
\]

The `96` equality is recorded as an order-level bridge; no unverified direct-product identification with the tomotope automorphism group is claimed.

## External context and boundary

Chandler, Sin, and Xiang developed the symplectic incidence-module machinery and explicit rank formulas in defining characteristic for odd-order symplectic spaces, while their characteristic-two companion emphasizes the much richer filtered module structure in characteristic two. The present packet studies a different but adjacent regime: the **cross-characteristic binary Levi operator of odd-order** `W(q)`. The direct parity proof of `D^3=offdiag(J)` is general; the displayed binary rank/Jordan formulas are certified here at `q=3,5,7,9`.
