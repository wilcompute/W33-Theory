# TOE52 — H27-equivariant W33-to-K81 carrier minimality and Bloch reciprocity

Date: 13 October 2026. Baseline W33 TOE51 commit 4a7898e4b2961b19c88fe01b7218c3215c65e928; Holotrade b0264880d7c5fd24c6af932b892324247ab57808. Both had no additional commits at the start of this research pass. The project already has TOE47 even-Weil 25D cusp projectors, TOE50 dual 1+24+15 W33 40-line identity, TOE51 Sp4 covariance (but NO constructed K81 embedding), and Holotrade's 2026-09-26 three K81 carrier regular decomposition. This pass resolves the **restricted abstract H27 module bridge**, NOT K81×C3 or Sp4 equivariance, photonic hardware or a theory of everything.

## A. A minimum-carrier theorem with explicit construction

### Construct the Heisenberg action on W33 lines

Use symplectic coordinates (e1,e2,f1,f2) over F3, standard form pairing ei and fi. The matrices

    M(a,b,c) =
      [1 a c  b]
      [0 1 b  0]
      [0 0 1  0]
      [0 0 -a 1] mod 3,

for a,b,c in F3 form an order-27 nonabelian exponent-three Heisenberg group with center of order3. Symplectic preservation and all group products were independently checked with modular matrix arithmetic. Its action on the 40 **native W33 isotropic lines** has orbit decomposition

    40 = 9+9+9+9+1+1+1+1.

Thus the 40-dimensional permutation module has EIGHT independent H27-invariant orbit-constant vectors. Under the existing exact W33 spectral projector resolution 40=1+24+15, these invariants split

    8 = 1 + 4 + 3.

Therefore invariant multiplicities of the spread P15, cusp P0+P24 and full line representation are 3, 5 and 8 respectively.

### Why one K81 cannot hold the full line module H27-equivariantly

Holotrade previously constructed each 81D K81 carrier as Reg(H27) tensor Reg(C3). Restricted to H27 this is **three copies of its 27D regular representation**. Each copy of the regular H27 representation contains one invariant vector; hence each K81 carrier has exactly three.

An injective H27-equivariant map must inject the domain's invariant subspace into the target's invariant subspace. Thus any embedding of the 15D spread, 25D cusp and complete 40D line modules must use, respectively, at least

    ceil(3/3)=1, ceil(5/3)=2, ceil(8/3)=3

separate K81 carriers. This immediately obstructs a one-slice 40→81 H27-equivariant isometry although 81>40.

### Construct integer intertwiners, then make them isometric

Write S_g for the 40-line permutation action and L_g for the 27-element regular left action. For each target comprising k×81 dimensions, the H27 representation is 3k copies of L_g. Begin with a fixed seeded integer matrix C (values -2,...,2). The **unnormalized Reynolds intertwiner**

    A = sum_{g in H27} T_g C (S_g)^(-1)

is an EXACT integer matrix, and satisfies T_h A=A S_h for every h. Restrict to the spread and cusp projectors using exact integer numerators:

    24 P15 = 8 I - 4 A_line + J,
    24 P25 = 16 I + 4 A_line - J.

Check ranks over the field F101 by modular Gaussian elimination. Nonzero minors modulo101 prove nonzero INTEGER minors, hence genuine rank lower bounds in characteristic zero:

| Available 81D carriers | Target dimension | Full W33 40 rank | Even cusp25 rank | Spread15 rank |
|---:|---:|---:|---:|---:|
| 1 | 81 | 35 | 23 | 15 |
| 2 | 162 | 38 | 25 | 15 |
| 3 | 243 | 40 | 25 | 15 |

These integer-certified ranks meet the invariant-count lower bounds. Consequently **one, two, three K81 carriers are both necessary AND sufficient for injective H27 maps of the spread15, cusp25 and complete line40 modules under the stated actions**.

To obtain isometries, restrict A to an orthonormal source sector basis U and form the polar factor

    F = A U [(A U)^T A U]^(-1/2).

Because the positive source Gram commutes with its H27 representation, F remains equivariant. All 27 group elements were tested; maximum covariance residual for each of the 15→81, 25→162 and 40→243 is below 1e-14, as is isometry error. A separate seeded 81×40 Reynolds matrix illustrates the failures: its full-line rank is35, cusp25 rank23, but spread15 rank15.

The explicit integer producer is analysis/w33_20261013_toe52_h27_bridge.py. Frozen machine certificate is data/w33_20261013_toe52_h27_K81_minimal_slices.json.

**Interpretation:** The existing Holotrade 243D frame bundle has *exactly the minimum three K81 slices* for an H27-equivariant encoding of the complete 40-line W33 representation. The 1+24+15 decomposition also has a tiered 15/25/40 minimum-slice structure. The existing bundle/slices and W33 projectors were previously known; the H27 restriction, sharp lower bound and attaining explicit integer intertwiners are the new synthesis.

**Physical boundary:** The isomorphism between the selected W33 unipotent H27 and Holotrade's regular frame H27 has been chosen as an abstract Heisenberg group isomorphism. It is not yet proven to be the natural physical frame map. Additional K81 external C3 action, mu12 clock and full Sp4(3) action have NOT been intertwined. Nothing here constructs an interferometer, a magic-state protocol, or an E6/SM dynamical model.

## B. Opposite Bloch momenta cannot improve spectral identifiability rank

The native W33 real-link Maxwell magnetic map satisfies P(-k)=complex-conjugate(P(k)). With positive REAL electric weights, its generalized magnetic operator M(k)=W^(-1/2) P(k)^dag P(k) W^(-1/2) obeys M(-k)=conjugate(M(k)). Thus for every positive w,

    T_n(-k)=Tr[M(-k)^n]=Tr[M(k)^n]=T_n(k),

and all derivatives with respect to real w_e coincide at +/-k. The source analysis/w33_20261013_toe52_bloch_reciprocity.py verified complex conjugacy at three nontrivial Bloch vectors, and ranks of nine first-three trace-moment gradients versus eighteen at the same vectors and their negatives were both **nine**. Certificate: data/w33_20261013_toe52_bloch_reciprocity.json.

In finite spectroscopy, opposite momenta can average independent measurement noise but ADD NO independent sensitivity to real link weights through reciprocal trace moments alone. Non-opposite k vectors, odd-in-k phase-sensitive observables, or genuinely nonreciprocal physics are needed. This is a restricted reciprocity theorem, not a claim about broken-time-reversal media.

## Reproducibility and prior art

Run:

    py -3 -m pytest -q tests/test_w33_20261013_toe52_h27_minimal_carriers.py tests/test_w33_20261013_toe50_spectral_and_dual_decoder.py tests/test_w33_20261013_toe51_five_fronts.py

The first test reruns both producers, reconstructs all 27 finite group elements, checks exact F101 ranks, the invariant count, three polar equivariant isometries and Bloch reciprocity. Pre-existing strong CP, Maxwell, and lepton sector claims are NOT completed by these algebraic maps. Relevant context: classical symplectic generalized quadrangles and extraspecial Heisenberg groups have a long mathematical history; Holotrade's K81 3-carrier note dated 26 September 2026 is established repository prior work.

## Five independent next steps

1. **Canonical cross-repo generator match:** identify W33's unipotent H27 with Holotrade's 27-frame torsor using actual labeled group generators and state transformations, not only abstract group isomorphism.
2. **Extend the external K81 clock:** test central C3 and the physical mu12 phases on the three isometries. Establish full K81 equivariance or compute a simultaneous-character obstruction.
3. **Compile a physical 15→81 optical readout:** synthesize the polar interferometer, control loss/phase calibration and estimate detector power and sample budget.
4. **Optimize nonredundant inverse spectroscopy:** avoid +/-k duplicate moments; maximize the whitened singular floor over k and spectral quantities to recover microscopic link defects under calibrated noise.
5. **Physical TOE synthesis gate:** one common anomaly-consistent gauge and gravitational action, dynamical vacuum and falsifiable SM predictions must connect the currently separate K81, fermion, gravity and strong-CP constructions.
