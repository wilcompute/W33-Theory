# Pass 1510 — Bidirectional exact-cover saturation and sampler-bias theorem

## Executive result

Pass 1505 enumerated the first 100,000 exact covers through one fixed canonical
frame and reduced them to 327 complete `PSp(4,3)` orbits, certifying at least
3,547,800 covers. Pass 1510 repeats the search with the candidate-frame order
reversed at every branch.

The two deterministic prefixes satisfy

\[
|S_{\rm fwd}|=|S_{\rm rev}|=100000,
\qquad
S_{\rm fwd}\cap S_{\rm rev}=\varnothing.
\]

Nevertheless, exact full-orbit traversal proves that **each prefix independently
hits the identical set of 327 complete group orbits**. Canonical orbit
representatives are frozen by SHA-256

```text
223be23d50147437acfa18cc8f4cea43083c6b87066fe6e26812d0de50c8abb4
```

and the union still has

\[
327\text{ orbits},
\qquad
\sum |\mathcal O|=3547800.
\]

The stabilizer-order census remains

\[
2^{228},\qquad 4^{84},\qquad 8^{15}.
\]

This is strong evidence that the deterministic search has saturated the currently
visible orbit frontier. It is **not** a proof that no additional exact-cover
orbits exist outside both prefixes.

## Sampler-bias theorem

The orbit set is stable, but the within-orbit frequencies are not. If
`f_i,r_i` are the forward and reverse prefix hits in orbit `i`, then

\[
\sum_i f_i=\sum_i r_i=100000,
\]

but only seven of the 327 pairs satisfy `f_i=r_i`. The exact redistribution is

\[
\sum_i |f_i-r_i|=10244,
\qquad
\sum_i(f_i-r_i)^2=463520,
\]

with maximum single-orbit difference 98. The Pearson correlation is

\[
0.9280509607335599,
\]

computed from the exact integer components

\[
964601357,
\qquad
994717730,
\qquad
1086056024.
\]

Thus branch reversal changes frequencies substantially even though it preserves
the observed orbit support. DFS order is therefore suitable for existence and
lower-bound certificates, but not for estimating a uniform distribution on
covers or cover orbits.

## Frozen binary provenance

```text
forward  ee6a429279fece6c4cd917acf2a07fdec2e9f8b66ebe9f7aa0db328ee6ed0172
reverse  e28c3c6c7d5869f93b04c3fc34320f60e65383f82cb3c2484978f46e73bfca5d
```

The repository contains both compiled-search sources and the canonical orbit
reducer. Routine CI validates the frozen certificate and regenerates a fast
100+100 smoke sample. A full 100,000+100,000 rerun is opt-in because the fully
reversed DFS is much slower than the forward ordering.

## Boundary

This theorem certifies objectwise agreement of two disjoint long-run prefixes.
It does not establish completeness of the global exact-cover census, uniformity
of either DFS sampler, or any physical interpretation of the covers.
