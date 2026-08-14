# Pass5182–5189 executed outcomes

**Status:** EXECUTED 2026-08-14, pending final namespace close after replay wiring. This packet is collision-reconciled against the independently landed Pass5174–5181 continuation and does not overlap the reserved Pass5190–5197 range.

## 5182 — q=5 strict counterexample leader ≥32

Pass5173 gave adjacent-pair cap 52 at leader size 30. For m=31 the deletion cap is 55. Pairwise Delsarte gives weight ≥797 through N1=41; the sharpened path relaxation closes N1=42..55. The weakest layer is N1=54 at 673; N1=55 rebounds to 832 because only the leaf-free degree profile survives. Hence every q=5 word below 625 has minimum chamber leader at least 32.

## 5183 — q=5 strict counterexample leader ≥33

A selected five-edge Levi path has outer chamber edges at gallery distance four. Such a pair lies in one apartment and has exactly two shortest galleries inside its C8, so P5≤2N4. At m=32 this raises the sole failing N1=56 branch to 631; N1=58 is impossible and nearby N1=55,57 were already 648,742. Hence strict counterexamples require leader ≥33.

## 5184 — all-q N3 quadratic-form bridge

For selected point/line degree vectors x,y,

    (x^T A_P x + y^T A_L y)/2 = N1 + 2N2 + N3.

The W point/line graphs have nontrivial eigenvalues q-1 and -(q+1), giving

    z^T A z <= (q-1)||z||^2 + m^2/(q+1).

At q=5,m=33 the upper spectral defect lies in 3/2+2Z>=0, yielding the exact integer cap

    N1+2N2+N3 <= 312+4N1.

This improves the leader-33 frontier but does not close it.

## 5185 — full cut-coset leader inequality

Pass5110 identifies the chamber-generator kernel with the full binary Levi cut space. Therefore a minimum chamber representative Y obeys, for every Levi vertex subset S,

    2|Y cap delta(S)| <= |delta(S)|,

or

    2 e_Gamma(S) <= 4 e_Y(S) + sum_v ((q+1)-2d_Y(v)).

At q=5 every host incidence between two selected-degree-three vertices must be selected, and every host 3-2-3 path contains a selected edge. This promotes the global coset-leader geometry beyond the singleton degree cap.

## 5186 — P components recover the W point graph

Chamber-star P-component footprints are canonically indexed by W-points. Each P component is supported on 2(q+1) points inducing K_{q+1,q+1}; its (q+1)^2 minimum tensor atoms are exactly the collinearity edges of that K_{q+1,q+1}. Two point footprints intersect in q components if the points are collinear and one component otherwise.

At q=5: 156 point footprints of size 25, 325 K6,6 component blocks on 12 points, and 36 minimum atoms per component.

## 5187 — P components are hyperbolic polar-pair dual grids

A P chart indexed by opposite points p,r determines the non-isotropic projective line H=<p,r>, while the common-neighbour line is H^perp. The connected P chart component is therefore indexed by the unordered polar pair {H,H^perp}; its point carrier H union H^perp is a dual grid.

For point-by-component incidence B and ordinary point-line incidence N,

    BB^T=(q^2-1)I+(q-1)A+J=(q-1)NN^T+J.

Every W line meets every dual grid in 0 or 2 points, so N^T B=0 over F2. Odd-q binary rank equality is frozen only as anchors q=3,5,7,11, not promoted all-q.

## 5188 — exact q=5 dual-grid incidence code

At q=5, rank_2 N=91 and rank_2 B=65. Since N^T B=0 and 91+65=156,

    im_F2(B)=ker_F2(N^T).

Thus the q=5 point-incidence dual is

    [156,65,12]_2,

with exactly 325 minimum words, the 325 P-component dual grids. This materializes one 65-dimensional incidence-dual half behind the Pass5130 bicycle count 129=2*65-1.

## 5189 — all-q minimum shell of the binary W-line dual

For every q, any nonzero point set meeting every W line evenly has at least 2(q+1) points. Equality forces an induced K_{q+1,q+1}, hence a hyperbolic polar-pair dual grid. Therefore

    d(C(W)^perp)=2(q+1)

and the complete minimum shell consists of exactly

    q^2(q^2+1)/2

dual grids, canonically the P tensor components.

## Evidence boundary

The q=5 apartment-code minimum-distance theorem remains open at chamber leaders >=33. The weight-625 equality shell still needs the connected L-side gluing; the P-side 25-atom reduction and classical dual-grid outer code do not prove emptiness. For even q>=4, minimum dual-grid words need not span the entire incidence dual. All claims in this packet are finite geometry/code statements, not physical performance claims.
