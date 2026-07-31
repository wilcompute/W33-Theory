# Passes 1485–1489 — the 36 involutions are the spreads, the degree-90 is invisible to permutation modules, and my own guard was noise

Five items. Two complete the `PGSp` picture of the signed edge module; one is a
measurement that condemns a guard I added and celebrated eleven passes ago.

---

## Pass 1485 (physics) — the size-36 outer class is the 36 spreads

Pass 1481 found six outer classes separating the two Steinberg extensions, with
the **largest** separation (`χ = 9` vs `−9`) on an involution class of size 36.
What that class is:

```text
size-36 involution : centraliser order 1440 = |PGSp|/36
                     fixes  0 of the 40 points
                     fixes 10 of the 40 lines
                     INNER? false
W(3,3) has 36 spreads; spread stabiliser order = 51840/36 = 1440
```

A **spread** of `W(3,3)` is exactly 10 pairwise disjoint lines covering all 40
points. This involution fixes ten lines and no points, and its centraliser has
precisely the spread stabiliser's order.

> **The 36 outer involutions are in bijection with the 36 spreads**, exactly as
> BT773's 540 outer involutions are in bijection with the 540 frames.

So both classes that detect the Steinberg's sign are geometric objects of
`W(3,3)`:

| class | size | geometric object | separation |
|---|---|---|---|
| involutions | 540 | **frames** (BT773) | `∓3` |
| involutions | 36 | **spreads** | `∓9` — the maximum |

The physical sector's chirality is read by the frames and, most strongly, by the
spreads. Neither is an auxiliary construction; both are the substrate's own
combinatorial objects.

---

## Pass 1486 — the degree-90 is invisible to every permutation module

Pass 1480 ruled out transitive 90-sets. Checking every maximal subgroup of
`PGSp(4,3)`:

```text
maximal index  2 (order 25920) : 90-multiplicity = 0
maximal index 27 (order  1920) : 0
maximal index 36 (order  1440) : 0
maximal index 40 (order  1296) : 0
maximal index 40 (order  1296) : 0
maximal index 45 (order  1152) : 0
```

**The degree-90 occurs in no primitive permutation module at all.** And Pass 1487
says where it does live — which explains the zero.

---

## Pass 1487 — the coexact block over `PGSp` is `30 ⊕ 90`, as predicted

If the two degree-45s fuse, the constraint block must read `30 + 90` over the
full group. Tested:

```text
dim coexact                       : 120
COEXACT over PGSp                 : [30 (#15), 90 (#25)]
is it 30 + 90 as predicted?       : TRUE
```

**Confirmed.** So the complete picture over the full group:

```text
signed 240-edge module over PGSp(4,3)
  =  15  (+) 24        gauge       39
  +  81                physical    81
  +  30  (+) 90        constraint 120
  =  240,  FIVE irreducibles, multiplicity-free
```

versus **six** over `PSp(4,3)` (`15, 24, 30, 45, 45, 81`). The fusion
`45 ⊕ 45 → 90` is the only change, and every block is `PGSp`-invariant with a
definite extension chosen.

**And the degree-90's absence from permutation modules is now explained**: it
lives in the *orientation-signed* module. A permutation module cannot see a sign,
so no amount of searching permutation carriers could ever have found it. That
also retro-justifies Pass 1476's negative — the 90 hyperbolic lines were never a
candidate, for a structural reason rather than an arithmetic accident.

---

## Pass 1488 — my own guard is noise, measured

`group_tokens` was added in Pass 1378 and credited with catching
BT781 → BT782, the case that had cost a rediscovery. Re-measuring flag rates over
the 27 pass witnesses, against Pass 328's calibration (~78% = noise, ~20% =
signal):

```text
results_in (all)   63.0%
  noun_number      18.5%
  compounds        22.2%
  group_tokens     81.5%   <- NOISE by this project's own standard
  edge_action      37.0%
```

**81.5%.** Group notation is ubiquitous here — every pass names groups — so the
class flags nearly everything. The one real catch did not make it a good class;
it made it a lucky one.

---

## Pass 1489 — the rarity cut, calibrated against the pinned case

The fix is a rarity cut, and the threshold is *derived*, not chosen:

```text
cut    flag rate   BT781->BT782 shared
 20      22.2%          1    MISSES the motivating case
 25      22.2%          2    FIRES     <- minimum cut that works
 40      37.0%          2    FIRES
none     81.5%          3    FIRES     <- noise
```

`grp:2^4:3` occurs in 25 files, so a cut of 20 kills the very case the class
exists for while a cut of 25 keeps it — and 25 lands exactly in the signal band.
Frequencies come from the persistent corpus index; if it is absent the cut is
skipped rather than guessed.

```text
self-test        : 5/5 PASS (BT810/BT811 back to its original 2 tokens)
sweep candidates : 17 -> 9
```

Note the self-test now reports `polar-pair@4, polar-pair@40` — the *original*
Pass 1120 pinned pair — because the common group tokens that had been inflating
it are filtered. The case is being caught for the right reason again.

**The general point**, and it is the third time this session: a guard that
catches one real case has demonstrated nothing about its rate. Pass 328 knew
that and measured; I added a class on the strength of a single catch and did not
re-measure for eleven passes.

---

## Pass 1490 — the resolution SAT

Still running (4,860 variables, 99,909 clauses). Undecided, and reported as
running.

## Prior art

- [BT773](analysis/BT773_involution_cube_theorem.md) — **owns** the 540 ↔ frames bijection this pass parallels for the 36.
- [Pass 328](analysis/w33_pass328_token_calibration.py) / Pass 1107 — **own** the flag-rate calibration Pass 1488 applies to my own class.
- [Pass 1481](analysis/w33_pass1480_1484_the_sign_lives_on_the_540.md) — the separating classes identified here.
