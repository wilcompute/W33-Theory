# Pass 4566 — the gap Pass 78 named, and the theorem this corpus is missing

A prior-art sweep on non-abelian edge weights and on scaling laws for signed spectra
returned three results. Two say the new work is new. The third is more useful: it says a
standard theorem that frames a result I already published here is **absent from the corpus
entirely**.

## 1. Pass 78 named this gap, and Pass 4565 is the first step into it

`w33_pass78_equivariant_closure.py:109`:

> *"It is not yet the full edge-zeta Artin factorization across all 34 irreducibles."*

That is precisely the non-abelian generalisation. The chain now reads:

| pass | structure group | object |
|---|---|---|
| 4409 | Z₂ and U(1) | signings, gradient descent on ρ |
| 4436 | Z₂ | Artin–Ihara L-function of the **1-dimensional sign character** |
| **4565** | **Z₂, Z₃, U(1), SU(2)** | **matrix edge weights; ρ measured per group** |
| *outstanding* | all 34 irreducibles | **the full edge-zeta Artin factorization** |

Pass 4436 factored the zeta of a double cover as `ζ_X · L(u, χ)` for a **one-dimensional**
χ. The general statement factors the zeta of a `G`-cover as a product over **all** irreps,
each `L(u, ρ)` appearing with multiplicity `dim ρ`. Pass 4565 put `SU(2)` matrices on edges
and measured spectra, which is the analytic half; the factorization is the arithmetic half,
and Pass 78 flagged it as undone before this arc began.

**Neither pass cites the other.** 4436 and 4565 are mine; 78 is not. That is the
cross-boundary citation `CLAUDE.md` asks for, recorded here.

## 2. Friedman's theorem is absent, and Pass 4438 needs it

Zero hits anywhere in the corpus for **Friedman's theorem** — that a random `d`-regular
graph satisfies `λ₂ ≤ 2√(d−1) + ε` with high probability. Alon–Boppana *is* present, but
only ever as a fixed threshold constant for `W(3,3)`, never as an asymptotic statement about
a family.

That absence matters, because **Pass 4438's headline is a finite-`n` shadow of Friedman**:

> 87% of random ±1 signings of W(3,3) are already Ramanujan.

I reported that as a deflation of my own search arc — correctly — but framed it as a fact
about this graph. It is not. It is what Friedman's theorem predicts you should see: the
signed adjacency matrix of a random signing behaves like a random regular graph, whose
spectral edge concentrates at `2√(d−1)`. The 87% is the probability of landing under the
threshold at `n = 40`, and Pass 4565 then showed the same quantity rising to 99.6% as the
structure group grows and the fluctuation shrinks.

So the correct frame is: **Alon–Boppana sets the floor, Friedman says random gets you
essentially to it, and the Ramanujan fraction is a finite-size fluctuation question.** None
of that was stated in 4438, and the deflation is sharper with it than without.

## 3. What is genuinely new

| direction | verdict |
|---|---|
| non-abelian / matrix edge weights | **new** — the corpus is strictly rank-1; only U(1) exists (Pass 4409) |
| scaling law for signed spectra | **new** — no `n`-dependence studied anywhere; every signing pass is single-graph at `n` = 40, 80, 160 |
| Alon–Boppana as a threshold | already present in 7 files |
| Friedman's theorem | **absent** |

The reserved-but-unexecuted pass `data/w33_pass_namespace_registry_v2.d/2974-2983.json`
proposed *"construct a genuinely nonabelian D4 multi-edge route syndrome"* and was never
run — a third independent place the corpus reached for this and stopped.

## Evidence boundary

This file records a literature/corpus relationship and derives nothing. The claim that Pass
4438's 87% "is" Friedman's theorem is an interpretive framing, not a proof: Friedman is
asymptotic in `n` and 4438 is one graph at `n = 40`, so the connection is a prediction about
what the `n`-dependence should look like, and the scaling measurement that would confirm or
break it is not in this file.
