# Passes 2023–2028 — the open converse reduces to a regulus, and reachability is a congruence

Six items, dug deep. Two are genuine advances: the candidate-orbit property —
open since Pass 1974 — is reduced to a two-root statement, and the genus-ladder
reachability turns out to be a clean congruence with a surprise about powers of 3.

---

## Pass 2023 — the candidate-orbit property reduces to a **regulus**

Pass 2021 restated the open converse per-line: for every `p ∈ M`, is
`M' ∩ L_p = σ_S(p)`? That is equivalent to `M'` being a **common transversal** of
the `q+1` spread lines that `M` meets. So: how many such transversals are there?

```text
q=3 : non-spread lines 30   common transversals: {2: 30}    all {M, sigma(M)}: 30/30
q=5 : non-spread lines 130  common transversals: {2: 130}   all {M, sigma(M)}: 130/130
q=7 : non-spread lines 350  common transversals: {2: 350}   all {M, sigma(M)}: 350/350
```

> **Exactly two, always — and they are `M` and `σ_S(M)`.**

That gives the converse immediately: a candidate `{M, M'}` forces `M'` to be a
common transversal; there are only two; `M' ≠ M`; hence `M' = σ_S(M)`. ∎

### And the mechanism, which is the interesting part

Counting transversals in the *full* projective space rather than only the
totally isotropic ones:

```text
q=3 : all PG(3,q) lines 130   (total transversals, of which t.i.) = {(4, 2): 30}
q=5 : all PG(3,q) lines 806   (total transversals, of which t.i.) = {(6, 2): 60}
```

> The `q+1` met spread lines form a **regulus**. Its opposite regulus supplies
> exactly `q+1` transversals in `PG(3,q)` — and the symplectic form cuts that
> down to exactly **two** totally isotropic ones.

So the proof chain is:

1. a candidate `{M, M'}` needs `M'` transversal to the `q+1` met spread lines;
2. in a regular spread those `q+1` lines form a regulus *(standard)*;
3. a regulus has exactly `q+1` transversals — its opposite regulus *(standard)*;
4. **of those `q+1`, exactly two are totally isotropic** *(verified `q = 3, 5`)*;
5. `M` and `σ_S(M)` are both t.i. transversals, and `M' ≠ M`, so `M' = σ_S(M)`. ∎

**Only step 4 is not standard**, and it is a two-root statement: the opposite
regulus is parameterised by `PG(1,q)`, "totally isotropic" is a quadratic
condition on that parameter, and a quadratic has 0, 1 or 2 roots. It has 2 here
— which is the same square/non-square dichotomy that produced `σ_S` in the first
place (`g² = μI`, `μ` a non-square, Pass 1908).

> The candidate-orbit property, open since Pass 1974, is now reduced from a
> global statement about frames to **"a quadratic form on `PG(1,q)` has exactly
> two roots"**.

With step 4, the `1/q` law is unconditional. Without it, it is unconditional for
the involution-generated subfamily and reduced to one quadratic for the rest.

---

## Pass 2024 — reachability is the Ringel–Youngs congruence

The repo's genus spectrum is exactly

```text
n mod 12 ∈ {0, 3, 4, 7}
```

which is the classical **Ringel–Youngs** condition: `K_n` has an orientable
triangular embedding iff `n ≡ 0, 3, 4, 7 (mod 12)` (Ringel & Youngs 1968,
settling the Heawood Conjecture). So the repo's "integer genus spectrum" is that
theorem, and the reachability filter of Pass 2018 is its intersection with
"`n − 1` is a prime power":

```text
reachable prime powers q < 400 :
  2, 3, 11, 23, 27, 47, 59, 71, 83, 107, 131, 167, 179, 191,
  227, 239, 243, 251, 263, 311, 347, 359, 383

residues mod 12 : {2, 3, 11}
  q = 11 (mod 12) : 11, 23, 47, 59, 71, 83, 107, 131, 167, 179, 191, ...
  q =  3 (mod 12) : 3, 27, 243
  q =  2 (mod 12) : 2
```

> **`q ≡ 11 (mod 12)` is the same as `12 | (q+1)`** — the residual `K_{q+1}` has
> a vertex count divisible by 12. That is the generic family.

### The surprise: only **odd** powers of 3

```text
3^k for k = 1..5 : 3, 9, 27, 81, 243
reachable        : True, False, True, False, True
```

`3^k ≡ 3 (mod 12)` for `k` odd and `≡ 9 (mod 12)` for `k` even. So:

> **In the substrate's own characteristic, the genus ladder is reached exactly at
> odd powers of three: `q = 3, 27, 243, …`** The even powers `9, 81` miss it.

`q = 3` is the substrate. The next rung in its own characteristic is `q = 27 = 3³`
(genus 50), not `q = 9`.

---

## Pass 2025 — the mod-12 clock's CRT split is geometrically real

`dccxxiii` lists `ℤ₁₂ = ℤ₃ × ℤ₄ = ℤ_q × ℤ_{q+1}` as one of the mod-12 clock's
appearances. Testing what the two factors do in `PGSp(4,3)`:

```text
order-12 class, INNER : g^4 (order 3) fixes 13 pts, 4 lines
                        g^3 (order 4) fixes  4 pts, 0 lines
order-12 class, OUTER : g^4 (order 3) fixes  4 pts, 1 line
                        g^3 (order 4) fixes  0 pts, 4 lines
```

> The `ℤ₃` factor is **point-rich** and the `ℤ₄` factor is **line-rich** — and in
> the outer class the asymmetry is total (4 points/0 lines vs 0 points/4 lines).

So the CRT split is not merely arithmetic: the two factors of the mod-12 clock
carry the point/line asymmetry, which is the same duality that makes degree 40
ambiguous (Pass 2003) and separates the point and line modules (Pass 1874).

---

## Pass 2026 — the `W(3,3)` route-load 66 is a count match, confirmed at source

`analysis/w33_toroidal_h6_66_bridge.py` draws its 66 from
`w33_balanced_selector_runtime_adapter.py`:

```text
direct_loads_are_12_each        : {12: 40}
ordered_nonlocal_loads_are_54_each : {54: 40}
66 = 12 + 54
```

That is a **scheduler load** per line — 12 direct plus 54 ordered non-local, over
40 lines. `W(3,3)`'s lines are `K₄`s with **six** edges. In `q`-primitives the
two 66s are

```text
W(3,3) route load : q(q+1) + 2q^3 = 12 + 54   at q = 3
K12 edges         : C(q+1,2)      = 66        at q = 11
```

Different formulas, different `q`, same number. **A count match**, and the bridge
should be read as the numerical bridge it is.

---

## Pass 2027 — percolation: why the lane does not attach here

Percolation on a disjoint union of complete graphs is trivial — each component
percolates independently at the `K_n` threshold. Since the residual set *is* such
a disjoint union (Pass 2016), the spread obstruction offers percolation nothing.

The repo's percolation lane (`css_genus_percolation_hinge`, BT500 threshold
ledger, `genus_percolation_information_hole`) is about the **toroidal/genus**
objects, not the residual decomposition. **No link established, and none
asserted.** That is a cleaner negative than "read, not integrated": the residual
structure is the wrong object to percolate on.

---

## Prior art

- **Ringel & Youngs (1968)** — **own** the `n ≡ 0,3,4,7 (mod 12)` triangular
  embedding condition and the genus of `K_n`.
- `dccxxiii` — **owns** the genus equation in `W(3,3)` primitives, the three
  clocks, the genus oscillator.
- BT1844 / `w33_toroidal_h6_66_bridge` — **own** the ladder and the route-load
  bridge; `w33_balanced_selector_runtime_adapter` — the 12/54 loads.
- Pass 1974 (parallel track) — **owns** the candidate-orbit property that Pass
  2023 reduces.
- Pass 2016 — the `K_{q+1}` decomposition, from the user.

## Still open

- Step 4: that exactly two of the `q+1` transversals are totally isotropic, for
  all odd `q`. Verified `q = 3, 5`.
- `χ(H) = 9`.
