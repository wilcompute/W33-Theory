# BT818 — The Heptad No-Go: alpha = 7, and Two Corpus Corrections

Full read of self_entanglement_companion.tex + exact computation on the
Witting rays.  Three results; two correct standing claims in the corpus.

## T1: alpha(W(3,3)) = 7 = Phi6  (CORRECTION to the GraphTheory table)

Exact maximum independent set of the collinearity graph, verified by two
independent methods (branch-and-bound + networkx exact max-clique of the
complement):

```text
alpha = 7        ratio/Lovasz bound = 10        gap = 3 = q
```

Consequences for docs/index.html ("Perfect Graph Partition" block):
- "alpha = 10 = ovoids of GQ(3,3)" is FALSE: W(q) has ovoids only for
  q even (Thas), and the true maximum partial ovoid has size 7.
- "chi = 4" is impossible (a 4-coloring needs alpha >= 10); in fact
  chi >= ceil(40/7) = 6.
- The "perfect graph" (chi x alpha = 40) and "Shannon Theta = 10 = alpha"
  claims collapse with it.  Theta is only bracketed: 7 <= Theta <= 10.

The optimal 7-set is a HEPTAD of seven pairwise non-orthogonal rays with
ALL overlaps exactly 1/3 = 1/q - seven equiangular lines in C4.  The
Csaszar seven (Phi6) reappears as the substrate's independence number.

## T2: the KS optimum is >= 36, not <= 34 (CORRECTION to the companion)

The companion's Witting Kochen-Specker theorem claims at most 34/40
contexts simultaneously satisfiable.  Local search finds markings
satisfying 36/40 (size 13 = Phi3, misses 4 = mu), so the stated bound is
wrong; 36 = (q!)^2 = the spread count.  True maximum lies in [36, 39]
(40 is impossible: an exactly-once marking of all contexts is an ovoid).

## T3: the Bell-line shell IS the entanglement stratification

The companion's Bell-line decomposition 1 + 12 + 27 and BT817's
entanglement strata are the same object, identified exactly: the unique
all-product context is the line L0; the 12 contexts meeting L0 each
contain exactly one product ray; the 27 skew contexts are fully
self-entangled.

## Boundary

Open: the exact KS maximum (36, 37, 38, or 39 - needs exact search or a
better bound); the heptad's geometry (orbit structure of equiangular
7-sets under PSp; relation to the Csaszar/F42 world); chi(W33) exactly
(>= 6); and propagating the corrections into docs/index.html and the
companion tex.
