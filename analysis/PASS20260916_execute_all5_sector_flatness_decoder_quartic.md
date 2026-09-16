# 2026-09-16 — execute-all-five: sector return, dual covers, flat directions, decoder, nonlinear adjoint

Status: **five fronts executed with exact finite certificates and explicit claim boundaries**.

## 1. A8^3 sector return: the simple-current route is topologically trivial

The A8^3 Niemeier glue code `C <= (Z9)^3` has order 27 and conformal-weight census

- `h=0`: 1 sector;
- `h=2`: 18 sectors;
- `h=3`: 8 sectors.

Thus `q(c)=h_c mod 1` vanishes on every glue word.  Consequently the monodromy bicharacter

`b(c,d)=q(c+d)-q(c)-q(d)`

vanishes identically.  The 26 nonzero simple currents form 13 inverse pairs `c,-c`, and every `V_c V_-c -> V_0` return is bosonic/local at the simple-current level.  The Z9 label therefore does not hide a ninth-root braiding gate.

The 729-dimensional order-three twisted ground register is an irreducible `3^(1+12)` Heisenberg module.  Any return endomorphism which commutes with that full Heisenberg action is scalar by Schur/finite Stone-von Neumann.  The remaining loophole is precise: a noncentral descendant/OPE return operator that does not reduce to the abelian simple-current monodromy data.

Artifacts:
- `analysis/w33_a8cubed_sector_return_monodromy.py`
- `data/w33_a8cubed_sector_return_monodromy.json`

## 2. The Steiner twin is point/line duality, not a new four-dimensional difference module

The Suzuki/U5(2) 120-cover and the classical 120 Steiner trihedral-pair cover have the same four pair-orbit sizes and the same 40-by-3 imprimitive shape, but their degree-40 quotients are the two dual generalized-quadrangle actions:

- Suzuki twin -> standard W33 **points**;
- classical Steiner -> W33 **lines**, i.e. Q(4,3) points.

Both rational permutation modules decompose as `1+24+15`.  Literal W33 point-line incidence `Z` satisfies

`ZZ^T=4I+A_point`, `Z^TZ=4I+A_line`

and has rank 25.  It transmits the common `1+24` and annihilates the two distinct 15-dimensional `-4` dark spaces.  Therefore the characteristic-zero difference carrier is the **pair of dual dark 15-spaces**.  The modular ranks `rank_F3(A_point+I)=11` and `rank_F3(A_line+I)=15` are a characteristic-three extension separator, not evidence for a new 4D rational module.

Artifacts:
- `analysis/w33_steiner_twin_point_line_dark_module.py`
- `data/w33_steiner_twin_point_line_dark_module.json`

## 3. Frozen SU(5) singlet vacuum: 16 quartic neutral directions protected through order eleven

A fresh reconstruction of the Holotrade frozen SU(5) witness gives 46 selected-SU(5) singlet momentum types:

- 24 untwisted;
- 22 twisted, distributed `4+9+9` over Wilson fixed-point label `n1=0,1,2`.

Exact full 16-dimensional lattice-momentum enumeration gives 36 neutral cubics (`20 UUU + 16 TTT`) and exactly **16 primitive neutral quartics**, every one of type

`U * T0 * T1 * T2`.

For each quartic support:

- no neutral cubic contains two support fields;
- no gauge-neutral dangerous term exists at orders 5,6,7;
- at order 8 the only dangerous monomial is the square of the quartic, but `2U+6T` fails the Z3 R rule;
- orders 9,10,11 are again empty;
- at order 12 the cube is the first gauge+R-admissible self-lift (`3U+9T`), with the three U copies assigned one to each untwisted plane.

Therefore the 16 lattice-neutral directions are protected against **gauge+R** F-terms through order 11.  They are standard zero-FI holomorphic D-flat candidates; the anomalous-U(1) Fayet-Iliopoulos shift is not available in the current witness data and is not silently set to zero.  Degree-12 space-group/Rule-4/Rule-5 and actual CFT coefficients remain open.

Holotrade artifacts:
- `analysis/w33_su5_singlet_flat_directions.py`
- `data/w33_su5_singlet_flat_directions.json`

## 4. The 165 complex Pauli shadow has an exact association-algebra decoder

For the reduced rank-78 Pauli projection frame,

`G = I + A/13`,

where `A` is `SRG(165,36,3,9)`.  Exact inversion in the Bose-Mesner algebra gives

`G^-1 = (91/64)I - (13/64)A + (117/3136)J`.

Thus each canonical dual encoding is a rational combination of itself, its 36 GQ neighbors and the global mean.  The Gram spectral gains are

- constant: `49/13`;
- 120-dimensional `+3` sector: `16/13`;
- 44-dimensional `-9` sector: `4/13`.

This turns `165=(1+44)+120=45+120` into exact collective readout/noise sectors.  Every principal subframe remains positive definite by interlacing, with condition number at most `49/4`.  Since the full 165 Gram matrix is nonsingular, however, deleting a frame vector removes one dimension of the complete coefficient span; this is robust conditioning, not exact erasure correction of the full 165-coordinate signal.

Artifacts:
- `analysis/w33_suzuki_165_fusion_frame_decoder.py`
- `data/w33_suzuki_165_fusion_frame_decoder.json`

## 5. Nonlinear cubic-H1 search: no cubic invariant; determinant is the first genuine new pointwise invariant

The ten tritangent homology channels are already certified as the adjoint `sp4(F3)`.  Solving polynomial invariance equations on that exact 10D module gives homogeneous invariant dimensions

`degree 1,2,3,4 = 0,1,0,3`.

So there is no invariant cubic.  The quadratic is `q2(X)=tr(X^2)`.  A formal degree-four basis can be taken as

`q2^2`, `det(X)`, and the Frobenius lift `qF=B(X^[3],X)`.

On F3-rational points `qF=2q2`, leaving `det(X)` as the first genuinely new nonlinear point-function.  Exhaustion of all `3^10=59049` adjoint elements shows all nine pairs `(q2,det) in F3^2` occur; determinant is independent of the quadratic controller.

Thus a phase `omega^(r det X)` for synchronized A8^3 central character `r=1,2` is an exact **candidate** nonquadratic invariant.  It is not yet a six-qutrit gate because no certified intertwiner maps the H1 controller coordinate `X` into a basis-dependent phase on the 729-dimensional ground register.  The linear and cubic routes are closed; the next magic search is quartic and coupling-dependent.

Artifacts:
- `analysis/w33_h1_adjoint_nonlinear_invariants.py`
- `data/w33_h1_adjoint_nonlinear_invariants.json`

## Combined boundary

This pass materially narrows the universal-computation problem.  Simple-current braiding/return is trivial, the linear H1 controller is symplectic, and no cubic adjoint invariant exists.  The first certified nonlinear scalar beyond the quadratic symplectic layer is the quartic adjoint determinant.  A universal gate still requires an explicit sector-return/OPE or state-injection mechanism that makes such a nonlinear invariant act on the six-qutrit computational register.
