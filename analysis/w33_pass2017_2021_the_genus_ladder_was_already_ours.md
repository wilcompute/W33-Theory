# Passes 2017–2021 — the genus-6 `66` is the same object, and the ladder was already in the repo

Following the thread rather than searching for what I expected found something
better than a coincidence check.

---

## Pass 2017 — the two 66s are **one object**, not a coincidence

The repo already contains the answer, in `data/w33_toroidal_h6_66_bridge.json`
and `analysis/BT1844_F12_genus6_edge_bridge.md`. The "two toroidal polyhedra"
are **Császár and Szilassi**, and the repo carries a *complete-adjacency ladder*
with genus formula `(n−3)(n−4)/12`:

```text
h0 fixed point       : n =  4, genus 0, edges  6     (K4)
h1 Csaszar/Szilassi  : n =  7, genus 1, edges 21     (K7)
h6 K12 dual pair     : n = 12, genus 6, edges 66     (K12)
```

So the genus-6 structure's 66 edges **are** `C(12,2)` — because a Császár-type
polyhedron of genus 6 is a triangular embedding of `K₁₂`. The 66 is not *like*
`K₁₂`'s edge count; it *is* `K₁₂`'s edge count.

> **`K₁₂` and the genus-6 toroidal polyhedron are the same object viewed two
> ways.** No `G`-set test is needed: the identification is definitional.

That answers the question and, unlike the last three "66 = 66" style claims,
survives because it was never a count match to begin with.

---

## Pass 2018 — the residual `K_{q+1}` lands exactly on that ladder

Pass 2016 showed the residual set of a spread seed is `q²+1` disjoint copies of
`K_{q+1}`. Testing those against the ladder's genus formula:

```text
   q  K_{q+1}  edges  (q-2)(q-3)/12  exact?   ladder entry
   3      K4       6         0.0000   True    h0 fixed point
   5      K6      15         0.5000   False
   7      K8      28         1.6667   False
  11     K12      66         6.0000   True    h6 K12 dual pair
  23     K24     276        35.0000   True
  27     K28     378        50.0000   True
```

> **The substrate's own `q = 3` is the ladder's `h0` entry, and `q = 11` is its
> `h6` entry.** Those are the only two `q ≤ 20` where the residual `K_{q+1}` has
> an *exact* Császár-type triangulation.

Prime powers with `(q−2)(q−3) ≡ 0 (mod 12)`:

```text
2, 3, 11, 23, 27, 47, 59, 71, 83, 107, 131, 167, 179, 191
```

`q = 3` is the smallest odd one — the substrate's own. This is why the `q = 11`
computation of Pass 2011 landed on 66 rather than on an arbitrary number.

---

## Pass 2019 — the classical Császár/Szilassi case has **no** symplectic counterpart

The ladder's middle entry `h1` is the actual Császár and Szilassi polyhedra:
`K₇`, genus 1, 21 edges. For that to be a residual `K_{q+1}` we would need
`q + 1 = 7`, i.e. **`q = 6`** — which is not a prime power, so `W(6,6)` does not
exist.

> The two famous toroidal polyhedra sit at the one rung of the ladder that the
> symplectic quadrangles cannot reach.

Recorded as a genuine gap, not a defect: `h0` and `h6` have symplectic
realisations, `h1` does not.

---

## Pass 2020 — the *third* 66, which is a count match and should be treated as one

`w33_toroidal_h6_66_bridge.json` also carries a `W(3,3)` quantity:

```text
w33_scheduler_66 : direct_line_load 12, nonlocal_line_load 54,
                   full_nonidentity_line_load 66 = 12 + 54,
                   line_histogram {66: 40}
theorem          : "W33 perfect route load 66 equals the h=6 complete-adjacency
                    toroidal edge count"
```

That is a scheduler load per line of `W(3,3)` — 40 lines, each carrying 66 — and
`W(3,3)`'s lines are `K₄`s with **6** edges, not 66. So this 66 and the `K₁₂` 66
are **different objects with the same number**.

The stated equality is *numerically true* and the record says so. But it is
exactly the shape that produced three false claims in this arc (Passes 1875,
1984, 2007), and no map between the two objects is exhibited. Flagged for the
same treatment: **compare the objects, not the counts.** I am not asserting the
bridge is wrong — only that it is a numerical bridge and should be read as one.

---

## Pass 2021 — the candidate-orbit property, restated per-line

Pass 2016's decomposition sharpens the one open step. A candidate frame's `q+1`
matching edges lie in `q+1` **distinct** copies of `K_{q+1}` — one per spread
line, since `M` meets each spread line at most once. So:

> **The candidate-orbit property is equivalent to: for every `p ∈ M`, the point
> `M' ∩ L_p` is `σ_S(p)`.**

That is a per-line statement about a single point, rather than a global statement
about frames — a strictly easier form of the same question, and the form a proof
should attack. What must be shown is that no *other* transversal of the `q+1`
lines is a line.

---

## Not done this pass

- Collapsing the `1/q` sections of both drafts to the `K_{q+1}` argument.
- Sweeping the arc's other ratios (`96.9%`, `0.9535`, `260`) for elementary
  explanations.

Listed rather than dropped.

---

## Prior art

- `analysis/BT1844_F12_genus6_edge_bridge.md` and
  `data/w33_toroidal_h6_66_bridge.json` — **own** the complete-adjacency ladder
  and the Császár/Szilassi framing. BT1843–1845 own the F12 mesh verifier.
- `manuscripts/tex/part18_jungerman_ringel.tex`,
  `exploration/w33_csaszar_szilassi_jordan.py` — the minimal-triangulation lane.
- Pass 2016 — the `K_{q+1}` decomposition, from the user's observation.

## Still open

- Whether the `W(3,3)` route-load 66 is more than a number.
- The candidate-orbit property, now in its per-line form.
