# Pass 462 — cover-law lemma L1 in Lean at q=3

The new module `formal/W33/Pass462CoverLawL1Q3.lean` joins the generic Pass-447/457 span-perpendicular argument to an explicit finite symplectic model.

It defines:

- \(\mathbf F_3^4\);
- the alternating symplectic form;
- canonical representatives of the 40 points of \(PG(3,3)\);
- the fixed point \(p_0\);
- the 27-point opposite chart;
- the central-elation translate \(z_t x\);
- projective common-neighbor and bulk predicates.

The module proves without `sorry` or custom axioms:

\[
\text{common}(x,z_tx,w)\Longrightarrow w\in p_0^\perp,
\]

for every opposite point \(x\) and nonzero \(t\), together with the exact cardinalities

\[
|\Gamma(x)\cap\Gamma(z_tx)|=4=q+1,
\]

and

\[
|\Gamma(x)\cap\Gamma(z_tx)\cap\text{bulk}|=0.
\]

These are packaged as `q3_cover_law_L1`. The abstract span/perp bridge remains generic over every field and module.

## Boundary

This is the first end-to-end formal L1 instance, at \(q=3\). A uniform symbolic projective-cardinality proof for every odd prime power remains open.
