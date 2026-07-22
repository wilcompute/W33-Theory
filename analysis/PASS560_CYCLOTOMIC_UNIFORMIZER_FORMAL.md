# Pass 560 — formal fifth-cyclotomic uniformizer identity

Lean now proves the translated fifth-cyclotomic identity

`Phi5(1-lambda) = lambda^4 - 5 lambda^3 + 10 lambda^2 - 10 lambda + 5`

and therefore

`lambda^4 = 5 (lambda^3 - 2 lambda^2 + 2 lambda - 1)`.

It also proves that the residual factor is `-1 mod lambda`. Under standard additive valuation laws, `v(5)=4`, and valuation zero for the residual factor, Lean derives `v(lambda)=1` and `v(lambda^n)=n`.

The polynomial algebra is now theorem-backed. Construction and completeness of `Q_5(zeta_5)`, and the local-ring theorem making the residual factor a unit, remain explicit model fields rather than hidden assumptions.
