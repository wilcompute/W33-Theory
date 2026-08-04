# Passes 3332–3343 — Gauge defects, fault-aware hypercubes, and Clebsch recovery

## Status

The exact verifier reports **18/18 checks passed** and the focused regression passes. The packet executes the five requested fronts and two additional constructions against live `master` after the merged Passes 3296–3319 and the parallel reservation for Passes 3320–3331.

The live chromatic boundary remains

\[
\boxed{10\leq\chi(H)\leq11}.
\]

No source-only result is promoted to an observed FPGA, physical error-rate, fault-tolerant quantum-memory, or laboratory claim.

---

## 3332–3333 — minimum nontrivial flat gauge defects

The filled port complex has 45 vertices, 720 edges and 240 edge-disjoint triangular faces. Flat coefficients take values in

\[
A=C_3^5\cong\mathbb F_3^5.
\]

Every graph edge belongs to one filled face. Consequently a weight-one cochain violates that face equation and cannot be flat.

A weight-two flat cochain must use two edges of one filled triangle. If the third edge is zero, the two nonzero values are determined by one vector \(v\in\mathbb F_3^5\setminus\{0\}\). The block graph has edge connectivity 32, so deleting those two support edges leaves it connected. If such a cochain were a coboundary, its vertex potential would be constant on the remaining graph and hence zero on the two deleted edges as well, a contradiction.

Therefore

\[
\boxed{d_{\rm gauge}=2}.
\]

There are

\[
240\cdot3=720
\]

geometric support patterns. The exact 25,920-element \(PSp(4,3)\) action is transitive on them. For every fixed nonzero coefficient vector:

\[
|\operatorname{Orb}(z_v)|=720,
\qquad
|\operatorname{Stab}(z_v)|=36.
\]

The orbit of \(v\) does not contain the orbit of \(-v\) when coefficient labels are fixed. Thus the full labeled classification has

\[
\boxed{242}
\]

\(PSp(4,3)\)-orbits and

\[
720\cdot242=\boxed{174{,}240}
\]

minimum cochains. After identifying \(v\sim-v\), the coefficient fiber is

\[
PG(4,3),\qquad |PG(4,3)|=\frac{3^5-1}{3-1}=121,
\]

giving 87,120 projective defect species.

The block graph has 5,280 triangles, of which 240 are filled and 5,040 are unfilled. Every minimum defect has nonzero holonomy on exactly

\[
\boxed{42}
\]

unfilled triangles. Its shortest gauge-invariant witness therefore has cycle length three.

---

## 3334–3335 — exhaustive fault-aware knight/hypercube routing

The frozen nonlinear signature controller uses an optimal \(Q_4\) placement with total routing work 34 and dilation two.

### Bare \(Q_4\)

All 32 single-edge failures remain connected. Sixteen leave the original schedule unchanged; the remaining sixteen increase dilation to three, with worst total work 40.

All 496 two-edge failures remain routable. The worst cases have dilation four or work 44.

A vertex failure is categorically different: every physical vertex stores one logical state, so every one of the 16 vertex failures removes at least two directed controller transitions. No unreplicated 16-slot implementation can tolerate arbitrary vertex loss.

### Mirrored \(Q_5=Q_4\square K_2\)

Store each logical state at the corresponding coordinate in both Q4 layers. Then:

- all 32 single-vertex failures preserve all transitions at exactly work 34 and dilation two;
- all 80 single-edge failures preserve all transitions at exactly work 34 and dilation two;
- all 3,160 two-edge failures preserve all transitions; only 16 cases increase the schedule;
- all 2,560 one-vertex/one-edge cases preserve all transitions;
- among 496 two-vertex failures, exactly 16 are catastrophic.

Those 16 catastrophic pairs are precisely the interlayer replica pairs

\[
\{x,x\oplus10000_2\}.
\]

Every other two-vertex failure retains all logical states.

Under a static one-cycle model with no state migration and one logical label per physical slot, arbitrary single-vertex tolerance requires two simultaneous copies of every one of the 16 states. Hence at least 32 physical slots are necessary. The mirrored Q5 construction attains this lower bound exactly.

`rtl/w33_q5_single_fault_router.v` implements the exact single-fault policy: route an entire dispatch in the layer opposite a layer-local fault; ignore an interlayer-edge fault by staying within one layer.

---

## 3336 — absolute global anchor/orbital no-go

The actual action on the 45 anchor octets has order 25,920 and is transitive. Its complete fixed-point character census is frozen by element order:

| order | fixed anchors | elements |
|---:|---:|---:|
| 1 | 45 | 1 |
| 2 | 13 | 45 |
| 2 | 5 | 270 |
| 3 | 9 | 80 |
| 3 | 6 | 240 |
| 3 | 3 | 480 |
| 4 | 1 | 3,780 |
| 5 | 0 | 5,184 |
| 6 | 4 | 1,440 |
| 6 | 2 | 2,160 |
| 6 | 1 | 2,160 |
| 9 | 0 | 5,760 |
| 12 | 1 | 4,320 |

The generated anchor group is perfect:

\[
G'=G,
\qquad |G|=25{,}920.
\]

The intrinsic signature-state automorphism group has order 72 and derived series

\[
72\to18\to9\to1,
\]

so it is solvable. Any global action on signature orbitals induced through intrinsic signature-state automorphisms therefore has solvable image. A homomorphic image of a perfect group is perfect, and a perfect solvable group is trivial.

Moreover, every coherent-algebra automorphism fixes the identity orbital, whereas the anchor action is transitive.

Therefore

\[
\boxed{\text{no intrinsic }PSp(4,3)\text{-equivariant anchor/orbital bijection exists}.}
\]

This is stronger than the earlier local canonicity obstruction. A correspondence can only be introduced by adding genuinely external structure that does not arise from the intrinsic signature coherent configuration.

---

## 3337 — the full \(M_{22}\) separable dual cannot improve nine

At a regular envelope basepoint the Terwilliger algebra is the complete matrix algebra

\[
T_x=M_{22}(\mathbb Q).
\]

Thus an arbitrary local positive kernel \(K\succeq0\) is already allowed; its symmetric cone has 253 coordinates.

The 45-block graph has spectrum

\[
32^1,\quad2^{24},\quad(-4)^{20}.
\]

For every nonzero separable lift

\[
W=A_{45}\otimes K,
\]

write \(\mu=\lambda_{\max}(K)>0\). Product spectra give

\[
\lambda_{\max}(W)=32\mu,
\qquad
\lambda_{\min}(W)=-4\mu.
\]

Hence every such full-local-algebra lift has Hoffman bound

\[
1-\frac{32\mu}{-4\mu}=\boxed9.
\]

The obstruction is not insufficient local algebra—the local algebra is already maximal. Any improved chromatic dual must be nonseparable across blocks and must retain profile-sensitive orientation tensors. This agrees with the parallel 1,045-coordinate rational-dual frontier.

---

## 3338–3339 — complete one/two-bit fault census and minimum recovery tag

Across the 22 valid five-bit envelope states there are 110 one-bit fault events and 220 two-bit fault events.

Validity alone detects only:

\[
36/110=18/55
\]

of one-bit faults and

\[
70/220=7/22
\]

of two-bit faults, because the remaining faults land on another valid envelope state.

For trusted side information, two source states are confusable under \(t\)-bit correction whenever their Hamming distance is at most \(2t\). Exact DSATUR exhaustion gives:

| contract | confusability distance | exact chromatic number | minimum trusted bits |
|---|---:|---:|---:|
| correct one bit | 2 | 7 | 3 |
| correct one, detect two | 3 | 11 | 4 |
| correct two bits | 4 | 16 | 4 |

The last result has a 16-clique lower-bound certificate and an explicit 16-colouring, so four trusted bits are necessary and sufficient for correcting every two-bit state fault.

The optimal tag is unexpectedly simple:

\[
\operatorname{tag}(x)=
\begin{cases}
x_{3:0},&x_4=0,\\
\neg x_{3:0},&x_4=1.
\end{cases}
\]

It labels the antipodal axis \(\{x,\bar x\}\) of \(Q_5\). Same-tag valid states are either identical or five bits apart, so their radius-two balls are disjoint.

`rtl/w33_envelope_clebsch_recovery.v` implements this decoder. All

\[
22\left(1+\binom51+\binom52\right)=\boxed{352}
\]

zero-, one-, and two-bit cases are exhaustively checked.

The four-bit tag must itself be trusted or protected independently; this packet does not hide that assumption.

---

## 3340 BONKERS — the recovery network is the Clebsch graph

Quotient \(Q_5\) by bitwise complement. The 32 words become 16 antipodal axes. The quotient graph is the folded 5-cube, exactly the Clebsch graph:

\[
\boxed{SRG(16,5,0,2)}
\]

with 40 edges, diameter two, and spectrum

\[
5^1,\quad1^{10},\quad(-3)^5.
\]

The envelope occupies the axes in a highly structured way:

- six axes contain two valid antipodal states;
- ten axes contain one valid state and one guard state;
- every guard word is the unique antipode of one of those ten valid states.

Thus the minimum two-error checksum is not an arbitrary lookup table. It is the natural vertex set of the Clebsch quotient network.

---

## 3341 BONKERS — projective gauge particles with 42 local witnesses

The minimum gauge defects form the exact homogeneous bundle

\[
720\times(\mathbb F_3^5\setminus\{0\}).
\]

After identifying coefficient inversion, this becomes

\[
720\times PG(4,3),
\]

with 87,120 projective defects. Every such defect is localized by exactly 42 shortest unfilled-triangle holonomies.

This yields a concrete two-level syndrome address:

1. one of 720 geometric face-corners;
2. one of 121 projective five-trit coefficient directions.

It is a finite gauge-defect atlas, not a claim of physical particles or spacetime curvature.

---

## Digital evidence and boundaries

The source packet includes:

- one exact Python verifier and two frozen compressed JSON artifacts;
- focused pytest regression;
- mirrored-Q5 single-fault router RTL;
- minimum Clebsch recovery RTL;
- exhaustive 352-case recovery and 96-route testbench;
- Icarus/Yosys/nextpnr evidence workflow;
- all three manuscript integrations and the public index insert.

Observed simulation, synthesis, placement, timing and PDF hashes remain gated by the focused workflow.
