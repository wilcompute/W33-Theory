# Four balanced point sources: three spinors, a bulk-cup obstruction, and unresolved physical completion

Date: 2026-11-19. **This is sourced Abelian E8 gauge-sector data and a conditional interaction test, not a compact G2 vacuum or a TOE.**

A balanced directed graph supplies a single charge-conserving SU4 Cartan source matrix of rank three. Its point-defect relative complexes give three chiral Spin10 16s without conjugate16s, five10s and eight charged singlets. Gauge weights permit a formally full-rank charged-family Yukawa texture. However, the strictly defined bulk relative-de-Rham cubic vanishes. Extra Abelian anomalies and SM-preserving D-flat GUT breaking also remain obstacles. We do not turn the formal texture into a mass prediction.

## Prior work and what is actually changed

`2026-11-18_E6_Morse_relative_families.md` already constructs harmonic point sources, the four-negative/one-positive relative index-three example, an explicit lens Green function, and mirror/Wilson/anomaly/Yukawa tests. `2026-11-18_linked_wire_H27_Novikov.md`, `2026-11-18_native_E8_C9_Clifford_link_Higgs_G2_qutrit.md`, and `2026-11-18_E8_full248_LES_Psi3_weakG2_localMUB.md` already explore nonexact flat systems, linked complements and the need to count the whole adjoint rather than one favorable block. We use none of their linked holonomies here.

`2026-11-19_E8_nonproportional_PW_vacuum_gates.md` has an independent supplied polynomial E8 background with net three16s but three conjugate16s, and a specified cubic F/D obstruction. Its noncompact profiles and overlap integrals are different from this point-source construction. Its common-profile parity predecessor is `toe_20261118_E8_H27_wire_index_parity.py`; that producer supplies our independently checked E8 roots. The latest parallel physical-sieve report9d7b6aafb supplies the compact exact-harmonic warning. The construction below explicitly includes sources and therefore does not violate that warning.

The sourced Higgs equations, relative-spectrum dictionary and charge-conserving overlap framework are established in [Braun–Cizel–Hübner–Schäfer-Nameki, sections4.2,5.3,6.2](https://arxiv.org/html/1812.06072). Their discussion distinguishes local perturbative profiles from true massless combinations and allows cancellation among flow trees. Our source matrix, graph classification and strict-cup calculation are applications, not a claim to have invented point-source model building or refuted their full singular theory.

## One globally charge-conserving Cartan background

Choose four distinct supplied points p_j on the round unit S3, for example the four coordinate unit vectors in R4. Let

    Q = [[ 2,-1,-1, 0],
         [-1, 2,-1, 0],
         [ 0,-1, 2,-1],
         [-1, 0, 0, 1]].

Every row sums to zero: each pole carries an actual traceless SU4 Cartan residue. Every column sums to zero: the total source for each eigenprofile vanishes, as required by compact Poisson solvability. The rank is3. Integer traceless diagonal residues lie in the SU4 cocharacter lattice under the standard exponential convention; this does not by itself identify allowed physical ALE defect charges.

Use the already known round-sphere Green function

    G(chi)=(pi-chi)cot(chi)/(4pi²),
    f_i(x)=sum_j Q_ji G(dist(x,p_j)),   phi=diag(df_1,...,df_4).

Away from a pole, Delta G=1/(2pi²). Column neutrality cancels these constants, so each f_i is harmonic there. Row tracelessness gives sum_i f_i=0 identically. The apparent antipodal singularity of the written formula is removable. With A=0, this is an explicit solution of the commuting sourced Abelian Higgs equations away from the four poles. Neither the pole positions, their source action nor a complete ALE-fibered G2 metric is dynamically derived.

## Relative complexes and full charged spectrum

For a nonzero effective profile with m negative and p positive residues, fill any zero-residue pole balls and excise the actual source balls. On S3 minus m+p balls, impose relative conditions on the m negative spheres. The long exact sequence gives

    (b0,b1,b2,b3)=(0,m-1,p-1,0).

In the convention used throughout this repo, b1 counts chiral fields in R and b2 counts conjugate-chiral fields. The formula is standard and depends on the specified operator domains. In particular **a ball with zero residue must be filled in for that sector**. Keeping an artificial absolute hole would add a spurious H2 class. H1 is unchanged by restriction to the common exterior, which we use separately for the cup diagnostic.

The producer builds an actual triangulation: barycentrically subdivide the boundary of a4-simplex, obtaining120 oriented tetrahedra; choose four vertex-disjoint tetrahedra as balls. It constructs each sector's relative coboundary matrices, fills its zero-residue balls, checks d²=0 over integers, and verifies all16 sector Betti vectors over both F101 and F103. The analytic LES proves the free integral groups; the finite-field ranks are independent implementation controls.

Use the standard branching

    248=(45,1)+(1,15)+(16,4)+(16bar,4bar)+(10,6).

The four spinor profiles have residue columns

| Spinor profile | residues | b1 | b2 |
|---|---|---:|---:|
| 16_1 | (2,-1,0,-1) | 1 | 0 |
| 16_2 | (-1,2,-1,0) | 1 | 0 |
| 16_3 | (-1,-1,2,0) | 1 | 0 |
| 16_4 | (0,0,-1,1) | 0 | 0 |

Thus there are three chiral16s and no conjugate16s in this model. For the six vector weights i+j, the b1 counts are1,1,1,0,1,1 in order12,13,14,23,24,34: **five10 fields**. Complementary weights are conjugate; counting b1+b2 again for all six would double count them. The twelve SU4 roots yield **eight charged singlets**. The resulting complex gauge-component count is48+50+8=106. Bulk H1 of the filled S3 vanishes; the unbroken gauge Lie algebra is so10+u1³, dimension48.

An independent control maps the even D3 halfspin weights (1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1) to the four SU4 weights q1=(1,0,0),q2=(0,1,0),q3=(0,0,1),q4=(-1,-1,-1). It evaluates the source profile of every one of the240 E8 roots and reproduces106 and all anomaly tensors directly. This is more than a representation-dimension assignment; it still uses the standard E8 branching rather than constructing a physical chiral compactification from it.

## Why a balanced directed graph appears

Restrict to four nonconstant eigenprofiles and require all conjugate16 counts to vanish. Each column must have exactly one positive residue. For net three16s the number of negative entries is7. A rank-three charge-conserving source matrix needs at least four source points, since its rank is at most N_sources-1.

At the minimal four-source value, row tracelessness forces each row to have one positive entry as well. After permuting rows, positive entries are diagonal and off-diagonal entries are nonpositive. Thus Q is a **balanced weighted directed graph Laplacian**, with7 negative off-diagonal entries and5 zeros. Balance is a statement about residue weights, not a quiver anomaly-cancellation theorem.

Enumerating all C(12,7)=792 unweighted directed supports gives24 balanced rank-three labeled graphs, exactly **one isomorphism class** under simultaneous vertex relabeling. Every member has the three families on distinct weights. Our Q is one representative: it is the sum of an oriented four-cycle and an edge-disjoint oriented triangle. The number7 and the restriction to unit edge weights are imposed design choices; this classification does not predict a physical number of generations.

There is also a support-parity warning. If all four profiles have nonzero residues at every pole, each pole contributes an even signed count across four profiles. The total16 index is then even. Odd index three here relies on zero-residue support strata. Adding a small complete-graph Laplacian turns on the missing poles and changes the count; it is a change of singular domains, not a continuous eigenvalue deformation in a fixed Fredholm problem. Quantized source types might protect the zeros, but that physical protection is not supplied.

## Gauge-allowed full rank versus a vanishing strict bulk cubic

With one family on each weight1,2,3, the SU4 epsilon tensor permits

    16_1 16_2 10_34,   16_1 16_3 10_24,   16_2 16_3 10_14.

All three indicated10 sectors have a chiral mode. The symmetric gauge-allowed flavor matrix is

    Y=[[0,a,b],[a,0,c],[b,c,0]],    detY=2abc.

This escapes the prior star-texture rank-two selection rule **at the gauge-selection level only**. The following test prevents us from declaring full-rank physical masses.

Let M be a rational homology three-sphere with finitely many disjoint balls removed, and let A be any union of boundary spheres. Since H1(M;R)=0, the LES identifies H1(M,A;R) with boundary constants modulo the common constant. Every class has a representative that is a linear combination of d(chi_j), where chi_j is a smooth cutoff equal1 near boundary j and0 outside its collar. Choose disjoint collars. On each collar all such forms are multiples of the same radial dr_j, and elsewhere they vanish. Therefore the wedge of any two of these representatives vanishes pointwise.

It follows that every relative cup pairing

    H1(M,A1) x H1(M,A2) x H1(M,A3) -> H3(M,A1 union A2 union A3)

vanishes. For a gauge-invariant triple with f1+f2+f3=0, untwisting alpha_i=e^(-f_i) a_i cancels all exponentials in the bulk overlap. At each nonzero source at least one of the three residues is negative, so the union of negative boundaries covers the common boundary for our three candidate couplings. Stokes makes the integral invariant under the allowed relative exact changes. On a finite smooth cutoff, if the cubic is precisely this relative product, its value is zero.

The producer independently integrates Alexander–Whitney products of all64 ordered triples of the four boundary vertex-cutoff coboundaries over the oriented116-tetrahedron exterior. Every integral is exactly zero. This is a discrete certificate accompanying the collar proof; it is not a simulation of singular harmonic zero modes.

A further literature cross-check is [Hübner, equation(5.28) and its cohomology discussion](https://arxiv.org/html/2009.07136v2): the complete massless colored-SQM interaction descends to a cup product, whereas individual flow-tree amplitudes are chain-level data. This supports testing the product globally rather than identifying one locally allowed interaction with a nonzero physical Yukawa. It does not itself prove the singular-domain comparison for the present residue matrix.

**Physical scope is essential.** This proves a result about the strict bulk relative-de-Rham model, including its finite-cutoff product and domain assumptions. We have not established that the complete singular gauge/M-theory action has no additional defect or boundary contribution, that the singular-limit product comparison preserves all domains, or that every M2 correction is represented by this strict product. It is therefore an interaction/comparison gate, not a blanket no-go for all point-source Yukawas. A local nonzero gradient-tree contribution alone would not settle the global massless coupling; the full sum and domain comparison must be computed. Nontrivial flat systems, nonfactorized spectral covers, wire complements with absolute H1, or new defect interactions change the hypotheses.

## Anomalies and a separate D-flat obstruction

For the full106-component charged spectrum, the exact traces in the q1,q2,q3 basis are

    Tr Q=(20,10,10),
    Spin10²-Q=(2,1,1),  with T(10)=1, T(16)=2.

The direct E8-root control matches the full cubic tensor as well. If t=(a,b,c) is one surviving Abelian direction, the mixed condition is2a+b+c=0. Substituting a=-(b+c)/2 into Tr(t.Q)³ gives

    (3/2)(b-5c)(b+c)(5b-c).

Thus the individually perturbatively anomaly-free U1 directions, up to rescaling, are(-3,5,1), (0,-1,1), and(-3,1,5). The full two-dimensional mixed-anomaly-free plane still has a nonzero cubic polynomial, so it cannot be retained as an anomaly-free U1² sector without further matter or inflow. This does not construct a Higgs mechanism leaving one of those lines, cancel global anomalies or determine a Green–Schwarz action.

For SM-preserving GUT breaking using only these massless fields, every right-handed-neutrino singlet in the three16s has chi=-5. The10s have no SM singlet and the SU4-root singlets have chi=0. At zero FI, D_chi=-5 sum|N_i|² therefore prohibits nonzero N VEVs alone. New conjugate-spinor/Higgs sectors, higher representations, source modifications or supersymmetry breaking would be substantive additions. Even a zero-mode Abelian D-flat configuration would still need the full pointwise nonlinear sourced Higgs equations.

## Reproduction and next boundary

    python analysis/toe_20261119_balanced_source_E8_cup_gate.py
    python -m pytest --noconftest tests/test_toe_20261119_balanced_source_E8_cup_gate.py -q

The corresponding JSON records residues, every sector, graph enumeration, relative matrices' Betti controls, actual-root anomalies and the conditional cup obstruction. Pole placements and quantized source data are supplied; no complete compactification, viable Higgs vacuum, charged masses or measured coupling prediction follows. This packet improves the mirror-free chiral gauge-sector construction while exposing the next interaction and vacuum gates.
