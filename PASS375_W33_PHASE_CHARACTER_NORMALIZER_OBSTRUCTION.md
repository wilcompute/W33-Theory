# Pass 375: phase-character normalizer and regular-complement obstruction

## Status

Pass 375 is GAP-owned, exact, and regression-tested.  It closes the first
algebraic question left by Pass 374: whether the four scalar sheets can be
mixed by an order-three automorphism, or by a regular subgroup inside the
obvious split deck enlargement.

The answer is no in both cases.  The fixed phase character cuts the abstract
$S_4$ sheet normalizer to $D_8$, and
$W(E_6)\times(C_2\times C_2)$ has no regular subgroup complementary to the
Pass 374 sheet stabilizer.

## Corpus ownership and object separation

The result-first audit found five nearby constructions that must not be
identified merely because they contain a Klein four group:

- BT571, BT637, and BT644 own the four scalar lifts, the independent X/Z deck
  flips, and the phase character;
- BT1480 owns a commuting $C_3\times V_4$ ABI branch product;
- BT783 owns an unrelated $C_2^2{:}C_3$ cube/tomotope replacement law;
- Pass 214 owns a source-line $V_4\triangleleft S_4$ torsor;
- Pass 374 owns the natural signed minimal-pair action and its
  $C_2\times C_2$ sheet stabilizer.

Pass 375 cites those owners.  It does not merge their $V_4$'s.  In
particular, the external scalar deck group $D$ and the geometric stabilizer
$K<W(E_6)$ below are different subgroups acting on different objects.

## 1. The fixed phase character excludes the order-three sheet action

Write the scalar deck as

\[
D=(\mathbb F_3^\times)^2
 =\{(a,b):a,b\in\{\pm1\}\}
 \cong C_2\times C_2,
\]

and use the already-owned character

\[
\chi(a,b)=ab.
\]

Its two fibres give the phase partition

\[
\chi^{-1}(+1)=\{(+,+),(-,-)\},\qquad
\chi^{-1}(-1)=\{(-,+),(+,-)\}.
\]

GAP computes

\[
\operatorname{Aut}(D)\cong GL(2,2)\cong S_3.
\]

There are three order-two kernels, equivalently three nonzero characters of
$D$.  A Sylow $C_3<\operatorname{Aut}(D)$ cycles all three.  Consequently it
does not preserve the selected kernel of $\chi$, whose automorphism stabilizer
is only

\[
\operatorname{Stab}_{\operatorname{Aut}(D)}(\ker\chi)\cong C_2.
\]

The unrestricted abstract extensions do exist:

\[
D{:}C_3\cong A_4,\qquad D{:}S_3\cong S_4.
\]

But neither order-three action preserves the owned phase character.  This also
separates the result from BT1480: the commuting product there is

\[
C_3\times D\cong C_6\times C_2,
\]

not $A_4$.

## 2. The exact phase-compatible sheet normalizer is \(D_8\)

The regular deck $D$ sits in the full permutation group $S_4$ of the four
scalar lifts, and

\[
N_{S_4}(D)=S_4.
\]

Once the two-block phase partition is fixed, its setwise stabilizer is instead

\[
\boxed{
\operatorname{Stab}_{S_4}
 \bigl(\{\chi^{-1}(+1),\chi^{-1}(-1)\}\bigr)
 \cong S_2\wr S_2\cong D_8.
}
\]

It contains the regular deck normally and has quotient

\[
D_8/D\cong C_2.
\]

There is no element of order three in this phase-compatible normalizer.  Thus
$A_4$ and $S_4$ are valid abstract extensions of a bare $V_4$, but they
are not automorphism groups of this $V_4$ together with its fixed
$\chi$-partition.

## 3. The actual Pass 374 stabilizer has its own \(D_8\) quotient

Pass 375 independently rebuilds the 40 points, 240 edges, 40 lines, and 1620
quadrangles of $W(3,3)$, then reconstructs

\[
PSp(4,3)<PGSp(4,3)\cong W(E_6)
\]

with orders $25{,}920$ and $51{,}840$.

A minimal X ray is a point-line flag and a minimal Z ray is a quadrangle.  The
chosen visible pair is a flag lying on an edge of that quadrangle.  The
projective visible-pair stabilizers have orders two and four.  Projectivizing a
signed minimal pair sends its stabilizer into the corresponding projective
stabilizer; Pass 374 already proves the same two orders for the signed
stabilizers.  Containment plus equal order identifies them (up to conjugacy).

For the full group, let

\[
K\cong C_2\times C_2 < W(E_6)
\]

be that actual sheet stabilizer.  GAP gives

\[
|N_{W(E_6)}(K)|=32,
\qquad
N_{W(E_6)}(K)\cong(C_2^4){:}C_2,
\]

and therefore

\[
\boxed{N_{W(E_6)}(K)/K\cong D_8.}
\]

This $D_8$ and the scalar phase-partition $D_8$ are isomorphic outputs on
different objects.  No intertwiner is claimed.  Their coincidence identifies
the next constructive target; it is not used as if an object-level map already
existed.

## 4. The split deck enlargement cannot contain the missing torsor

The most obvious way to fuse the four Pass 374 orbits is the split group

\[
E=W(E_6)\times D,
\qquad |E|=207{,}360.
\]

It acts transitively on the four copies of $W(E_6)/K$, with stabilizer
$K\times1$, so the state set has size

\[
[E:K]=51{,}840.
\]

Suppose a subgroup $R<E$ acted regularly on those states.  Then $R$ would
complement $K$:

\[
E=RK,\qquad R\cap K=1,\qquad |R|=51{,}840.
\]

Projection $E\to D$ must map $R$ onto $D$, because $K$ lies entirely
in $W(E_6)\times1$.  Hence

\[
|\ker(R\to D)|=\frac{51{,}840}{4}=12{,}960.
\]

That kernel embeds in $W(E_6)$.  GAP enumerates all 350 conjugacy classes of
subgroups of the constructed $W(E_6)$ and finds no subgroup of order
$12{,}960$.  Therefore

\[
\boxed{
W(E_6)\times(C_2\times C_2)
\text{ contains no regular }51{,}840\text{-state complement.}
}
\]

There is also a short independent reason.  The derived subgroup
$PSp(4,3)$ is simple of index two in $W(E_6)$.  An order-$12{,}960$
subgroup would meet it in order $12{,}960$ or $6{,}480$.  The first case
would give an index-two subgroup of the simple group.  The second would give a
nontrivial degree-four coset action; simplicity would make
$PSp(4,3)\hookrightarrow S_4$, impossible by order.

As an external cross-check, the online ATLAS lists $U_4(2)\cong PSp(4,3)$
with order $25920$ and outer automorphism group $C_2$, and lists the maximal
subgroups of $U_4(2){:}2$; none has order $12960$:
<https://brauer.maths.qmul.ac.uk/Atlas/clas/U42/>.  The theorem here remains
GAP-owned because it uses the repository's explicit action and stabilizer.

## Breakthrough boundary

Pass 374's equality

\[
51{,}840=|W(E_6)|
\]

is still not a torsor theorem.  Pass 375 now proves more sharply that neither
an order-three automorphism of the fixed scalar character nor the split central
deck product supplies the missing regular transport.

Any successful lift must therefore be genuinely coupled: it must change how
the scalar deck and geometric stabilizer are glued, rather than append the
deck as a commuting factor.  The two independently arising $D_8$ quotients
give the smallest exact place to test such a coupling, but an explicit
intertwiner or an orbit-fingerprint obstruction remains to be constructed.

## Artifacts

- `analysis/w33_pass375_phase_character_normalizer_obstruction.g`
- `data/w33_pass375_phase_character_normalizer_obstruction.json`
- `tests/test_pass375_gap_phase_character_normalizer_obstruction.py`
- `PASS375_W33_PHASE_CHARACTER_NORMALIZER_OBSTRUCTION.md`

## Honest scope

Pass 375 is a finite-group obstruction theorem.  It proves exact normalizer and
subgroup facts for the owned finite actions.  It does not identify the scalar
and geometric $D_8$'s, construct a nonsplit transport group, establish braid
statistics, or supply a continuum physical dynamics.
