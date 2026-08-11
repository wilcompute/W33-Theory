# Pass 4937 — the missing ten becomes an exact finite controller

## Result

Pass 4864 identified the ten-dimensional ternary quotient outside the
oriented \(K_{3,3}\) span as the simple adjoint Lie algebra

\[
Q_{10}\cong \mathfrak{sp}_4(\mathbb F_3).
\]

Pass 4861 independently proved that a full three-port matching removes the
local \(S_3^{45}\) sheet gauge and leaves one global
\(PGSp(4,3)\) of order \(51{,}840\). Pass 4937 composes those two exact
objects. It produces a literal ten-trit correction register and its affine
frame group:

\[
\boxed{\mathbb F_3^{10}\rtimes PGSp(4,3)},
\qquad
|\mathbb F_3^{10}\rtimes PGSp(4,3)|
=3^{10}\cdot 51{,}840=3{,}061{,}100{,}160.
\]

The update law is simply

\[
v\longmapsto vA_g+w,
\qquad v,w\in\mathbb F_3^{10},\quad g\in PGSp(4,3).
\]

This is an exact finite controller candidate. No HoloBox instruction currently
executes that update.

## Why dual numbers appear

Let

\[
R=\mathbb F_3[\epsilon]/(\epsilon^2)
\]

and let \(J\) be the alternating form preserved by \(Sp_4(3)\). A matrix
\(I+\epsilon X\) preserves \(J\) precisely when

\[
X^{\mathsf T}J+JX=0.
\]

GAP solves these sixteen linear equations and obtains nullity ten. The
solutions are exactly \(\mathfrak{sp}_4(\mathbb F_3)\). Because
\(\epsilon^2=0\),

\[
(I+\epsilon X)(I+\epsilon Y)=I+\epsilon(X+Y).
\]

Thus the reduction map has the split exact sequence

\[
1\longrightarrow \mathfrak{sp}_4(\mathbb F_3)^+
\longrightarrow Sp_4(R)
\longrightarrow Sp_4(3)
\longrightarrow 1,
\]

and its kernel has \(3^{10}=59{,}049\) elements. This is the precise sense in
which the Pass-4864 residual is a first-order symplectic correction space.

The kernel is elementary abelian. Its group commutator is therefore zero. The
nonabelian Lie bracket from Pass 4864 is tangent data obtained from matrix
commutators before imposing \(\epsilon^2=0\); it must not be confused with the
commutator inside the square-zero kernel.

## Two equal orders do not identify two groups

There are now two natural extensions of order \(3{,}061{,}100{,}160\):

\[
Sp_4(\mathbb F_3[\epsilon]/\epsilon^2)
\quad\text{and}\quad
\mathfrak{sp}_4(\mathbb F_3)^+\rtimes PGSp(4,3).
\]

They are not the same group. The adjoint action of \(Sp_4(3)\) kills its
scalar center, so the dual-number symplectic extension retains a central
\(C_2\). The \(PGSp\) action is faithful and centerless, has no nonzero fixed
vector on the ten-space, and its commutant has dimension one. The affine
extension consequently has trivial center. GAP freezes the separating
invariant:

\[
|Z(Sp_4(R))|=2,
\qquad
|Z(\mathbb F_3^{10}\rtimes PGSp(4,3))|=1.
\]

This firewall matters because the identical orders make a silent
identification tempting.

## The 59,049 offsets have only 17 exact state classes

The faithful \(PGSp(4,3)\) action partitions the complete ten-trit register
into exactly seventeen orbits. Their sizes are

\[
\boxed{
1,80,240,480,540,540,1080,1080,4320,4320,
5184,5184,5760,6480,6480,8640,8640.}
\]

They sum to \(59{,}049\). The singleton is zero, so there is no nonzero fixed
offset. This is a usable compiler taxonomy: a controller can classify any
ten-trit correction state by one of seventeen symmetry classes before choosing
a representative. The certificate does not yet provide the optimal canonical
representative algorithm or an opcode lowering.

## Exact systems interpretation

Pass 4861's port matching is the required interface boundary. Before the
matching, \(S_3^{45}\) can relabel local sheets independently, so a global
ten-trit correction coordinate has no fixed physical port meaning. After the
matching, the remaining global symmetry is exactly \(PGSp(4,3)\), which is the
group acting on the Pass-4864 adjoint quotient. The affine controller is
therefore the smallest direct composition of the two certified objects:

- \(w\in\mathbb F_3^{10}\) is a first-order correction or control offset;
- \(g\in PGSp(4,3)\) is the globally consistent frame;
- \(v\mapsto vA_g+w\) is the exact finite update.

This supplies a design target for a HoloBox control plane, not a completed
integration. The current runtime has chamber transitions, mailbox state,
content-addressed receipts, and recursive path-copy persistence; it has no
ten-trit adjoint register, no \(PGSp\) frame opcode, and no compiler map from a
receipt or panel trace into \(w\).

## Ownership and boundary

- Pass 4864 owns the explicit \(Q_{10}\cong\mathfrak{sp}_4(\mathbb F_3)\)
  intertwiner and Lie bracket.
- Pass 4861 owns the minimal port matching and residual global \(PGSp(4,3)\).
- The tangent-space description of classical groups over dual numbers is
  standard mathematics. The repository-specific advance is its explicit
  composition with the certified W33 quotient, port-matching boundary, group
  separation, and complete seventeen-orbit offset atlas.

The result is finite and characteristic three. It does not construct an
individual HoloBox selector, guest-state transition, compiler lowering,
hardware timing result, isolation boundary, continuum gauge field, particle,
mass, or coupling.

## Reproduce

```console
gap -q -b analysis/w33_pass4937_adjoint_dual_number_controller.g
python3 -m pytest -q tests/test_w33_pass4937_adjoint_dual_number_controller.py
```

Expected GAP line:

```text
Pass 4937 adjoint dual-number controller: 30/30 checks; status=PASS
```

The test rebuilds the JSON in an isolated temporary directory and requires
byte identity with
`data/PART_W33_PASS4937_ADJOINT_DUAL_NUMBER_CONTROLLER.json`.
