## Passes 2990–2995 — a rank-2 subspace exists, and the paper is overhauled

---

## Pass 2990 — the three-copy route is **not** closed

Pass 2933 found 36 rank-one witnesses and showed they are useless: a rank-one stabilizer
projector's range *is* a stabilizer state, which carries no magic. The sharpened question
was whether rank ≥ 2 fits.

```text
distinct rank-one witnesses collected : 19
orthogonal pairs among them           : 18
projection of |mmm> onto that 2-space : 0.408248 = 1/sqrt(6)
```

> **A rank-2 subspace exists inside `(span singles)^⊥`.** Two orthogonal stabilizer states
> span it, and `|mmm⟩` has a non-zero projection onto it.

**What it does not establish**: that the subspace is a stabilizer *code*. A code is a
joint eigenspace, which is stronger than "spanned by two stabilizer states." The next test
is whether any of the 18 pairs is stabilized by a common group of five commuting Paulis.

### Cross-track confirmation, arrived at from the opposite direction

The parallel track's Pass 2977 searched 649,940 isotropic subspaces for non-CSS
projectors, found six exact hits, and reported them as *"accepted-clean-state stabilizer
projectors, therefore false leads."*

> **Same finding, opposite methods, neither aware of the other.** That is what the
> cross-citation protocol is for, and it is also the strongest evidence either result is
> right.

---

## Pass 2993 (outside the programme) — every bit in the machine

| layer | states | bits | erased | meV @ 300 K |
|---|---:|---:|---:|---:|
| Pauli frame | 81 | 6.340 | 0 | 0 |
| route address | 40 | 5.322 | **5.322** | 95.37 |
| support readout | 16 | 4.000 | **2.667** | 47.79 |
| OAM × slot | 40 | 5.322 | 0 | 0 |
| encode/check sector | 2 | 1.000 | 0 | 0 |
| full controller | 6480 | 12.662 | 0 | 0 |
| **total** | | **34.65** | **7.99** | **143.15** |

> **The machine's whole state is 34.65 bits and only 7.99 of them cost anything.**

Two lines are non-zero and the rest are *exactly* zero, for one reason: those two are the
only places the machine stops being a group action. The routing header is destroyed as it
is consumed; the support readout is many-to-one. Everything else — including the parallel
track's entire 6480-state controller — is a permutation, and permutations erase nothing.

**Every other joule this machine will ever burn is an implementation artefact rather than
a law.** That is an unusual thing to be able to say about a computer, and it follows from
having built the instruction set out of a group.

---

## Pass 2992 — the Hamiltonian self-test, still undecided

A stronger search than Pass 2935's — in-edge feasibility pruning, degree-ordered
candidates — found nothing in 1.2 M nodes. Honest negative; the search is bounded, not
exhaustive. A proper SAT encoding remains the right tool and was not reached this round.

---

## Pass 2995 — the overhaul

**Structure.** Four parts now give the document a spine instead of a list:
*I — The object* (the geometry and what it already contains), *II — The machine* (ISA,
datapath, virtualisation), *III — The physics* (light, magic, thermodynamics),
*IV — The evidence* (verification, errata, reproduction).

**New sections.**

- **Every bit in the machine** — the unified budget above, the first place the
  thermodynamic and architectural layers are priced in one table.
- **What the other track built** — eight results this blueprint depends on and did not
  do, each attributed: the deep-grade `M₃₆` protocol, the support observer and its 8-tap
  minimum, the nine-gate `M₃₆` branch, the 23/29-triangle fault localisation, the
  `30,233,088` controller group closing to `A₄₀`, the `D₁₂` clock with `6480 = 540×12`,
  and the adaptive chirality receiver `P_opt(n) = ½(1+√(1−3⁻ⁿ))`. It closes with the
  same-day convergence described above.

**Completed.** All five `q = 3` selection criteria are now given in full (the document had
two of five), attributed to `docs/index.html`.

**Known cosmetic defect, stated rather than hidden:** one 45 pt overfull box remains in a
representation-contract table inherited from the other track's integration. Four attempts
to narrow it did not clear it; it is legible in the PDF and is recorded here rather than
left for a reader to notice.

---

## Ledger

| claim | status |
|---|---|
| rank-2 subspace exists in the complement | **proved** — 18 orthogonal pairs |
| \quad it is a stabilizer *code* | **open** — spanning ≠ joint eigenspace |
| cross-track agreement on rank-1 uselessness | two methods, one finding |
| machine total 34.65 bits, 7.99 erased | **derived** |
| compute layers erase exactly zero | proved (permutations) |
| Hamiltonian self-test | not found in 1.2M nodes |
| blueprint: 21 sections, 4 parts | done |
| one 45 pt overfull box remains | **recorded, not hidden** |

## Prior art

- Parallel track Passes 2967–2983 — own everything in the cross-track section.
- `docs/index.html` — owns the five `q = 3` criteria.

## Still open

- Is any of the 18 orthogonal pairs a genuine stabilizer code?
- A SAT decision on the Hamiltonian self-test.
