# Pass5699--5703 prior-art and correction ledger

This note separates the surviving finite results from earlier repository owners,
standard covering-graph theory, and claims withdrawn during replay.  It is a
publication-source companion, not an integrated manuscript section.

## 1. Covering zeta factorization is established theory

Stark and Terras develop Artin (L)-functions for finite graph coverings and the
covering-zeta factorization used in Pass5699:

> H. M. Stark and A. A. Terras, "Zeta Functions of Finite Graphs and
> Coverings, Part II," *Advances in Mathematics* **154** (2000), 132--195,
> DOI `10.1006/aima.2000.1917`.

The repository already cites and scopes that theory in
`analysis/PASS4475_4478_PRIMARY_LITERATURE.md`.  Pass5699's corpus-level addition
is therefore narrow: it applies the standard (mathbb Z/2)-cover factorization
to three explicitly generated lifts of one deterministic factor-pair tower and
checks the finite determinants.  The general factorization is not new here.

## 2. The base Levi spectrum and 1,620 octagons have earlier owners

- `data/PART_BT545_W33_LEVI_MINIMAL_LOGICAL_CYCLE_results.json` already owns
  the (80)-vertex, (160)-edge, degree-four Levi graph, its spectrum
  ({pm4,pmsqrt6,0}) with multiplicities (1,24,30), cycle rank (81),
  and exactly (1,620) simple 8-cycles.
- `w33_pass75_zeta_equidistribution.json` already records the same (1,620)
  octagons as the undirected shortest incidence-graph primes, with oriented
  prime count (3,240).

Consequently Pass5700 does not newly discover the 1,620 count.  Its bounded new
calculation is the exact eighth-trace decomposition

```text
193280 = 80*2092 + 25920
```

and the explicit action on the (25,920) ordered cycle encodings.  Those
encodings split by whether the initial vertex is in the point grade or the line
grade.  Calling this split "chirality" was a carrier error.

## 3. This is not either pre-existing Ramanujan tower

Pass5683 and Pass5693 freeze a particular producer-order contract: the original
line-major base edge order and Pass5683's stored negative-edge set are used
before sorting derived lifts.  Pass5699 instead globally sorts the base edge
list and performs a fresh four-matching factorization and six-candidate choice
already on the (80)-vertex parent.  The resulting construction is therefore
named the **separate deterministic factor-pair tower** throughout this packet.

No graph isomorphism, signing gauge equivalence, or equivariant comparison with
Pass5683/5693 has been computed.  Equality of vertex counts and Ramanujan bounds
does not identify the towers.

## 4. The Pass5696 orientation weld is invalid

`data/PART_W33_PASS5696_AGL_ORIENTATION_TWISTED_SU3.json` defines the character
(chi(g)=det(g)) on the affine group (operatorname{AGL}(2,3)) and twists an
eight-dimensional augmentation representation.  Pass5699 assigns signs to
edges of a Levi graph to build a (mathbb Z/2) covering.  These are different
domains, and the packet constructs no map between them.

The former statements that the edge signing was "the same datum" and that its
Artin factors represented physical orientation sectors are withdrawn.  Only a
finite graph-cover local system and its determinant survive.

## 5. Root grade is not point--line duality

The corrected odd-(q) carrier record (`analysis/w33_pass4563_w33_is_not_self_dual.py`
and the Pass4761 retraction audit) distinguishes the W(3,3) point geometry from
its nonisomorphic dual line geometry.  The Levi graph is bipartite, and every
oriented 8-cycle alternates the two grades.  Changing the starting position by
one step changes a point-rooted encoding into a line-rooted encoding, but it is
not induced by the point-action group used in Pass5700.

Thus the two (12,960)-element orbits do not establish chirality, a W(E6)
duality merger, a grading-reversing automorphism, or a regular action on the
(1,620) unrooted cycles.  The reported order-two stabilizer is an ordinary
orbit--stabilizer fact inside each root grade.

## 6. The statistical statement is finite and sampled

Pass5702 uses three signed spectra of sizes (80,160,320).  Its low moments are
exact integer traces, but the CDF comparison uses a fixed (241)-point grid and
double-precision trapezoidal quadrature with (4,000) panels per grid point.
The three reported maxima are therefore **sampled CDF discrepancies**, not
exact Kolmogorov--Smirnov statistics.  There is no quadrature error bound, no
all-level convergence theorem, and no fitted rate.  The former GOE, chaos, and
eigenphase-spacing interpretation had no controlled ensemble or hypothesis test
and is withdrawn.

## 7. W(3,9) is a rediscovery, and q=5 belongs to Pass5667--5674

`data/PART_W33_PASS5226_5227_ODD_Q_OVOID_DEFICIENCY.json` already records for
W(3,9):

```text
randomized-greedy baseline = 46
certified independent-set witness = 50
Hoffman upper bound = 82
```

Accordingly the repository boundary is
(50leqalpha(W(3,9))leq82), with the exact value open.  Pass5703 now only
reconstructs `SRG(820,90,8,10)` independently and checks that owner certificate.
Its former (51)-to-(80) interval was unsupported and is withdrawn.

The old `analysis/PASS5703_Q5_TRANSITIVE_IDENTIFICATION.g` candidate template is
now an executable tombstone.  The live q=5 owner is the 56-check GAP packet
Pass5667--5674 (`analysis/w33_pass5667_5674_q5_reye_equivariant_orientation.g`),
which is materially stronger than an abstract candidate-group listing.

## Publication boundary

The neighboring Pass5706 source makes the provenance distinction executable:
`analysis/w33_pass5706_ramanujan_levels45_and_color_gauge.py` imports the
Pass5683 and Pass5693 producers, initializes from Pass5683's `levi()` and frozen
`NEG`, and continues that switching-gauge-fixed tower to 2,560 vertices.  It does
not import or continue Pass5699.  Thus the Pass5704--5711 namespace phrase
"past the new Pass5699--5703 arithmetic packet" is chronological, not a tower
identity.

The corrected report, TeX fragment, and HTML source remain unintegrated until
that distinction is propagated through the neighboring publication surfaces.
Nothing in this packet proves a continuum limit, a partition function, physical
chirality, quantum chaos, an all-level spectral law, or a new independence
number.
