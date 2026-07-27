# Passes 1109–1110 — the 135 as cosets of Q₈, and why the Steinberg dies in every quotient

Two results that close the last two open ends of the 1079–1108 arc, plus the
resolution of an open question BT790 posed and never settled.

---

## Pass 1109 — the C₃ of Pass 1097 is SL(2,3)/Q₈

Pass 1107 found that the 135 maximal partial spreads of W(3,3) are a **published**
family: dual to the maximal partial ovoids of size q²−1 of Q(4,q), described in the
literature as *sharply transitive subsets of SL(2,q)*. That description is now
tested against this repository's own structure, and it lands exactly.

**Computed.** A sharply transitive subset of SL(2,3) has size q²−1 = 8 and acts
sharply transitively on the 8 nonzero vectors of 𝔽₃²; equivalently, for any two
distinct members s,t the ratio s⁻¹t fixes no nonzero vector. Exhaustive
enumeration over |SL(2,3)| = 24:

```text
sharply transitive subsets of size 8 in SL(2,3) : 3
of which are subgroups                          : 1   (element orders 1,2,4×6 → Q₈)
the 3 subsets ARE the 3 left cosets of Q₈       : true
SL(2,3)/Q₈                                      : C₃
```

So there are exactly **three**, they are the cosets of the quaternion group, and the
quotient permuting them is **C₃**.

**The match.** Pass 1097 found, independently and from the geometry alone, that each
polar pair carries exactly three 4-blocks and that the polar-pair stabiliser acts on
that triple through **C₃, not S₃** — a canonical orientation with no explanation
attached at the time. Pass 1100 then found 135 maximal partial spreads. These are
the same 3:

```text
135  =  45 polar pairs  ×  3 cosets of Q₈ in SL(2,3)
```

and the unexplained C₃ orientation on each triple is SL(2,3)/Q₈. The geometric
side and the published group-theoretic side agree, and the agreement is what
identifies the C₃ rather than merely naming it.

---

## Pass 1110 — the Steinberg multiplicity is a cycle rank

Pass 1101 measured that both degree-81 constituents sit in the 540-frame module and
in **none** of the three block quotients, and Pass 1108 verified that the 81 is the
Steinberg module of Sp(4,3). Neither said *why* the quotients kill it. They do,
and the reason is topological.

For a rank-2 group of Lie type the Tits building Δ is one-dimensional — here the
point–line incidence graph of W(3,3) — and the Steinberg module is its top reduced
homology, St ≅ H̃₁(Δ). That is directly visible:

```text
Δ :  V = 40 points + 40 lines = 80,   E = 160 incidences
b₁(Δ) = E − V + 1 = 160 − 80 + 1 = 81 = dim St     ✓
```

Over ℚ, invariants commute with taking the quotient graph, so
**dim(St^H) = b₁(Δ/H)**. Computing both sides independently:

| H | \|H\| | Δ/H: V, E, comps | b₁(Δ/H) | Steinberg multiplicity |
|---|---|---|---|---|
| frame stabiliser (C₂ × S₄) | 48 | 9, 10, 1 | **2** | **2** |
| 4-block stabiliser | 192 | 6, 5, 1 | **0** | **0** |
| 12-block stabiliser | 576 | 4, 3, 1 | **0** | **0** |
| 15-block stabiliser | 720 | 3, 2, 1 | **0** | **0** |

The multiplicities are computed from the character table as fixed-point counts, the
cycle ranks from the quotient graphs; they agree in all four rows.

**So the answer is: every block stabiliser has a TREE quotient.** A tree has no
cycles, hence no H̃₁, hence no Steinberg. The frame stabiliser's quotient is the
only one with independent cycles, and it has exactly two.

*(The multiplicity 2 here is for the inner group PSp(4,3), which has a single
degree-81 irreducible. Pass 1101 reported 1 + 1 for the outer group U4(2):2, whose
two 81s each restrict to it — Pass 1092's restriction data. The two are consistent;
the inner count is the one that matches b₁.)*

---

## BT790's open question, resolved

BT790 asks whether W(3,3) contains **7 mutually skew totally isotropic lines**
(for a Császár torus embedding), expects the maximum to be 4 or 5, sets out two
outcomes, and says "the verifier will decide."

It is decided, and neither expectation was right: **the maximum is 10.** W(3,3) has
36 spreads, each of 10 pairwise disjoint totally isotropic lines covering all 40
points, so seven mutually skew lines exist in abundance — any 7 of a spread's 10.
**Outcome A holds.**

BT790 now carries that resolution, with one caveat recorded there: Outcome A was
stated conditionally on the maximum being *exactly* 7, so any downstream claim that
needs seven rather than *at least* seven still has to be re-derived.

---

## Pass 1111 — two ownership corrections and one open question closed

The guard's new noun-number tokens (Pass 1107) fired again while this file was
being written, and both hits were real.

**`polar-pair@4` → BT810.** BT810 already owns the 45 polar pairs outright, and
states them *more completely* than Pass 1097 did: the polarity is fixed-point-free
on the 90 hyperbolic lines, giving 45 pairs, with

```text
Stab{L, L^perp} = (SL(2,3) x SL(2,3)) : C2,   order 1152, index 45
```

and the mechanism — the pair splits 𝔽₃⁴ into two orthogonal symplectic planes,
each carrying Sp(2,3) = SL(2,3) = 2T, swapped by the polarity. It also places the
45 in the Schläfli dictionary as the tritangent planes.

So **Pass 1097's contribution is narrower than its headline claimed**: the polar
pairs are BT810's; what 1097 adds is the equivariant bijection from the 12-block
system to them. Pass 1097 has been amended. This also means Pass 1109's SL(2,3)
is not a new appearance — BT810 already has SL(2,3) sitting at each polar pair.
What 1109 adds is that the *three cosets of Q₈* index the three 4-blocks and that
SL(2,3)/Q₈ is the C₃.

**BT773 owns the 540 and its order-48 stabiliser**, under a third name again:
"there are 540 cubes in W(3,3), one per 3A₁ involution", with 51840 = 540 × 2 × 48.
Pass 1079 has been amended to cite it. The same 540 has now appeared as outer
involutions (Pass 1067), cubes (BT773), skew pairs (BT810) and frames (Pass 1079) —
four names for one object, which is precisely the condition that makes this corpus
rediscover itself.

**And BT810's open question is closed.** It asks: "is the order-48 chart group 2O
or O_h as an abstract group (both order 48 — settle by element orders)?" Settled
exactly as proposed:

```text
element orders in the stabiliser : [1:1, 2:19, 3:8, 4:12, 6:8]   → 19 involutions
2O (binary octahedral) has exactly ONE involution (its centre)
IsomorphismGroups(H, C2 x S4)        -> succeeds
IsomorphismGroups(H, SmallGroup(48,28) = 2O) -> fail
```

**H = C₂ × S₄ = O_h**, the full octahedral group. A consequence worth flagging in
BT810's own terms: its "platonic ladder" should not be read as uniformly binary —
2T and 2I are double covers, O_h is not.

## Scope

Pass 1109 is an exhaustive enumeration in a group of order 24 plus a comparison
against two earlier certificates; it identifies the C₃ and claims nothing about
q ≠ 3. Pass 1110 computes two quantities that are theoretically equal and checks
they agree — it explains the pattern, it does not prove the general theorem, and
the equality dim(St^H) = b₁(Δ/H) is standard building theory, cited not claimed.

## Prior art

- `analysis/w33_pass1097_name_the_frame_quotients.g` — the 45 as polar pairs, and the unexplained C₃.
- `analysis/w33_pass1100_name_the_135.g` — the 135 maximal partial spreads.
- `analysis/w33_pass1107_partial_spread_census.md` — the literature identification.
- `analysis/w33_pass1101_eightyone_location.g` — the multiplicities.
- `analysis/w33_pass1108_steinberg_identification.g` — the Steinberg verification.
- `data/w33_pass1092_u42dot2_character_identification.json` (parallel track) — the restriction data.
- `analysis/BT790_csaszar_embedding.md` — the question resolved above.
