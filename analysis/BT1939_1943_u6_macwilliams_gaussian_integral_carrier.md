# Passes 1939–1943 — U6 super-shard, complete split MacWilliams transform, Gaussian no-descent, integral phase order, and Hodge–Eisenstein carrier separation

## Executive result

All five requested fronts were executed. Passes 1940, 1942, and 1943 close as exact finite theorems. Pass 1939 advances the exact U6 computation by a factor of 26.6 over the previous pilot and exposes cross-shard collisions explicitly, but the global coefficient remains open. Pass 1941 closes the literal Gaussian-to-residual-duad transport and proves that the current unoriented color quotient cannot carry any conjugation-odd phase cut; a global frame-to-chart incidence map is still required.

The aggregate packet verifies 40/40 certificate assertions and 21/21 frozen release assertions.

## Pass 1939 — a 58,282,126-error U6 super-shard

Every fixed-coordinate weight-six error is assigned uniquely by the two smallest remaining coordinates `a<b`. Merging all 28 primitive shards with `b<=8` gives a pairwise-disjoint super-shard of

\[
58{,}282{,}126
\]

errors, 26.6047 times the Pass-1907 pilot and 0.935435% of the full fixed-coordinate chart.

The exact merged census is:

- syndrome groups: `46,732,216`;
- singleton groups: `38,099,164`;
- maximum multiplicity: `65`;
- collision edges: `16,815,942`;
- weight-0/2/4 lower-shadow groups: `1,568,064`;
- lower-shadow singleton groups: `863,754`;
- nonlower super-shard singletons: `37,235,410`.

Counting the 28 primitive shards separately gives `11,426,760` collision edges and `41,309,405` singleton groups. The merged super-shard therefore reveals

\[
\boxed{5{,}389{,}182}
\]

cross-shard collision edges and destroys

\[
\boxed{3{,}210{,}241}
\]

apparent singleton groups that cannot be detected by independent shard accounting.

These are still super-shard-local counts. Shards with `b>8` and partners omitting the fixed coordinate remain unmerged, so no global sixth-order BSC coefficient is promoted.

## Pass 1940 — complete 20+180+40 MacWilliams transform

The exact split MacWilliams transform of the 7,355-bin dual enumerator produces the rank-195 primal code enumerator with

\[
2^{195}
\]

words and

\[
\boxed{39{,}081}
\]

nonzero cells in the `21 x 181 x 41` split array.

The dual complement subgroup `C2 x C2` lies in the code hull. It therefore acts in two ways simultaneously:

1. translation by the phase-40 and residual-plus-pair-200 codewords gives the same three complement symmetries in the primal enumerator;
2. orthogonality to those hull words forces
   \[
   h\equiv0\pmod2,
   \qquad r+p\equiv0\pmod2.
   \]

The minimum shell closes completely:

\[
A_4(4,0,0)=15,
\quad A_4(1,3,0)=120,
\quad A_4(0,4,0)=225,
\quad A_4(0,2,2)=180,
\]

so

\[
15+120+225+180=540.
\]

Every nonzero shell has exact first moments in partition ratio

\[
20:180:40=1:9:2.
\]

For a shell of total weight `w`, the average split weight is therefore

\[
\left(\frac{w}{12},\frac{3w}{4},\frac{w}{6}\right).
\]

This holds for every nonzero shell of the full transformed enumerator, not only the low-weight shells.

## Pass 1941 — literal duad transport and the phase no-descent theorem

The 15 projective Gaussian minimal lines identify literally with the 15 residual vertices through the frozen `residual_to_duad_index` map. Their adjacency is exactly

\[
KG(6,2)=\operatorname{SRG}(15,6,1,3).
\]

The C4-oriented chart uses

\[
y_{\ell,k,c},\qquad \ell=0,\ldots,14,
\quad k\in\mathbb Z_4,
\quad c=0,\ldots,8,
\]

for 540 binary variables. The ordinary color quotient is

\[
x_{\ell,c}=\sum_{k\in\mathbb Z_4}y_{\ell,k,c}.
\]

This quotient has dimension 135 and kernel dimension 405. Complex conjugation sends `k` to `-k`, and the conjugation-odd moment is

\[
\Phi_{\ell,c}=y_{\ell,1,c}-y_{\ell,3,c}.
\]

There are exactly 135 independent such moments, and all 135 lie in the quotient kernel. Equivalently, no linear functional of the unoriented variables `x[l,c]` can equal `Phi[l,c]`.

Thus projective KG incidence and color counts are not merely empirically insensitive to phase: they are exactly incapable of carrying it. Existing pins lift consistently through `sum_k y=x`, but they leave every C4 orientation unresolved.

The current global solver colors 540 frames and does not yet expose a certified residual-duad key for each frame variable. The exact transport therefore closes at the separator chart. A frame-to-chart incidence ABI must be added before the phase cuts can enter the global solver.

## Pass 1942 — the overlapping C4 and C6 phases generate M3(Z)

On the `A6` multiplicity lattice let

- `A` be the natural V9 in the 24-sector;
- `B` be the natural V9 in the 90-sector;
- `C` be the sign-twisted V9 in the 90-sector.

The exceptional-S6 paired carrier supplies the Gaussian quarter-turn

\[
R_4=
\begin{pmatrix}
0&-1&0\\
1&0&0\\
0&0&1
\end{pmatrix},
\]

while the unique Eisenstein phase supplies the sixth-order unit

\[
U_6=
\begin{pmatrix}
1&0&0\\
0&0&1\\
0&-1&1
\end{pmatrix},
\]

whose `B+C` characteristic polynomial is `t^2-t+1`.

The 30 distinct positive words in `R4,U6` through length four generate an additive lattice whose Hermite normal form is exactly `I9`. Therefore

\[
\boxed{\mathbb Z[R_4,U_6]=M_3(\mathbb Z)}.
\]

Consequences:

- rational algebra: `M3(Q)`;
- integral index in `M3(Z)`: 1;
- trace discriminant: 1 in absolute value;
- center and common commutant: scalar integers;
- no quaternionic order and no finite SU(2) enhancement.

The generated unit group is infinite: `R4 U6` has characteristic polynomial

\[
t^3-t^2-1,
\]

and hence spectral radius greater than one.

The previous real `so(3)` result remains the infinitesimal adjacent-plane statement. Integrally, the overlapping Gaussian and Eisenstein phases saturate the full matrix order rather than a quaternion algebra.

## Pass 1943 — Hodge–Eisenstein carrier separator and the charge audit

The two literal V9 carrier embeddings have equal domain Gram and identical graph-holonomy channel, but they lie in different Hodge sectors:

\[
L_1 A_{24}=10A_{24},
\qquad
L_1 A_{90}=4A_{90}.
\]

The exact spectral projectors are

\[
P_{10}(L)=-\frac{L(L-4I)(L-16I)}{360},
\]

and

\[
P_4(L)=\frac{L(L-10I)(L-16I)}{288}.
\]

They satisfy

\[
P_{10}A_{24}=A_{24},\quad P_{10}A_{90}=0,
\]

\[
P_4A_{24}=0,\quad P_4A_{90}=A_{90}.
\]

Thus the normalized Hodge energy

\[
\epsilon(A)=\frac{\operatorname{tr}(A^TL_1A)}{\operatorname{tr}(A^TA)}
\]

is exactly 10 on `A24` and 4 on `A90`.

The ambient character fields give an independent separator:

- `A24`: exact/gauge-gradient sector, field `Q`, degree 1;
- `A90`: coexact/divergence-free sector, field `Q(omega)`, degree 2, conductor 3, phase units `mu_6`.

Therefore the pair

\[
(\text{Hodge eigenvalue},\text{ambient character field})
\]

is `(10,Q)` for `A24` and `(4,Q(omega))` for `A90`. This distinguishes the embeddings even though the 36-dimensional V9 graph-holonomy channel cannot.

### Physical boundary

The sixfold phase is localized to the coexact, divergence-free 90-sector. The exact `15+24` block is the image of the point-to-edge differential and carries the discrete divergence/source channel. Hence the proposed argument that the Z6 phase is supported because it lives in the Gauss-law constraint sector is false for this Hodge decomposition.

The structurally supported interpretation is instead a transverse flux or holonomy phase quantum. Matching the six units to the electric-charge spectrum remains a conditional physical identification; it is not derived here. Likewise, the odd-dimensional phase obstruction of the harmonic 81 is exact, but calling it a neutrino is an analogy rather than a prediction.

## Evidence boundaries

- The split MacWilliams transform, minimum-shell decomposition, integral order, and Hodge–field separator are exact.
- Global U6 remains open beyond the certified 58.28-million-error super-shard.
- The Gaussian chart transport is literal, but the global frame-to-chart incidence map is not yet available.
- `M3(Z)` is an arithmetic multiplicity order, not a physical gauge group.
- The unique Z6 phase is exact; electromagnetism, charge normalization, and generation assignments are not derived.
