# Passes 4161–4168 — broader anomaly search, relational hardware, noisy decoding, storage, nonlinear landscape, and three outside-box probes

## Evidence status

Exact packet status: `PASS_EXACT_BROADER_ANOMALY_HARDWARE_GRAPH_QUANTIZED_T7_STORAGE_BOUND_LANDSCAPE_PUSH_SEARCH_RESISTANCE_DIAMONDS`.

Frozen semantic certificate: `db91cd6c70138d44917ba4274a7d087927caec691be5d49efd83528e7f8d4bd5`.

The promoted results below are finite algebraic, combinatorial, MILP, or deterministic finite-corpus statements. They do **not** derive the Standard Model, fabricate a processor or photonic chip, prove a globally complete nonlinear landscape, establish quantum speedup experimentally, derive physical inertia, establish a spacetime entropy law, or prove gravity/cosmology/a theory of everything.

## Pass 4161 — broader representation anomaly optimization

The search family was expanded from fundamental/singlet color representations to

- `SU(3) ∈ {1,3,3bar,6,6bar,8}`,
- weak dimensions `1,2,3`, and
- `Y=n/6`, `-6 ≤ n ≤ 6`.

This gives 228 nontrivial candidate species. The exact integer anomaly coordinates are `SU3^3`, `12 SU3^2 U1`, `12 SU2^2 U1`, `6 grav^2 U1`, and `216 U1^3`.

The original 145-state carrier has anomaly vector `(-28,-28,-69,-222,-3594)`. An exact MILP gives a minimum added one-particle dimension of **68**, hence a **213-state** anomaly-free carrier within this finite family. The dimension-optimal representative uses 35 multiplets and has added Dynkin loads `T3=11`, `T2=7.5`.

A second exact optimization minimizes the possible added color Dynkin load over the entire finite family and still gives `T3 >= 11`. Since the original carrier already carries `T3=16`, the repaired color load is at least 27. In the stated Weyl-only one-loop convention,

`b0_SU3 = 11 - (2/3)*27 = -7`.

Thus **one-loop SU(3) asymptotic freedom is impossible inside this finite repair family**. This is a useful negative result: anomaly cancellation alone can make the representation burden worse even while decreasing total state count.

## Pass 4162 — bounded-degree hardware graph for the 58-mode relational lift

The 28 dual-rail payload qubits are arranged on a complete binary tree. Each logical tree edge is implemented with the full `K2,2` rail coupling, each dual rail has an internal rung, and the exposed clock mode couples to the reservoir and root rails.

The resulting physical graph has:

- 58 modes,
- 139 pair couplers,
- maximum mode degree 7,
- logical tree diameter 8,
- root eccentricity 4.

Nearest-neighbor payload primitives retain 2- or 3-mode support. Routing an arbitrary payload CNOT to one adjacent tree edge and restoring it gives an exact depth upper bound `2*(8-1)+1 = 15`; an arbitrary clock-controlled payload gate has depth at most `2*4+1 = 9`.

A 28-qubit GHZ state needs one Hadamard followed by four binary-tree CNOT layers, for depth **5** and 27 CNOTs. This is a connectivity/routing contract, not a fabricated or fault-tolerant processor.

## Pass 4163 — quantized noisy seven-fault theorem

The two low-dynamic-range integer moment rows from Pass 4147 are reused. For lattice-amplitude errors

`e = Delta z`, `support(z) <= 7`, `|z_i| <= K`,

and additive measurement noise satisfying

`||eta||_infinity < Delta/2`,

all incidence and weighted measurements can be divided by `Delta` and rounded componentwise to recover the exact integer syndrome. The inherited stacked-spark certificate `spark >= 15` then makes the seven-sparse integer error unique.

The direct weighted-channel full-scale range is `7*K*11992`. Signed ADC requirements are therefore 18 bits for `K=1`, 19 bits for `K=3`, and 22 bits for `K=15`.

If the weighted accumulation is performed modulo the certified prime `p=24001`, only 15 residue bits are required, provided `2K<p`. This modular accumulator is an architecture requirement, not a claim that analog dynamic range disappears for free.

## Pass 4164 — storage primitive comparison

The exact nine-slot serialization schedule requires up to eight 5-ps storage intervals, i.e. 40 ps. At assumed group index 2, a low-loss tapped delay bank requires only about **5.996 mm** maximum path imbalance.

Using the current public LIGENTEC AN800 delay-line figure `<5 dB/m`, the longest 6-mm delay contributes `<0.03 dB` per use and `<0.15 dB` over five uses. This is a tenfold propagation-loss improvement over the prior explicit `0.5 dB/cm` comparison point.

A passive single-pole resonator has a sharp time–bandwidth conflict for an unreshaped 5-ps pulse. Storage of 40 ps below 1 dB requires approximately `Q >= 2.11e5`, whereas a transform-limited 5-ps Gaussian pulse with about 88-GHz bandwidth requires `Q <= 2.20e3` to fit the linewidth. Meeting the bandwidth condition would imply about **96 dB** storage loss over 40 ps. High-Q therefore fixes lifetime while destroying input bandwidth for this pulse model.

The present first physical storage candidate is therefore a foundry-qualified low-loss tapped delay bank. Resonant or frequency-bin storage remains interesting after explicit pulse reshaping / conversion losses are included.

## Pass 4165 — global mixed-landscape basin push

A maximum-principle argument gives globally valid equilibrium boxes. At a vertex attaining the maximum signed amplitude, the graph-Laplacian term is dissipative. The resulting scalar bounds are:

- selector 24: `|u| <= 2.50439835`, `|v| <= 2.13976351`;
- selector 15: `|u| <= 3.79360056`, `|v| <= 3.53797676`.

A deterministic macroscopic corpus then used 64 sequential uniform `[-0.5,0.5]^80` initial conditions for each selector, BDF evolution to `t=160`, full 80-variable Newton refinement, and canonicalization under all 25,920 projective symplectic permutations plus global sign.

Selector 24 produces **29** canonical roots: five pure bivalent classes and **24 mixed** classes. Of the mixed classes, **23 are stable** and one has Morse index one. Comparing against the old 64-seed small-noise corpus, only four mixed classes overlap. Therefore **20 macro-corpus mixed classes are new**, of which **19 are stable** and one is index one.

Selector 15 produces four canonical classes: one pure class and three mixed classes, with two stable mixed roots and one index-one saddle.

This decisively falsifies the idea that the near-zero perturbative basin census captures the full stable landscape. It still does not prove a globally complete 80-dimensional equilibrium catalogue.

## Pass 4166 — outside-box: exact W33 search reflection

The uniform projector is a quadratic adjacency polynomial:

`P0 = (A^2 + 2A - 8I)/160 = J/40`.

Hence the diffusion reflection is

`R = 2P0 - I = (A^2 + 2A - 88I)/80`.

With a marked-vertex oracle `O_w=I-2|w><w|`, the iterate `G=R O_w` is the usual two-dimensional Grover rotation, but with the diffusion reflection compiled exactly from the W33 adjacency algebra. Starting from probability `1/40`, four oracle queries give exact success

`3920137321 / 4000000000 = 0.98003433025`.

No hardware speedup is claimed.

## Pass 4167 — outside-box: exact effective-resistance metric

The W33 Laplacian pseudoinverse is

`L^+ = (7/80)I + (1/160)A - (13/3200)J`.

It gives only two nonzero pairwise resistance distances:

- adjacent vertices: `13/80` for 240 pairs;
- nonadjacent vertices: `7/40` for 540 pairs.

Their ratio is exactly `14/13`, and the Kirchhoff index is `267/2 = 133.5`.

This is an exact resistor-network metric. Interpreting it as an 'inertial' geometry is only an analogy; it does not derive physical mass or inertia.

## Pass 4168 — outside-box: finite Levi causal diamonds

The 80-vertex Levi graph has diameter four. Every unordered pair belongs to exactly one of four interval types:

- distance 1: 160 pairs, interval size 2, one geodesic, layers `1,1`;
- distance 2: 480 pairs, interval size 3, one geodesic, layers `1,1,1`;
- distance 3: 1,440 pairs, interval size 4, one geodesic, layers `1,1,1,1`;
- distance 4: 1,080 pairs, interval size 14, four geodesics, layers `1,4,4,4,1`.

Defining finite geodesic entropy `S=ln(number of shortest paths)` gives `S=0` through distance three and `S=ln4` for every diameter-four diamond. In the diameter-four case, the middle waist contains exactly four vertices, so

`S = ln |waist| = ln 4`.

This is finite generalized-quadrangle combinatorics, not a spacetime or holographic entropy law.

## Artifacts

- `data/w33_pass4161_broader_rep_anomaly_optimization.json`
- `data/w33_pass4162_relational_hardware_graph.json`
- `data/w33_pass4163_quantized_noisy_t7_decoder.json`
- `data/w33_pass4164_storage_primitive_comparison.json`
- `data/w33_pass4165_global_mixed_landscape_push.json`
- `data/PART_4161_4168_BROADER_ANOMALY_HARDWARE_NOISY_STORAGE_LANDSCAPE_BONKERS.json`
- `analysis/w33_pass4161_4168_broader_anomaly_hardware_noisy_storage_landscape_bonkers.py`
- `tests/test_w33_pass4161_4168_broader_anomaly_hardware_noisy_storage_landscape_bonkers.py`

Remote CI, manuscript PDF compilation, fabrication, hardware calibration, and a globally exhaustive nonlinear proof remain external evidence gates.
