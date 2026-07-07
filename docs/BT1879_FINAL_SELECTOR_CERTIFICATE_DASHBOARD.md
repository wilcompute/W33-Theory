# BT1879 — Final Selector Quotient Certificate Dashboard

## Canonical selector

Metric winner: **2**

Canonical E8 selector pairs:

\[
(3,68),\quad (4,42),\quad (38,65),\quad (90,144)
\]

## Quotient status table

| Stage | Status | Witness | Claim |
|---|---:|---|---|
| Support minimality | Closed | BT951 | Support 60 with six minimizers |
| Certificate graph | Closed partial | BT953 / BT1837 | Certificate orbits `[[0,1],[2],[3],[4],[5]]` |
| Vertex metric | Closed | BT954 | Minimizer 2 selected |
| Tetracode metric | Closed | BT956 / BT1840 | Minimizer 2 selected through recovered matrix |
| Transported S4 | Closed | BT959 / BT1845 | Orbit 24, stabilizer 1, support-60 singleton |
| Glue stabilizer | Closed | BT1855 | Signed monomial tetracode glue stabilizer `48 = 2 x 24` |
| S4 transport to H | Closed | BT1856 | S4 quotient transports to H |
| Support phase action | Closed at H support level | BT1861 / BT1871 | Central-inversion phase fixes winner-2 support mask |
| Integral E8 representative phase lift | Open | BT1870 / BT1875 / BT1876 | Needs concrete integral E8 representative vectors and chain-boundary compatibility |

## Phase bit

Invariant: `A2_integral_phase_coset_bit`

Ambient quotient:

\[
O(A_2)/W(A_2)
\]

| Bit | Meaning | H-support action |
|---:|---|---|
| 0 | Identity/Weyl coset | Fixes support selector |
| 1 | Central-inversion coset | Fixes support selector |

Both bits are invisible on the mod-2 H support selector. The nontrivial bit is an integral phase/bookkeeping class, not a support-mask change.

## Basis material found

BT1876 identifies `analysis/bt982_explicit_integral_e8_basis.py` as the primary candidate for instantiating the remaining model. BT982 constructs `final_integral_basis_B` in vertex E8 root coordinates and checks the standard E8 Cartan Gram. The next bridge is to map BT982 basis columns onto the BT1875 selector-pair/phase template and prove chain-boundary compatibility.

## Final boundary

Everything visible on the mod-2 H support shadow is closed.

The only remaining open layer is:

\[
\text{construct/prove a concrete integral E8 representative phase lift for the central-inversion class, with chain-boundary compatibility.}
\]

## Primary certificate

Machine-readable certificate: `data/PART_BT1874_FINAL_SELECTOR_QUOTIENT_CERTIFICATE.json`.
