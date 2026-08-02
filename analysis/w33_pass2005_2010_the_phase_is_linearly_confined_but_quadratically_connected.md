# Passes 2005–2010 — the phase is linearly confined but **quadratically connected**

Six items. The first is the outside-the-box one and it materially changes what
"confined" means. Two of my five planned items were not done and are marked so.

---

## Pass 2005 (physics/CE) — confinement is a **first-order** statement only

Pass 1963 established `Hom_PSp(90, X) = 0` for `X ∈ {15, 24, 30, 81}` and I
called the phase "dynamically isolated". The parallel track's Pass 1975 was
careful to say linear confinement "is not an absolute law of nature". Testing the
second-order channels:

```text
Sym^2(90)   dim 4095 : contains 15 x3,  24 x1,  30 x3,  81 x5
Lambda^2(90) dim 4005 : contains 15 x0,  24 x4,  30 x2,  81 x7
90 (x) 81   dim 7290 : contains 15 x2,  24 x3,  30 x5,  81 x11
```

> **The phase is linearly confined and quadratically connected.** No equivariant
> *linear* map exports it, but `Sym²(90)` contains **all four** rational blocks —
> including the physical 81 with multiplicity 5.

And a selection rule falls out of the asymmetry:

> **`Λ²(90)` contains no 15 at all**, while `Sym²(90)` contains it three times.
> The antisymmetric channel cannot reach the gauge `15`; the symmetric one can.

That is exactly the shape of a **hidden sector** in field theory: a symmetry that
cannot mix at first order but communicates through higher-dimension operators.
Stated as structure, not as a physical identification — the withdrawn readings
(charge, flux, colour, generation, neutrino) stay withdrawn.

**The engineering statement, which is sharper.** A linear buffer cannot read this
phase — `Hom = 0` says so. A **mixer** can: `Sym²` is the quadratic channel, and
it reaches every sector. So in the three-plane controller architecture the
parallel track proposed, the bridge out of the six-phase domain is necessarily a
nonlinear element, and `Λ²` versus `Sym²` tells you *which* nonlinearity reaches
which plane. That is a design constraint derived from representation theory
rather than assumed.

---

## Pass 2006 — my `1/q` proof had a gap, and they found it

Pass 1982 claimed the converse: that every residual candidate frame is
`{M, g(M)}`. My argument was "the same uniqueness forces `M' = g(M)`". It does
not. Uniqueness gives that `M' ∩ L_p` is a *single point*; it does not give that
that point is `g(p)`. `L_p` has `q+1` points and `g(p)` is only one of them.

The parallel track's Pass 1974 isolates exactly this as the **candidate-orbit
property**, verified at `q = 3, 5, 7` and open in general. **Their scoping is
correct and mine was not.** What my proof actually establishes, unconditionally:

- the involution-generated frames `{M, g(M)}` *are* candidates, `q(q²+1)/2` of them;
- they touch `(q+1)(q²+1)/2` residual edges with multiplicity exactly `q`;
- for `q` even no such `g` exists, so that subfamily is empty.

The step from "this subfamily" to "all candidates" is the open converse. The
`1/q` ratio is therefore proved *for the involution-generated subfamily* and
measured for the whole candidate set.

---

## Pass 2008 — the degree-ambiguity table

Extending Pass 2003 to every degree either track has used:

| index | subgroup classes | verdict |
|---|---|---|
| 15, 20, 24, 30, 60, 81 | **0** | no transitive `G`-set of this degree exists at all |
| 27, 36, 45 | 1 | **safe** — a count match is sufficient |
| 40 | 2 | **ambiguous** (the point/line duality) |
| 90 | 3 | **ambiguous** |
| 120 | 2 | **ambiguous** |
| 270 | 8 | **ambiguous** |

Two things worth flagging to the other track. Degrees **90 and 120 are
ambiguous** — any "these 90 are those 90" claim needs the character test, not a
count. And degrees **15, 20, 24, 30, 60, 81 admit no transitive `PGSp(4,3)`
action at all**, so identifications at those sizes are necessarily statements
about a smaller group (their exceptional `S₆`), never about `G` — which is
consistent with how they have posed them, and worth having in a table.

---

## Pass 2007 — the 360-orbit: an arithmetic hint, not a claim

The 360-orbit of spread pairs has stabiliser of order 144, and `1152/144 = 8`
where 1152 is the octet (polar-pair) stabiliser. So `360 = 45 × 8` *arithmetically*
fibres over the 45 octets.

**That is exactly the reasoning that produced two false claims** (Passes 1875,
1984). It is recorded as an arithmetic observation requiring the character test,
and the test is not run here. No correspondence is claimed.

---

## Passes 2009, 2010 — not done

- Naming the three classes that share the 270's centraliser signature (sizes
  1620 and 540): **not attempted this pass.**
- Orbit-built parallel classes with enumerated subgroup classes filtered by
  orbit length: **not attempted this pass.** Pass 2002's diagnosis stands as the
  spec for how to do it.
- Why two spreads meet in exactly 1 or 4 lines: **not attempted.**

Listed rather than silently dropped.

---

## Prior art

- Passes 1971–1975 (parallel track) — **own** the maximality correction, the
  candidate-orbit scoping that corrects my Pass 1982, the v5 constraint-audit
  library, the propagation-horizon diagnosis, and the 32-row claim ledger.
- Pass 1963 — the linear confinement Pass 2005 bounds to first order.
- Pass 2003 — the ambiguity sweep Pass 2008 completes.

## Still open

- The candidate-orbit property, for all `q`.
- Whether the quadratic couplings are physically meaningful or only
  representation-theoretic room.
- `χ(H) = 9`.
