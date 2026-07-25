# July 10–11, 2026 Recent-Commit Audit: Passes 157–192 and Levi v2–v5

## Scope

This audit began with a GitKraken fetch and a complete two-day commit scan on
`master`, then re-read the current `w33_paper.tex`, `photonic_holonet.tex`,
`holonet_practical_implications.tex`, and `docs/index.html`. Searches were
expanded through related witnesses, JSON, tests, Continuity decisions, and the
controller data before treating a connection as new.

The high-volume history falls into four clusters:

| commit cluster | content inspected | audit disposition |
|---|---|---|
| `6af94d35d` through `11f5d9122` | Passes 158–168, chiral lattices, binary shadow, theta/MacWilliams | executable core retained; later claims checked against object witnesses |
| `cd3b5b1fa` | Passes 169–172 and 175 | repaired orbital-signature, exact character, and shell-generation claims |
| `d8cc2006d` | Passes 173–182 | retained incidence/E8/theta/Sastry–Sin/Poisson results; corrected noncanonical 11/8, Hom, and intrinsic-axis boundaries |
| `bd0fb7ebe` | Passes 183–187 | replaced sampled/heuristic statements by exhaustive distributions, brick boundaries, S3/C2, exact sparse families, and exhaustive irreducibility scans |
| Levi v2/v3 commits | symbolic rank, code/runtime, E6 geometry, optical compiler | inspected for continuity and claim-tier consistency |
| `bd86da8c4` v4 merge and prerequisites | Lean mirror, cohomology, incidence functor, foundry/HIL | aggregate made fresh-by-default and exact-cache checked; formal scope narrowed to what Lean proves |
| `31eef35a9` v5 merge and prerequisites | Fourier/H2/E8 lanes, hybrid, RTL/time taggers/GDS | hardware/API/RTL and claim-tier audit completed; abstract/model artifacts no longer presented as fabricated-device proof |

Recent speculative physics commits were read as part of the requested history
scan, but this packet does not independently endorse their phenomenological
claims. Verification status is kept separate from publication status.

## Corrected claims

1. **Order eight.** A selected Smith generator can read `11/8`; it is not a
   generator invariant. Exhaustive distributions are dark `{3,11}/8` and code
   `{5,13}/8`, with equal multiplicities on each side.
2. **Pass 183 cokernel.** Matching invariant factors proves an abstract finite
   abelian group isomorphism, not a discriminant-quadratic-form isometry.
3. **Passes 181/184.** Nonzero Hom is not automatically an embedding;
   endomorphism dimension one means brick, not automatically simple. Explicit
   rank-ten maps and the exhaustively simple five are stated separately.
4. **Passes 182/185.** The true four-valent orbital remains group-selected.
   Once selected, all line/axis labels are intrinsic and equivariant. Three
   axes form `S3/C2`, not a free S3 torsor.
5. **Passes 186/188.** The dodecads are not icosahedra. They are exact crowns
   `K6,6` minus a matching, glued from two exact K6 families with faithful S6.
6. **Pass 190.** Steinberg numbers are modular composition multiplicities,
   not by themselves a selected logical register or hardware protection
   result.
7. **Pass 191.** `120*36=4320` is not a transitive product carrier. It splits
   as `3240+720+360=120*(27+6+3)`. The distinguished three-suborbit, not the
   full product, supplies the native S3 completion fibre.
8. **Levi v5 hardware.** The GDS output is an abstract placement sketch; the
   hybrid result is fixed-seed/model power; the Verilog-A is static; the phase
   manifest is incomplete (`376` commands versus `120` layout slots). Vendor
   adapters, timestamp-sensitive routing, overflow handling, snapshot RTL, and
   backpressure behavior are now tested at their actual tier.

## New exact breakthroughs

### Complete order-eight census

```text
address dark : 3 -> 32768, 11 -> 32768
route dark   : 3 ->   512, 11 ->   512
point code   : 5 -> 32768, 13 -> 32768
line code    : 5 ->   512, 13 ->   512
```

### Binary uniseriality

`F2^40` has exactly eight invariant submodules and layers
`1|14|1|8|1|14|1`. The result is based on exhaustive nonzero-vector orbit
scans and successive simple-socle computations, not a Norton shortcut.

### Steinberg carrier census

Live GAP transports the computed table to CTblLib `U4(2)` and gives the
Steinberg-81 column

```text
(points, lines, arcs, shell, trades, supports,
 skew, hyperbolic, Q42 arcs, flags)
= (0, 0, 2, 3, 0, 0, 2, 1, 2, 1).
```

### Double-six completion geometry

```text
axes x double-sixes = 3240 + 720 + 360
                     = 120 x (27 + 6 + 3)
pair stabilizers    = 8, 36, 72.
```

For the special three, the axis stabilizer `216` acts through full S3 with
kernel `36`.

### Signed edge codec

```text
240 signed trades <-> 40 W33 lines x 6 edges
1 -> C3^3 -> H_line -> S4 -> 1.
```

Sign reversal is edge complement. The six signed states carry S4 on
tetrahedral edges; complementary pairs give the S3/C2 axis quotient.

## Levi v4/v5 tier audit

- v4 aggregate reruns all five witnesses and compares normalized fresh output
  with committed certificates. Formal/cohomology/functor tracks use exact
  comparison; numerical foundry/HIL fields use declared portable rounding.
- The Lean files certify arithmetic/parity and explicit finite matrix
  assemblies. They do not formalize the W33 incidence-Fourier rank theorem.
- v5 aggregate owns and regenerates five normalized result certificates.
- The RTL reducer snapshots completed frames and holds output under
  backpressure. A local Icarus 12.0 compile/simulation passed.
- Swabian and quTAG adapters use their actual physical-channel, overflow, and
  data-loss APIs; clean reads fail closed.
- The E8-lane witness covers all 40 points and 162 payload addresses and keeps
  the 50k random replay explicitly as smoke testing.

## External checks used

- Sastry–Sin, *The code of a regular generalized quadrangle of even order*:
  https://people.clas.ufl.edu/sin/files/the-code-of-a-regular-generalized-quadrangle-of-even-order.pdf
- Chandler–Sin–Xiang, incidence modules for finite symplectic spaces:
  https://arxiv.org/abs/math/0603100
- GAP character-table transformation contract:
  https://docs.gap-system.org/doc/ref/chap71_mj.html
- Swabian Time Tagger API:
  https://www.swabianinstruments.com/static/documentation/TimeTagger/api/TimeTaggerLibrary.html
- quTAG software manual:
  https://www.qutools.com/files/quTAG/quTAG-Softwaremanual_V1.5.0-20191212.pdf
- Lean independent checker:
  https://github.com/leanprover/lean4checker

## Verification ledger

- Pass 181–192 audit suite: **15 passed**.
- Levi v4 suite: **8 passed** (fresh aggregate/formal path included).
- Levi v5 suite: **10 passed**.
- Pass 169–180 focused regression set: **24 passed** across the full run and
  focused post-repair rerun.
- Live GAP 4.15.1: Passes 184 and 190 regenerated successfully.
- Python compilation: all modified Pass 163/170/179/181–192 witnesses passed.
- JSON: 13 modified/new certificates parse and report `PASS`.
- Public HTML: no duplicate IDs.
- Tectonic 0.15.0: `w33_paper.tex`, `photonic_holonet.tex`, and
  `holonet_practical_implications.tex` all compile to PDF. Existing typography
  warnings remain; there are no fatal errors.

## Claim tiers after audit

| tier | examples | permissible reading |
|---|---|---|
| exact finite theorem | orbit sizes, Smith data, Hom dimensions, S4/S6 actions | proved by exhaustive/integer witness |
| formal arithmetic mirror | Lean rank recurrences and finite matrices | kernel-checked at the encoded scope |
| deterministic model | hybrid optical/FPGA, foundry placement, replay | reproducible model output, not measured silicon/photonics |
| device interface | vendor adapters, RTL protocol | API/protocol tested; bench calibration and fabrication remain open |
| physics interpretation | protected memory, particles/couplings | hypothesis unless separately measured or derived |
