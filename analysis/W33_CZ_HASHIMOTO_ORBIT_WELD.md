# CZ-context / Hashimoto-turn weld

**Status:** exact finite-geometry theorem in a chosen Darboux gauge. The qutrit/photon interpretation is asserted only for `q=3`.

## Result

For odd prime `q`, let the two-qudit controlled-Z Clifford act on `V = X + P = F_q^2 + F_q^2` by the symplectic shear `G_B(x,p)=(x,p+Bx)`, with `B=[[0,1],[1,0]]`.

The all-q CZ theorem in this repository proves that the Lagrangian contexts of `W(3,q)` have cycle profile `1^(2q+1) q^(q^2+q-1)`. The non-fixed q-cycles refine as `(q-1)+q^2`: `q-1` cycles from contexts meeting the fixed Lagrangian `P` in a non-axis direction, and `q^2` cycles from transverse graph contexts because `S -> S+B` and `Sym_2(F_q)/<B> ~= F_q^2`.

Now fix the directed collinearity edge `e1 -> e2` in the same Darboux frame. Its non-backtracking continuations split intrinsically as `(q-1)+q^2`: `q-1` remaining points on the same generalized-quadrangle line and `q^2` points on the other `q` lines through `e2`.

The verifier constructs the explicit branch-preserving map `F_q^* disjoint_union F_q^2 -> F_q^* disjoint_union F_q^2` using `s -> [1,s,0,0]` and `(a,c) -> [a,c,1,0]` after projectivization. Hence `#(nontrivial CZ context orbits)=q^2+q-1=k-1`, where `k=q(q+1)` is the collinearity degree and `k-1` is the Hashimoto outdegree.

At `q=3`, this becomes `11=2+9`, exactly the independently verified W33 triangle-turn/open-turn decomposition of the 480-state nonbacktracking carrier. Thus, after fixing a compatible frame, one nontrivial CZ context orbit and one local routing continuation use the same finite instruction alphabet. This is a concrete gate/route weld behind the architecture slogan “routing a packet is applying a gate,” but it is deliberately weaker than a global equivariant identification.

## q=3 cyclotomic corollary

The fixed-context count is `2q+1`. Comparing with `Phi_6(q)=q^2-q+1` gives `Phi_6(q)-(2q+1)=q(q-3)`. Thus among positive q the CZ fixed-context shell is cyclotomic exactly at q=3: `7=2*3+1=Phi_6(3)`. The corpus already contains the bare arithmetic identity; the new content here is its occurrence as the fixed-context complement of the CZ/Hashimoto weld.

## Verification

`analysis/w33_cz_hashimoto_orbit_weld.py` enumerates the local projective symplectic turn shell and the CZ orbit labels for `q=3,5,7,11` and checks the context count, degree, moving-orbit count, `(q-1,q^2)` branch match, explicit bijection completeness, cycle accounting, and cyclotomic factorization. The frozen summary is `data/w33_cz_hashimoto_orbit_weld.json`; focused regression is `tests/test_w33_cz_hashimoto_orbit_weld.py`.

## Evidence boundary

The map depends on a selected Darboux frame, the displayed CZ shear, and a directed base edge. No claim is made that it is a natural `PSp(4,q)`-equivariant global intertwiner. No physical one-photon realization is claimed outside `q=3`. The external generalized-quadrangle literature supplies the standard collinearity parameters; the new content here is the explicit welding of the repository's independently certified CZ orbit quotient to its Hashimoto turn alphabet.
