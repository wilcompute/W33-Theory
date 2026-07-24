# Pass 810 — Corrected synthesis of the deformation / flat-block / Burnside arc

> **Purpose.** `PASS_682_ARXIV_SYNTHESIS_PASSES_641_677.md` states two results
> (its Theorems B and C) that do not hold as written. This note gives the honest
> status of every claim in the arc so the preprint can be corrected before
> submission. It is written across the track boundary: the flat-block passes are
> the Python track's, the W(3,3)-lattice passes (682/722/803) are the K-track's,
> and both are cited by certificate.

---

## 1. The two corrections

### 1a. The flat-block eigenlattice gluing (corrects Pass 676, and PASS_682 §5, Theorem B)

**Claimed:** the flat block's two eigenlattices glue over `Z[ζ_q]` to
`(Z/2q)^{q-1} ⊕ (Z/q)^{(q²-1)/2-(q-1)}`, with `q`-primary rank `(q²-1)/2` equal
to the antipodal-pair count — the "deformation–Burnside bridge."

**Correct (Pass 808, certified `data/w33_pass808_flatblock_gluing_correction.json`):**
the saturated eigenlattices `L_{q-1}=ker(F-(q-1)I)` and `L_{-(q+1)}=ker(F+(q+1)I)`
glue as

```
Z^n / (L_{q-1} ⊕ L_{-(q+1)})  =  im((F+(q+1)I) mod 2q)  ≅  (Z/2)^{(q-1)²/2}
```

— **pure 2-torsion, no q-torsion at all**: `(Z/2)²`, `(Z/2)⁸`, `(Z/2)¹⁸` at
`q=3,5,7`. Verified three independent ways (spectral projector + Smith, the
two-branch theorem, brute-force subgroup enumeration).

**Why Pass 676 was wrong:** it glued the eigenlattice *images*
`im(F+(q+1)I), im(F-(q-1)I)` — which are *unsaturated* finite-index sublattices —
instead of the saturated eigenlattices, and used a faulty hand-rolled Smith
routine (it returned `[6,6,3,3]` where even the image object's true Smith form is
`[3,3,6,6,6,6]`).

**Consequence:** there is **no deformation–Burnside bridge**. The gluing rank
`(q-1)²/2` never equals the antipodal-pair count `(q²-1)/2` — `2≠4`, `8≠12`,
`18≠24`. The rank coincidence Pass 676 reported was the Smith bug.

### 1b. The tower claim (corrects PASS_682 Theorem C / "Pass 679")

**Claimed:** the flat-block eigenlattice over `Z[ζ_{q^n}]` has `q`-primary rank
`(q^{2n}-1)/2` for all `n`, "proved in Pass 679."

**Status (Pass 807, certified `data/w33_pass807_...json`):**

- Passes 678 and 679 have **no witness code and no data certificate** in the
  repository. The claim exists only as prose.
- The counting identity — `#{antipodal pairs in (Z/q^n)²} = (q^{2n}-1)/2` — is
  **true for all n** (elementary; it is the Burnside base of Pass 661).
- The **deformation side does not realize it for n>1**: the modulus-`q^n` flat
  block fails `F²+2F-(q²-1)I=0` in *every* entry at `(3,2)` (81/81) and `(5,2)`
  (625/625), and at `q=9` has neither `q-1=8` nor `-(q+1)=-10` as an eigenvalue.
  There is no two-branch eigenlattice gluing at `n>1`.

**Consequence:** "Theorem C" is a counting identity mis-stated as a deformation
theorem. And after §1a, even at `n=1` the flat-block gluing is `(Z/2)^{(q-1)²/2}`,
not `(q²-1)/2` — so the bridge fails at every `n`.

---

## 2. What is solid (keep)

| Result | Statement | Certificate |
|---|---|---|
| Burnside formula (Pass 661) | `|Fix_all(g)|=(pⁿ)^{c⁺(g)}` over every odd `Z/pⁿ`; reproduces 7, 2 034 735, both exact `Z/9` integers; new `Z/25, Z/27` | `w33_pass661_...json` |
| Abstract order & Ext (Pass 662/663) | `S=F+q+1` sends `F²+2F-(q²-1)=0` to `S²-2qS=0`; abstract order `O_q=Z_p[S]/(S(S-2q))` has Ext quiver `(0, Z/p^{v_p(2q)}, Z/p^{v_p(2q)}, 0)`; at `q=2` this is the S8 commutant with `Ext=Z/4` | `w33_pass662_...`, `w33_pass663_...` |
| Two-branch gluing theorem (Pass 806) | For integral `S(S-cI)=0` in block form `[[cI,Y],[0,0]]`, gluing `= ⊕_i Z/(c/gcd(d_i,c))`, `d_i=Smith(Y)`; verified 240 random blocks 3 ways; reproduces the K-track's `(Z/4)⁶⁶` from `c=4, Smith(Y)=(1⁶⁶,12)` | `w33_pass806_...json` |
| Corrected flat-block gluing (Pass 808) | `(Z/2)^{(q-1)²/2}`, pure 2-torsion | `w33_pass808_...json` |
| k-branch generalization (Pass 809) | `Z^n/⊕L_i = Z^n/∩_i ker(N_i mod D_i)`; multi-conductor for `k≥3` | `w33_pass809_...json` |
| Ring-tower field-specificity (Pass 807) | flat block fails its quadratic for `n>1`; the bridge is field-only | `w33_pass807_...json` |

**The K-track's W(3,3)-lattice realizations are independent and stand:** the
signed-turn operator `K` with spectrum `-6⁸¹, 2¹²⁰, 4²⁴, 10¹⁵` (Pass 682); the
cycle lattice `S=(K+6I)/2`, `S(S-4)=0`, gluing `(Z/4)⁶⁶` (Pass 722); the cut
lattice `S=K-4I`, `S(S-6)=0`, gluing `(Z/2)⁵⊕(Z/6)¹⁰` (Pass 803). These are
computed directly on canonical lattices; only Pass 682's *imported* value for the
"real cyclotomic two-branch substrate" (it quoted Pass 676's `(Z/6)²+(Z/3)²`)
should be updated to `(Z/2)²`.

The theorem that ties all three lattices together is Pass 806: one gap-`c` order
supports gluings as different as `(Z/2)²` (flat block), `(Z/4)⁶⁶` (cycle) and
`(Z/2)⁵⊕(Z/6)¹⁰` (cut), determined entirely by the Smith type of the off-diagonal
block `Y`. The conductor `c` is intrinsic to the order; the gluing type is a
property of the realization.

---

## 3. Suggested preprint edits

1. **Delete Theorem B** (the `(q²-1)/2` gluing rank) and replace with the
   Pass 806 theorem plus the Pass 808 flat-block value `(Z/2)^{(q-1)²/2}`.
2. **Restrict Theorem C** to the counting statement (Burnside pair count
   `(q^{2n}-1)/2`, all `n`) and drop the deformation identification; remove the
   citations to the certificate-less Passes 678/679.
3. **Update §5**'s imported flat-block gluing from `(Z/6)²+(Z/3)²` to `(Z/2)²`.
4. Keep §§2–4 (Burnside, 2-adic tower, Bridge Theorem for the *abstract order*)
   and the K-track lattice realizations unchanged — they are certified.

Net effect: the paper loses a bridge that was an artifact and gains a clean,
correct organizing theorem (Pass 806) with three certified realizations.
