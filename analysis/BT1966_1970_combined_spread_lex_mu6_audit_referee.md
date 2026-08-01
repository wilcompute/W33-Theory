# Passes 1966–1970 — combined spread symmetry, all forty cuts, the intrinsic phase role, constraint audit, and referee draft

The five requested fronts are complete with **35/35** frozen checks.

## 1966 — combined spread-signature geometry

The 36 spread-by-colour counts are now explicit variables in the same model as the 540 frame-colour variables. A deterministic linear functional on this signature supplies geometric orbit-minimum cuts. The nine-colour model has 5,184 variables, 3,033 base constraints, and 3,073 constraints with all forty cuts. On the exact 25,920-element PSp orbit of a known proper 14-colouring, the forty cuts retain 807 representatives. A bounded nine-colour HiGHS run remains `UNKNOWN`.

## 1967 — all forty point transvections

The forty cut coefficient vectors have rank 40. Exact survivor counts are 13,021 after one cut, 6,520 after three, 3,244 after eight, 1,756 after sixteen, 1,219 after twenty-four, 950 after thirty-two, and 807 after forty. Thus the full family removes 96.8866% of the known feasible orbit while retaining representatives.

## 1968 — what the internal `mu6` is

The finite integral centralizer torsion is `(C2)^4 x C6`. Its unique odd Sylow `C3=<mu6^2>` is characteristic. Every nontrivial phase power fixes exactly the 150-dimensional rational block sum and acts on the Eisenstein coexact 90. The outer involution inverts `mu6`; together they generate `D12`. This gives an intrinsic representation-theoretic description: a cyclotomic sector marker and chirality-reversed internal clock. No physical identification is made.

## 1969 — backward constraint audit

The audit distinguishes vacuous constraints, scope errors, restrictive-but-invalid cuts, and verified constraints never inserted. Exact replays include `504->504` for a no-op, `504->252` for a real cut, `81->81` for `x<=y+8`, the certified spread-cap counterexample `13>5`, model growth `249->249` for the unused Pass-1955 cut, `249->1209` for Pass 1956, and `3033->3073` plus orbit reduction `25920->807` for Pass 1966. The two oldest builders were not located and remain postmortem-only.

## 1970 — referee-shaped standalone draft

`analysis/W33_SPREAD_OBSTRUCTION_REFEREE_DRAFT.tex` now gives a self-contained article structure: abstract, definitions, theorem-status labels, finite-case scope, prior-art ownership, a consolidated withdrawal table, reproducibility checklist, and five open problems. It explicitly keeps `chi(H)=9` open and does not treat the draft as publication or peer review.

## Boundaries

- `chi(H)=9` remains undecided.
- Orbit reduction on a known feasible 14-colouring is not a nine-colouring proof.
- The internal `mu6` is not identified with charge, flux, QCD colour, a generation index, or a particle.
- A missing historical audit stamp is not proof of unsoundness.
- Two oldest constraint failures are documented from the maintained postmortem because their original executable builders were not located.
