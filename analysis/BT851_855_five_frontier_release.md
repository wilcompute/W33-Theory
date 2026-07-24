# Passes 851–855 — modular-factor compatibility, Heisenberg/coalescence separation, Bockstein isolation, adaptive audit control, and optimal generic phase trees

## Cross-cutting correction — Pass 682 v2

The old Pass 682 certificate still treated the retracted unsaturated-image result

\[
[6,6,3,3],\qquad \operatorname{rank}_{3}=4
\]

as a passing check.  The repaired certificate now locks the saturated Pass 808 result

\[
\boxed{[2,2]},\qquad \boxed{\operatorname{rank}_{3}=0}.
\]

The exact W33 chain result is unchanged: the signed-turn spectrum is

\[
-6^{81},\ 2^{120},\ 4^{24},\ 10^{15},
\]

and \(H_1\) is the \(-6\)-eigenspace, so \(S=K+6I\) acts as zero there.  The correction strengthens the separation theorem: there is no cyclotomic three-primary target to realize.  The genuine rank-ten three-primary interface comes from W33 eigenvalue coalescence in the cut/full-\(K\) correspondence.

## Pass 851 — ATLAS-compatible factor fingerprints

Pass 821 decomposed the 66-dimensional mod-two gluing head into factors

\[
\boxed{14,6,40,6}.
\]

The frozen characteristic-two representation catalogue contains unique dimension matches at \(6,14,40\).  The internal invariants sharpen the match:

- the \(6\)- and \(14\)-dimensional factors generate full matrix algebras and are absolutely irreducible over \(\mathbf F_2\);
- the \(40\)-dimensional factor has generated algebra dimension \(800=40^2/2\) and endomorphism dimension two, hence commutant \(\mathbf F_4\) and scalar-extension split \(20+20\);
- the \(6\)-factor occurs twice.

Thus the external labeling problem is reduced from an open module search to a finite standard-generator conjugacy check.  No external label is asserted without that final generator certificate.

## Pass 852 — Heisenberg/coalescence separation

The genuine W33 three-primary correspondence is the absolutely irreducible ten-dimensional module detected simultaneously by:

\[
\text{cut-lattice rank}=10,
\qquad
\text{adjacency coalescence rank}=10,
\qquad
\text{full-}K\text{ gluing rank}=10.
\]

Restriction to the extraspecial qutrit Heisenberg subgroup \(H_{27}\) has radical dimensions

\[
10,9,7,3,1,0,
\]

and therefore Loewy layers

\[
\boxed{1,2,4,2,1}.
\]

The middle layer has dimension four, but it is only an \(H_{27}\)-local filtration layer.  Absolute irreducibility of the full ten-dimensional \(PSp(4,3)\)-module forbids a nonzero proper full-group four-dimensional submodule or quotient.  The saturated cyclotomic flat block has three-primary rank zero, so the local four-layer is not flat-block gluing.

## Pass 853 — scalar Bockstein isolation

For the 81-dimensional mod-two homology representation,

\[
\operatorname{End}(V)=\mathbf F_2 I\oplus\mathfrak{sl}(V)
\]

because \(81\) is odd.  The certified cohomology dimensions are

\[
H^1(G,\operatorname{End}V)=0,
\]

\[
H^2(G,\operatorname{End}V)\cong\mathbf F_2,
\qquad
H^2(G,\mathfrak{sl}V)=0.
\]

Hence the Bockstein

\[
\beta:H^1(G,\operatorname{End}V)\longrightarrow H^2(G,\operatorname{End}V)
\]

has zero image.  Exact integral generator matrices supply compatible actions modulo every \(2^n\), the realized obstruction is zero at every square-zero step, and vanishing \(H^1\) gives uniqueness of the fixed-scalar lift.  The surviving scalar Schur-multiplier line is ambient and isolated from the actual deformation tower.

## Pass 854 — unequal-cost adaptive audit allocation

The four audit streams are assigned explicit physical costs

\[
(1.00,1.35,1.80,1.55).
\]

The exact static cost-minimax LP maximizes

\[
\min_j\sum_i x_i D_{ji}/c_i,
\qquad x_i\ge0,
\qquad \sum_i x_i=1.
\]

Its optimal cost fractions are

\[
\boxed{(0.22382235,0.33215160,0.24078389,0.20324216)}.
\]

A predictable adaptive policy retains 20% robust exploration and sends the remaining 80% to the probe with maximal KL-per-cost for the currently largest past-data likelihood ratio.  Predictability preserves every likelihood-ratio martingale and therefore the equal-weight mixture e-process.

Across 40 deterministic replays per alternative, worst mean physical detection cost falls from

\[
823.1675
\]

to

\[
\boxed{634.85375},
\]

a

\[
\boxed{22.88\%}
\]

improvement.  Every alternative is detected within the 4,000-cost-unit budget, and 200 matched-null replays produce no alarm.

## Pass 855 — exact optimal generic phase trees

The nine primitive affine switching hyperplanes from Pass 825 have

\[
2^9=512
\]

formal sign patterns, but exact LP feasibility leaves only

\[
\boxed{19}
\]

full-dimensional cells in the declared controller box.  Those cells realize

\[
\boxed{16}
\]

generic phases.  The remaining six of the full 22 phases occur only on switching walls as tie strata:

\[
\begin{aligned}
&\texttt{ep|g|o1|t1|t2},\\
&\texttt{ep|h3|g|o1|o2|t1|t2},\\
&\texttt{ep|h3|g|o1|t1|t2},\\
&\texttt{ep|h3|o1|o2|t1},\\
&\texttt{ep|h3|t1|t2},\\
&\texttt{g|t1|t2}.
\end{aligned}
\]

For each of the 54 discrete science chambers, exhaustive dynamic programming over the feasible sign cells produces an exact minimum-depth binary tree using the fixed nine comparisons.  The results are

\[
\boxed{\text{worst optimal depth}=4},
\]

\[
\boxed{\text{mean optimal depth}=3.574074\ldots}.
\]

Thus generic points need at most four comparisons, versus depth nine in the exact nested DAG.  Boundary points and ties remain delegated to the exact 1,000-node Pass 825 runtime.

## Verification boundaries

- Pass 851 proves compatibility and uniqueness by internal invariants, not standard-generator conjugacy.
- Pass 852 identifies the four-dimensional layer only after restriction to \(H_{27}\); it is not a full-group quotient.
- Pass 853 isolates the realized deformation tower but does not compute the full integral cohomology ring.
- Pass 854 is exact for the static unequal-cost LP; the adaptive policy is anytime-valid and replay-superior, not globally optimal over every adaptive strategy.
- Pass 855 is globally depth-optimal for generic cells using the fixed nine hyperplanes.  It does not permit arbitrary new comparisons, and wall points retain the exact DAG fallback.
