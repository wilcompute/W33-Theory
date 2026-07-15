# A reflection group cannot orient itself

### An obstruction to deriving fermion chirality from a Weyl-group substrate

*Standalone note. The argument below is elementary and general; it is stated here
because a specific programme spent a long time not noticing it applied. It is not
a theorem about W(3,3) — that is only where it was found.*

---

## The claim

> Let a physical structure be built from a finite reflection group `W`, and let a
> chirality (a handedness, an orientation, a choice of half-spin) be a datum that
> distinguishes two objects exchanged by some `w ∈ W` with `det(w) = −1`.
>
> **Then no `W`-invariant selects that chirality.** Any quantity built from the
> structure is `W`-invariant by construction, and an invariant cannot separate two
> objects the group exchanges. The chirality is *relative*, and selecting one
> requires a datum that breaks `W` — an input from outside the structure.

The content is entirely in noticing that reflection groups **contain their own
orientation reversals**. That is what "reflection group" means. A group that
contains a reflection cannot supply an orientation, for the same reason a coin
cannot call its own toss.

## Why it is not trivial

It looks trivial once stated, and it is — as an argument. It is not trivial as a
*habit*, for three reasons:

**1. The chirality can be genuinely present.** The obstruction is not that the
structure lacks chirality. In the case that prompted this note, the substrate has
chirality in abundance: an irreducible `F₂`-module `H₈` with `End = F₄` splitting
over `F₄` into a mutually dual, non-isomorphic pair `4a ⊕ 4b` with transvection
values `(−1 ± 3√−3)/2`; and, in characteristic zero, two 16-dimensional half-spin
representations `S± = Λ^{even/odd}(5a)` that are non-isomorphic complex conjugates
with an explicit invariant pairing. Both chiralities are *there*, fully realized.
The structure is not chirality-poor. It is chirality-**symmetric**, which is worse,
and looks like progress right up until you ask which one you have.

**2. The deciding fact is usually already computed.** In the motivating case, the
integral outer involution `T` had been constructed, and its certificate recorded
`det(T) = −1` and `⟨inner, T⟩ = W(E₆)` — the structure's own automorphism group.
Everything needed was on disk, in JSON, passing its tests. The number sat there
for fifteen passes while the chirality question was treated as open. **Nobody
multiplied `det = −1` by "improper elements exchange half-spins".**

**3. Failure to find a selector reads as "not yet".** This is the real cost. An
absent selector is indistinguishable, from the inside, from a selector you haven't
found — so the search continues, indefinitely, and every failure is read as
motivation rather than evidence. The obstruction converts an open-ended hunt into
a closed question with an answer. **A no-go is not a defeat; it is the thing that
stops you paying rent on a hunt.**

## The three routes (the motivating case)

Each is independent; they agree.

| route | argument |
|---|---|
| **Character** | The outer automorphism swaps the conjugate pair `5a ↔ 5b` (they fuse to a single irreducible degree-10 of `W(E₆)` — a *fused* pair is precisely a swapped pair). So `α(S⁺) = α(1+10a+5b) = 1+10b+5a = S⁻`. |
| **Geometric** | The outer contains coefficient conjugation, and `conj(5a) = 5a*`, so it exchanges the two maximal isotropic summands of `V = 5a ⊕ 5a*`. Half-spins are indexed by the two *families* of maximal isotropics. |
| **Determinant** | `det(T) = −1` is improper, and improper orthogonal elements exchange the half-spins of `Spin(2n)` (Pin/Spin). The invariant symmetric form is unique up to scalar since `5a ≇ 5a*`. |

## The generalization: every multiplicity is a torsor

The same argument does not stop at chirality. In the motivating case the integral
lifts form — in the source's own words — **"an Eisenstein C₃ torsor"**: three
lattice leaves, cyclically permuted, *stabilizing none*. A torsor is by definition
a set with no distinguished point.

So the structure offers two multiplicities and cannot break either:

- **2** half-spins, exchanged by `T` → torsor under `⟨T⟩`
- **3** lattice leaves, cycled by `ω` → `C₃` torsor

> **A substrate can present a multiplicity but cannot break one.
> Every multiplicity it offers is a torsor under its own symmetry.**

This kills a tempting move. Three leaves and three generations is a match, and a
matching count is not evidence — but the real objection is sharper than
coincidence: **a torsor has no hierarchy, and a mass spectrum is nothing but a
hierarchy.** A torsor is precisely the object that refuses to say which point you
are at; a generation hierarchy is precisely the datum that says which one you are.
The structures have opposite content. The count was never the problem.

## Scope — what this does not say

- It does **not** say the substrate is wrong, or that chirality is unexplainable.
  It says chirality is not derivable *from inside a reflection-group structure*,
  and must enter as symmetry-breaking input.
- It does **not** apply to structures whose symmetry group is orientation-preserving
  by construction (inside `ker(det)`). Those may well select — the question is
  whether there is any reason to prefer the index-2 subgroup, and that is a physics
  question, not a group-theory one.
- It is **not** novel mathematics. Every ingredient is standard: `det`, Pin/Spin,
  torsors. It is a piece of bookkeeping that happens to close a question.

## The transferable part

This obstruction should apply to any programme deriving fermion handedness from a
Weyl or reflection group — which is a large family. The check is cheap:

> **Find the element of your symmetry group that exchanges the two chiralities.
> If it exists, stop looking for a selector. Compute `det`.**

If it exists, no internal datum will ever select, and the search that feels like
it is converging is not. The cost of not asking, measured once: roughly fifteen
passes.

---

*Machine-verified witnesses: `analysis/w33_pass346_the_chirality_no_go.py` (26/26),
`analysis/w33_pass348_every_multiplicity_is_a_torsor.py` (41/41). Every input is
prior art — the constructions are due to the GAP track (Passes 331–333) and the
argument form to an earlier pentad-chirality no-go (BT857); the contribution here
is the connection.*
