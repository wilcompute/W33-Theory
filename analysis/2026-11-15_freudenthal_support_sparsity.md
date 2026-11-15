# Sparsity of the Freudenthal pairing over all 40 quiver supports

The four-dimensional invariant contains the derivative pairing $\langle dN(p),dN^\vee(q)\rangle$ of the electric and magnetic cubics. The [previous calculation](2026-11-15_cubic_quiver_five_checks.md) found that all 100 ordered pairs were required in a fixed ten-support formula. Here the allowed indices range over all 40 supports of the [cubic del Pezzo quiver](2026-11-15_cubic_quiver_steiner_reconstruction.md). The minimum is still 100 for positive-semidefinite coupling forms, with all minimizers classified. It is also 100 for arbitrary scalar couplings that use exactly ten charts on either leg. [Ceresole, Ferrara and Marrani, 4d/5d correspondence](https://arxiv.org/abs/0707.0964)

## Incidence and the constraints

Let $S$ be the $40\times45$ chart–tritangent mask matrix, with column $v_t$ for term $t$. Each column has 24 ones. Let $B$ be the point–line incidence matrix of $Q(4,3)$, with columns $b_\ell$. Each point is on four lines and each line has four points. The overlap calculation gives $SS^{\mathsf T}=15J+3BB^{\mathsf T}$. Since the constant vector is in the span of the columns of $B$, the two column spaces agree. Write $V$ for this 25-dimensional space. These polar lines are distinct from the 27 lines of the complex cubic surface.

An ordered pair matrix $W$ uses the coefficient $W_{pq}$ on the derivative pairing of chart $p$ with chart $q$. In the fixed signed tritangent bases it recovers the target exactly if

$$v_t^{\mathsf T}Wv_u=1$$

for every ordered pair of tritangents that share a cubic-surface line, including $t=u$. There are 585 such tests. A derivative monomial determines its tritangent because a pair of intersecting lines determines their third line, so their nonzero signed coefficients cancel when comparing the restricted polynomial to the full one.

## Global positive-semidefinite minimum

Suppose $W$ is real symmetric and its restriction to $V$ is positive semidefinite. For neighboring tritangents the three prescribed values give $(v_t-v_u)^{\mathsf T}W(v_t-v_u)=0$. Positivity makes every such difference orthogonal to all of $V$ under the form. The tritangent graph is connected, so all the columns represent the same unit vector in the quotient by the radical. Consequently the pairing is one on every pair of tritangents, including the unmeasured pairs.

Each $b_\ell$ is a combination of the $v_t$ with coefficient sum $4/24=1/6$, by comparing its coordinate sum. Thus

$$B^{\mathsf T}WB=\frac1{36}J.$$

The converse also follows from the equal spans and coordinate sums. Every nonzero $W_{pq}$ can affect just $4\cdot4=16$ entries of the polar line-pair matrix. Its 1,600 nonzero entries require at least 100 ordered chart pairs. The same bound holds for any exact reconstruction with $B^{\mathsf T}WB=J/36$, regardless of positivity.

At 100 pairs their 16-entry rectangles must cover the line-pair matrix without overlap, so all 100 weights equal $1/36$. If $W$ is positive semidefinite on all 40 coordinates, any active row must have positive diagonal. Two active points on the same polar line would give overlapping diagonal rectangles. The active points therefore form a partial ovoid, and ten are necessary to cover all lines. Exactly ten form an ovoid $O$. Thus the minimizers under full positive semidefiniteness are precisely the 36 matrices $\mathbf1_O\mathbf1_O^{\mathsf T}/36$.

## Stability under coefficient error

The same 100-pair bound survives a small uniform error. The verifier checks that the tritangent graph has diameter two. In a positive-semidefinite form, an error of at most $\varepsilon$ in each prescribed coefficient gives squared distance at most $4\varepsilon$ on each graph edge, and at most $16\varepsilon$ between any two tritangent columns by the triangle inequality. With both diagonal values within $\varepsilon$ of one, the real bilinear value on any pair is within $9\varepsilon$ of one.

For each polar line $\ell$, the verifier gives $b_\ell$ explicitly as a combination of tritangent columns. The coefficient is $-7/54$ when the tritangent is present in none of the four charts on $\ell$ and $1/27$ when it is present in three. There are nine of the first type and 36 of the second, so the expansion has $\ell^1$ norm $5/2$. Every entry of $B^{\mathsf T}WB$ is therefore within $(225/4)\varepsilon$ of $1/36$. For $\varepsilon<1/2025$ no entry can vanish, which gives the 100-pair bound even for this approximate reconstruction.

## Arbitrary scalar couplings on a ten-chart leg

Fix $t$ and sum the five equations across a cubic-surface line in $t$. Each chart keeps three of those five terms. For the row marginal $r=W\mathbf1$, this gives $S^{\mathsf T}r=(5/3)\mathbf1$ and hence $B^{\mathsf T}r=(5/18)\mathbf1$. The analogous condition holds for the column marginal. Each must meet all 40 polar lines. In particular, if exactly ten rows of $W$ are active, they form an ovoid.

For an ovoid on the left, restrict the ordered-pair system on the right to 25 independent chart rows of $S$. Its 250-column matrix has a full modular minor over $\mathbb F_{101}$, proving full rank over characteristic zero. The verifier transports this to all 36 choices using the Weyl generators. Thus the equations fix each active row's response on $V$ separately. An ovoid product on the right gives the response explicitly, so each row gives every right polar line weight $1/36$. Each of the ten rows must therefore contain at least ten nonzero entries. In the 100-entry case each row independently uses an ovoid on the right, with weights $1/36$. This describes the ten-row optima even for signed or complex weights. The transposed argument applies when the right leg uses exactly ten charts. [Ball, ovoids and dual spreads](https://web.mat.upc.edu/simeon.michael.ball/ovoidsofO5q.pdf)

## Entrywise positive couplings

The certificate exhibits an integer symmetric perturbation $H$ supported in an 18-chart principal block. It is invisible on all 585 measured tritangent pairs and changes at least one polar line-pair value. Adding a sufficiently small rational multiple of $H$ to the uniform matrix $J/576$ gives a strictly entrywise positive solution whose restriction to $V$ is indefinite. Thus exact recovery and entrywise positivity leave some line-pair weights undetermined. The general signed and entrywise nonnegative support minima with more than ten active charts on each leg remain open.

The exact rational ranks on $V$ are 205 for the symmetric constraints and 186 for the alternating constraints. Together they leave a $25^2-391=234$ dimensional family of invisible bilinear perturbations, of which 120 are symmetric. A finite CP-SAT search for 50 equal-weight ordered pairs ended with status unknown.

Replay with NetworkX and SymPy.

    python -B analysis/toe_20261115_freudenthal_support_sparsity.py

The [certificate](../data/toe_20261115_freudenthal_support_sparsity.json) includes the modular rank and an exact rational witness for the entrywise positive case. Positive semidefiniteness here is a mathematical condition on the support pairing. A physical derivation of that condition in a compactification with a faithful charge dictionary remains open.
