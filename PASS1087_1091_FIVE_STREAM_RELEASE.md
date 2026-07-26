# Passes 1087–1091 — canonical Steinberg parity, exact frame algebra, dual-Hesse geometry, controller boundary, and formal locks

## Release status

All five requested directions were executed above the live Pass-1086 frontier.

- **77/77 exact certificate checks passed.**
- **7/7 focused pytest tests passed in 0.02 seconds.**
- The new Lean module is wired into `formal/W33.lean`; no local Lean executable was available, so compilation of the new module is delegated to the committed CI workflow.
- A real operating-system TCP transport boundary was exercised against a loopback reference controller. No physical optical hardware was connected.

## Pass 1087 — canonical resolution of the two Steinberg copies

Pass 1083 found a two-dimensional space of `PSp(4,3)`-equivariant maps from the 81-dimensional Levi cycle module into the 504-dimensional frame-incidence kernel. Pass 1087 computes the multiplier-two outer similitude on that Hom-space.

In the cross-relation basis `(T1,T2)`, the action is

\[
\begin{pmatrix}1&-1\\0&-1\end{pmatrix}.
\]

The canonical eigenmaps are therefore

\[
T_+=T_1,\qquad T_-=T_1+2T_2.
\]

Both have rank 81, and

\[
\operatorname{rank}[T_+\;T_-]=162.
\]

They have identical inner equivariance but opposite outer parity. The outer trace is `+3` on the first image and `-3` on the second. Thus they are the two inequivalent extensions

\[
\mathrm{St}_+,\qquad \mathrm{St}_-=\mathrm{St}_+\otimes\varepsilon
\]

of the same inner Steinberg module, where `epsilon` is the multiplier-sign character of the outer `C2` quotient. The outer element preserves each image; it does not exchange them. No identification with signed-E8 sheets or chirality is made without another equivariant map.

## Pass 1088 — exact rank-32 and rank-22 adjacency-algebra decomposition

The complete inner and outer frame adjacency algebras were split at the good prime

\[
p=1{,}000{,}033,
\]

which does not divide the group order and contains both `sqrt(3)` and `sqrt(-1)`. Distinct central eigenvalues permit exact Lagrange construction of primitive central idempotents.

For the inner `PSp(4,3)` action,

\[
\mathbb C^{540}\cong
1+3\cdot15+2\cdot20+2\cdot24+2\cdot30_a+2\cdot30_b+60+64+2\cdot81.
\]

The multiplicity-square identity is

\[
1^2+3^2+2^2+2^2+2^2+2^2+1^2+1^2+2^2=32.
\]

The 504-dimensional spread-incidence kernel is

\[
2\cdot15+20+2\cdot24+2\cdot30_a+2\cdot30_b+60+64+2\cdot81.
\]

For the outer projective-similitude action,

\[
\mathbb C^{540}\cong
1+2\cdot15_a+15_b+2\cdot20+2\cdot24+60_a+2\cdot60_b+64+81_++81_-.
\]

Consequently the inner Steinberg isotypic component splits exactly as

\[
2\cdot81\longrightarrow81_+\oplus81_-.
\]

The executable witness regenerates the full orbital-basis coefficient vectors of every primitive idempotent. The committed compact certificate retains all component dimensions, multiplicities, localization tables, and individual idempotent SHA-256 hashes. It also verifies objectwise that the spread module is `1+15+20`.

## Pass 1089 — the nine triple hyperplanes are dual Hesse

The nine multiplicity-three hyperplanes in the `G32 -> G25` parabolic slice are exactly

\[
x_i-\zeta x_j=0,
\qquad 1\le i<j\le3,
\qquad \zeta\in\{1,\omega,\omega^2\}.
\]

They form the reflection arrangement of `G(3,3,3)`, also called the Ceva(3) or dual-Hesse arrangement. It is the configuration

\[
(9_4,12_3):
\]

nine lines and twelve triple points.

The twelve `G25` reflecting hyperplanes form the Hesse arrangement, with nine quadruple points and twelve double points. The two arrangements are mutually projectively dual:

- the twelve triple points of the nine-line arrangement are exactly the twelve `G25` line normals;
- the nine quadruple points of the `G25` arrangement are exactly the nine extra line normals.

Their union has intersection profile

\[
12\text{ quintuple points},\quad9\text{ quadruple points},\quad36\text{ double points}.
\]

The order-648 `G25` action has scalar kernel `C3` and projective Hessian image of order 216 on both arrangements. This provides exact cube-root phase geometry but does not identify these objects with unrelated nine-fiber constructions without a separate map.

## Pass 1090 — production-shaped controller protocol boundary

The 240-command acquisition schedule crossed an actual operating-system TCP socket using protocol `W33-MZI-TCP/1.0`.

The protocol enforces:

- canonical JSON-lines framing;
- CRC32 on each request and response;
- immutable manifest, session, and sequence locks;
- explicit ACK/NACK replies;
- calibration IDs bound to all routes and acquisitions;
- four routed detector ports before acquisition;
- hash-chained telemetry and HMAC signing;
- externally committed key material;
- a separate offline-unblinding executable.

All 240 commands were ACKed: 40 calibrations, 160 routes, and 40 acquisitions. The synthetic witness is

\[
W=10.03975>7.
\]

Malformed CRC and route-without-calibration probes both failed closed. The manifest contains only the escrow-key commitment and explicitly excludes the obsolete contextual-fraction label.

This advances the earlier in-process rehearsal to a serialized TCP controller boundary. It remains a loopback reference controller, not a physical-device result. A vendor deployment requires an endpoint or adapter implementing the same fail-closed protocol.

## Pass 1091 — formal orbital and intertwiner lock

The corrected finite maps are explicit Lean definitions:

- the 32-orbital transpose involution;
- the 32-orbital outer-fusion involution;
- the 22-orbital transpose involution.

`native_decide` locks

\[
12\text{ inner self-paired},\quad20\text{ non-self-paired},\quad10\text{ transpose pairs},
\]

and

\[
22\text{ outer-fusion orbits},\quad14\text{ outer self-paired orbitals}.
\]

The two exact `540 x 160` Steinberg tensors are SHA-256 locked in the Lean module. The Python formal certificate independently rechecks

\[
BT_\pm=0,\qquad T_\pm D^T=0,\qquad T_\pm K=160T_\pm,
\]

inner equivariance, and outer parity.

Lean also contains generic matrix lemmas showing that `B*T=0` puts each column of `T` in the left kernel and that the cycle-projector identity holds entrywise. The large tensors remain external exact certificates rather than enormous Lean literals.

## Authoritative artifacts

Executable witnesses:

- `analysis/w33_pass1087_canonical_steinberg_parity.py`
- `analysis/w33_pass1088_frame_adjacency_wedderburn.py`
- `analysis/w33_pass1089_dual_hesse_triple_hyperplanes.py`
- `analysis/w33_pass1090_controller_protocol_boundary.py`
- `analysis/w33_pass1090_offline_unblind.py`
- `analysis/w33_pass1091_formal_orbital_intertwiner_lock.py`

Formal source:

- `formal/W33/Pass1091FrameOrbitalIntertwiner.lean`

Machine certificates:

- `data/w33_pass1087_canonical_steinberg_parity.json`
- `data/w33_pass1088_frame_adjacency_wedderburn.json`
- `data/w33_pass1089_dual_hesse_triple_hyperplanes.json`
- `data/w33_pass1090_controller_protocol_boundary.json`
- `data/w33_pass1091_formal_orbital_intertwiner_lock.json`
- `data/w33_pass1087_1091_release.json`

Hardware surfaces:

- `hardware/w33_pass1090_manifest.json`
- `hardware/w33_pass1090_analysis.json`
- `hardware/w33_pass1090_unblinding_receipt.json`
- `hardware/w33_pass1090_transcript_summary.json`

Regression and CI:

- `tests/test_w33_pass1087_1091.py`
- `.github/workflows/pass1087_1091_exact.yml`
