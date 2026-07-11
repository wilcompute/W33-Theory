# Pass 176 — The Incidence Fixed-Line Bridge to the E8 Shadow

## Result

Let (M) be the (40)-line by (40)-point incidence matrix of
(W(3,3)), and put

\[
C=\ker_{\mathbb F_2}M=[40,15,8],
\qquad
R=\ker_{\mathbb F_2}M^{\mathsf T}=[40,15,10].
\]

Pass 164 constructed the address-side quadratic shadow

\[
H_{10}=C^\perp/C\cong \mathbb F_2^{10},
\qquad q_A([x])=\frac{\operatorname{wt}(x)}2\pmod2,
\]

and Pass 174 constructed the route hull

\[
K=R\cap R^\perp=[40,9,16],
\qquad
q_R(z)=\frac{\operatorname{wt}(z)}4\pmod2.
\]

The missing map between them is the original incidence operator.  The native
(\PSp(4,3)) action on (H_{10}) has a unique nonzero fixed vector (f),
which is isotropic.  Incidence induces the exact equivariant quadratic
isometry

\[
\boxed{
 f^\perp/\langle f\rangle
 \;\xrightarrow{\;M\;}\;
 K/\langle\mathbf1\rangle .
}
\]

Both sides are the plus-type (8)-space (E_8/2E_8).  This supplies the
chosen objectwise identification that Pass 174 deliberately left open.

## Why incidence descends

The context code is (C^\perp=\operatorname{row}M).  Since (M) kills
(C), it descends to (H_{10}).  Exact elimination gives

\[
 M(H_{10})=\operatorname{im}(MM^{\mathsf T}),
 \qquad \dim M(H_{10})=10,
\]

and all (1024) quotient classes have distinct images.  The unique fixed
class satisfies

\[
\boxed{M(f)=\mathbf1.}
\]

Restricting to the polar hyperplane gives

\[
M(f^\perp)=R\cap R^\perp=K.
\]

The verifier enumerates both (512)-element sets independently before
comparing them; equality is not inferred from matching dimensions alone.

## Objectwise quadratic identity

For every one of the (512) classes ([x]\in f^\perp), the image
(z=Mx\) is doubly even and obeys

\[
\boxed{
 \frac{\operatorname{wt}(x)}2
 \equiv
 \frac{\operatorname{wt}(Mx)}4
 \pmod2 .
}
\]

The route-hull enumerator is recovered exactly:

\[
W_K(t)=1+135t^{16}+240t^{20}+135t^{24}+t^{40}.
\]

After quotienting the fixed lines, the quadratic census is

\[
256=136_{q=0}+120_{q=1},
\]

so the form is plus type.

## The Pass-175 240 becomes a two-sheet cover of the 120

The context code contains exactly (240) weight-six words.  Pass 176 proves
simultaneously that:

- they represent (240) distinct classes of (H_{10});
- those classes are exactly all anisotropic elements of (f^\perp);
- translation by (f) preserves the set and pairs it into (120) fibres;
- the two weight-six representatives in every fibre have disjoint supports;
- incidence maps them bijectively to the (240) weight-(20) words of (K).

Thus

\[
\boxed{
2\longrightarrow240\longrightarrow120
}
\]

is not a numerical analogy.  It is the fixed-line quotient map, on explicit
context and route words.

Polar orthogonality on the (120) anisotropic fibres gives

\[
\boxed{\operatorname{SRG}(120,63,30,36)},
\]

with (3780) edges.  This is the anisotropic (E_8/2E_8) graph of the
Pass-124/174 capstone, now recovered from the Pass-175 weight-six shell by
the original (W(3,3)) incidence matrix.

## Equivariance and boundary

Eight native symplectic transvections generate an action of exact order
(25920=|\PSp(4,3)|) on (H_{10}).  The witness checks

\[
M(gx)=g(Mx)
\]

for all (8\cdot1024=8192) generator/object pairs, and checks the induced
action on every vertex and edge of the (120)-graph.

This proves equivariance for the native (PSp(4,3)) coordinate action.  It
does **not** assert that this group is the full automorphism group of the
strongly regular graph.  The (240)-sheet carrier has a canonical antipodal
pairing, but Pass 176 does not yet reconstruct signed integral (E_8) Gram
products on those sheets.

## Reproduction

```bash
python analysis/w33_pass176_incidence_fixed_line_e8_bridge.py
pytest -q tests/test_pass176_incidence_fixed_line_e8_bridge.py
```

Artifacts:

- `analysis/w33_pass176_incidence_fixed_line_e8_bridge.py`
- `data/w33_pass176_incidence_fixed_line_e8_bridge.json`
- `tests/test_pass176_incidence_fixed_line_e8_bridge.py`

The certificate reports `PASS` on all (26) checks.
