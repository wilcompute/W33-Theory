# Pass 2015 — physics and computer-engineering architectures

This note separates three levels deliberately:

1. **exact structural inputs** from the finite geometry and representation theory;
2. **engineering architectures** suggested by those inputs;
3. **physics hypotheses** that remain untested.

No withdrawn particle interpretation is restored.

## Exact structural inputs

### Spread transport layer

The 36 spreads carry a valency-15 rank-three relation with

`A^2 = 9I + 6J`.

Consequently every distinct pair of spread channels has exactly six two-hop
paths through the four-line relation, independent of whether the pair itself is
adjacent.  On mean-zero signals,

`R=(A-(5/12)J)/3`

is an exact involution.

### Two local pair geometries

- A four-line spread pair has stabilizer `S4×D8` and decoration fibers of sizes
  `1,2,6`: half-turn, inverse quarter-turn pair, and six cyclic orders.
- A one-line spread pair has an 18-node, degree-4 rook-double graph with full
  automorphism group 144.

### Exact-cover schedule compression

A literal `D8` subgroup schedule stores twelve frame orbits rather than sixty
individual frames.  Expanding the orbit blocks covers all 240 edges exactly
once.

### Phase-sector channels

The Eisenstein 90 has no equivariant linear map into `15,24,30,81`.  At second
order, however, `Sym²(90)` contains all four rational blocks.  The antisymmetric
channel `Λ²(90)` contains no 15, giving an exact channel-selection rule.

---

## Computer-engineering proposal 1 — rank-three spread mixer

Implement 36 logical lanes with the valency-15 adjacency matrix as a fixed
interconnect.

A two-stage route has an exact deterministic path count:

- nine length-two returns to the source;
- six length-two routes to every other lane.

This makes the network attractive as a test architecture for uniform diffusion,
redundant routing, or deterministic scrambling without a stored routing table.
The centered transform `R` is involutory, so the same datapath can encode and
decode mean-zero spread signals.

**Implementation sketch:** fifteen-neighbour XOR/add network, global mean removal,
and a divide-by-three/scaled fixed-point stage.  The exact arithmetic should be
implemented over an explicitly chosen ring; the real-matrix identity alone does
not specify a digital word format.

## Computer-engineering proposal 2 — rook-double crossbar

Represent each bank of nine lines as a `3×3` array.  A lane connects to the four
lanes in the opposite bank sharing its row or column.

The result is the exact one-line-pair local graph:

- two banks of nine ports;
- four cross-bank links per port;
- 36 physical links;
- local symmetry group order 144.

This is a compact topology for a dual-bank switch, memory permutation network,
or photonic mode coupler.  Its mathematical identification is exact; signal
integrity, layout, and fabrication claims require a separate device model.

## Computer-engineering proposal 3 — `D8` orbit scheduler

Store the twelve selected subgroup-orbit identifiers and two generators of the
`D8` action.  Expand the orbit descriptors into a 60-frame schedule on demand.

The exact block sizes are

`2,2,4,4,4,4,4,4,8,8,8,8`.

The resulting schedule covers each of 240 edge channels exactly once.  Relative
to a flat 60-frame table, the control representation is group-compressed and
comes with a native self-check: regenerate the orbit, form the 240-bit union,
and require population count 240 with no overlap.

This can be prototyped in software first, then mapped to an FPGA using wide mask
intersection, population count, and orbit-expansion microcode.

## Computer-engineering proposal 4 — quadratic phase readout

A linear buffer or linear crossbar cannot export the 90-sector phase into the
rational planes in an equivariant design.  A square-law device, multiplier,
parametric mixer, or other bilinear element can access `Sym²(90)` channels.

The exact selection rule is:

- symmetric mixer: gauge-15 target allowed, multiplicity three;
- antisymmetric mixer: gauge-15 target absent.

That is a concrete verification target.  A prototype should compare otherwise
matched symmetric and antisymmetric mixers and check whether the 15-projected
response vanishes in the antisymmetric configuration.  Representation theory
allows a channel; it does not determine its physical coupling strength.

## Computer-engineering proposal 5 — stabilizer-aware G-set ABI

Every geometric object exchanged between software or hardware modules should
carry more than a count.  The interface record should include:

- object degree;
- stabilizer order and structure;
- permutation-character or conjugacy fingerprint;
- transporter/canonical-label certificate;
- provenance of the group action.

This prevents errors such as treating the two degree-40 actions, the multiple
240 actions, or the three nonconjugate degree-540 stabilizers as interchangeable.
It is the group-theoretic analogue of a strong type system.

---

## Physics hypotheses worth testing, not claiming

### Linearly dark, quadratically bright sector

The 90 is a mathematically precise analogue of a sector with forbidden
first-order mixing but allowed higher-order communication.  This resembles the
logic of a hidden sector, but no Standard Model field or measured coupling is
identified.

### Discrete propagation kernel

The identity `A²=9I+6J` means two spread-transport steps erase pair-specific
differences at the level of path counts.  It may be useful as a toy model of
finite isotropization, scrambling, or propagation.  A physical Hamiltonian and
unitary normalization remain to be constructed.

### Local clock and routing labels

The `1/2/6` fibers over four-line spread pairs provide canonical finite labels:
linewise half-turn, orientation of a quarter-turn, and cyclic ordering.  They
could organize phase, direction, and schedule metadata in a device.  They are
not established particle quantum numbers.

## Withdrawals retained

The internal `C6` is not promoted as:

- electric charge;
- Dirac or homological flux;
- QCD colour;
- a generation index;
- a neutrino label.

Those interpretations remain withdrawn.  The standing results concern exact
representation channels, finite geometry, and proposed engineering uses.
