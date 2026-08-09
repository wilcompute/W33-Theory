# Part CCCCCXIII — CP Kernel Jarlskog Theorem

## Executive result

Part CCCCCXII unified the flavor kernel. Part CCCCCXIII isolates the CP-violating subkernel and keeps the algebra exact.

The result is:

```text
CKM CP  -> rational cyclotomic slope / Wolfenstein area kernel
PMNS CP -> exact algebraic angular kernel with sqrt(5)
```

Both are projections of the same W(3,3) cyclotomic angular surface, but they live in different algebraic layers.

---

## 1. CKM CP kernel

The W(3,3) Wolfenstein parameters are:

```text
lambda_CKM = q^2/v = 9/40
A_CKM      = q^4/Phi_4^2 = 81/100
rho_bar    = (lambda/(mu+1))^2 = 4/25
eta_bar    = (Phi_6/Phi_4)^3 = 343/1000
```

The unitarity-triangle CP slope is:

```text
tan(gamma) = eta_bar/rho_bar = 343/160.
```

The leading Wolfenstein Jarlskog kernel is:

```text
J_CKM^(lead) = A^2 lambda_CKM^6 eta_bar.
```

Exactly:

```text
J_CKM^(lead) = 1195967049543 / 40960000000000000
             ≈ 2.91984142955e-5.
```

---

## 2. PMNS CP kernel

The W(3,3) PMNS parameters are:

```text
sin^2(theta_12) = mu/Phi_3 = 4/13
sin^2(theta_23) = mu/Phi_6 = 4/7
sin^2(theta_13) = q^2/(lambda*Phi_4)^2 = 9/400
delta_CP/pi     = (k-1)/Phi_4 = 11/10
```

Thus:

```text
delta_CP = 11pi/10.
```

So:

```text
sin(delta_CP) = -sin(pi/10),
sin^2(delta_CP) = (3 - sqrt(5))/8.
```

---

## 3. PMNS Jarlskog square

The PMNS Jarlskog factor has square:

```text
J_PMNS^2 = s12^2 c12^2 s23^2 c23^2 s13^2 c13^4 sin^2(delta_CP).
```

The rational prefactor is:

```text
B = s12^2 c12^2 s23^2 c23^2 s13^2 c13^4
  = 37150083 / 33124000000.
```

Therefore:

```text
J_PMNS^2 = B * (3 - sqrt(5))/8.
```

Equivalently:

```text
J_PMNS^2 = 111450249/264992000000 - 37150083*sqrt(5)/264992000000.
```

Taking the sign from `sin(11pi/10)<0`:

```text
J_PMNS ≈ -0.0103488208839.
```

---

## 4. Shared angular surface

The CKM and PMNS CP kernels use the same W(3,3) angular ingredients in different ways:

```text
CKM eta base:  Phi_6/Phi_4 = 7/10
PMNS CP base:  (k-1)/Phi_4 = 11/10
```

CKM turns the cyclotomic ratio into a rational cubic:

```text
eta_bar = (7/10)^3 = 343/1000.
```

PMNS turns the shifted Perron ratio into an angle:

```text
delta_CP = (11/10)pi.
```

That is why CKM CP is rational in this approximation while PMNS CP carries the exact pentagonal radical.

---

## 5. Verified checks

The verifier confirms:

| check | status |
|---|---:|
| true Master Equation `q! = 2q` | pass |
| W(3,3) atoms | pass |
| CKM parameters | pass |
| `tan(gamma)=343/160` | pass |
| leading CKM Jarlskog exact fraction | pass |
| PMNS angles and phase | pass |
| PMNS rational prefactor `B` | pass |
| `sin^2(delta_CP)=(3-sqrt(5))/8` | pass |
| exact PMNS Jarlskog square | pass |
| PMNS solar/atmospheric ratio `7/13` | pass |
| CKM eta base `7/10` | pass |
| PMNS delta base `11/10` | pass |
| CP hierarchy positive | pass |

---

## 6. Why this matters

This theorem separates two kinds of CP structure:

```text
CKM:  rational CP slope/area from cyclotomic ratios
PMNS: algebraic CP phase from a cyclotomic angle
```

So quark and lepton CP violation are not unrelated. They are two projections of one angular surface:

```text
Phi_6/Phi_4 and (k-1)/Phi_4.
```

---

## 7. New files

- `exploration/PART_CCCCCXIII_CP_KERNEL_JARLSKOG_THEOREM.py`
- `PART_CCCCCXIII_CP_KERNEL_JARLSKOG_THEOREM.md`
- `PART_CCCCCXIII_cp_kernel_jarlskog_theorem_results.json`

---

## 8. Next target

The next target is to connect the CP kernel to the earlier Bargmann/holonomy phase result:

```text
universal elementary phase = 6 mod 12 = -1
PMNS delta base = 11/10
CKM eta base = 7/10
```

The question is whether CP violation is the observable projection of the W(3,3) holonomy/phase lattice.
