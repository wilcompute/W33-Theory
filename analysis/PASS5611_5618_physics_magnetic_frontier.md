# Passes 5611–5618 — physics-first magnetic frontier

## Scope and repo archaeology

This packet executes the five carry-forward targets from Pass5603–5610 and three additional physics probes.  It deliberately reuses rather than duplicates the older repository layers:

- `scripts/grade_weil_phase.py` for section-dependent versus invariant Heisenberg cocycles and Weil corrections;
- `tools/toe_affine_plane_z3_connection.py`, `tools/toe_affine_plane_z3_holonomy.py`, and `tools/toe_heisenberg_connection_model.py` for the E6/firewall-derived `AG(2,3)` connection and its exact Heisenberg curvature;
- `analysis/BT4065_BT4072_explicit_qsp_dirac_magic_gauge.md` for the causal Clifford Dirac walk;
- `tools/toe_z3_lift_constraint.py` and `tools/toe_yukawa_affine_textures.py` for the 27-vertex E6 cubic/lift/Yukawa layer;
- the Pass5416–5418 / Pass5468 exact 13-cover stabilizer GAP constructions; and
- the Pass5596/5606 Latin–Reye–F4 action-level gates.

The main physics conclusion is a separation of roles.  The symplectic/Heisenberg phase is a real source of finite spectral complexity and gauge curvature, but maximal finite symmetry still produces an atomic large-q spectrum.  The phase is also not intrinsic on projective points: it naturally lives on the vector/frame lift above them.

## Pass5611 — exact all-q affine magnetic spectrum

On the affine event bulk `V=F_q^2`, define

\[
A_q((x,y),(u,v))={\bf 1}_{x\ne u,\,y\ne v}\,\chi(xv-uy),
\]

where `chi` is a nontrivial additive character.  For the normalized Segre section this is obtained from the previous section phase by the diagonal gauge `f(x,y)=xy`.

Write `K` for the full symplectic Fourier kernel and `R,C` for the same-first-coordinate and same-second-coordinate kernels. Then

\[
A=K-R-C+I,
\]

with

\[
K^2=q^2I,\quad R^2=qR,\quad C^2=qC,
\]
\[
KR=RK=qR,\quad KC=CK=qC,\quad RCR=qR,\quad CRC=qC.
\]

This closes the spectrum exactly:

\[
\boxed{-(q-1)^{\,q(q-1)/2}},\qquad
\boxed{(q+1)^{\,q(q-3)/2}},
\]
\[
\boxed{(1-\sqrt q)^{\,q}},\qquad
\boxed{(1+\sqrt q)^{\,q}}.
\]

Direct numerical matrix replays at `q=3,5,7,11` reproduce the formula.  After scaling eigenvalues by `q`, the two `1+-sqrt(q)` bands have total empirical mass `2/q`, while the two macroscopic bands approach equal masses. Therefore

\[
\boxed{\mu_{A_q/q}\Longrightarrow\tfrac12\delta_{-1}+\tfrac12\delta_{+1}.}
\]

So the Heisenberg phase strongly splits finite spectra but still does **not** yield a Weyl-law continuum in the maximally regular all-q bulk.

The normalized projective `P1 x P1` section differs from the affine block by only `2q+1` boundary points, hence by a rank at most `2(2q+1)` perturbation after zero-padding.  Its empirical spectral distribution has the same limit.  Pass5613 below is essential: this projective section is a gauge choice, not an intrinsic projective observable.

## Pass5612 — minimum histories are semilinear projectivities

Pass5604 gave the exact code parameters

\[
[(q+1)^2,(q+1)^2/2,q+1]_2.
\]

Let `S` be a minimum support of size `q+1` in the `C_+` code.  Every opposite-determinant projectivity meets `S` evenly.  There are

\[
a=\frac{q(q-1)}2
\]

opposite projectivities through one cell and

\[
b=\frac{q-1}{2}
\]

through two compatible cells.  If `m_h` is the intersection size with an opposite projectivity, then

\[
\sum_hm_h=(q+1)a,
\qquad
\sum_h{m_h\choose2}=bP,
\]

where `P` counts compatible pairs in `S`.  Since `m_h` is even,

\[
{m_h\choose2}\ge m_h/2.
\]

The resulting lower bound on `P` is exactly `C(q+1,2)`, the absolute maximum.  Equality forces every pair in `S` to be compatible and every `m_h` to be `0` or `2`.  Thus every minimum support is exactly one cell in each row and column: the graph of a permutation of `P1(q)`.

No opposite-determinant projectivity may agree with that permutation on three points. Equivalently, the permutation preserves the two PSL orbits (the determinant-square colouring) on ordered triples.  The standard projective switching/line automorphism group is `P-Sigma-L_2(q)`: PSL extended by field automorphisms.  Iverson–Mixon's projective-line switching analysis independently identifies `P-Sigma-L_2(q)` as the relevant colour-preserving semilinear symmetry in the PSL line construction (Algebraic Combinatorics 7 (2024), 37–76; arXiv:1905.06859).

The executable checks are important because they expose an extension-field correction:

- `q=3`: all `4!` permutations checked; exactly `12=|PSL_2(3)|` qualify;
- `q=5`: all `6!` checked; exactly `60=|PSL_2(5)|` qualify;
- `q=7`: all `8!` checked; exactly `168=|PSL_2(7)|` qualify;
- `q=9`: Frobenius `x -> x^3` is not a PGL projectivity but satisfies every opposite-coset parity check.  Together with PSL it constructs a 720-element `P-Sigma-L_2(9)` minimum-word family.

Thus the earlier tempting statement “minimum words are exactly PSL rows” is false over extension fields.  The natural minimum histories are semilinear.

## Pass5613 — correction: phase lives on the vector/frame lift

Pass5609's 16-event spectrum is exact for its chosen normalized representatives, but the phase `omega^B(s,t)` is not projectively intrinsic.  Flip the sign of one representative.  The second and third trace moments remain the same, but

\[
\operatorname{tr}A^4:2256\longrightarrow2400,
\]

and higher moments change as well.  This is not a harmless diagonal gauge.

There is a structural reason.  At `q=3`, the central element `-I` of `Sp(4,3)` fixes every projective point but swaps the two nonzero vector lifts `v <-> -v`.  Hence there is no `Sp(4,3)`-equivariant section from projective points to nonzero vectors.

The intrinsic q=3 object is therefore the two-sheeted vector lift.  Lift the 16 Segre projective events to all 32 vectors `+-v`, and use the alternating Heisenberg cocycle

\[
\psi(v,w)=\frac12B(v,w)=2B(v,w)\pmod3.
\]

The resulting 32-dimensional Hermitian magnetic operator has the remarkably clean spectrum

\[
\boxed{-6^6\oplus(-3)^7\oplus(-1)^3\oplus2^6\oplus3^5\oplus6^4\oplus9^1}.
\]

The first eight trace moments are

`0, 576, 288, 20592, 43200, 1007136, 4219488, 59923152`.

This matches the older repo's conceptual separation in `grade_weil_phase.py`: a raw Heisenberg section cocycle is section-dependent, whereas the alternating cocycle class and its Weil correction are the invariant data.  Gurevich–Hadani's finite-field quantization/Weil-representation framework is the appropriate external mathematical setting (J. Symplectic Geom. 7 (2009), arXiv:0705.4556).

A second q-family consequence is exact:

\[
|F_q^*|=q-1
\]

nonzero vector lifts lie above each projective point.  This is literally a **two-sheeted** sign cover iff `q-1=2`, i.e. iff `q=3` among odd q.  That creates a mathematically honest spin/frame-like q=3 selector; it does not yet derive physical spin statistics.

## Pass5614 — q=3 physical selector stack

Three logically separated mechanisms select q=3:

1. **Exact Bose–Mesner degeneration:**
   \[
   k_2=\frac{q(q+1)(q-3)}4,
   \qquad
   m_1=\frac{(q-3)(q+1)^2}{4}.
   \]
   At q=3 a relation and a primitive idempotent simultaneously disappear.

2. **Exact spin-like lift condition:** the projective-to-vector fiber has size `q-1`; it is a double cover only at q=3.

3. **Repo phenomenological dictionary, kept explicitly model-dependent:** using the existing all-q formulas,
   \[
   \sin^2\theta_{23}-\sin^2\theta_W-\sin^2\theta_{12}
   =\frac{q(q-3)}{q^2+q+1}.
   \]
   Hence the repo mixing sum rule also closes at q=3.  This is supporting model evidence, not an independent experimental derivation.

The older `GRAVITY_BREAKTHROUGH.py` exactly computes `kappa=1/6` on all 240 q=3 W33 edges, but its displayed all-q curvature extrapolation is not proved there.  This packet therefore does not use that extrapolation as a theorem.

## Pass5615 — exact cover/F4 object map remains fail-closed

The repo was searched back through the Pass5416–5418 and Pass5468 GAP sources.  The exact selected cover is

`[7,31,74,112,129,141,158,190,194,227,255,278,321]`.

Its setwise stabilizer has order 1152, the image on the 13 vertices has order 576, the pointwise kernel has order 2, and the image has orbit structure `1+12`.  Pass5606 now asks GAP for an explicit `S12` conjugator from that moving 12-orbit to the independent Klein-V4 Latin action.  `w33_pass5615_cover_f4_object_dictionary_gate.py` consumes that exact witness and composes it with the already frozen F4-short-root-pair-to-Latin conjugator.

The GitHub Actions GAP run is still queued as this packet is written.  Therefore no object dictionary is asserted yet; the consumer intentionally emits `FAIL_CLOSED_PENDING_DIRECT_GAP_OBJECT_MAP` until the direct witness exists.

## Pass5616 — exact relativistic-form dispersion with magnetic internal bands

Reuse the Pass4067 Clifford matrices `alpha_j,beta` and the intrinsic q=3 magnetic operator `H_mag`.  Define

\[
H(p)=\sum_{j=1}^3p_j\alpha_j\otimes I+
\beta\otimes M,
\qquad
M=m_0I+gH_{\rm mag}.
\]

Clifford anticommutation gives an exact identity, not a low-momentum fit:

\[
\boxed{H(p)^2=|p|^2I+I\otimes M^2.}
\]

Therefore every magnetic internal eigenvalue `h` carries the dispersion

\[
\boxed{E_{h,\pm}(p)=\pm\sqrt{|p|^2+(m_0+gh)^2}}.
\]

For q=3, `h` runs over `-6,-3,-1,2,3,6,9` with multiplicities `6,7,3,6,5,4,1`.  A 128-dimensional numerical Kronecker replay verifies the squared-Hamiltonian identity to machine precision and matches the full predicted spectrum.

This dovetails with the established quantum-walk literature: causal local walks can converge to the Dirac equation, and discrete gauge fields can be coupled with exact lattice gauge invariance (Arrighi–Forets–Nesme, arXiv:1307.3524; Arnault–Debbasch, arXiv:1508.00038).  Here the new result is the exact insertion of the repo-derived magnetic internal operator.  `m0`, `g`, physical `c`, and particle assignments remain undetermined.

## Pass5617 — E6/firewall curvature becomes a qutrit Harper sector

The older repo already derives an `AG(2,3)` Z3 connection from the E6 27-vertex cubic/firewall structure and verifies

\[
F(d_1,d_2)=-\det(d_1,d_2)\pmod3.
\]

For the four affine direction classes there are six unordered independent direction pairs at each of nine points. All 54 point/direction-class plaquettes have nonzero curvature: 27 carry flux 1 and 27 flux 2.

With the declared Wilson convention

\[
S_W=\sum_p(1-\operatorname{Re}\omega^{F_p}),
\]

this finite sector gives `S_W=81`.  The number is normalization-dependent and is not promoted as a physical constant.

More important is the operator consequence. Constant Z3 curvature forces magnetic translations to obey the qutrit Heisenberg relation

\[
ZX=\omega XZ.
\]

The minimal Harper operator

\[
H_H=X+X^\dagger+Z+Z^\dagger
\]

has exact spectrum

\[
\boxed{-2,\quad1-\sqrt3,\quad1+\sqrt3}.
\]

This supplies a direct `E6 cubic -> finite gauge curvature -> magnetic translation -> band structure` chain.  Finite-lattice magnetic-translation/Harper reduction is standard; see Sekiguchi–Okamoto–Fujiwara, arXiv:0812.1426.  No continuum Yang–Mills coupling is claimed.

## Pass5618 — a useful matter-selection falsifier

The same E6/firewall construction organizes the 36 allowed cubic triads as three Z3 lifts of each of 12 affine lines.  In shifted lift coordinates every allowed triad has

\[
(t_0,t_1,t_2)=(k,k+\lambda,k+2\lambda),
\]

so

\[
t_0+t_1+t_2=0\pmod3.
\]

However every forbidden bad9 fiber is `(0,1,2)` and also has total charge zero.  Therefore

\[
\boxed{\text{all 45 E6 cubic triads are Z3-neutral}.}
\]

This kills a tempting but incorrect physical explanation: **simple Z3 charge conservation cannot be the 36/9 Yukawa firewall selector.**  The distinction must be encoded in richer data already present in the repo: affine incidence, Wilson/triangle holonomy, the L-infinity `l3` support on bad9, CE2/metaplectic phase, or chirality on the q=3 vector double cover.

## External boundary

The external literature was used as prior-art/context, not as evidence for W33 physics:

- Gurevich & Hadani, *Quantization of symplectic vector spaces over finite fields*, arXiv:0705.4556 — canonical finite Heisenberg/Weil framework.
- Iverson & Mixon, *Doubly transitive lines II: Almost simple symmetries*, arXiv:1905.06859 / Algebraic Combinatorics 7 (2024) — PSL projective-line switching symmetries and `P-Sigma-L_2(q)`.
- Arrighi, Forets & Nesme, *The Dirac equation as a quantum walk: higher dimensions, observational convergence*, arXiv:1307.3524 — causal local Dirac quantum walks and continuum convergence.
- Arnault & Debbasch, *Quantum Walks and discrete Gauge Theories*, arXiv:1508.00038 — discrete local U(1) gauge invariance and Dirac/gauge continuum limits.
- Sekiguchi, Okamoto & Fujiwara, *Magnetic translation symmetry on the lattice*, arXiv:0812.1426 — finite-lattice magnetic translation and Harper reduction.

## Overall physics verdict

The packet makes the architecture more constrained:

- projective geometry supplies finite events/histories;
- the vector/Heisenberg lift supplies the natural phase/frame variable;
- E6/firewall geometry supplies a concrete Z3 connection and curvature;
- the phase can generate nontrivial finite spectra and exact relativistic-form internal Dirac bands;
- maximal all-q regularity still produces an atomic large-q spectral measure;
- and simple Z3 neutrality is too weak to select matter couplings.

So the next missing object is not another famous finite group.  It is a **controlled hierarchy/refinement or defect dynamics** that turns the exact finite symplectic gauge data into a genuine continuum-scale dispersion while preserving the q=3 lift and algebraic selectors.
