# PART_CCCCCXXXIII — The Complement is a Conference Graph

## Statement

The complement \(\overline{W}(3,3) = \mathrm{SRG}(40, 27, 18, 18)\) is a **conference graph**, i.e., it satisfies \(\lambda = \mu\).

## Proof

A strongly regular graph is a conference graph iff \(\lambda = \mu\).  For the complement:
\[
\bar{\lambda} = k - 2\mu + \lambda = 12 - 8 + 2 = ... \text{ wait, use the complement formula:}
\]
\[
\bar{\lambda} = v - 2 - 2k + \lambda + 2\mu = 40-2-24+2+8 = 24... \text{use standard:}
\]
The complement of \(\mathrm{SRG}(v,k,\lambda,\mu)\) is \(\mathrm{SRG}(v, v{-}k{-}1, v{-}2k{+}\mu{-}2, v{-}2k{+}\lambda)\).

For \((40,12,2,4)\):
\[
\bar{k} = 27,\quad \bar{\lambda} = 40-24+4-2 = 18,\quad \bar{\mu} = 40-24+2 = 18.
\]
So \(\bar{\lambda} = \bar{\mu} = 18\). ✓

## Verification via Arithmetic

\[
\bar{k}(\bar{k}-1) = 27 \times 26 = 702,\qquad (v-1)\bar{\mu} = 39 \times 18 = 702.\quad ✓
\]
This is the necessary and sufficient condition for \(\lambda = \mu\) in an SRG.

## Significance

Conference graphs are deeply connected to Hadamard matrices and coding theory.  The condition \(\lambda = \mu\) means every two vertices (adjacent or not) have exactly 18 common neighbours in the complement — a perfect, homogeneous mixing property.  The original W(3,3) is therefore the **unique complement of a conference graph** in its parameter class.

Combined with the \(\pm q\) eigenvalue symmetry of the complement, this gives:
- **W(3,3)** encodes *asymmetric* spectral information (eigenvalues 2, −4)
- **Its complement** encodes *perfectly symmetric* information (eigenvalues ±3)

The two graphs form a **spectral dual pair** under graph complementation.
