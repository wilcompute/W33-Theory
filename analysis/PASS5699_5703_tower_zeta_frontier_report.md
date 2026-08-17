# Pass5699--5703 corrected report: a separate finite factor-pair tower

## Corrected outcome

This packet now has a reproducible, bounded result: three explicit balanced
2-lifts of the W(3,3) Levi graph form a **separate deterministic factor-pair
tower** on \(80,160,320,640\) vertices.  The tower supports standard Artin--Ihara
covering factorizations, exact finite Ramanujan certificates, an exact
eighth-trace identity, and finite spectral diagnostics.

It is not the frozen Pass5683/5693 tower.  Its base edge list is globally sorted
and its four-matching/six-pair selection starts on the 80-vertex parent, whereas
the earlier tower preserves a line-major base order and applies Pass5683's
frozen signing before sorting derived levels.  No isomorphism or signing-gauge
comparison between the two towers has been computed.

## Pass5699: standard covering factorization on three explicit lifts

For a signed parent adjacency matrix \(A_s\), the two-lift adjacency is exactly
conjugate to the block sum of the unsigned and signed parent matrices.  Hence

\[
 \operatorname{spec}(A_{\rm child})=
 \operatorname{spec}(A_{\rm parent})\sqcup
 \operatorname{spec}(A_s).
\]

Combining this exact block identity with the Bass determinant gives the
standard Stark--Terras \(\mathbb Z/2\)-cover factorization

\[
 \zeta_{\rm child}(u)^{-1}
 =\zeta_{\rm parent}(u)^{-1}L(u,\chi)^{-1},\qquad
 L(u,\chi)^{-1}
 =(1-u^2)^{r-1}\det(I-uA_s+3u^2I).
\]

This use of covering-graph Artin \(L\)-functions is established theory, already
cited in `analysis/PASS4475_4478_PRIMARY_LITERATURE.md`.  The finite W33-specific
calculation here is the application to the three constructed lifts.

Using the BT545 Levi spectrum, the base determinant reduces to

\[
 \Delta_{\rm Levi}(u)
 =(1-u^2)(1-9u^2)(1+9u^4)^{24}(1+3u^2)^{30}.
\]

At all three signed parent sizes \(80,160,320\), every signed determinant root
lies on \(|u|=1/\sqrt3\).  The unsigned levels have the four familiar trivial
roots \(\pm1,\pm1/3\); all remaining roots lie on that circle.  The determinant
functional equation is also factorwise exact because

\[
 (3u^2)\left(1-\frac{\lambda}{3u}+\frac{1}{3u^2}\right)
 =1-\lambda u+3u^2.
\]

The edge-sign local system is **not** Pass5696's determinant character on
\(\operatorname{AGL}(2,3)\).  No map between those objects is constructed, so no
orientation-sector or partition-function interpretation is retained.

## Pass5701: exact finite Ramanujan certificates

For each selected signed parent, the integer matrix

\[
 B=12I-A_s^2
\]

has an exact rational LDL decomposition with every pivot strictly positive.
The certified parent sizes and minimum pivots are:

| parent vertices | exact pivots | minimum pivot (decimal display) |
|---:|---:|---:|
| 80 | 80 | 4.8179893548 |
| 160 | 160 | 4.4896522954 |
| 320 | 320 | 4.5237671147 |

Thus \(\rho(A_s)<2\sqrt3\) for the three selected signings and the corresponding
children through 640 vertices are Ramanujan.  This is an exact theorem for those
three matrices, not an all-level recursion theorem.  No signing on a 640-vertex
parent, and hence no 1,280-vertex child, is produced by this packet.

## Pass5700: trace excess and the actual two cycle orbits

The base Levi graph satisfies the exact identity

\[
 \operatorname{Tr}(A_{\rm Levi}^8)
 =193280
 =80\cdot2092+25920
 =80M_8^{\rm tree}+|\operatorname{PSp}(4,3)|.
\]

Dividing the excess by \(16=8\) starting positions times two directions gives
\(1,620\) unrooted girth-eight cycles.  BT545 and Pass75 already own that cycle
count; the displayed trace decomposition is the bounded result here.

For the four computed tower levels, the exact excesses are

```text
25920, 25600, 25216, 24928
```

and the girth is \(8\) at each level.  The strict decrease is an observation on
these four graphs only.

The \(25,920\) ordered encodings of the base cycles split into two
\(\operatorname{PSp}(4,3)\)-orbits:

```text
point-rooted encodings: 12960, stabilizer order 2
line-rooted encodings:  12960, stabilizer order 2
```

This is the bipartite root grade, not chirality.  The nonidentity stabilizer of
a representative point-rooted encoding is an involution with point-action cycle
shape \(1^8 2^{16}\).  Since W(3,3) is not self-dual, nothing here supplies a
point--line merger, a grading-reversing Levi automorphism, or a regular action on
the 1,620 unrooted cycles.

## Pass5702: exact moments and sampled CDF discrepancies

For signed parent sizes \(80,160,320\), exact integer traces reproduce the
4-regular-tree moments through degree six:

\[
 M_2=4,\qquad M_4=28,\qquad M_6=232.
\]

The per-vertex degree-eight discrepancies from the tree value \(2092\) are
\(-4,-12/5,-9/10\).  Higher exact trace rows through degree twelve are stored in
the certificate.

The separate numerical diagnostic compares each empirical signed spectrum to
the Kesten--McKay CDF on a fixed 241-point grid.  Each reference CDF value uses
double-precision trapezoidal quadrature with 4,000 panels.  The resulting
sampled discrepancies are

```text
0.02102, 0.01079, 0.00540.
```

They decrease across the three computed sizes.  They are not exact
Kolmogorov--Smirnov statistics, carry no rigorous quadrature error bound, and do
not establish a rate or an all-level limit.  No controlled random ensemble or
hypothesis test was supplied, so the former GOE and chaos interpretation is
withdrawn.

## Pass5703: W(3,9) reconstruction, not a new independence bound

The deterministic producer independently reconstructs the point graph

\[
 \operatorname{SRG}(820,90,8,10)
\]

over \(\mathbb F_9=\mathbb F_3[a]/(a^2+1)\) and exhaustively verifies its degree
and common-neighbour parameters.  It then checks the actual prior owner,
`data/PART_W33_PASS5226_5227_ODD_Q_OVOID_DEFICIENCY.json`, which records

\[
 50\leq\alpha(W(3,9))\leq82,
\]

with randomized-greedy baseline \(46\), an explicit witness of size \(50\), and
the Hoffman upper bound \(82\).  The former Pass5703 interval \(51\) to \(80\)
was unsupported and is withdrawn.  Pass5703 adds no independence-number result.

The former q=5 candidate-group script is now an executable tombstone.  The live
owner is the stronger 56-check GAP packet Pass5667--5674.

## Reproducibility and publication status

- `analysis/w33_pass5699_5703_runner.py` replays all five certificate owners.
- `tests/test_w33_pass5699_5703_tower_zeta_corrections.py` checks the corrected
  semantics and replays the packet in an isolated tree, requiring byte-identical
  JSON.
- `analysis/PASS5699_5703_external_prior_art_and_corrections.md` records the
  ownership and retraction ledger.
- `data/w33_pass_namespace_registry_v2.d/5699-5703.json` registers this packet as
  corrected, replayable, and publication-source-unintegrated.

The TeX and HTML fragments remain source-only until the neighboring
Pass5704--5711 lane is reconciled.  In particular, the Pass5706 producer imports
Pass5683 and Pass5693 and starts from Pass5683's frozen base signing; it extends
that earlier tower to 2,560 vertices and does not continue Pass5699.  The
neighboring namespace's phrase "past Pass5699--5703" is chronological, not an
identification of the towers.  All surviving statements are finite graph, exact
matrix, finite group-action, or explicitly labelled numerical observations.  No
continuum limit, physical spectrum, physical chirality, partition function,
quantum chaos, or Yang--Mills mass gap is claimed.
