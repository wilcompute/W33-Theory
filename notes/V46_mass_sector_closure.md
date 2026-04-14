# V46 — Exact Mass-Sector Closure after the Light-Quark Repair

## Starting point

The repaired fermion packet now uses

\[
\frac{m_c}{m_t}=\frac{1}{136}, \qquad
\frac{m_u}{m_c}=\frac{1}{vg}=\frac{1}{40\cdot 15}=\frac{1}{600},
\]

\[
\frac{m_b}{m_t}=\frac{1}{v+\lambda}=\frac{1}{42}, \qquad
\frac{m_s}{m_b}=\frac{q}{136}=\frac{3}{136}, \qquad
\frac{m_d}{m_s}=\frac{1}{(q+\lambda)\mu}=\frac{1}{20}.
\]

This is already numerically good. The new point is that the packet also closes
**algebraically** in several exact ways.

## Closure 1 — strange/up bridge

Divide the strange suppression by the charm suppression:

\[
\frac{(m_s/m_b)}{(m_c/m_t)}
  = \frac{q/136}{1/136}
  = q
  = 3.
\]

So the strange/charm bridge is exactly the field-size parameter \(q\).

## Closure 2 — light-quark bridge

Compare the light-up suppression to the light-down suppression:

\[
\frac{(m_u/m_c)}{(m_d/m_s)}
  = \frac{1/600}{1/20}
  = \frac{1}{30}.
\]

Since

\[
v-\Phi_4 = 40-10 = 30,
\]

this becomes

\[
\frac{(m_u/m_c)}{(m_d/m_s)} = \frac{1}{v-\Phi_4}.
\]

That is striking because \(v-\Phi_4\) is exactly the same \(30\) that enters the
inflation sector before the \(N=60\) bridge is taken.

## Closure 3 — strange/charm ratio

Eliminate the top and bottom scales:

\[
\frac{m_s}{m_c}
  = \frac{m_s/m_b}{m_c/m_t}\frac{m_b}{m_t}
  = q \cdot \frac{1}{v+\lambda}
  = \frac{3}{42}
  = \frac{1}{14}
  = \frac{1}{2\Phi_6}.
\]

So

\[
\frac{m_s}{m_c} = \frac{1}{2\Phi_6}.
\]

## Closure 4 — up/down ratio

Eliminate the heavy scales in the opposite direction:

\[
\frac{m_u}{m_d}
  = \frac{m_u/m_c}{m_d/m_s}\cdot\frac{m_c}{m_s}
  = \frac{1}{30}\cdot 14
  = \frac{7}{15}.
\]

Since \(\Phi_6 = 7\) and \(g=15\),

\[
\frac{m_u}{m_d} = \frac{\Phi_6}{g}.
\]

## Closure 5 — product identity

Multiplying the last two exact identities gives

\[
\frac{m_s}{m_c}\frac{m_u}{m_d}
  = \frac{1}{14}\cdot\frac{7}{15}
  = \frac{1}{30}
  = \frac{1}{v-\Phi_4}.
\]

So the mass sector contains the same \(30\)-mode bridge as the repaired
inflation sector.

## Interpretation

After the light-quark repair, the fermion sector is no longer just a set of
accurate formulas. It contains an exact closure packet:

\[
\frac{m_s/m_b}{m_c/m_t}=q,\qquad
\frac{m_u/m_c}{m_d/m_s}=\frac{1}{v-\Phi_4},\qquad
\frac{m_s}{m_c}=\frac{1}{2\Phi_6},\qquad
\frac{m_u}{m_d}=\frac{\Phi_6}{g}.
\]

These identities eliminate the intermediate heavy scales and show that the
repaired mass packet is internally rigid, not merely numerically lucky.
