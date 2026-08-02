# Pass 1975 — bounded physics and computer-engineering implications

This document deliberately separates exact structure, engineering proposals, and
speculative physics.  The withdrawn charge and flux readings remain withdrawn.

## A. Exact structural inputs

1. The signed 240-edge carrier decomposes as
   `15 + 24 | 81 | 30 + 90`, with exact/harmonic/coexact dimensions
   `39 | 81 | 120`.
2. The 90 is the only non-rational block.  Its integral phase units form `C6`;
   the outer involution inverts the phase, so the finite phase normalizer is
   `D12`.
3. Multiplicity-freeness forces every `PSp(4,3)`-equivariant linear map from the
   90 to the 15, 24, 30, or 81 to vanish.
4. The frame-colouring search has 540 frame variables, 240 rainbow `K9`
   constraints, 36 spread signatures, and a 40-transvection geometric action.
5. Embedding geometric lex constraints into spread-first `FIXED_SEARCH` worsens
   the measured tree even though it strongly reduces one known group orbit.

## B. Computer-engineering proposals

### 1. Symmetry canonicaliser as a separate hardware front end

The failed combined solver suggests architectural separation rather than a
larger monolithic model.  A front end can:

- accumulate the `36 x 9` spread-count signature;
- apply the 40 fixed spread permutations;
- evaluate deterministic integer keys;
- emit the minimum representative and its group tag;
- feed only canonical cubes to the exact solver.

The datapath is counters, fixed-address permutations, integer multiply-adds, and
a reduction tree.  It is natural for an FPGA or ASIC and does not constrain the
solver's internal branching order.

### 2. Cube-and-conquer with geometric deduplication

Generate search cubes by the spread variables, canonicalise each cube under the
40 transvections, hash the canonical signature, and distribute only unseen cubes
to workers.  This uses geometry for distributed-work deduplication rather than
as late-propagating inequalities.  Correctness requires storing the group element
that maps each discarded cube to its representative.

### 3. Exact-cover accelerator

Each colour class is a 60-frame exact cover of 240 edges, with four edges per
frame.  A hardware kernel can represent candidate frames as 240-bit masks and
perform conflict tests with wide bitwise ANDs, population counts, and priority
selection on the least-covered edge.  Nine coupled cover engines can share the
240 edge-indexed `K9` incidence memory.  This is closer to the problem's native
combinatorics than forcing every structure through a generic MILP.

### 4. Three-plane system architecture

The Hodge split suggests a useful *engineering metaphor*:

- exact 39: source injection, calibration, and syndrome ingress;
- harmonic 81: persistent logical state;
- coexact 120: transport and circulation, including the phase-bearing 90.

A photonic or FPGA controller could enforce separate address spaces and explicit
bridges between these planes.  This is an architecture inspired by the exact
linear decomposition, not a claim that these blocks are Standard Model fields.

### 5. Isolated six-phase control domain

Because the internal `C6` is linearly confined to the 90, it is better viewed as
a protected control/calibration clock than as a conserved charge.  A photonic
implementation could use six calibrated phase states on a coexact routing layer,
with chirality reversal implementing phase inversion.  Interfaces to the other
blocks must be deliberately symmetry-breaking or nonlinear; accidental linear
cross-coupling is forbidden only in the ideal equivariant model.

## C. Physics implications that are supported

- Orientation is necessary for the non-rational phase sector: the phase occurs
  in the signed coexact module, not in an unsigned permutation module.
- The phase is internal and sector-selective.  It is reversed by the outer
  involution and cannot be exported linearly by a `PSp(4,3)`-equivariant map.
- The 81-dimensional harmonic block cannot carry a real complex structure
  because its dimension is odd.
- Exact, harmonic, and coexact sectors are mathematically distinct and should not
  be identified merely because they share the same 240-edge carrier.

## D. Physics hypotheses worth testing, not claiming

1. **Nonlinear phase mediation.**  Linear equivariant transfer from the 90 is
   impossible, but invariant bilinear or cubic maps may couple two phase-bearing
   states into a rational sector.  The next test is to compute trivial and target
   constituent multiplicities in `Sym^2(90)`, `wedge^2(90)`, and `90 tensor 81`.
2. **Controlled symmetry breaking.**  A physical device may deliberately break
   `PSp(4,3)` at an interface.  The minimal subgroup at which a map from the 90
   to another block appears is an experimentally meaningful design parameter.
3. **D12 phase-reversal protocol.**  The algebraic relation
   `c mu c = mu^{-1}` could implement a six-state phase code with a reversible
   handedness operation.  Robustness must be tested under loss, detuning, and
   phase noise before assigning physical significance.
4. **Hodge-separated error channels.**  Faults could be classified by projection
   into exact, harmonic, and coexact components.  This is testable in simulation
   and may produce better diagnostics even if no fundamental-physics reading
   survives.

## E. Hard boundaries

- `C6` is not derived electric charge.
- `C6` is not a homological or Dirac flux quantum.
- No QCD-colour, generation, or neutrino identification is supported.
- The hardware proposals do not establish `chi(H)=9` or the existence of a
  physical W33 device.
- A broken-symmetry device can couple sectors that the ideal equivariant model
  keeps separate; “confined” is a theorem about equivariant linear maps, not an
  absolute law of nature.
