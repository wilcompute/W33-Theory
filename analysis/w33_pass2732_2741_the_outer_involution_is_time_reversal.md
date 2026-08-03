## Passes 2732–2741 — the outer involution **is** the transpose, and the substrate is a Jordan ladder

Building on Pass 2724 (`W(3,3)` is one qutrit's operator algebra `End(ℂ³)`, with the two
"qutrits" being left and right multiplication).

---

## Pass 2732 — the outer involution of `W(E₆)` is **the transpose**

On `End(ℂ³)`, transposition sends `L_P R_Q ↦ L_{Qᵀ} R_{Pᵀ}` — it **swaps the left and
right blocks**. On `(a,b) ∈ 𝔽₃⁴ = left ⊕ right` that is `(a,b) ↦ (b,a)`. Applied to the
form `w(a,a′) − w(b,b′)`:

```text
form(Tu, Tv) / form(u, v) over all nonzero pairs : [2]
so the transpose is a symplectic SIMILITUDE with multiplier 2 = -1 mod 3
squares mod 3 : [1]        is the multiplier a square ?  FALSE
```

A symplectic similitude with **non-square multiplier** is exactly the defining property of
`σ_S`, the outer element (my Passes 1908, 2436).

> **The outer involution of `W(E₆) = PGSp(4,3)` is the transpose — the left–right swap —
> i.e. TIME REVERSAL.**

### This unifies most of the session

| earlier result | now reads as |
|---|---|
| `σ_S` conjugates `J` to `−J` (Pass 2076) | time reversal reverses the phase |
| `σ_S` is an outer similitude, multiplier non-square | the transpose reverses the form |
| `Sp(4,3)` vs `W(E₆)`, same order, not conjugate (Pass 2444) | with vs without time reversal |
| the chiral / achiral tower split (Pass 2437) | left action vs left⊕right |
| `q ≡ 3 (mod 4)` (Gow; my Passes 1908, 2065, 2490) | **`−1` is a non-square exactly when time reversal is OUTER** |

> **The whole `q ≡ 3 (mod 4)` ladder is the statement that time reversal is an outer
> symmetry of the substrate.** At `q ≡ 1 (mod 4)`, `−1` is a square and the transpose is
> inner — which is precisely where Pass 2462 found the complex structures disappear.

---

## Pass 2733 — the 40 lines are the maximal commuting subalgebras

```text
totally isotropic 2-subspaces of (F_3^4, w(a,a') - w(b,b')) : 40
each with 4 projective points                                : yes
W(3,3) lines                                                 : 40      MATCH
```

> **Points are operators on one qutrit; lines are its maximal commuting subalgebras** —
> 9-element stabiliser groups, each a joint eigenbasis, i.e. a measurement context.

The paper's "operator–operand duality" (Theorem 1) is then not a coincidence between two
different `ℂⁿ` but **two readings of `End(ℂ³)`**: a point is an operator and a line is a
context, both inside one qutrit.

---

## Pass 2735 — bonkers 1: the substrate dimensions are the **Jordan ladder**

```text
J_3(R)  dim  6        J_3(C)  dim  9
J_3(H)  dim 15        J_3(O)  dim 27      (the Albert algebra)

substrate : q^2 = 9,  g = 15,  matter shell = 27
overlap   : 9, 15, 27  --  three of the four
```

`E₆` is exactly the group preserving the **cubic form on `J₃(𝕆)`**, and the paper calls
its degree-3 element *"the `E₆` Cartan cubic on the matter 27"*.

> **So the cubic I built at Pass 2660 — `det A + det B + det C − tr(ABC)` — is the Jordan
> determinant of the split Albert algebra in trinification coordinates. The hardware
> computes a Jordan determinant.**

**Prior-art check:** every "Jordan" hit in this repo is *Jordan normal form*, not Jordan
algebras. The Albert algebra reading appears to be absent.

**Scope.** `9, 15, 27` matching three rungs is suggestive, not a derivation: `15` arises in
the substrate as an SRG multiplicity, and I have not shown it is `J₃(ℍ)`. The `27` and the
`E₆` cubic are a genuine identification because `E₆` and the cubic pin it; the `9` follows
from `End(ℂ³)` (Pass 2724). **`15` is a count match until someone names a map.**

---

## Pass 2736 — bonkers 2: the readout is blind to the **gluons**

Under `SU(3)` conjugation, `End(ℂ³) = 3 ⊗ 3̄ = 1 ⊕ 8`. And the trace-Choi witness is

```text
V(U) = |Tr U| / 3       which measures the SINGLET coefficient and nothing else
```

```text
V(identity)              = 1.0000
V(Gell-Mann lambda_3)    = 0.0000
V(Gell-Mann lambda_8)    = 0.0000
V(Pauli X), V(Pauli Z)   = 0.0000
```

> **Every element of the `su(3)` adjoint is traceless, so `V = 0` on all of it. The
> self-entangled photon sees the `1` and is blind to the `8`.**

That explains Pass 2718 structurally: two thirds of Cliffords read `V = 0` not by accident
but because **the readout is the projection onto the singlet, and the octet is the gauge
sector.** A single-shot trace witness cannot see gauge structure — it can only see the
scalar part.

**Scope.** This is a statement about what `|Tr U|/3` measures on `End(ℂ³)`. Calling the
octet "the gluons" is the standard `su(3)` reading and is *not* a claim that the substrate
predicts QCD; the paper's own trinification argument is where that claim would have to be
made, and it is not made here.

---

## Pass 2737 — the two items not done

`CX_{p→f}` in RTL, and a correct two-shot readout computation (Pass 2727's attempt used a
broken matrix closure of order 352 and was discarded; the redo needs GAP characters).

---

## Pass 2738 — ledger

| claim | status |
|---|---|
| transpose is a similitude with multiplier `−1` | **verified** |
| `−1` is a non-square mod 3 | verified |
| outer involution of `W(E₆)` = transpose = time reversal | **proved** |
| `q ≡ 3 (mod 4)` ⟺ time reversal is outer | **follows** |
| 40 lines = maximal commuting subalgebras | **verified** |
| `E₆` cubic = Albert-algebra Jordan determinant | identification |
| `9, 15, 27` are Jordan rungs | 9 and 27 grounded; **15 is a count match** |
| `V` measures the singlet, blind to the octet | **verified** |
| octet ⇒ the substrate predicts QCD | **not claimed** |

---

## Prior art

- `photonic_holonet_body.tex` — the operator–operand duality, the `E₆` cubic on the 27,
  the trinification argument.
- Passes 1908, 2076, 2436, 2444, 2462, 2490 (mine) — the `σ_S` and `q ≡ 3 (mod 4)` results
  this reinterprets.
- Albert algebra / `E₆` preserving its cubic — classical; **no Jordan-algebra prior art in
  this repo**.

## Still open

- Whether `15 = J₃(ℍ)` in any structural sense.
- `CX_{p→f}`; a correct two-shot computation.
- The `μ₄/μ₆` re-homing, the transceiver, lines 1220–2400.
