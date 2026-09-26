# Pass 10965 — baryon triality is structurally impossible in the W(3,3) class

Producer: `analysis/w33_pass10965_baryon_triality_impossible.py`
Certificate: `data/w33_pass10965_baryon_triality_impossible.json`
Regression: `tests/test_w33_pass10965_baryon_triality_impossible.py`

## Why ask

Passes 10960–10964 showed that no matter parity survives the Fayet–Iliopoulos term in the
215 W(3,3) Z6 Standard Models. The other discrete symmetry that protects the proton in the
MSSM is **baryon triality** B3 = exp(2πi(B − 2Y)/3) (Ibáñez–Ross): charges mod 3
q 0, u^c 1, d^c 2, e^c 1, L 1, H_d 1, H_u 2. It forbids u^c d^c d^c and qqql and allows the
lepton-number-violating couplings. Holotrade b81ef8c excluded this "escape" by operator
counts (the three dimension-four operators are locked). This pass gives the structural
reason, exactly, for all 215 models.

## Result

A gauge B3 must be a Z3 character of the U(1) charge lattice agreeing with B3 on every
q, u^c, d^c, e^c up to a hypercharge rotation. Over GF(3) the system is **inconsistent in
215 of 215 models** (control: with target zero it is consistent in all 215).

**The obstruction is SU(5).** In 214 models single copies satisfy the exact charge identity

    Q(u^c) + Q(e^c) = 2 Q(q),

so every character has χ(u^c) + χ(e^c) − 2χ(q) = 0; B3 gives 1 + 1 − 0 = 2, and the
hypercharge shift contributes 2 + 0 − 2 = 0 (mod 3), so no shift repairs it. The remaining
model carries an explicit integer relation among its q, u^c, d^c, e^c charge vectors with
the same property.

## Consequence

Together with Passes 10960/10962 the discrete-symmetry landscape of proton protection in
the class is exhausted except for **R-symmetries**: the anomaly-free Z4^R of Lee, Raby,
Ratz, Ross, Schieren, Schmidt-Hoberg and Vaudrevange (arXiv:1009.0905), the unique
SU(5)-compatible choice, which in heterotic orbifolds comes from the internal rotation
(R-charge) sector rather than from the U(1) lattice. That is the one remaining route.

Scope: gauge (lattice-character) B3 only; R-symmetries and non-Abelian discrete flavour
symmetries are not covered.
