# Eight-front recovery + physics closure

Date: 2026-08-29

This note closes the requested five Holotrade continuations plus three literature-informed physics attacks. It also reconciles the parallel PG(3,4) polarity/sentinel and sentinel-shell-matroid commits that landed during the pass.

## Five Holotrade continuations

### 1. PSp orbit of the 19/19 attractor

The 933 policy-selected 19/19 period-two cycles are not themselves a PSp-invariant set because the deterministic lexicographic tie-break breaks geometric symmetry. They all lie inside one ambient PSp(4,3) orbit of 12,960 unordered cycles. A cycle stabilizer has order 2; either 10-point state has orbit 6,480/stabilizer 4; the shared 9-point core has orbit 1,440/stabilizer 18.

Commits: `5b902bd4c40e0892b6a103e330348d983195c489`, `d7b8becb9364e2d2c806e6aba556f3d14e6877ba`.

### 2. Generic healthy recovery collapses to local incidence arithmetic

For any healthy 10-busy W33 state,

`F_after = F + s1(source) - z(destination) - 1[shared line was singleton]`.

Every busy source has at least three adjacent idle destinations, so the 3-ray/1-hop floor is always available. Maximizing this score, then release headroom, then labels reproduces the existing topology-aware software scorer exactly on all 92,160 decisions encountered over 32 steps from the 2,880 starts (25,184 distinct states).

Commits: `1b6596d87f96742000fec008816ac50fc3716978`, `243373912b55c9c876481d889e00a2accae87238`, `972aba54d8b79d825a3c0100c5899f374273dcf7`.

### 3. Exhaustive two-failure and worst-triple recovery

All `2880*C(30,2)=1,252,800` two-idle-node failure pairs were exhausted. Their initial free-line histogram is `0^83520 1^77760 2^544320 3^547200`. The topology-aware policy restores at least three lines after one move in every case that starts below three.

All `11,692,800` three-idle-node initial patterns were counted. The worst zero-initial-placement class has 1,247,040 cases; all regain at least three free lines after one aware migration. The aware policy reaches nine within six moves in all but 306 worst triples; the legacy tie-break leaves 549,224 worst triples below three after six moves.

Commits: `0d4ee8f3caa402b12c8d4af8580c99211243bbd2`, `4e3222dc398254f124f138c2b93d3deb50a5a8a0`.

### 4. Energy optimization moved to the correct H_n layer

In the actual seeded Fleet, level-1 point-to-point movement stays inside one datacenter and cannot change site energy. Restricting 320 sources to cross-datacenter candidates, the minimum full-address cost is exactly 7 rays / 33 hops for every source. Equal-cost candidate sets contain 52--219 nodes, so energy/carbon may legitimately break ties only there.

On the declared seeded catalog, energy-aware tie-breaking changes 148/320 destinations while preserving the primary movement cost. Aggregate `baseEnergy*PUE` falls 15,505.55 -> 13,547.88 (12.63%) and the catalog carbon index 96,016 -> 72,256 (24.75%). These are deterministic catalog sensitivities, not telemetry.

Commits: `c4a7ad64ac02344f863bdd9a8a332e0ff8bcd71d`, `b43fa651490876ac26fa0a5d4e998f0a8d4e0fdc`.

### 5. Combined recovery RTL core

The first move still uses the one-bit 3+3 hinge-block selector; after `advance`, the RTL switches to the exact local incidence scorer. The committed core embeds the 40 W33 lines and all 40 point-line masks directly.

Software regression establishes: entry objective equivalence on all 2,880 near-ovoids; exact second-move identity on all 2,880; exact generic healthy-policy identity on the previously certified 92,160 decisions. Source-level registered state is three bits (`valid`, `entry_q`, `block_q`).

A Yosys structural/synthesis harness is committed, but this execution environment did not contain Yosys/yowasp-yosys; no new LUT/cell count is claimed.

Commits: `2db636f99cc1f9b6236e1a4b3ae56581ffca74d4`, `36dea5627ada87f4d277a0f937b4118233bab758`, `62469d73e9921cebcdc4479fa17d3924f14a91ab`, `e041251beac28509be471672b51f42789276a7fb`, `1c36cf43e50bf075ed92b32d051bac29a118c3c7`.

## Three physics-oriented outside-box attacks

### A. 85-state flat-band robustness/index audit

The chiral 40x45 coupling has rank 25 and therefore 35 zero modes. Arbitrary chiral-preserving perturbations protect only five by sublattice imbalance/index; a concrete perturbation reaches rank 40. The full 15+20 dark sector is protected by the established PSp representation mismatch `40=1+24+15`, `45=1+24+20`.

Commits: `2ec375424b14f44b92e190fabd91099a66432ee6`, `51d65abef198db1949a7152c99a950d25bf45f51`.

Parallel reconciliation: the new polarity/sentinel and shell-matroid packet strengthens the same 40x45 carrier over F2. In particular the 45 columns of B are the complete weight-eight sentinel orbit and their Hamming geometry reconstructs GQ(4,2). This does not alter the real/complex chiral-rank statement; it supplies an additional binary-code incarnation of the same columns.

### B. Exact qutrit x chirality synthetic coordinate

The six local microstates admit coordinates `(chi,t) in F2 x F3` with group `C3 x S3 = (C3 x C3):C2`. The center is a common qutrit translation; the quotient C2 swaps the two chirality blocks selected geometrically by the residual hinge points. The minimal two-leg/three-site synthetic Hamiltonian has characteristic polynomial

`((x-2)^2-g^2) ((x+1)^2-g^2)^2`.

Commits: `e08916884334b1f69adc547f1df68d7c7347f3e5`, `1fe2f1330286877f62d91f8ffed3c18efea09a77`, cleanup `e017bff7e673dd5749328af3d232c885216c8c12`.

### C. Koopman period-two mode and time-crystal no-promotion

Every deterministic recovery attractor is a two-cycle, so its two-state Koopman operator has eigenvalues +1 and -1. But the measured free-line headroom overlaps the -1/pi mode only for 36/2,880 starts (the 16/17 cycles). The 19/19, 17/17 and 16/16 cycles are state-periodic but headroom-stationary.

Together with the absence of a demonstrated periodic many-body drive, thermodynamic limit, and perturbation-robust spontaneous time-translation breaking, this is an exact reason to retain `period-two recovery orbit` / `Koopman -1 mode` language and not promote the phenomenon to a discrete time-crystal phase.

Commits: `6214d5561a4e862baac493f32292ff7ec3148e65`, `0adb8114e452ad27be3b139251f01159bde9132f`.

## Literature selection boundary

The outside-box ideas were chosen after repo audit and web review of recent synthetic-dimension, flat-band, and discrete-time-crystal literature. Literature supplied analogies and falsification criteria; every promoted project statement above is finite and exact.

The manuscript insert is `analysis/PASS10933_10940_physics_flatband_synthetic_koopman_insert.tex`; the literature/repo audit note is `analysis/2026-08-29_PHYSICS_OUTSIDE_BOX_FLATBAND_SYNTHETIC_KOOPMAN.md`.
