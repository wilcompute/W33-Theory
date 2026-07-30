# RESULTS VOCABULARY — find the same result under different words

This is the human-curated semantic companion to the machine-generated
[`RESULTS_INDEX.md`](RESULTS_INDEX.md). The index catches a repeated formula,
integer, code parameter, or sequence; this file catches a repeated result that
has been renamed. An alias below means “search the same result neighborhood,”
not that every use of the words is logically interchangeable.

Use the exact-result index first. If it misses, search the aliases here, then
read the listed primary artifacts end to end before claiming novelty. Always
carry the stated group, carrier, and scope into the new claim.

## The 540 — and the trap that there are FIVE transitive species

**Aliases:** `540 frames`, `540 skew pairs`, `540 cubes`, `540 nonedges`,
`540-class`, `3A1 involutions`, `Q3 charts`, disjoint line pairs,
noncollinear point pairs, `GQ(4,2)` arcs, outer quartics, and cubic
nonincidence flags.

**Complete classification (Pass 1139):** for
\(G=\operatorname{PSp}(4,3)\cong U_4(2)\), a transitive degree-540 set is
\(G/H\) with \(|H|=48\). The table of marks has exactly five conjugacy
classes of order-48 subgroups:

| TOM | canonical tag | stabiliser | rank | carrier |
|---:|---|---|---:|---|
| 77 | `{540:point-nonedge}` | `((C4 × C2):C2):C3` | 25 | noncollinear W(3,3) point pairs / `4A` |
| 78 | `{540:double-six-nonincident}` | `C2 × S4` | 28 | nonincident double-six/cubic-line flags |
| 79 | `{540:gq42-arc}` | `C2² × A4` | 27 | ordered Hashimoto arcs of `GQ(4,2)` |
| 80 | `{540:outer-4c}` | `A4:C4` | 21 | restricted W(E6) class `4C` |
| 81 | `{540:line-nonedge}` | `C2 × S4` | 32 | disjoint line pairs / skew frames / `2D` |

**THE FACTORIZATION IDENTIFIES NOTHING.** `25920 = 540 × 48` is true of all
five actions. Even the abstract stabiliser does not suffice: TOM 78 and 81
both have stabiliser `C2 × S4`, but the subgroups are nonconjugate, their
normalizers have orders 96 and 48, and their action ranks are 28 and 32.
The full-Weyl identity `51840 = 540 × 96` likewise applies to its three
size-540 element classes `4A`, `2D`, and `4C`. **Cite the object, never the
factorization.** The legacy alias `bt1205` calls one 540 `root_triples` and
must be resolved from its actual construction.

**THE NONEDGE HAZARD REMAINS.** W(3,3) is not self-dual, so "nonedge" of
the point graph (TOM 77) and "nonedge" of the line graph (TOM 81) are
nonisomorphic \(G\)-sets. Always say *point*-nonedge or *line*-nonedge.
That two-way warning was correct but was not a complete census.

**The cubic bridge:** the unique \(S_6\) double-six stabilizer has line
orbits \(12+15\), so
\[
36\cdot27=36\cdot12+36\cdot15=432+540.
\]
The incident flags have \(A_5\) stabilizer and give Pass 1137's projective
432-carrier; the complementary flags are TOM 78, the rank-28 species.

**Status and boundary:** the line-nonedge action owns the rank-32
imprimitivity and three block systems; Pass 161 already analyzed the
point-nonedge and `GQ(4,2)` arc actions at ranks 25 and 27. Pass 1139 adds
the exhaustive census, TOM 78 and 80, and the complete joint-rank matrix.
No map between two species follows from a shared count, rank entry, or
abstract subgroup type.

**Primary artifacts:** [Pass 1139](PASS1139_COMPLETE_DEGREE540_SPECIES_CENSUS.md)
(complete TOM census and cubic complement),
[Pass 161](analysis/w33_pass161_gq42_ihara_inheritance.py) (the first three
natural carriers), [BT773](analysis/BT773_involution_cube_theorem.md)
(cubes, one per 3A₁ involution),
[Pass 1067](data/w33_pass1067_outer_class_geometry.json) (`2D`/frame class),
and [Pass 1079](analysis/w33_pass1079_frame_action_rank32.g) (frame block
systems).

## The three 432s — directed Schläfli edges in A2 colors

**Aliases:** `three 432 orbits`, `A2 color fibres`, `mixed A2 triples`,
`S5 carrier`, directed Schläfli edges, Schläfli arcs, `TOM 295`,
`81_minus bridge`, and the formerly dark cubic-kernel blocks.

**Canonical objects:** after fixing \(A_2<E_8\), the six \(27\)-root shells
pair by negation into three colors. In each color, the map from a mixed
\(A_2\) triple to its ordered opposite-shell pair is an equivariant bijection
onto the \(27\cdot16=432\) directed edges of
\(\operatorname{SRG}(27,16,10,8)\). The directed-edge stabilizer is \(S_5\);
this is the rank-26 TOM-295 action, not an arbitrary index-432 \(S_5\) action.

**The Steinberg transform:** the natural reversal-odd class-projector map
\[
T(i\to j)=\operatorname{primitive}
\bigl((K-24)(K-18)(K-12)(K-9)(e_i\wedge e_j)\bigr)
\]
has rank \(81\) and projects the oriented-edge module onto \(81_-\). Its
432 columns form 216 antipodal lines with \(G^2=3200G\) and absolute angles
\(0,1/15,1/5\). The three color copies have total rank \(243\) and carry
\(81_-\boxtimes\mathbb Q[C_3]\).

**Integral identity:** in the integral \(325\)-coordinate contraction-zero
chart, the nonzero Smith factors of \(T\) are
\[
1^{15},2^6,4^8,8^{29},40^{23}.
\]
Thus the image-saturation quotient has order \(2^{178}5^{23}\), with rank
drops \(81\to15\) modulo \(2\) and \(81\to58\) modulo \(5\), but no drop
modulo \(3\). Separating the three colors into trivial and augmentation
sectors has color Smith form \((1,1,3)\), hence index \(3^{81}\) on the
rank-\(81\) packet. Do not merge these two facts: \(2,5\) are internal
edge-lattice primes; \(3\) is the integral color-Fourier prime.

**Projector normalization:** the natural edge image has
\(\operatorname{content}Q(e_i\wedge e_j)=280\), while the selected
projector scale is \(11200\). Thus \(T=Q/280=40P_4\) on this carrier.
Every Smith invariant divides \(40\). Prime \(7\) divides both \(11200\)
and \(280\), so it cancels before the primitive lattice and causes no
rank drop.

**Five-primary critical-group bridge:** the reduced W33 Laplacian has Smith
profile \(1^{16},10^8,40,160^{14}\), so its \(5\)-primary critical group is
\((\mathbb Z/5)^{23}\). This is not merely equinumerous with the
\(5\)-primary edge-lattice saturation quotient. As literal
\(\mathbb F_5W(E_6)\)-modules,
\[
(\overline L_T/L_T)_{(5)}\otimes\mathrm{sgn}
 \cong K(W_{3,3})_{(5)}
\]
uniquely up to \(\mathbb F_5^\times\). The untwisted Hom dimension is zero;
the sign-twisted and \(PSp(4,3)\)-restricted Hom dimensions are each one.
Moreover, the saturated \(81\)-module is the nonsplit exact sequence
\[
0\to58\to81\to K(W_{3,3})_{(5)}\otimes\mathrm{sgn}\to0.
\]
Its complete submodule dimension profile is \(0,58,81\), even after
restriction to \(PSp(4,3)\); `58+23` is therefore a composition-factor
ledger, not a direct-sum decomposition.
Aliases include `five-primary sandpile bridge`, `rank-23 sign-twist`, and
`Pass 1147 critical-group module`, `nonsplit 58-23 extension`, and
`saturated frame mod 5`. A displayed matrix is basis-dependent; no canonical
integral lift is part of the vocabulary entry. The bare \(5^{23}\) and
\((\mathbb Z/5)^{23}\) counts predate Pass 1147; use the module/Hom/extension
data when citing this result as new.

**Status and boundary:** adjoining these blocks to the disjoint rank-45 cubic
map gives a rank-288 map on the 2240 \(A_2\) triples and an exact
1952-dimensional residual. The color torsor is intrinsic but a labeled
`Omega_432 x C3` chart chooses an origin and generator. The Fourier split is
finite representation theory, not a physical generation or Yukawa theorem.
Do not identify the 135-dimensional oriented-edge kernel with another
135-carrier merely from the shared count.

**Primary artifacts:** [Pass 1147](PASS1147_SCHLAEFLI_STEINBERG_FOURIER_BRIDGE.md),
[Pass 1138](PASS1138_EXPLICIT_CUBIC_INCIDENCE_BRIDGE.md), and
[Passes 1142–1146](PASS1142_1146_EXACT_RELEASE.md).

## The 36 — spreads

**Aliases:** `36 spreads`, `36 regular spreads`, `36 double-sixes`,
`M36 vacuum`, `36-class`, index-36 maximal, 15-block system.

**Canonical object:** the spreads of W(3,3) — sets of 10 pairwise disjoint
totally isotropic lines covering all 40 points. Stabiliser **S₆**, index 36.
Classically the 36 double-sixes of the 27 lines on a cubic surface.

**Status and boundary:** the frame action's 15-block system is isomorphic to this
**as a G-set** (Pass 1097, by stabiliser conjugacy) but the blocks are **not**
the spreads' fibres — a spread holds 45 frames, a block holds 15, and the two
36-dimensional modules meet only in the constants (Pass 1081). Do not conflate
the abstract G-set with the concrete embedding.

**Primary artifacts:** [BT810](analysis/BT810_completed_geography_schlafli.md),
[BT813](analysis/BT813_vacuum_transition_matrix.md),
[Pass 1079](analysis/w33_pass1079_frame_action_rank32.g),
[Pass 1081](data/w33_pass1081_frame_module_lattice.json).

## The 45 — polar pairs

**Aliases:** `45 polar pairs`, `45 hyperbolic polar pairs`,
`45 tritangent planes`, `M45 vacuum`, index-45 maximal, 12-block system.

**Canonical object:** PG(3,3) has 130 lines, 40 totally isotropic and 90
hyperbolic; the symplectic polarity L ↦ L^⊥ is fixed-point-free on the
hyperbolic lines, giving exactly 45 pairs {L, L^⊥}. Stabiliser
`(SL(2,3) × SL(2,3)):C₂` of order 1152 in PGSp(4,3) (576 in PSp), because the
pair splits 𝔽₃⁴ into two orthogonal symplectic planes each carrying
Sp(2,3) = SL(2,3) = 2T, swapped by the polarity.

**Status and boundary:** its point orbits on the 40 are **[8, 32]** — the pair's
own 8 points in one orbit, the rest in another (Pass 1117, closing BT810's open
question; BT810 had guessed "9+9" and "4 + 4 + 16", both wrong).

**Primary artifacts:** [BT810](analysis/BT810_completed_geography_schlafli.md)
(owns the identification), [BT813](analysis/BT813_vacuum_transition_matrix.md),
[Pass 1097](analysis/w33_pass1097_name_the_frame_quotients.g) (the block-system
bijection only).

## The 135 — maximal partial spreads

**Aliases:** `135 maximal partial spreads`, `unextendable partial spreads of
size 8`, 4-block system, and — dually — `maximal partial ovoids of size q²−1 of
Q(4,q)`; structurally `sharply transitive subsets of SL(2,3)`.

**Canonical object:** the 8 pairwise disjoint totally isotropic lines covering
32 of the 40 points whose 8 missed points contain no line, so the partial spread
extends by nothing. Census: 1755 size-8 partial spreads = 1620 extendable
(= 36 spreads × C(10,2)) + **135** maximal. Equal to 45 polar pairs × 3 cosets
of Q₈ in SL(2,3), with SL(2,3)/Q₈ = C₃ the orientation on each triple.

**Status and boundary:** **PUBLISHED, not new** — this is a studied family
(Penttila; Cimráková–Fack 2005). Any q-general count is refuted: the family is
reported empty for q = pʰ with p odd and h > 1, so the fit q³(q²+1)/2 (correct
at q = 2 and 3) does **not** generalise.

**Primary artifacts:** [Pass 1100](analysis/w33_pass1100_name_the_135.g),
[Pass 1107](analysis/w33_pass1107_partial_spread_census.md),
[Pass 1109/1110](analysis/w33_pass1109_1110_sl23_and_steinberg.md).

## Inverse-closed Heisenberg section

**Aliases:** `section`, `section function`, `central-offset function`, `odd
map`, `inverse-closed section`, `signed antipodal coloring`, one value per
antipodal pair.

**Canonical object:** a map
\(c:(R^2\setminus\{0\})\to R\) satisfying \(c(-v)=-c(v)\), stored by one
coordinate for each pair \(\{v,-v\}\). It selects
\(S(c)=\{(v,c(v)):v\ne0\}\) in the Heisenberg group.

**Status and boundary:** the all-section spectral arc ranges over every such
odd map. A “good section” or “distance-regular section” is a much smaller
subfamily: at \(q=3\), the 81 sections split into the 9 distance-regular linear
sections and 72 others under the full affine automorphism action. Later
symplectic-orbit counts use a smaller determinant-one action, so their seven
orbits do not contradict the earlier two affine orbits.

**Primary artifacts:** [Pass 394](analysis/w33_pass394_cover_law_proof_and_section_classification.py),
[Pass 395](analysis/w33_pass395_cayley_section_classification.py), and the
fixed block convention in [Pass 473](analysis/w33_pass473_universal_trace_laws_and_q3_det_law.py).

## Symplectic section action

**Aliases:** `Sp(2,p) action`, `SL(2,p) action`, determinant-one action,
symplectic reparameterization, symplectic section orbit.

**Canonical object:** in dimension two,
\(\operatorname{Sp}(2,p)=\operatorname{SL}(2,p)\), acting by
\((g\cdot c)(v)=c(g^{-1}v)\). This is not the determinant-twisted
\(\operatorname{GL}(2,p)\) action and not the full affine
\(\operatorname{GL}(2,p)\)-by-linear-offset action on Heisenberg sections.

**Status and boundary:** `charpoly(D_c)` is constant on symplectic orbits.
At \(p=3\), the 81 sections have seven such orbits; Burnside gives exact orbit
counts at \(p=3,5,7\), and Pass 540 extends the signed-cycle calculation to
\(\mathbb Z/9\mathbb Z\). At \(p=3\), the induced permutation image on the
four antipodal pairs is \(A_4\); the acting group itself has order 24.

**Primary artifacts:** [Pass 536](analysis/w33_pass536_symplectic_invariance.py),
[Pass 537](analysis/w33_pass537_burnside.py), and
[Pass 540](analysis/w33_pass540_symplectic_separator_chainring.g).

## Cyclic tuple orbit

**Aliases:** cyclic orbit, rotation orbit, necklace, period-\(d\) class,
orbit-size class \(S_d\), cycle type, closed-walk class.

**Canonical object:** the cyclic-rotation orbit of a zero-sum \(m\)-tuple in
the expansion of \(\operatorname{tr}(D^m)\). The symbol \(S_d\) denotes the
sum over orbits of minimal period \(d\). The trace is reconstructed by summing
\(dS_d\) over \(d\mid m\), with an overall factor \(q\) when the central trace
has been normalized out of the definition of \(S_d\).

**Status and supersession:** the decomposition is exact, but Pass 510 showed
that decomposition alone is not a mechanism for high valuation. Pass 514
proves the sieve; Pass 517 replaces tuple enumeration by the Möbius/power-sum
closed form; Pass 519 identifies the underlying object as a weighted
closed-walk transfer matrix. Pass 524 supersedes Pass 517's original
`free(m)=1` characterization: it also occurs when \(m\) is a prime different
from the residue characteristic. “Necklace count” is combinatorial language,
not a separate physical object.

**Primary artifacts:** [Pass 509](analysis/w33_pass509_cyclic_orbits_and_deviations.py),
[Pass 510](analysis/w33_pass510_orbit_size_decomposition.py),
[Pass 514](analysis/w33_pass514_sieve_theorem.py),
[Pass 517](analysis/w33_pass517_mobius_closed_form.py),
[Pass 519](analysis/w33_pass519_transfer_matrix.py), and
[Pass 524](analysis/w33_pass524_status_upgrade.py).

## Spectral merge

**Aliases:** orbit merge, characteristic-polynomial collision, spectral
collision, cospectral pair, block-spectral non-injectivity, sheet-data
non-injectivity.

**Canonical usage:** always state both the equivalence relation and the
spectral carrier. The corpus contains distinct claims about

- different symplectic section orbits with the same `charpoly(D_c)`;
- different full affine section orbits with the same central-block data; and
- nonisomorphic Cayley graphs with the same full graph spectrum.

**Status and supersession:** Pass 456 classifies the four original \(q=5\)
graph-spectrum collisions as three affine repeats plus one genuine
nonisomorphic pair; Pass 473 strengthens the genuine pair to complete
per-central-character block-spectral non-injectivity. At \(q=3\), Passes
536–539 locate one `charpoly(D_c)` merge, and Pass 540 explains it as the two
\(D_4\) chiral demicubes. Passes 480–482 already establish many sampled
genuine \(q=5\) pairs and the sheet-exchange/sheet-coincidence mechanism split.
Pass 540 adds a further exact full-support certificate, outside the eight
explicit affine pairs retained by Passes 456/479/482 and realizing the known
sheet-coincidence mechanism, inside a deterministic sample of 3,000
full-support symplectic orbits. The exhibited pair is exact; the sample is not
an exhaustive collision census, and Pass 482 did not retain every sampled
representative. Consequently neither a novelty ordinal nor Pass 538's global
rarity/image-cardinality interpretation is justified.

**Primary artifacts:** [Pass 456](analysis/w33_pass456_q5_collision_anatomy.py),
[Pass 473](analysis/w33_pass473_universal_trace_laws_and_q3_det_law.py),
[Pass 481](analysis/w33_pass481_t1_theorem_second_mechanism_q9_law_freeness.py),
[Pass 482](analysis/w33_pass482_order_theorem_q9_criterion_mechanism_census.py),
[Pass 538](analysis/w33_pass538_merge_rarity.py),
[Pass 539](analysis/w33_pass539_orbit_anatomy.py), and
[Pass 540](analysis/w33_pass540_symplectic_separator_chainring.g).

## Lambda-adic valuation

**Aliases:** \(\lambda\)-valuation, cyclotomic valuation, cyclotomic depth,
ramification depth, cyclotomic divisibility, `v_lambda`, `vlam`.

**Canonical object:** \(v_\lambda\) for \(\lambda=1-\zeta_p\), normalized by
\(v_\lambda(\lambda)=1\). It measures divisibility in the cyclotomic integer
ring, not an ordinary absolute value. At \(p=3\), for a nonzero rational
integer \(n\), \(v_\lambda(n)=2v_3(n)\); that translation is not valid with
the same factor at arbitrary \(p\) or for nonrational coefficients.

**Status and boundary:** Pass 487 delimits the character-order/chain-ring
scope of the sharp determinant congruence. Pass 535 translates the \(q=3\)
coefficient bounds into the familiar divisibilities \(9\mid e_2\) and
\(27\mid e_3\). Pass 541 uses rationality at \(q=3\) to convert the complete
power-sum recurrence into an all-exponent \(\lambda\)-valuation theorem. Do
not silently replace a \(\lambda\)-adic statement by a \(p\)-adic one without
first establishing rationality and the ramification factor.

**Primary artifacts:** [Pass 483](analysis/w33_pass483_modlambda_qplus1_theorem.py),
[Pass 487](analysis/w33_pass487_scope_of_the_law_and_det_hunt.py),
[Pass 535](analysis/w33_pass535_image_closed.py), and
[Pass 541](analysis/w33_pass541_q3_all_m_recurrence.g).

## q=3 all-exponent trace-valuation law

**Aliases:** all-\(m\) minimum, all-exponent \(q=3\) law, six-cubic recurrence
theorem, mod-9 recurrence cover, finite-clock proof, exact factorial-agreement
locus.

**Canonical object:** over all 81 \(q=3\) sections, for every integer
\(m\ge2\),

\[
 \min_c v_\lambda\!\left(\operatorname{tr}D_c^m\right)
 =2\bigl(m+[m\text{ odd}]\bigr).
\]

The exponent \(m=1\) is excluded because every section has trace zero. The
six realized characteristic polynomials are
\(x^3-9ax-27b\), with
\((a,b)\in\{(0,0),(1,0),(2,0),(3,0),(3,1),(4,3)\}\). After \(x=3y\), their
power sums satisfy
\(S_m=aS_{m-2}+bS_{m-3}\). The row \((1,0)\) attains every even exponent.
Modulo 9, the \((3,1)\) recurrence has period word `3,0,6`, while the
\((4,3)\) tail has period word `8,0,5,6,2,3`; together they attain all odd
residue classes modulo 6. Repetition of these finite recurrence states is the
infinite proof step; the sweep through \(m=60\) is only regression control.

**Status and boundary:** Pass 541 closes the finite-window noncancellation
question left open by Passes 521--523 and 528, within the repo's complete
\(q=3\) six-cubic image. The earlier factorial expression remains false. It
agrees with the true minimum exactly when
\(s_3(m)+[m\text{ odd}]=2\), equivalently, for \(m\ge2\), exactly when
\(m=3^j\) with \(j\ge1\), or \(m=3^i+3^j\) with \(0\le i\le j\). The
prime-power tower is therefore contained in, but does not exhaust, the
agreement locus. No \(q\ge5\), chain-ring, or uniform composite-\(m\) cyclic
relation-space theorem follows from this recurrence calculation.

**Primary artifacts:** [Pass 541](analysis/w33_pass541_q3_all_m_recurrence.g),
its [certificate](data/w33_pass541_q3_all_m_recurrence.json), and the
[proof synthesis](PASS541_Q3_ALL_M_RECURRENCE_THEOREM.md).

## Maximal real cyclotomic subring

**Aliases:** real subring, Hermitian reality, conjugation-fixed coefficients,
\(\mathbb Z[\zeta_p]^+\), `Q(zeta_p)^+`.

**Canonical object:** the fixed ring of complex conjugation inside
\(\mathbb Z[\zeta_p]\). Inverse closure makes \(D_c\) Hermitian, so every
coefficient of `charpoly(D_c)` lies in this real subring.

**Status and supersession:** Pass 491 proved the determinant-only statement;
Pass 533 proves the Hermitian entry identity and upgrades it to every
characteristic-polynomial coefficient, completing the link that Pass 532 had
only checked computationally. The subring equals \(\mathbb Q\) only at
\(p=3\); “real” must not be rewritten as “rational” for \(p>3\). Its prime
has ramification index two upstairs, explaining even \(\lambda\)-valuations.

**Primary artifacts:** [Pass 491](analysis/w33_pass491_real_subring_and_third_failure.py),
[Pass 532](analysis/w33_pass532_hermitian_reality.py), and
[Pass 533](analysis/w33_pass533_hermitian_derived.py).

## Section support

**Aliases:** support of \(c\), nonzero-offset support, vector support, pair
support, full-support section.

**Canonical object:** vector support is
\(|\{v\ne0:c(v)\ne0\}|\); pair support counts stored antipodal pairs with a
nonzero value. For an odd section in odd characteristic, vector support is
twice pair support. Thus the \(q=3\) notation `8/8 support` is the same as
`4/4 antipodal-pair support`.

**Status and boundary:** Pass 539 proves that the unique merged pair at
\(q=3\) is exactly the two full-support orbits, but support does not separate
them and does not classify all seven orbits. Pass 540 supplies the finer
coordinate-product separator. Do not conflate section support with graph
vertex support, matrix sparsity, or codeword support elsewhere in the repo.

**Primary artifacts:** [Pass 539](analysis/w33_pass539_orbit_anatomy.py) and
[Pass 540](analysis/w33_pass540_symplectic_separator_chainring.g).

## Moore–Dickson bracket scalar and oriented coordinate product

**Aliases:** coordinate product, product parity, oriented bracket product,
Moore–Dickson scalar, lex-ordered six-bracket scalar, full-support product character.

**Canonical object:** fix an oriented representative set \(R\) for the four
antipodal pairs at \(q=3\). The bare coordinate product
\(P_R(c)=\prod_r c_r\) depends on that frame. If
\(F_R=\kappa_R(X^3Y-XY^3)\), then
\(\chi(c)=\kappa_RP_R(c)\) is representative- and ordering-independent.  In
the certificate's lexicographic (even-oriented) ordering it equals the product
of the six symplectic brackets among the lifted points \(c_rr\).  An odd
reordering flips that alternating bracket but not \(\chi\); equivalently the
bracket naturally lives in the projective orientation line.  The certificate
frame has \(\kappa_R=1\), so \(\chi=P_R\) there. Reorienting one representative
flips both factors, not \(\chi\).

**Status and boundary:** in a fixed frame, \(P_R\), and intrinsically \(\chi\), is invariant under
\(\operatorname{Sp}(2,3)\), takes values 1 and 2 on the two full-support
orbits, and transforms by the quadratic determinant character under the
determinant-twisted \(\operatorname{GL}(2,3)\) action. A determinant-nonsquare
element swaps the two intrinsic values. At \(q=5\), fixed-frame coordinate
product remains one exact symplectic invariant but is only one component of
the finer line-ratio feature; it is not a complete classifier.
“Moore–Dickson scalar” here means the intrinsic form coefficient, not the bare
oriented product, the unoriented six-bracket, or every invariant called a
Dickson invariant elsewhere.

**Primary artifact:** [Pass 540](analysis/w33_pass540_symplectic_separator_chainring.g).

## D4 chirality demicubes

**Aliases:** even/odd \(Q_4\) sign words, the two 8-vertex demicubes,
half-spin/conjugate-half-spin weights, spinor/conjugate-spinor sheets,
product-parity fibers.

**Canonical object:** the 16 full-support \(q=3\) sections become the 16 sign
words in \(Q_4\). The two fibers of the oriented product scalar are the two
8-word parity halves, identified with the \(D_4\) spinor and conjugate-spinor
weight sets.

**Status and boundary:** Pass 540 gives the exact carrier-level
identification and explains why `charpoly(D_c)` merges the two symplectic
orbits: determinant-one symmetry preserves chirality, while the larger
determinant-nonsquare action swaps it together with the two central characters;
at \(q=3\), Galois conjugacy collapses in
\(\mathbb Q(\zeta_3)^+=\mathbb Q\), and the equality is checked directly.
Hermitianity alone would not force the merge. BT1416 independently certifies the
8-vertex demicube graph \(K_{2,2,2,2}\), and BT1815 records the
\(D_4^*/D_4=\{0,v,s,c\}\) spinor/conjugate-spinor dictionary. Those are prior
carriers of the same standard geometry, not automatic identifications with
every “chirality” bit elsewhere in the corpus.

**Primary artifacts:** [Pass 540](analysis/w33_pass540_symplectic_separator_chainring.g),
[BT1416](analysis/BT1416_even_q4_demicube_guard_ledger.md), and
[BT1815](analysis/bt1815_d4_gkp_quartet_operator_assignment.py).

## Signed-cycle Burnside census over a chain ring

**Aliases:** signed-cycle Burnside, positive/negative signed cycle,
chain-ring section action, Hjelmslev shell, \(\mathbb Z/9\) orbit census,
primitive/deep pair filtration.

**Canonical object:** \(SL(2,\mathbb Z/9)\) acts by signed permutations on the
40 antipodal nonzero-vector pairs. Because 2 is a unit, a negative signed
cycle fixes only coordinate 0, while each positive cycle contributes nine
choices (eight under full support). Burnside averaging therefore reduces the
enormous section space to the exact signed-cycle profile.

**Status and boundary:** Pass 540 proves
`228100045392509153077600971330057241` total orbits and
`2051277771273019233341050472890368` full-support orbits, with an exact
primitive/deep Hjelmslev-shell refinement. These are orbit counts only; no
chain-ring characteristic-polynomial classification or semisimple
representation-theory transfer is claimed.

**Primary artifact:** [Pass 540](analysis/w33_pass540_symplectic_separator_chainring.g).
