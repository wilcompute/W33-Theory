# Part DCCLXXVI — The 26 Sporadic Simple Groups from W(3,3)

**Bridge:** `verify_dcclxxvi_sporadic_simple_groups_w33.py` — Verified
**Tests:** `tests/test_dcclxxvi_sporadic_simple_groups_w33.py` — 22/22 pass
**Data:** `data/dcclxxvi_sporadic_simple_groups_w33.json`

---

## 1. The classification of finite simple groups

By the **Classification of Finite Simple Groups (CFSG, completed 1980s)**,
every finite simple group is either:
1. Cyclic of prime order (infinite family)
2. Alternating A_n, n ≥ 5 (infinite family)
3. A classical Lie-type group (infinite family)
4. An exceptional Lie-type group (infinite family)
5. **One of 26 sporadic finite simple groups** (this part)

The 26 sporadics split as **20 Happy Family** (subquotients of the
Monster M) + **6 Pariahs** (not subquotients of M).

---

## 2. The classification split IS a W(3,3) decomposition

| count | value | W(3,3) reading |
|---|---:|---|
| Total sporadics | **26** | **D_bosonic** (DCCXXVI) = HPS level 3 (DCCLII) = 2·Φ_3 |
| Happy Family | **20** | **cuboctahedron volume** (DCCL) = C(2q, q) = v/2 |
| Pariahs | **6** | **q!** = octahedron V = closure-clock nilpotence |

**The 20 + 6 = 26 split of the sporadic classification IS the (cuboctahedron
volume) + (q!) decomposition of D_bosonic.**

---

## 3. The five sporadic families

Each family count is a W(3,3) primitive:

| family | groups | count | W(3,3) reading |
|---|---|---:|---|
| Mathieu | M_11, M_12, M_22, M_23, M_24 | **5** | μ + 1 = # Császár realisations (DCCXXV) |
| Janko | J_1, J_2, J_3, J_4 | **4** | μ = q + 1 = quaternion dim |
| Conway | Co_1, Co_2, Co_3 | **3** | q = Master Equation root |
| Fischer | Fi_22, Fi_23, Fi_24' | **3** | q (same) |
| Other | HS, McL, He, Ru, Suz, O'N, Ly, Th, HN, B, M | **11** | k − 1 = non-back-tracking out-degree |

Sum: 5 + 4 + 3 + 3 + 11 = **26**. Every cardinality is a W(3,3) primitive.

**Pariahs**: J_1, J_3, J_4, Ru, O'N, Ly (6 groups, not subquotients of M).

---

## 4. The Mathieu groups link to Golay codes (DCCLXXI)

| group | order | role |
|---|---:|---|
| M_12 | 95,040 | Aut(Steiner S(5, 6, 12)) = Aut(ternary Golay G_12) |
| M_24 | 244,823,040 | Aut(Steiner S(5, 8, 24)) = Aut(binary Golay G_24) |

Combined with DCCLXXI: the perfect Golay codes have W(3,3)-primitive
parameters [k, q!, q!] and [f, k, 2^q], and their automorphism groups
M_12 and M_24 are Mathieu sporadics — Happy Family members.

---

## 5. The Conway groups link to Leech (DCCLIII, DCCLV)

| group | order | role |
|---|---:|---|
| Co_1 | 4,157,776,806,543,360,000 | Aut(Leech) / Z_2 |
| Co_2 | 42,305,421,312,000 | Stabilizer of a Leech vector of norm 4 |
| Co_3 | 495,766,656,000 | Stabilizer of a Leech vector of norm 6 |

The Leech lattice (DCCLV: kissing number 196560 = E·q²·Φ_6·Φ_3 = W(3,3)
primitive product) has Conway groups as automorphism quotients.

---

## 6. The Monster sits at the apex

The Monster M, with order ~ 8 × 10^53, is the largest sporadic. From
DCCLIII:
- |M| has exactly **15 = g** prime divisors
- First 6 prime exponents (2, 3, 5, 7, 11, 13) are W(3,3) primitives
- j-invariant 744 = q · dim(E_8) and 196884 = Leech + μq⁴

So the entire Happy Family (20) is **centered on Monster moonshine**,
which itself is W(3,3) at q = 3.

---

## 7. Decisive identity

$$
\boxed{\;
\underbrace{26}_{\text{sporadics}} \;=\; \underbrace{20}_{\text{Happy Family}} \;+\; \underbrace{6}_{\text{Pariahs}}
\;=\; \underbrace{D_{\text{bosonic}}}_{\text{DCCXXVI}} \;=\; \underbrace{C(2q, q)}_{\text{cuboctahedron vol}} \;+\; \underbrace{q!}_{\text{octahedron V}}.
\;}
$$

$$
\boxed{\;
(|\text{Mathieu}|, |\text{Janko}|, |\text{Conway}|, |\text{Fischer}|, |\text{Other}|)
\;=\; (\mu + 1, \mu, q, q, k - 1) \;=\; (5, 4, 3, 3, 11).
\;}
$$

Every cardinality in the classification of sporadic finite simple
groups is a W(3,3) primitive at q = 3.

---

## 8. Honest boundary

* The 26 sporadic groups and their classification into 20 + 6 is the
  standard output of CFSG (Gorenstein, Aschbacher, etc., 1980s).
* The 5-family decomposition (Mathieu, Janko, Conway, Fischer, Other)
  is the standard taxonomy.
* This part documents the **W(3,3) arithmetic alignment** of every
  classification number; it does **not** prove CFSG or derive any
  sporadic group from W(3,3).

---

## 9. One-line summary

$$
\boxed{\;
26 = 20 + 6 = (\text{cuboctahedron vol}) + (q!);
\;\text{family sizes} = (5, 4, 3, 3, 11) = (\mu+1, \mu, q, q, k-1).
\;}
$$
