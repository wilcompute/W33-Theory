# Passes 2560–2567 — Exact orbit, chromatic, representation, and octet-quotient closures

## Executive theorem packet

This packet executes all five post-2557 frontiers and two additional quotient probes. It strengthens the global U6 singleton theorem by a factor exceeding four, reduces the frame-graph chromatic uncertainty to one bit, replaces the conjectural rank-nine character grouping by exact central-projector intersections, and determines the first nonlinear full-group covariant degree. The two outside-box probes identify unexpectedly rigid modulo-two and modulo-three quotients of the common octet edge-phase carrier.

## Pass 2560 — 263 regular global U6 singleton orbits

The deterministic seed-93731 run completes 2,000 exact weight-six tests against the full 91,007,752-syndrome lower shadow and the complete alternative-representative test. It yields 71 lower-shadow hits, 1,666 nonsingleton weight-six fibers, and 263 singleton fibers. Canonicalization under the full effective PGSp action of order 51,840 gives 263 distinct orbit representatives; every stabilizer is trivial. Therefore

\[
U_6^{\rm singleton}\ge 263\cdot 51{,}840=13{,}633{,}920.
\]

The equality problem remains open.

## Pass 2561 — chromatic interval reduced to 10 or 11

The complete K8-link theorem already proves that no nine maximum independent sets partition the frame graph, so \(\chi(H)\ge10\). A new literal assignment of the 540 vertices to eleven colours is checked against all 8,640 graph edges. Its class sizes are

\[
43,44,46,46,47,48,48,49,51,58,60.
\]

Hence

\[
\boxed{10\le\chi(H)\le11.}
\]

No unsuccessful ten-colour heuristic run is used as evidence.

## Pass 2562 — exact rank-nine/PSp character fusion

The PSp action on frames has rank 32. An explicit integer central element of its orbital algebra has eight rational eigenspaces of ranks

\[
60,45,48,162,40,120,64,1.
\]

Exact Lagrange projectors in the rational orbital algebra intersect the nine PGSp-fusion idempotents in an integer matrix. Combining this with

\[
1+3(15)+2(20)+2(24)+4(30)+60+64+2(81)=540
\]

gives

\[
\begin{aligned}
162&=81+81,\\
135&=60+15+30+30,\\
108&=64+24+20,\\
60&=30+30,
\end{aligned}
\]

with the remaining rank-nine spaces carrying \(1,15,15,20,24\). This corrects the earlier tentative claim \(135=15+4\cdot30\).

## Pass 2563 — cubic obstruction, unique septic lift

The official integral four-dimensional \(\chi_{21}\) representation of \(2.U_4(2)\) is reduced at the good prime 1,000,081. Exact modular Reynolds linear algebra closes the group at order 51,840 and gives full-group self-covariant dimensions

\[
\dim\operatorname{Cov}_d(V,V)=1,0,0,1
\quad(d=1,3,5,7).
\]

The Sylow-five normalizer still has dimensions \(1,4,11,24\) in those degrees. Thus all four cubic normalizer covariants die on extension to the full group, but a unique 278-term degree-seven self-covariant survives. The first full-group nonlinear channel is septic.

## Pass 2564 — four tight octet Fourier–MacWilliams shells

For a global signature \(t\), put

\[
u=3t-4\mathbf1,
\qquad
v=H^Tt-4\mathbf1=\frac13H^Tu.
\]

On all 720 signatures,

\[
HH^Tu=12u,
\qquad
Hv=4u,
\qquad
\|v\|^2=\frac43\|u\|^2.
\]

The vectors \(v\) split into four zero-sum tight frames on the same 20-dimensional space, of sizes 45, 270, 135, and 270. Their squared norms are 192, 288, 480, and 576. This is an exact common spectral carrier linking cover signatures to syndrome geometry.

## Pass 2565 — abstract Schläfli incidence from the mod-two quotient

Reducing the 240-coordinate vectors \(v\) modulo two gives exactly 72 patterns: 45 of weight 64 and 27 of weight 160. The 27 heavy patterns, adjacent when their intersections have size 112, form

\[
\operatorname{SRG}(27,10,1,5).
\]

Each light pattern is incident with the three heavy patterns meeting it in 64 coordinates. These incidence triples are exactly all 45 triangles of the 27-vertex graph. Every heavy pattern lies in five triples. The induced graph on the 45 triples has parameters \((45,12,3,3)\), the complement of the octet \(\operatorname{SRG}(45,32,22,24)\). Thus the quotient is precisely the abstract Schläfli 27-line/45-tritangent incidence structure.

## Pass 2566 — rigid 360-class mod-three quotient

The triangle-incidence matrix has rank 44 over \(\mathbf F_3\). Reducing the 720 vectors \(v\) modulo three gives exactly 360 classes:

\[
45\times1,
\qquad270\times2,
\qquad45\times3.
\]

Across all 405 pairs lying in one residue class, the signature difference has exactly four \(+3\), four \(-3\), and 37 zeros, while the divided edge-phase difference has 48 \(+1\), 48 \(-1\), and 144 zeros. There is exactly one within-class difference type.

## Evidence firewall

All promoted statements are finite exact computations with frozen semantic hashes. The unresolved U6 equality, ten-colour existence, carrier-level physical interpretation of the septic covariant, algebraic cubic-surface coordinates, and any external interpretation of the 360-class quotient remain explicitly open.
