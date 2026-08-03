# Passes 2666–2673 — the index reaches the manuscripts, and two of my identifications shift

---

## Pass 2666 — the value index now covers `.tex` and `.md`

Three withdrawals in two batches (Passes 2650, 2651, 2652) traced to
`photonic_holonet_body.tex`, which nothing indexed: `build_certificate_index.py` covered
`data/*.json`, and the prose indexes (`RESULTS_INDEX.md`, `TOPICAL_ALIASES.md`) match
**words**, not values.

Manuscripts carry load-bearing **numbers in running text**. The index now scans `*.tex`,
`analysis/*.md` and `docs/*.md` alongside the certificates, reporting file and line.

```text
py -3 scripts/build_certificate_index.py 51840
  -> 909 places, across certificates AND manuscripts
```

*(`51840` is too common to be a useful query — the point is that manuscript lines now
appear at all.)*

---

## Pass 2668 — the 36-lane mixer is the **control plane**

`photonic_holonet_body.tex` line 2783:

> *"the `36` timetables form `SRG(36,15,6,6)`, the **other** rank-3 geometry of the same
> group, so the **control plane** and the **data plane** (`SRG(40,12,2,4)`) are the two
> classical [rank-3 geometries]"*

and line 2856 tabulates `SRG(36,15,6,6)` as *"basis-overlap law | control-plane fabric"*.
`w33_paper_body.tex:477` names the same graph `NO⁻(6,2)`.

> **The 36-lane mixer I made routable (Pass 2612) is the paper's control-plane fabric.**
> The 40-point graph is the data plane. Those are the two rank-3 geometries of one group,
> and the machine needs both.

I had been calling it "the spread mixer", following the parallel track's Pass 2053
identification as the 36 spreads / `NO₆⁻(2)` — which is the same graph and consistent.
But the *architectural role* was already named, and naming it correctly matters: my Pass
2661 stack table lists the mixer as "degree-2 symplectic interconnect", which is the
**control** plane, and the data plane has no RTL at all.

**Consequence for Pass 2661's "complete `W(3,3)` core fits one FPGA":** that stack is
control plane + cubic + clock + chirality. **It does not contain the data plane.** The
claim should read *"the control-plane core"*, not *"the complete core"*. Corrected here.

---

## Pass 2669 — the manuscripts already carry `φ`, by a different route

`golden`/`Fibonacci` appear **22 times in `photonic_holonet_body.tex` and 30 in
`w33_paper_body.tex`** — 52 mentions I did not know about when I wrote Passes 2083 and
2439. What they say:

```text
"the 120 icosians: 8 units + 16 half-units + 96 golden [units]"
"two arithmetics --- Eisenstein (q=3) and icosian (golden quaternion)"
"the repo's Golden D4/Weyl shell"
"In the anyonic Fibonacci representation"
"Otto's 2022 ... golden quartic, icosahedral coefficients, chirality"
```

> **`φ` enters this project through the ICOSIAN arithmetic — the golden quaternions and
> the icosian description of `E₈` — as one of two named arithmetics alongside the
> Eisenstein one.**

That is a different object from my Pass 2439 result (`φ` as the spectral radius of
`R₄²U₆` in `SL₃(ℤ)`), so Pass 2439 is not a rediscovery. But it does correct the framing:

**Pass 2083 claimed "`φ` is absent from the finite geometry, present only in the infinite
arithmetic". That is too strong.** It is absent from `W(3,3)`'s character fields and from
Gaussian binomials — those computations stand — but `E₈` has an icosian description in
which golden arithmetic is manifest, and `E₈` is squarely inside this project. The honest
statement is: **`φ` is absent from `W(3,3)`'s own character theory and present in `E₈`'s
icosian arithmetic**, with my `SL₃(ℤ)` growth rate a third, so far unrelated, appearance.

Whether the three are connected is unexamined.

---

## Pass 2670 — the two items not done

- **Wiring the `E₆` cubic to the mixer** — not done. Both are placed (473 LC and 4048 LC,
  4615 total with the clock) and share the `μ₃` phase representation, so the integration
  is mechanical, but it was not performed.
- **The qutrit Pauli hierarchy recursion** — still the one of four never examined.

---

## Pass 2671 — ledger

| claim | status |
|---|---|
| value index covers `.tex` and `.md` | **done** |
| mixer = the paper's control-plane fabric | **identified** |
| Pass 2661's "complete `W(3,3)` core" | **corrected — it is the control-plane core; no data plane** |
| `φ` absent from the finite geometry (Pass 2083) | **too strong — `E₈`'s icosian arithmetic is golden** |
| Pass 2439 `φ` in `SL₃(ℤ)` is a rediscovery | **no — different object** |
| the three `φ`s are related | **unexamined** |
| cubic wired to mixer | not done |
| qutrit Pauli recursion | not examined |

---

## Prior art

- `photonic_holonet_body.tex` §Networking and the physics-to-architecture dictionary —
  **own** the control-plane / data-plane identification.
- `w33_paper_body.tex` — **owns** the icosian/golden arithmetic and `NO⁻(6,2)`.
- Pass 2053 (parallel track) — the `NO₆⁻(2)` identification of the 36-graph.

## Still open

- Wiring the cubic to the mixer; a data-plane RTL, which does not exist.
- Whether the icosian `φ`, the `SL₃(ℤ)` `φ`, and the `D₄` golden shell are one thing.
- The qutrit Pauli hierarchy recursion.
- Pages 50–100 still only partially read.
