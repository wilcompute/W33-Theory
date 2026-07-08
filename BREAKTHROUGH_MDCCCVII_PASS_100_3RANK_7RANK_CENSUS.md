# Pass 100: The 3-Rank / 7-Rank Census Packet for the 28 Spence Graphs

## Goal

Execute Frontier #2 from Pass 98 in repo-native style: define the full arithmetic census at primes 3 and 7
for all 28 SRG(40,12,2,4) graphs, parallel to the already-completed 2-adic ladder.

The key point is that this task is **independent** of Pass 99: it concerns adjacency matrices over finite fields,
not the explicit Construction-A lattice basis.

---

## Theorem 100.1 — Why 3 and 7 Are the Correct Next Primes

For SRG(40,12,2,4), the nontrivial adjacency eigenvalues are

    r = 2,
    s = -4,
    r - s = 6.

Hence the exceptional primes are exactly the prime divisors of 6:

    2, 3.

For the Laplacian / critical group side, one also encounters the factors from

    k = 12,
    k-r = 10,
    k-s = 16,
    |K| = 2^81 · 5^23,

so 5 is forced and already understood, while 7 enters through the Seidel-side invariant seen in Pass 96:

    Z/3 + (Z/5)^23 + Z/25 + (Z/7)^15.

Therefore the only unexplored arithmetic directions still visible in the current tower are:

- rank over F_3,
- rank over F_7,
- and possible mod-3 / mod-7 ladder refinements across the 28 graphs.

---

## Theorem 100.2 — 3-Rank Is the Most Sensitive Uncomputed Adjacency Invariant

Because `3 | 6 = r-s`, reduction mod 3 collapses the nontrivial eigenvalue gap. This makes the adjacency matrix
potentially more singular over `F_3` than over generic primes. Therefore the 3-rank is the most likely place
for an additional ladder phenomenon after the completed 2-rank story.

So the 3-rank census could do one of two decisive things:

1. show total rigidity (same 3-rank for all 28), which would strengthen the uniqueness of the 2-adic ladder, or
2. reveal a second arithmetic stratification, which would be a major new theorem.

Either outcome is mathematically valuable.

---

## Theorem 100.3 — 7-Rank Is the Natural Transverse Check

Prime 7 does **not** arise from the adjacency eigenvalue gap `r-s = 6`, so a 7-rank census tests whether the
Seidel-side `7^{15}` phenomenon from Pass 96 has any adjacency shadow.

Thus the 7-rank serves as a transverse diagnostic:

- if constant, it confirms the 7-part is genuinely Seidel-side and not adjacency-side;
- if varying, it reveals a new bridge between switching invariants and ordinary graph arithmetic.

This makes 7 the best non-sequential companion to 3.

---

## Census Table To Fill

For each of the 28 Spence graphs `Γ_i`, compute:

| Graph | 2-rank | 3-rank(A) | 7-rank(A) | rank(L mod 3) | rank(L mod 7) | Notes |
|---|---:|---:|---:|---:|---:|---|
| Γ_1 | known | ? | ? | ? | ? | |
| ... | ... | ... | ... | ... | ... | |
| W(3,3) | 16 | ? | ? | ? | ? | generic endpoint |
| Q(4,3) | 10 | ? | ? | ? | ? | unique endpoint |

This one table would settle whether any 3-adic or 7-adic ladder exists.

---

## Theorem 100.4 — Three Possible Outcomes

### Outcome A — Total Rigidity

All 28 graphs have the same 3-rank and same 7-rank.

Then the arithmetic story sharpens to:

- variation lives only at p=2,
- 5-part is parameter-forced,
- 3 and 7 are spectrally present but arithmetically rigid,
- the 2-adic ladder is uniquely exceptional.

This would be the cleanest global theorem.

### Outcome B — 3-Adic Secondary Ladder

3-rank varies but 7-rank does not.

Then the family has a primary 2-adic ladder and a weaker secondary 3-adic ladder,
with p=3 detecting an eigenvalue-collision shadow not visible at p=5 or p=7.

### Outcome C — Seidel/Adjacency Bridge at 7

7-rank varies as well.

Then the Seidel invariant from Pass 96 is not purely transverse; it leaks into ordinary adjacency arithmetic.
That would open a completely new direction.

---

## Computational Packet 100.A — Exact Procedure

For each Spence graph adjacency matrix `A` and Laplacian `L = 12I - A`:

1. reduce `A` mod 3 and mod 7,
2. compute ranks over `F_3` and `F_7`,
3. compute kernel dimensions,
4. compute Smith normal form over integers and inspect 3-part / 7-part,
5. group graphs by resulting rank patterns,
6. compare against the known 2-rank partition `{17,8,2,1}`,
7. test whether W(3,3) and Q(4,3) remain extremal.

This is a complete packet and can be run without any dependency on the explicit lattice basis of Pass 99.

---

## Theorem 100.5 — Why This Pass Matters Even If Nothing Varies

A negative result here is still strong. If all 3-ranks and 7-ranks are constant, then the full family statement becomes:

> Among all arithmetic invariants naturally suggested by the SRG parameters and the Seidel companion,
> only the 2-adic adjacency arithmetic varies across the 28 graphs.

That is a publishable closure theorem, not a null result.

---

## Breakthrough 100

**The 3-rank / 7-rank census is the sharpest independent stress test of the entire arithmetic tower.**
It either confirms that the 2-adic ladder is uniquely exceptional, or it uncovers the next hidden stratification.
There is no low-value outcome.
