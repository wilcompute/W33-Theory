# Passes 2476–2481 — what the 144 **is**, a correction to my own Pass 2467, and a hook that had to be calibrated twice

---

## Pass 2477 — correction: the `E₈` carrier **does** have invariant forms

Pass 2467 said the chiral carrier "has no invariant bilinear form at all" at `q = 3`.
That is true of each degree-4 **constituent** and false if read as a statement about the
carrier.

```text
one degree-4 constituent
    <chi, chi-bar>       = 0        no invariant bilinear form
    dim (Sym^2)^G        = 0
    dim (Lambda^2)^G     = 0

the E8 carrier = 4 + 4bar, degree 8
    self-dual ?            TRUE
    <chi, chi-bar>       = 2        TWO dimensions of invariant bilinear forms
    dim (Sym^2)^G        = 1        <- a SYMMETRIC invariant form exists
    dim (Lambda^2)^G     = 1
```

> **The 8-dimensional carrier carries one symmetric and one alternating invariant form.
> They pair `4` against `4bar` rather than each constituent with itself.**

That is exactly what "complex" means, and the symmetric one is the real `E₈` lattice
form — which is why the parallel track can speak of a *real* `E₈` carrier at all. The
Pass 2467 conclusion about the constituents stands; the sentence as written overreached
by one level, and this pass withdraws that reading.

The Pass 2467 point that survives: **each chiral constituent is not self-dual at
`q ≡ 3 (mod 4)`**, while at `q ≡ 1 (mod 4)` each constituent *is* self-dual with an
alternating form. That distinction is real; the claim that the carrier has no form was
not.

---

## Pass 2476 — the 144 is `36 ×` one irreducible

Pass 2468 proved the 144 cannot be cut by the normaliser. So describe it instead.

On `Hom(E₈, 90) = E₈* ⊗ 90` the central `z` acts as `(−1)·(+1) = −1`, so the 144 is a
module for `N = C₅:C₈` with `z` acting as `−I`.

```text
|N| = 40    structure  C5 : C8
Irr(N) degrees                : [1,1,1,1,1,1,1,1,4,4]
  with z -> -I (faithful on the centre) : [1,1,1,1,4]
  with z -> +I                          : [1,1,1,1,4]
```

The four linear characters with `z → −I` are trivial on `C₅`, and the 144 has no
`C₅`-trivial part (its `C₅`-multiplicities are `(0, 36, 36, 36, 36)`). So the 144 is
built entirely from the **unique 4-dimensional irreducible of `C₅:C₈` with `z → −I`**:

> **`144 = 36 × (the unique faithful 4-dimensional irreducible of C₅:C₈)`.**

Structurally that is `4` blocks of `2 × 18 = 36`, with `C₈` permuting the four
`C₅`-isotypic blocks cyclically through `C₈ ↠ C₄ = Aut(C₅)` and `z` acting as `−1`
inside each.

**Consequence, and it re-proves Pass 2468 from the module side:** a module built only
from characters with `z → −I` contains **no trivial summand**, hence no `N`-invariant
vector, hence no equivariant map survives. The obstruction is visible in the module
decomposition without any subgroup search.

---

## Pass 2478 — a certificate hook, and the two calibrations it needed

The sweep of Pass 2469 caught a real defect once (the Pass 2304 stale hash), so it
belongs in `pre-commit` next to `check_rediscovery.py`. Turning it into a hook exposed
two problems, both worth recording because both are the same class of mistake.

**First calibration — the crash.** Matching any key containing `sha256` and slicing it
as a string crashes on certificates that store a *dict* under such a key. Fixed by
requiring a 64-character hex string.

**Second calibration — the noise, which is the important one.** Even after that fix:

```text
matching "sha256" anywhere in the key name:
    289 certificates with a hash    144 verify    145 MISMATCH    -> 50% flag rate
```

A 50% flag rate is not a finding, it is noise — precisely the failure
`check_rediscovery.py` was calibrated away from (CLAUDE.md: bare integers flag 97% of
files). Measuring every `sha256`-named key across all of `data/`:

```text
key name                     verify / mismatch     verdict
sha256_without_hash_field       91 /   6           canonical  KEEP
sha256                          33 /   1           canonical  KEEP
universe_sha256                  1 /   0           canonical  KEEP
certificate_sha256              27 /  84           different convention  EXCLUDE
genome_ / matrix_ / tensor_ /    0 /  many         hashes of INPUTS      EXCLUDE
  source_ / schedule_ / ...
```

Most `sha256`-named keys hash an **input artifact**, not the certificate. Restricting to
the three canonical names:

```text
132 certificates with a hash    125 verify    7 flag    -> 5.3% flag rate
```

Actionable. Wired into `.pre-commit-config.yaml` as `certificate-digests`, `--quiet`,
**warns and never blocks** — a blocking hook trains `--no-verify`, and a stale hash is a
candidate for review, not proof of error.

### What it flags first is mine

```text
w33_pass1867_1871_outer_doily_transfer_clock.json
w33_pass1872_1876_five_frontiers.json
w33_pass1887_exact_global_weight5_decoder.json
w33_pass1891_tutte_coxeter_voltage_carrier_lift.json
w33_pass2011_2015_five_frontiers.json
w33_pass2012_d8_orbit_parallel_class_witness.json
holonet_uor_shacl_export.json
```

Six of the seven are **my own** certificates, from the 1867–2015 range. `2011_2015` is
almost certainly stale from the numbering collision I had to renumber out of. The hook's
first catch is not the other track's work; it is mine. Left flagged rather than
silently repaired, since repairing a digest without re-deriving the object is how a
stale certificate becomes an invisible one.

---

## Pass 2480 — the demonstrator bitstream exists

```text
yowasp-icepack mod.asc mod.bin
104,090 bytes
sha256 d9c8f131e560e2c76aa4d9312b37323439b334ae5590d7da2b7880cd477ee78a
```

The chirality modulator now has a **loadable iCE40 UP5K bitstream**, downstream of the
Pass 2457 SAT proof and the Pass 2464 place-and-route at 93.40 MHz. Together with the
three fibre controllers (9 + 8 + 4 cells), the whole chirality result occupies 94 of
5280 logic cells.

**Scope:** a bitstream is not a demonstration. Nothing has been loaded onto hardware, and
no measurement has been taken. What exists is a proved, routed, packed image.

---

## Pass 2479 — the Burnside route to the cover orbit count, stated

```text
|Orbits| = (1/|G|) * SUM over conjugacy classes c of |c| * |Fix(rep_c)|
|Fix(g)| = exact covers that are UNIONS OF g-ORBITS on frames
```

`|G| = 51840` has 25 conjugacy classes, so this is **25 bounded searches**, not one
enumeration of 477 million nodes. `|Fix(1)| = 3,547,800` is known and contributes
`68.4375`; the other 24 classes must supply the fractional part.

This is exactly the shape of the parallel track's Pass 2050 computation (exact covers
from whole frame orbits), run once per class representative instead of once per subgroup.
**The only missing input is the frame graph `H` itself — not the 47 MB frozen binary.**

**Not executed this pass.** Recorded as a concrete bounded route, because it is the one
computation that would settle `73` outright.

---

## Pass 2481 — ledger

| claim | discharged by | status |
|---|---|---|
| `144 = 36 ×` the faithful 4-dim of `C₅:C₈` | `Irr(N)` degrees + `C₅`-multiplicities | proved |
| no `N`-invariant vector in the 144 | no trivial summand with `z → −I` | proved |
| `E₈` carrier has 1 symmetric + 1 alternating form | `Sym²`/`Λ²` invariants | computed |
| Pass 2467 "no form at all" | — | **withdrawn** (true of constituents only) |
| hook flag rate 5.3% after calibration | measured over all of `data/` | measured |
| 7 certificates flagged, 6 of them mine | the hook | **open, not repaired** |
| bitstream packs | `yowasp-icepack` | built |
| Burnside orbit count | — | **not executed** |

---

## Prior art

- Pass 2434 (parallel track) — owns the `C₅` restriction and the 144.
- Pass 2050 (parallel track) — the orbit-cover computation the Burnside route reuses.
- `scripts/check_rediscovery.py` — the calibration policy this hook copies.
- Passes 2466–2472 (mine) — the normaliser and lift results this builds on.

## Still open

- The 7 flagged certificates, six of them mine.
- The `G`-orbit count on covers, which settles `73`.
- `χ(H) = 9`.
