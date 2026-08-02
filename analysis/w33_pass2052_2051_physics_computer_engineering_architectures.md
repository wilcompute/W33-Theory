# Passes 2051–2052 — bounded physics and computer-engineering architectures

The exact input is representation theory and finite geometry.  The output below
is divided into supported selection rules, engineering designs, and hypotheses.
No particle label, coupling constant, fabricated device or experimental result is
claimed.

## Exact selection rules

- The signed-edge 90 has no equivariant linear export to 15, 24, 30 or 81.
- Explicit quadratic maps nevertheless reach all four rational targets.
- The natural antisymmetric commutator channels reach 30 and 81 but vanish on
  15 and 24.
- The vertex-energy channels reach 15 and 24 symmetrically.
- J-twisted maps to 30 and 81 are chirality-odd; the untwisted maps are
  chirality-even.
- Simultaneous mu6 rotation leaves the 15 and J-twisted channels invariant.
  The 24 and untwisted commutator channels form period-three bilinear response
  spaces.

These statements support a two-stage interpretation: the phase sector is dark to
linear probes but bright to selected quadratic probes.  They do not establish a
physical hidden sector or a nonzero microscopic interaction.

## Architecture 1 — full-group schedule canonicalizer

Store each low-order scheduling subgroup with a full-group conjugacy fingerprint,
not merely its abstract structure.  The 33 local positive classes collapse to 14
full-group types, so a compiler can canonicalize subgroup descriptors before
exact-cover search.  The 12 first-witness schedule orbits form a regression
suite, not a complete schedule library.

## Architecture 2 — D8 orbit microsequencer

A fixed D8 engine stores twelve seed descriptors and expands orbit blocks of
sizes 2,2,4,4,4,4,4,4,8,8,8,8.  A 240-bit overlap accumulator rejects repeated
edges while a population counter confirms complete coverage.  With fixed
subgroup generators, the frame-ID payload falls from 600 bits to 120 bits before
metadata and protection bits.

## Architecture 3 — rank-three involutory network

Implement the 36-spread graph as a degree-15 interconnect.  The identity
A²=9I+6J means that on zero-sum data the same two-hop fabric implements 9I.
After division by three, the mixer is its own inverse.  This supports reversible
encode/decode scheduling, deterministic two-hop path multiplicity six, and a
simple built-in self-test: two applications must return the original mean-zero
word.

## Architecture 4 — chirality lock-in quadratic readout

Run matched quadratic channels before and after the outer chirality operation.
Even maps add; J-twisted odd maps change sign.  Their sum and difference isolate
chirality-even and chirality-odd response without assigning a particle meaning
to either.  A symmetric multiplier stage is required for the 15/24 channels; a
commutator or nonreciprocal differencing stage is required for the natural 30/81
antisymmetric channels.

## Architecture 5 — six-phase cycling and period-three demodulation

Cycle the internal mu6 phase through six settings.  Phase-neutral channels remain
constant.  The other canonical bilinear maps repeat after three settings because
simultaneous input inversion cancels in a quadratic observable.  A three-bin
Fourier or lock-in readout therefore separates invariant and rotating quadratic
channels while using a six-state calibration clock.

## Architecture 6 — rook-double local router

Use two 3×3 port banks.  Connect cross-bank cells sharing a row or column.  The
result is the exact 18-node, degree-four local geometry of a one-line spread
pair.  Its order-144 automorphism group provides a natural interface-security
test: routing-table transformations must remain inside the certified local group.

## Physics hypotheses worth falsifying

1. A linearly dark but quadratically bright response may provide a finite-model
   analogue of higher-dimension hidden-sector mediation.
2. Chirality-odd J-twisted channels may model an externally phase-referenced
   pseudoscalar response, whereas untwisted channels behave as chirality-even
   intensities.
3. The rank-three mixer may model a discrete two-step isotropization kernel,
   because every distinct spread lane receives exactly six length-two paths.

These are hypotheses only.  Electric charge, homological or Dirac flux, QCD
colour, generation and neutrino assignments remain withdrawn.
