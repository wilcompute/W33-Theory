# BT4214-BT4221 — canonical small-cover/SU(4)/hysteresis/clock/Hawking/Pell/vacuum/velocity packet

Status: `PASS_EXACT_EIGHT_FRONT_WITH_SMALL_COVER_SU4_HYSTERESIS_CLOCK_FULL_GAUSSIAN_PELL_VACUUM_VELOCITY_BOUNDARIES`.

Frozen certificate: `data/PART_4214_4221_SMALL_COVER_SU4_QUANTUM_HYSTERESIS_CLOCK_HAWKING_PELL_VACUUM_VELOCITY.json`.

Semantic SHA-256: `2b2e3951e7e5a017cd41217d764ab34cc1e74ec23ba28b72044bb0126cf1bce4`.

## Renumbering note

Glue-track commit `84db6db5c80a99b21c58f21351774eb522e031b4` reserved Pass 4213 before this physics block was reserved. Commit `ee0af6eaf011c596cbfa8078c47f7b0127bcf10b` explicitly directed the physics packet to 4214--4221. The earlier 4213--4220 namespace is therefore retained only as collision history and is noncanonical. The computations below are unchanged; only their pass identifiers were shifted by one.

## Pass 4214 — explicit 359-sheet girth-14 Levi cover

The corrected W(3,3) point-line Levi graph has 80 vertices, 160 edges, degree four, girth eight, and fundamental-group rank 81. Gauge-fixing a BFS spanning tree leaves 81 cotree voltage variables. The exact simple-cycle constraints consist of 1,620 length-eight, 5,184 length-ten, and 43,200 length-twelve cycles.

A deterministic frozen `Z_359` voltage assignment gives nonzero voltage on all 50,004 cycles. Therefore the cover has 28,720 vertices, 57,440 edges, and certified girth at least 14. It is 182.5543175 times smaller than the earlier `Z_65537` certificate. The full voltage vector hash is `6ef49dddf452edd7ffce8d99ddf87cc10170847675aa4b0f837f203088736779`. The search establishes an explicit construction, not global minimality.

## Pass 4215 — dense SU(4) holonomic gate generation

Each rank-two singlet bundle already supports dense local SU(2) from the exact Wilczek--Zee loops. For two bundles, add one auxiliary bright level coupled only to computational `|11>`. An adiabatic Bloch-sphere loop of solid angle `2*pi` gives Berry phase `pi` on `|11>`, hence exact computational holonomy `CZ=diag(1,1,1,-1)`.

`CZ|++>` has concurrence one. Explicit commutator closure of local Pauli generators and their CZ conjugates spans all 15 traceless two-qubit Pauli directions. Thus dense local `SU(2)xSU(2)` plus this geometric entangler has dense closure `SU(4)`.

## Pass 4216 — quantum reduction of the hysteretic scale bit

For

`ds/dt = gamma[ln80 - 4s + g n_B(2e^-s) - 0.004 n_B(2e^-s)^2]`,

classical equal-well coexistence occurs at `g=0.5700939873487846`. The left minimum, barrier, and right minimum are respectively

`1.2870434725072475`, `3.8542873086844556`, `5.3097911843769285`.

The common barrier is `4.459741211737891`. With dimensionless kinetic mass one, the zero-energy instanton action is `7.788170121507699`, so the tunnelling amplitude contains `exp[-7.7881701215 sqrt(M)/hbar_eff]`. For `D=0.25`, the Kramers lifetimes are `8.9680991e7` and `2.9529576e7` model-time units. The logical two-state reduction is `H_eff=-(Delta/2)sigma_x+(epsilon/2)sigma_z`; unbiased erasure obeys the `kT ln2` Landauer floor.

## Pass 4217 — exact three-local clock compressed to 61 auxiliaries

The previous exact three-local Gray history used 72 condition-AND ancillas and 24 transition flags. An exact MILP over all balanced `2+2` decompositions of the 24 four-literal spectator conditions proves that only 13 shared pair conjunctions are required. Adding 24 final condition ancillas and 24 transition flags yields 61 auxiliaries total, a 36.4583% reduction from 96.

The propagation remains exactly three-local with the same legal gap `2 Omega`, perfect-transfer time `pi/(2 Omega)`, and full revival `pi/Omega`. The 13-pair optimum is only within this frozen balanced-tree compilation class, not a global minimum over all clock encodings.

## Pass 4218 — complete 19-mode Gaussian Hawking resource hierarchy

The finite chain contains one outgoing, nine partner, and nine environment modes (38-dimensional Nambu map). At zero uniform thermal loading, outside-versus-partners has logarithmic negativity `0.2085352998331478`, outside-to-partners Gaussian steering `0.0085289241216891`, reverse steering `0.023218011304377176`, and outside-to-partners coherent information `0.05180133511382398` nats.

Uniform thermal loading destroys the resources at distinct thresholds:

1. outside-to-partners steering: `n_th=0.004282699509245052`;
2. positive outside-to-partners coherent information: `0.007925058160578414`;
3. partners-to-outside steering: `0.011744823769689085`;
4. PPT entanglement: `0.11593620709206348`.

For the frozen 512-sample correlated-disorder ensemble at `n_th=0.005`, all 512 remain PPT-entangled; outside-to-partners steering survives in 228, positive coherent information in 415, and reverse steering in 482.

## Pass 4219 — Pell near-echoes, but no exact global recurrence

The Levi adjacency spectrum is `{0,+/-4,+/-sqrt(6)}`. Because `4/sqrt(6)` is irrational, no finite nonzero time can make all eigenphases commensurate, so exact global continuous-time-walk revival is impossible.

Nevertheless, `11760^2-6(4801)^2=-6` gives a controlled near-echo at `t=4801*pi/2=7541.393164942298`. The operator-norm recurrence error is `4.007133400667635e-4`. Pell multiplication by the fundamental unit `5+2sqrt(6)` yields exponentially improving subsequences.

## Pass 4220 — exact point/line harmonic-vacuum entanglement

For `K=5I-A_Levi`, the point-line incidence singular values are `4^1`, `(sqrt6)^24`, and `0^15`. A singular channel sigma contributes one-side symplectic eigenvalue

`nu(sigma)=1/4 sqrt(2+10/sqrt(25-sigma^2))`.

Thus the 15 zero-singular channels are unentangled, while the coupled channels sum to point-versus-line ground-state entropy `2.455297387200524` nats (`3.542245364421825` bits) and logarithmic negativity `6.980418739066683` nats.

## Pass 4221 — high-girth radial information velocity

On the degree-four tree that locally models the girth-14 cover, shell sizes are `N0=1` and `Nr=4*3^(r-1)`. In normalized radial coordinates the bulk hopping is `sqrt(3)J`, giving

`E(q)=2 sqrt(3) J cos q`,

and maximum radial group velocity

`v_max=2 sqrt(3)J=3.4641016151377544 J`.

A girth-at-least-14 ball is tree-like through radius six, whose ballistic boundary time is `sqrt(3)/J`. Branching therefore grows parallel channel capacity as `3^r` while radial propagation speed grows only as `sqrt(3)`. This graph velocity is not identified with physical `c`.

## Evidence boundary

These are exact finite graph-cover, holonomic-control, effective stochastic/semiclassical, clock-gadget, Gaussian-channel, recurrence, harmonic-network, and high-girth tree-band statements. They do not establish fabricated hardware, observed Hawking radiation, physical spacetime memory, measured quantum vacuum entanglement, a speed-of-light derivation, gravity, cosmology, or a theory of everything.
