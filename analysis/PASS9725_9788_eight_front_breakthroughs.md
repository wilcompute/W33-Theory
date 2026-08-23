# Passes 9725–9788 — derived-scheme no-go, full unitary glue symmetry, Witt-sign transporter obstruction, coherent Holonet, and three outside-box bridges

## Scope

This packet executes the five continuations queued after Pass9465–9528 and three additional attacks chosen after reading the live parallel lanes.  Passes 9725–9788 were reserved on master before any later claim in this interval.  Parallel work at Pass9701–9724 corrected the Leech filtration baseline and removed a frame-dependent Type-II-code interpretation; later Pass9801–9824 proved the Leech V2 generator is canonical but that an intrinsic Leech frame cannot coordinatize Lambda/2Lambda by mod-2 inner products.  Both corrections are treated as authoritative here.

The main change of direction is sharp: the missing Niemeier-to-Suzuki R weld is no longer merely 'not constructed'.  With the currently distinguished Lagrangian halves it is impossible by orthogonal Witt sign.  The same R nevertheless has billions of opposite-sign transverse Lagrangians, so the obstruction points to exactly what must change rather than killing the program.

## 1. Pass9725–9732 — the natural Q^-(5,3) association-scheme bridge is impossible

The 252 nonsingular projective points of the standard six-dimensional minus form split intrinsically into two norm fibers of 126.  For a source point of either norm, the natural O^-(6,3) coherent configuration has relation valencies

- same-fiber orthogonal: 45,
- same-fiber nonorthogonal: 80,
- opposite-fiber orthogonal: 36,
- opposite-fiber nonorthogonal: 90.

Therefore every O^-(6,3)-invariant undirected union on all 252 nonsingular points has degree in

`{0,36,45,80,81,90,116,125,126,135,161,170,171,206,215,251}`.

The exact G2(4) fixed-edge D-cell has size 252 but induced degree 66; 66 is absent from that list.  The tempting 126-point G2 B-union-C cell has induced average degree 31, while one Q^- norm fiber has only invariant degrees 45, 80 or 125.  Hence **no natural point-orbital union can realize either count match**.

The surviving bridge must move to a derived object such as nondegenerate two-spaces or R-transverse Lagrangians, or twist the G2 rank-14 orbitals in a way not induced by point orthogonality.

## 2. Pass9733–9740 — the full glue-pair stabilizer is O^-(6,3), not projectively trivial

Pass9465 exhaustively proved that the ordered ternary Golay/E6-relative pair has only `{+I,-I}` in its common **signed-coordinate monomial** stabilizer.  That statement was correctly scoped but is not the full intrinsic answer.

Inside

`C_Sp(12,3)(R) ~= U(6,3)`,

the complete stabilizer of the ordered pair `(C_G,C_E)` is

`O^-(6,3)`,

with

`|O^-(6,3)| = 26,127,360`,

projective order

`13,063,680`.

Proof: `C_E=R C_G`.  An element commuting with R and preserving C_G automatically preserves C_E.  Since `B=K R^T`, restriction to C_G lies in `O(B|C_G)`.  Conversely every `A in O^-(B|C_G)` extends uniquely by `u(Rg)=R A g`; the extension preserves B, commutes with R, hence preserves K.  Allowing the two halves to swap adjoins R and doubles the order to `52,254,720` because `R^2=-I` already lies in the ordered stabilizer.

So the concrete pair is coordinate-rigid but intrinsically orthogonal: a large distinction that matters for the transporter problem.

## 3. Pass9741–9748 — the two orientation bits agree abstractly, but their parent stabilizers cannot weld directly

The rank-24 line carriers give

`3^3:S4 -> C2`, kernel `3^3:A4`,

with orders `648 -> 324`.

The G2(4) edge carrier gives

`G2(2).2 -> C2`, kernel the ordered-edge stabilizer,

with orders `24,192 -> 12,096`.  Endpoint reversal exchanges the unique nonsymmetric rank-14 pair `AD <-> BB/CC`, each valency 1,512.

Thus both orientation structures are literally one-bit C2 quotients.  Since `Aut(C2)` is trivial, **once an external bridge identifies the underlying unoriented objects, the orientation identification is forced**.

But the parent groups cannot embed in either direction: their gcd is 216; the W33 line stabilizer has a `3^4` factor absent from the G2 edge stabilizer, while the latter has a factor 7 absent from the former.  Orientation is therefore a consistency bit, not the transporter itself.

## 4. Pass9749–9756 — canonical R transport is blocked by Witt sign

Both sides now have exactly the same formal symplectic architecture:

- a 12D symplectic F3-space,
- an order-four exchanger squaring to `-I`,
- a 6+6 Lagrangian polarization,
- the symmetric half-form `C_L(u,v)=K(u,Rv)` (Suzuki uses `J(u,xv)`).

The vendored ATLAS Suzuki matrix was rechecked: `x` is symplectic and `x^2=-I`.

But the canonical half-forms have opposite sign:

- glue/Golay half: `Q^-(5,3)`, 112 singular projective points;
- Suzuki/M12:2 half: `Q^+(5,3)`, 130 singular projective points.

Assume a symplectic transporter T sends the distinguished glue half to the distinguished Suzuki half and conjugates `R` to `x`.  Then `K(g,Rh)` is carried by congruence to `J(Tg,xTh)`.  Orthogonal sign and singular-point count are congruence invariants, forcing `112=130`, contradiction.

Therefore

**there is no polarization-compatible symplectic transporter for the currently canonical halves.**

This is stronger than the previous `7.88e19 choices` observation.  Hall–Janko endpoint orientation cannot fix a Witt-sign mismatch; the chosen Lagrangian must change on at least one side.

## 5. Pass9757–9764 — coherent 40 x 3 Holonet stress model

The optical discriminator is upgraded from intensity diffusion to complex amplitudes on

`40 W33 ports x 3 internal qutrit/OAM-time-bin modes`.

Each stage applies

- coherent W33 propagation `exp(-i theta A_W33/12)`,
- bounded independent port phases,
- bounded loss,
- a random small 3x3 internal unitary,
- finite multinomial detector shots,
- a noisy dark monitor.

The seeded classifier is deliberately simple:

- line fraction `<0.5` -> E8,
- otherwise dark fraction `>0.17` -> E6,
- else -> A2.

Moderate profile: 500 trials per carrier, 1,500/1,500 correct.  E8 line fraction stayed in `[0.056,0.148]`; line carriers stayed above `0.924`.  A conditional `++++` versus `+++-` phase realization of the orientation bit also separated perfectly.

Heavy profile: four stages, phase errors up to 0.60 rad, intensity-loss floor 0.70, 2,000 shots, 10% dark confusion.  Again 1,500/1,500 carrier classifications were correct: E8 line fraction at most `0.268`, line carriers at least `0.7675`; E6 dark fraction at least `0.276`, A2 at most `0.119`.  The phase-orientation score, however, lost sign separation.

This yields an experimentally useful hierarchy: **line support and dark fraction survive substantially stronger coherent disorder than a direct phase readout of the orientation bit.**  The orientation phase tag remains a conditional encoding model, not a derivation from hardware.

# Three outside-box attacks

## 6. Pass9765–9772 — R has two enormous transverse-Lagrangian sign orbits

For fixed symplectic complex structure `R^2=-I`, every Lagrangian `L` transverse to `RL` has nondegenerate symmetric form

`C_L(u,v)=K(u,Rv)`.

The unitary centralizer `U(6,3)` has exactly two such orbits:

| half-form | stabilizer | orbit size |
|---|---:|---:|
| `Q+(5,3)` | `O+(6,3)`, order 24,261,120 | **7,530,558,336** |
| `Q-(5,3)` | `O-(6,3)`, order 26,127,360 | **6,992,661,312** |

Total R-transverse Lagrangians: `14,523,219,648`; all Lagrangians of `Sp(12,3)`: `16,358,540,800`; nontransverse remainder: `1,835,321,152`.

This immediately supplies the escape route from the Pass9749 no-go: the canonical glue half is minus type, but the *same K and R* admit over 7.5 billion plus-type transverse Lagrangians.  The next selector problem is therefore precise: find a canonical plus-type glue Lagrangian (or a canonical minus-type Suzuki one), preferably from the Hall–Janko/Leech data.

## 7. Pass9773–9780 — if a uniform Leech-frame/Hall–Janko common selector exists, it is forced to have 13 states

Only the corrected parallel Leech facts are used:

- V2 is type-4-free: 0 type-4 classes versus generic singular-generator baseline 48;
- all 4,095 nonzero classes are intrinsic type-8 frames;
- the later parallel Pass9801 shows the pure order-8 class, hence V2, is canonical;
- but a frame itself gives rank only 1 as a mod-2 inner-product coordinate map, so the naive frame-coordinate route is closed.

The Hall–Janko/G2 carrier has 416 vertices and 20,800 edges.  Arithmetic gives

`gcd(4095,416)=13`,

`gcd(4095,20800)=65`,

`gcd(4095,416,20800)=13`.

Therefore, if all three canonical sets admit surjections onto one selector set S with constant fiber sizes (the minimal regularity for a transitive/equivariant common quotient), then

`|S| divides 13`.

The only nontrivial possibility is

`|S| = 13 = Phi_3(3)`.

This does **not** prove such a quotient exists.  It says that uniformity would force 13 uniquely; the newest parallel frame theorem further says it cannot arise from naive mod-2 frame coordinates.

## 8. Pass9781–9788 — the F9 glue and zeta_9 Bruhat–Tits filtration are the unramified and ramified halves of one degree-12 local field

This is the strongest cross-lane synthesis of the packet.

The transverse glue package gives

`F9^6 = F3^12`, with `R^2=-I`.

Since `x^2+1` is irreducible mod 3, adjoining its root gives the residue extension `F9/F3`; over Q3 this is the **unramified quadratic** extension `Q3(i)`.

Independently, the parallel Bruhat–Tits lane identifies the order-9 filtration with

`Q3(zeta_9)/Q3`,

a **totally ramified** extension of degree

`phi(9)=6`,

with uniformizer `pi=1-zeta_9` corresponding to the filtration direction `I-M`.

Unramified and totally ramified finite extensions are linearly disjoint.  Their compositum

`L = Q3(i,zeta_9)`

has

`[L:Q3] = e f = 6*2 = 12`,

ramification index `e=6`, residue degree `f=2`, residue field `F9`.

Moreover `3 = unit * pi^6` in `O_L`, so `O_L/3O_L` has a six-step pi-adic filtration and **each successive graded piece is F9**.  Its associated graded additive space is exactly

`F9^6`,

hence F3-dimension 12.

This gives a principled arithmetic interpretation of two previously independent discoveries:

- `R` is the **unramified degree-2/residue-field direction**;
- `I-M` / `1-zeta_9` is the **totally ramified degree-6/uniformizer direction**;
- together they naturally produce the degree-12 filtered object whose associated graded is the transverse glue phase space.

This is not yet an integral isomorphism between a Niemeier glue lattice and `O_L`; the claim is a standard local-field construction applied to the two exact repo structures, and the `F9^6` identification is associated-graded/additive rather than a semisimple ring identity.

## Net selector hierarchy after this packet

The old route

`marked line -> orthogonal sign -> R`

has been replaced by a more precise one:

1. natural Q^- point-scheme bridge: **ruled out**;
2. orientation C2: **compatible but insufficient**;
3. canonical minus glue polarization -> canonical plus Suzuki polarization: **ruled out by Witt sign**;
4. fixed R with a replacement plus/minus Lagrangian: **algebraically available in billions of choices**;
5. canonical selector for that replacement: **the real open problem**;
6. corrected Leech/Hall–Janko data constrain any uniform three-way quotient to **13 states**, but do not yet construct it;
7. local-field `(e,f)=(6,2)` synthesis gives a new arithmetic arena in which such a selector could potentially live.
