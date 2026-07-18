# Pass 436 — Polhill genuinely-nonabelian PDS audit

## Verdict

The novelty gate is closed in the negative for the **parameter family and Heisenberg PDS construction**.

Polhill, Davis, Smith, and Swartz, *Genuinely nonabelian partial difference sets*, Journal of Combinatorial Designs 32 (2024), 351–370, explicitly contain all of the following:

1. Corollary 4.7 states that a PDS with parameters

   \[
   (q^3,q^2+q-2,q-2,q+2)
   \]

   cannot be abelian when \(q\) is odd.
2. The discussion immediately following Theorem 4.8 states that two known constructions provide nonabelian PDSs with these parameters.
3. The first construction works for every odd prime power and uses the Heisenberg group over \(GF(q)\).
4. The smallest case is explicitly identified as \((27,10,1,5)\).
5. An explicit \((27,10,1,5)\)-PDS in the order-27 Heisenberg group is displayed.
6. The resulting graph is identified with the complement of the Schläfli graph.

The Heisenberg construction is attributed there to William M. Kantor, *Generalized polygons, SCABs and GABs*, Lecture Notes in Mathematics 1181 (1986), 79–158. The second, exponent-\(p^2\) construction is separately attributed in that literature.

## Required correction

The repository must not claim novelty for:

- existence of the Heisenberg PDS;
- the parameter family;
- genuine nonabelianness of the family;
- the \(q=3\) \((27,10,1,5)\) instance.

The previous sentence “whether this family appears elsewhere is left open” is false and is removed in this pass.

## Surviving project contribution boundary

The following remain distinct repository contributions, subject to their own proofs and attribution checks:

- recovering the known Heisenberg PDS as **flat section plus center** inside the elation action of \(W(3,q)\);
- proving the antipodal cover law for the bulk and locating the fiber pairing as the exact operation producing the known SRG;
- classifying the nine linear cover sections at \(q=3\) as one \(\operatorname{Aut}(H)\)-orbit;
- the complete prime-to-characteristic Smith theorem of Pass 435;
- the full Smith weld of Pass 437;
- the finite-field versus residue-ring conductor atlas of Pass 438;
- the torsion-sensitive optical falsifier of Pass 439.

## Release decision

The final open v1.2 gate is closed. Version 1.2 may ship with the corrected attribution language and with no novelty claim for the PDS family itself.
