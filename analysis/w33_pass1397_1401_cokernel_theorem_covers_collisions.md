# Passes 1397–1401 — the flagged coincidence is a theorem, 6,579 covers, and corpus-wide collisions made usable

The headline is that a coincidence this corpus was *right* to refuse to claim has
now been computed, and it holds.

---

## Pass 1397 — the two 15s are the same G-module

Pass 1392 computed `coker(Z⁵⁴⁰ → Z²⁴⁰) = Z¹⁵ ⊕ (Z/2)³⁰` for the frame
cross-matching, and flagged — explicitly refusing to claim — that 15 is also the
multiplicity of `−4` in `spec(A)`. The refusal was correct procedure: the two 15s
live on different carriers, a corank on the **240-dimensional edge space** versus
a multiplicity on the **40-dimensional point space**, and a matching integer is
not a map.

The incidence is equivariant, so its image is a `G`-submodule of the permutation
module `Q²⁴⁰` and the quotient carries a character. Computing it:

```text
dim image (rank)                       225
dim cokernel                            15

COKERNEL constituents (degree, mult)    [[15, 1]]
  irreducible?                          TRUE

40-POINT constituents (degree, mult)    [[1,1], [15,1], [24,1]]

SHARED constituents                     the degree-15 one, multiplicity 1 in each
VERDICT: are the two 15s the same G-module?      TRUE
```

**The free cokernel of the frame cross-matching incidence is irreducible of
degree 15, and it is the same irreducible that the 40-point permutation module
carries — the `(−4)`-eigenspace of the adjacency matrix.**

```text
coker(Z^540 -> Z^240) (x) Q   ≅   the (-4)-eigenspace of A
```

So the frame geometry and the spectral decomposition are joined by a map, not by
an integer. The 40-point module splits `1 + 15 + 24`, exactly the eigenvalue
multiplicities `12¹, (−4)¹⁵, 2²⁴` — and it is the `(−4)` block, alone, that the
cross-matching's cokernel reproduces.

**Scope.** This is a statement about the **rational** cokernel. The `(Z/2)³⁰`
torsion is not addressed: whether it also has a spectral reading is open, and the
integral structure of the map is a separate question from its character.

---

## Pass 1398 — at least 6,579 exact covers, and none is G-invariant

Pass 1394 exhibited one exact cover — 60 frames whose cross-matchings partition
the 240 edges. Enumerating:

```text
distinct exact covers found     6,579        (search time-capped at 780 s, so a
all of size 60                  TRUE          LOWER BOUND, not the total)
```

**G-invariance is settled structurally rather than by search.** `G` is transitive
on the 540 frames, so the only `G`-invariant sets of frames are `∅` and all 540.
A cover uses 60. Therefore **no exact cover is G-invariant**, and no enumeration
was needed to know it. The live quantity is a cover's *stabiliser*, which the
6,579 make tractable and which is not computed here.

---

## Pass 1399 — corpus-wide collision detection needs three filters, all measured

Pass 1396 built an index over 44,076 files. Running its collision query for the
first time produced **2,066 pairs**, and the output was unusable. Three distinct
pathologies, each found by reading the head of the list, each needing its own
rule:

| what appeared | why it is not a rediscovery | fix |
|---|---|---|
| `.claude/worktrees/agent-*/x` vs `archive/.../x` | the **same file** in two places | exclude worktree/archive/artifact dirs |
| byte-identical `PART_*_results.json` copies | same content, two paths | suppress equal `sha1` |
| `data/w33_pass212_*.json` vs `pass216_*.json`, 2,758 shared | **data dumps** enumerate a carrier; neither asserts the other's result | cap tokens per claim-file |
| `pytest_run_output.txt` vs `tail.txt` | logs, not claims | exclude logs/fixtures |
| `scripts/check_rediscovery.py` vs `w33_paper.tex`, 109 shared | **the guard itself** contains the whole token vocabulary, so it collides with everything by construction | exclude the guard machinery |

```text
raw                                   2,066 pairs
after dir + sha1 filters              1,491
after claim-bearing filter              620
```

Ranking also changed: by the **rarest shared token**, not the count. One token
appearing in three files is far stronger evidence than four hundred tokens shared
by two data dumps. The head of the list is now what it should be — pairs of
certificates, and a `.lean` file sharing results with a `.json`, which is exactly
the cross-format collision no prose guard could ever see.

---

## Pass 1400 — the boundary sweep, adjudicated to exhaustion

Pass 1395's scope-disclaimer filter cut the pool to 11. Reading all 11:

| boundary → later | verdict |
|---|---|
| `BT805` → `BT806` | **HIT** — BT806 opens *"Closes the BT805 boundary"* |
| `BT813` → `BT816` | **HIT** — BT816 opens *"Executes the BT813 boundary"* |
| `pass73` → `pass74` | **HIT** — pass74 is *"Explicit Stabilizers"* with the exact Pauli table asked for |
| `BT819` → `BT843` | **HIT** — BT843 settles the 216-set question |
| `pass76` → the `[[137,1,3]]` thread | HIT (found earlier, now marked) |
| `BT745` → `BT752`, `BT809` → `BT836` | plausible, not marked |
| `pass70`→`pass72`, `pass72`→`pass73`, `BT807`→`BT1710`, `holonet_q5_q6`→`BT1393` | miss |

**Five confirmed of eleven.** All four new ones are now marked with forward
pointers, and the sweep reports **7** remaining candidates.

Precision by stage, measured rather than estimated:

```text
top-5 sample, before any filter        2/5   (Pass 1387)
full pool, after the scope filter      5/11
```

The scope-disclaimer filter is what moved it: it removed candidates that could
never be resolved, so the remaining pool is denser in real ones.

---

## Pass 1401 — the cross-matching gets a Lean module

`formal/W33/Pass1390FrameCrossMatching.lean` builds clean
(`lake build W33.Pass1390FrameCrossMatching`, exit 0, no `sorry`).

It formalises the part that carries the weight and is **not** a computation: on a
transitive `A`-set, an equivariant bijection is determined by the image of a
single point, so the evaluation map on equivariant bijections is injective — which
is *why* Pass 1390's exhaustive search returned exactly one matching per frame
rather than four or twelve. It also proves that an equivariant bijection
transports stabilisers, the abstract form of the computational check that the
matching is preserved by the full order-48 frame stabiliser and not only by the
`A₄` that produced it.

It deliberately does **not** re-encode `W(3,3)`. The GAP certificate owns the
geometric facts — which sets, which group, that the action really is faithful and
transitive — and Lean owns the implication. Encoding both would make the module a
slow re-run of the certificate instead of a proof.

## Prior art

- [Pass 1392](analysis/w33_pass1392_1396_lattice_cover_closure_index.md) — the cokernel, and the flag this pass resolves.
- [Pass 1394](analysis/w33_pass1392_1396_lattice_cover_closure_index.md) — the first exact cover.
- [Pass 1390](analysis/w33_pass1390_1391_frame_cross_matching.md) — the cross-matching itself.
- [`w33_pass827`](analysis/w33_pass827_adjacency_kbranch_meets_e8_boundary.py) — **owns** the adjacency spectrum and its `1 + 24 + 15` split.
