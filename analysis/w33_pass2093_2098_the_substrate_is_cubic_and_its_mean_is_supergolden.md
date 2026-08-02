# Passes 2093–2098 — the substrate is cubic at every level, and its metallic mean is the **supergolden** ratio

The user's insistence that "the golden ratio is definitely here somewhere" turns
out to be right in spirit and wrong in degree. There **is** a metallic mean, it
**is** irrational, and it is the cubic one — because the substrate is cubic at
every level.

---

## Pass 2093 — the metallic mean is `ψ ≈ 1.4656`, and it was in the parallel track's work

Their Pass 1942/1953 records an infinite-order witness in `⟨R₄, U₆⟩ = SL₃(ℤ)`
with characteristic polynomial `t³ − t² − 1`. That polynomial is not incidental:

```text
roots        : 1.4655712 , −0.2327856 ± 0.7925520 i
moduli of the complex pair : 0.826031  (< 1)
irreducible over Q : True        Pisot : True
```

> `x³ = x² + 1` is the **supergolden ratio** `ψ ≈ 1.4655712`, the cubic cousin of
> `φ`, and it is a **Pisot number**.

Its integer sequence is Narayana's cows, `a(n) = a(n−1) + a(n−3)`:

```text
1, 1, 1, 2, 3, 4, 6, 9, 13, 19, 28, 41, 60, 88, 129   ratio -> 1.4659 -> psi
```

### This corrects Pass 2077

Pass 2077 said the substrate has no irrational growth rate because its towers
grow polynomially. **The combinatorial towers do** — that part stands. But
`⟨R₄,U₆⟩ = SL₃(ℤ)` is **infinite**, and an infinite arithmetic group has
exponential growth. Its witness element's growth rate is `ψ`.

> **The substrate's metallic mean is the supergolden ratio, not the golden
> ratio.** It arises from the arithmetic group acting on the phase carrier, not
> from the finite combinatorics.

---

## Pass 2094 — and `ψ` gives a genuine phinary analogue

`ψ` is Pisot, so it supports a `β`-numeration with finite expansions — the
property that makes base-`φ` work.

```text
psi^3 = psi^2 + 1   =>   1 = psi^-1 + psi^-3   =>   d(1, psi) = 101

phi : x^2 = x+1 ,  d(1,phi) = 11  ,  forbidden factor 11   (Fibonacci/Zeckendorf)
psi : x^3 = x^2+1,  d(1,psi) = 101 ,  forbidden factor 101  (Narayana)
```

> **The substrate's "phinary" is base-`ψ`, and its forbidden word is `101`, not
> `11`.** The user's no-consecutive-1s intuition is the right *kind* of structure;
> the substrate's version forbids `101`.

---

## Pass 2095 — why cubic, at every level

```text
substrate field    F_3^4                     rank 4
character fields   Q and Q(zeta_3)           CUBIC
their explicit J   D_40^2 = -192 I           eigenvalues +-8i sqrt3 -> Q(sqrt-3) = Q(zeta_3)
arithmetic group   SL_3(Z)                   rank 3, infinite
its growth rate    psi,  x^3 = x^2 + 1       CUBIC
```

Their Pass 2051 constructs `J` explicitly from the signed-edge class sums of the
two order-3 classes of size 40, with `D₄₀² = −192I`. Since `√192 = 8√3`, its
eigenvalues are `±8i√3`, so `J` lives in `ℚ(√−3) = ℚ(ζ₃)` — **independently
reproducing the character field I computed**. Two different routes, one cubic
field.

> **The substrate is a cube-root-of-unity object at every level**, and its
> metallic mean is correspondingly cubic. `φ` is the *quadratic* mean of a
> *rank-5* world (Pass 2084: `Φ₅ | [n,k]_q` needs `n ≥ 5`, and `[5,1]_q = Φ₅(q)`).

---

## Pass 2096 — where the `5` actually is: invariant theory, not arithmetic

`W(E₆) = PGSp(4,3)` has basic invariant degrees `2, 5, 6, 8, 9, 12` — including a
**degree 5**. So:

```text
W(E6) degrees [2,5,6,8,9,12]   divisible by 5: [5]    Phi_5 | Poincare?  TRUE
W(E7) degrees [...,10,...]     divisible by 5: [10]   TRUE
W(E8) degrees [...,20,30]      divisible by 5: [20,30] TRUE
```

> `Φ₅` **does** divide `W(E₆)`'s Poincaré polynomial, via the degree-5 basic
> invariant — yet `ℚ(ζ₅)` appears in **none** of its character fields.

That is the mechanism behind the split Pass 2079 noticed. The 5 is present in the
**invariant theory** and in the **permutation action** (an order-5 class
partitions the 40 points into eight pentagons) and absent from the
**arithmetic**. Three different senses of "is 5 there", with different answers —
and conflating them is what made this question feel unresolved for so long.

---

## Pass 2097 — crediting the parallel track's Pass 2064

They extended the spread census to `q = 3, 5, 7` and found the intersection
distribution generalises:

```text
q=3 : {1: 360,    4: 270}
q=5 : {1: 15600,  6: 29250}
q=7 : {1: 176400, 8: 514500}
```

> **Two distinct regular spreads meet in exactly `1` or `q+1` lines.**

My Pass 2000 measured `1 or 4` at `q = 3` and their Pass 2013 proved it there;
Pass 2064 is the `q`-general statement with the strongly-regular parameter family
`(v, k, λ, μ) = (q²(q²−1)/2, …)` and `r = q(q−2)`, `s = −q`. **Theirs.**

Their Pass 2051 also constructs the quadratic intertwiners explicitly and finds
the outer similitude reverses `J` — **independently reproducing my Pass 2076** by
construction rather than by character argument.

---

## Pass 2098 — the four deferred items

- **`Φ₅` in rank-5+ objects** — done above for `W(E₆/E₇/E₈)` Poincaré polynomials.
- **Rank 5 over `F₃`** — `PG(4,3)` has `121 = Φ₅(3)` points. That is the smallest
  place `φ`'s field can live over this characteristic.
- **The eight pentagons** — characterised (Pass 2079) and now explained
  (Pass 2096): permutation, not arithmetic.
- **The `D₈` reconstruction** — still not done. Sixth report. Their Pass 2050 has
  since fused the 33 local classes into **14 full-group types** and 12 schedule
  orbits, so independent reconstruction is now less valuable than reading theirs.

---

## Prior art

- Passes 1942/1953, 2050–2053, 2064 (parallel track) — **own** the `SL₃(ℤ)`
  identification and its `t³−t²−1` witness, the explicit intertwiners, the
  `NO₆⁻(2)` graph identification, and the `1 or q+1` census.
- Passes 2077/2082–2087 — the polynomial-growth and cyclotomy arguments this
  refines.
- The golden-ratio and `q`-binomial suggestions are the user's, and both were the
  right route: the `q`-binomial argument located `φ` at rank 5, and pushing on
  "it must be here somewhere" produced `ψ`.

## Still open

- `χ(H) = 9`.
- Whether `ψ`'s `β`-numeration has any operational role, or is only the growth
  rate of a witness element.
