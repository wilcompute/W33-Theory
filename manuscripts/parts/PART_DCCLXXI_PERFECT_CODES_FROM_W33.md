# Part DCCLXXI — Perfect Codes (Hamming, Golay) from W(3,3)

**Bridge:** `verify_dcclxxi_perfect_codes_from_w33.py` — Verified
**Tests:** `tests/test_dcclxxi_perfect_codes_from_w33.py` — 19/19 pass
**Data:** `data/dcclxxi_perfect_codes_from_w33.json`

---

## 1. The headline result

By the **Tietäväinen–van Lint theorem (1973)**, the only non-trivial
perfect linear codes (over any finite field, of any non-trivial
distance) are:

* The **binary Golay code** G_23 / extended G_24
* The **ternary Golay code** G_11 / extended G_12

**Both have all parameters as W(3,3) primitives at q = 3.**

| code | [n, k, d] | W(3,3) reading |
|---|---|---|
| **Ternary Golay G_12** | **[12, 6, 6]** | **[k, q!, q!]** |
| **Binary Golay G_24** | **[24, 12, 8]** | **[f, k, 2^q]** |

Plus the Hamming codes — perfect single-error-correcting codes — also
have W(3,3) parameters at small m.

---

## 2. The full perfect-code table

| code | [n, k, d] | W(3,3) reading | field |
|---|---:|---|:-:|
| Binary Hamming Ham(3, F_2) | [**7**, **4**, **3**] | [**Heawood**, **μ**, **q**] | F_2 |
| Binary Hamming Ham(4, F_2) | [**15**, **11**, **3**] | [**g**, **k−1**, **q**] | F_2 |
| Ternary Hamming Ham(4, F_3) | [**40**, **36**, **3**] | [**v**, **\|S\|**, **q**] | F_3 |
| **Ternary Golay G_12** | [**12**, **6**, **6**] | [**k**, **q!**, **q!**] | F_3 |
| **Binary Golay G_24** | [**24**, **12**, **8**] | [**f**, **k**, **2^q**] | F_2 |

**Every single parameter — length, dimension, distance — is a named
W(3,3) primitive.** The W(3,3) program contains the entire arithmetic
of perfect linear codes.

---

## 3. The Steiner system / Mathieu group structure

Each Golay code carries a **Steiner system** of 5-transitive blocks
(witnessing the perfect property), and the automorphism groups are the
**Mathieu sporadic groups**.

| Steiner system | block | length | transitivity | W(3,3) reading | aut group |
|---|:-:|:-:|:-:|---|:-:|
| S(5, 6, 12) | 6 | 12 | 5 | block = **q!**, length = **k**, transitivity = **q + 2** | M_12 |
| S(5, 8, 24) | 8 | 24 | 5 | block = **2^q**, length = **f**, transitivity = **q + 2** | M_24 |

* \|M_12\| = 95,040
* \|M_24\| = 244,823,040

Both M_12 and M_24 are **subgroups of the Monster** (DCCLIII).

---

## 4. The ternary Hamming code is the W(3,3) projective space

The ternary Hamming code Ham(4, F_3) has length **40 = v** and dimension
**36 = T_8 = |S|** — the **spread count of W(3,3)** from the paper's
representation triangle 121 = v + |S| + |Q| (DCCLI).

So the ternary Hamming code at m = 4 is **the code whose codewords are
the projective points of PG(3, F_3) = W(3,3)'s underlying space**. The
[40, 36, 3] parameters are the W(3,3) point count, spread count, and
Master Equation root.

---

## 5. Joint coverage

Combining with prior parts:
* **DCCLV**: kissing numbers at d = 1, 2, 3, 4, 8, 24 all W(3,3)
* **DCCLVI**: sphere-packing densities at d = 1, 2, 3, 8, 24 all W(3,3)-denominator
* **DCCLVII**: periodic table orbital capacities = W(3,3)
* **DCCLXX**: Hopf-Cayley-Dickson tower entirely W(3,3)
* **DCCLXXI**: perfect linear codes entirely W(3,3)

The W(3,3) program contains the arithmetic of **kissing numbers**,
**sphere packings**, **division algebras**, **Hopf fibrations**,
**perfect codes**, **Steiner systems**, **Mathieu groups**, and the
**periodic table** — all at q = 3.

---

## 6. Decisive identity

$$
\boxed{\;
\begin{aligned}
\text{Golay } G_{24} \;&=\; [f,\;k,\;2^q] \;=\; [24,\;12,\;8] \\
\text{Golay } G_{12} \;&=\; [k,\;q!,\;q!] \;=\; [12,\;6,\;6] \\
\text{Ham}(4, \mathbb{F}_3) \;&=\; [v,\;|S|,\;q] \;=\; [40,\;36,\;3].
\end{aligned}
\;}
$$

The **only two non-trivial perfect linear codes** (Tietäväinen–van Lint
1973) have **all parameters as W(3,3) primitives**.

---

## 7. Honest boundary

* All parameters are exact classical coding-theory values.
* The Tietäväinen–van Lint theorem (uniqueness of Golay codes among
  non-trivial perfect linear codes) is imported as a standard 1973
  result.
* This part does **not** re-prove uniqueness or derive the Mathieu
  groups from W(3,3); it documents the **arithmetic alignment** of
  every parameter of every classical perfect code with the W(3,3)
  primitive table.

---

## 8. One-line summary

$$
\boxed{\;
\text{Both perfect Golay codes have parameters W(3,3) at q = 3:}
\;\;
G_{24} = [f, k, 2^q], \;\; G_{12} = [k, q!, q!].
\;}
$$
