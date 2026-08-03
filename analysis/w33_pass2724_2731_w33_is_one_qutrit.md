## Passes 2724–2731 — `W(3,3)` is **one** self-entangled qutrit, not two

The suggestion was that `W(3,3)` might not be a two-qutrit commutation geometry at all —
that it could be a single self-entangled qutrit giving the *appearance* of two, past and
future. That is correct, and it is provable in four lines.

---

## Pass 2724 — the identification

Choi–Jamiołkowski says

```text
C^9 = C^3 (x) C^3 = End(C^3)
```

— the `ℂ⁹` is the **operator algebra of one qutrit**. Under that identification the two
tensor factors are not two particles: they are **left multiplication and right
multiplication** on a single carrier.

```text
single-qutrit Pauli group mod phase : X^a Z^b,  (a,b) in (Z/3)^2,  order 9
left-mult (x) right-mult            : (Z/3)^2 + (Z/3)^2 = (Z/3)^4,  order 81
projective classes                  : (81 - 1)/2 = 40
W(3,3) points                       : 40
```

Two operators `L_P R_Q` and `L_{P'} R_{Q'}` commute up to a phase whose exponent is

```text
w(a,a') - w(b,b')          w = the single-qutrit symplectic form
```

— the **minus sign** because right multiplication is the opposite algebra. Building the
40 projective classes and that form:

```text
commutation graph of the 40 (left,right) classes
  degrees : {12}
  SRG parameters (v, k, lambda, mu) = (40, 12, 2, 4)
  W(3,3) is SRG(40,12,2,4)          MATCH: True
```

> **`W(3,3)` is the commutation geometry of one qutrit's two-sided operator algebra.**
> The "two qutrits" are the left and right actions on a single carrier — past and future.
> No second particle is required anywhere in the construction.

---

## Pass 2725 — what the minus sign is doing

The form is `w(a,a') − w(b,b')`, not `w(a,a') + w(b,b')`. That is forced: right
multiplication acts through the **opposite** algebra, so its symplectic contribution
enters with reversed orientation.

> **The past–future distinction is a sign.** Left and right multiplication carry the same
> form with opposite orientation, and the hyperbolic sum of the two is exactly the `W(3,3)`
> form.

This is the same shape as the chirality result from earlier in the session: an orientation
reversal between two copies of one structure. There the reversal was `σ_S` conjugating `J`
to `−J`; here it is right-multiplication reversing `w`. **Whether they are the same
reversal is not established** — flagged, not claimed.

It also explains the paper's own care at line 42: `Sp(4,3)` and `W(E₆)` both have order
51840 but *"the two extensions must not be conflated"*. On this reading the `F₃⁴` is
`(left) ⊕ (right)` and the outer involution is naturally the **left–right swap**, i.e.
the transpose — time reversal.

---

## Pass 2726 — why this is not merely a restatement

The paper already says the two registers are past and future time bins of one photon. What
is new is that **the geometry does not need the tensor product at all**: the 40 points are
the projective classes of `End(ℂ³)`'s Pauli structure, and the `SRG(40,12,2,4)` comes out
of a one-qutrit computation with a sign.

Consequences worth testing:

- The 40 points are **operators on one qutrit**, so the "state/operator duality" of
  Theorem 1 becomes an identity between two readings of `End(ℂ³)` rather than a
  coincidence between two different `ℂⁿ`.
- Self-entanglement is then not a preparation trick but the statement that **a qutrit's
  operator algebra is nine-dimensional**, which is automatic.
- And the machine's readout `V(U) = |Tr U|/3` is the normalised trace on `End(ℂ³)` — the
  natural inner product of exactly this algebra.

---

## Pass 2727 — a failed computation, reported

I attempted a two-shot protocol to beat the `2/3` blindness of Pass 2718: measure
`(|Tr U|, |Tr UV|)` for a fixed probe `V` and count distinguishable signatures. It
reported `4 → 11`.

**Discarded.** My matrix closure produced **352** elements, which is not the order of any
single-qutrit Clifford group (mod Pauli it is 24; with phases 216 or 648). The `key`
normalisation — dividing by the largest-magnitude entry — is unstable when two entries tie,
so the closure ran away. The numbers are on the wrong group and mean nothing.

Pass 2718's ternary alphabet stands: that came from GAP's `SL(2,3)` character table, not
from a matrix closure.

---

## Pass 2728 — ledger

| claim | status |
|---|---|
| `ℂ⁹ = End(ℂ³)` under Choi | classical |
| left×right Paulis give `(81−1)/2 = 40` classes | **verified** |
| their commutation graph is `SRG(40,12,2,4)` | **verified — it is `W(3,3)`** |
| the past–future split is the sign in `w(a,a′) − w(b,b′)` | proved |
| that sign is the chirality reversal | **flagged, not claimed** |
| the outer involution is the left–right swap | **plausible, untested** |
| two-shot protocol gives 11 signatures | **discarded — group order 352 is wrong** |
| `CX`, `μ₄/μ₆`, transceiver, lines 1220–2400 | not done |

---

## Prior art

- `photonic_holonet_body.tex` Theorem "Two realizations, one geometry" and §"The carrier"
  — own the past⊗future reading and the trace-Choi witness.
- Choi–Jamiołkowski — classical.

## Still open

- Whether the left–right sign reversal and the `σ_S` chirality reversal are the same map.
- Whether the outer involution of `W(E₆)` is literally the transpose.
- A correct two-shot readout computation.
- `CX_{p→f}`, the `μ₄/μ₆` re-homing, the transceiver, lines 1220–2400.
