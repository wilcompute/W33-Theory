# Passes 1416–1420 — five-frontier exact release

## Executive result

This release executes the five requested fronts and adds one outside-the-box
correction that changes the interpretation of the signed-turn question.

1. **The two 15-dimensional modules are explicitly intertwined.**
   The previous shortcut looked in the unsigned 240-edge permutation module,
   while the signed-turn operator uses the orientation-signed edge action.
   The correct natural map is

   `F = d^T (A-12I)(A-2I) N / 16`.

   It annihilates the frame-matching image and maps the rational cokernel
   isomorphically onto `ker(K-10I)`.
2. **Exact-cover symmetry is richer than the sample suggested.**
   Stabilizers `C2` and `D8` occur in addition to `C4`, `C2xC2`, and `C4xC2`.
   Sixteen deterministic `C2` cover orbits are pairwise distinct.  Together
   with the four additional stabilizer types they give the certified lower
   bound `226800`, replacing the old time-capped `6579` bound.
3. **The two isomorphic modular 14s are geometrically separated.**
   Modulo 2, the bridge has rank 14 and square zero.  It selects the nontrivial
   reduction of the rational 15 as a canonical 14-dimensional quotient; the
   second 14 lies in the 31-dimensional torsion-side kernel.
4. **The manuscripts now have a precise claim audit.**
   `w33_paper.tex` already states the correct evidence-tiered boundary.
   `photonic_holonet.tex` still overpromotes finite theorems into a complete
   physical architecture and physical predictions.  Pass 1419 lists the exact
   language and the operational requirements for contextual fraction, magic,
   Chern measurement, and optical universality.
5. **One shared manuscript source prevents drift.**
   `BT1420_frame_signed_turn_bridge_insert.tex` contains the exact theorem and
   scope firewall.  The idempotent integrator inserts it after the table of
   contents in both root manuscripts.

## Pass 1416 — Frame-cokernel / signed-turn intertwiner theorem

Let `M` be the 540-by-240 frame cross-matching matrix, `N` the unsigned
point-edge incidence, `d` the oriented incidence, `A` the W33 adjacency, and
`K` the signed-turn operator.  The verifier proves

`K d^T = d^T(6I-A)`.

With `P=(A-12I)(A-2I)=96E_{-4}`, the integral bridge

`F=d^T P N/16`

satisfies

`F M^T=0`, `(K-10I)F=0`, and `rank_Q(F)=15`.

Therefore it descends to the explicit equivariant isomorphism

`coker(M) tensor Q -> ker(K-10I)`.

The stronger projector identities

`Fnum Fnum^T = 1536 P10num`

and

`Fnum^T Fnum = 1536 Cnum`

show that this is a scaled partial isometry between the two canonical
15-dimensional realizations.

## Pass 1417 — Exact-cover orbit frontier

Five stabilizer types have explicit cover representatives:

- `C2`, orbit size `12960`;
- `C4`, orbit size `6480`;
- `C2xC2`, orbit size `6480`;
- `D8`, orbit size `3240`;
- `C4xC2`, orbit size `3240`.

The `C2` example has twelve fixed selected frames.  This is a direct correction
to any universal reading of the earlier “diagonal stabilizer” sample.

The deterministic Algorithm-X prefix produces sixteen exact covers through one
fixed frame; their full PSp orbits are disjoint and all have stabilizer `C2`.
The resulting certified lower bound is

`16*12960 + 6480 + 6480 + 3240 + 3240 = 226800`.

The total remains open; no extrapolation is made.

## Pass 1418 — Mod-2 bridge Loewy flag

Modulo 2, define `C=N^T P N/16` and `F=d^T P N/16`.  The exact flag is

`im(F) < im(C) < im(M^T) < ker(F)`

with dimensions

`14 < 15 < 195 < 226`.

Moreover `C^2=F^2=CF=FC=0` over `F2`.  Since `F` annihilates the matching
image, it induces a rank-14 map from the 45-dimensional modular cokernel, with
31-dimensional kernel.  Combined with the certified composition factors

`1,1,1,6,8,14,14`,

this selects one 14 as the rational bridge reduction and leaves the torsion
copy in the kernel.

## Pass 1419 — Manuscript audit

The audit adopts four evidence tiers:

- exact finite theorem;
- executable engineering specification;
- experimental proposal;
- conditional physical hypothesis.

The Holonet must not identify the last three with the first.  In particular,
`4/40` is a finite deficit ratio, not automatically the resource-theoretic
contextual fraction of an empirical probability model.

## Pass 1420 — Shared promotion source

The shared TeX insert and idempotent integrator prevent `w33_paper.tex` and
`photonic_holonet.tex` from drifting on the exact result or its scope.

## Validation

- Pass 1416: 24/24 checks pass.
- Pass 1417: 16/16 checks pass.
- Pass 1418: 15/15 checks pass.
- Frozen certificates are deterministic.
- The shared TeX insert compiles in a minimal document.
- The integration helper is idempotent by unit test.

## Honest boundaries

- The exact number of covers and complete orbit census remain open.
- The mod-2 quotient is not claimed to split semisimply.
- The finite module bridge is not a physical propagator by itself.
- No finite result here proves one-photon scalable universality, experimental
  contextual fraction `1/10`, pump Chern `2`, Standard-Model parameters, or
  cosmology.
