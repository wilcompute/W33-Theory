# BT4213-BT4220 — small high-girth cover, SU(4) holonomy, quantized hysteresis, compressed clock, full Hawking channel, Pell echo, vacuum entanglement, and information velocity

Status: `PASS_EXACT_EIGHT_FRONT_WITH_SMALL_COVER_SU4_HYSTERESIS_CLOCK_FULL_GAUSSIAN_PELL_VACUUM_VELOCITY_BOUNDARIES`.

Frozen certificate: `data/PART_4213_4220_SMALL_COVER_SU4_QUANTUM_HYSTERESIS_CLOCK_HAWKING_PELL_VACUUM_VELOCITY.json`.

Semantic SHA-256: `c79c7edd47d9d038b921838df73baba17d74043af4c74a0d3d35543335019d26`.

## Pass 4213 — shrink the explicit high-girth Levi cover

The corrected W(3,3) point-line Levi graph has 80 vertices, 160 edges, degree four, girth eight, and free fundamental-group rank 81. Pass 4189 exhibited a Z_65537 voltage assignment with nonzero voltage on every simple base cycle of lengths 8, 10, and 12, hence a 5,242,960-vertex cover with girth at least 14.

Gauge-fix a BFS spanning tree to zero voltage. Only the 81 cotree edges remain independent. The short-cycle constraints are exactly 1,620 length-eight cycles, 5,184 length-ten cycles, and 43,200 length-twelve cycles, for 50,004 nonzero linear conditions.

A finite min-conflict search over prime cyclic voltage groups found a Z_359 assignment. The frozen 81-coordinate vector is stored in the certificate. Re-evaluation of all 50,004 cycles gives zero violations:

- length 8: 0/1,620 zero-voltage cycles;
- length 10: 0/5,184;
- length 12: 0/43,200.

Therefore the explicit cover has

- 80*359 = 28,720 vertices;
- 160*359 = 57,440 edges;
- certified girth >= 14.

This is a 182.5543-fold reduction in sheet count and vertex count relative to the earlier Z_65537 certificate. No global minimality claim is made; 359 is the smallest solution found in this search campaign.

## Pass 4214 — two singlet bundles generate dense SU(4)

Pass 4190 established that the two exact Wilczek-Zee loops Uy and Uz generate a dense SU(2) on one rank-two singlet bundle. Take two such bundles as two logical qubits.

Introduce one auxiliary bright state |a> that couples only to the computational state |11>. In the two-level subspace span{|11>,|a>}, adiabatically transport the instantaneous eigenstate around a Bloch-sphere loop enclosing solid angle 2*pi. Its Berry phase is pi modulo 2*pi. The other three computational states remain spectators. The computational holonomy is therefore exactly

`CZ = diag(1,1,1,-1)`.

CZ acting on |++> produces concurrence one, so it is entangling. An explicit Pauli commutator closure starting from all six local one-qubit generators and their CZ conjugates spans all 15 traceless two-qubit Pauli generators. Hence the closure is SU(4).

Thus dense local SU(2) x SU(2) plus this exact geometric CZ yields dense two-qubit SU(4). This is a finite holonomic universality construction, not a fabricated or fault-tolerant processor and not a proof that one auxiliary level is globally minimal.

## Pass 4215 — quantized hysteretic scale memory

Use the saturating scale flow

`ds/dt = gamma [ln80 - 4s + g n_B(2e^-s) - 0.004 n_B(2e^-s)^2]`.

Define U'(s)=-F(s). At the classical coexistence coupling

`g_coex = 0.5700939873487846`,

the stationary points are

- left minimum: s_L = 1.2870434725072475;
- barrier: s_B = 3.8542873086844556;
- right minimum: s_R = 5.3097911843769285.

The two minima have equal potential and the common barrier height is

`Delta U = 4.459741211737891`.

The curvatures are 3.0125453867, -5.0904166704, and 27.7856122786 at left, barrier, and right respectively.

For a dimensionless kinetic mass M=1, the zero-energy semiclassical instanton action across the barrier is

`S0 = integral sqrt(2[U(s)-Umin]) ds = 7.788170121507699`.

Hence the tunnel amplitude carries the exponential factor exp[-S0 sqrt(M)/hbar_eff]. At M=hbar_eff=1 this factor is 4.1461087778e-4; its square is 1.7190217997e-7. This is only the exponential part: an absolute tunnelling frequency requires a physical kinetic calibration.

For the overdamped Langevin realization with D=0.25, Kramers theory gives

- left -> right rate 1.1150635033e-8 and lifetime 8.9680991e7;
- right -> left rate 3.3864353395e-8 and lifetime 2.9529576e7.

Projecting onto the two metastable wells yields the effective logical Hamiltonian `H_eff=-(Delta/2)sigma_x+(epsilon/2)sigma_z`. At equilibrium entropy production is zero; away from equilibrium the two-state entropy production is `(pL kLR-pR kRL) ln[(pL kLR)/(pR kRL)] >= 0`. Erasing an unbiased logical bit costs at least `kT ln 2`.

## Pass 4216 — 96 auxiliary clock bits -> 61

The exact three-local clock from Pass 4188 used 72 AND ancillas plus 24 transition flags. The 72 AND ancillas arose because every one of the 24 four-literal Gray spectator conditions was compiled independently as a three-AND tree.

There are only 37 distinct two-literal pair conjunctions available across all three balanced 2+2 decompositions of the 24 conditions. An exact mixed-integer linear program chooses one pairing per transition while minimizing the union of pair conjunctions. The optimum is 13 shared pair ancillas.

The resulting exact architecture uses

- 13 shared pair conjunctions;
- 24 final four-literal condition ancillas;
- 24 dynamic transition flags;
- total AND ancillas 37;
- total auxiliary ancillas 61;
- 5 Gray clock qubits, for 66 clock/control qubits total.

This removes 35 of the 96 auxiliaries, a 36.4583% reduction, while leaving the existing exact three-local propagation construction unchanged: legal gap 2 Omega, perfect transfer at pi/(2 Omega), and full revival at pi/Omega.

The number 13 is certified optimal only within the balanced 2+2 AND-tree decomposition of these frozen 24 Gray spectator conditions, not over every imaginable clock encoding.

## Pass 4217 — full 19-mode Hawking channel

The full Gaussian model contains one outgoing mode, nine partner modes, and nine greybody/environment modes: 19 annihilation modes and a 38-dimensional Nambu map.

At zero thermal loading the outside-versus-nine-partner state has

- logarithmic negativity 0.2085352998331478;
- Gaussian steering outside -> partners 0.0085289241216891;
- Gaussian steering partners -> outside 0.023218011304377176;
- coherent information outside -> partners 0.05180133511382398 nats;
- reverse coherent information -0.011752693847972256 nats.

Under uniform thermal loading the resource thresholds separate:

1. outside -> partners steering dies at n_th = 0.004282699509245052;
2. outside -> partners coherent information crosses zero at 0.007925058160578414;
3. partners -> outside steering dies at 0.011744823769689085;
4. PPT entanglement survives until 0.11593620709206348.

The hierarchy is therefore not merely entangled/not-entangled: directionality and communication witnesses disappear much earlier.

The correlated-disorder audit uses 512 deterministic Gaussian samples with sigma_log(r)=0.35, sigma_logit(Gamma)=0.25, and two-cell correlation length. At n_th=0 all 512 remain entangled, steerable in both directions, and positive in outside->partner coherent information. At n_th=0.005:

- entangled: 512/512;
- outside -> partners steerable: 228/512;
- partners -> outside steerable: 482/512;
- positive coherent information: 415/512.

This is an exact finite Gaussian-channel audit for the stated ensemble, not observed Hawking radiation or a theorem for arbitrary channels.

## Pass 4218 — Pell near-echoes and the exact recurrence obstruction

The Levi adjacency spectrum contains 0, +/-4, and +/-sqrt(6). Exact nonzero global continuous-time-walk revival would require 4t and sqrt(6)t to be simultaneous integer multiples of 2*pi. Because 4/sqrt(6) is irrational, no such finite nonzero t exists.

Nevertheless Pell-type Diophantine approximants produce controlled near-recurrences. If x is divisible by four and

`x^2 - 6 m^2 = -6`,

then at `t=pi m/2` the +/-4 sectors revive exactly and the +/-sqrt(6) phase mismatch is `(pi/2)(m sqrt(6)-x)`.

For m=4801 and x=11760,

- x^2-6m^2=-6 exactly;
- t=7541.393164942298;
- phase mismatch 4.007133427477225e-4;
- operator-norm recurrence error 4.007133400667635e-4.

Multiplication by the fundamental Pell unit 5+2sqrt(6) generates exponentially improving subsequences. This is a spectral recurrence result for the finite walk, not a physical clock.

## Pass 4219 — exact point-line vacuum entanglement

Consider the harmonic network with kernel `K=5I-A_Levi`, corresponding to mass^2=1. The point-line incidence singular values are

- sigma=4 with multiplicity 1;
- sigma=sqrt(6) with multiplicity 24;
- sigma=0 with multiplicity 15.

After singular-vector decomposition, every nonzero sigma is one independent coupled point-line oscillator pair. The one-side symplectic eigenvalue is

`nu(sigma)=1/4 sqrt(2+10/sqrt(25-sigma^2))`.

Hence

- nu(4)=1/sqrt(3);
- nu(sqrt(6))=(1/4)sqrt(2+10/sqrt(19));
- nu(0)=1/2, so the 15 zero-singular channels are unentangled.

Summing the pure Gaussian pair entropies gives exact point-versus-line vacuum entanglement

- von Neumann entropy = 2.455297387200524 nats = 3.542245364421825 bits;
- logarithmic negativity = 6.980418739066683 nats.

This is a finite harmonic-network ground state, not measured vacuum entanglement or a continuum area-law theorem.

## Pass 4220 — high-girth information velocity

On the degree-four tree that locally models the high-girth Levi covers, shell sizes are

`N_0=1`, `N_r=4*3^(r-1)` for r>=1.

In the normalized radial basis, the root-to-first-shell hopping is 2J while the bulk shell hopping is sqrt(3)J. The bulk radial band is

`E(q)=2 sqrt(3) J cos q`,

so the maximum radial group velocity is

`v_max = 2 sqrt(3) J = 3.4641016151377544 J`.

A girth-at-least-14 cover has tree balls through radius six. The fastest bulk radial front reaches that boundary after

`6/v_max = sqrt(3)/J = 1.7320508075688774/J`.

The structural lesson for the photon/information analogy is precise: branching makes shell capacity grow as 3^r, but it increases the radial band velocity only through sqrt(3). Packing more internal nodes therefore increases parallel channel capacity far faster than it increases propagation speed. This finite graph velocity is not identified with physical c and is not claimed to be the optimal Lieb-Robinson velocity for every state.

## Evidence boundary

All eight statements are finite graph-cover, holonomic-control, effective stochastic/semiclassical, exact clock-gadget, Gaussian-channel, spectral-recurrence, harmonic-network, or high-girth tree-band statements. They do not establish a fabricated device, observed Hawking radiation, physical spacetime memory, a measured quantum vacuum, a speed-of-light derivation, gravity, cosmology, or a theory of everything.
