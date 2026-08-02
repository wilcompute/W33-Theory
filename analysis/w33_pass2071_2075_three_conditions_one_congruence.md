# Passes 2071–2075 — three conditions, one congruence: `q ≡ 3 (mod 4)`

The strongest convergence in this arc. Three statements from completely different
places all turn out to be the same congruence, and one of them is `σ_S` being
literally multiplication by `i`.

---

## Pass 2071 — `q ≡ 3 (mod 4)` means `σ_S` is multiplication by `i`

`σ_S` needs a similitude `g` with `g² = μI` and `μ` a **non-square** (Pass 1908).
The question nobody had asked: **can `μ = −1`?**

```text
   q  q mod 4   -1 mod q   squares mod q          -1 a non-square?
   3        3          2   {1}                    TRUE
   5        1          4   {1,4}                  false
   7        3          6   {1,2,4}                TRUE
  11        3         10   {1,3,4,5,9}            TRUE
  13        1         12   {1,3,4,9,10,12}        false
  19        3         18   {1,4,5,6,7,9,11,...}   TRUE
  23        3         22   {1,2,3,4,6,8,9,...}    TRUE
```

> **`μ = −1` is available exactly when `q ≡ 3 (mod 4)`** — and then `g² = −I`, so
> `g` is a **complex structure** on `F_q⁴`. It is literally multiplication by `i`,
> with `F_{q²} = F_q(i) = F_q[x]/(x²+1)`.

At `q = 3` the earlier computation found `μ = 2`, and `2 = −1 mod 3`. So the
substrate's spread involution *was* multiplication by `i` all along; Pass 1908
just didn't name it.

### And that is the same condition as two others

```text
Gow (1985) : PSp(4,q) has complex characters   iff  q ≡ 3 (mod 4)
Pass 1908  : sigma_S is multiplication by i     iff  q ≡ 3 (mod 4)
Pass 2065  : q is a primitive root mod 2q+1     iff  q ≡ 3 (mod 4)   [q odd]
```

> **Three conditions — representation-theoretic, geometric, and number-theoretic
> — are one congruence.** Gow's complex characters, the spread involution being
> an `i`, and the characteristic generating its own Heawood number's
> multiplicative group are the same fact about `q`.

That is not a count match: each is *proved* equivalent to `q ≡ 3 (mod 4)`
separately, so the coincidence is at the level of the congruence, not of a
number.

---

## Pass 2072 — the converse

Reachable `q` (Pass 2024) are `q ≡ 2, 3, 11 (mod 12)`. Among them:

```text
    q  mod 12  Sophie Germain?  primitive root?
    3       3            True             True
   11      11            True             True
   23      11            True             True
   27       3           False            False
   47      11           False            False
   83      11            True             True
  131      11            True             True
  179      11            True             True
```

> **For `q > 3`: `q` is primitive-root ⟺ `q` is reachable **and** `2q+1` is
> prime.** Reachability already forces `q ≡ 11 (mod 12)` for the odd primes,
> hence `q ≡ 3 (mod 4)`; the only extra requirement is that `2q+1` be prime.

**A caveat on `q = 2`.** The Legendre argument of Pass 2065 assumes `q` odd. For
`q = 2`, `p = 5` and `2` *is* a primitive root mod 5 — but `2 ≢ 3 (mod 4)`. So
the equivalence is for odd `q`; `q = 2` satisfies the conclusion by a different
route. Recorded because I would otherwise have stated a false "iff".

---

## Pass 2073 — Gray code and no-consecutive-1s are one object

The user's question. They are not two ideas:

> The **Fibonacci cube** `Γ_n` has as vertices the length-`n` binary strings with
> no `11`, and joins two when they differ in **one bit** — Gray-code adjacency.
> So `Γ_n = ` (hypercube) `∩` (Zeckendorf-admissible), and `|V(Γ_n)| = F(n+2)`,
> which Pass 2066 verified for `n ≤ 8`.

The repo already has the Gray/hypercube lane —
`analysis/2026-05-29_gray_hamming_router_lift.md`,
`2026-05-29_cl4_q4_hypercube_network_unification.md`,
`BT1320_BT1325_hypercube_tower_holonet.md` — so the routing side is theirs.

**Not completed:** whether `Γ_n` is Hamiltonian for the `n` of interest. The DFS
did not finish, and Hamiltonicity of Fibonacci cubes has a literature I have not
consulted. Reported as unfinished, not as unknown-in-principle.

---

## Pass 2074 — phinary on `BT695`'s object: nothing found

`BT695` owns `K₃,₃ → [9,4,4] → SU(2)₃ → Fibonacci anyons`, so if Zeckendorf
structure lives anywhere here it should be there rather than in the spread lane.
`K₃,₃`'s cycle space is `β₁ = 4`, i.e. all of `F₂⁴` — **no no-consecutive-1s
constraint**, because every one of the 16 vectors is a cycle.

So the Fibonacci content of `BT695` is in the *fusion rules* (`τ × τ = 1 + τ`),
not in a Zeckendorf-style digit restriction. **No new link found**, and combined
with Pass 2068 (no golden eigenvalue, no Fibonacci recursion in the substrate's
counts) the phinary lane is currently a vocabulary rather than a mechanism.

---

## Pass 2075 — the `D₈` reconstruction, still blocked

Reproduced the setup — 540 frames, `H ≅ D₈ × S₄` of order 192, 116 subgroup
classes of order 2/4/8 — but the exact-cover search hits GAP's recursion trap.
An iterative bitset version is the fix and is **not done**. Third report of this
item as incomplete; I am not going to record it as a negative.

---

## What to send the other track

1. `W(3,3)` is selected by `q + 1 = 4`: its lines are tetrahedra, the unique
   simplex whose star acts in middle degree, so `σ_S`'s 1-factor choice is a
   star-orbit choice (Pass 2062).
2. `q ≡ 3 (mod 4)` unifies three conditions — Gow's complex characters, `σ_S`
   being multiplication by `i`, and `q` generating `(ℤ/(2q+1))^×` — and implies
   genus-reachability (Passes 2065, 2071).

---

## Prior art

- **Gow (1985)** — the `q mod 4` reality theorem; in-repo Passes 353/355.
- BT695 — **owns** the Fibonacci-anyon bridge; `2026-05-29_gray_hamming_router_lift`
  and the hypercube-tower files — **own** the Gray/routing lane.
- Pass 1908 — the similitude construction now identified as multiplication by `i`.
- Passes 2011–2015 (parallel track) — **own** the `D₈` witness.

## Still open

- `χ(H) = 9`.
- Hamiltonicity of the Fibonacci cube, and whether it matters here at all.
- The `D₈` reconstruction.
