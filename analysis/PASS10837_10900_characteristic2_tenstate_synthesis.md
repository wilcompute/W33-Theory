# Pass10837–10900 — characteristic-2 defect and ten-state bridge synthesis

This packet closes the order-two normalizer defect as modular extension data and isolates the surviving Hall–Janko ten-state projective-line bridge.

## 10837–10844 — the D26 defect is 32 missing nonsplit extensions
On the 316-dimensional C13-fixed sector,

- `F2[V2] = 1^64 + J2^126`,
- `H1(Levi H4) = J2^158`.

The nontrivial `W12^315` C13-sector already has the unique compatible semilinear D26 extension. Hence the entire order-two obstruction is confined to the fixed sector. The minimal stable repair is

`F2[V2] + J2^32 ~= H1 + 1^64`.

## 10845–10852 — Wilson C6 has a PG(2,4) fixed cone
For the explicit order-six complement `n`, write `n=su` with `s=n^4` of order3 and `u=n^3` of order2. On `F4^6`,

`n ~ J2(1) + J2(w) + J2(w^2)`.

Thus `Fix(u)=F4^3`, projectivizing to `PG(2,4)`. The unique `s`-fixed F4 line gives three scalar-equivalent translations, each pairing the 64 fixed vectors into 32 pairs.

## 10853–10860 — fixed H(4) geometry is an affine-frame tree
The 2B-fixed H(4) Levi subgraph has 21 points, 25 lines and 45 flags and is a tree. Inside `PG(2,4)` it selects one origin and one line at infinity. The five non-leaf H(4) lines are precisely the five radial projective lines through the origin; four extra H(4) leaves hang from every direction at infinity.

## 10861–10868 — local pairing works, global translation repair fails
The 64 fixed states admit one scalar-gauge class of C3-compatible perfect matchings, but no nonzero translation survives the irreducible C13 action. Therefore a translation-type intrinsic repair cannot extend globally through the C13 clock.

## 10869–10876 — HJ C13:C12 gives a ten-state carrier
On the 32 C13 cycles of the 416-point Hall–Janko controller, the full C12 complement has cycle profile

`1^1 3^1 4^1 6^2 12^1`.

Quotienting by the inner C6 gives 10 states. The residual outer C2 acts as `1^2 2^4`.

## 10877–10884 — the ten-state outer bit is split-projective on P1(F9)
On `P1(F9)`, field Frobenius has profile `1^4 2^3`, so it is ruled out. The split projective involution `z -> -z` has exactly `1^2 2^4`, fixes `0, infinity`, and has centralizer `D16` in `PGL2(9)`. Its six-state quotient is

`{0,infinity} disjoint-union F9^x/{+/-1} = 2 poles + C4`.

This matches the six full Hall–Janko normalizer orbits at the C2-set level. No C4/cross-ratio transporter is claimed yet.

## 10885–10892 — Tate/Ext meaning of 32 and 64
In characteristic two,

`F2[C2] ~= F2[e]/(e^2)`

and `Ext^1(1,1)=F2`. The unique nonzero extension is `J2`. Therefore the defect is exactly 32 copies of the unique nonsplit self-extension

`0 -> 1 -> J2 -> 1 -> 0`.

Tate cohomology gives the stable shadow:

- `Hhat^n(C2,1)=F2` for every degree,
- `Hhat^n(C2,J2)=0` because J2 is projective.

Hence the V2 fixed sector carries 64 Tate classes and H1 carries none. The identity `64=2*32` is structural: each missing J2 consumes two split trivial composition factors and annihilates their stable/Tate obstruction.

## Frontier after Pass10900
The raw 32-count bridges are dead: neither Hall–Janko 32 cycles nor local translation pairings realize the global extension defect. The positive surviving objects are instead:

1. the `PG(2,4)` affine-frame fixed geometry of the characteristic-2 normalizer;
2. the six-state `2 poles + C4` quotient of the Hall–Janko/P1(F9) ten-state carrier;
3. the modular extension class itself, which requires a non-translation or external chain-level realization.

The next packet should therefore test objectwise projective-line structure on HJ10, compare the local 32-pair quotient with the HJ32 normalizer action, and search for an external 32-extension carrier rather than forcing an intrinsic translation model.
