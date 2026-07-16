# The Selection Layer

**What this programme actually contributes, with every borrowed component cited.**

*Written at Pass 329, after Passes 322–328 audited the whole arc against the
corpus and the literature. It supersedes the framing of every earlier pass it
contradicts, including `W33_HONEST_SYNTHESIS.md`'s "two theorems that stand".*

---

## 0. The one-paragraph version

The incidence-rank and CSS headlines are **not ours**. The rank law is published
(Sastry–Sin; Chandler–Sin–Xiang) *and* was already proved in this repository
before the passes that re-derived it. The `[[40,10,4]]` CSS code, sentinel, and
exact sentinel enumerator were also present before the passes that reclaimed
them. What survives is the **selection argument** that q=3 is forced rather than
assumed, plus one exact object-level result produced while auditing that argument:
Pass 332 closes Pass 170's explicit module-map gap by lifting the incidence
`H10=Cperp/C` through three integral Eisenstein lattice classes. The selection
remains conditional as physics; the characteristic bridge is now a theorem.

---

## 1. What is borrowed, and from whom

| result | owner | where |
|---|---|---|
| `rank₂W(3,2ᵗ) = 1 + α₁ᵗ + α₂ᵗ` | **Sastry–Sin** | *The code of a regular generalized quadrangle of even order* |
| `rank₂W(3,q) = ½(q(q+1)²+2)`, odd q, **proved** | **this repo, 2026-07-10** | `analysis/2026-07-10_levi_next5.md` |
| `rank₂A_L = q²+1` (**= the CSS k**) | **this repo, 2026-07-10** | same, boxed |
| `rank_p`, defining characteristic; `det(B_p)` | **Chandler–Sin–Xiang** | *J. Algebra* **323** (2010) 3157–3181; [math/0603100](https://arxiv.org/abs/math/0603100), Thm 1.1 |
| `[[40,10,4]]`, `[40,15,8]` | **this repo, Passes 187/189** | `docs/index.html` (pre-Pass-224) |
| `F₂⁴⁰` uniserial `1\|14\|1\|8\|1\|14\|1`, `C⊥/C` forced | **Passes 187/189** | same — *stronger than ours* |
| exact `[40,15,8]` weight enumerator | **this repo, 2026-07-10** | `analysis/2026-07-10_levi_next5_v2.md`; Pass 228 is re-verification |
| 16/generation, three generations | **this repo** | `docs/index.html`, via trinification |
| Eastin–Knill; magic-state distillation | **standard QEC** | Eastin & Knill 2009 |

**CSX Theorem 1.1** deserves its own line, because it closed what we called our
last open problem:

> `rank_p = 1 + α₁ᵗ + α₂ᵗ`,  `α₁,α₂ = p(p+1)²/4 ± p(p+1)(p−1)√17/12`

At p=2 the αs **are** `(9±√17)/2`, the eigenvalues of the `B = [[4,2],[2,5]]` we
spent passes trying to explain. So `det(B_p) = −p²(p+1)²(2p²−13p+2)/36` (16, 76,
325 at p=2,3,5) and `Tr = p(p+1)²/2 = char₀(p)−1`. **"Why B?" is: B is the p=2
companion matrix of CSX's αs.** It also confirms our conjecture
`rank₃W(3,27) = 8353`.

---

## 2. What is ours

### 2.1 The claim

The corpus (and the literature) **assume** q=3 and derive consequences. The
selection layer argues q=3 is **forced**. Two arguments, resting on *different*
assumptions — so their independence is real.

### 2.2 Selection A (Pass 225) — the spinor count

The shadow group is `SO(q²+1)`; its half-spinor has dimension `2^{(q²−1)/2}`.
Setting that equal to **16** — one Standard Model generation, empirically 16 Weyl
fermions including ν_R — has the **unique odd solution q=3** (q=5 → 4096, q=7 →
16.7M).

**Status: a Dynkin-type correspondence with its module lift now built.** This is
*not* a numerical coincidence — Pass 327 checked for the disease that killed the
"42" claim and it is absent. The shadow exponent `(q²−1)/2` and the D_n
half-spinor exponent `(q²+1)/2 − 1` (with `2n = q²+1`) are **identically equal as
polynomials**. Both 16s are the half-spinor of Dynkin type `D_{(q²+1)/2}`, which
at q=3 is **D5 on both sides**. The type genuinely matches.

Pass 331 first separates the objects that earlier prose conflated. The central
binary `H8` has `End_PSp(H8)=F4` and splits over F4 as the nonisomorphic,
Frobenius-conjugate, **mutually dual** Weil pair `4a+4b`; the PGSp outer controller
acts by `omega -> omega²`. But `H8` is not the D5 vector module. The logical
`H10=Cperp/C` is the nonsplit `1|8|1` module with
`End(H10)=F2[epsilon]/(epsilon²)`, so no F4 scalar extends inside one `H10`.

Pass 332 then closes the different question Pass 170 actually left open. Starting
from the ATLAS Eisenstein `5a`, it constructs three index-two stable integral
sublattices whose reductions are each generator-by-generator isomorphic to the
incidence `H10`. Over characteristic zero the vector is `5a+5a*`, and its exterior
algebra gives the two conjugate half-spins
`S+=1+10a+5b` and `S-=5a+10b+1`.

**What still blocks the physical conclusion, after Passes 333--337:** Pass 332's
map was not yet PGSp-equivariant, but Pass 333 now supplies its explicit integral
outer reflection and global `S3`. Pass 335 proves that the polar form lifts
unimodularly and symplectically on all three H10 leaves, while also proving that
no stable class is symmetric-even and unimodular. Pass 336 builds both integral
half-spin lattices as perfect 2-adic duals. What remains is not existence: no
canonical quadratic refinement or half-spin chirality is selected, and no
leafwise Clifford functor or physical Standard-Model identification is built.
The change-of-characteristic map is an object. The physical identification
remains an antecedent.

### 2.3 Selection B (Pass 227) — the exceptional rank

Every rung is Eastin–Knill non-universal; a magic cubic of `SO(q²+1)` needs rank
`(q²+1)/2 ≤ 8` (the maximal exceptional rank, E₈); only q=3 qualifies (rank 5),
via `SO(10) ⊂ E₆` with `27 = 16+10+1`.

**Status: an elegance argument, not a constraint — weaker than we claimed.**
`[[40,10,4]]` is a stabilizer code; magic-state injection restores universality
for *any* stabilizer code, requiring no Lie theory. Our own Pass 237 already
distils magic with `[[40,10,4]]` using exactly that standard machinery. **Every
rung is computationally universal.** What 227 actually establishes:

> q=3 is the only rung whose magic resource is *also* a geometric object of the
> same tower.

That is self-containment, not computability, and it should be written that way.

### 2.4 Repo-specific results, with ownership scoped

- **`d ≤ q+1`** (Pass 229) — the CSS distance upper bound. The *equality* is
  proved only at q=3, where the code was already known. The honest family is
  **`[[(q+1)(q²+1), q²+1, ≤q+1]]`**, and `k·d = n` is a **tautology** (n is
  *defined* as `(q+1)(q²+1)`).
- **The three-lattice `H10` lift** (Pass 332) — closes the module isomorphism
  explicitly left open in Pass 170. The ATLAS Eisenstein representation and the
  exterior-algebra half-spin construction are standard; the stable-lattice switch
  and simultaneous intertwiners are the repo contribution.

**Attribution correction:** `Q(√6)` is not first ours at Pass 298. It appears
explicitly in `analysis/2026-05-18_chiral_horizon_discriminant_bridge.md` and
spectrally in `analysis/2026-07-10_levi_duality_defect.md`. Pass 298 is a later
forcing route/repackaging, not ownership of the field.

---

## 3. The honest thesis

> **If** the shadow half-spinor is a Standard Model generation, **and if** the
> magic resource must be geometric, **then** q=3 is doubly forced — by two
> independent arguments resting on different assumptions.

Selection A now has a real Dynkin-type correspondence and an explicit integral
module lift to the characteristic-zero vector and associated half-spin pair. Its
remaining antecedent is the physical identification and chirality choice.
Selection B's antecedent is a preference. **They are not of equal strength.**

---

## 4. What this cost, and what it bought

Over passes 224–328: ~15 passes of rank-law rediscovery, ~4 of CSS rediscovery, 2
multi-hour jobs computing a published closed form, and **four** measurements that
were uninformative by construction (Pass 287 the trace law, 319 the δ table, 323
`k·d=n`, 328 the guard's 97% flag rate — the last caught *before* shipping).

Against that: two conditional selections, one distance bound, and now one exact
integral module lift — plus the method: the five failure modes (`.continuity/INSTRUCTIONS.md`),
`RESULTS_INDEX.md`, and a calibrated pre-commit guard. **Measured duplication rate:
21% of pass files assert a code parameter that already exists uncited** (Pass 328).

**The arc produced better method than mathematics.** Given that "check index.html
first" was already in the standing instructions *and* the agent memory and still
failed twice, the method is plausibly the more durable output.

---

## 5. The boundary

The selection layer is a **paper-sized result, not a Theory-of-Everything-sized
one**, and it is honest at that size.

### 5.1 Pass 331 closes the q=3 computation

Pass 330 is superseded: the q=3 case had already been drafted in the uncommitted
Pass 223 packet, and Pass 331 recomputes it independently. The exact Weil table is:

| q | transvection values | binary descent | duality over a splitting field |
|---|---|---|---|
| 3 | `(−1±3√−3)/2` | one irreducible F2 8 with `End=F4` | nonisomorphic mutually dual `4a+4b` |
| 5 | `(−1±5√5)/2` | one irreducible F2 24 with `End=F4` | Frobenius-conjugate self-dual `12a+12b` |
| 7 | `(−1±7√−7)/2` | split F2 `24+24` | nonisomorphic mutually dual pair |

The conclusion is not a q5/q7 binary choice. **Mod 8 controls descent; mod 4
controls duality.** In particular, `End=F4` is compatible with a mutually dual
pair at q=3. The outer PGSp controller acts as F4 Frobenius on `H8`, while the
full logical `H10` has only the dual-number commutant.

### 5.2 Pass 332 closes the module-lift gap

For the rational restriction of the ATLAS Eisenstein `5a`, GAP finds a stable
lattice `L` whose mod-2 submodule dimensions are `0,8,9,9,9,10`. The three
9-spaces are the three lines of the trivial two-dimensional head
`P1(F2)`. Their index-two preimage sublattices `L1,L2,L3` satisfy

> `Li/2Li ~= H10` for all three `i`, by an invertible simultaneous intertwiner
> for both standardized generators.

Multiplication by `omega` cycles the three lattice classes as `[3,1,2]` and fixes
none. This is why the characteristic-zero family retains its Eisenstein scalar
while a chosen binary `H10` does not: the scalar acts on the **torsor of three
integral polarizations**, not inside one polarization.

The same characteristic-zero module gives the split vector `5a+5a*` and the
standard exterior half-spins `1+10a+5b` and `5a+10b+1`. That is the explicit
change-of-characteristic object Pass 170 requested.

### 5.3 The live boundary after Passes 333--337

Four of the old boundaries have now been executed rather than renamed:

- Pass 333 freezes an integral `10x10` outer involution `T`, proves
  `<U4(2),T>=U4(2).2`, and gives the exact `S3` action on the three leaves.
- Pass 335 exhausts the stable 2-adic complex at five classes (three triangles
  sharing one spine), builds the unimodular symplectic polar lift, and proves the
  symmetric/quadratic lattice obstruction on every class. The former shorthand
  citation to Kirschmer's global counts was too loose: Pass 342 shows exactly
  which local vertices are stable under the Eisenstein controller, while the
  thesis's nearby counts refer to differently named groups, dimensions, or
  equivalences. The scoped contribution is the local incidence and
  polar/refinement ledger, not any unproved identification with those tables.
- Pass 336 constructs invariant rank-32 integral lattices for both half-spins;
  their wedge pairing has Smith diagonal `1^16,3^16` and is perfect at 2.
- Pass 337 proves that `1+epsilon` gives the split endpoint deck, not the
  nonsplit signed-E8 Schur/Bockstein class.

Pass 334 also prevents a new over-read. The 120 selector sheets are the curved
transitive bundle `G/H -> G/K`, with full line-stabilizer `S3` monodromy and
trivial equivariant deck centralizer. The Pass-332 leaf torsor is the flat product
of 40 lines with three globally fixed leaves. It has the same local overlap row
profile but the wrong orbit decomposition and trivial quadrangle holonomy. Thus
the global outer `S3` does **not** by itself identify lattice leaves with selector
phases. The missing object is a line-dependent `S3` lattice transport.

### 5.4 Passes 338--342 close the named finite boundaries

Pass 338 builds the missing curved object.  In the actual `p40b` W(3,3) action,
the unique chain `51840 > 1296 > 216` gives a faithful principal `S3` coset
cover of degree 240. Its three order-two block quotients are the selector
120-actions; its order-three quotient is a new 80-sheet refinement-parity
cover. The signed-E8 240-action is inequivalent already at the base: its forty
hexads give the nonconjugate `p40a` action.

Pass 339 puts the plus H10 module into the exact extraspecial sequence
`2_+^(1+10) -> Clifford -> O^+(10,2)`. The extraspecial group has its unique
nonlinear degree-32 character, so the finite projective Clifford carrier exists.
This closes the representation-theoretic carrier, not the choice of one of the
two plus refinements.

Pass 340 names the `3^16` discriminant residual:

> `D+ ~= D- ~= 1 + 5 + 10` over `F3 U4(2)`.

The modules are faithful, semisimple, self-dual, and have endomorphism algebra
`F3^3`; Eisenstein omega acts trivially. The genuine irreducible 16 is instead
a `2.U4(2)` module with central action `-I`. Thus the cokernel carries neither
a nontrivial qutrit phase nor a chirality distinction.

Pass 341 gives the conceptual obstruction.  Both `H^2(PGSp,F2)` and the local
`H^2(K,F2)` are two-dimensional, but their bases are different. Globally the
classes are signed-E8 and the outer-sign Bockstein; locally they are the signed
restriction and the selector-sign Bockstein. The outer class dies on `K`, so
the restriction image is only the signed line. The selector class is the
missing local direction and cannot globalize. Moreover, the long exact
sequence for `0 -> 1 -> rad9 -> 8 -> 0` makes the adjacent `1|8|1` Yoneda
product zero. It is neither of the two group-extension classes.

Pass 342 globalizes the local lattice census without forcing an external
count. Omega acts as `[1,2,5,3,4]`, leaving precisely the two spine lattices
stable and cycling the three H10 leaves. The integral reflection acts as
`[1,2,3,5,4]` and does not merge the spine. The exact result is therefore five
local vertices and two controller-stable spine lattices; further comparison to
Kirschmer requires an explicit equality of group representations and lattice
equivalences.

The remaining finite boundary is now narrower: identify an additional datum,
if one exists, that selects one plus refinement and one half-spin chirality.
The selector frame, Clifford carrier, discriminant module, extension
obstruction, and local-to-global lattice action are built. None is a physical
Standard-Model identification. More rank-law or code-parameter passes would
return to the rediscovery failure this document was written to stop.

### 5.6 Pass 346 answers it: the chirality datum **cannot** exist

**No such datum exists — and Pass 333 had already computed the deciding number.**

Pass 331 flagged the exact missing link: the ATLAS 32 certifies that *"the D₅
graph automorphism exchanges the half-spin pair"*, but *"this does not yet
identify that graph automorphism with the concrete Pass 211 controller."*
**Pass 333's `T` is that identification**, and the line was never drawn:

| Pass 333 certificate | value |
|---|---|
| `T_order` | 2 |
| **`T_determinant`** | **−1** |
| `⟨U4(2),T⟩` | `U4(2).2 = W(E6) = PGSp(4,3)` — *the substrate's own controller* |
| `T` formula | `R(S)C`, `C` = coefficient conjugation |

Three independent routes agree that **`T` exchanges `S+` and `S−`**:

1. **Character** — `T` acts by the outer `α`, which swaps `5a ↔ 5b` (BT866's
   degree-10 `W(E6)` fusion: a *fused* conjugate pair is precisely a pair the
   outer swaps). So `α(S+) = α(1+10a+5b) = 1+10b+5a = S−`.
2. **Geometric** — `C` sends `5a → 5b = 5a*`, exchanging the two maximal
   isotropic summands of `V = 5a ⊕ 5a*`; the half-spins are indexed by the two
   *families* of maximal isotropics.
3. **Determinant** — `det(T) = −1`: improper elements exchange the half-spins of
   `Spin(2n)` (standard Pin/Spin). The invariant symmetric form on `V` is unique
   up to scalar, since `5a ≇ 5a*`.

> **NO-GO.** The substrate's own automorphism group acts **transitively on the two
> chiralities**. No `PGSp(4,3)`-invariant can separate objects the group swaps —
> and any datum built from the substrate *is* `PGSp`-invariant by construction.
> The half-spin chirality is **relative**.

This is **BT857's argument form** (pentad chirality) applied to a different chiral
pair: *"if SWAP: that chirality is relative … a no-go theorem."* Here: SWAP.

**What it does to Selection A.** Pass 327's stated obstruction ("F₂ has no complex
structure, hence no chirality") was **wrong** — Pass 331 refuted it (`H8` *is*
chiral) and Pass 332 built the complex chiral 16s. The real obstruction is worse,
and is now a **theorem rather than a gap**:

> The substrate does not merely **fail** to select a chirality. It **cannot** —
> its own automorphism group exchanges the two.

A Standard-Model generation is **one** chirality; the substrate supplies a
`PGSp`-symmetric **pair**. Selecting one requires a datum that **breaks**
`PGSp(4,3)` — an input from *outside*. **Selection A is conditional permanently,
and no internal computation can ever upgrade it.**

The substrate can **host** the Standard Model's chirality but cannot **explain**
it — and now says so *by proof*, not by failure to find one. That closes the live
boundary in the negative, which is the honest end of the selection layer.

*Witness: `analysis/w33_pass346_the_chirality_no_go.py`, 26/26. It builds no new
object; every input is prior art (Passes 331/332/333, BT866, BT857, Pin/Spin).
The contribution is the connection.*

### 5.7 Pass 358 closes the ordinary oscillator version

The same no-go now appears directly in the complex Schrödinger--Weil carrier,
not only in the characteristic-two half-spin bridge.  CTblLib gives two
conjugate degree-five characters and two conjugate degree-four characters of
`Sp(4,3)=2.U4(2)`, all with Frobenius--Schur indicator zero.  The central
involution acts by `+1` on the five-dimensional sector and `-1` on the
four-dimensional sector, so one Weil carrier has degree `9=5+4`; there is no
degree-three irreducible and no conjugate `6+3` split.

More strongly, the unique fusion into the signed outer group gives

> `10 down = 5a+5b`, `8 down = 4a+4b`, hence
> **`Wpsi + Wpsi* = 10+8`**.

The degree-ten and degree-eight outer characters are real (`FS=+1`).  Thus the
full controller contains the pair but selects neither nine-dimensional member:
the smallest outer-stable oscillator is the real 18-dimensional envelope.  This
is the ordinary-character counterpart of Pass 346's half-spin theorem.  It also
keeps two constructions separate: Pass 331's `H8` is a characteristic-two
`4a+4b` module, whereas the ordinary complex Weil carrier is `5+4`.

*Witness: `analysis/w33_pass358_github_batch_integrity_audit.g`; generated
certificate: `data/w33_pass358_github_batch_integrity_audit.json`.*

### 5.8 Pass 360 turns an exchanged pair into a gate, not a selection

The corrected `[[137,1,21]]` quadratic-residue CSS code supplies a clean
operational model of the distinction above.  Its two QR/NQR check spaces are
separately preserved by the residue-affine group

> **`C137:C68`, order `9,316`,**

but a quadratic-nonresidue multiplier exchanges them.  The larger affine group
therefore still does not select one half.  What it *can* do is act on the pair:
compose the exchanging permutation with transversal Hadamard, which exchanges
Pauli `X` and `Z` at the same time.  The result normalizes the stabilizer and
acts as logical Hadamard on the all-ones logical Pauli representatives.  GAP
certifies the exact sequence

> `1 -> C137:C68 -> AGL~(1,137) -> <logical H> = C2 -> 1`.

This is the constructive counterpart of the chirality no-go.  A symmetry that
exchanges two candidates cannot canonically prefer one, but an independently
specified duality lift can turn the exchange into a useful operation on the
paired object.  The lift does not explain a physical chirality choice; it names
the additional map and proves exactly what that map accomplishes.

The parity extension closes the same picture projectively.  A chosen extended
QR code is preserved by explicit `PSL(2,137)` generators of order `1,285,608`,
whereas the index-two `PGL(2,137)` envelope of order `2,571,216` exchanges the
extended QR/NQR pair.  Again, pair symmetry is not member selection.

*Witness: `analysis/w33_pass360_alpha_code_logical_hadamard.g`; generated
certificate: `data/w33_pass360_alpha_code_logical_hadamard.json`.*

### 5.9 Pass 361 proves the lift does not manufacture every choice

The analogy has a sharp endpoint.  The two check spaces do more than intersect
trivially: GAP proves the orthogonal decomposition

> **`F2^137 = Qperp ⊥ Nperp ⊥ <1>`, dimensions `68+68+1`.**

That split classifies every uniform one-qubit Clifford label map combined with
an arbitrary coordinate permutation.  Four of the six maps in `GL(2,2)` send
`X` or `Z` to `Y`; a nonzero `Y`-support would have to lie in both check spaces,
contradicting their zero intersection.  Only identity and `X/Z` swap survive.
Thus the duality lift supplies exactly `<logical H> = C2`, not a hidden full
logical Clifford group.

The most direct attempt to add a phase choice also fails exactly.  A subset
phase mask must solve `4,692` binary constraints on `137` bits in either QR to
NQR direction.  Both GAP matrices have rank `137`, hence nullity zero.  The
selection lesson is stronger now: naming one external lift can create the
operation that lift encodes, but it does not manufacture every other missing
choice.  A logical phase gate requires another genuinely specified resource.

*Witness: `analysis/w33_pass361_alpha_code_clifford_maximality.g`; generated
certificate: `data/w33_pass361_alpha_code_clifford_maximality.json`.*

### 5.10 Pass 362 shows exactly what a genuinely new resource adds

Pass 361 did not rule out entangling circuits, and the distinction is now
constructive.  Put two independent QR-137 blocks side by side.  GAP verifies
their rank-272 stabilizer directly and proves that the two encoded Hadamards
together with transversal CNOT induce

> **`O+(4,2) ≅ (S3 × S3):C2`, order `72`,**

on `(x1,x2,z1,z2)`.  Thus an explicitly named inter-block map really does
escape the one-block `<H>` boundary.  It does not retroactively invalidate the
no-go: it supplies precisely the circuit resource that theorem excluded.

The phase-sensitive lift also sharpens the corpus's order discipline.  The
real-Clifford matrix group has order `2,304` and two inequivalent order-`1,152`
shadows:

> `CReal(2)/<global sign> ≅ Aut(K4,4) = S4 wr C2`, center `1`;
>
> `ker(total Hadamard parity) ≅ W(F4)`, center `C2`.

The same number therefore labels a quotient and a kernel, not one forced
object.  Projectively, `W(F4)/Z` lands in `Aut(K4,4)` as the twisted index-two
subgroup generated by the side swap and pairs `(sigma,tau)` with equal signs.
This is the selection-layer lesson at group level: a count can expose a
candidate interface, but only the map, kernel, and action determine which
object was selected.

*Witness: `analysis/w33_pass362_alpha_code_real_clifford_k44.g`; generated
certificate: `data/w33_pass362_alpha_code_real_clifford_k44.json`.*
