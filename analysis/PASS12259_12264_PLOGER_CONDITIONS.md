# Passes 12259–12264: the Wilson-line conditions settled; the corpus audited against them

Claude track. Producer: `analysis/w33_pass12259_to_12264_ploger_conditions.py`. Drivers: `analysis/search_drivers_12259/`. That folder includes
a text extract of hep-th/0702176.

## 12259: which condition is correct

Plöger, Ramos-Sánchez, Ratz and Vaudrevange (*Mirage torsion*, JHEP 04 (2007) 063) give conditions (7a)–(7f). Two matter
here:

- **(7d):** N_a(A_a·V_i) ∈ 2ℤ;
- **(7f):** gcd(N_a, N_b)(A_a·A_b) ∈ 2ℤ.

They derive both from Φ_vac(g, h)^{gcd(n,s)} = 1 (their A.11), i.e. from requiring well-defined projection phases. Inputs
that satisfy only the mod-1 forms are consistent only after a lattice shift, which in general changes the spectrum
("mirage torsion"). Read directly, their projections are ill-defined.

(7d) for V0 is our 12235 parity condition. **The non-supersymmetric orbifolder checks only the mod-1 form of (7f).**

### Audit against all of (7a)–(7f)

| model set | consistent |
|---|---|
| A8 Standard Models | 104/104 |
| three-family bases (12111) | 9/9 |
| twisted-10 models (12217) | 88/153 |
| SU(5)×U(1) scans (12161–12182) | 86/163 |

Only (7f) ever fails.

## 12260: the engine disagreement

The engines still disagree on Witten-twisted 10s in the fully consistent models. A sector-resolved comparison needs the
patched N=0 engine rebuilt with sector output; the rebuild attempt failed at link time. **Located, not resolved.**

## 12261: existence counts restated on the consistent sets

| set | consistent / total | three-generation (consistent / total) |
|---|---|---|
| 12163, third torus | 57/121 | 20/52 |
| 12182, third torus | 31/53 | 12/21 |
| twisted-10 models | 88/153 | 32/58 |

Scalar 10s: 0 in every set. Theorem 7.7 is unchanged.

## 12262: cross-track review

The note now states the settled condition and is offered to the other track for review; a decision is logged.
