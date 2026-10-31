# Five-front continuation: exact group action, Moore exclusion, and rate entropy

This packet executes the five investigations requested after `e3ef31b58`.
It resolves specific finite questions and constructs a rate model and a
continuum control. It does **not** classify every exterior arc, determine every
odd-q code distance, derive our universe's dynamics, or solve the TOE.

All computations use the existing checkout. Remote Desktop Commander again
reported TheHeavyCrown offline. Existing unrelated edits were preserved.

## 1. Exterior arcs: a larger finite classification and the last Moore case

Producer: `w33_20261031_exterior_search.py`.

The previous packet identifies nonsquare-good matchings with exterior arcs of
a conic. The new search uses exact modular arithmetic and integer bitsets:

- Pairs of conic parameters are candidate chords, or equivalently their poles.
- Joining-line discriminants impose the square or nonsquare condition.
- When a chord is selected, all incompatible chords are removed.
- Every line through two selected poles is forbidden to further poles.
- Choose an uncovered conic parameter with the fewest remaining partners.
  If any parameter has no partner, this branch cannot be a perfect matching.

**Why normalization is exhaustive.** PGL(2,q) is transitive on unordered pairs
of the conic. It preserves cross-ratios and chord concurrence. Thus any solution
can be transported to one containing `{0,infinity}`. Fixing this pair loses no
existence class; no further stabilizer or cyclic symmetry is imposed.

The new complete nonsquare exclusions are at primes
**67,71,79,83,103,107,127**. Controls reproduce 3,7,11 as positive and 19,31 as
negative. With the earlier complete prime searches through 61, the previous
packet's all-q=1 mod4 theorem, and the prime-power controls in
`search_drivers_12466/chord_search_gf.json`, this gives:

> Among odd prime powers q <= 127, this matching family exists exactly at
> q=3,7,11. The statement for all larger q=3 mod4 remains open here.

The older literature already discusses the q=7,11 exterior-arc examples and
their apparent rarity (Van de Voorde, Section 3). The finite extension above is
an executable repository result, not a claim to a new classical construction.

The original run completed all of these fields. Later contended reruns timed
out at 103,107,127. `data/w33_20261031_exterior_search_attempts.json` retains
both sets of attempts, the exact original source and its hash; its recursive
search, line-mask function and bit encoding are AST-identical to the current
producer. The accepted exclusions are the actual completed runs. Time limits
in later attempts are not reinterpreted as successful searches.

### The square family at q=113

The conic backend completes the q=113 square-good search with **15,319 visited
states**, maximum selected depth 6, and no matching. The independent
homogeneous-cross-ratio backend computes exactly the same entire compatibility
graph: its SHA-256 is

`5bba75a31abd9995109e18d45d0f2c5ad7faffb004a5eed5271369d7ef7606d9`.

That graph has 6,441 vertices, one per unordered conic pair. Its two exact
predicate implementations agree on all 41,486,481 ordered entries. The second
backend's traversal timed out; **only the completed conic traversal supplies
nonexistence**. A separate direct cross-ratio recursion also timed out. Neither
timeout is treated as an exclusion. Small-field triple concurrence is checked
against the independent Moebius implementation in the preceding packet.

Pass 12492 proves that equality in the twin-pair Moore bound is equivalent to
a square-good matching. The Moore degree theorem restricts the field orders to
q=3,5,13,113. The new search, with the q=3,5,13 controls, therefore yields:

> **Among coverage-{0,2}, twin-paired even line sets of W(3,q), q odd, the bound
> |S| >= 2+(q+1)^2/2 is attained only at q=5, by the Petersen construction.**

In particular W(113) has no twin-paired Moore-equality set of 6,500 lines.
This does not decide the abstract degree-57 Moore graph problem, exclude
non-twin-paired sets of that size, or determine the general minimum distance.

## 2. The full Petersen stabilizer: the cut module matters

Producer: `w33_20261031_petersen_stabilizer.py`.
Input: the frozen 20-line optimum in
`search_drivers_12466/even_line_sets_gf_q5.json` (Pass 12484).

### Exhaustion, not an order-based identification

Fix an ordered twin pair A,B. Any set stabilizer sends it to an ordered twin
pair: 20 possibilities. Choose symplectic frames adapted to each pair. Every
symplectic map between two such decompositions is

`F_image diag(M, M^(-transpose)) F_source^(-1)`, `M in GL(2,5)`.

There are 480 such M, hence 9,600 candidate symplectic maps. Testing the actual
20-line set and quotienting scalar +/-I gives all **960 projective stabilizers**.
Their image on the ten twin pairs has order **60**, with element orders
`1^1,2^15,3^20,5^24`: it is A5, not all Aut(Petersen)=S5.

The kernel is elementary abelian of order **16**. Its flip patterns on ten pairs
form the binary **K5 cut code [10,4,4]**, with weight enumerator

`1 + 5 z^4 + 10 z^6`.

Its five weight-four words recover five vertex stars. Each twin-pair coordinate
belongs to exactly two stars, hence labels an edge `{i,j}` of K5. Directly
checking the original line intersections shows that pair adjacency is exactly
disjointness of K5 edges: the Kneser graph KG(5,2), or Petersen graph.

An explicit A5 complement is certified. Its conjugation action is the deleted
permutation module, giving

`G = (even sign vectors in F2^5) semidirect A5 = W(D5)'`.

Six exact symplectic matrix generators, their 20-line permutations, and a
faithful signed SO(5) representation are frozen. The latter is checked against
the actual group multiplication, not inferred from its order. The group is
perfect. The preimage of the kernel in Sp(4,5) has order 32, central +/-I and
element-order counts `1^1,2^11,4^20`: the extraspecial minus-type lift.

The kernel also has an **explicit two-qubit operator dictionary**. The producer
finds actual matrices A,B,C,D with A^2=B^2=-I, C^2=D^2=I, two anticommuting
pairs and all cross-pair commutators trivial. A 64-equation linear system over
F5 then produces an invertible S intertwining them with

`iX tensor I, iZ tensor I, I tensor X, I tensor Z`, under `i -> 2 mod5`.

The actual four matrices, reduced Pauli matrices and S are frozen. This is a
kernel-level operator identification, not merely an extraspecial-group name.
It differs from the order-27 qutrit H27 and order-243 two-qutrit execution
groups in `2026-09-21_e8_matter81_h27_address_operator_compiler.md` and
`2026-09-21_physical_external_a2_h27.md`: their scalar centers and carrier
representations must not be identified. A physical coupling or a full complex
unitary lift of the entire stabilizer is still unbuilt.

**A tempting false connection was rejected.** The notation `2^4:A5` does not
specify the module. This group has 240 elements of order six and kernel orbits
5+10. The affine Mathieu M20=ASL(2,4) uses the other module and has no
order-six class. They are not the same group. The GAP table and original group
literature are useful external checks, not substitutes for the action above.

**Another count match was rejected.** Twenty D5 root rays do not give the
actual twenty-line action. Every A5 complement in this line action is transitive
on all twenty lines, while the unsigned coordinate A5 in the usual D5 ray
action has two orbits of ten. The search enumerates complements containing a
fixed order-three element; all 80 order-three elements are conjugate, which
makes this test exhaustive up to conjugacy. Thus the abstract signed-coordinate
representation is valid, but an equivariant line-to-root-ray bijection is not.

## 3. General even line sets: a rigorous bound beyond the twin assumption

Producer: `w33_20261031_even_set_bounds.py`.

The coverage-{0,2} sets are precisely hyperovals on the dual Q(4,q). This is
established terminology and literature: De Bruyn's classification work already
includes Q(4,3). In particular the q=3 minimum is not claimed as new here.

For an arbitrary nonempty even line set, split into two exhaustive cases:

1. **Some point has coverage r>=4.** Each of those r concurrent lines has q
   other points requiring another chosen line. A line not through that point
   can meet at most one of the r concurrent lines by the GQ axiom. Hence
   `|S| >= r(q+1) >= 4(q+1)`.
2. **All covered points have coverage two.** Around a chosen line L, the q+1
   neighbours are mutually disjoint. Write c_X for the number of its neighbours
   met by a chosen line X at distance two. Pass 12488's antiregularity argument
   gives `sum c_X=q(q+1)` and `sum binom(c_X,3)<=binom(q+1,3)`.

The second problem has an exact scalar relaxation. At D distance-two lines,
put `a=floor(q(q+1)/D)`, `r=q(q+1)-Da`. Discrete convexity makes the smallest
possible triple cost

`(D-r) binom(a,3) + r binom(a+1,3)`.

Take the smallest D whose cost fits the budget, add q+2, and round up to even.
Evenness of |S| follows by summing incidence rows over p-perp modulo two:
this counts precisely lines not through p; the lines through p are even too.
Finally take the minimum of this hyperoval bound and the heavy-coverage bound.

| q | general lower bound | coverage-{0,2} bound | heavy-coverage bound |
|---|---:|---:|---:|
| 3 | 10 | 10 | 16 |
| 5 | 16 | 16 | 24 |
| 7 | 24 | 24 | 32 |
| 9 | 32 | 32 | 40 |
| 11 | 42 | 42 | 48 |
| 13 | 52 | 52 | 56 |
| 17 | 72 | 76 | 72 |

These are proved lower bounds, **not exact distances**. The local triple budget
belongs to Pass 12488; this packet makes the relaxation explicit and covers
the previously separate heavy-coverage case. The stronger conjectured
quadratic bound for arbitrary even sets remains unproved.

## 4. An action for fluctuating rates changes the selection problem

Producer: `w33_20261031_tick_rate_entropy.py`.
Uses the actual 120 projectors from Pass 12055 and the October 19 operator-frame
identities. Their fixed-rate majorization theorem remains valid.

### A specified microscopic ensemble

Take N classical tick labels a_i and N two-qutrit copies. Supply the mean-field
Hamiltonian

`H_N = (1/N) sum_{i,j} (I-Pi_{a_i})^(j)`.

For an empirical rate vector phi, its quantum partition function is
`[Tr exp(-H(phi)/T)]^N`, where `H(phi)=sum phi_a(I-Pi_a)`.
The number of label configurations is `N!/product (N phi_a)!`. Stirling's
formula and the polynomial bound on the number of empirical types give the
exact large-N free-energy functional

`Phi_T(phi) = F_T(phi) + T sum phi_a log phi_a`.

Equivalently minimize jointly over phi and density matrices rho:

`E(phi,rho) - T[H_classical(phi)+S_quantum(rho)]`,
`E=1-sum phi_a Tr(rho Pi_a)`.

The all-to-all coupling and the annealed ensemble are **supplied choices**.
This is a derived action for that named model, not a derivation of the model
from W33 or a real-time local action for physical clock rates.

### Exact low-temperature limit: contexts beat single events

At zero energy every active projector fixes the support of rho. A single tick
allows rank three: maximum joint entropy log3. Distinct compatible ticks have
common rank at most one. A pure stabilizer state admits four ticks on its
commuting context, giving joint entropy log4 at equal rates. Noncommuting ticks
have no common eigenvector. Therefore log4 is the largest entropy at zero
energy, attained at one of the 360 stabilizer contexts/states.

Compactness and continuity of the two entropies give

`lim_{T->0+} min Phi_T / T = -log4`.

In comparison a single event tick gives `-log3` in that limit. Thus this
annealed model does **not** supply robust one-event real-form selection.
This does not contradict Pass 12055: it is a different, explicitly specified
ensemble in which the rates themselves have entropy.

### A proved first-order ordering transition, with bounds

At uniform rates, H=(2/3)I. On the simplex tangent space the exact Hessian has
80 eigenvalues `120T-1/(3T)` and 39 eigenvalues `120T`. Hence its local spinodal
is `T_s=1/sqrt360`, about 0.052705 (rate scale R=1).

The uniform product has energy 2/3 and entropy log1080. A pure four-tick context
trial has energy zero and entropy log4. Thus uniform cannot be globally
minimizing below `T_0=2/(3 log270)`, about 0.11908, which exceeds T_s.

Conversely the Gram-frame identity gives
`||delta Q||_F<=sqrt3||delta phi||_2`. Pinsker's inequalities for classical and
quantum relative entropy bound the entropy deficit below by half the sum of
squared norms. Applied to the exact cross term
`-Tr(delta rho delta Q)`, they prove uniform is uniquely globally minimizing
for `T>sqrt3`. Consequently the global ordering transition lies in
`[2/(3 log270),sqrt3]`, strictly above the uniform spinodal. The uniform state
remains a strict local minimum there, so the global ordering transition is
discontinuous. Its precise location and complete phase diagram are not proved.

Numerical alternating minimization is labelled as a stationary-point search.
At T=.01 the four-tick trial has Phi=-.01386294 and the event tick -.01098612.
At T=.1 uniform is locally stable yet a context trial already beats it. The
proofs above, rather than the local optimizer, establish the stated limits
and transition bounds.

### A constructive event phase, with its controlling input exposed

The entropy competition also identifies how a named model *can* favor events.
Use N classical tick labels and M quantum copies with the same Hamiltonian
`(1/N) sum_{i=1}^N sum_{j=1}^M h_{a_i}^{(j)}`. At fixed ratio kappa=N/M the
free energy per quantum copy is `F+kappa T sum phi log phi`. The zero-energy
entropy maximum is now `max(log3,kappa log4)`, so

`lim min Phi_{T,kappa}/T = -max(log3,kappa log4)`.

For `0<kappa<log3/log4` (about .79248), every zero-temperature accumulation
point is a single event tick with a maximally mixed rank-three quantum state.
For kappa above this value it is a four-tick context with a pure stabilizer
state. At the boundary both families tie. This is an open event-selecting
parameter region of an explicit microscopic ensemble, not a claim that W33
chooses that count ratio. It supplies a concrete conditional selection model;
local rate kinetics and the physical E8 real-form coupling remain separate.

## 5. A controlled continuum candidate and an obstruction to native chirality

Producer: `w33_20261031_continuum_chirality.py`.

### What the actual group permits

The normal sign kernel has nontrivial character orbits of lengths 5 and 10.
Any representation nontrivial on it contains a whole orbit, so a faithful real
representation has dimension at least five. The signed SO(5) witness attains
this minimum. Its symmetric invariant metric space has dimension exactly one:
Q=cI. It has no invariant Lorentzian form.

More generally a faithful Lorentz action of the entire perfect group needs at
least **six spacetime dimensions**. Perfectness excludes a time-orientation
sign character. Averaging the orbit of a future timelike vector under a finite
group produces an invariant timelike vector, whose spatial orthogonal
complement must still be faithful. That needs at least five dimensions. The
bound is attained by `1 plus the signed SO(5) representation`.

This only constrains an attempted **faithful spacetime action of this entire
finite group**. It does not forbid a 3+1 theory in which G acts internally,
through a quotient, or is broken. The group is not identified with the
Lorentz group or used to select a physical signature.

### An internal E6 connection with a named carrier

The signed five-axis representation naturally acts on the standard D5 weight
model `27=1_4+10_{-2}+16_1`. The code constructs all 27 weights and all 45
charge-zero, weight-zero triples. The actual six group generators preserve
this unsigned cubic support, with sector orbits 1+10+16 and cubic types 5+40.
Pass 11185 already owns that sector/cubic dictionary; the new content is the
explicit action transported from this q=5 stabilizer. A lift to the actual
signed Chevalley cubic and physical Yukawa coefficients remains unbuilt.

This also clarifies an order-based ambiguity in the earlier text of
`w33_pass11185_e6_yukawa_sectors.py`: its 1,920-element Sp(4,3) frame stabilizer
contains central +/-I, while W(D5) has trivial center. The two cannot be
identified merely because their orders match. Its sector and counting results
are retained. The 960-element projective group, a 1,920-element symplectic
double cover, and the full 1,920-element W(D5) must be kept distinct.

### A named positive control

Supply the scaled even lattice D5 and its forty root hopping directions.
The group-invariant Laplacian symbol is

`sigma_a(k)=(1/(8a^2)) sum_{r in D5 roots}(1-cos(a r.k)) -> |k|^2`,

with rigorous error `<= (5/6) a^2 |k|^4`. The code checks this convergence and
the actual six group generators. This is added five-dimensional Euclidean
locality. It is not an emergent 3+1 manifold, and its twenty root rays are not
identified with the twenty original lines.

### Changing a scalar Wilson function cannot generate a chiral index

For any square incidence/gauge matrix M and any real function f on its squared
singular values, the balanced Hermitian kernel

`H_f = [ f(M M*), M ; M*, -f(M* M) ]`

decomposes under the singular-value basis into traceless blocks with eigenvalues
`+/-sqrt(f(s^2)^2+s^2)`. If invertible, `Tr sign H_f=0` and the overlap index is
zero. This includes rank-deficient M with paired null singular spaces.

The producer tests three different f on the actual gauged W33 incidence matrix
and a rank-deficient control. GW defects are at floating-point roundoff and
every index is zero. This extends the functional scope of TOE41's specific
linear two-hop regulator; the original spectral-pairing obstruction remains
its result. It does not rule out other kernels, topology or chiral measures.
The external torus/flux controls already in the repo are not rediscovered.

## Validation, provenance and remaining scope

`tests/test_w33_20261031_five_fronts.py` checks exact group generators and
closure, independent conic/cross-ratio predicates, search completion gates,
cut-code recovery, rate curvature and entropy comparisons, the general bound's
two branches, lattice symmetry, and the generalized index obstruction.
The previous conic-bridge tests are retained as regressions.

All five research fronts were investigated. The resolved finite claims above
do not establish all five broad research goals. In particular larger-field
classification, exact general distances, a local physical vacuum and a
predictive 3+1 chiral/gravitational continuum remain open. The previous
215-page/full-week intellectual-reading task also remains incomplete; this
packet does not retrospectively claim it was finished.

### Primary literature checked

- Blokhuis, Seress, Wilbrink, *Characterization of complete exterior sets of
  conics*: https://doi.org/10.1007/BF01204717
- Van de Voorde, *On sets without tangents and exterior sets of a conic*,
  Section 3: https://arxiv.org/abs/1201.0484
- Hoffman, Singleton, *On Moore Graphs with Diameters Two and Three*:
  https://doi.org/10.1147/rd.45.0497
- De Bruyn, *Classification Results for Hyperovals of Generalized Quadrangles*:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC7340883/
- De Bruyn, *On hyperovals of polar spaces*:
  https://doi.org/10.1007/s10623-010-9400-1
- GAP Character Table Library, affine M20 module and naming check:
  https://www.math.rwth-aachen.de/homes/Thomas.Breuer/ctbllib/ctbltoc/data/2%5E4colonA5.html
- Gibbs variational principle, primary early treatment:
  https://doi.org/10.1103/PhysRev.96.18
- Ginsparg-Wilson: https://doi.org/10.1103/PhysRevD.25.2649
- Luescher, exact modified lattice chirality:
  https://arxiv.org/abs/hep-lat/9802011

## Five independent next investigations

- Prove an all-q exterior-arc exclusion, rather than extending finite searches indefinitely.
- Strengthen the general even-set bound where heavy coverage or unpaired structure defeats Moore counting.
- Derive a local rate model whose ensemble and interactions select the desired physical vacuum.
- Build a native regulator outside the paired H_f family with a nonzero, stable index and anomaly checks.
- Construct an explicit internal-symmetry/spacetime coupling that respects the faithful-representation obstruction.
