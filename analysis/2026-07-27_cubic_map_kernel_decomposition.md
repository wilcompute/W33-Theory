# Step 4 — Complete Irreducible Decomposition of the Cubic-Map Kernel

**Date:** 2026-07-27  
**Status:** COMPLETE

Let `M` be the 2240-dimensional permutation module on E8 A2 root triples and let
`L_cubic:M→C[45]` be the equivariant lift-to-cubic-support map. The exact incidence
calculation gives rank 45, so `dim ker L_cubic=2195`.

## Image module

The 45 E6 cubic supports have permutation character decomposing as

`C[45]=1+20+24`.

Independently, their disjointness graph is `SRG(45,32,22,24)` with spectrum
`32^1,2^24,(-4)^20`, producing the same `1+24+20` packet.

## Kernel module

The exact 2240-carrier decomposition is

`14*1 + 16*6 + 5*15 + 4*15a + 22*20 + 3*24 + 9*30 + 4*60a + 10*64 + 3*81_minus + 1*90`.

Subtracting the image gives

`ker L_cubic = 13*1 + 16*6 + 5*15 + 4*15a + 21*20 + 2*24 + 9*30 + 4*60a + 10*64 + 3*81_minus + 1*90`.

The degree reconstruction is 2195 exactly. In particular,

`3*81_minus ⊂ ker L_cubic`.

Thus the direct Steinberg-to-unsigned-cubic-support bridge is representation-
theoretically obstructed, not merely absent from the current construction.

The previous heuristic `1952=7*276+20` does not describe the irreducible
kernel and is superseded. Pass 1147 now gives the number `1952` its correct
object-level meaning: augment the cubic map by the three explicit rank-81
Schläfli-edge/Steinberg transforms on the three A2-color fibres. The resulting
rank is `45+3*81=288`, so its kernel is `2240-288=1952`, with exact
decomposition obtained by deleting `3*81_minus` from the display above:

`13*1 + 16*6 + 5*15 + 4*15a + 21*20 + 2*24 + 9*30 + 4*60a + 10*64 + 1*90`.

This is not a realization of `7*Lambda^2(24)+20`; it is a different, explicit
equivariant kernel.

## Certificate

- verifier: `analysis/w33_pass1135_cubic_kernel_decomposition.py`
- result: `data/w33_pass1135_cubic_kernel_decomposition.json`
- status: PASS
