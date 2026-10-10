# W33 Theory — Round 31: 17-fold girth-10 cover, qutrit detector overhead, Spin16 branching firewall, observer causal lift and C8 two-boson loss

Date: 9 October 2026 | Repo: wilcompute/W33-Theory

## Research integrity and prior art

All five independent Round30 next steps were investigated in this pass. Before tinkering we read the new parallel Pass11834–11838 writeup and reviewed the Round30 implementation. The parallel packet ALREADY constructs the 9D Weil SU9 representation, Rac5 / Di4 singletons, exact finite Poincaré shells, bulk/boundary modes, one-dimensional E8 centralizer under SL2(F9), and Lean Clifford quadric. Those results are not rediscoveries here and remain a finite-field kinematic skeleton, NOT physical 3+1D spacetime or measured matter.

Earlier Round30 established the exact 83-fold connected cyclic voltage graph cover, girth10 and HGP [[220434721,44102881,10]]_3, plus an exhaustive one-fault verified-cat circuit conditional on ideal readouts. This pass improves the cover degree to **17**, derives detector readout/repetition cost, excludes a further class of Spin16 embeddings, constructs an explicitly observer-filtered Z^3 causal extension and quantifies two-photon loss in the proposed 8-site experiment. We preserve preexisting dirty and untracked research.

## I. Qutrit verified-cat readout and repeated detector budget: a quantitative limitation

The Round30 GHZ/CZ circuit needs 80 Wilson w=8 checks and 79 Gauss w=4 checks, with 797 verifier parity readouts and 159 stabilizer outcomes per extraction round; 956 data couplings. Previously, 275408 after-gate Pauli-fault cases were enumerated, but verifier readout and final measurement faults were explicitly **ideal**.

Model separately an independent symmetric ternary **classical report-flip channel** with probability p per verifier/outcome. For a verifier whose true report is zero, probability that every report in a global batch is correct is (1-p)^797; hence mean repeat batches 1/(1-p)^797. At p=0.001 the average is **2.22** batches; at p=0.005 **54.3**, at p=0.01 **3011.3**. By contrast, if each check can be independently prepared/retried, the expected total cat preparations for 159 accepted checks is 80/(1-p)^7 + 79/(1-p)^3, approximately **163.1** at p=.005, instead of 159 times 54.3. Independent retries are a scheduling and fault-model assumption, NOT demonstrated hardware concurrency.

For an unchanged ternary syndrome measured three times with independent symmetric report errors, strict majority wrong probability is exactly **(3/2)p²−(1/2)p³**; 'all three different' erasure probability is (3/2)p²(1-p). Probability any wrong among 159 independently repeated checks follows directly. But a true time-varying syndrome [0,0,1] gives outdated majority0 even with PERFECT readout, so majority cannot replace an evolving space-time detector-history decoder.

This is NOT a complete noisy verifier circuit, repeated FT threshold or logical QEC decoder. It makes the next physical gate explicit.

Producer: `analysis/w33_20261009_toe31_cat_detector_budget.py`; machine certificate `data/w33_20261009_toe31_cat_detector_budget.json`.

## II. Concrete W33 girth-ten cover reduced from degree83 to degree17; 2-cover impossible

Use the actual W33 Levi 160-edge, 80-vertex graph, its 1620 oriented signed 8-cycle matrix, and the voltage-cover construction of Round30. New heuristic varies all 160 edge voltages modulo candidate prime p. It maintains signed eight-cycle holonomies and updates a variable on a violated cycle to reduce the global violation count. Frozen RNG seed 31029. In this *specific limited search* p=3,5,7,11 stalled with 403,174,94,27 violated eight cycles respectively; these are **NOT mathematical nonexistence results**. At p=17 it solved all 1620 constraints after only **146** updates (first restart).

Independently reconstruct the graph on V=80×17=**1360** vertices and E=160×17=**2720** edges, verify 4-regularity, all-vertex BFS connectivity, no zero signed holonomy for ANY of the 1620 original eight-cycles, and an explicit simple **ten-cycle witness**, hence lift girth exactly 10. Applying the standard full-row-rank ternary HGP to graph incidence check (1359)x(2720) gives the quantum code

`[[9245281,1852321,10]]_3`,

with encoding rate ≈20.035% and check weight at most6. It requires **23.84x fewer physical qutrits** than the Round30 83-fold example, while still obviously impractical at more than nine million qutrits. We explicitly construct the 1360-vertex graph, **not** the enormous HGP parity check matrices; exact parameters use the standard HGP distance theorem and explicit graph-girth witness.

Stronger exact obstruction: over F2 the linear system C v = 1 (all 1620 eight-cycle holonomies odd, equivalent to 2-cover girth>=10) is inconsistent. A GF2 elimination certificate finds rank81 and nontrivial dependency: an **odd** number of eight-cycle rows sum to zero mod2. Therefore a cyclic **two-fold** W33 cover cannot eliminate all eight-cycles. There may be smaller degree-three and other nonlinear voltage covers; this pass proves neither degree17 minimal nor p=11 impossible.

Producer: `analysis/w33_20261009_toe31_compact_voltage_cover.py`; second independent certificate producer `analysis/w33_20261009_toe31_compact_cover_certificate.py`; full 160-integer voltage witness in `data/w33_20261009_toe31_compact_voltage_cover.json`; graph and 10-cycle certificate in `data/w33_20261009_toe31_compact_cover_certificate.json`.

Contextual literature: the exact graph-incidence HGP distance formula is standard (https://doi.org/10.1103/PhysRevX.11.011023); 2026 high-girth hypergraph-product voltage work (https://arxiv.org/abs/2604.27817) warns that the *Tanner graph* may have orthogonality-forced cycles even when **our base incidence graph** girth increases. Do **NOT** conflate the two graph girths; claims here concern minimum code distance via incidence kernel, not Tanner graph girth or circuit threshold.

## III. Spin16 exceptional E8 embedding: a broad conditional 81-representation obstruction

Following Round30 exclusion of all F4×G2 embeddings, screen a substantive surviving E8 subgroup, Spin16 / HSpin16. The standard E8 Lie algebra branches as 248 = 120_so16 + 128_halfspin.

**Theorem (finite PERFECT G):** Suppose the G action admitted by this subgroup has an associated orthogonal 16D complex vector module splitting into two nondegenerate invariant even-dimensional oriented factors Va ⊕ Vb, where a,b≥4 and a+b=16. Since G is perfect, determinant characters on each invariant factor are trivial, so the G action does NOT interchange factor chirality. Under Spin(a)×Spin(b),

`120 = Λ²Va ⊕ Λ²Vb ⊕ (Va⊗Vb)`,

in dimensions `a(a−1)/2, b(b−1)/2, a b`, while the chosen half-spin 128 splits into two **64-dimensional** tensor-spin modules. For a=4,6,8,10,12, no invariant block exceeds **66 dimensions**. By semisimplicity, an irreducible 81D Steinberg constituent cannot occur. This is a conditional subgroup-class theorem, not an overall E8 no-go.

A concrete orthogonal candidate from the ATLAS small PSp4(3) irreps is 16 = 5a ⊕ 5b=5a* ⊕ 6_real. It preserves nondegenerate 10+6 and therefore also fails to realize Steinberg81 *if* its SO16 homomorphism lifts to the relevant E8 HSpin16 subgroup. Existence of the central lift was not proved. Irreducible16, odd/odd decompositions, degenerate splittings, and 2+14 remain open; no full actual E8 character restriction or bracket intertwiner is claimed.

Producer: `analysis/w33_20261009_toe31_E8_spin16_even_split_obstruction.py`. Input E8=120+128 appears in https://books.physics.oregonstate.edu/GELG/e8.html ; ATLAS PSp4(3) characters https://brauer.maths.qmul.ac.uk/Atlas/v3/clas/U42/.

## IV. Finite AdS 'light cone' via observer-filtered three-space unwrapping

Parallel finite tangent geometry is the elliptic-type F3 quadratic space of dimension four, expressible after change of basis as `Q(x,y,z,t)=x²+y²+z²−t² mod3`. Its 20 nonzero null vectors partition **8 zero temporal residue, six residue+1, six residue−1**. Under chosen observer/time orientation, the six forward rays are exactly (±e1,±e2,±e3,Δt=+1), lifting spatial F3³ to Z³ and t to Z. The remaining 14 original null directions must be **discarded** to impose that time orientation, breaking finite Lorentz symmetry.

This yields a conventional anisotropic cubic *externally lifted* spatial causal cone: the L1 radius-r ball has exactly `(4r³+6r²+8r+3)/3` spatial points, e.g. 1,7,25,...,1561 at r=10. Unlike Round30's Z×F3^4 81-spatial-position saturation after two ticks, this spatial cover keeps growing ∼4r³/3.

This is a useful explicit discrete escape from the finite-causality no-go, but it **assumes** an infinite Z time, an infinite Z³ lattice, a choice of observer and a radical truncation of original null directions. It is NOT dynamical emergence of physical 3+1D Minkowski, Lorentz invariance, Einstein equations or c.

Producer: `analysis/w33_20261009_toe31_observer_lightcone_lift.py`.

## V. Two-boson hardware loss: a quantitative missing feasibility condition

With the proposed C8 attractive Bose–Hubbard parameters `t/h=5MHz, U/t=32`, one must supply `U/h=160MHz`, eight calibrated links, eight independently known detunings and eight nonlinearities. The relevant slow bound-pair gap is ~0.1817MHz, so accurate slow-band measurements sit on a 160MHz binding carrier.

Assume (ONLY AS A MODEL) two independent photons with per-photon Markovian energy lifetime T1. Then probability of **both** surviving evolution t is `exp(-2t/T1)`. For a 60μs Ramsey sweep, pair no-loss probability at the endpoint is:

| Hypothetical per-photon T1 | Pair survives at t=60μs |
| ---: | ---: |
|25μs|0.82%|
|50μs|9.07%|
|100μs|30.12%|
|200μs|54.88%|
|500μs|78.66%|

To retain at least 50% *pair* survival at 60μs requires **T1 ≥ 120/ln2 ≈173.1μs**. This requirement is separate from, and often stricter than, the phase-coherence T2 criterion; all values here are assumed, NOT measured. The source also emits 15 conditional T1,T2 signal-visibility and shot-overhead cases.

Actual C8 control implementation still needs an existing lab platform with measured detunings, nonlinearities, two-photon loss, pair-selective drive, phase-sensitive readout, contrast, reset and full channel calibration. No physical device was accessed; a hardware-feasibility specification is the completed task, not a demonstration.

Producer: `analysis/w33_20261009_toe31_C8_two_boson_loss_hardware_gate.py`.

## Overall research status

The strongest new mathematical asset is the **verified 17-fold girth10 W33 cover certificate** (9.25M rather than 220M physical qutrits). The strongest new E8 statement is the **conditional Spin16 even/orthogonal splitting no-go**, excluding a natural orthogonal 5+5*+6 candidate but leaving important embedding classes unresolved. The strongest physical bottlenecks are the cat verifier readout and T1-limited pair survival; both make clear why mathematical code distance or an attractive H spectrum do not prove deployable hardware.

No exact Standard Model parameter derivation, complete fundamental TOE, physically emergent Lorentzian Einstein spacetime, certified noisy FT decoder threshold, or laboratory hardware result is claimed.

Reproducibility: six scripts (plus standalone second cover checker), six machine-readable JSON certificates, an independent focused pytest suite, this report. Parallel research files and local dirty work are excluded from the commit.
