# Local C3 lift-charge theorem for the 648 -> 216 Clifford extension

## Exact input

The certified point-stabilizer extension is

\[
1\longrightarrow Z\cong C_3\longrightarrow K\longrightarrow Q\longrightarrow 1,
\qquad |K|=648,\quad |Q|=216,
\]

with `Q` the projective one-qutrit Clifford / Hessian `ASL(2,3)` quotient.  The extension is nonsplit.  The exact lift-order census from `PART_W33_20260829_CLIFFORD_C3_CIRCUIT_COVER.json` contains two classes of order-three quotient elements:

- 32 elements whose three lifts all have order 3;
- 48 elements whose three lifts all have order 9.

## Lift charge

Let `q in Q` have order three and choose any lift `g in K`.  Define

\[
\omega(q)=g^3\in Z.
\]

This is independent of the lift: replacing `g` by `g z^a`, with central `z^3=1`, leaves the cube unchanged because

\[
(gz^a)^3=g^3z^{3a}=g^3.
\]

Moreover

\[
\omega(q^{-1})=\omega(q)^{-1}.
\]

Thus the cube is a canonical local obstruction attached to each oriented order-three quotient element.

## Restriction classification

For a cyclic subgroup `C=<q>` of order three, its full preimage in `K` has order nine.  There are only two possibilities relevant here.

1. If `omega(q)=1`, every lift has order three.  The preimage has exponent three, hence is
   \[
   C_3\times C_3.
   \]
   The restricted central extension splits.

2. If `omega(q) != 1`, every lift has order nine.  The preimage is cyclic,
   \[
   C_9,
   \]
   and the restricted class is nonzero in `H^2(C3,C3) ~= C3`.

The 80 nonidentity order-three quotient elements form 40 cyclic subgroups, two generators per subgroup.  Therefore the exact census gives

\[
\boxed{16\text{ split }C_3\times C_3\text{ restrictions}}
\]

and

\[
\boxed{24\text{ nonsplit }C_9\text{ restrictions}}.
\]

Equivalently, the global extension class is detected nontrivially on

\[
\boxed{\frac{24}{40}=\frac35}
\]

of the cyclic order-three subgroups of `Q`.

After choosing a generator `z` of the central deck group, every nonsplit cyclic subgroup contributes one oriented generator with cube `z` and its inverse with cube `z^2`.  Hence the 48 nonzero oriented charges split exactly as

\[
\boxed{24\,z+24\,z^2}.
\]

## Interpretation and boundary

This sharpens the earlier global nonsplitting witness.  The obstruction is not merely a statement that no global section exists: it can be localized to 24 concrete cyclic order-three directions in the Clifford quotient, where the central three-sheeted cover thickens `C3` to `C9`.

The statement is finite-group/cohomological.  The central `C3` is an exact deck/extension charge.  Identifying its two nonzero characters with a measured optical phase, OAM phase, or hardware clock phase requires a separately proved physical intertwiner.

## Reproducibility

- executable: `analysis/w33_20260830_clifford_c3_lift_charge.py`
- input: `data/PART_W33_20260829_CLIFFORD_C3_CIRCUIT_COVER.json`
- frozen output: `data/PART_W33_20260830_CLIFFORD_C3_LIFT_CHARGE.json`
