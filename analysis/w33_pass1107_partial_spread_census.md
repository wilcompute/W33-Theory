# Pass 1107 — the size-(q²−1) partial-spread census, and a closed form that is false

Pass 1100 found that the 135-block quotient of the 540-frame action is the set of
**maximal partial spreads of size 8** in W(3,3), with the exact census

```text
q = 3:  1755 = 1620 extendable + 135 unextendable
```

This pass asks whether that split is q-general. It has two halves and they point in
opposite directions, so both are stated.

## The half that holds: extendable = (#spreads) · C(q²+1, 2)

The natural q-general size is **q²−1**, two short of a full spread (q²+1). At both
computable orders the extendable count is exactly "a spread with two lines deleted":

| q | points | lines | spreads | size q²−1 | total | extendable | (#spreads)·C(q²+1,2) | unextendable |
|---|---|---|---|---|---|---|---|---|
| 2 | 15 | 15 | 6 | 3 | 80 | 60 | 6 · C(5,2) = 60 | 20 |
| 3 | 40 | 40 | 36 | 8 | 1755 | 1620 | 36 · C(10,2) = 1620 | 135 |

The identity is exact at both, which also says a partial spread of size q²−1 lies in
**at most one** spread — otherwise the product would over-count.

## The half that does not: q³(q²+1)/2

Both unextendable counts fit a clean closed form, and it is not curve-fitting — it
is forced by a structural correspondence that holds at both orders:

```text
#frames        = (q²+1)(q+1)·q³ / 2          (a line is disjoint from exactly q³ others)
block size     = q + 1                        (3 at q=2, 4 at q=3)
unextendable   = #frames / (q+1) = q³(q²+1)/2
```

which gives 20 at q=2 and 135 at q=3, both correct. The block correspondence was
verified independently at q=2: the doily's frame action has a block system of
**20 blocks of size 3**, each using exactly **q²−1 = 3** distinct lines — the same
shape Pass 1100 established at q=3.

**And it is still wrong in general.** W(q) is the dual of Q(4,q), so a maximal
partial spread of W(q) is a maximal partial ovoid of Q(4,q), and that family is
studied: maximal partial ovoids of size q²−1 of Q(4,q) are described as *sharply
transitive subsets of SL(2,q)*. Penttila exhibited them for q ∈ {5,7,11};
Cimráková and Fack confirmed by computer search. The literature reports that for
q = pʰ with p odd and **h > 1 they do not exist at all**, and that no example is
known beyond q = 11.

A polynomial count cannot be reconciled with a family that is empty at q = 9 and
q = 27. So `q³(q²+1)/2` fits every order this repository can compute and is
refuted by the two orders it cannot. **Two data points were not enough**, which is
exactly the risk flagged when the formula was proposed.

## What this changes upstream

Pass 1100's identification of the 135 stands — at q = 3 the block quotient *is*
that family, and the census 1755 = 1620 + 135 and the block correspondence are
this repository's contribution. But the **object is published**, and Pass 1100 has
been amended to say so. This is failure mode 5 at the external boundary: the
mathematics was right, the witness passed, and only the novelty was false.

The internal guard could not have caught it — the corpus genuinely does not
contain this. Only a literature check does, which is why `CLAUDE.md` lists
"check the external citations already in the repo" alongside the corpus search.

## The guard change paid for itself immediately

Item 1 of this batch taught `scripts/check_rediscovery.py` noun-number tokens
(`ovoid@7`, `partial-spread@8`), because 1–2 digit integers were invisible to the
index's `\d{3,9}` pattern and that blind spot had cost a whole pass. On its first
run against this file it emitted `partial-spread@4` against
`analysis/BT790_csaszar_embedding.md`, which turned out to contain a **false
standing claim**:

> "a partial spread of mutually skew totally isotropic lines has size at most 5"
> … "The maximum totally-isotropic skew partial spread has size 4 or 5"

W(3,3) has 36 **spreads**, each of 10 pairwise disjoint totally isotropic lines,
so the maximum is 10. The census above found 1755 partial spreads of size 8 alone.
BT790 now carries a correction banner. The measured cost of the new token class
was +1.5 points of flag rate (30.9% → 32.4% at MAX_FILES = 25); the first thing it
bought was a retracted error.

## Boundary

Open: whether the q = 2 count of 20 belongs to the same family at all (the doily
is self-dual and even-q behaviour differs throughout this corpus — it has ovoids,
W(3,3) does not); whether the block correspondence has any content at q ∈ {5,7,11}
where the family is known to exist; and what the count actually is as a function
of q, which the sporadic existence pattern suggests is not a formula.

## Sources

- [The known maximal partial ovoids of size q²−1 of Q(4,q)](https://arxiv.org/pdf/1201.5967)
- [On the smallest maximal partial ovoids and spreads of the generalized quadrangles W(q) and Q(4,q)](https://www.sciencedirect.com/science/article/pii/S0195669806002162) — Cimráková & Fack, European J. Combin. (2005)
- [Searching for maximal partial ovoids and spreads in generalized quadrangles](https://projecteuclid.org/journals/bulletin-of-the-belgian-mathematical-society-simon-stevin/volume-12/issue-5/Searching-for-maximal-partial-ovoids-and-spreads-in-generalized-quadrangles/10.36045/bbms/1136902607.pdf)
- [On large maximal partial ovoids of the parabolic quadric Q(4,q)](https://arxiv.org/pdf/1201.5992)

## Prior art in this repository

- `analysis/w33_pass1100_name_the_135.g` — the q=3 census and the block identification.
- `analysis/w33_pass1079_frame_action_rank32.g` — the three block systems.
- `analysis/w33_pass1097_name_the_frame_quotients.g` — the 45 as polar pairs.
- `analysis/BT818_ovoid_nogo_theta_gap.md` — α(W(3,3)) = 7 and the KS bracket.
