## Passes 2716–2723 — the self-entangled photon reads a **character**, and its alphabet is ternary

The user's note that self-entanglement is not yet fully figured out is right, and reading
the carrier section against this session's character work says something the paper does
not state.

---

## Pass 2716 — what self-entanglement actually is, from the paper

**Stage A (spatial):** a diagonal photon meets a PBS,
`(|H⟩+|V⟩)/√2 ↦ (|H,a⟩+|V,b⟩)/√2`. Path and polarisation are maximally entangled
**within one photon**. That `ℂ⁴` is the Witting carrier.

**Stage B (temporal):** a tritter *is* `F₃`; a three-bin delay ladder `(0, τ, 2τ)` defines
past and future; one EOM applies `CX_{p→f}`. The temporal Bell qutrit is

```text
|Omega> = CX_{p->f} (F_3 (x) I) |0>_p |0>_f = (1/sqrt3) sum_j |j>_p |j>_f
```

and inserting `U` in the future arm gives the **trace–Choi witness**

```text
V(U) = |Tr U| / 3,      V(F_3) = 1/3,     V(X) = V(Z) = 0
```

> *"the photon implements the Choi–Jamiołkowski isomorphism on itself: it measures
> channels against its own past."*

**So the machine's readout is a character.** That is the sentence that connects
self-entanglement to everything this session has computed.

---

## Pass 2717 — a wrong turn, caught by a sanity check

I first computed `|Tr U|` in the **9-dimensional** Weil representation of `Sp(4,3)`,
reasoning that `ℂ⁹` is the past⊗future space. Result: `|Tr U|² ∈ {1, 3, 9, 27, 81}` — all
powers of 3, which is a real and pretty fact about the Weil character.

**But it gives `V(I) = 9/3 = 3`, and a visibility cannot exceed 1.**

The `U` in `V(U) = |Tr U|/3` is inserted *in the future arm*: it acts on `ℂ³`, not `ℂ⁹`.
Wrong object, caught by the one check that was free — the identity must read `V = 1`.

*(The `{1,3,9,27,81}` fact is recorded as a Weil-character observation, unattached to the
visibility.)*

---

## Pass 2718 — the correct answer: **the readout alphabet is ternary**

The single-qutrit Clifford group mod Pauli is `SL(2,3)`, order 24, acting on `ℂ³` by its
degree-3 representation. That character, class by class:

```text
order  size   Tr U    V = |Tr U|/3
  1      1      3        1
  2      1      3        1
  4      6     -1       1/3
  3      4      0        0
  6      4      0        0
  3      4      0        0
  6      4      0        0
```

```text
|Tr U|^2 in {0, 1, 9}        so        V in {0, 1/3, 1}
```

> **The self-entangled photon's visibility takes exactly three values.** Not by design —
> the degree-3 character of `SL(2,3)` has exactly three distinct absolute values, and the
> readout is that character.

**A qutrit machine whose own measurement is ternary**, and ternary for a representation-
theoretic reason rather than an engineering one.

Both of the paper's stated checks fall out: `V(F₃) = 1/3` is the order-4 class where
`Tr = −1`, and `V(X) = V(Z) = 0` because Paulis are traceless.

### The output distribution, which the paper does not give

Under uniform random Clifford:

```text
V = 1     :  2 of 24  =  1/12
V = 1/3   :  6 of 24  =  1/4
V = 0     : 16 of 24  =  2/3
```

> **Two thirds of Clifford gates are invisible to the machine.** A random Clifford returns
> `V = 0` more often than not, so the trace-Choi witness is a *sparse* readout: it
> distinguishes the identity coset and the order-4 class and sees nothing else.

That is a concrete statement about how much a single self-entangled photon can learn about
a gate in one shot, and it is forced by `SL(2,3)`'s character table.

---

## Pass 2719 — why this bears on the rest of the session

The machine measures `|χ(U)|`. Everything this session computed — Frobenius–Schur
indicators, permutation characters, the Weil split `9 = 4 + 5`, the central-character
partition — is character theory of the same groups.

> **The chiral/achiral split of Pass 2448 is a split of the machine's own readout.** For
> two qutrits the `ℂ⁹` carries `χ₉ = χ₄ + χ₅`, faithful plus inflated, so a two-qutrit
> trace witness reads a sum of one chiral and one achiral term.

Not built, and not claimed as a protocol — but it is the first place where the session's
representation theory and the machine's physical readout are the *same object* rather than
two things that share a group.

---

## Pass 2720 — the four items not done

`CX_{p→f}` RTL (the instruction that *creates* `|Ω⟩`, and the natural next build), the
`μ₄/μ₆` re-homing, the transceiver, and lines 1220–2400. The batch went to
self-entanglement, as asked.

---

## Pass 2721 — ledger

| claim | status |
|---|---|
| readout is the Choi witness `V = \|Tr U\|/3` | the paper's, quoted |
| `V` computed in the 9-dim Weil rep | **wrong object — `V(I) = 3 > 1`** |
| `\|χ₉\|² ∈ {1,3,9,27,81}` | true, but unattached to `V` |
| `SL(2,3)` degree-3 character gives `V ∈ {0, 1/3, 1}` | **proved** |
| `V(F₃) = 1/3`, `V(X) = V(Z) = 0` | **both reproduced** |
| distribution `1/12, 1/4, 2/3` | **new — not in the paper** |
| two-qutrit witness reads `χ₄ + χ₅` | observed, not built |

---

## Prior art

- `photonic_holonet_body.tex` §"The carrier" — owns Stages A and B, `|Ω⟩`, and the
  trace-Choi witness. Witness `bt820_self_entanglement_protocol.py`.
- Choi–Jamiołkowski — classical.
- Pass 2448 (mine) — the `9 = 4 + 5` Weil split.

## Still open

- `CX_{p→f}` in RTL — four of eight instructions.
- Whether the sparse readout (`2/3` of Cliffords invisible) is a limitation of the
  single-shot witness or of the architecture.
- The `μ₄/μ₆` re-homing, the transceiver, lines 1220–2400.
