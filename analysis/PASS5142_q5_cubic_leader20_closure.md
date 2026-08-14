# Pass 5142 — q=5 cubic leader-20 closure

**Status:** theorem. The q=5 apartment-code distance theorem itself remains open.

Pass 5134 proved that an 18-chamber cut-minimal leader can have as many as 27 adjacent chamber pairs, and that pairwise Delsarte/Bonferroni data alone then falls to a useless weight lower bound of 320. Pass 5140 supplied the missing third-order coefficient: a chamber triple with sorted gallery distances `(1,1,2)` is contained in exactly `q^2` apartments.

The key observation is that an apartment contains only eight chambers. For occupancy `0<=r<=8`,

\[
7\mathbf 1_{r\ \mathrm{odd}}
\ge
7r-14\binom r2+6\binom r3.
\]

Summing over all apartments gives

\[
\operatorname{wt}\ge (S_1-2S_2)+\frac67S_3.
\]

Here `S1` is the chamber-star first moment, `S2` is exactly the pair-overlap quantity already optimized in Pass 5134, and `S3` is the triple-star moment.

For a selected Levi subgraph, let `Y` be its selected-chamber line graph and let `n1=|E(Y)|`. Every non-triangular centered wedge of `Y` is a unique `(1,1,2)` chamber triple. Therefore

\[
N_{112}=\sum_{e\in V(Y)}\binom{\deg_Y(e)}2-3\tau(Y).
\]

Because selected Levi degrees are at most three, `deg_Y<=4`. Convexity gives a lower bound on the first term from `(m,n1)`, while every line-graph triangle is a degree-three selected Levi star and hence `tau(Y)<=floor(n1/3)`.

## Leader 18

Pairwise Delsarte bounds are:

- `n1<=25`: weight at least `800` already;
- `n1=26`: pair bound `520`, but `N112>=26`, so `S3>=650` and the cubic bound is at least `1078`;
- `n1=27`: pair bound `320`, but `N112>=27`, so `S3>=675` and the cubic bound is at least `899`.

Thus every leader-18 word has weight at least

\[
\boxed{800}.
\]

## Leader 19

Deleting any one of the 19 selected Levi edges leaves an 18-edge subcubic girth-eight graph, so Pass 5134 gives wedge count at most 27 after every deletion. If `W` is the original wedge count, the sum of all deletion decrements is `2W`; averaging gives `17W/19<=27`, hence `W<=30`. Equality `W=30` would force every selected edge to have endpoint-degree sum at least five, eliminating all degree-one endpoints. But then

\[
3N_3+2N_2=38,
\qquad
3N_3+N_2=30,
\]

has no integer solution. Hence

\[
\boxed{n_1\le29}.
\]

The remaining branches are:

- `n1<=26`: pair bound `909`;
- `n1=27`: cubic bound at least `1120`;
- `n1=28`: cubic bound at least `869`;
- `n1=29`: cubic bound at least `673`.

Thus every leader-19 word has weight at least

\[
\boxed{673}.
\]

Combining with Pass 5126, every hypothetical q=5 word of weight strictly below `625` must now have minimum chamber leader

\[
\boxed{\ge20}.
\]

This is a strict-counterexample barrier, not the full q=5 distance theorem. Leaders `>=20` remain open, and equality at weight `625` is not classified here.
