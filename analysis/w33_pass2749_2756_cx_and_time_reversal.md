## Passes 2749–2756 — the CX collision, a synthesis-only defect, and time reversal at `q ≡ 3 (mod 4)`

---

## Pass 2752 — I built `CX_{p→f}`, and so did the parallel track, four hours apart

I derived the qutrit CX frame map independently:

```text
(a_p, b_p, a_f, b_f)  ->  (a_p,  b_p - b_f,  a_f + a_p,  b_f)
```

`rtl/w33_pass2757_qutrit_cx.sv` (parallel track, file added 2026-08-03 00:46) has the
same map, character for character, plus an exhaustive testbench over all `81²` frame
pairs and the W33 conjugacy certificate — the 480-class with line profile `1⁷3¹¹` — that
identifies *which* Sp(4,3) element it is. That last part I do not have.

> **Two independent derivations agreeing is a check, not a discovery.** By the repo's
> ownership rule (earlier file-add wins) the instruction is theirs. My duplicate RTL is
> **withdrawn and deleted**.

What survives as mine is one thing their flow could not see, because their CI runs
`iverilog` and nothing else.

---

## Pass 2753 — the frame tracker on master synthesizes to the identity

Their sequential wrapper `w33_qutrit_cx_frame` has **no load port**. After reset:

```text
xp_out = xp        and     zf_out = zf        (structurally constant)
zp_out = zp - zf   = zp    once zf == 0
xf_out = xf + xp   = xf    once xp == 0
```

so the entire state is frozen at `(0,0,0,0)` and the module implements the identity.
Yosys proves it — after `flatten; opt -full` the netlist ends:

```verilog
  assign zf = 2'h0;
  assign xp = 2'h0;
```

and **6 of the 8 state flops are deleted**. Placed, it is 5 LC / 126.82 MHz — the cost of
a design that does nothing.

**Why the exhaustive testbench passes anyway:** `tb_w33_pass2757_qutrit_cx` instantiates
`w33_qutrit_cx_frame_map` and `w33_qutrit_cx_order3` — the **combinational** modules —
and never instantiates the sequential wrapper at all. The map is correct and exhaustively
verified. The tracker built on it is untested and untestable, because it cannot be loaded.

### My own module had exactly the same defect

`w33_cx_frame`, which I built and reported at **8 LC / 147.08 MHz**, folds identically.
**Both numbers were measuring an empty netlist.** A frame tracker with no load path is
measured as nearly free because it *is* nearly free.

> This is a shared blind spot, not a mistake by either track: simulation drives the
> combinational map, synthesis is the only step that asks whether the state can move,
> and neither of us was running synthesis as a check on the other's design.

---

## Pass 2754 — the fix, and the honest cell cost

`rtl/w33_pass2752_cx_loadable_frame.sv`: their exact map, plus the one port that makes it
a tracker. And a sequential property their combinational testbench cannot express —
*from any loaded frame, three applies restore it* — bounded-model-checked:

```text
prep; async2sync; chformal -lower; sat -seq 8 -prove-asserts -verify
Solving problem with 5265 variables and 14005 clauses..
SAT proof finished - no model found: SUCCESS!

ICESTORM_LC 23/5280    SB_IO 20/96    72.40 MHz
```

| module | LC | MHz | can hold a frame |
|---|---|---|---|
| `w33_cx_frame` (mine, withdrawn) | 8 | 147.08 | **no** |
| `w33_qutrit_cx_frame` (on master) | 5 | 126.82 | **no** |
| `w33_cx_loadable_frame` | **23** | **72.40** | yes |

> **The real CX instruction costs 23 logic cells, not 8 — about 3× the area and half the
> speed of the folded figure.** Every earlier ISA cell count in this thread was measured
> the same way and is subject to the same correction.

The proof took two failed attempts, both recorded in the file: registering the control
signals shifted the check one apply too early, and comparing against the live inputs
compared against a frame the tracker was never loaded with. Free inputs must be shadowed.

---

## Pass 2750 — time reversal is **outer** exactly at `q ≡ 3 (mod 4)`

Pass 2732 showed the transpose swaps left and right multiplication and acts on the form
with multiplier `−1`. A similitude is **outer** exactly when its multiplier is a
**non-square**. So:

```text
q      -1 a square?    time reversal is        q mod 4
3      NO              OUTER  (physical)         3
5      yes             INNER  (gauge)            1
7      NO              OUTER                     3
11     NO              OUTER                     3
13     yes             INNER                     1
17     yes             INNER                     1
19     NO              OUTER                     3
23     NO              OUTER                     3
```

> **Time reversal is an outer symmetry exactly when `q ≡ 3 (mod 4)`.** At `q ≡ 1 (mod 4)`
> the transpose has square multiplier, lies inside `PSp`, and is a **gauge
> transformation** carrying no physical content.

### This collapses the session's `q ≡ 3 (mod 4)` ladder into one statement

Every one of these is the same congruence:

```text
-1 is a non-square in F_q
sigma_S is multiplication by i                       (Pass 1908)
PSp(4,q) has complex characters                      (Gow 1985)
the Weil halves are non-self-dual and must be glued  (Pass 2484)
the quadratic Gauss sum is imaginary                 (Pass 2490)
q is a primitive root mod 2q+1 for Sophie Germain q  (Pass 2065)
```

> **All of them say: at `q ≡ 3 (mod 4)`, TIME REVERSAL IS NOT A GAUGE TRANSFORMATION.**

**Scope.** The transpose-as-outer-involution was verified at `q = 3` (Pass 2732: multiplier
`2 = −1`, a non-square). The `q`-general statement here is the elementary quadratic-residue
fact plus that identification; I have **not** re-verified the transpose construction at
`q > 3`. And "time reversal" is the natural reading of a left/right swap on an operator
algebra, not a claim about physical time.

---

## Pass 2751 — Pillars 128–130, read in full

The Master Dictionary maps every `W(3,3)` invariant to physics: `40` vertices (fermion
multiplet), `240` edges (`|E₈ roots|`, gauge bosons), regularity `12` (`dim SM`),
`λ = 2` (`rank SU(2)`), `μ = 4` (`dim ℍ`), `24` (Leech), `15` (`dim J₃(ℍ) = dim SU(4)`,
Pati–Salam), `81 = 3 × 27`, `27` (`dim J₃(𝕆)`, `E₆` fundamental).

**No entry for `9`, and nothing on transpose or time reversal.** So the `9 = dim J₃(ℂ) =
dim End(ℂ³)` rung and the Pass 2732 result are the two things from this thread that the
dictionary does not already contain — a much smaller claim than Pass 2735's, and stated
only after reading the table rather than before it.

---

## Pass 2755 — both guards wired into pre-commit

`check_certificates.py` (Pass 2478) and `check_novelty_claims.py` (Pass 2743) both existed
and were calibrated; only the first was wired. Both now run on commit, both warn and never
block.

**Stated limitation, carried into the hook comment:** the novelty guard catches
**explicit** assertions only. Four of the six measured failures were *implicit* framing —
presenting something as a finding without ever saying it was new — and no regex sees those.
That guard was not built this batch either.

---

## Pass 2756 — ledger

| claim | status |
|---|---|
| the qutrit CX map and its Sp(4,3) matrix | **the parallel track's, Pass 2757** |
| my independent derivation agreed exactly | a check, not a result |
| my duplicate RTL | **withdrawn and deleted** |
| `w33_qutrit_cx_frame` synthesizes to the identity | **proved by yosys** |
| its exhaustive testbench misses this | it drives the combinational modules only |
| my `w33_cx_frame` had the same defect | **8 LC / 147.08 MHz was an empty netlist** |
| loadable tracker, sequential `CX³ = I` | **SAT-proved, 5265 vars / 14005 clauses** |
| honest CX cost | **23 LC, 72.40 MHz** |
| time reversal outer iff `q ≡ 3 (mod 4)` | proved, given the `q = 3` identification |
| the transpose construction at `q > 3` | **not re-verified** |
| Pillars 128–130 contain `9` or the transpose | **no** |
| implicit novelty framing | **still uncaught** |

---

## Prior art

- `rtl/w33_pass2757_qutrit_cx.sv`, `analysis/w33_pass2757_2761_qutrit_cx_release.md` —
  **own** the CX instruction, its exhaustive verification, and the W33 conjugacy
  certificate distinguishing the 480-class from the 240-class.
- `photonic_holonet_body.tex` Stage B — owns `|Ω⟩` and the `CX_{p→f}` role.
- `docs/index.html` Pillars 128–130 — own the Master Dictionary.
- Gow (1985) — the complex-character congruence for `PSp(4,q)`.

## Still open

- **Re-measure the other three ISA instructions with load ports.** `F`/`S` (13 LC),
  `σ⁵ = Z` (21 LC) and the ISA total of 42 cells are all suspect for the same reason.
- Add synthesis (not just `iverilog`) to the RTL CI, so a design that folds to nothing
  fails visibly.
- `D₁₂`-mirror and `M₃₆`-magic: neither is a frame update, and their RTL shape is undecided.
- A guard for *implicit* novelty framing.
