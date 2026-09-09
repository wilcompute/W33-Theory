# Eight experiments in representation, observation and physical accounting

Seven mathematical/computational investigations are executed below. Physical
reset-work collection (item 4 of the eight requested investigations) remains
blocked by missing instrument data. Its protocol and analyzer are implemented;
no synthetic output is counted as a physical measurement. This extends
`W33_COMPUTATION_RESOURCE_FRONTIERS.md` (7594f2006) and cites the parallel
Holotrade depth work rather than claiming a new orbit census.

## 1. Reversible noise seeds: retain the cause, clear the record

Two unbiased seed bits a,b generate an error E=2(a+b-1), giving probabilities
1/4,1/2,1/4 for errors -2,0,2. For L independent timings, the seed register uses
2L bits, but the errors have only 1.5L bits of entropy. Given Y and the seed S,
the entire noisy record O is determined. The executable map is

    (Y,S,R) -> (Y,S,R XOR encode(O(Y,S))).

It is a total involutive permutation, with a documented extension outside the
valid Y ensemble. The n=3,L=2 instance checks 65,536 states. Correlated records
are cleared; Y and the four seed bits remain. Here H(O|Y,S)=0, while H(S|Y,O)=1
bit: a zero error has two possible seed preimages. The two equal-probability
zero-error seeds cannot simply be merged reversibly. This quantifies both the
retained storage and the information left over after observing its effect.
It does not erase S or establish a zero-heat device. The accounting is within
[Bennett's reversible-computation framework](https://arxiv.org/abs/physics/0210005).

## 2. Authenticated redundant arithmetic removes repeated borrow chains

Represent a logical natural number as P-N, with P>=N and both physical counters
monotone. Logical INC increments P. Logical DEC increments N if P!=N, otherwise
it is a no-op. The invariant makes an ordering comparison unnecessary:
canonical authenticated root equality decides precisely whether P=N.
Trusted genesis creates (value,0); verified transitions preserve the invariant.
An arbitrary externally supplied root pair is not admitted by this construction.

`w33_monotone_difference_counter.py` implements this adapter using existing
zipper INC proofs. Its verifier uses only the trusted pre-state and opened proof
nodes, without reading a store or decoding integers. Operation dispatch selects
which physical counter may change. Truncation, wrong-counter, changed-transition
and nonempty zero-decrement proofs are rejected. This is an arithmetic primitive;
it does not replace the two-register guest ABI or its process-consumption owner.
General redundant counters are established algorithmic prior work; see the
[increment/decrement exercise in Mehlhorn's course](https://people.mpi-inf.mpg.de/~mehlhorn/DatAlg2008/Ex0809.pdf).

For U increments, D successful decrements and Z zero decrements,

    T = Z+5(U+D)+2s(P0)+2s(N0)-2s(Pf)-2s(Nf).

This is the sum of the two earlier monotone cost laws. From (0,0), arithmetic
microticks are at most Z+5(U+D), irrespective of the interleaving. At arbitrary
initial values, the initial potential is explicit. Wrapper hashing, program
validation and wall-clock time are outside this tick accounting.

All 320 six-operation paths from starting values 0..4 pass. For 128 INC/DEC
cycles around 2^64, the old binary representation costs 33,536 ticks; the new
one costs 1,390, with the same final logical value. It retains 489 distinct
nodes in this no-GC run. P and N grow with execution history even if P-N stays
small. Normalization or collection can incur work; equality between *different*
pair representations is not reducible to root equality. These costs have not
been hidden behind an amortized physical-performance claim.

## 3. Coherent ternary erasure with explicit gates

For radix three, write X=q3^m+r and Y=X+3^m. The carry category k_3(q) is the
number of trailing zero trits of floor(Y/3^m), capped at d=n-m. Store the timing
statistic as m low trits r and d unary prefix trits. This uses n record trits;
it is deliberately a different, redundant encoding from the binary eraser.

A chain of equality-controlled modular shifts computes prefix flags on d clean
qutrit ancillas. Subtract r and those flags from the record modulo three, then
reverse the chain. Every gate is a total permutation; the declared basis is
one- or two-equality-controlled qutrit shifts. There are 3d+2m gates. This is an
explicit logical qutrit circuit, not a decomposition into a particular device's
native gates or into Clifford+T. Exact constructions for such controlled qutrit
operations are prior work:
[Yeh and van de Wetering](https://arxiv.org/abs/2204.00552).

The n=3,m=1 circuit has eight gates on nine qutrits, including two clean
ancillas. All 19,683 basis states form a permutation and pass the inverse
check. A complex superposition of all 27 valid inputs, with distinct phases,
transforms to the same amplitudes on Y with record and ancillas zero. The
maximum state-vector error is zero in the simulation. Removing an uncompute
gate fails a negative control. No coherent physical device was measured.

## 4. Physical reset-work experiment: analyzer ready, collection blocked

The live `/sys/class/powercap` tree contains no energy counters. Holotrade's
`data/telemetry_shadow_host.json` independently records `raplEnergy: false`
and null energy deltas. Neither source provides work measurements for a
controlled reset experiment. A user query requesting an accessible instrument
or recorded dataset remains unanswered at publication preparation.

The experiment should prepare a random bit R and, in the side-information arm,
a retained perfect copy S. Compare a reset of R with the reversible operation
R <- R XOR S. Use the same physical encoding and starting/ending Hamiltonian,
record the fate of S, randomize protocol order, measure repeated cycles, and
account for controller/seed resets separately. A logically reversible operation
can still dissipate substantial work. The ideal conditional-information bounds
are ln(2) kBT without S and zero with S, under symmetric degenerate-memory
assumptions; this does not predict the actual difference in device energy.

The implemented CSV analyzer consumes protocol, temperature, work and internal
energy change in SI units. It computes heat to the bath Q=W-Delta U, per-cycle
Q/(kBT), means and standard errors for both protocol groups. Standard errors
assume independent cycles; an experiment with drift or autocorrelation needs
blocking/covariance analysis. Provenance requires device identity, calibration
reference, raw-source reference and `hardware-measured` source class. A SHA-256
digest binds the ingested CSV. Those fields are experimenter attestations, not
independent instrument authentication. Negative admission tests reject synthetic
source labels and incomplete provenance.

    python analysis/w33_reversible_observation_experiments.py \
      --measurements /path/cycles.csv --metadata /path/provenance.json

No measurement file is supplied by this packet. The internal arithmetic fixture
is explicitly synthetic and excluded from physical results. Status remains
`BLOCKED_NO_PHYSICAL_DATA`; a software timing benchmark or another paper's
unrelated work measurement cannot close this item.

## 5. Exported Holotrade preimages and actual signed-sampler checks

Holotrade's new `analysis/signed_pencil_sampling_witness.py` reuses its existing
geometry. It constructs one mass-12 depth-one and one mass-16 depth-two profile,
exports all 40 signed point coefficients and all 40 line excesses, and verifies
N^T x=e exactly. The mass-16 histogram is 26 zeros, 12 ones and two twos, matching
the earlier class. It does not rerun the long orbit census or prove a blocker.
Prior ownership is 1075622/66062ec, per decision-17889096.

Depth is independently checked by an exact positive-pencil cover search. Choose
a positive residual line: every cover must choose one of its four points.
Subtract the candidate pencil and recurse. Exhaustion covers every possibility.
For depth at most one, also try all 40 possible negative pencils. A supplied
preimage achieves depth two while every smaller depth is ruled out.

For each profile, 40 indicator observables and an alternating-sign observable
check the signed sampler's mean and second moment using exact fractions. The
integer l1 weights are 5 and 8, giving second-moment bounds 25/9 and 4. These are
bounds for the specified pencil sampler, not universal optimal sampling costs.

## 6. Extra experiment: common noise cancels in timing differences

Reusing one two-bit seed across L timings reduces seed storage, but creates a
common additive offset. An observer can subtract the first timing from every
other timing and eliminate that offset exactly. Finite probability enumeration
for n=3 gives:

| Timings | Independent jitter leakage | Shared jitter leakage |
|---|---:|---:|
| 1 | 0.808965 bits | 0.808965 bits |
| 2 | 1.364110 bits | 2.500000 bits |
| 4 | 2.005035 bits | 3.000000 bits |

For two and four timings, the differences alone recover all the information
present in the exact timing transcript. Reversible seed retention therefore
needs an observer model: seed reuse can save memory while undoing privacy.
This is the specified additive-error model, not a measured side-channel attack.

## 7. Extra experiment: exact padding versus leakage frontier

For one increment from a uniform four-bit input, exact durations are
3,5,7,9,11 with multiplicities 8,4,2,1,1. Enumerate all 16 contiguous partitions
of that ordered alphabet, padding every member to its group's maximum. This
exhausts the stated deterministic policy family; it does not exhaust randomized
or nonmonotone policies. Thirteen policies are nondominated in expected delay
and information leakage.

No padding leaks 1.875 bits. An expected 13/8 extra ticks reduces this to about
0.811278 bits. Zero timing leakage requires padding all completions to tick 11,
adding exactly 49/8 expected ticks. The finite frontier is stored in the
certificate. Physical observers may also see intermediate events, power or
memory accesses, which this duration-only policy does not conceal.

## 8. Extra experiment: fractional relaxation fails to remove negativity

The proposed integrality-gap search returned **no gap** for the two exported
representatives. This is a useful negative result: real-valued coefficients
have the same minimum l1 weight as integer coefficients. SciPy proposes primal
and dual vectors, but exact rational checks, not solver tolerance, certify them.
For B=N^T, the certificate proves

    Bx=e,  |B^T y|<=1,  ||x||_1 = y.e.

For any real preimage z, y.e=y.Bz<=||z||_1. The supplied primal meets this bound,
proving optima 5 and 8 over the real numbers. Thus the selected depth-one/two
profiles require negative coefficients even after relaxing integrality. The
general signed-sampling principle is prior work:
[Pashayan, Wallman and Bartlett](https://arxiv.org/abs/1503.07525).
This says nothing about a quantum state's magic or an unrestricted simulator.

## Reproduce and scope

    python analysis/w33_monotone_difference_counter.py
    python analysis/w33_reversible_observation_experiments.py
    # In Holotrade (numpy/scipy required):
    python analysis/signed_pencil_sampling_witness.py

The certificates distinguish logical PASS from missing physical data. The
three additional ideas are completed experiments even though the integrality-gap
hypothesis was refuted for the tested objects. New source/proof results were
searched against both repos and the result index; no worldwide novelty claim
is made. Full earlier history/manuscript intake is still incomplete. GitKraken
found neither repo advanced at this turn's initial fetch.

## Parallel update during publication

W33 f89225a7d adds `w33_signed_representation_economics.py`, which keeps
semantic steps, authenticated retention, replay and signed-sampling factors
in separate ledger coordinates. That distinction is consistent with this
report's arithmetic-microtick and estimator-only bounds. Its nine checks pass.
Holotrade 26dcf6c/604215f/e45fd0a extends our published019e443 sampler source
to all seven mass-16 exceptional orbits and the one-pencil mass-20 descendant
frontier. We read the complete source delta; its larger census/decoder run is
not rerun in this packet. The two-representative witnesses here retain their
original scope and ownership. Full mass-20 classification is not claimed.
