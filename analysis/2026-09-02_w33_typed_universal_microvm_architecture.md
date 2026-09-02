# 2026-09-02 — Typed Universal MicroVM Architecture

## Result

This pass turns the existing W33 packet VM, recursive HoloBox runtime, Holotrade
typed-microVM theorem, and the September 2 outer-parity/carrier corrections into
one conservative virtual-machine contract.

The central design rule is:

> **Geometry routes computation; it does not silently redefine computation.**

The guest semantics is an ordinary abstract machine. Every state transition is
then wrapped in a W(3,3) route and a replayable certificate. This separates
semantic correctness from transport geometry while still making the geometry
architecturally operative.

The executable witness is:

```text
analysis/w33_typed_universal_microvm.py
tests/test_w33_typed_universal_microvm.py
data/w33_typed_universal_microvm.json
```

Local verification: 5/5 regression tests pass.

## 1. The ABI must distinguish two different 51840-element worlds

An older repository artifact described the Clifford opcode group as

```text
Sp(4,3) = W(E6)
```

because both have order 51840. The current manuscript correctly repairs that
conflation.

The VM therefore has separate namespaces:

| namespace | finite object | order | VM role |
|---|---|---:|---|
| Clifford lift | `Sp(4,3)` | 51840 | lifted symplectic/Clifford frame transport |
| projective Weyl control | `PGSp(4,3) ~= W(E6)` | 51840 | projective similitude / outer-control transport |

They have the same order but are different extensions of `PSp(4,3)` and are
not interchangeable opcode tables.

This is not cosmetic typing. The September 2 modular-router theorem now shows
that outer extension signs can invert after a chosen integral reduction modulo
3. A VM that erases the extension type can therefore erase mathematically real
state.

## 2. The 216 carrier bit is a machine type, not a runtime bit

Holotrade proved that the circuit-216 carrier and paired-hemisystem-216 carrier
are inequivalent under the full substrate automorphism group. Consequently:

```text
circuit216            -> Steinberg-81 addressable
paired-hemisystem216  -> Steinberg-64 addressable
```

and there is no legal in-machine “gauge conversion” instruction between them.

The reference VM encodes this as an immutable capability:

```text
Capability(
    carrier = CIRCUIT_ST81 | PAIR_ST64,
    logical_dimension = 81 | 64,
    permissions = ...
)
```

Wrong carrier/module pairings are rejected at construction. Runtime retyping
raises an error.

This is directly analogous in systems spirit—not mathematical origin—to a
capability architecture: authority and type travel with the pointer/state
instead of being inferred from an ambient address.

## 3. Universal core: a two-counter machine, not a numerology claim

The software-universality layer uses the classical two-counter machine. Its
macro ISA is only:

```text
INC(r, next)
DECJZ(r, nonzero_target, zero_target)
HALT
```

with two unbounded natural-number counters.

Two-counter machines are a standard universal model of computation. Therefore
an exact interpreter for arbitrary finite programs in this ISA is enough for
Turing-complete *VM semantics*.

That theorem is intentionally narrower than several older “universal computer”
claims in the repository:

- it does not infer universality from an integer coincidence;
- it does not require `Sp(4,3) ~= W(E6)`;
- it does not claim a finite 40-node device has physically infinite memory;
- it does not claim that a Clifford-only photonic kernel is quantum universal.

The quantum-universality boundary remains the existing one: a separately
validated non-Clifford physical port is required.

## 4. One compute step

A guest step is:

```text
guest state
   |
   | 1. decode/validate typed macro instruction
   v
semantic transition (INC / DECJZ / HALT)
   |
   | 2. assign deterministic W33 execution portal
   v
W33 route (0, 1, or 2 hops)
   |
   | 3. record line buses
   v
post-state
   |
   | 4. hash certificate
   v
trace_root'
```

The route never changes the guest result. It is the certified transport layer.

For each step the certificate records:

```text
pre-state digest
post-state digest
program counter before/after
typed instruction
immutable carrier
logical module dimension
symmetry namespace
W33 point route
W33 line buses
new trace root
```

This makes the execution trace replayable and gives a natural hardware/formal
verification target.

## 5. Why W33 is useful as virtual hardware

The verifier reconstructs W(3,3) directly and checks:

```text
points   = 40
lines    = 40
degree   = 12
lambda   = 2
mu       = 4
diameter = 2
```

Hence every macro event can be assigned to a portal and transported to the next
portal in at most two W33 hops.

For a recursive address of depth `d`, the existing fractal-microVM runtime
already gives the natural extension: change one coordinate at a time, each with
at most two W33 hops. That turns one finite router into a scalable virtual
address fabric.

The important systems separation is:

```text
finite W33 cell     = router / typed local machine
recursive address  = scaling mechanism
content store       = durable state
counter/tape model  = abstract unbounded semantics
```

No single finite cell is asked to be infinite.

## 6. Content-addressed state is the right memory model

The existing W33 fractal runtime already uses SHA-256 content addressing and an
OCI-shaped graph. That is exactly the right direction.

A VM snapshot should be a Merkle root over:

```text
program image
immutable machine type
registers / counters
program counter
recursive child roots
inbox/outbox roots
trace root
```

This buys deterministic replay, cheap copy-on-write forks, deduplication of
identical submachines, proof that a loaded state matches its descriptor, and
recursive composition: a network of microVMs can itself be one loadable
microVM state.

The OCI image specification independently uses content-addressable identities
and Merkle-DAG descriptors, so the existing HoloBox direction is aligned with a
mature systems pattern rather than being an ad hoc serialization trick.

## 7. Validator architecture

The next compiler should use a WebAssembly-like phase split:

```text
decode -> validate -> instantiate -> execute
```

but with W33-specific validation rules.

At minimum the validator must prove before execution:

```text
program counters are in range
counter register indices are valid
carrier/module dimension is consistent
carrier never changes
Clifford-lift and projective-Weyl opcodes never alias
capability permissions are monotone
every routed edge is a real W33 line edge
every instruction has a deterministic trace schema
```

WebAssembly 3.0 is a useful external precedent because its validation algorithm
is a one-pass typed check over a flat opcode stream, with distinct value,
control, and initialization stacks. The W33 VM does not need to copy Wasm, but
it should copy the discipline: malformed bytecode must be rejected before it
can become a packet.

## 8. Capability pointers instead of naked addresses

A future W33 memory reference should be a typed capability:

```text
W33Capability {
    machine_type,
    module_dimension,
    recursive_address,
    rights,
    object_digest,
    optional_outer_extension_tag
}
```

A raw integer address is insufficient because the current mathematics says
some distinctions are not reconstructible safely from a number alone.

This mirrors a key CHERI systems lesson: put provenance, bounds/authority, and
permissions into an architectural capability rather than trusting software to
reconstruct them later.

## 9. Executed witness

The regression program transfers all of counter 1 into counter 0:

```text
input  = (7, 11)
output = (18, 0)
```

It executes in:

```text
24 certified macro steps
24 transition certificates
max W33 route = 2 hops
```

A second run reproduces the exact final trace root, and the same abstract
classical result is obtained on both machine types while their ABI identities
remain distinct.

## 10. What “computation” is in this architecture

A useful conceptual reframing falls out of the implementation:

> **Computation is a typed state transition; routing is a proof-carrying
> realization of that transition in a finite geometry.**

That separates three things that the older prose often intentionally merged:

```text
meaning       = guest transition semantics
placement     = W33 portal / chamber
realization   = route, bus, physical gate sequence
```

They may coincide in a future photonic implementation, but the VM should not
assume that coincidence. Keeping them separate is precisely what lets us test
whether the hardware really realizes the claimed computation.

## 11. External research cross-checks

- WebAssembly Core 3.0: abstract stack-machine semantics, structured control,
  validation before execution, and explicit runtime store.
- OCI Image Specification: content-addressable image identity and Merkle-DAG
  descriptors.
- CHERI: architectural capabilities as unforgeable authority/provenance-bearing
  pointers.
- Minsky counter machines: two counters suffice for universal computation; the
  later literature also studies reversible universal two-counter machines.

These are engineering precedents, not evidence for the W33 finite-geometric
claims.

## 12. Honest theorem boundary

What is proved by the executable artifact:

```text
arbitrary finite two-counter programs have exact deterministic semantics;
every macro step receives a valid deterministic W33 route of <= 2 hops;
carrier type is immutable;
81/64 module dimensions are type-checked;
the two order-51840 domains are not aliased;
execution is content-addressed and deterministically replayable.
```

What is not proved:

```text
one finite W33 cell has unbounded physical storage;
a host Python integer is itself a photonic counter;
the typed VM is a fabricated processor;
the Clifford kernel alone is quantum universal;
the non-Clifford physical port meets thresholds/loss/error budgets;
the software VM establishes any proposed particle/cosmology interpretation.
```

That separation is the main architectural upgrade.
