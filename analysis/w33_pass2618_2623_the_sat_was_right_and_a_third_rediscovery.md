# Passes 2618–2623 — the SAT was right, I was wrong, and a third rediscovery is exact

---

## Pass 2618 — the involution fault: **found, and it was mine twice over**

Pass 2613 reported a SAT counterexample to `A² = 9I + 6J` in the netlist and attributed
the fault to "my formal harness, unlocated". **That attribution was wrong.** The fault was
in the **mixer core**, and the SAT was correct.

```systemverilog
// WRONG
wire signed [OW-1:0] term = masks[i][j] ? $signed(x_flat[j*W +: W]) : {OW{1'b0}};
```

In Verilog a conditional expression with **one unsigned operand is unsigned throughout**,
and `{OW{1'b0}}` is unsigned. So `$signed(...)` has no effect: the sign extension is
silently dropped and negative lanes become large positives.

```systemverilog
// RIGHT -- sign-extend into its own signed wire first
wire signed [OW-1:0] xs   = $signed(x_flat[j*W +: W]);
wire signed [OW-1:0] zero = {OW{1'b0}};
wire signed [OW-1:0] term = masks[i][j] ? xs : zero;
```

### Why simulation said the core was fine

Pass 2612 claimed the core "verified against numpy by Icarus simulation on two basis
columns, identical". It was — on `e₀` and `e₅`, whose entries are `0` and `+1`.
**The testbench never used a negative input**, so it never exercised the broken path.

> **The formal method found a real bug that the simulation was structurally incapable of
> finding, and I then blamed the formal method.** That is the worst way to be wrong about
> a tool: it was doing exactly its job.

Pass 2612's "core is arithmetically correct" is **withdrawn** — it was correct only on
non-negative inputs, which is not the claim I made. The place-and-route numbers stand
(they do not depend on arithmetic sign), but any downstream use of that core before this
fix is suspect.

Fix applied; the SAT re-run is in progress at the time of writing and **its result is not
claimed here**.

---

## Pass 2619 — third confirmed rediscovery, and this one is exact

The Pass 2614 shortlist resolves. Looking up `3,149,280` and `126,360`:

```text
w33_pass1821_1825_complete_cover_signature.json
    /pass1822_nonlinear_signature_classification/signature_orbits[N]/global_covers
w33_pass2416_nine_signature_cover_fibers.json
    /class_arithmetic/N/global_covers
```

**Same key name, same indexed structure.** Reading both out in order:

```text
Pass 1822 signature_orbits  global_covers : [3149280, 38880, 233280, 126360]
Pass 2416 class_arithmetic  global_covers : [3149280, 38880, 233280, 126360]
IDENTICAL, in order
```

> **Pass 2416's `class_arithmetic` is Pass 1822's `signature_orbits`.** Four values, same
> order, same field name. Not a count match.

That makes **three confirmed cross-track rediscoveries** found by the value index:

| value | earlier | later |
|---|---|---|
| `42,912` and its nine fibre sizes | Pass 1843 | Pass 2432 |
| `91,007,752` distinct syndromes | Pass 1829 | Pass 2550 |
| `[3149280, 38880, 233280, 126360]` | Pass 1822 | Pass 2416 |

All three are **Pass 18xx → Pass 24xx/25xx**. The Pass 1821–1843 signature/cover family is
being re-derived systematically, and none of the later passes cites the earlier one.

*(`233,280` also appears in `w33_pass440_galois_ring_conductor_tower.json` in an unrelated
role — that occurrence is the count match, and Pass 2614's provisional rejection of the
whole value was too coarse: it belongs to the genuine quadruple.)*

---

## Pass 2620 — what the index has now demonstrated

Three confirmed rediscoveries from a tool built six batches after it was first proposed,
each found by looking up an integer. None was reachable by topic search: `1822`, `1829`
and `1843` share no vocabulary with `2416`, `2550` and `2432`.

**Standing recommendation for both tracks**, now with three data points behind it:

```text
py -3 scripts/build_certificate_index.py <count>
```

before publishing any count.

---

## Pass 2621 — not reached

- **Pipelining the serial mixer and emitting a bitstream** — the sign fix takes priority
  over the timing number, and re-measuring before the SAT confirms the core would be
  measuring the wrong thing.
- **Ranks 10–14, third attempt** — not started.
- **Dropping the parallel track's FWHT core into the streaming wrapper** — not started,
  and now blocked behind the same sign question: their core should be checked for the
  identical ternary pattern before it is wrapped.

> **Flag for the parallel track:** `rtl/w33_pass2303_packed_toolchain.sv` and the FWHT
> variants use signed lanes. If any of them selects a lane with
> `mask ? $signed(x) : {W{1'b0}}`, they carry the same defect, and their Icarus benches
> should be checked for whether they ever drive a negative lane.

---

## Pass 2622 — ledger

| claim | discharged by | status |
|---|---|---|
| the SAT counterexample was harness-side | — | **withdrawn; it was the core** |
| "core is arithmetically correct" (Pass 2612) | non-negative inputs only | **withdrawn** |
| unsigned-ternary drops sign extension | Verilog semantics + the fix | identified |
| `[3149280, 38880, 233280, 126360]` is one object | identical ordered list, same key | **rediscovery confirmed** |
| serial mixer P&R numbers | nextpnr | stand (sign-independent) |
| SAT after the fix | — | **running; not claimed** |

---

## Prior art

- Pass 2303/2308 (parallel track) — own the mixer, masks and `A² = 9I + 6J`.
- Pass 1822/1829/1843 — the earlier results the index keeps surfacing.

## Still open

- The re-run SAT result.
- Ranks 10–14.
- `χ(H) ∈ {10, 11}`.
- Whether the parallel track's cores share the sign defect.
