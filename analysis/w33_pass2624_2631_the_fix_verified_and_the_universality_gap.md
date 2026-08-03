# Passes 2624–2631 — the sign fix verified, and where my hardware sits in the repo's quantum architecture

---

## Pass 2626 — the fix verified, and the bug measured

A testbench that drives **negative** lanes, which the Pass 2612 bench never did:

```text
fixed core   : 14,076 lane checks,      0 errors   PASS  A^2 = 9I + 6J on signed inputs
pre-fix core : 14,076 lane checks, 12,780 errors   FAIL
```

> **The unsigned-ternary bug corrupted 91% of signed lane checks**, and the original
> two-column bench passed anyway because both columns were non-negative.

The new bench sweeps all 36 negative basis vectors, all 36 positive ones, the all-minus-one
extreme, 18 mean-zero pairs (where `A/3` must be an involution), and 300 random vectors in
`[−3,3]`. It is committed as `tests/rtl/w33_pass2626_signed_mixer_tb.sv` and reproduces
the failure against the pre-fix core on demand — so the regression cannot silently return.

The Yosys SAT re-run is still executing at the time of writing; **its result is not
claimed**. Simulation now covers 14,076 lane checks including every sign pattern the bug
touched, which is the evidence this pass rests on.

**Audit of my other RTL:** the chirality modulator, Fibonacci datapath and fibre
controllers were grepped for the same `cond ? $signed(x) : {W{1'b0}}` pattern. **None
carries it.** The parallel track's `w33_pass2303_packed_toolchain.sv` uses a
`function [35:0] mask` with a case statement and is likewise clean.

---

## Pass 2628 — where my hardware sits in the repo's quantum architecture

The user asked what quantum-computing material already exists. A survey found **3,844
occurrences across 669 files** — this is a large pre-existing layer, not a gap. The
load-bearing claims:

```text
"universality scaffold: exact qutrit Clifford processor, exact tetrahedral control bus"
"universality boundary before any full braiding claim"
GKP lattices, GKP+surface threshold, "GKP photonic demonstrator should cross FT near 8-9 dB"
```

and from the corpus memory: the logical layer is substrate-forced with **code = GKP tower
`A₂ < D₄ < E₈`** and **gates = degree-2 symplectic + degree-3 `E₆` cubic = Lloyd–Braunstein
universal**; Clifford alone is in `P`, Clifford + cubic is `BQP`.

Mapping what I have built onto that:

| architecture layer | status | built by |
|---|---|---|
| interconnect / symplectic (degree 2) | **routable RTL**, 4048 LC, 19.65 MHz, 21 pins | Pass 2612 |
| phase controller `μ₄`/`μ₆` | **routed + bitstream**, 73 LC, 93.40 MHz | Pass 2457/2464 |
| chirality select / fibre `C₆`, `S₃` | routed, 9 / 8 / 4 LC | Pass 2438/2470 |
| **degree-3 `E₆` cubic gate** | **nothing** | — |

> **Everything I have built is the Clifford/symplectic half. The degree-3 cubic — the
> part that takes the machine from `P` to `BQP` — has no RTL at all.**

### The observation worth acting on

The parallel track's Pass 2554 found that for the faithful 4-dimensional module of the
nonsplit `5:8`, **`dim Cov₃(V,V) = 4`** — four independent **cubic** equivariant self-maps
survive even though no invariant linear map does. They framed this as "a nonlinear escape
channel" past the `Hom = 0` obstruction.

> **Those four cubic covariants are exactly the degree-3 object the universality scaffold
> is missing**, and I have the toolchain to synthesise one.

**Scope, and it is a real one.** This is an identification by *degree and equivariance*,
not a proof that any of those four is the `E₆` cubic the Lloyd–Braunstein argument needs.
Their own caveat applies: these are `5:8`-module covariants, not full `PSp(4,3)`-equivariant
carrier couplings. Recorded as **the best-posed hardware target on the board**, not as a
result.

---

## Pass 2629 — the other items

- **Pass 1822** — located and its `signature_orbits` confirmed identical to Pass 2416's
  `class_arithmetic` (Pass 2619). Not read end to end; the three rediscoveries all trace
  to the 1821–1843 family and someone should read that family properly.
- **Ranks 10–14** — third attempt not made.
- **Pipelining the serial mixer** — deliberately deferred until the SAT confirms the
  fixed core; re-measuring timing on an unverified datapath measures the wrong thing.

---

## Pass 2630 — ledger

| claim | discharged by | status |
|---|---|---|
| sign fix is correct | 14,076 signed lane checks, 0 errors | verified |
| the bug affected 91% of signed checks | pre-fix core, 12,780 mismatches | measured |
| my other RTL is clean | pattern grep | verified |
| their `pass2303` core is clean | uses a case function | verified |
| SAT after the fix | — | **running, not claimed** |
| cubic covariants are the missing gate | degree + equivariance only | **target, not result** |
| ranks 10–14 | — | not attempted |

---

## Prior art

- Pass 2554 (parallel track) — **owns** the four cubic `5:8` covariants.
- Pass 2303/2308 (parallel track) — own the mixer and its masks.
- The GKP tower, Lloyd–Braunstein universality and the qutrit Clifford scaffold are
  pre-existing corpus results, cited not claimed.

## Still open

- The re-run SAT.
- An RTL cubic gate — the first thing that would move the machine past Clifford.
- Ranks 10–14, `χ(H) ∈ {10,11}`, and the 1821–1843 family read.
