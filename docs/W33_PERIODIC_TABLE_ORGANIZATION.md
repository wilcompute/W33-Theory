# W33 Periodic Table Organization

This note sets a stable naming policy for the living W33 paper.

The main organizational mistake to avoid is mixing five different things under one label:

1. carrier
2. realization
3. algebra
4. computation
5. witness

The repo is strongest when those five layers stay separate and each claim says exactly which layer it belongs to.

## 1. Core distinction

| Layer | Meaning | Guiding question |
| --- | --- | --- |
| Carrier | The exact finite or geometric object on which data lives | What is fixed? |
| Realization | A concrete presentation of the same carrier | How is it presented, embedded, or drawn? |
| Algebra | The law acting on the carrier | What structure is preserved? |
| Computation | A verified transition, split, lift, or operator on that carrier | What changes, and what stays fixed? |
| Witness | The smallest exact datum proving the frontier statement | What single target remains? |

## 2. Symbol policy

Use symbols by role, not by local convenience.

- Reserve `q, v, k, lambda, mu, r, s, f, g, E, T, Theta, Phi3, Phi6, Phi12` for carrier-level invariants of `W(3,3)` and its immediate finite packets.
- Use `C_*` for carrier families.
- Use `R_*` for realizations of a fixed carrier.
- Use `A_*` for algebras or law packages acting on a carrier.
- Use `O_*` or `F_*` for operators and functors.
- Use `W_*`, `Delta*`, or explicit coordinate names for frontier witnesses.

Recommended reading rule:

1. Name the carrier first.
2. Name the realization second.
3. Name the algebra third.
4. Name the computation fourth.
5. Name the remaining witness last.

If one sentence cannot say those five items in order, the statement is probably still mixing levels.

## 3. The periodic table itself

The useful analogy is not a literal chemistry-style table of disconnected objects. The repo behaves more like a two-axis table:

- rows: carrier and realization families
- columns: algebra and computation types

| Row | Exact anchor | Algebra layer | Canonical computation |
| --- | --- | --- | --- |
| Finite incidence row | `W(3,3)`, `AG(2,3)`, Hesse packet | incidence and symplectic/Pauli laws | incidence, complement, quotient |
| Cubic/moduli row | Schlaefli `27/45`, Burkhardt `40` | exceptional and cubic-surface symmetry packages | orbit matching, transport across models |
| Toroidal realization row | cataloged `5` Csaszar and `2` Szilassi realizations | common half-turn `Z2` symmetry | duality and orbit comparison |
| Pascal sector row | Gaussian row `[1, 40, 130, 40, 1]` | signed sector algebra, Seidel split | `130 = 40 + 90`, local `13 = 4 + 9` |
| Transport frontier row | fixed `81 -> 162 -> 81` package | unipotent/holonomy/nilpotent transport algebra | witness activation, affine displacement |
| Exceptional envelope row | exact qutrit ladder with E8-side `E6 + A2` boundary: `27`, `240`, `729`, and `72 + 6 + 162` | exact finite extension ladder and zero-sector `E6 + A2` split | ladder closure up to the E8 boundary |

The word "periodic" is useful because the same columns recur across different rows. The word is limited because the algebra side is not one flat list. For algebras, the better analogy is a magic-square layout: interacting inputs produce different symmetry envelopes.

Same-table bridge theorem.

These rows belong in one table because they are distinct exact layers of one
q=`3` backbone:

- the realization row supplies one exact dual realization packet
- the Pascal row and exceptional row share the same `40`-point / `240`-edge shell
- the frontier row and exceptional row share the same `81` seed
- the exceptional row extends that same backbone only up to the E8-side
 `E6 + A2` boundary, while the frontier row keeps the remaining witness problem
 explicit

So the table is not a pile of analogies. It is one exact finite backbone read at
four different verified layers.

On the source-dictionary side, imported CCT terms should now say which shared
backbone invariant they are using: the `40` shell, the `81` seed, or the `240`
edge/root shell, with the q=`3` selector recorded separately when needed.

## 4. Csaszar and Szilassi should be used as a realization row

The repo already contains an exact realization-level bridge. Its point is subtle and important.

What is exact:

- there are `5` cataloged Csaszar realizations and `2` cataloged Szilassi realizations in the archived sheet used by the bridge
- all `7` cataloged realizations share the same half-turn symmetry `(x, y, z) -> (-x, -y, z)`
- the induced orbit data is dual
- Csaszar realizations have `4` vertex orbits and `7` face orbits
- Szilassi realizations have `7` vertex orbits and `4` face orbits

What is not yet exact:

- the count `5 + 2 = 7` is not yet proved to be a canonical algebra of realizations
- the bridge does not classify those models up to affine, projective, or isotopic equivalence

So these objects should organize the realization layer, not be overpromoted into a finished seven-element algebra. Their exact use is as a duality template:

- Csaszar = vertex-complete toroidal seed
- Szilassi = face-complete toroidal dual seed

That is already enough to justify a "realization row" in the table.

## 5. Pascal tells us what computation means

The Pascal material stops being decorative as soon as the Gaussian row is read as geometry.

The exact line-level facts are:

- `[4 choose 2]_3 = 130 = 40 + 90`
- the `40` are totally isotropic projective lines
- the `90` are non-isotropic projective lines
- this induces `780 = 240 + 540` on the edges of `K_40`
- through each projective point, `13 = 4 + 9`
- the signed sector operator is `S = A - A_N`

The Pascal row now sharpens further on the target side. Centering the spread
and anti-line probes resolves the line module as `40 = 1 + 15 + 24`. The spread
channel becomes an exact `ETF(36,15)`, the anti-line channel collapses to a
doubled `45`-vector transport frame in the `24`-sector, and both channels
share a Naimark shadow `21 = 1 + 20` whose sign graphs are swapped by
complement. The executable surfaces are
`scripts/w33_parseval_measurement_frame_audit.py`,
`scripts/w33_parseval_target_geometry_audit.py`,
`tests/test_w33_parseval_measurement_frame_audit.py`, and
`tests/test_w33_parseval_target_geometry_audit.py`.

This gives the right internal meaning of computation.

In this program, computation should usually mean one of five exact actions:

1. quotient or projectivization
2. dualization
3. sector splitting
4. transport or lift
5. witness activation

That is stronger than "doing arithmetic with interesting numbers." It means applying an exact operator to a fixed carrier and tracking what invariant package survives.

## 6. Algebra families

The paper should define algebras by action, not by rhetoric.

### Incidence algebra

Points, lines, complements, cliques, and local neighborhoods on the finite carrier.

### Symplectic/Pauli algebra

The two-qutrit commutation law and its Clifford/symplectic symmetry package.

### Sector algebra

The Pascal/Seidel split between isotropic and non-isotropic sectors on the same ambient geometry.

### Transport algebra

Holonomy, nilpotent increments, and carrier-preserving K3 tail transport on the fixed host.

### Exceptional envelope

The exceptional row should no longer be treated as a rhetorical bucket.
The exact executable row now available in the repo is:

- one-qutrit local shell of size `27`
- two-qutrit kernel with `240` edges on `W(3,3)`
- exact three-qutrit / six-qutrit match at operator size `729`
- E8-side root split `72 + 6 + 162 = 240`
- E8-side line orbits `36 + 27 + 27 + 27 + 1 + 1 + 1`

What remains non-exact is not the finite row itself but the last promotion step:
there is still no functorial derivation from the qutrit kernel alone all the
way to the E8-side decomposition. The exact statement is therefore an
exceptional-envelope row with a controlled boundary, not a finished exceptional
unification theorem.

This ordering matters. The exceptional envelope should sit at the top as an organizing compression, not replace the exact lower layers that are already verified.

## 7. Working definition of computation

A good sentence for the paper is:

> Computation is a verified carrier-preserving transition between realizations or sectors, expressed by an exact operator and reduced to a smallest witness when a frontier remains.

Examples already present in the repo:

- `81 -> 40` by projectivization
- Csaszar `<->` Szilassi by dual realization logic
- `130 -> 40 + 90` by Pascal line split
- `H = I + N` by unipotent transport language
- `Delta C = 14105` by witness activation on the fixed tail package

## 8. Recommended paper flow

For each major section, try to keep the same order.

1. Fix the carrier.
2. State the realizations currently in play.
3. State the algebra acting on them.
4. State the exact computation or operator.
5. State the surviving witness or frontier.

This is the cleanest way to make the paper read like a genuine framework instead of a stack of numerological correspondences.

## 9. Exact anchors already in the repo

- `exploration/w33_realization_orbit_bridge.py`
- `tests/test_w33_realization_orbit_bridge.py`
- `exploration/w33_mobius_szilassi_dual.py`
- `tests/test_w33_mobius_szilassi_dual.py`
- `PART_LXIV_PASCAL_LINE_SPLIT_THEOREM.md`
- `PART_LXIV_pascal_line_split.py`
- `part7_pascal_information_functor.tex`
- `scripts/w33_q3_master_lock_audit.py`
- `tests/test_w33_q3_master_lock_audit.py`
- `scripts/w33_parseval_measurement_frame_audit.py`
- `tests/test_w33_parseval_measurement_frame_audit.py`
- `scripts/w33_parseval_target_geometry_audit.py`
- `tests/test_w33_parseval_target_geometry_audit.py`
- `scripts/w33_qutrit_ladder_audit.py`
- `tests/test_w33_qutrit_ladder_audit.py`
- `scripts/w33_e8_correspondence_boundary_audit.py`
- `tests/test_w33_e8_correspondence_boundary_audit.py`
- `scripts/w33_cct_crosswalk.py`
- `tests/test_w33_cct_crosswalk.py`
- `scripts/w33_periodic_table_organization.py`
- `tests/test_w33_periodic_table_organization.py`

The organization language is now also executable. The summary surface

- `scripts/w33_periodic_table_organization.py`

packages the realization row, Pascal computation row, frontier
witness row, and exceptional-envelope row into one checked table. The
exceptional row itself is sourced from the exact ladder and boundary
surfaces

- `scripts/w33_qutrit_ladder_audit.py`
- `scripts/w33_e8_correspondence_boundary_audit.py`

and the exporter

- `tools/export_w33_periodic_table_organization.py`

freezes that exact surface as the tracked artifact

- `artifacts/w33_periodic_table_organization_summary.json`

The focused test file

- `tests/test_w33_periodic_table_organization.py`

now also loads the committed artifact and checks it directly against
`build_payload()`, so the frozen JSON cannot drift away from the
executable summary. The appendix taxonomy in `w33_paper.tex` points to
the same script, test, and artifact trio.

Those are enough to support the organization scheme without inventing a new speculative layer.
