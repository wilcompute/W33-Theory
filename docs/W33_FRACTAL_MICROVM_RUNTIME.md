# W33 Fractal MicroVM Runtime

This is the executable systems form of the recursive Holonet idea: a microVM
contains a 40-slot network of microVMs, and the whole network is stored and
loaded through the same state descriptor as one leaf microVM.

## What is new

The repo already had a packet interpreter, a controller-wrapped VM, the BT350
network-as-node concept and unproved `2n` diameter assertion, Passes 2642--2644's
same-port recursive hardware module, a `40^n` recursive packet count,
recursive routing-table compression, UOR-shaped canonical content IDs and
command certificates, and a paper design for
immutable CID containers, WASM/OCI components, policies, receipts, and a
Projection Engine. That integrated design remains on the Witting architecture
roadmap.
What was missing was an executable nested state and lifecycle layer. This
runtime adds:

- a deterministic six-opcode chamber ISA (`HP0..HP2` means hold point and
  change line; `HL0..HL2` means hold line and change point);
- immutable content-addressed images and snapshots;
- recursive 40-way child manifests;
- lazy structural deduplication and path-only copy-on-write;
- table-free routing between radix-40 addresses;
- one graph-preserving handle at every depth:
  `load, step, run, send, snapshot, fork, seal`.

The container vision is therefore inherited; the implementation advance is the
content graph that makes a leaf, a recursive network, and a copy-on-write fork
instances of one executable state object.

## The microVM unit

State is an incident pair `(point,line)`. The point is an endpoint label/address;
the line is its active four-member line/bus context. An `HP` instruction keeps the endpoint
and selects another incident line. An `HL` instruction keeps the line context
and selects another endpoint on it. The three software selectors are a declared
canonical chart; geometry supplies the three alternatives but does not label them.

## A network that is itself an image

At `6` levels the uniform manifest denotes
`105,025,641` recursive network VMs plus
`4,096,000,000` addressable leaf VMs---
`4,201,025,641` stateful VMs in all---but identical subtrees require
only `7` node blobs. Mutating one leaf copies only
`7` blobs along its digest path. The root
digest is itself a normal microVM-state descriptor, so the network and the leaf
share one loader ABI.

This is now an operational identity, not only a media-type identity. A runtime
can resolve any nested radix-40 address without expanding its siblings, append a
mailbox value, execute that guest, and checkpoint the result by replacing only
the digests on the addressed path. The frozen witness delivers and consumes
`13` at depth six. Execution allocates exactly
`7` path-state blobs; delivery allocates the
same path plus one separately addressable receipt blob. Every untouched sibling
keeps its digest. The reachable delivery receipt commits the source, target,
full legal route, message digest, and previous receipt; changing only the source
changes the root.

## Fractal routing

An address is a radix-40 word. The checked sample route uses
`12` line transactions against the exact bound
`12`. Each hop changes one address digit along one legal
W33 line. No next-hop table is stored.

The hop unit matters. This is a logical W33 collinearity/line-bus transaction,
whose GAP-checked base diameter is 2. BT827's separate chart-aware lowering
budgets three cube moves plus five chart-web moves per digit, hence `8n`. The
two bounds describe different layers and are not competing measurements.
BT350 first asserted the `2n` law in the corpus. The independent
[`w33_fractal_microvm_routing.g`](../analysis/w33_fractal_microvm_routing.g)
witness now proves it for this explicit Cartesian W33 routing object and freezes
the metric distinction at 7/7 checks.

## Practical lowering

- **OCI:** the bundle uses the OCI image-layout marker and image index at the
  top level. Its root is a custom W33 state descriptor and its internal
  `{slot,digest}` child references form a W33 DAG, not OCI descriptors.
- **Firecracker/Kata:** run a leaf blob as the guest workload and let the W33
  parent be the shim/supervisor and network policy.
- **WebAssembly Component Model:** map each leaf to a component world; recursive
  imports/exports become the same typed parent interface.

Those adapters are not yet implemented. This Python runtime proves deterministic
composition, content addressing, copy-on-write, and recursive routing; it is not
an operating-system or hardware isolation boundary.

## Run the lifecycle

`analysis/holobox.py` is the reference CLI over this object graph:

```console
python3 analysis/holobox.py build --output /tmp/holobox --levels 6   --program RECV,HALT
python3 analysis/holobox.py verify /tmp/holobox
python3 analysis/holobox.py send /tmp/holobox --source 0/0/0/0/0/0   --target 3/10/17/24/31/38 --message 13 --output /tmp/holobox-message
python3 analysis/holobox.py run /tmp/holobox-message --address 3/10/17/24/31/38   --commit /tmp/holobox-run
python3 analysis/holobox.py fork /tmp/holobox --address 3/10/17/24/31/38   --output /tmp/holobox-fork
python3 analysis/holobox.py route 0/0/0/0/0/0 39/38/37/36/35/34
```

The bundle is deliberately **OCI-shaped**, not yet OCI-conformant: only its
top-level layout/index follows OCI structure. No registry round trip or
external-runtime conformance claim is made.
