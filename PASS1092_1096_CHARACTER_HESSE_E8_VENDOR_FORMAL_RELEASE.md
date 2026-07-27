# Passes 1092–1096 — ATLAS characters, Hessian fiber equivalence, E8 obstruction, vendor adapter, and formal locks

## Status

- **75/75 exact certificate checks passed.**
- **7/7 focused pytest tests passed in 0.06 seconds.**
- The formal module is umbrella-wired; no local Lean executable was available.
- The vendor adapter was exercised against a reference TCP controller. No physical optical hardware or vendor device was connected.

## Pass 1092 — exact `U4(2):2` character identification

The matrix-derived projective similitude action was enumerated as the order-51840 group `U4(2):2`, with inner subgroup `U4(2)` of order 25920. Official ATLAS standard generators were found internally:

- `c` is in class `2C`;
- `d` is in class `9A`;
- `cd` has order 10;
- `c,d` generate the full group.

All 25 official ATLAS class words hit distinct computed classes and match the published orders and centralizer orders. Traces of the exact primitive frame idempotents give ten orthonormal integral characters in official ATLAS class order. Their multiplicity-weighted sum reconstructs the 540-frame permutation character exactly.

The documented CTblLib unipotent degree-15 vector matches `15a` uniquely. The complete frame-visible character list is:

- `1`;
- `15a`, `15b`;
- `20`;
- `24`;
- `60a`, `60b`;
- `64`;
- `81_plus`, `81_minus`.

The sign character pairs `15a <-> 15b` and `81_plus <-> 81_minus`; `60b` is sign-stable and vanishes on the outer coset.

Index-two Clifford theory gives the exact restrictions:

- `15a|U4(2) = 15b|U4(2) = 15`;
- `81_plus|U4(2) = 81_minus|U4(2) = 81`;
- `60b|U4(2) = 30a + 30b`;
- `60a,20,24,64,1` restrict irreducibly to the same-dimensional inner types.

Frobenius reciprocity gives:

- `Ind(15) = 15a + 15b`;
- `Ind(30a) = Ind(30b) = 60b`;
- `Ind(81) = 81_plus + 81_minus`;
- each remaining invariant inner type induces to an outer character plus its multiplier-sign twist.

A GAP/CTblLib companion matches every vector to the library row index when GAP is available.

## Pass 1093 — dual Hesse equals the nine firewall fibers

The nine multiplicity-three slice hyperplanes carry a projective Hessian action of order 216. The unique conjugacy class of eight fixed-point-free order-three elements, together with the identity, forms a regular normal subgroup

\[
C_3^2.
\]

Choosing two translation generators gives explicit affine coordinates on the nine hyperplanes. Under those coordinates every Hessian transformation acts as

\[
u \mapsto Au+b,
\qquad A\in SL(2,3),\quad b\in\mathbb F_3^2.
\]

Thus the projective group is exactly

\[
ASL(2,3)=3^2:SL(2,3),
\]

and the nine hyperplanes are equivariantly identical to the repository's nine Heisenberg positions `u in F3^2`. The associated firewall fiber is

\[
\{(u,z):z\in\mathbb F_3\}.
\]

The certificate publishes an explicit hyperplane-to-`u` bijection. Its coordinate choice is unique only up to the expected affine Hessian action.

## Pass 1094 — exact E8 bridge obstruction

The faithful `W(E6)=U4(2):2` action was constructed directly on all 240 doubled-coordinate E8 roots using the first six Bourbaki reflections. It has the Pass-1020 orbit profile

\[
1^6+27^6+72.
\]

The induced action on 120 antipodal root lines was also computed. Both permutation characters were evaluated in the same 25-class ATLAS order as Pass 1092.

The exact inner products are

\[
\langle 81_+,\mathbb C[E_8\text{ roots}]\rangle=
\langle 81_-,\mathbb C[E_8\text{ roots}]\rangle=0,
\]

and

\[
\langle 81_+,\mathbb C[E_8/\pm]\rangle=
\langle 81_-,\mathbb C[E_8/\pm]\rangle=0.
\]

Therefore every `U4(2):2`-equivariant linear map from either frame-kernel Steinberg copy to the root or root-line permutation module is zero. The proposed signed-root-sheet bridge is not merely unproved; it is representation-theoretically impossible in these carriers.

This also preserves the critical group distinction: the transitive signed-root action belongs to `Sp(4,3)=2.U4(2)`, whereas `81_plus/minus` are modules of `U4(2):2=W(E6)`.

## Pass 1095 — vendor-neutral controller adapter

A transport-separated adapter now wraps the W33 controller protocol. It enforces:

- a hard dry-run mode that opens no socket and triggers no acquisition;
- firmware identity and allowlisting;
- immutable manifest and sequence locks;
- explicit acquisition arming;
- calibration binding and expiry;
- four-port routing before acquisition;
- replay rejection;
- emergency-stop support.

The complete 240-command schedule passed through a reference TCP controller only in armed mode. Dry-run mapped all commands without opening a connection. Unarmed acquisition and unapproved firmware both failed closed.

This is a production-shaped adapter conformance test, not a physical-device result.

## Pass 1096 — formal character/Hesse/E8 locks

The Lean module freezes, in official ATLAS class order:

- the 25 class sizes;
- `chi81Plus` and `chi81Minus`;
- the multiplier-sign character;
- the 240-root and 120-root-line permutation characters;
- the identity `chi81Minus = epsilon * chi81Plus`;
- all four zero E8 multiplicity numerators;
- the rank-32 and rank-22 dimension/multiplicity identities;
- the two distinct Steinberg tensor SHA-256 hashes.

The large tensors remain external exact certificates rather than enormous Lean literals. The module is imported by `formal/W33.lean` and compiled in the isolated workflow.

## Authoritative artifacts

- `analysis/w33_pass1092_u42dot2_character_identification.py`
- `analysis/w33_pass1092_u42dot2_character_match.g`
- `analysis/w33_pass1093_dual_hesse_firewall_fiber_equivalence.py`
- `analysis/w33_pass1094_e8_root_sheet_bridge.py`
- `analysis/w33_pass1095_vendor_controller_adapter.py`
- `analysis/w33_pass1096_formal_character_hesse_e8_lock.py`
- `formal/W33/Pass1096CharacterHesseE8Lock.lean`
- `data/w33_pass1092_u42dot2_character_identification.json`
- `data/w33_pass1093_dual_hesse_firewall_fiber_equivalence.json`
- `data/w33_pass1094_e8_root_sheet_bridge.json`
- `data/w33_pass1095_vendor_controller_adapter.json`
- `data/w33_pass1096_formal_character_hesse_e8_lock.json`
- `data/w33_pass1092_1096_release.json`
- `hardware/w33_pass1095_vendor_adapter_receipt.json`
- `tests/test_w33_pass1092_1096.py`
- `.github/workflows/pass1092_1096_exact.yml`
