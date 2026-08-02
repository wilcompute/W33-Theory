# Passes 2496–2501 — `χ(H)=9` reduces to a `K₈` test, and the Gauss sum closes the arc

---

## Pass 2496 — the `K₈` criterion: `χ(H)=9` reduced to 327 clique computations

`data/w33_pass1511_1515_cover_resolution_frontiers.json` is far stronger than I credited
in Pass 2489, and its own theorems are exact:

```text
1512  every one of the 327 frozen PSp(4,3) cover orbit types contains a cover
      disjoint from the canonical cover
1513  the 13648 known disjoint partners form a graph with 188338 edges and 494
      triangles but NO K4.  Hence the largest packing containing the canonical
      cover, inside the certified frontier, has FOUR covers.
1515  removing the selected four covers leaves a 300-row, 240-column, 4-uniform,
      5-regular residual.  Uniform weight 1/5 is a fractional exact cover of total
      weight 60, but exhaustive Algorithm X proves there is NO INTEGRAL exact
      cover -- the four-packing has no fifth layer.
```

Pass 1515 is an **integrality gap**: the residual is fractionally solvable and integrally
infeasible. That is a real obstruction, not a search failure.

The file's boundary is scrupulous and I do not sharpen it:

> *"Neither statement proves that four is the global packing number over undiscovered
> cover orbits or over different four-packings."*

**What this pass adds is the reduction.** A 9-colouring is 9 pairwise disjoint covers.
Fix any one of them; the other eight are pairwise disjoint and all disjoint from it — so
they form a `K₈` inside that cover's disjointness link. Hence:

> **`χ(H) = 9` requires some cover whose disjointness link contains `K₈`.**
>
> Links are constant on `PSp(4,3)`-orbits, so there are at most **327 distinct link
> types**. Computing the clique number of one representative link per orbit and finding
> every one below 8 would **refute `χ(H) = 9`** on the frozen frontier.

The one link computed so far has clique number **3**, against the **8** required — not
close. That is 327 clique computations on ~13k-vertex graphs, all inputs present, and it
is the first route to a decision rather than another failed search.

**Caveat, stated because it is the whole caveat:** the 13,648 partners are the certified
frontier, not a proved-complete set. A refutation this way is conditional on frontier
completeness, which Pass 1533's quantifier audit explicitly does not claim.

---

## Pass 2497 — the Gauss sum **closes the arc**

```text
g(3) = 0.000000 + 1.732051i = i*sqrt(3) = sqrt(-3)
```

- `ℚ(g(3)) = ℚ(√−3) = ℚ(ω)`, the **Eisenstein field**.
- Pass 353 records the character field of the Weil half as exactly `ℚ(√−3) = ℚ(ω)`.
- My Pass 1021's fibration fibre is the **Eisenstein units** `ℤ₆ = ℤ[ω]ˣ`.

> **The quadratic Gauss sum at `q = 3` generates the field whose ring of integers has the
> `E₈` fibration's fibre group as its unit group.**
>
> ```text
> Gauss sum  ->  character field  ->  ring of integers  ->  C6 fibre  ->  chirality
>   sqrt(-3)       Q(omega)            Z[omega]           Z[omega]^x
> ```

Every link in that chain was already in the corpus separately; what is new is that they
are one chain, and that Pass 2490's congruence and Pass 2437's `C₆` fibre are the two
ends of it. `q ≡ 3 (mod 4)` makes the Gauss sum imaginary, which makes the character
field imaginary quadratic, which is what gives `ℤ[ω]` a unit group of order 6 rather than
order 2 — and order 6 is exactly what a 6:1 fibration needs.

---

## Pass 2498 — `BT921` does **not** supply `J`; the KO lead stays open

Pass 2492 flagged the Frobenius–Schur ↔ KO-dimension alignment as a lead needing an
explicit real structure. `analysis/BT921_hodge_dirac_spectral_triple.md` was the place to
look, and it does not close it:

```text
Dirac D = d + d* on the W(3,3) 2-complex: 40 vertices, 240 edges
zero modes = substrate homology (1 + 81 + 40)
```

but its own remaining-work list includes

> *"the first-order / orientability axioms (Connes' conditions) for the `W(3,3)` triple"*

`J` is named as a gap there, not exhibited. **So the KO lead cannot be closed from the
existing material and remains a lead.**

One observation worth keeping: BT921's Dirac lives on **40 vertices and 240 edges** —
precisely the base and total space of both towers in Passes 2436–2444. The spectral triple
and the fibrations are built on the same two sets. That is a reason to expect the
alignment to be real, and it is not evidence that it is.

---

## Pass 2499 — `1887` is genuinely stale: a **second** cause

```text
w33_pass1887_exact_global_weight5_decoder
   value/key types present : bool, int, str
   float values            : 0
   integer-like dict keys  : 0
```

Neither the integer-key round-trip defect (Pass 2482) nor float instability applies.

> **`1887` is stale in the ordinary sense — the object was changed and the digest was not
> recomputed.** That was my original hypothesis, discarded too early when the
> integer-key defect turned up and then over-generalised.

So there are at least two independent causes among the flagged certificates, and Pass
2493's withdrawal of the single-cause theory was correct. Still **not repaired**:
re-deriving `1887` needs its producer, which is not in `analysis/*.py` under that name.

---

## Pass 2500 — the sweep: what else was already answered on disk

Prompted by `73` (Pass 2488), a check of what the frontier certificates already settle
that this arc treated as open:

| treated as open | actually settled, and where |
|---|---|
| why `73` divides the cover count | orbit histogram, `pass1510` |
| the `G`-orbit structure on covers | 228/84/15 by stabiliser, `pass1510` |
| is the cover family intersecting | **no** — explicit disjoint pair, `pass1511` |
| do all orbits have disjoint partners | **yes**, all 327, `pass1512` |
| max packing containing the canonical cover | **4**, no `K₄`, `pass1513` |
| can a fifth cover be added to it | **no** — integrality gap, `pass1515` |
| where the frame graph `H` is built | `pass1505/1533/1821/2412`, Pass 2485 |

**Seven questions, all answered in committed data, several of which this arc spent passes
on.** That is the repo's documented failure mode operating on my own track, and the count
is now large enough to be a process problem rather than a series of lapses.

The actionable version: **before opening a question, grep `data/*.json` for its answer**,
not just `analysis/*.md` for its topic. The certificates are prose-free and therefore
invisible to every topic search.

---

## Pass 2501 — ledger

| claim | discharged by | status |
|---|---|---|
| `χ(H)=9` needs a cover-link containing `K₈` | pigeonhole on a 9-packing | proved |
| ≤ 327 distinct link types | links constant on orbits | proved |
| one link has clique number 3 | `pass1513`, exhaustive | theirs, cited |
| four-packing has no fifth layer | `pass1515` Algorithm X | theirs, cited |
| `g(3) = √−3` generates `ℚ(ω)` | direct computation | proved |
| `ℤ[ω]ˣ = ℤ₆` is the `E₈` fibre | Pass 1021 | mine, cited |
| `BT921` supplies `J` | — | **no; lead stays open** |
| `1887` cause | no floats, no int keys | genuinely stale; **not repaired** |
| 327 clique computations | — | **not executed** |

---

## Prior art

- `pass1510`–`pass1515`, `pass1533` — **own** the orbit census, the disjointness graph,
  the four-packing, and the integrality gap. Passes 2488/2496 factor and reduce; they do
  not re-derive.
- Pass 353 — **owns** the `ℚ(√−3)` character field.
- Pass 1021 (mine) — the Eisenstein-unit fibre.
- `BT921`, `W33_SPACETIME_DIMENSION_FROM_KO`, `W33_TWO_CONTINUA` — the Connes material.
- Gauss — the quadratic Gauss sum sign law.

## Still open

- The 327 link clique numbers. This is the decision procedure.
- Whether the frozen 13,648-partner frontier is complete, which any refutation depends on.
- `J` for the `W(3,3)` spectral triple, and with it the KO alignment.
- Five certificates, at least two distinct causes.
