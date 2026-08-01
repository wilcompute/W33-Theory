# Passes 1612–1616 — the frame kernel is the Hoffman eigenspace, and the substrate picks a hand

> **Number-label warning.** These five numbers are used by two packets. This one
> is the glue track (`analysis/w33_pass1612_*`, `w33_pass1615_1616_*`,
> `w33_pass1616_*`); the parallel track's `analysis/BT1611_1615_*` and
> `w33_pass1611_1615_torsion_xor_lattice_octet.*` cover torsion/XOR/lattice/
> coherent-configuration and share no result with this file. The filenames, not
> the numbers, are the identifiers — cite those. This block was computed as
> 1606–1610, renumbered once, and collided again; `scripts/next_pass_number.py`
> exists because of it.

Five items. Two of them close a loop with the parallel track's octet work; two
answer a question about chirality that this repo has asked in three different
forms; one is a geometric restatement of the resolution problem.

---

## Pass 1612 — `M Mᵀ = 4I + A_H`, so the frame kernel **is** the Hoffman eigenspace

The frame cross-matching matrix `M` (540 × 240, Pass 1390) and the frame graph
`H` (540 vertices, 32-regular) were built for different purposes. They are the
same object:

```text
max edges shared by two distinct frames : 1
M M^T == 4I + A_H                       : True
spec(H) : 32^1, 14^44, 8^15, 4^81, 2^84, (-4)^315
```

Two distinct frames share **at most one** edge, so `M Mᵀ` has diagonal 4 and
off-diagonal 0/1 — it is literally `4I + A_H`. Therefore

> **`ker(Mᵀ)` = the `(−4)`-eigenspace of `H`**, and `col(M) = E₋₄(H)^⊥`.

```text
rank_Q(M)  = 225   (= 225 mod a large prime)
rank_F2(M) = 195   <- the parallel track's [240,195,4]_2 frame code
rank_F3(M) = 225
540 - dim E_(-4) = 540 - 315 = 225   -> col(M) = E_(-4)^perp : True
mod-2 deficiency = 225 - 195 = 30
```

Every number here was already in the corpus separately. `240 − 225 = 15` and
`225 − 195 = 30` are exactly the two summands of Pass 1397's cokernel theorem,

```text
coker(M) = Z^15 (+) (Z/2)^30,
```

which is now visible as a statement about `H`'s spectrum rather than about a
Smith form. The 2-torsion is the only torsion: `rank_F3 = rank_Q`.

---

## Pass 1613 — why the octet cuts are redundant, and the generator that produces them

Pass 1541 (parallel track) **owns** the 45 octets, the `[240,195,4]₂` code, the
405 exact-8 resolution cuts, and the observation that those cuts are *redundant
over ℚ*. It does not say why. Pass 1612 does.

Pass 1491 proved every colour class `S` of a resolution is Hoffman-tight, i.e.
`χ_S − (1/9)·1 ∈ E₋₄`. So for **any** frame-subset `T`,

```text
|S cap T| = |T|/9 + <chi_T, chi_S - (1/9)1>
```

and the second term vanishes whenever `χ_T ⊥ E₋₄`. Hence:

> **Spectral constraint generator.** For every `w ∈ col(M) = E₋₄^⊥`, every colour
> class of every resolution satisfies `⟨w, χ_S⟩ = (Σw)/9` — exactly, with no
> search. The free-constraint space has dimension exactly **225**.

The octet cuts are one instance of this, and I rebuilt the octets independently
to check. Not from their construction: a 4×4 grid in `SRG(40,12,2,4)` is
recovered from a non-collinear pair `{p,q}` via its μ-set, and since `μ = 4` and
each grid has 12 non-collinear same-part pairs, there are `540/12 = 45` of them.

```text
grids (octets) found          : 45
octet edge-weights            : [16]
times each edge is covered    : [3]
|frame cap octet| values      : [0, 2]
frames meeting a fixed octet twice : [72]

max ||P_(-4) chi_N(o)||       : 4.687e-15    <- the redundancy, proved
max |P_(-4) (column of M)|    : 1.825e-15
```

Independent construction, identical numbers — including their 16, their 0-or-2,
and their 72. And `χ_N(o) ⊥ E₋₄` to machine zero explains the ℚ-redundancy they
measured.

**The mod-2 half is the interesting one**, and it lands exactly:

```text
rank_F2(M^T)       = 195
rank_F2([M^T; N])  = 225     <- the octets add exactly 30
rank_Q ([M^T; N])  = 225     <- and nothing at all over Q
```

> **The 45 octets restore, over `F₂`, precisely the 30 dimensions that the frame
> system loses — the `(Z/2)³⁰` of the Pass 1397 cokernel. Exactly those, and no
> more.**

**Attribution, and it matters here.** The parallel track's Pass 1607 reports the
same `195 → 225` rank gain, and its Pass 1606 gives the full Loewy filtration of
the 30-dimensional torsion. Those are **theirs**; I reproduced the number
independently and did not know it when I computed it. What this pass adds is not
the number but its *source*: `225` is `dim E₋₄(H)^⊥`, forced by
`M Mᵀ = 4I + A_H`, which is why the count is 225 and why the ℚ-redundancy they
observed had to hold. Number theirs, mechanism new.

One caution, because the same word means two things. In *edge* space the picture
is different: `rank_F2([M; K]) = 209`, so there the octets add only **14** — and
14 is their own absolutely-irreducible `F₂` module from Pass 1537. Frame space
and edge space give 30 and 14; both are correct, and they are not the same claim.

---

## Pass 1614 — a resolution is a regular 8-simplex inscribed in `E₋₄`

Restating Pass 1491 with the classes taken together. Nine disjoint classes of
size 60 in 540 give, for the centred indicators `u_c = χ_{S_c} − (1/9)1`:

```text
||u_c||^2                         = 160/3
<u_c, u_c'> for c != c' (disjoint) = -20/3
regular simplex needs <.,.> = -||u||^2/(9-1) : True
sum of the nine u_c                = 0
```

> A resolution of `W(3,3)`'s frames is exactly a **regular 8-simplex centred at
> the origin of the 315-dimensional `(−4)`-eigenspace**, whose nine vertices are
> centred maximum-independent-set indicators.

The simplex condition is automatic, so this is not itself an obstruction — but
it is the correct shape of the search, and it says the nine classes are forced
into mutual angles with no freedom at all.

---

## Pass 1615 (physics) — the signed edge module is chiral

The signed 240-edge module `V` is canonical: reversing the chosen orientation of
any edge conjugates the representation by a diagonal `±1` matrix, so its
character does not depend on any convention. Its decomposition (Pass 1482/1487,
reconfirmed here from an independent `PGSp(4,3)` construction):

```text
V = 15 (#6) + 24 (#14) + 30 (#15) + 81 (#24) + 90 (#25)   = 240
```

Let `ε` be the sign character of `PGSp/PSp`. Then:

```text
V (x) eps  =  V  ?   FALSE
```

and, block by block,

| block | degree | role | `ε`-stable? |
|---|---|---|---|
| Irr[6] | 15 | gauge | **no** |
| Irr[14] | 24 | gauge | **no** |
| Irr[15] | 30 | constraint | **no** |
| Irr[24] | 81 | **physical** | **no** |
| Irr[25] | 90 | constraint | yes |

Four of the five blocks carry a sign. The lone `ε`-stable one is the 90 — which
is exactly the block that arises by *fusion* of two `PSp` degree-45s, so it could
not have carried one.

Where the total sign is visible:

```text
class  ord   size    chi(V)      object
   10    2     36     -20        the 36 SPREADS   (Pass 1485)
   19    2    540     +12        the 540 FRAMES   (BT773)
   12    6   1440      -2
   17    6   1440      -2
```

The two involution classes that read the whole module's handedness are the same
two geometric classes that read the Steinberg's (Pass 1481/1485) — and the
values are larger: `∓20` and `±12` against the 81's `∓9` and `±3`.

---

## Pass 1616 (physics) — the handedness cannot be relabelled away, and six classes cancel

`V ⊗ ε ≇ V` is only a *non-removability* statement if the twist is not induced by
an automorphism of the group; otherwise "chirality" would be a naming
convention. Verified rather than assumed:

```text
|Aut(PGSp(4,3))| : 51840
|Inn(PGSp(4,3))| : 51840
COMPLETE (Aut = Inn, trivial centre) : True
```

`PGSp(4,3) = U₄(2):2` is a complete group, so every automorphism is inner and
every inner automorphism fixes every character. The `ε`-twist is therefore
realised by **no** automorphism at all, and the two degree-81s (`Irr[23]`,
`Irr[24]`, interchanged by `ε`) are genuinely distinct `PGSp`-modules. The
substrate's edge module carries `Irr[24]`, not `Irr[23]`.

**This is why it differs from Pass 346.** There, the Weil representation's
spinor halves `S±` were swapped by the substrate's own controller `T` — an
element *inside* the group — so no internal observable could distinguish them and
chirality was unselectable. Here the swap is not inner, not outer, and not an
automorphism. Nothing in or around the group performs it. The handedness is
selected, and Pass 1615 names the selector: the frames and the spreads.

It also extends BT746, which proved chirality absolute for the *presentation
torsor* by an orbit count. The same conclusion now holds for the carrier of the
Hodge/Maxwell decomposition, by a character argument.

### The blocks' signs partially cancel

Ten classes see at least one block's sign; only four survive in the total.

```text
class ord  size       15    24    30    81    90 |   V   V(x)eps
   3    4  1620       -1     .     .     1     . |   0      0   CANCELS
   5    4   540       -1     .     4    -3     . |   0      0   CANCELS
   9    8  6480        1     .     .    -1     . |   0      0   CANCELS
  10    2    36       -5     4   -10    -9     . | -20     20
  12    6  1440       -2     1    -1     .     . |  -2      2
  17    6  1440        1    -2    -1     .     . |  -2      2
  19    2   540        3     4     2     3     . |  12    -12
  20   10  5184        .    -1     .     1     . |   0      0   CANCELS
  24   12  4320       -1     .     1     .     . |   0      0   CANCELS
  25    6  4320        .     1    -1     .     . |   0      0   CANCELS
```

Six of ten cancel exactly. Note the two size-540 classes behave oppositely: the
order-4 one cancels, the order-2 one — BT773's frame class — does not. The
chirality of the whole module concentrates on the frames and the spreads because
everywhere else the gauge, physical and constraint signs annihilate each other.

### Which degree-30 splits

`PSp(4,3)` has three degree-30 irreducibles; `PGSp(4,3)` has two. So one splits
and two fuse.

```text
PSp degree-30 irreducibles : [11, 12, 13]
PGSp Irr[15] deg 30 | restricts to PSp [11]      eps-stable: false
PGSp Irr[16] deg 30 | restricts to PSp [11]      eps-stable: false
PGSp Irr[19] deg 60 | restricts to PSp [12, 13]  eps-stable: true
```

`#11` splits into the two extensions `Irr[15]`/`Irr[16]`; `#12` and `#13` fuse
into the degree-60 `Irr[19]`. The coexact block picks `Irr[15]`. This answers the
parallel track's Pass 1541 step 5 for the extension question — their `V = 4U + Sd`
realises the degree-30 that *splits*, and its sign is carried on the same two
classes as everything else.

---

## Prior art

- **Passes 1606–1610 (parallel track, `analysis/BT1606_1610_five_continuations.md`)
  own** the `195 → 225` mod-2 rank gain and the complete Loewy filtration of the
  30-dimensional torsion, published while this block was being computed. Pass
  1613 supplies the spectral mechanism behind their number; it does not restate
  their filtration. Their Pass 1608 also studies a chirality — of *four-packings*,
  where the outer element **does** conjugate the two residual octet Grams, so
  that chirality is invisible to the Bockstein sector. Pass 1615's chirality is a
  different object with the opposite verdict, and the two do not collide.
- **Pass 1536 / 1537–1541 (parallel track) own** the 45 octets, the
  `[240,195,4]₂` frame code, the 405 exact-8 cuts, the ℚ-redundancy observation,
  and the absolutely irreducible `F₂` 14. Pass 1613 explains the redundancy and
  measures the mod-2 completion; it does not re-derive their objects.
- [BT746](analysis/BT746_absolute_chirality_z12.md) — **owns** "chirality is an
  absolute geometric invariant of `W(3,3)`, not a convention", proved by an orbit
  count on presentation pairs. Pass 1615/1616 is the same conclusion for a
  different carrier by a different method.
- [BT866](analysis/BT866_h2_oriented_irreducible_decomposition.md) — **owns** the
  observation that a rational degree-30 has two inequivalent extensions to
  `W(E₆)`. Pass 1616 identifies *which* of the three it is and what the other two
  do.
- [BT773](analysis/BT773_involution_cube_theorem.md) — **owns** the 540
  involutions ↔ frames bijection.
- Pass 1397 — the cokernel `Z¹⁵ ⊕ (Z/2)³⁰`; Pass 1491 — Hoffman tightness;
  Pass 1481/1485 — the separating classes; Pass 1482/1487 — the block extensions.
- Pass 346 — **owns** the unselectability of the Weil spinor chirality, which
  Pass 1616 distinguishes from this result rather than contradicting.
- [Passes 331–332](PASS331_332_WEIL_INTEGRAL_CHIRALITY_BRIDGE.md) — **own** the
  mod-2 Weil shadow `H₈`, where the outer controller acts by Frobenius
  (`t⁻¹ωt = ω²`) and so `End_PGSp(H₈) = F₂`: the outer coset *does* interchange
  the two `F₄`-halves. That is precisely the contrast. In the edge module the
  interchange is the `ε`-twist, which by Pass 1616 no group element and no
  automorphism performs — so that module's hand is selected while the half-spin's
  is not. The two results are about different carriers and point opposite ways
  for a stated structural reason.

## Still open

The resolution itself (`χ(H) = 9`). Pass 1614 says the search space is a regular
8-simplex in a 315-dimensional space and Pass 1613 says 225 of the linear
constraints are free; neither decides it. The SAT instance remains undecided.
