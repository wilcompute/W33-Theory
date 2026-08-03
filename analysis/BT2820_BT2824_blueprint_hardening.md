# Passes 2820--2824: Blueprint Hardening and Execution-State Closure

## Status

`COMPLETE_EXACT_COMPILE_PENDING` until the repository workflow integrates the public documents, compiles all three canonical manuscripts, and freezes the audit certificate.

## Pass 2820 -- Public ISA versus internal micro-ISA

The public Holonet interface remains the eight-opcode, three-bit instruction set.  The exact internal frame engine needs only four operations,

\[
F_p,\qquad \mathrm{CX}_{p\to f},\qquad \mathrm{CX}_{f\to p},\qquad Z_p,
\]

encoded by two bits.  These four operations generate the complete linear group of order

\[
51{,}840
\]

and, with translations, the affine group of order

\[
81\cdot 51{,}840=4{,}199{,}040.
\]

The measured `72 LC / 60.80 MHz` result belongs to the loadable public full-frame unit.  It is not silently reassigned to the four-operation minimal engine; that engine requires its own synthesis and place-and-route evidence.

## Pass 2821 -- Exact deep-grade M36 distillation

The exhaustive search class is now explicit: all 5,355 binary `[[4,2]]` stabilizer projectors, all four syndromes, and all 11,520 logical Clifford decoders.  Shallow and both middle M36 grades have zero improving branches.  The deep eight-ray grade has exactly 48.

One explicit branch is

- input ray 5,
- stabilizers `IYZY` and `YZXY`,
- syndrome `(-1,+1)`,
- Hadamard on the second logical qutrit/qubit coordinate of the enumerated decoder chart,
- output ray 7.

Its exact curve is

\[
P_{\rm succ}=\frac{p^2-2p+2}{4},
\]

\[
F_{\rm out}=\frac{5p^2-12p+8}{4(p^2-2p+2)},
\]

\[
F_{\rm out}-F_{\rm in}
=\frac{p(p-1)(3p-2)}{4(p^2-2p+2)}.
\]

Thus it improves fidelity for

\[
0<p<\frac23,
\]

which contains the deep M36 magic interval.  This supersedes the previous arbitrary-decoder no-go.  It is a state-fidelity distillation theorem, not a fault-tolerant injection threshold, asymptotic-yield theorem, or laboratory demonstration.

## Pass 2822 -- PG(3,2) support codec and the new execution obstruction

Pass 2808 proves that binary support masks form an exact PG(3,2) geometric shell with tetrahedral capacity profile

\[
(4,6,4,1)\odot(1,2,4,8)=(4,12,16,8).
\]

The new computation asks whether that 16-class support shell can also replace the full 81-state ternary frame during deterministic instruction execution.  It cannot.

The two states

\[
(0,1,0,0),\qquad (0,2,0,0)
\]

have the same binary support mask `0100`, but after `Z_p` their support masks are respectively `0100` and `0000`.  Therefore support is not a congruence for the selected micro-ISA.

Deterministic partition refinement under the four selected operations gives

\[
\boxed{16\longrightarrow40\longrightarrow78\longrightarrow81}.
\]

The terminal partition is discrete.  Full ternary phase is eventually forced.

### Support-for-readout / phase-for-execution theorem

The PG(3,2) support shell is an exact geometric, equitable, and capacity-preserving codec for readout, routing, and visualization.  It is not a lossless deterministic execution quotient of the four-operation affine frame machine.  The correct architectural separation is:

\[
\boxed{\text{support for readout, phase for execution}.}
\]

## Pass 2823 -- Scope and evidence hardening

- The finite `mu_12` sensor lift has exponent 3 for odd depth and 9 for even depth.  Arbitrary `U(1)` representatives require exponent `3^n`.
- Transpose is an anti-symplectic involution that conjugates the two controlled-add directions.  Its projective class is inner at `q=5` and outer diagonal at `q=7`.
- The live mixer is `rtl/w33_pass2773_spread_mixer36_synth.sv`.  The historical dead source `rtl/w33_spread_mixer36.sv` was removed and must not remain in the evidence ledger.
- Exact finite calculations are reproduced by the verifier.  Remote Icarus/Yosys/nextpnr evidence remains separately observable and must not be inferred from mathematical checks.

## Pass 2824 -- Executable migration and drift closure

The release contains:

- an exact verifier and frozen JSON certificate,
- an idempotent migration tool for `w33_paper.tex`, `photonic_holonet.tex`, `holonet_machine_blueprint.tex`, `docs/index.html`, and the pass registry,
- regression tests for the support refinement and M36 operating curve,
- a manuscript-ready shared TeX insert,
- a GitHub Actions workflow that integrates, audits, compiles, publishes PDFs, and commits generated canonical artifacts back to `master`.

## Literature boundary

The published tomotope has the numerical profile `(4,12,16,8)` with four tetrahedral and four hemioctahedral facets.  The PG(3,2) support-capacity identity is a separate repository theorem; matching counts are not asserted to be an incidence isomorphism.  Likewise, nearby magic-state protocols may change the allowed gate set or output family.  Pass 2804 claims only the explicitly enumerated stabilizer-projector/logical-Clifford search class above.
