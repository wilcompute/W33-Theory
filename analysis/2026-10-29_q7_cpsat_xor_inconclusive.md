# W(3,7) CSS distance: reproducible native-XOR CP-SAT stress test (inconclusive)

**October 29, 2026.** The existing exact certificate gives \(10\le d\le14\) for the binary adjacency CSS code \([[400,48,d]]_2\). The upper bound is exhibited by the symmetric difference of intersecting isotropic eight-point lines; the lower bound excludes nonzero kernel words of weights \(2,4,6,8\). These facts are *prior work*, not new theorem claims here.

**New independent test:** \`analysis/w33_20261029_q7_cpsat_native_xor_probe.py\` reconstructs all 400 projective points of \(\mathbb F_7^4\) and degree-56 symplectic adjacency, creates 400 Boolean support variables, imposes **native CP-SAT XOR parity constraints** for all 400 adjacency rows, and restricts Hamming weight to 10–12. By point transitivity and the two orbits on ordered distinct pairs (collinear or noncollinear), any such counterexample may be moved to include point 0 plus one representative point in one of two orbits. Both cases must be proved infeasible to certify \(d=14\).

With Google OR-Tools 9.15, 8 search workers and 90 seconds per case on the authorized Windows computer:
- Adjacent pair \((0,8)\): solver returned **UNKNOWN** after approximately 90.21 s, with 1,097,539 branches and 144,608 conflicts.
- Nonadjacent pair \((0,1)\): **UNKNOWN** after approximately 90.04 s, with 1,314,829 branches and 156,955 conflicts.

Neither a weight-10/12 counterexample nor an infeasibility proof was found. **No stronger distance claim is justified**; \(10\le d\le14\) remains the certified interval. This transcript is useful as a performance baseline for stronger SAT encodings, stabilizer-chain symmetry breaks, parity-check redundancy or a purely geometric proof.

Reproduction: \`python analysis/w33_20261029_q7_cpsat_native_xor_probe.py\` after installing \`ortools\`. The verifier reports \`OPEN_AFTER_CP_SAT\` unless both pair orbit cases prove \`INFEASIBLE\`.
