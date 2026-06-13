# BT887 — The Gauge Group Factors as Color × Electroweak: 648 = 27:24

**Status: PROVEN (machine-verified, `analysis/bt887_color_electroweak_factorization.py`, data `data/bt887_color_electroweak_factorization.json`)**

The internal structure of the gauge group C(R) = 1⊕3⊕8 (BT876). It factors
exactly into color and electroweak parts, with the color-blindness of the
electroweak sector derived.

## The theorems

- **T1:** C(R) (order 648) = **3^{1+2} : SL(2,3)** = 27:24 — a **normal
  Heisenberg radical N = O₃** (order **27 = q^q**, the color part) with Levi
  quotient **SL(2,3) = 2A₄** (order **24 = f**, the electroweak part).
- **T2:** the color radical N acts on the 12 gauge bosons in 4 orbits of 3
  (the 4 lines through p₀), so its **invariant subspace is 4-dimensional —
  exactly the electroweak 1⊕3** — and it acts nontrivially on the
  complementary **8 (gluon octet)**. The W/Z/photon (electroweak bosons) are
  **color-blind**; the gluons carry the color radical's action.
- **T3:** so the substrate gauge group is **color (27 = q^q, the Heisenberg
  radical) ⋊ electroweak (24 = f, the SL(2,3) Levi)**, with 12 = k = 8 + 3 + 1.

## Reading

The Standard-Model gauge group's two-tier structure is the substrate's
radical/Levi decomposition of the local gauge group C(R):

| part | substrate object | order | gauge content |
| --- | --- | --- | --- |
| color | Heisenberg radical 3^{1+2} = O₃ | 27 = q^q | SU(3), the gluon octet 8 |
| electroweak | Levi SL(2,3) = 2A₄ | 24 = f | SU(2)×U(1), the 1⊕3 |

The color-blindness of the electroweak bosons — a defining SM fact — is here a
theorem: the color radical fixes the electroweak subspace pointwise (the 4
lines through p₀ are color-orbits, the W/Z/γ are constant-on-line = color
singlets). And the two tier sizes are the substrate's signature integers
27 = q^q (color/Heisenberg) and 24 = f (electroweak/24-cell). The gauge group
is not SU(3)×SU(2)×U(1) as a direct product but the *semidirect* color⋊electroweak
— color as the normal radical, electroweak as the Levi — exactly the structure
of a parabolic.

## The gauge picture (BT876–887)

```text
gauge group   C(R) = 27:24 = color ⋊ electroweak          (BT887)
  color       3^{1+2} = O₃, order q^q = 27, the gluon 8
  electroweak SL(2,3) Levi, order f = 24, the 1⊕3
module        1⊕3⊕8 = U(1)×SU(2)×SU(3)                    (BT876)
center        = generations Z₃                            (BT880)
connection    flat on lines, quaternionic-curved on Q     (BT882/883)
```

## Open

- The U(1) hypercharge as a specific element of the SL(2,3) Levi's torus, and
  the weak-mixing angle from the 3-vs-(1) embedding in the Levi.
- The color radical being the Heisenberg group 3^{1+2} = the same group that
  carries the matter shell (BT858) — color and the matter 27 share the
  Heisenberg structure; make the identification precise.
