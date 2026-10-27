# Native gauge propagation: an integral audit, a flat-mode obstruction, and a supplied completion

27 October 2026. Exact integer and polynomial calculations, with explicitly identified numerical controls. This packet does not solve the TOE. It advances the dynamics/continuum questions on page 137 of `papers/forty_points/main.pdf` by building and testing a specific link-field model.

## Intake coverage and reproducibility

The GitHub plugin confirmed `wilcompute/W33-Theory`, default branch `master`. GitKraken fetched and fast-forwarded the working checkout to `630df49e8`. The snapshot contains **481 commit subjects** in the calendar window 20 October 00:00 EDT through 28 October 00:00 EDT, frozen in `analysis/2026-10-27_week_commit_subjects.txt`. This includes repeated automatic formula-universe commits and reservations. This is a calendar-week window through the session date, not a rolling 168-hour cutoff.

The paper is **210 pages**, SHA256 `c5b44ee9e447561e4fbb892bb870d2506187e37e35c613a39eaf85af6cf6e19c`. All pages were extracted to scratch; selected sections and their TeX sources were read and page 137 was rendered and inspected. **The requested full reading of every commit patch and every PDF page remains incomplete.** Neither the extraction nor the commit-subject inventory counts as a full reading. No conclusion here is presented as a global audit of that corpus.

Reproduce:

```powershell
python analysis/w33_20261027_native_bloch_face_module.py
python -m pytest -q tests/test_w33_20261027_native_bloch_face_module.py
```

Frozen result: `data/w33_20261027_native_bloch_face_module.json`. The script rebuilds all short cycles, hashes its prior face certificate, computes Smith form, verifies exact finite-field Laurent specializations, and checks physical unitary Bloch momenta separately.

## Prior results used, rather than rediscovered

* `analysis/2026-10-23_native_gq24_css_135_4_4.md` already constructs the native 27-vertex, 135-edge four-period graph, a 105-face basis of zero-period C3/C4/C5 loops, the finite `[[135,4,4]]_3` code, and a noncommuting Gauss-invariant **Z3** Hamiltonian. Those results are not new here.
* `analysis/w33_20261023_native_135_4_4_css.py` is the executable owner of those code parameters; the rediscovery guard points to it, and its complete implementation was read before this packet was written.
* `analysis/w33_20261023_native_zero_holonomy_face_completion.py` owns the census: 45 closed triangles, 189 closed quadrilaterals, 1053 closed pentagons; selected independent face counts 45+56+4. We rebuild these exact values.
* `analysis/w33_pass12189_12193_five_bridges.py` and Pass11991 own the primitive Z4 voltages and scalar acoustic metric G.
* `analysis/w33_20261010_toe38_local_maxwell_2complex.py` already adds **three commutator loops on a different three-period Levi cover**. `analysis/w33_20261013_toe61_full_gauss_audit.py` explains why they are zero chain rows at zero momentum. The six-commutator construction here is the four-period application of that idea, not a new general principle.
* The electric-plus-loop-magnetic Hamiltonian is standard: Kogut–Susskind, [Phys. Rev. D 11, 395 (1975)](https://doi.org/10.1103/PhysRevD.11.395). [Kaplan–Stryker, Phys. Rev. D 102, 094515 (2020)](https://doi.org/10.1103/PhysRevD.102.094515) discusses Gauss constraints in U(1) lattice gauge theory. The repository-specific work below is the exact native map and its spectrum.

## 1. The integral question is settled for the selected finite complex

Collapse a spanning tree with 26 edges. The 109 remaining chord coefficients are integral coordinates on the graph cycle lattice. Restrict the **signed integer**, not mod-three, 105 face boundaries to those coordinates. Its Smith form has exactly **105 unit factors**. Therefore

```
H1(finite selected-face complex; Z) = Z^4, with no torsion.
```

This fills the integral-homology question explicitly left open in the October23 code report. It does not determine the fundamental group or translated-cover homology.

## 2. A one-cell face basis does not complete propagation

For each oriented edge e=(a,b), define D_ea(k)=-1 and D_eb(k)=exp(i k.V_e). For each lifted zero-period loop f, sum the edge fields with the phase of the **running integer deck position**, obtaining F_f(k). The telescoping identity is exactly F(k)D(k)=0. Its numerical residual is checked at the declared real momenta; the integer Laurent specialization also verifies it exactly modulo 101.

The supplied noncompact harmonic Hamiltonian is

```
H = (1/2) sum_e E_e^2 + (1/2) ||F A||^2,
Gauss = D^dag E = 0.
```

This changes the local field from the prior finite Z3 rotor to a continuous noncompact U(1) variable. Code distance does not establish the properties of this new Hamiltonian.

At a generic momentum D has rank27, so link fields modulo gauge have dimension108. A **105-row** curl can constrain at most105 of them. Thus the periodically repeated selected105 model has at least **three exact transverse magnetic flat modes** there. These are not removed by Gauss's law. The generic rank105 is certified by an exact modular specialization and the row-count upper bound.

At k=(0.17,-0.23,0.31,0.11), the all1287 short-face curl has numerical rank106 and still leaves two flat modes. Along the third or fourth coordinate axis, it has numerical rank105 and leaves three. The exact modular witness gives rank106 at z=(2,3,5,7) in F101; this is a **generic lower bound**, not by itself a proof of the generic upper bound106. The selected105 bound already proves that a one-cell independent subset cannot be used as a complete propagating gauge presentation.

## 3. Six literal 16-edge loops remove the generic flat sector

Choose a rooted tree, then four based fundamental loops whose integer periods are the rows of

```
W = [ 0  1  1 -1
     -1  0  1 -1
      0  0  1 -1
      0  0  1  0 ],   det W = 1.
```

Append their six commutators, [li,lj]=li lj li^-1 lj^-1. Every commutator has **16 edge traversals**, returns to the same vertex and integer cell, and is given explicitly in the certificate. Its zero-momentum signed chain vanishes, but its translated Bloch row does not. This is exactly the distinction emphasized by the TOE61 prior audit.

The completed curl has111 rows: selected105 plus six commutators. At z=(2,3,5,7) over F101, exact elimination gives rankD=27, rankF=108 and FD=0. Since rankF<=135-27=108 over the Laurent function field, this proves **generic rank108 exactly**. A nonzero integer Laurent minor modulo101 cannot be the zero polynomial; its restriction to the unit torus is nonzero on a dense open subset. This proves a generic statement, not absence of all exceptional finite momenta.

The numerical controls at all five declared nonzero momenta have no transverse zero eigenvalues. At k=0 there remain four global holonomies, as required by H1=Z4. On five rays, three eigenvalues scale as |k|^2 while the fourth remains separated near 0.013918. Thus the completion removes a specific flat-band obstruction while retaining the long-wavelength holonomies.

## 4. Equal loop coefficients do not give a single cone

Let h=V-B phi be the harmonic representative of the four integer voltage cochains. Its link Gram matrix, already implicit in the scalar calculation, is

```
M = h^T h = 27 G = [10  5 -6  0
                     5 10  0 -6
                    -6  0 12 -6
                     0 -6 -6 12].
```

In the four-dimensional harmonic sector A=h x, the leading commutator flux is i (Wk) wedge (Wx). The short-face block has full rank105 at zero, so optical corrections can cancel its first-order flux. They cannot affect the commutator contribution at that order, because the commutator rows vanish at zero. The effective magnetic quadratic form is therefore

```
K(n) = W^T (|Wn|^2 I - (Wn)(Wn)^T) W.
```

For k=t e1, exact symbolic arithmetic gives

```
det(K(e1)-lambda M) = 2 lambda (9 lambda-1)(162 lambda^2-72 lambda+5).
```

The three transverse squared speeds are

```
(4-sqrt(6))/18, 1/9, (4+sqrt(6))/18
       0.08613946, 0.11111111, 0.35830499.
```

Their agreement with decreasing-t numerical dispersion is checked. Three unequal speeds mean this simple supplied completion does **not** share a single Maxwell cone. The loop and tree choices are additional modeling data. Also, four deck coordinates in a Hamiltonian with external time are **four spatial dimensions plus time**, not the observed 3+1 signature.

## 5. A positive finite-loop coupling can engineer the scalar acoustic cone

There is a useful constructive converse. Write C2(A) for the second compound matrix (the induced metric on exterior two-forms). Supply the positive six-by-six loop-flux coupling

```
H_loop = C2(W^-1)^T C2(M) C2(W^-1) / 27.
```

The exact rational matrix is frozen in the certificate. Sylvester's criterion verifies positivity. A symbolic identity in all four components of n proves

```
K_H(n) = ((n^T M n) M - (Mn)(Mn)^T) / 27.
```

Relative to the electric harmonic Gram M, all three nonzero eigenvalues are now **n^T G n**. Hence this finite-range completion can be made to match the scalar acoustic cone at leading long wavelength. It mixes six fluxes based at the same cell, each supported on a literal finite loop; no dense link-space projection is introduced. Finite-k dispersion need not remain degenerate.

This is an **engineered compatibility witness**, not a selected law of nature. The original equal-loop Hamiltonian fails the common-cone test; a chosen positive area metric repairs it. The missing selection principle now has a precise target: why should the microscopic couplings be this induced area metric? The model also still needs a physically justified reduction to three spatial directions and coupling to matter before any claim about our universe.

## Independent validation and limits

The tests independently walk every commutator through actual vertices and cells, verify period determinant1, reproduce the modular rank witness, and change every vertex's integer cell representative by a seeded random offset. The latter is a different voltage gauge; it preserves the physical transverse spectrum to numerical tolerance. This controls coordinate artifacts rather than merely repeating a stored table.

No full compact-U1 phase diagram, Z3 many-body spectrum, gravity, chirality selection, renormalization, measured constants, or physical device is inferred. In particular, equality of leading classical wave speeds does not establish a quantum continuum limit.

## Five independent next investigations

1. **Microscopic selection:** derive or rule out the induced six-loop area metric from an action with fewer adjustable parameters, instead of fitting its cone.
2. **Physical dimensionality:** test a justified compactification or constraint selecting three of the four spatial periods, including the extra polarization and scalar modes.
3. **Compact quantum dynamics:** study finite-cover U1/Z3 Wilson-loop observables and phase structure, distinguishing the harmonic model from the finite qutrit code.
4. **Matter compatibility:** construct explicit E6/internal-module link couplings and test Gauss invariance, chirality and common limiting speeds.
5. **Independent corpus audit:** finish all 481 historical patches and all210 paper pages, keeping a page/commit coverage ledger and checking these results against each newly read artifact.
