# Passes 4475 and 4478 — primary-literature boundary

## Artin–Ihara covering-graph context

H. M. Stark and A. A. Terras, **“Zeta Functions of Finite Graphs and Coverings, Part II,”** *Advances in Mathematics* **154** (2000), 132–195, DOI 10.1006/aima.2000.1917.

That paper develops Galois theory for normal unramified finite graph coverings, attaches graph analogues of Artin L-functions, proves covering-zeta factorisations into L-functions, and derives Ihara/Bass-type determinant formulas.  Pass 4475 uses that established language only as context.  The W33-specific coefficient identities

```text
tr(B_sigma^3) = 24 sum_l sigma_l
tr(B_sigma^4) = 960 + 8 W4
log L_sigma(u) = 8(sum_l sigma_l)u^3 + (240+2W4)u^4 + O(u^5)
```

are the repository's finite calculation and are regenerated independently by `analysis/w33_pass4472_4479_apartment_module_thermo_ihara_pauli.py`.

## Real four-qubit Pauli geometry

M. Saniga, P. Lévay and P. Pracna, **“Charting the Real Four-Qubit Pauli Group via Ovoids of a Hyperbolic Quadric of PG(7,2),”** arXiv:1202.2973 (2012).

The paper describes the real four-qubit Pauli geometry in `W(7,2)` / a hyperbolic quadric and records the split into **135 symmetric** and **120 skew-symmetric** nonidentity Pauli elements.  Pass 4478 does not infer its result from those counts: it constructs an explicit hyperbolic basis of the independently obtained apartment 8-space and verifies on all 256 vectors that its invariant quadratic becomes

```text
q(a_1,b_1,...,a_4,b_4) = sum_i a_i b_i mod 2,
```

which is the parity of Y-like positions in the standard binary Pauli representation.  The literature then independently confirms the 135/120 geometric interpretation.

## Boundary

Neither citation supplies the W33 apartment-code construction.  Conversely, the finite isometries here do not imply a physical four-qubit implementation, a physical gauge field, or continuum Artin/Ihara dynamics.  The citations establish the ambient mathematical languages; the executable W33 identities are separate claims with separate certificates.
