# Six positive native magnetic Wilson-loop differences: an all-momentum theorem

**Date:** 28 October 2026. **Scope:** native 27-site / 135-link / four-period voltage-cover Euclidean gauge model. This is an independent continuation of `9baf04f1752f`, `449bcd3c5568`, `f18d0e98eb53`, and the later exact global rank theorem in `analysis/PASS12341_12345_GLOBAL_BLOCH_AND_PHYSICAL_CONTROLS.md`. It does **not** derive a physical photon, Lorentzian time, gauge coupling, mass gap, gravity or a theory of everything.

**Deliverables:** `analysis/w33_20261028_six_term_native_bloch_repair.py`, this report, `data/w33_20261028_six_term_native_bloch_repair.json`, and `tests/test_w33_20261028_six_term_native_bloch_repair.py`.

## 1. Existing global geometry

The previous all-Bloch theorem proves (by literal Laurent unit minors in the native 135-edge complex) that the 105 selected short faces F have rank105 for every character in `(C*)^4`, while the four primitive period rows remain independent modulo F. The six based commutators induce the canonical four-dimensional bivector map

```text
C(d): C^4 -> Lambda² C^4,
       u -> d wedge u,

d_i = h_i-1,  h=z^W,
W = [ 0  1  1 -1
     -1  0  1 -1
      0  0  1 -1
      0  0  1  0 ], det W=1.
```

The existing three compact magnetic channels are

```text
R = [1 0  5 -5 1 0
     0 1 -1  0 1 0
     0 0  5 -5 0 1].
```

They match the native O(k²) acoustic cone, but the rank of `R C(d)` falls to two on the nonidentity quadratic sheet `Q(d)=0`. The already-proved **twelve-term** repair (and earlier twenty-four-term version) restores the full six-commutator kernel at all unitary momentum.

## 2. Two *extra* native commutator channels suffice algebraically

Choose just original commutator channels 0 and 5, i.e. select

```text
P = [1 0 0 0 0 0
     0 0 0 0 0 1].
```

The stacked five-by-six integer matrix `A=[R;P]` has rank5 and the exact kernel

```text
ker A = span{ v },   v=(0,1,1,1,0,0).
```

In the natural ordered six-bivector basis `(01,02,03,12,13,23)`, the Plücker/Klein quadratic is

```text
Pf(v) = v_01 v_23 - v_02 v_13 + v_03 v_12 = 1.
```

Therefore v is a **nondecomposable symplectic bivector**. Every nonzero vector in the image of `C(d)` for `d != 0` is a *decomposable* bivector `d wedge u`, and hence has Pfaffian zero. Thus

```text
ker A intersect image C(d) = {0} for all d in C^4\{0},
rank A C(d) = rank C(d) = 3.
```

This is a full complex-projective statement rather than a sample-point rank coincidence. Exact enumeration further shows the same fact for **all 15 pairs of native original commutator channels**: each primitive kernel generator has a nonzero Pfaffian. The (0,5) pair is especially convenient because its primitive Pfaffian is 1, not 25 or 30.

**Algebraic lower bound (proper scope).** A four-by-six matrix has kernel dimension at least two. Any projective line inside that kernel meets the Plücker quadric `Pf=0` over the algebraically closed field C (a homogeneous quadratic on P1 has a zero). Thus **at least five** scalar flux channels are required to be injective on *every abstract nonzero complex momentum bivector d wedge C4*. This does **not** establish that five channels are necessary to avoid rank loss only on the physical unitary Bloch torus, nor that six translated cosine terms is globally minimal.

## 3. Six *positive compact* translated differences are enough over the full Bloch torus

At cell position x, let `f_0(x)` and `f_5(x)` denote the phases of the two literal native based commutator Wilson loops. Add

```text
Delta V = epsilon sum_(a in {0,5}) sum_(mu=0,1,2)
          [1 - cos(f_a(x+e_mu)-f_a(x))],
epsilon>0.
```

These are **six** positive gauge-invariant compact U(1) terms. The Bloch quadratic form is

```text
Delta H(k) = epsilon w(z) (P L6(z))^dag (P L6(z)),
w(z) = |z_0-1|²+|z_1-1|²+|z_2-1|².
```

**Case A: w(z)>0.** At least one of `z0,z1,z2` differs from 1. Both additional P channels are positive and active. Since `rank A C(d)=3`, the full native curl `[F; R L6; sqrt(w) P L6]` has the **same magnetic kernel** as `[F;L6]`, using the existing Laurent-period independence theorem.

**Case B: w(z)=0.** On the unit torus this means `z0=z1=z2=1`. Along the residual one-dimensional line, `h=(z3^-1,z3^-1,z3^-1,1)` and the existing quadratic exceptional polynomial reduces *exactly* to

```text
Q(h-1) = 6 (z3^-1-1)^2.
```

It is nonzero whenever `z3 !=1`, so the original mixed 3-channel curl already has rank108 and the inactive repair is not needed. Equivalently its explicit 3-by-3 commutator minor is `6(z3^-1-1)^3`.

**Case C: identity.** At `z=(1,1,1,1)`, all commutator Bloch rows vanish and both models have rank105, with the same four global holonomies.

Hence the **magnetic Hessian nullspace equals the full six-loop model for every unitary Bloch character**. This is an all-momentum kernel theorem, not a positivity lower bound uniform in system size. Each commutator row is O(k), while w=O(k²); the new term enters at **O(k⁴)** and does not alter the established O(k²) native acoustic cone. It may change finite-momentum dispersion and near-zero stiffness.

The six-term construction **halves the prior 12-term count** (and quarters the original 24-term count). Its native cost is loop traversals plus translated loop differences; no photonic optical hardware resources or locality times have been estimated. The count refers to written compact cosine couplings, not fundamental gates.

## 4. Independent native 135-link matrix audit

The verifier reconstructs all 105 short faces, six actual based 16-edge commutators and their four-component integral voltages from the current repository's frozen inputs. It computes exact finite-field Gaussian ranks on all torsion characters:

| Test | Field | Characters | Repaired ranks | Difference from six-loop reference |
|---|---:|---:|---|---:|
| Third roots | F103 | 81 | 1 of rank105; 80 of rank108 | 0 |
| Fourth roots | F101 | 256 | 1 of rank105; 255 of rank108 | 0 |
| Fifth roots | F101 | 625 | 1 of rank105; 624 of rank108 | 0 |

These finite-field checks are a second code-level verification of the literal native geometry. They do **not** replace the projective-Pfaffian plus residual-line theorem. For finite-field specializations, positive physical weights `|z-1|²` are represented only by the *activation condition* `z!=1`, not by the complex-conjugate numerical weight in Fp; the rank check is structural.

For the previously published exact order-three nongauge witness at `z=(omega,omega,1,1)`, the original commutator norms were `[4112913,4112913,4112913,4112913,4112913,0]` and the original vector norm was 19641258. The (0,5) repair thus has normalized extra stiffness at epsilon=0.001 of

```text
6*4112913 / (1000*19641258) = 49/39000 > 0.
```

This is one *witness-dependent Rayleigh cost*, not the actual smallest eigenvalue or a universal parameter. It is smaller than the 12-term repair's 49/13000 because the (0,5) pair includes a loop that happens to vanish on that particular witness. This may be beneficial for perturbative action cost or disadvantageous for the size of the induced gap.

## 5. Consequences, source ownership and next falsifiers

This is a geometric optimization of the **supplied** U(1) compact lattice action; it does not derive the action from the E6 matter determinant. The known parallel work has already proved a **two-dimensional sheet of nongauge Bloch zeros** for the unrepaired three-loop model and a finite-cover soft-mode bound; the six-term repair removes the exact nongauge kernel but says nothing about a uniform gap or the physical dimension of spacetime.

The nondecomposable Pfaffian is a natural bridge to the Klein-quadric language already present elsewhere in W33: **decomposable bivectors describe projective lines; a nondegenerate bivector describes a symplectic form and lies off the Klein quadric**. Here that distinction provides a concrete *engineering certificate* for choosing flux channels—an invariant-algebraic reason the reduction succeeds, not merely a matching cardinality.

### Five independent next experiments

1. **Fewer-than-six compact loops:** search unequal translation patterns and other integer-linear Wilson combinations for a proof-certified 2–5-harmonic all-torus completion, or establish a lower bound using the global quadratic exceptional sheet and Laurent ideal.
2. **Measured gap and propagation:** compute a full 135-link Bloch spectrum for the six-term action over adaptive four-torus meshes and derive a quantitative low-energy finite-cover bound, checking near-exceptional quasi-zero modes.
3. **Microscopic selector:** compute the full anomaly-consistent matter-induced six-flux polarization tensor with reflection and E6 cubic couplings to see whether any six-term design is dynamically selected over the positive-definite six-channel action.
4. **Compact quantum theory:** quantize the **full native link** Hamiltonian with six-term magnetic completion, Gauss constraints and increasing periodic spatial volume, not just the engineered three-angle rotor.
5. **Klein-quadric/photonic bridge:** classify the 15 Pfaffian-certified channel choices under the actual native H27 and orientation symmetries, and design falsifiable optical interference signatures distinguishing two-commutator choices.
