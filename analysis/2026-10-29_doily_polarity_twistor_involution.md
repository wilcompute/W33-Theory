# Symplectic doily polarity makes the finite twistor transform an involution

**2026-10-29; exact algebraic research extension.** This short packet builds on the committed 30-code/15-state transform in analysis/2026-10-29_klein_e8_hamming_twistor_transform.md. Classical point-plane duality and W(3,2) are well known; the specific orthogonal operator model and comparison with our eight-qubit state-frame map are project-specific.

Define the nondegenerate symplectic form on four binary coordinates by B(x,y)=x0*y1+x1*y0+x2*y3+x3*y2. The fifteen nonzero vectors of F2^4 are the points of PG(3,2). The map p→p-perp is a symplectic polarity identifying each point with one of the fifteen projective planes.

The 15x15 **symmetric** point-plane incidence matrix M has M[p,q]=1 iff B(p,q)=0. Counting orthogonal hyperplane intersections proves M^2=4I+3J. Every row contains seven ones, including its diagonal. The off-diagonal collinearity adjacency A=M-I is the symplectic GQ(2,2) or *doily*, an SRG(15,6,1,3) with spectrum 6(1), 1(9), -3(5). Direct enumeration reconstructs exactly fifteen totally isotropic projective lines with three points each.

The **same rational normalization** as the Klein two-ruling code-state transform,

    T=(3M-J)/6,

now gives a **symmetric orthogonal involution**: T=T^T and T^2=I. Since trace(T)=5, its +1 eigenspace has dimension 10 and its -1 eigenspace dimension 5. The constant vector lies in the +1 sector. The 10-dimensional +1 sector splits under Sp4(2) into trivial dimension1 and dimension9; the -1 sector has dimension5.

This is an explicit coordinate choice via polarity of the abstract finite two-ruling incidence transform from the preceding commit; the two ordered 15-state lists must be relabeled accordingly before writing T as symmetric. The corresponding **finite state transform** is not Penrose's holomorphic sheaf-cohomological transform; it does not produce spacetime, a quantum field equation, or an E6/SU5 particle multiplet. The coincidence of the 10+5 dimensions with a chosen particle-physics branching is not evidence of an embedding.

Executable checks: analysis/w33_20261029_doily_polarity_twistor_involution.py; tests/test_w33_20261029_doily_polarity_twistor_involution.py; frozen certificate data/w33_20261029_doily_polarity_twistor_involution.json. Independent local tests **2/2 pass**. The same project now has two finite incidence transforms of distinct types: the earlier point-to-line Radon map (rank11), and this polarity-normalized point-to-plane transform (rank15, invertible, involutive).

Independent falsifiers: (i) implement optical mode decompositions of the +10/-5 sectors; (ii) determine the actual H27 action on those sectors rather than assuming Sp4(2) is native; (iii) identify which, if any, finite incidence cohomology the involution preserves; (iv) check real-structure compatibility with a complex twistor lift; (v) test the 10+5 split against the canonical E6 matter regulator through actual representation matrices.
