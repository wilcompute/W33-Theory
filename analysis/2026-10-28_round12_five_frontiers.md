# Five independent W33/TOE fronts: exact constraints and finite-grid repair counterchecks

**Research date:** 28 October 2026. **Context:** continuation after commit `449bcd3c5568`. This packet takes the previous five independent next steps as research problems, runs exact finite calculations, and explicitly marks which end goals remain open. It does **not** claim an experimental theory of everything, a derived matter determinant, a Lorentzian theory, a full Brillouin-zone repair with fewer than 12 terms, or a continuum gauge mass gap.

**Reproduction:** `analysis/w33_20261028_round12_five_frontiers.py`; `tests/test_w33_20261028_round12_five_frontiers.py`; `data/w33_20261028_round12_five_frontiers_certificate.json`.

The parallel Pass12340 packet `analysis/PASS12340_CAUSAL_RESPONSE_AND_IDENTIFIABILITY.md` already owns an exact retarded 27-site Kubo susceptibility and the order-three Bloch counterexample. The earlier `analysis/2026-10-28_sixfront_ratio_and_12repair.md` already owns the **12-term, all-unitary-character** repair. Neither is relabeled as newly discovered here.

## 1. Matter-derived magnetic action: exact underdetermination at the E6 response stage

The existing E6 decomposition is
`10_(1,1)+bar5_(-3,1)+1_(5,1)+5_(-2,-2)+bar5_(2,-2)+1_(0,4)`.
The 27 weights give `T=sum(dim_i q_i q_i^T)=diag(120,72)`. If every internal species sees exactly the **same** native 27-site response function `F(z)`, then its quadratic Abelian response is `Pi_ab(z)=F(z)T_ab`. This is a trace factorization, not a computed full magnetic effective action.

To test what the canonical charge assignment alone actually fixes, change the response weight of **only the 10_(1,1) multiplet** from `1` to `1+eta`. The exact trace becomes

```text
T(eta) = [120+10eta   10eta
            10eta  72+10eta].
```

At `eta=1`, the matrix is `[[130,10],[10,82]]`, with a **nonzero** mixed response and diagonal ratio `65/41` rather than `5/3`. This modification does not alter the canonical cubic's charge-neutrality identities. A physical symmetry, common masses or dynamics would be required to fix those response weights; no assertion is made that arbitrary weights arise from a consistent E6 vacuum.

The previously proved reflection sends `H(theta)=H0+theta J` to `H(-theta)`. **Conditional theorem:** if the regulator, functional measure and vacuum preserve that reflection, the *reflection-odd* coefficient theta must vanish within this affine magnetic family. Endpoints theta=±2 are not selected by that unbroken symmetry. An actual fermion determinant, regulator anomaly calculation and vacuum construction remain open. The present calculation **excludes the inference** that the E6 5:3 charge trace alone selects the special three-channel magnetic endpoint.

## 2. How close is the 12-term Bloch repair to minimum?

The certified 12-term repair remains the only presently established **all-unitary-momentum** construction in this line. Rather than assert it optimal, enumerate all **81** cubic-root characters `z_mu=omega^(a_mu)`, `a_mu∈{0,1,2}`, directly using the 105 native faces, six native commutators and existing integer mixing matrix R. Perform all rank computations independently over **both F103 and F109** (both contain primitive cubic roots).

At each prime the histogram is:

```text
rank 105: 1 (identity)
rank 108: 70
rank 107: 10 (five conjugate pairs).
```

The ten exceptional exponent vectors are

```text
(1,1,0,0), (2,2,0,0), (1,1,1,0), (2,2,2,0),
(1,1,0,1), (2,2,0,2), (0,0,2,1), (0,0,1,2),
(1,1,2,1), (2,2,1,2).
```

For all ten, adding **one** of the native six commutator rows (loop 0) raises rank to108; in all ten `a0+a3 !=0 (mod3)`. Therefore a **single** candidate compact loop-difference harmonic

```text
epsilon*[1-cos(f_0(x+e_0+e_3)-f_0(x))]
```

eliminates **every detected cubic-root-grid defect** at these two primes and enters at infrared order k^4.

This **does not prove** one harmonic works over the *continuous* Brillouin torus. In fact, a useful methodological caution emerged at fifth roots: one prime, 101, reports a spurious mixed-rank107 at exponents (4,0,3,3), whereas primes151 and181 both give rank108 for that exact same fifth-root character. Since an authentic cyclotomic rank defect would persist under rational specialization away from exceptional primes and be closed under Galois conjugation, it is unsafe to promote isolated finite-prime rank drops into complex zero modes. The known exact rational cyclotomic witness at `(omega,omega,1,1)` remains valid.

**Definitive exact falsifier found after the finite-grid census.** The parallel Pass12341 global theorem (on current master) proves that the full mixed curl has rank107 precisely when the explicit quadratic \(Q(d)=d^TNd/2\) vanishes, where \(h=z^W\) and \(d=h-1\). Restrict to the subtorus \(z_0=z_3=1\), writing \(z_1=a,z_2=b\); then \(h=(ab,b,b,b)\), and the exact polynomial simplifies to

```text
Q = 5(ab-1)^2 - 10(ab-1)(b-1) + 11(b-1)^2.
```

Choose the **exact unitary** character

```text
z = (1, (-1+2*i*sqrt(30))/11, (1+2*i*sqrt(30))/11, 1).
```

Both nontrivial phases have squared modulus1, their product is -1, and direct SymPy substitution into the committed N matrix gives \(Q=0\) **exactly**. But the candidate's translation factor is \(z_0z_3=1\), so its only added positive cosine has **zero quadratic Bloch stiffness** here. By the independent Pass12341 global rank theorem the mixed curl rank is107, unchanged by the proposed term, while the original six-loop curl rank is108. **The one-term candidate is therefore disproved on the continuous unitary torus.** It remains a useful caution that a complete torsion-grid check is not a global proof.

The proved **12-term** repair survives this counterexample, and its global minimality remains unknown. Smaller multi-term designs may still exist. Exact source control is \(one_term_exact_falsifier()\) in this packet.

## 3. New rigorous whole-flux ground energy interval for the compact 3-rotor

Use the **actual** lifted-loop integer electric Gram:

```text
G = [794 -42 768; -42 22 -52; 768 -52 766].
```

The three leading principal minors of `G-7I` are exactly `787,10041,335`, all positive, so `G>7I`. Any integer flux `m` with Euclidean norm squared at least4 satisfies `m^T Gm>28`. Exhausting the 26 nonzero vectors in `{-1,0,1}^3` proves the **global** shortest nonzero flux norm is **22**, attained only at `(0,±1,0)`.

Let the positive cosine potential be `V=sum_a w_a(1-cos(q_a.theta))`. Its exact summed coefficient is `W=7009/28125`. Decompose the complete infinite electric-flux Hilbert space into `P=|0><0|` and `Q=I-P`. Then

```text
PHP=W,
QHQ >= 11*g²*Q,
||QHP||² = 1/2 sum_a w_a²
          = 297803260427/44651250000000.
```

The last identity uses the nine distinct non-opposite integer harmonic charges in the existing compact potential. By Cauchy-Schwarz and the min-max principle, the full three-rotor ground energy is bounded exactly by

```text
( W+11g²-sqrt((W-11g²)²+4||QHP||²) ) / 2
    <= E0 <= W.
```

At the supplied coupling `g=1/5`, this gives the **genuinely analytic, infinite-flux** interval

```text
0.219026376... <= E0 <= 0.249208888888...
```

with no unverified finite-box eigenvalue premise. It is weaker than an earlier informal numerical estimate but more rigorous. This is **not** an infinite-*spatial-volume* lattice gauge mass-gap theorem; it concerns the three-mode quantum mechanical rotor, whose Hamiltonian itself is an engineered choice.

Reference for the general Hamiltonian lattice-gauge rotor approach: Kogut and Susskind, *Phys. Rev. D* 11,395 (1975), https://doi.org/10.1103/PhysRevD.11.395.

## 4. The 3D reflection-even lattice has a nontrivial Z2 glue

The native integer period reflection is

```text
REF=[-1 0 0 0; 1 1 0 0; -1 0 1 0; 0 0 0 1].
```

Its eigenlattice with eigenvalue +1 is spanned by `e1,e2,e3`, while its primitive -1 generator is `v_-=(2,-1,1,0)`. Stack these integral vectors into the columns of E: `det E=-2`. The native metric diagonalizes into an even 3x3 Gram with determinant648 and odd norm18, but the **integral** eigensublattices have index two:

```text
Z^4/(Lambda_even + Lambda_odd) ~= Z/2.
```

The missing coset is the lattice charge-parity information associated with an odd original first coordinate. Therefore a naive real-vector decomposition cannot be interpreted automatically as an integer compactification. A complete orbifold / boundary model must handle the Z2 glue, possible twisted sectors, gauge flux, fermionic boundary conditions and anomalies. No claim is made that twisted particles or spacetime emerge.

## 5. Stronger H4–E6 intertwiner falsifier; a basis-invariant replacement for 5:3

Known Coxeter orders are `|W(H4)|=14400`, `|W(E6)|=51840`. The first does **not** divide the second, nor does the rotation subgroup order7200. By Lagrange's theorem, neither group embeds faithfully into W(E6). Furthermore a direct **isometric root-subsystem** embedding is impossible because a simple H4 order-five bond has normalized product `-cos(pi/5)` (irrational), whereas E6 crystallographic equal-length root inner products are rational.

Thus the root-count identity `120/72=5/3` cannot be explained as a direct Weyl subgroup or isometric root-subsystem inclusion. This does **not** preclude E8-mediated icosian projections, representation correspondences, or nonfaithful maps; any such construction must specify the actual maps.

For the two-U1 E6 quadratic trace `diag(120,72)`, the raw diagonal ratio 5/3 is basis-dependent. The canonical primitive rebasis `U=[[1,0],[1,1]]` gives `[[120,120],[120,192]]`. A **genuine GL(2,Z) invariant** is the determinant `8640` and Smith normal-form invariants `(24,360)`, rather than a chosen diagonal ratio. No connection between these invariant factors and H4 is proved.

References: Coxeter finite group orders and H4 noncrystallographic roots https://www.math.wm.edu/~vinroot/involmodelcox.pdf ; https://arxiv.org/abs/hep-th/0510191 ; E6 order/root count standard Lie/root tables.

## Next independent research directions

1. Derive the complete parity-respecting E6 fermionic polarization tensor with the actual native 27-site Weyl/cubic overlap operator, including a real fermionic mass/vacuum specification.
2. Classify the exceptional complex Bloch characters by exact Laurent Gröbner/saturation, and either *prove* the one-cosine candidate globally sufficient or construct an explicit missing momentum.
3. Improve the analytic 3-rotor bound by projecting onto the six shortest nonzero flux vectors and deriving a certified second-stage Feshbach estimate; then study increasing **spatial** volume.
4. Construct the explicit Z2-glued parity orbifold cell, compute its homology, and test fermionic consistency and mode counting, without assuming Lorentzian time.
5. Search E8 icosian projection/representation bridges with a **fixed invariant trace pairing** and test the Smith invariants (24,360) and root-order obstructions as falsifiers.
