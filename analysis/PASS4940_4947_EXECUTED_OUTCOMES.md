# Passes 4940–4947 — Executed Outcomes

Status: **EXECUTED / FROZEN**, with the explicit exception that Pass4944 gate-level Yosys cell/timing evidence remains pending a real runner. The functional RTL theorem is frozen independently.

## Pass4940 — exact hard-word distance

The Pass4859 received word was solved exactly against the 35-dimensional cut class by a deterministic 36-vertex bitset branch-and-bound. The search fixed one vertex to quotient the cut/complement symmetry, used exact fixed/free mismatch bounds plus edge-disjoint odd-signed-triangle lower bounds, and exhausted 8,242,747 nodes.

- exact distance to the cut class: **134**
- Pass4859 twist certificate: `g(x)=x+sigma`
- exact distance to the switched class: **134**
- therefore `d(x,K)=134`
- updated global interval: **134 <= rho(K) <= 179**

This does not close the global covering radius.

## Pass4941 — ambiguity-cancelling quartic

Let `q1,q2` span the two-dimensional PSp-equivariant quadratic Steiner-to-adjoint Hom plane. Pass4875 proves the outer PGSp/PSp involution acts by `-I_2`; Pass4871 supplies the unique intrinsic bracket on `Q10`.

Define `F(x)=[q1(x),q2(x)]`.

- homogeneous degree: 4
- GL2 basis change: `F` scales by the determinant
- outer parity: even
- projectively basis-independent: yes
- exact image span: **10**
- every two-support input: zero
- each quadratic channel annihilates the whole 40D fiber-constant subspace

Thus the quadratic ambiguity cancels at degree four without selecting an arbitrary quadratic channel; only an overall nonzero scalar remains.

## Pass4942 — defining-characteristic Steiner degeneration

The rational 4-class Steiner scheme has a 40D fiber-constant sector and an 80=20+60 transverse sector. Direct 120x120 relation-matrix calculation over F3 gives:

- `N=I+R1`: rank 40, `N^2=0`
- `im(N)` dimension 40 lies inside `ker(N)` dimension 80
- `R2` ranks: **34 -> 14 -> 0**
- `R2` Jordan type: **3^14 2^6 1^66**
- `R3` rank: 39
- `R3^2=0`

This is a non-semisimple modular filtration. It specifically does **not** justify the separate shorthand claim that the F3 Bose–Mesner algebra becomes “rank two” merely because rational eigenvalues coincide modulo 3. Pass4948 was independently reserved to audit/correct that parallel claim and its dependents.

## Pass4943 — explicit common-S6 crosswalk

The marked-double-six shell and the Pass1848 duad–syntheme carrier were placed on the same literal six labels.

- common group: `S6`, order 720
- adjacent-transposition generators agree coordinate-for-coordinate on all 15 duads
- marked-residue extension: `S6 x C2`, central triad-complement involution, center order 2
- duad–syntheme extension: `Aut(S6)=S6:2`, exceptional involution swaps duads with synthemes, center order 1

The common S6 carrier is therefore explicit, while the two order-1440 groups remain non-identifiable.

## Pass4944 — literal 45-way AGL(1,3) selector RTL

Committed:

- `rtl/w33_pass4944_port_selector45.sv`
- `rtl/tb_w33_pass4944_port_selector45.sv`

The local rule is `i -> (-1)^b i + r mod 3`.

Exact semantics:

- 6 selector states
- 3 valid ports each
- 18/18 state/input cases
- all six permutations of three ports realized
- every selector state bijective
- local output collisions: **0**
- parallel selector count: 45
- combinational selector stages: 1

Control state:

- local independent encoding: 45 two-bit trit fields + 45 reflection bits = **135 bits**
- Pass4872 global fixed-binary information optimum: **117 bits**
- exact locality premium: **18 bits**

A globally packed 117-bit arbitrary-table decoder is not implemented. Yosys cell counts and FPGA timing remain pending an actual runner.

## Pass4945 — full S3 matching holonomy

The canonical R2 perfect matching over each of the 540 W33 nonedges defines an S3 transport after local labels are chosen on each Steiner three-fiber.

- complement edges: 540
- independent fundamental cycles: 501
- generated holonomy group: **S3**, order 6
- all six permutations occur

Hence the connection cannot be globally trivialized and does not globally reduce to C2 or C3. The holonomy conjugacy class is gauge invariant although individual edge permutations depend on local labels.

## Pass4946 — two inequivalent 120-shells recover dual W33 incidence

Pass4877 proved the 120 maximum cuts and 120 Steiner triangles are not equivariantly bijective. Define `B(C,T)=1` exactly when maximum cut `C` splits Steiner triangle `T`.

- 120x120 cross-incidence matrix
- every row weight: 108
- every column weight: 108
- row classes: 40 classes of 3 identical rows
- column classes: 40 classes of 3 identical columns
- the column classes are exactly the forty Steiner triads/fibers

On the 40x40 quotient, the complementary non-splitting matrix `Z=1-B` has row and column weight 4. Two quotient points are collinear iff they share a zero row; the resulting graph is exactly `SRG(40,12,2,4)` and is explicitly isomorphic to the Pass4870 W33 quotient.

Therefore the two inequivalent 120-shells are threefold refinements of the dual line and point actions of W(3,3), not a false 120-to-120 identification.

## Pass4947 — connection curvature detects triad centers

There are 3,240 triples of pairwise noncollinear W33 points.

- identity holonomy: **1080**
- transposition holonomy: **2160**
- order-three holonomy: **0**

Independently:

- zero common centers: **1080**
- two common centers: **2160**

The two classifications agree exactly. In classical generalized-quadrangle terminology, matching curvature is flat exactly on acentric triads and reflective exactly on centric triads.

The number 1080 occurs elsewhere in the repository; no identification with another 1080-shell is promoted without an explicit equivariant map.

## Integration and release

- frozen JSON certificates: 8
- focused regression: `tests/test_w33_pass4940_4947_exact_packet.py`
- shared manuscript insert: `analysis/PASS4940_4947_radius_quartic_holonomy_duality_insert.tex`
- all three root manuscripts consume the shared frontier manifest
- public page: `docs/pass4940-4947-radius-quartic-holonomy.html`
- root card source: `analysis/PASS4940_4947_radius_quartic_holonomy_index_insert.html`
- idempotent root materializer: `tools/integrate_pass4940_4947_public.py`
- exact evidence/release workflow: `.github/workflows/w33_pass4940_4947_exact_packet.yml`

Repository-wide GitHub Actions congestion is substantial. Public-root materialization and gate-level Pass4944 synthesis must therefore be reported by observed run state, not inferred from committed workflow source.
