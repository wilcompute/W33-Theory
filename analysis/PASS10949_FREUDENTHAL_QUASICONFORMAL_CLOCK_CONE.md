# Pass 10949 — Freudenthal quartic, the quasiconformal 57-cone, and the clock real form

Producer: `analysis/w33_pass10949_freudenthal_quasiconformal_clock_cone.py`
Certificate: `data/w33_pass10949_freudenthal_quasiconformal_clock_cone.json`
Regression: `tests/test_w33_pass10949_freudenthal_quasiconformal_clock_cone.py` (8 tests, ~6 s)

Everything below is computed on the committed executable Chevalley bracket
`artifacts/e8_structure_constants_w33_discrete.json`. The Hesse clock pair is the
one frozen on 2026-09-25: the striation's |3|-grading is the `alpha_7` coefficient
`a7`, and the contact grading of its positive tick line is the `alpha_8`
coefficient `a8` (the highest root `theta = omega_8` is that line's root).

This pass executes the "Freudenthal bridge", "real-form bridge" and "57th
coordinate" items of the Albert–Freudenthal–E8 temporal proposal, and corrects
two of its count-level claims.

## 1. The Freudenthal 56 does not extend the clock 54

Bigrading the 240 roots by `(a8, a7)` puts the contact layer `a8 = -1` (the 56) at
clock degrees `0, -1, -2, -3` with sizes `1, 27, 27, 1`. The clock layer `a7 = -1`
(the 54 = 27 x 2) sits at contact degrees `0, -1` with 27 each.

**The two share exactly one 27.** The proposal's `54 + 2 = 56` is refuted
objectwise: the second 27 of the Freudenthal system is the clock's
*second-order* layer, and its two scalar poles are

- `alpha = e_{-alpha_8}`: clock degree 0, the lowering vector of the `A1` in the
  |3| Levi `E6 + A1`;
- `beta = e_{-(theta - alpha_8)}`: clock degree `-3`, a member of the
  two-dimensional clock doublet.

## 2. Heisenberg form

`[x_i, x_j] = Omega_ij e_{-theta}` on the 56 is a signed perfect matching
(`det = +-1`, unimodular over `Z`): `alpha <-> beta` and `X_k <-> Y_k` where `X`
and `Y` carry the **same canonical `i27` history label**. `g_{-3} = 0`, so
`e_{-theta}` is central and `g_{-1} + g_{-2}` is the 57-dimensional Heisenberg
algebra.

## 3. The E7 quartic and its Freudenthal normal form

`Q(x) = (1/6) coeff_{e_-theta} ad_x^4 e_theta` has content-6 integrality, **1036
monomials** with primitive coefficients `{1: 28, +-2: 378, +-4: 630}`, and is
**exactly E7-invariant** (all 126 Levi root generators, symbolic check). Its
monomials fall into exactly the five Freudenthal types and satisfy the exact
polynomial identity

```text
Q(alpha, X, Y, beta) = (alpha*beta + T(X,Y))^2 - 4*beta*N(X) - 4*alpha*N(Y) + 4*T(X#, Y#)
```

where `N` is the repository's signed 45-triad E6 cubic from
`canonical_su3_gauge_and_cubic.json`, `X#_k = dN/dX_k`, and
`T(X,Y) = sum_k t_k X_k Y_k` with `t_k = Omega(X_k,Y_k) Omega(alpha,beta)`.
**No sign repair is needed.** So the tick line's 56 is the Freudenthal triple
system of the split Albert algebra whose norm is the committed cubic, and the cubic
history volume enters the quartic *only* multiplied by the clock pole `beta`.

## 4. Albert identities and Jordan frames

The committed cubic satisfies `(X#)# = N(X) X` and `X . X# = 3 N(X)` as exact
polynomial identities: it is the norm of a cubic (split Albert) Jordan algebra over
`Q`. Each index lies in 5 triads and each pair in at most one. In each of four
27-layers, **the 45 triads are exactly the 45 strongly orthogonal root triples** —
the coordinate Jordan frames. (This corrects PART_CCLXXXV's "27 minimal
idempotents": 27 is the number of coordinate rank-one directions; frames are the
45 triads.) For every coordinate idempotent the split Peirce decomposition is
`1 + 16 + 10`, and the Peirce-0 quadratic form is five hyperbolic planes, inertia
`(5,5)`.

## 5. The quasiconformal 57-dimensional light cone

For `p = (X, tau)` put `v_p = exp(ad(X + tau e_-theta)) e_theta`.

- Symbolically, `coeff_{e_-theta}(v_p) = N(X, tau) = Q(X)/4 - tau^2`.
- The Heisenberg law `(X1,t1)(X2,t2) = (X1+X2, t1+t2+Omega(X1,X2)/2)` holds.
- The distance `D(p,p') = N(X-X', tau-tau'-Omega(X',X)/2) = B(v_p,v_p')/B(e_-theta,e_theta)`.
- The Weyl element `w = exp(ad e) exp(-ad f) exp(ad e)` swaps `e_theta` and
  `-e_-theta`; every inverted point stays in the big cell, with
  `w v_p = -N(p) v_{i(p)}`, and
  `D(i(p), i(p')) = D(p,p') / (N(p) N(p'))` on all 15 checked pairs.

This is the Günaydin–Koepsell–Nicolai quasiconformal realization of E8
(hep-th/0008063), now objectwise on the committed basis. The central coordinate
enters the cone only through the accumulated symplectic area
`tau - tau' + Omega/2` — the precise sense in which the 57th coordinate
"accumulates action".

## 6. Real forms: the clock is E8(-24), the committed split form is the height twist

`K(e_a, e_-a) = -60 (-1)^{ht a}`. The compact conjugation is
`sigma_c(e_a) = (-1)^{ht a} conj(e_-a)` (automorphism on all 30,628 basis pairs), and
the repository's certified split involution `Theta` equals `sigma_c` composed with
the **height parity** `(-1)^{ht} = exp(i pi rho^vee)`.

| twist | E8 | contact-Levi E7 | E6 |
| --- | --- | --- | --- |
| tick line `L+`: `(-1)^a8` | E8(-24) | compact | compact |
| tick line `L0`: `(-1)^a7` | E8(-24) | **E7(-25)** | compact |
| tick line `L-`: `(-1)^(a7+a8)` | E8(-24) | E7(-25) | compact |
| height `(-1)^ht` (committed split) | E8(8) | **E7(7)** | E6(2) |
| height·L+, height·L0 | E8(8) | E7(7), E7(-5) | E6(2) |
| height·L- | E8(-24) | E7(-5) | E6(2) |

The three tick-line roots `theta, -(theta - alpha_8), -alpha_8` sum to zero,
have pairwise product `-1` and are orthogonal to the E6: they are the external
`A2`. Their parities are three commuting E8(-24) involutions forming a Klein
four-group with **E8 = 80 + 56 + 56 + 56** — common fixed algebra `e6 + t2`, one
Freudenthal 56 per tick line.

## 7. Where the Lorentzian slice actually lives

On the contact Levi, `p+ = {a8 = 0, a7 = +1}` (27 roots) carries the Hermitian Jordan
triple `{x,y,z} = -[[x, sigma_c y], z]` of E7(-25). Under this conjugation all 27
root vectors are tripotents (`{e,e,e} = 2e`); under the committed split
conjugation only 12 of 27 are. Taking the tripotent `e` of a canonical triad
frame, `A = {x : {e,x,e}/2 = x}` with `x o y = {x,e,y}/2` is a 27-dimensional
commutative Jordan algebra with **positive-definite trace form (27,0,0)** — a
Euclidean Jordan algebra of rank 3, i.e. the Albert algebra `H3(O)`. For a
primitive idempotent of the frame the Peirce spaces are `1 + 16 + 10`, and the
rank-two determinant on the Peirce-0 space has **inertia (1, 9)**.

So the proposal's "selecting a primitive idempotent reduces the exceptional cubic
geometry to 9+1 Minkowski" is **true in the clock real form and false in the
committed split form** (where it is `(5,5)`). Over `F_3` the two are
indistinguishable — both quadrics are `O+(10,3)` — so signature is a real-form
datum, not a finite-field one.

## Scope and prior art

Classical inputs are cited, not claimed: Freudenthal (1954); Krutelevich,
J. Algebra 314 (2007); Günaydin–Koepsell–Nicolai, CMP 221 (2001); Faraut–Korányi,
*Analysis on Symmetric Cones*; Baez, *The Octonions* (2002). Repository prior art:
`analysis/w33_magic_square_substrate.py` states `56 = 2*27 + 2` as a dimension
identity; `PART_CCLXXXV_ALBERT_JORDAN_BRIDGE.md` gives Albert-algebra counts;
`w33_e8_split_real_form_involution.py` certified E8(8) on this basis (identified
here as the height twist); `w33_20260925_e8_parabolic_cubic_clock_lift.py` froze
the 45-triad cubic as the |3|-bracket law.

Rediscovery-guard audit (`scripts/check_rediscovery.py`, run before commit): the
flagged compounds `e7+hesse`, `e7+levi`, `hesse+levi`, `e_6/e_8+levi` point to
`analysis/BT1720_BT1723_repo_mining_execution.md` (magic-square Latin heptad and
Coxeter-number counts), `analysis/BT1745_BT1748_execution_summary.md` (exceptional
tower list), `analysis/PASS7376_7384_deep_followup.md` (a BT660 Levi carrier and
E8/E7 local spectra), `PASS1087_1091_FIVE_STREAM_RELEASE.md` (dual-Hesse
hyperplanes) and the parent `analysis/w33_20260925_hesse_clock_e8_gradings.py`;
`alpha@60` points to the split-real-form certificate cited above. Each was read:
none constructs the quartic, the Heisenberg cone or the real-form restriction.

What is new is objectwise: the tick-line identification of the Freudenthal
system with no sign repair, the refutation of `54 + 2 = 56`, the Klein four-group
of tick lines, and the real-form control showing that the Lorentzian Peirce slice
is selected by the clock involution. None of this is dynamics: no Hamiltonian,
spacetime, energy scale or CPTP arrow is derived.
