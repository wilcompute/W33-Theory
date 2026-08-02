# Passes 2106–2110 — the golden ratio **is** in the substrate: `R₄²U₆` has spectral radius `φ`

The user has insisted for many batches that `φ` is here somewhere. It is. It was
found by independently verifying the parallel track's own generators — their
Pass 2051/1942 matrices — rather than by searching the geometry.

---

## Pass 2106 — `R₄²U₆` has characteristic polynomial `(t+1)(t² − t − 1)`

Their phase-controller generators are

```text
R4 = [[0,-1,0],[1,0,0],[0,0,1]]     order 4, det 1
U6 = [[1,0,0],[0,0,1],[0,-1,1]]     order 6, det 1
```

Verifying their claim first: `R₄U₆` has characteristic polynomial `t³ − t² − 1`,
spectral radius `1.4655712` — the supergolden `ψ`. **Confirmed exactly.**

But checking neighbouring words:

```text
R4^2 U6 = [[-1,0,0],[0,0,-1],[0,-1,1]]     det 1
char poly : t^3 - 2t - 1  =  (t+1)(t^2 - t - 1)
roots     : -1 ,  (1-√5)/2 ,  (1+√5)/2
spectral radius = 1.6180339887  =  phi   (EQUAL, exactly)
```

> **`t³ − 2t − 1` factors as `(t+1)(t² − t − 1)`. The golden quadratic comes out
> whole, and the spectral radius of `R₄²U₆` is exactly `φ`.**
>
> Its eigenvalues are `−1, φ, −1/φ`, so its **eigenvalue field is `ℚ(√5)`.**

---

## Pass 2107 — the three shortest words give the three smallest metallic constants

```text
R4 U6^2   t^3 - t - 1        rho = 1.3247179572   plastic number (smallest Pisot)
R4 U6     t^3 - t^2 - 1      rho = 1.4655712319   supergolden psi
R4^2 U6   t^3 - 2t - 1       rho = 1.6180339887   GOLDEN phi
```

All three lie in `⟨R₄, U₆⟩ = SL₃(ℤ)` at **word length ≤ 3**, from the same two
generators, on the same phase carrier.

This also settles Pass 2100's question: `ψ` is **not** distinguished. It is the
growth rate of one particular word. The group contains `φ` and the plastic number
just as readily, at comparable length.

---

## Pass 2108 — where `φ` is, precisely

The apparent contradiction with Passes 2082–2087 resolves cleanly, because those
passes were about **different objects**:

| statement | verdict |
|---|---|
| `φ` in the character fields of `PGSp(4,3)` | **no** — they are `ℚ` and `ℚ(ζ₃)` |
| `φ` as a root of a rank-4 Gaussian binomial | **no** — those factor into cyclotomics |
| `φ` in the finite substrate's spectra or counts | **no** — measured, Passes 2068/2099 |
| `φ` in the **infinite arithmetic group** on the phase carrier | **YES** — `R₄²U₆` |

> **`φ` is absent from the finite geometry and present in the infinite
> arithmetic.** Both halves are true, and neither contradicts the other.

The rank argument survives intact and is sharpened: `Φ₅` cannot divide a rank-4
Gaussian binomial, so `ℚ(ζ₅)` never appears in the finite structure. But
`ℚ(√5) ⊂ ℚ(ζ₅)` appears in the *eigenvalue field* of an `SL₃(ℤ)` element — and an
infinite group's spectrum is not constrained by the finite group's character
field. **A degree-3 matrix reaches `φ` through a reducible characteristic
polynomial**, `(t+1)(t²−t−1)`, which is exactly how a cubic object touches a
quadratic irrationality.

That is why the search kept failing: I was looking in the finite geometry, where
Pass 2083's cyclotomy argument is a genuine obstruction, and `φ` lives one level
out — in the arithmetic group the parallel track constructed.

---

## Pass 2109 — what this does and does not claim

**Claimed.** `⟨R₄,U₆⟩` contains elements whose spectral radii are the plastic
number, `ψ` and `φ`, at word length ≤ 3; the golden one has eigenvalue field
`ℚ(√5)`; and the parallel track's `ψ` claim is confirmed exactly.

**Not claimed.** That `φ` is *selected* or distinguished. `SL₃(ℤ)` is the full
modular group of rank 3 and contains elements of unboundedly many growth rates —
their Pass 1953 proved `⟨R₄,U₆⟩ = SL₃(ℤ)` outright. So "`φ` is in the substrate"
means "`φ` is a spectral radius of a short word in the phase controller", not
"the substrate produces `φ` as an invariant".

The honest form: **the phase controller's arithmetic is rich enough to contain
`φ`; the substrate's finite geometry is not.** Whether the specific word `R₄²U₆`
has operational meaning — as their `μ₄`/`μ₆` clock combination does — is open,
and is the question worth asking next.

---

## Pass 2110 — the other items

- **`χ(H) = 9` from their 12 schedule orbits** — not attempted; their Pass 2050
  data is the input and their step 1 is the right plan.
- **The degree-6 reflection carrier** — not found; Pass 2101 established only
  that it is not in the signed edge module.
- **The `D₄` relation at `q = 7, 11`** — not computed. Their Pass 2088–2089 now
  proves the geometric side for all odd `q` (`J² = μI`, `σ = [J]`, orbit size
  `q²(q²−1)/2`), so only the representation-theoretic half remains, and their
  step 3 proposes exactly this.
- **The final ledger audit** — not done.

---

## Prior art

- Passes 1942/1953, 2051 (parallel track) — **own** `R₄`, `U₆`, the
  `⟨R₄,U₆⟩ = SL₃(ℤ)` identification and the `t³−t²−1` witness. This pass verifies
  that witness and finds `φ` in a neighbouring word.
- Passes 2082–2087 — the cyclotomy and rank arguments, which stand and are
  sharpened rather than overturned.
- The insistence that `φ` must be present is the user's, and it was correct.

## Still open

- Whether `R₄²U₆` means anything operationally.
- `χ(H) = 9`.
