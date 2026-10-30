# Pass 541 — the q=3 trace-valuation law for every exponent

Passes 519–523 found and explained the finite-window pattern

\[
  \min_c v_\lambda\!\left(\operatorname{tr}D_c^m\right)
  =2\bigl(m+[m\text{ odd}]\bigr),
\]

but they did not prove it beyond the measured window.  Pass 528 then reduced
all 81 sections to six characteristic polynomials.  That reduction makes
the infinite problem finite at the level of recurrences, and Pass 541 closes
the remaining noncancellation step.

## Theorem

For every integer $m\ge2$, over the complete $q=3$ section space,

\[
  \boxed{
  \min_c v_\lambda\!\left(\operatorname{tr}D_c^m\right)
  =2\bigl(m+[m\text{ odd}]\bigr)}.
\]

The statement is exhaustive in $c$ and infinite in $m$.  The exponent
$m=1$ is excluded because every section has trace zero.

## Proof

The six realized characteristic polynomials are

\[
 x^3-9a x-27b,\qquad
 (a,b)\in\{(0,0),(1,0),(2,0),(3,0),(3,1),(4,3)\}.
\]

Put $x=3y$.  If $S_m$ is the $m$-th power sum of the roots of
$y^3-ay-b$, then

\[
 S_0=3,\qquad S_1=0,\qquad S_2=2a,\qquad
 S_m=aS_{m-2}+bS_{m-3},
\]

and

\[
 \operatorname{tr}D_c^m=3^mS_m,\qquad
 v_\lambda(\operatorname{tr}D_c^m)=2m+2v_3(S_m).
\]

For even $m$, integrality gives the lower bound $2m$.  The row
$(a,b)=(1,0)$ satisfies $S_m=S_{m-2}$, with $S_1=0,S_2=2$; hence
$S_m=2$ for every even $m\ge2$, attaining the bound.

For odd $m$, all three nonzero $b=0$ rows vanish.  The two remaining rows
are

\[
\begin{aligned}
 A_m&=3A_{m-2}+A_{m-3}, &(A_0,A_1,A_2)&=(3,0,6),\\
 B_m&=4B_{m-2}+3B_{m-3}, &(B_0,B_1,B_2)&=(3,0,8).
\end{aligned}
\]

Modulo $3$, every odd term of both sequences is zero, so every finite odd
trace has valuation at least $2(m+1)$.  Modulo $9$, the $A$-state is
periodic with word

\[
  3,0,6
\]

from $m=0$, while the $B$-tail from $m=2$ has period six with word

\[
  8,0,5,6,2,3.
\]

Therefore $A_m$ is $3$ or $6\pmod9$ for odd
$m\equiv3,5\pmod6$, and $B_m\equiv3\pmod9$ for
$m\equiv1\pmod6$, beginning at $m=7$.  Those are all odd residue classes;
one row always has $v_3(S_m)=1$.  The odd lower bound is attained, proving
the formula.  Repetition of the recurrence state, not a long numerical sweep,
is the infinite step.

## Two corollaries

First, the coefficient-valuation profile is now a complete invariant of the
trace-valuation sequence for every $m$ on the realized $q=3$ image.  Its
only repeated fiber is $(a,b)=(1,0),(2,0)$; both have odd power sums zero and
even power sums $2a^{m/2}$, which are $3$-adic units.

Second, Legendre's identity $2v_3(m!)=m-s_3(m)$ turns the comparison with the
disproved factorial formula into an exact theorem:

\[
  \text{agreement}\quad\Longleftrightarrow\quad
  s_3(m)+[m\text{ odd}]=2.
\]

Because the parity of an integer is the parity of its ternary digit sum, this
condition has an explicit classification for $m\ge2$:

\[
  m=3^j\quad(j\ge1),
  \qquad\text{or}\qquad
  m=3^i+3^j\quad(0\le i\le j).
\]

The first family is the prime-power tower.  The second is the full two-place
ternary branch, so the tower is a proper subset of the agreement locus.

## Boundary

Nothing here transfers the formula to $q=5$, where the section image is much
larger and the existing minima are sampled.  Nothing here repairs the
factorial formula; it proves the different $q=3$ law and identifies exactly
where the two expressions happen to agree.  It also does not address the
uniform composite-$m$ completeness conjecture for the cyclic-class relation
space.

The exact owner is
[`analysis/w33_pass541_q3_all_m_recurrence.g`](analysis/w33_pass541_q3_all_m_recurrence.g),
which emits
[`data/w33_pass541_q3_all_m_recurrence.json`](data/w33_pass541_q3_all_m_recurrence.json).
The regression harness is
[`tests/test_pass541_gap_q3_all_m_recurrence.py`](tests/test_pass541_gap_q3_all_m_recurrence.py).
