# Pass5603–5610 external prior-art boundary

Checked 2026-08-16 UTC.

## PSL2 fixed-point / character background

Primary source used: Ling Long, Rafael Plaza, Peter Sin, Qing Xiang, *Characterization of intersecting families of maximum size in PSL(2,q)*, arXiv:1608.07304.

Relevant established input from their Section 2:
- `PSL(2,q)` acts 2-transitively on the `q+1` points of `PG(1,q)` for odd prime powers `q`.
- projective transformations are separated by their eigenvalue/fixed-point behavior;
- the standard degree-`q` character is `#Fix(g)-1`;
- the remaining complex characters are organized into principal and cuspidal families.

Pass5603 uses that standard character framework as input and records the repo-specific fusion eigenmatrix, multiplicity aggregation, and symbolic Bose–Mesner structure-constant closure. No priority claim is made for the general PSL2 character table.

## M12 / ternary-Golay twelve

Authoritative database checked: ATLAS of Finite Group Representations, `M12` page.

ATLAS gives `|M12|=95040` and the maximal-subgroup orders `7920, 1440, 660, 432, 240, 192, 192, 72` (with repeated conjugacy classes where applicable). None is divisible by `576`. Therefore no subgroup of `M12` can have order `576`: any proper subgroup would lie in a maximal subgroup, and Lagrange would require its order to divide the maximal subgroup order.

Pass5608 independently constructs the induced monomial action on the twelve projective weight-12 ternary-Golay lines and obtains order `95040` with orbital sizes `12,132`. Thus the negative identification with the order-576 rank-3 Reye/Latin/F4 action does not rest on the ATLAS order table alone.

## Physical boundary

No external source was found or used to claim that the finite magnetic operator of Pass5609 is a physical Hamiltonian, spacetime Laplacian, Lorentzian wave operator, or experimentally realized system. The phase-twisted spectrum and Z3 Wilson flux are internal finite calculations; their physical interpretation remains a hypothesis to be tested by a scaling/continuum program.
