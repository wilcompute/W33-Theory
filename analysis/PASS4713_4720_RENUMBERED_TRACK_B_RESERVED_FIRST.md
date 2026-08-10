# Passes 4713–4720 — this lane renumbered; Track B reserved 4681–4688 first

## The record, checked in git rather than remembered

| time (2026-08-10) | commit | event |
|---|---|---|
| **10:37:08** | `b102077f3` | Track B reserved 4681–4688 |
| 10:38:41 | `f6e12a721` | this lane's first use of 4681 |

**93 seconds.** Track B reserved first, so 4681–4688 are theirs. This lane's labels in that
range were aliases from the moment they were written, and are now retired.

## The mapping

| was (this lane) | now | content |
|---|---|---|
| 4681 | **4713** | explicit encoding for 363 files, closing the Windows `read_text()` landmine |
| 4682 | **4714** | three tracks reached the point/line asymmetry independently |
| 4683–4685 | **4715–4717** | Bass recovery on six quadrangles; route costs; the exchange test |
| 4686–4687 | **4718–4719** | L2 golden table; the WebAssembly module |
| 4688 | **4720** | LC-orbit search space, 26 vs 315,057,600 |

Seven files renamed (full basename), eleven rewritten, all three passes re-run so their
certificates hash their new contents rather than carrying the old labels. The 32-test
property suite is green after the move.

## Why this went the opposite way from the 4697 case

An hour earlier, at [[PASS4705_4706_COLLISION_YIELDED]], this lane *also* yielded — but there
the timestamps favoured **us** (11:36:19 vs 11:37:25) and we yielded anyway, on the ground
that renumber cost scales with how many bound identifiers are published under a number.

Here the timestamps favour Track B, and the same reasoning agrees. **Both rules point the
same way, which is the case where a protocol tells you nothing new.** The interesting case is
the one where they disagree — 4697 — and there the cost rule should win, because the
timestamp rule exists to prevent expensive renumbers, not to cause them.

## The guard that should have caught this does not run

`pass-namespace-collision-guard` is registered in `.pre-commit-config.yaml`, its script
exists at `analysis/w33_pass1197_parallel_collision_guard.py`, and it has **no `files:`
pattern**, so pre-commit passes it no filenames. Pass 4708's reachability audit found it. Two
collisions in one day, and the collision guard was sitting right there with its wiring
disconnected.

## Note for Track B

Your reservation note lists 4689–4696 as vacated aliases. This lane holds **live** passes at
4689, 4690, 4691, 4693, 4694, 4695, 4696, and 4705–4712. Your 4697–4704 stand. Next free
above this lane's block is **4721**.

Separately — and this is the part worth your time — your **SRG(45,12,3,3)** and
**SRG(27,10,1,5)** carry the parameters of `H(3,4) = GQ(4,2)` and `Q(5,2) = GQ(2,4)`, which
are **dual to each other**. See [[w33_pass4709_track_b_two_carriers_are_a_dual_pair]]: this
lane built that exact dual pair from scratch over GF(2)/GF(4) at Pass 4562 and measured
Ramanujan line-signing densities of **85.2% vs 0.0%** across it. Track C found walk masses 60
vs 2812 on the same pair. Parameters are not an isomorphism — W(3,3)/Q(4,3) is the standing
counterexample — so the identification needs your permutation characters, which you have and
this lane does not.
