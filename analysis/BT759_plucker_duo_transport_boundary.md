# BT759 — Pluecker Duo-Transport Boundary

BT758 gives the executable \(Q(4,3)\) model:

\[
Q(x)=x_0x_1+x_2x_3+x_4^2=0\subset PG(4,3).
\]

It verifies:

\[
|Q(4,3)_{\rm pts}|=40,\qquad |Q(4,3)_{\rm lines}|=40,
\]

with four points per line and four lines through each point, and both point-collinearity and dual line-intersection graphs have

\[
\operatorname{SRG}(40,12,2,4).
\]

## The duo question

BT750 identified the duo bit as the central half-turn

\[
r^6
\]

inside the local \(D_{12}\) stabilizer of a rectangle lift fiber. BT755 proposed testing whether this central half-turn is visible on the dual \(Q(4,3)\)/Pluecker side.

The honest conclusion after BT758 is:

\[
\boxed{Q(4,3)\text{ is now executable, but }r^6\text{ has not yet been transported into it.}}
\]

## Required transport map

To decide the Pluecker-duo claim, the next verifier must construct a map

\[
\tau:
\{
\text{BT748 root-triple torsor coordinates}
\}
\longrightarrow
\{
\text{oriented }Q(4,3)\text{ apartments or dual line frames}
\}.
\]

Then the test becomes:

```text
T6a: tau(r^6 x) is defined for every local lift coordinate x.
T6b: tau(r^6 x) has the same underlying Q(4,3) apartment as tau(x).
T6c: tau(r^6 x) reverses the dual-apartment orientation or applies the candidate Pluecker polarity.
T6d: the action has order 2 and no fixed oriented frame.
```

Only after T6a--T6d pass can we promote the statement to:

\[
\boxed{\text{duo bit }=\text{ Pluecker mirror / dual-apartment orientation bit}.}
\]

## Boundary

BT758 proves the finite-geometric target. BT759 prevents overclaiming: the target exists, but the \(r^6\) transport has not yet been proven.
