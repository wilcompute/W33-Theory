# Passes 1054--1059: the Hessian point side, the signed obstruction, and the theorem firewall

## Executive result

Six independent attacks were run against the current Pass-1047 frontier. They close four of the five proposed next moves, sharpen the fifth into an exact no-go theorem, and add an adversarial sixth workstream against the newest parallel commits.

The central synthesis is

\[
240\ \text{signed endpoints}
\longrightarrow
120\ \text{unsigned local axes}
\longrightarrow
40\ W(3,3)\ \text{points},
\]

with two sharply different symmetry layers:

* the **unsigned** 120-axis carrier is exactly equivariant under the internal projective group \(PSp(4,3)\);
* the **signed** 240-endpoint carrier has no internal equivariant lift. A four-equation \(\mathbb F_2\) certificate XORs to \(0=1\).

This makes the previously qualitative statement “the substrate cannot orient its own axes” a finite, reproducible obstruction theorem.

---

## Pass 1054 -- explicit Hessian affine normal form

The selected order-648 point stabilizer is reconstructed directly from the 40-point symplectic action and put into the normal form

\[
H \cong 3^{1+2}_{+}:SL(2,3).
\]

The witness constructs:

* a unique normal extraspecial Heisenberg subgroup \(N\) of order 27;
* generators \(x,y,z\) with \(z=[x,y]\in Z(N)\), and unique coordinates \(x^a y^b z^c\);
* a disjoint complement \(L\) of order 24;
* the full \(SL(2,3)\) action of \(L\) on \(N/Z(N)\cong\mathbb F_3^2\);
* a unique \(N L\) decomposition of all 648 elements;
* a faithful affine degree-27 action with center 3 and derived subgroup 216.

This upgrades Pass 1046 from an invariant fingerprint to an explicit permutation-level isomorphism with the Hessian semidirect product. It does **not** yet provide a complex \(3\times3\) CHEVIE conjugating matrix.

Witnesses:

* `analysis/w33_pass1054_hessian_affine_isomorphism.py`
* `data/w33_pass1054_hessian_affine_isomorphism.json`

---

## Pass 1055 -- unsigned equivariance and the signed obstruction

The code quotient \(C^\perp/C\cong\mathbb F_2^8\) is rebuilt independently. The 120 local pencil-octahedron axes are identified with all 120 anisotropic classes and then, through an explicit plus-type quadratic isometry, with the 120 antipodal \(E_8\) root lines.

For every generator of a generating set of \(PSp(4,3)\), the 120-axis map commutes exactly:

\[
F(g\cdot a)=g\cdot F(a).
\]

The unsigned carrier is therefore an actual equivariant object, not merely an SRG or spectral coincidence.

The signed problem asks whether one can choose one bit \(s_a\in\mathbb F_2\) for every axis so that the induced action on the two endpoints preserves the signed \(E_8\) inner products. The complete linear system is inconsistent. Four explicit equations suffice:

\[
E_1+E_2+E_3+E_4:\qquad 0=1.
\]

The certificate uses only generators 6 and 19 and axes 0, 48, 49, 50, 60. Thus no reassignment of the 120 root signs repairs equivariance.

Consequently:

\[
\boxed{\text{axis / }\mathbb Z_3\text{ choice is internal; endpoint / }\mathbb Z_2\text{ choice is not.}}
\]

Witnesses:

* `analysis/w33_pass1055_unsigned_equivariant_signed_obstruction.py`
* `data/w33_pass1055_unsigned_equivariant_signed_obstruction.json`

---

## Pass 1056 -- exact fusion of the two order-648 classes

Both maximal order-648 stabilizers are embedded in the same degree-40 action of \(PSp(4,3)\), and every subgroup conjugacy class is fused into the ambient conjugacy classes.

The exact distinction is:

| stabilizer | subgroup classes | normal 27 | center of normal 27 | derived of normal 27 |
|---|---:|---|---:|---:|
| point / Hessian | 24 | extraspecial \(3^{1+2}\) | 3 | 3 |
| line / dual | 17 | elementary abelian \(3^3\) | 27 | 1 |

This supplies the full class-fusion data needed to prevent the repeated integer 648 from collapsing two nonisomorphic groups.

Witnesses:

* `analysis/w33_pass1056_two_648_class_fusions.py`
* `data/w33_pass1056_two_648_class_fusions.json`

---

## Pass 1057 -- action-semantics firewall and Pass-1043 amendment

Pass 1043 computed the list

\[
[1,1,1,27,27,27,36]
\]

using

```gap
Orbits(Stabilizer(Q120,1), [1..120])
```

so the list consists of **point-stabilizer subdegrees**. The manuscript fingerprint to which it was compared was described as a **whole-group orbit partition**. Those are different invariants.

The independent recomputation shows that the code embedding itself:

* is transitive on all 120 anisotropic classes;
* has whole-group quotient orbits \(1+120+135\);
* nevertheless has exactly the same rank-7 point-stabilizer subdegrees \([1,1,1,27,27,27,36]\).

Therefore the Pass-1043 inference “the Springer tower realizes the Pass-117 embedding” is not established by that test. The raw subdegree calculation remains valid; its interpretation is superseded.

Firewall rule:

> Compare the same acting group, on the same ambient set, using the same invariant type. Subdegrees compare only with subdegrees; whole-group orbit partitions compare only with whole-group orbit partitions.

Witnesses:

* `analysis/w33_pass1057_action_semantics_firewall.py`
* `data/w33_pass1057_action_semantics_firewall.json`

---

## Pass 1058 -- a second experimental discriminator

The point/Hessian stabilizer has central \(C_3\), while the dual line stabilizer has trivial center. Two explicit generators on the 40 modes turn this into a finite process-tomography test.

Among all order-3 candidates:

* point side: exactly two nonidentity candidates commute with both generators; each has cycle type \(1^{13}3^9\);
* dual side: none commute with both; the closest impostor produces exactly 27 total mode mismatches.

This gives a discriminator independent of the contextual-fraction test:

1. calibrate the two displayed generator permutations \(a,b\);
2. implement an order-3 candidate \(c\);
3. compare \(ca\) with \(ac\), and \(cb\) with \(bc\);
4. two exact commuting candidates means point/Hessian side; none, with a 27-mode gap, means dual side.

Witnesses:

* `analysis/w33_pass1058_central_c3_discriminator.py`
* `data/w33_pass1058_central_c3_discriminator.json`

---

## Pass 1059 -- adversarial audit of the parallel Pass-2/3/4 arc

The parallel commits contain useful arithmetic and toy-model checks, but they also promote several unconstructed maps into theorems. The audit retains the exact layer and rejects the promotions.

### Exact results retained

* \(1-81+40=-40\);
* \(196560=6\mu q^2\Phi_3\Phi_4\Phi_6\);
* \(196884=196560+18^2\);
* \(\dim Gr(4,14)=40\);
* the displayed Jones matrices are unitary;
* the BC rotation has exactly two gap lengths at 30, with ratio \(1.5740226838\);
* the finite W33 adjacency gap is \(12-2=10\);
* the nontrivial Ihara roots lie on \(|u|=1/\sqrt{11}\).

### Hard corrections

* the Lock-0 script uses \(4/(q^2+1)\), which equals \(2/5\) at \(q=3\), while printing \(1/10\);
* a linear action cannot cycle summands of dimensions \(5,5,30\); the H2 decomposition supports at most the \(C_2\) swapping the two 5s;
* \(\mathcal A(14,4,4)\) has dimension \(km=16\), not 40;
* \(W(3,3)\) has 40 line contexts, not 120;
* \(|S_4|=24\), not 48; \(25920/48=540\) is not a quotient by \(S_4\);
* the claimed gap ratio 15.357 is numerically incorrect;
* the CMB script prints a chi-square constant but loads no data and evaluates no likelihood;
* the Pass575 “fix” commit changes no Lean source and therefore verifies no build;
* a finite graph spectral gap does not solve the continuum Yang--Mills mass-gap problem;
* a common RH-shaped circle does not establish equality of Ihara and Weil zeta functions.

The amendment preserves these as research directions while keeping them out of the theorem tier until the missing maps, data analyses, continuum limits, or formal builds exist.

Witnesses:

* `analysis/w33_pass1059_parallel_claim_audit.py`
* `data/w33_pass1059_parallel_claim_audit.json`

---

## Verification ledger

| pass | exact checks |
|---|---:|
| 1054 | 14 |
| 1055 | 10 |
| 1056 | 12 |
| 1057 | 8 |
| 1058 | 7 |
| 1059 | 20 |
| **total** | **71** |

The regression suite reruns every witness from source. Pass 1056 is the slow path because it enumerates and fuses all conjugacy classes; the other five complete in seconds.

## Honest boundary

This package proves finite group, action, code-quotient, fusion, and obstruction statements. It does not claim:

* a complex-matrix conjugator to CHEVIE's \(G_{25}\) model;
* an internal signed-root action after the no-go certificate;
* a physical execution of the central-\(C_3\) discriminator;
* a W33 amplituhedron, CMB transfer function, Yang--Mills continuum theory, Weil variety, or moonshine module.
