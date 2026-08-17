# Passes 5776–5783 — Reye/Latin common 9-space and the outer/sign split

## Scope

This packet starts from the frozen Pass5667–5674 q=5 certificate and does **not** import a new geometric model.  The inputs are exactly:

- the 12 moving cover cells,
- the 16 zero-containment triples (already certified as the Reye `12_4,16_3` configuration),
- the 12 multiplicity-six heavy supports,
- the exact rank-three carrier character pairings, and
- the already certified outer carrier involution and point-side sign character.

The new result is an exact reconstruction theorem tying those ingredients together.

## Pass 5776 — the two incidence systems have one centered Gram operator

Let

- `H` be the `12 x 12` incidence matrix between the moving cover points and the 12 heavy six-subsets;
- `R` be the `12 x 16` incidence matrix between the same points and the 16 Reye triples;
- `J=J_12`.

The frozen data give row/column sums

\[
H:\ 6/6,
\qquad
R:\ 4/3.
\]

Direct exact multiplication gives

\[
\boxed{
HH^T-3J=RR^T-J=:K_9.
}
\]

Moreover

\[
\boxed{K_9^2=4K_9},
\qquad
\boxed{\operatorname{rank}_{\mathbb Q}K_9=9},
\qquad
\operatorname{tr}K_9=36.
\]

Therefore

\[
\boxed{P_9=\frac14K_9}
\]

is a rational orthogonal projector of rank nine.

This is stronger than the Pass5667 character-inner-product statement.  The heavy shell and Reye shell do not merely share some constituent: their **centered incidence Grams are identical on the point carrier**.

## Pass 5777 — the projector reconstructs an intrinsic `3 x 4` system

Every diagonal entry of `K_9` is `3`; every off-diagonal entry is `0` or `-1`.  Define

\[
A_{\mathrm{blk}}=3I_{12}-K_9.
\]

Then `A_blk` is the adjacency matrix of

\[
\boxed{3K_4}.
\]

On the moving-twelve labels the three components are

\[
\boxed{
\{1,3,8,10\},\quad
\{2,5,7,12\},\quad
\{4,6,9,11\}.
}
\]

In the original thirteen-cover positions these are

\[
\boxed{
\{2,8,11,3\},\quad
\{13,6,5,9\},\quad
\{10,4,7,12\}.
}
\]

After block-ordering,

\[
K_9=I_3\otimes(4I_4-J_4),
\qquad
P_9=I_3\otimes\left(I_4-\frac14J_4\right).
\]

Hence the 9-space is simply the direct sum of the three within-block zero-sum spaces.  Its orthogonal complement is the 3-space of block-constant functions, which splits as the global constant plus a 2-dimensional block-contrast space.

So the point permutation module has the explicit dimension decomposition

\[
\boxed{\mathbb Q^{12}_P=\mathbf1\oplus U_{2,P}\oplus W_9.}
\]

## Pass 5778 — the Reye shell is literally the Klein `V4` Latin square

Every one of the 16 Reye triples meets each `K4` component exactly once.  More strongly, for every pair of components, every cross-pair occurs in exactly one Reye triple.  Thus the zero shell is a transversal design

\[
\boxed{TD(3,4)}.
\]

Equivalently it is the incidence geometry of a Latin square of order four.

With the component order printed by the verifier, the raw table is

\[
\begin{pmatrix}
2&0&3&1\\
0&2&1&3\\
3&1&2&0\\
1&3&0&2
\end{pmatrix}.
\]

The symbol relabel

\[
(0,1,2,3)\mapsto(1,3,0,2)
\]

turns this into

\[
\boxed{
\begin{pmatrix}
0&1&2&3\\
1&0&3&2\\
2&3&0&1\\
3&2&1&0
\end{pmatrix}
}
\]

which is the Cayley table of `V4 = F_2^2` under XOR.

An explicit q=5 cover-coordinate chart is therefore

\[
\begin{aligned}
\text{row }0,1,2,3&\leftrightarrow 2,8,11,3,\\
\text{column }0,1,2,3&\leftrightarrow 13,6,5,9,\\
\text{symbol }0,1,2,3&\leftrightarrow 7,10,12,4,
\end{aligned}
\]

with incidence law

\[
\boxed{s=r\oplus c.}
\]

This upgrades the earlier action-level conjugacy to an object-level reconstruction from the q=5 zero shell itself.  The coordinate names `row/column/symbol` remain gauge choices under the full autoparatopy group; the `TD(3,4)` object is intrinsic.

## Pass 5779 — the heavy shell is the complementary intercalate class

There are

\[
\binom42^3=216
\]

balanced six-subsets choosing two points from each of the three four-blocks.
Count how many of the 16 Reye/Latin triples lie entirely inside such a six-set.  The complete spectrum is

\[
\boxed{
0^{12}\oplus2^{192}\oplus4^{12}.
}
\]

The two exceptional 12-sets are exact:

- the `4`-line class is precisely the set of the 12 intercalate supports of the Klein Latin square;
- the `0`-line class is precisely the 12 multiplicity-six heavy supports from the q=5 multidesign;
- complementing inside the moving twelve exchanges the two classes.

Thus

\[
\boxed{
\text{heavy support}
=\text{complement of a Klein intercalate support}.
}
\]

This reconstructs the heavy shell from the zero shell without referring back to multiplicity six.  It does **not** produce a preferred point-to-heavy bijection.

## Pass 5780 — exact rank-three module decomposition

Pass5667 already proved that each of the point, heavy and Reye-line permutation characters has norm three and that every pair has inner product two.  Each transitive rank-three permutation module is therefore multiplicity-free with two nontrivial irreducible constituents.

The incidence matrices above have rank ten, while their centered versions have rank nine.  Hence the shared nontrivial constituent is exactly `W_9`.  The dimension decompositions are

\[
\boxed{
\mathbb Q^{12}_P=\mathbf1\oplus W_9\oplus U_{2,P},
}
\]

\[
\boxed{
\mathbb Q^{12}_H=\mathbf1\oplus W_9\oplus U_{2,H},
}
\]

and

\[
\boxed{
\mathbb Q^{16}_L=\mathbf1\oplus W_9\oplus V_6.
}
\]

So the mysterious pairwise character overlap `2` has a concrete meaning:

\[
\boxed{\text{trivial line }+\text{ one common irreducible 9-space}.}
\]

## Pass 5781 — outer twist and sign twist act in fundamentally different ways

Pass5674 already constructed an order-two outer automorphism carrying the point-stabilizer class to the heavy-stabilizer class.  Since the point and heavy modules share a **unique** 9-dimensional nontrivial constituent and the outer map is involutive, it must fix that common constituent and exchange the two distinct 2-dimensional spokes:

\[
\boxed{
W_9\mapsto W_9,
\qquad
U_{2,P}\leftrightarrow U_{2,H}.
}
\]

The point-side sign tensor twist behaves differently.  Pass5674 gave

\[
\langle\varepsilon\pi_P,\pi_H\rangle
=\langle\varepsilon\pi_P,\pi_L\rangle=0.
\]

Its frozen odd-element fixed-count distribution is

\[
0^{168},\quad2^{108},\quad6^{12}.
\]

Because `\langle\pi_P,\pi_P\rangle=3`, this also yields

\[
\langle\varepsilon\pi_P,\pi_P\rangle
=\frac{3\cdot576-2(108\cdot2^2+12\cdot6^2)}{576}=0.
\]

Therefore

\[
\boxed{
\varepsilon\otimes\mathbb Q^{12}_P
\perp
\mathbb Q^{12}_P\oplus\mathbb Q^{12}_H\oplus\mathbb Q^{16}_L.
}
\]

So the two operations are sharply separated:

- **carrier outer involution:** preserves the common 9-core and swaps 2-dimensional spokes;
- **point sign tensor:** moves the entire point packet to a disjoint character sector.

## Pass 5782 — the two order-576 groups are now explicitly disambiguated

There is no contradiction between Pass5300 and Pass5667 once the producer maps are kept straight.

Pass5300 concerns the projective-symplectic Hoffman-cover stabilizer

\[
H\cong2_+^{1+4}:(S_3\times C_3),
\qquad |H|=576,
\qquad Z(H)\cong C_2.
\]

Pass5417 instead defines `act` as the **permutation image on the thirteen cover cells of the full graph-automorphism stabilizer**.  Its frozen producer certificate is

\[
\boxed{
\mathrm{act}\cong2^4:(S_3\times S_3),
\qquad |\mathrm{act}|=576,
\qquad Z(\mathrm{act})=1.
}
\]

That centreless group is exactly the group appearing in the Reye/Latin reconstruction above.  Pass5300 already related the *quotient* `H/Z(H)` to the even Latin subgroup; this packet does not identify `H` with the full Latin autoparatopy group.

## Prior-art boundary

The classical `12_4,16_3` Reye configuration is old.  In particular, Monson, Pellicer and Williams, *The tomotope*, **Ars Mathematica Contemporanea 5** (2012), 355–370, DOI `10.26493/1855-3974.189.e64`, identify the tomotope medial layer graph with the Levi graph of Reye's configuration and record automorphism-group order 576.

Those facts are prior art.

What is new **inside this repository packet** is the exact bridge from the q=5 W33-derived multidesign certificate:

1. its Reye zero shell and heavy shell have the same centered rank-nine Gram projector;
2. that projector reconstructs the `3 x 4` block system;
3. the Reye shell becomes an explicit Klein `V4` `TD(3,4)` in the q=5 labels;
4. the heavy shell is exactly the complementary intercalate class; and
5. this forces the `1+9+2`, `1+9+2`, `1+9+6` representation decomposition and the outer/sign distinction.

## Evidence boundary

Everything here is a finite incidence, Latin-square, permutation-module, and exact rational-matrix statement.  It does not derive continuum dynamics, particle content, gauge interactions, measured masses or couplings, or physical unification.
