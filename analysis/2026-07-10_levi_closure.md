# Levi Closure — Five-Track Execution Report

**Status: PASS, with one explicit theorem boundary.** Four tracks close exactly. The universal odd-`q` parity theorem is proved, while the simple all-odd-`q` binary rank formulas are reduced to three precise incidence-code lemmas and remain computationally certified at `q=3,5,7,9`, not mislabeled as proved.

Focused validation: **11/11 tests pass**.

## 1. Odd-order rank theorem

For every odd `q`, the generalized-quadrangle axiom proves

\[
D_q^3=\begin{pmatrix}0&J\\J&0\end{pmatrix},\qquad D_q^4=0.
\]

An incident point-line pair has `q` intermediate alternatives and a nonincident pair has one; both are odd. A fourth incidence step vanishes because every point and line has `q+1` incidences, which is even. Therefore `rank(D^3)=2`, the nilpotency index is exactly four, and there are exactly two maximal `J4` chains for every odd `q`.

The complete proposed Jordan formula is equivalent to

\[
\operatorname{rank}_2M=\frac{q(q+1)^2+2}{2},\quad
\operatorname{rank}_2A_P=\frac{q(q^2+1)}2+1,\quad
\operatorname{rank}_2A_L=q^2+1.
\]

The exact census verifies these at `q=3,5,7,9`, including genuine `GF(9)`. A targeted literature search found defining-characteristic rank theorems, but not a primary proof of these cross-characteristic binary identities. They remain the clean three-lemma all-order frontier.

## 2. Exact PSp(4,3)-module decomposition

Eight symplectic transvections generate faithful order-`25920` actions on both homologies. Exact orbit-and-span enumeration gives

\[
\boxed{H_P\oplus H_L\cong U_8^+\perp U_6^-\perp U_{14}^-}.
\]

All three factors are irreducible. The point module has orbit sizes `120,135`. The six-dimensional line factor has orbit sizes `27,36`; its `27`-orbit is exactly the nonzero isotropic set of `O_6^-(2)`. The fourteen-dimensional factor has orbit sizes

```text
45, 120, 216, 270, 540, 720, 1080, 1440, 2592, 2880, 3240, 3240.
```

Both line factors have Arf invariant one and are orthogonal, so their sum has plus type `O_20^+(2)`. Adding the point sector gives an explicit block embedding

\[
\mathrm{PSp}(4,3)\hookrightarrow O_8^+(2)\times O_6^-(2)\times O_{14}^-(2)
\subset O_{28}^+(2).
\]

## 3. Typed packet ABI is live

`analysis/holonet_typed_packet.py` implements

```text
(type bit, homology syndrome, 40-bit payload)
```

with eight syndrome bits for point/address packets and twenty for line/route packets. Legal mirror conversion applies `M^T` or `M`, toggles type, and lands in a target boundary with syndrome zero. A raw type retag is rejected.

The installed command now exposes:

```text
holonet packet-info
holonet packet-demo
holonet packet-fuzz --seed 3 --trials 1000
```

The deterministic certificate passes `256/256` legal mirrors and rejects `256/256` raw retags.

## 4. BT1880–BT1889 selector boundary closed

The two maximal Jordan chains are explicit:

\[
P_0\to L_1\to P_2\to L_3\to0,
\qquad
L_0\to P_1\to L_2\to P_3\to0.
\]

Both have stage weights `1,4,12,40`. These eight `Z^40` states supply the canonical control basis:

\[
\text{slot }s\longleftrightarrow
(\text{point-seeded stage }s,\text{ line-seeded stage }s)
\longleftrightarrow(\text{BT982 columns }2s,2s+1).
\]

Integral phase inversion is compatible because `D(-v)=-D(v)`. The final selector certificate now has no open chain-boundary stage. This is a control/payload crosswalk; it does not identify the `J4` span with `E8/2E8` homology.

## 5. Exact 48/96 group resolution

The tomotope group is

\[
\boxed{(V_4\oplus V_4)\rtimes S_3\cong S_4\times_{S_3}S_4},
\]

with profile `{1:1,2:27,3:32,4:36}`. The local square and mirror groups are

\[
D_4\cong V_4\rtimes C_2,
\qquad
D_{12}\cong S_3\times C_2.
\]

The runtime order-`48` object is the fiber product

\[
\boxed{G_{48}=D_4\times_{C_2}D_{12}},
\]

with profile `{1:1,2:19,3:2,4:12,6:14}`. Its phase double has order `96` but is not the tomotope group: it contains order-six elements, while the tomotope group has none. Thus `96` is a count bridge through common quotient architecture, not a group isomorphism.

## Consolidated architecture

\[
\boxed{
U_8^+\perp U_6^-\perp U_{14}^-
\longrightarrow\text{typed ABI}
\longrightarrow\text{two J4 rails}
\longrightarrow S_3
\longrightarrow D_{12}\text{ mirror bus}
}
\]
