# Passes 2502–2509 — the Weil halves **are** the pentagon's regular representation, and a validation gate earns its keep twice

---

## Pass 2502 — the chiral half is the pentagon's **augmentation ideal**

An order-5 element partitions the 40 points into eight pentagons (Pass 2079). Restricting
the two Weil halves to one pentagon `C₅`:

```text
degree 4 (CHIRAL,  faithful)  chi(5A) = -1   C5-multiplicities (0,1,1,1,1)
degree 5 (ACHIRAL, inflated)  chi(5A) =  0   C5-multiplicities (1,1,1,1,1)
```

> **The achiral Weil half restricted to a pentagon is the pentagon's REGULAR
> representation. The chiral half is its AUGMENTATION IDEAL — the regular representation
> with the trivial character removed.**

So the Weil parity split — even/odd under `x ↦ −x` on `𝔽₃²` — becomes, on restriction to
a pentagon, exactly **"with or without the trivial character"**. In signal terms:

```text
achiral  =  AC + DC        (keeps the pentagon's centre of mass)
chiral   =  AC only        (the zero mode is removed)
```

This makes the parallel track's Pass 2434 arithmetic transparent rather than coincidental:
the `E₈` carrier is `4 + 4bar`, so it restricts as `(0,2,2,2,2)` — two copies of the
augmentation ideal — and the 90 restricts as `18 ×` the regular representation. Hence
`dim Hom = 0·18 + 4·(2·18) = 144`, with the leading `0` being precisely the missing DC
component of the chiral side.

It also names the `C₅` obstruction geometrically: **the chiral tower has no zero mode on a
pentagon, and the achiral tower does.**

---

## Pass 2503 — the `K₈` criterion, attempted: the validation gate fired **twice**

Pass 2496 reduced `χ(H) = 9` to "does any cover's disjointness link contain `K₈`", with at
most 327 link types. Everything needed is on disk — the 327 representatives decode, and
`g++ 13.3` is available for the existing C++ workers. I built the geometry and group from
scratch with a deliberate validation gate: **reproduce the parallel track's 13,648 before
reporting anything new.**

It failed twice, and both failures were caught by the gate rather than published.

**Failure 1 — hand-written generators.**

```text
group order on frames : 192          (should be 25920)
regenerated covers    : 62,784       (should be 3,547,800)
|link(canonical)|     : 53           (should be 13,648)
```

My four guessed symplectic matrices generate a group of order 192. Had I not checked
against a known number, I would have reported a link size of 53 and a spuriously tiny
clique number.

**Failure 2 — form convention.** Replacing them with the genuine
`GeneratorsOfGroup(SP(4,3))` from GAP produced

```text
ValueError: frozenset({0, 1, 2, 3}) is not in list
```

because GAP's `SP(4,3)` preserves a **different symplectic form** than my
`x₀y₁ − x₁y₀ + x₂y₃ − x₃y₂`, so the image of a totally isotropic line under a GAP
generator is not isotropic for my form.

> **The computation is NOT done and no link number is claimed.** The remaining step is
> one careful conventions fix: either build the frame action inside GAP, where the group
> and its form agree, and export the 540-point permutations; or conjugate GAP's
> generators into my form's basis.

Recorded in full because the gate is the point. Two wrong answers were produced and
neither was published; a run without the 13,648 check would have produced a confident
number from a group of order 192.

---

## Pass 2504 — what `1/5` means: mundane, and the pentagon link is rejected

Pass 2501 asked whether the residual's uniform fractional weight `1/5` connects to the
pentagon, `C₅`, and Pass 2079's eight pentagons. It does not.

```text
frames                     540
cliques per frame            4      (240 nine-cliques x 9 / 540)
frames per edge-clique       9      (540 x 4 / 240)
after removing 4 covers    300 frames remain, 240 edge columns
   row degree                4      = cliques per frame
   column degree             5      = 9 - 4, the frames left in each clique
```

> **The `5` is `9 − 4`: nine frames per edge-clique, four consumed by the four-packing.**
> Nothing pentagonal. The `4` and `5` here are *cliques per frame* and *frames remaining*,
> not the Weil dimensions `(q²∓1)/2`.

Same numbers, different origins — a count match, and by this repo's own rule a count
match is not a link unless a map is named. **Rejected.**

Worth stating plainly because Pass 2501 proposed it as promising, and the `4 + 5` Weil
split really does appear elsewhere in this arc. Two independent `4`s and `5`s in one
project is exactly the situation that manufactures false connections.

---

## Pass 2505 — frontier completeness is now the load-bearing question

Every conditional result in this thread — the four-packing maximality, the clique-3
link, the `K₈` reduction — rests on the 327-orbit / 13,648-partner frontier being
complete, which `Pass 1533`'s quantifier audit explicitly does **not** claim:

> *"Both enumerations are finite prefixes. Agreement under branch reversal is saturation
> evidence, not an exhaustion certificate."*

> **`χ(H) = 9` is no longer the load-bearing open question. Frontier completeness is.**
> A `K₈`-free verdict over all 327 links would settle `χ(H) = 9` *given* completeness, and
> would say nothing without it.

That reframing is the most useful thing this pass produces: the effort should go to a
completeness certificate (canonical augmentation, or an exhaustive solver emitting one),
not to more packing searches.

---

## Pass 2506 — `J`, and the certificate index

- **`J` for the `W(3,3)` triple** — Pass 2498 established `BT921` names it as a gap rather
  than exhibiting it. No progress; the KO alignment (Pass 2492) remains a lead.
- **The certificate answer index** — proposed, not built. `build_topical_aliases.py`
  indexes prose tokens; certificates are prose-free, which is why seven answers sat
  invisible (Pass 2500). Extending it to index certificate *values* is the fix.

---

## Pass 2507 — ledger

| claim | discharged by | status |
|---|---|---|
| achiral half = `C₅` regular representation | `χ(5A) = 0` | proved |
| chiral half = `C₅` augmentation ideal | `χ(5A) = −1` | proved |
| this explains the 144 | multiplicity arithmetic | proved |
| `K₈` criterion | Pass 2496 pigeonhole | proved |
| any link clique number | — | **not computed; gate fired twice** |
| `1/5` is pentagonal | — | **rejected as a count match** |
| frontier completeness | — | **open, and load-bearing** |
| `J` for the triple | — | open |
| certificate answer index | — | proposed, not built |

---

## Prior art

- Pass 2434 (parallel track) — the `C₅` Hom space this explains.
- Pass 2079 (mine) — the eight pentagons.
- `pass1510`–`pass1515`, `pass1533` — the frontier, its numbers, and its quantifier audit.
- Passes 353/355 — the `q ≡ 3 (mod 4)` chirality reading, cited not re-derived.

## Still open

- Frontier completeness — now the load-bearing question.
- The 327 link clique numbers, after the conventions fix.
- `J` for the `W(3,3)` spectral triple.
- Five certificates, at least two causes.
