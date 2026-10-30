# Pass 1335 — the Brauer tree closes the `58|23` extension

Pass 1147 proved that the saturated Schläfli-frame reduction in
characteristic five is a nonsplit sequence

\[
0\longrightarrow I_{58}\longrightarrow S_{81}
\longrightarrow Q_{23}\longrightarrow0
\]

over both \(W(E_6)\) and \(PSp(4,3)\), but deliberately left the dimension
of the ambient \(\operatorname{Ext}^1\) space open. Pass 1335 closes that
boundary.

## Exact group-block theorem

For \(G=W(E_6)\cong U_4(2).2\) and
\(G'=PSp(4,3)\cong U_4(2)\), GAP/CTblLib finds a Sylow-\(5\) subgroup of
order \(5\). The inner group has one relevant defect-one block. The outer
group has two sign-twist-related \(81\)-characters in two corresponding
defect-one blocks; GAP checks both, and both have the same tree. In each case
the ordinary vertices have degrees

\[
1,\ 24,\ 81,\ 64,\ 6
\]

in that path order. Its four simple edges have dimensions

\[
1,\ 23,\ 58,\ 6.
\]

The \(23\)- and \(58\)-edges meet at the ordinary \(81\)-vertex, whose
decomposition row is exactly \(23+58\). The defect group is cyclic and the
exceptional multiplicity is one. Brauer-tree algebra theory therefore gives

\[
\dim_{\mathbb F_5}\operatorname{Ext}^1_G(23,58)
=\dim_{\mathbb F_5}\operatorname{Ext}^1_G(58,23)=1,
\]

and the same two equalities for \(G'\).

Because Pass 1147 already constructs a nonzero class in the sign-twisted
\(\operatorname{Ext}^1(23,58)\) pair selected by its saturated frame module,
that class spans the full group. Its middle module is the unique nonsplit
isomorphism type up to rescaling the two simple endpoints. The second outer
block gives the sign-twisted companion statement; dimension alone is not being
used to identify the two \(81\)-characters.

## What the Pass-1330 Hecke radical sees

The literal \(432\)-character contributes

\[
2\cdot6+2\cdot64+81
\]

inside the same cyclic-defect block. Its rational commutant contribution has
dimension \(2^2+2^2+1^2=9\). This is the nonsemisimple nine-dimensional
central block in Pass 1330. The other nine-dimensional block is the
defect-zero species-\(20\) contribution \(M_3(\mathbb F_5)\).

A direct GAP derivation calculation from the certified \(26^3\) multiplication
tensor gives the scalar-simple Ext quiver

\[
h_6\rightleftarrows h_5\rightleftarrows h_7,
\]

with every displayed Ext space one-dimensional. This agrees with
\(\dim J=6\), \(\dim J^2=2\), and \(J^3=0\).
Here \(h_i\) denotes the \(i\)-th one-dimensional simple \(H_{26,\mathbb F_5}\)
module in the frozen seven-character order emitted by the Pass-1330
certificate; \(h_5,h_6,h_7\) are precisely the three scalar simples in the
nonsemisimple nine-dimensional block. These labels are Hecke-character indices,
not group-module dimensions.

The scope distinction is essential: this Hecke block is a
**condensation shadow** of the group block. It is not the literal
\(58|23\) middle module, and the Hecke quiver alone does not prove the group
Ext theorem. The full Brauer tree does.

## Triality does not mix the extension

Over \(\mathbb F_5\),

\[
\mathbb F_5[C_3]\cong\mathbb F_5\times\mathbb F_{25};
\]

\(x^3-1\) has factor degrees \(1+2\). Since \(5\) divides neither
\(|C_3|\) nor \(|S_3|\), the color algebras are semisimple. Künneth therefore
forces cross-color Ext to vanish.

The colored \(243\)-space has middle dimensions \(81+162\) over
\(\mathbb F_5\). After scalar extension to \(\mathbb F_{25}\), the quadratic
color sector splits into the \(\omega\) and \(\omega^2\) channels, yielding
three independent \(81\)-extensions. Full \(S_3\) triality packages these as
the trivial and standard color sectors; it transports the extension but
cannot create, destroy, or canonically select one copy.

## Reproduce

```bash
python3 analysis/w33_pass1335_export_hecke_gap_input.py
gap -q analysis/w33_pass1335_brauer_tree_hecke_corner.g
python3 -m pytest -q tests/test_w33_pass1335_brauer_tree_hecke_corner.py
```

The GAP-owned certificate is
[`data/w33_pass1335_brauer_tree_hecke_corner.json`](data/w33_pass1335_brauer_tree_hecke_corner.json),
SHA-256
`1a148fc745c623ecc6769e681144e0a5dc94997fb54674f331e93ed1f57604e2`.

## External foundation

The ordinary and modular character tables and decomposition matrices used by
the witness are the data structures documented in the
[official GAP Character Table Library manual](https://docs.gap-system.org/pkg/ctbllib/doc/manual.pdf).
The passage from adjacency in a line-shaped Brauer tree to the first-extension
quiver is standard Brauer-tree algebra; for an explicit treatment of the
Ext algebra for the line case, see O. Dudas,
[“The Ext-algebra of the Brauer tree algebra associated to a line”](https://arxiv.org/abs/2101.12480).
These references justify the general inference; the particular tree,
decomposition rows, block choice, and nonsplit module are computed in this
repository.
