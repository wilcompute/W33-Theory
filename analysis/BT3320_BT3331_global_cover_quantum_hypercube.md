# Passes 3320–3331 — Global exact-cover closure, quantum Hamming walk, and hypercube boundary

## Status

The eight requested fronts are implemented as one exact packet. The focused verifier regenerates the cover arithmetic, rational-dual compression, decoder contract, adaptive proof tree, Szegedy phase ledger, exterior-sector falsifier, tau-Fourier decomposition, and the hypercube host from source. The live chromatic boundary remains

\[
10\leq\chi(H)\leq 11.
\]

No queued workflow, timeout, numerical phase display, or source-level RTL statement is promoted beyond its evidence class.

## 3320–3321 — Complete global cover reconciliation

The historical exact global certificate contains

\[
3{,}547{,}800
\]

exact 60-frame covers in 327 \(PSp(4,3)\)-orbits. The closed Hamming switch component from Passes 3296–3297 contains 1,574,640 covers in 135 orbits. Their exact complement is therefore

\[
\boxed{1{,}973{,}160\text{ covers in }192\text{ orbit classes}.}
\]

The stabilizer distribution reconciles objectwise:

\[
(228,84,15)-(108,27,0)=(120,57,15)
\]

for stabilizer orders \((2,4,8)\). Equivalently,

\[
1{,}973{,}160
=120(12{,}960)+57(6{,}480)+15(3{,}240).
\]

This closes the global count while preserving a structural distinction: the known Hamming component supplies explicit switch paths; the 192 exterior orbit classes are certified by the global orbit census but not thereby connected to the Hamming component.

## 3322 — Exact orbit compression of the rational dual batch

The profile-aware rational dual originally exposes 55 matrices and 1,045 coordinates for each of 195,490 deficit profiles. Quotienting matrix positions by each profile stabilizer reduces the total batch from

\[
204{,}287{,}050
\]

to

\[
\boxed{98{,}191{,}335}
\]

exact rational block coordinates. Thus 106,095,715 coordinates are removed before any SDP search. The exact retained fraction is

\[
\frac{93{,}963}{195{,}490},
\]

and the eliminated fraction is \(101{,}527/195{,}490\). The balanced profile needs only two matrix orbits, hence 38 coordinates. This is a compiler theorem, not an eleven-colour certificate.

## 3323 — Exhaustive \(S_3\) Fourier decoder contract

The decoder specification and an independent behavioral RTL model agree on all

\[
2\cdot8\cdot8^3=8{,}192
\]

input cases: valid/invalid gate, all eight three-bit symbols, and all reliability triples over \(\{0,\ldots,7\}\). The outcome histogram is

\[
2100\text{ correctable},\quad460\text{ ties},\quad1024\text{ invalid symbols},
\]

with 4,608 idle or detected-but-not-correctable cases. The vector stream SHA-256 is

`693cf77d3dc355b4040ef1eb82ae96ee8db53c30388cf95192ec98fafffdddbe`.

Local Icarus was unavailable; simulator equivalence remains a separate workflow gate.

## 3324 — Proof-carrying UNKNOWN refinement

The ten unresolved depth-three children below parent \((0,3)\) are partitioned exactly into 100 depth-four grandchildren

\[
(0,3,c,d),\qquad c,d\in\{0,\ldots,9\}.
\]

All records have distinct canonical hashes and each parent has the complete ten-child cover. The existing proof run has completed workflow jobs for shards 0–3 and is solving shard 4, but status artifacts were not imported; therefore every such result remains UNKNOWN. Green workflow completion is not SAT or UNSAT evidence.

## 3325 — Szegedy compiler for the Hamming-orbifold walk

For \(P=W/10\), the discriminant eigenvalues are

\[
1,\frac7{10},\frac25,\frac1{10},-\frac15,-\frac12.
\]

Using \(U=(2\Pi_B-I)(2\Pi_A-I)\), each discriminant value \(\lambda\) produces phases

\[
z=e^{\pm2i\arccos\lambda}
\]

and the exact quadratic

\[
z^2-(4\lambda^2-2)z+1=0.
\]

The sparse compiler has 1,242 nonzero directed species transitions and 1,350 weighted arc tokens. Its stationary amplitude is proportional to \(\sqrt{|O_i|/243}\). This is an exact quantum-walk spectrum, not a physical speedup claim.

## 3326 BONKERS — the 192/tomotope count-only analogy fails

The exterior census has 192 orbit classes, numerically matching the 192 tomotope flags. But the exterior classes carry a certified three-colour stabilizer partition

\[
120+57+15=192.
\]

Cardinality alone supplies no equivariant map to tomotope flags, and forgetting the partition discards exact structure. The packet therefore rejects the identification from the number 192 alone while leaving open a future construction with additional equivariant data.

## 3327 BONKERS — tau-invariant ternary Fourier decomposition

The full ternary Hamming graph has spectrum

\[
10^1,\;7^{10},\;4^{40},\;1^{80},\;(-2)^{80},\;(-5)^{32}.
\]

The affine involution has eigenspace traces \((1,2,4,8,4,8)\). Therefore the invariant multiplicities are exactly

\[
\boxed{1,6,22,44,42,20},
\]

summing to 135, and the anti-invariant multiplicities are \((0,4,18,36,38,12)\). This derives the quotient spectrum from the full ternary Fourier grading rather than numerical diagonalization of the 135-state quotient.

## 3328–3329 — Exact hypercube boundary and host

Encode one trit using a dedicated one-hot block:

\[
0\mapsto100,\qquad1\mapsto010,\qquad2\mapsto001.
\]

Five trits become 243 constant-weight-five words in \(Q_{15}\), satisfying

\[
\boxed{d_{Q_{15}}(\mathrm{enc}(x),\mathrm{enc}(y))=2d_{H(5,3)}(x,y).}
\]

Thus \(H(5,3)\) is exactly the distance-two graph on this block-one-hot code. The involution \(\tau\) becomes a pure permutation of the 15 binary coordinates:

\[
(9,11,10,7,6,8,4,3,5,0,2,1,12,13,14).
\]

An ordinary hypercube embedding is impossible: \(H(5,3)\) contains triangles, whereas every \(Q_n\) is bipartite.

The packet therefore separates three cube roles:

1. the intrinsic toroidal-knight controller network \(Q_4\);
2. the secondary 16-state complement codec \(Q_4\), whose raw Levi adjacency remains \(4K_4\);
3. the intrinsic block-one-hot \(Q_{15}\) host for the 243-state ternary cover cube.

No canonical map from the 16 controller states to the 135 cover species is claimed.

## Reproduction

```bash
python bootstrap/pass3296_3307/materialize.py
python analysis/bt3320_3329_global_cover_quantum_hypercube.py
python -m pytest -q tests/test_bt3320_3331_global_cover_quantum_hypercube.py
```

Expected status:

`PASS_EXACT_EIGHT_FRONT_GLOBAL_COVER_QUANTUM_HYPERCUBE_PACKET`
