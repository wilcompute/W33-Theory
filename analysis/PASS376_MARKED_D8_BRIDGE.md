# Pass 376: the marked (D_8) bridge has four choices

Pass 375 correctly stopped at an important boundary: the phase-compatible
normalizer of the four scalar lifts and the quotient

\[
N_{W(E_6)}(K)/K
\]

are both abstractly (D_8), but they arise on different objects.  Equality of
the group name did not supply an intertwiner.

Pass 376 resolves exactly the group-theoretic part of that question, and no
more.  It constructs a marked-extension isomorphism

\[
\bigl(D_8,\;D=(\mathbb F_3^\times)^2\cong V_4\bigr)
\;\cong\;
\bigl(N_{W(E_6)}(K)/K,\;C_N(K)/K\cong V_4\bigr).
\]

The two marked extensions have the same quotient (C_2), the same conjugation
fingerprint (1+1+2) on the marked (V_4), and their centers correspond.  The
fixed phase-character kernel is exactly the phase-side center:

\[
\ker\chi=Z(D_8),\qquad |Z(D_8)|=2.
\]

There are, however, exactly **four** marked isomorphisms.  Their residual
ambiguity group is (C_2\times C_2).  Thus the new result is a canonical
central-(C_2) *type* correspondence, not a canonical choice of map.

## What is computed

The GAP witness rebuilds the (40)-point, (240)-edge (W(3,3)) geometry,
forms the full (W(E_6)=PGSp(4,3)) action of order (51840), and selects the
same visible-pair stabilizer (K\cong V_4) used in Passes 374--375.  It then
computes

\[
|N_{W(E_6)}(K)|=32,
\qquad
N_{W(E_6)}(K)/K\cong D_8,
\qquad
C_N(K)/K\cong V_4.
\]

On the scalar side it starts with the four signed lifts, preserves the fixed
(2+2) character partition, and obtains

\[
D=(\mathbb F_3^\times)^2\cong V_4
\triangleleft D_8,
\qquad D_8/D\cong C_2.
\]

The corresponding geometric statement is

\[
C_N(K)/K\triangleleft N_{W(E_6)}(K)/K,
\qquad
\bigl(N_{W(E_6)}(K)/K\bigr)\big/\bigl(C_N(K)/K\bigr)\cong C_2.
\]

In both cases the quotient action on the marked (V_4) has orbit sizes
(1+1+2).  This is stronger than an order comparison and weaker than a
state-space identification, exactly as it should be.

For corpus searches, the compact exact signature is
`32/8/4/2/1/1/2/4`: normalizer order, quotient order, marked-deck order,
quotient order, conjugation orbit profile, and marked-isomorphism count.

## The fourfold boundary

GAP constructs one marked isomorphism mapping the phase deck (D) onto
(C_N(K)/K) and maps the center to the center.  It also enumerates the full
marked ambiguity:

\[
\#\{\text{marked isomorphisms}\}=4,
\qquad
\operatorname{Aut}(D_8;D)\cong C_2\times C_2.
\]

Consequently no choice in this certificate singles out one scalar sheet as a
geometric point, one physical phase, or a regular (W(E_6)) action.  Those
would require additional data beyond the two marked group extensions.

## Ownership and scope

- Pass 374 owns the natural signed-chain action on the four (12960)-state
  minimal logical (X/Z) sheets.
- Pass 375 owns the phase-character restriction to (D_8), the geometric
  (D_8) quotient, and the no-regular-complement theorem.
- Pass 376 owns only the marked (V_4{:}C_2) comparison and the exact
  fourfold ambiguity count.

This is a finite-group theorem.  It establishes no hardware implementation,
physical phase identification, continuum bridge, or Standard-Model claim.

## Reproduce

```bash
gap -q analysis/w33_pass376_marked_d8_bridge.g
python3 -m pytest tests/test_pass376_gap_marked_d8_bridge.py -q
```

The witness writes
`data/w33_pass376_marked_d8_bridge.json`; it records 20 exact checks, including
the marked-extension structure, both (1+1+2) conjugation profiles, the center
map, the search signature `32/8/4/2/1/1/2/4`, and the (C_2\times C_2)
ambiguity group.
