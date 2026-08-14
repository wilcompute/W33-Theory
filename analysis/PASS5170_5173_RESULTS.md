# Pass5170–5173 executed outcomes

**Status:** EXECUTED 2026-08-14. This packet continues the q=5 apartment-code distance frontier after Pass5169 while preserving the strict evidence firewall. It does **not** claim the q=5/all-q minimum-distance theorem.

## Pass5170 — distance-three injection closes leader 28

A cut-minimal chamber leader is a bipartite subcubic girth-eight Levi subgraph. Selected three-edge paths inject into opposite-part nonedges; otherwise two paths with the same endpoints create a C4 or C6. A leaf reaches at most four opposite vertices by such a path and therefore forces unreached nonedges. For m=28 the raw deletion cap is N1<=51; N1=51 is impossible by endpoint-degree sums, and every ordered bipartition degree profile at N1=49,50 violates the new injection/leaf constraints. Hence N1<=48, where the exact cubic lower bound is 651. Strict q=5 counterexamples therefore require leader >=29.

## Pass5171 — P4/N3 coupling closes leader 29

A selected four-edge Levi path injects into its outer chamber pair at gallery distance three, giving P4<=N3. At m=29, N1=51 is impossible and the generic cubic relaxation closes N1<=49. At N1=50 the distance-three/leaf test removes every six-leaf profile. Conditioning the exact Delsarte program on N3>=P4 gives weight lower bounds 715 for the leaf-free degree type and 630 for the three-leaf degree type. Strict counterexamples therefore require leader >=30.

## Pass5172 — all-q incidence bridge for N2

For any selected chamber set Y, with point/line degree vectors x,y, incidence matrix N, size m, and adjacent-pair count N1,

    N2 = x^T N y - (m+2N1).

For W(3,q), NN^T=(q+1)I+A_point has eigenvalues (q+1)^2, 2q, 0. Thus sigma_2(N)=sqrt(2q), yielding an exact spectral upper bound on N2 once the point/line adjacent-pair split is known. This is an intrinsic matrix bridge between the Levi degree profile and the chamber association-scheme/Delsarte variables.

## Pass5173 — sharp P5 extension closes leader 30

Let td count endpoint incidences of selected four-edge paths at selected degree d. Then

    P5 = 2P4 - t1 - t2/2.

A degree-one endpoint can terminate at most 8 four-edge paths and a degree-two endpoint at most 16, so

    P5 >= max(0,2P4-8n1-8n2).

At m=30, N1=53 is impossible. Pairwise Delsarte gives weight >=776 through N1=40; the strengthened cubic bound gives 827 at N1=50; and after P4<=N3 coupling the dense N1=51,52 layers give 794 and 760. Strict q=5 counterexamples therefore require chamber leader >=31.

## Evidence boundary

The q=5 minimum-distance theorem remains open for leaders >=31, and the weight-625 equality shell remains unclassified. The promoted claims are finite generalized-quadrangle/code, association-scheme, and spectral-incidence statements. They are not hardware timing, optical-noise, fault-tolerance, or particle-identification claims.
