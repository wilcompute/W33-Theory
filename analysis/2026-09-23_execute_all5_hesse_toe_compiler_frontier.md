# 2026-09-23 — Execute-all-five Hesse/TOE compiler frontier

This packet consolidates the five requested attacks and the two additional exact consequences that emerged while executing them. The key distinction is preserved throughout: the instruction/control compiler closes exactly and invertibly, while the 81-root basis compiler does not close through cubic incidence alone.

## Full physical Clifford-648 extension

The Hesse36 compiler extends to the full physical qutrit Clifford group
G = H27_address : SL(2,3), of order 648.

The ordinary Hesse 36 is the transitive coset action G/H18. The safe carrier splits into three 12-orbits with common stabilizer H54, with H18 normal in H54 and H54/H18 = C3. The quotient generator is literally the address center z=(0,0,1).

Therefore Ind_H18^G(1) is the direct sum over the three C3 characters of Ind_H54^G(chi). The resulting compiler is twelve independent qutrit Fourier transforms, with T36* T36 = 3 I36, rank 36, and 108 nonzero entries. Every 648^2 target group-law relation and all 648 intertwining identities are checked exactly.

Evidence: analysis/w33_hesse36_full_clifford648_fourier_compiler.py and data/w33_hesse36_full_clifford648_fourier_compiler.json.

## Frozen E8 matter-81 lift: exact rank-73 boundary

The frozen E8 matter shell is 81 = 27 frames x 3 external phases, and the 45 tritangents lift to exactly 270 E8 zero-sum cubic triples.

Cubic incidence does not supply an invertible root-basis compiler:
- rank(27x36 ordinary incidence) = 21;
- rank(81x216 ordinary cubic incidence) = 73;
- rank(81x270 full cubic incidence) = 73.

Thus the exact dark complement has dimension eight. Canonical E6 cubic signs and SU(3) epsilon parities are nonzero rephasings of the same support and cannot raise this rank.

Evidence: analysis/w33_hesse36_e8_matter81_root_lift_boundary.py and data/w33_hesse36_e8_matter81_root_lift_boundary.json.

## New result: the dark eight is an exact K-module

Let K = H27_address x C3_external. The 8-dimensional left kernel of the full 81x270 incidence is K-invariant. Exact rational restriction matrices on all 81 group elements give

D8 = chi_ext + chi_ext^2 + V_omega + V_omega^2,

with dimensions 1+1+3+3=8. The first two are the two nontrivial one-dimensional external-C3 characters; the latter two are the conjugate 3-dimensional H27 Schrodinger irreps with trivial external character.

The exact dark-character trace histogram is (-4)^4, (-1)^50, 2^24, 5^2, 8^1.

This turns the root-lift gap from eight unknown directions into a precise representation target. A future invertible 81-root compiler must supply these four sectors.

Firewall: 8 = rank(E8) is only a numerical equality here. No Cartan identification is claimed.

Evidence: analysis/w33_hesse36_e8_matter81_dark8_decomposition.py and data/w33_hesse36_e8_matter81_dark8_decomposition.json.

## Gauge selector: six Fourier assignments, two conjugates, one frozen orientation

The earlier Q8 bridge counted 1,179,648 **objectwise equivariant bijections**.
The full-Clifford construction is a nonobjectwise Fourier intertwiner, so its
six character-to-sheet assignments are a different object type and are not a
subset obtained by reducing that Q8 count.  The complete full-Clifford
intertwiner space has dimension seven.

Inside the induced/Fourier ansatz, the three safe sheets are now certified
objectwise as beta=0,1,2.  Assigning the three C3 characters to those sheets
has 3! = 6 choices.  Requiring beta=0 to carry the trivial character leaves
two conjugate assignments, (0,1,2) and (0,2,1).

Real E6 cubic signs and integer Qpsi/matter-parity data cannot distinguish the
pair.  The repository already fixes an oriented physical root gauge:

- the compiler quotient generator is address z=(0,0,1);
- the physical Clifford dictionary uses normal form Z^a X^b z^c and identifies
  that coordinate as central z;
- the external-A2 E8 theorem fixes z=Z_FI=exp(2*pi*i Qpsi/3)=omega I in the
  Pass5727 orientation.

Relative to that convention, beta maps to the character z -> omega^beta and
the selected assignment is (0,1,2).  Reversing the frozen Coxeter orientation
selects the conjugate assignment.  This is coordinate consistency, not a
dynamical proof of spontaneous chirality or vacuum selection.

Evidence: analysis/w33_hesse36_compiler_gauge_selector_audit.py and
analysis/w33_hesse36_physical_fi_orientation_selector.py.

## Photonic lowering

The exact full-Clifford compiler requires twelve balanced qutrit F3 mixers. The current vendor-neutral demonstrator inventories nine tritters, so the exact resource schedule is 9+3 over two waves.

Every one of the 36 logical channels traverses exactly one active F3. The second wave is temporal resource reuse, not additional Fourier depth.

Repository-owned falsifiers remain |delta V(F3)| <= 0.05 and radial leakage <= 0.10. Insertion loss and tritter process fidelity remain explicitly unmeasured. M36 injection remains refused because this compiler is Clifford-only.

Evidence: analysis/w33_hesse36_photonic_fourier_schedule.py and data/w33_hesse36_photonic_fourier_schedule.json.

## Full 45/270 cubic-instruction lift

The base Hesse split 45=9 fiber+36 ordinary lifts to 270=54 fiber+216 ordinary. The unique large phase-fixed Clifford instruction orbit is the 216 ordinary sector.

The exact instruction compiler is

T270 = I54 direct_sum (T36 tensor I6).

It has rank 270, 702 nonzero entries, and Gram I54 direct_sum 3I216. Scaling the ordinary sector by 1/sqrt(3) gives a unitary instruction compiler.

The four base Pappus components replicate across six phase permutations, producing 24 phase-decorated Pappus controller components.

Evidence: analysis/w33_hesse_pappus_45_270_instruction_compiler.py and data/w33_hesse_pappus_45_270_instruction_compiler.json.

## Current TOE/compiler interpretation

The finite architecture now separates into five exact layers:

1. scheduler/address geometry: the regular K=H27 x C3 action on 81 addresses;
2. instruction compiler: a full-rank Clifford/Fourier transform on all 270
   cubic instructions;
3. root chart: 73 independent cubic modes plus an explicit eight-dimensional
   Fourier/magic complement;
4. representation compiler: an 81 by 81 K-Fourier-coordinate permutation that
   preserves 27 coordinates and minimally retypes 54;
5. operator execution: Pauli243 acting as I9 tensor M9 with multiplicity
   commutant M9 tensor I9.

The remaining matrix problem is concrete: materialize the group-Fourier
analysis/synthesis matrix in the frozen E8 root/address order and compose it
with the minimal permutation and the explicit trinification operator chart.
The remaining physics problem is to realize the 54 representation retypings
and the three-state Qpsi repair through allowed coherent interactions.


## Follow-on closure: dark eight, hybrid 81, and the minimal 54 retypings

The six-dimensional Schrodinger portion of the dark eight is selected by one
exact right-multiplicity qutrit ray.  The four noncentral Hesse projector sums
have stacked rank two and unique common kernel

\[
m=(1,-\omega,0).
\]

For the repository Strange reference \(S=(0,1,-1)\),

\[
m=ZX^2S.
\]

Thus the dark \(V_\omega\) multiplicity ray is a single-qutrit Clifford image
of Strange magic, and the \(V_{\omega^2}\) sector carries its conjugate.  This
is separate from `M36_Q4_RAW`, the ququart/two-qubit Witting resource.

A deterministic complete root/address coordinate basis is

\[
\boxed{81=73_{\rm cubic}+2_{\rm external\ Fourier}
+3_{V_\omega}+3_{V_{\omega^2}}.}
\]

The 73 cubic columns are deterministic pivots of the exact 81 by 270 incidence
matrix.  The eight dark columns are Hermitian-orthogonal to all 270 cubic
columns and have Gram diagonal

\[
81,81,54,54,54,54,54,54.
\]

The resulting 81 by 81 matrix over \(\mathbf Q(\omega)\) has exact rank 81 and
frozen digest
`sha256:d61fb8e8982a5a394d32a112a150896266ef7ecf0ae9e1806087fc36d834c125`.

Comparing irreducible multiplicities with the trinification operator module
gives exact maximum equivariant ranks

\[
73_{\rm visible}\to81_{\rm op}:24,\qquad
8_{\rm dark}\to81_{\rm op}:3,\qquad
81_{\rm full}\to81_{\rm op}:27.
\]

Therefore every invertible compiler must change representation type on at
least

\[
\boxed{81-27=54}
\]

coordinates.  The explicit K-Fourier permutation attains that lower bound:
27 compatible Schrodinger coordinates map equivariantly, while 27 conjugate
Schrodinger and 27 one-dimensional coordinates are retyped.  This closes the
finite Fourier-coordinate conversion problem.  It does not yet provide the
root/address-to-Fourier analysis matrix or a Hamiltonian for the retypings.

The separate 54 fiber-instruction sector is not the same object.  An exact
character comparison gives maximum common equivariant rank 27 and unequal
center traces, so the numerical equality 54=54 cannot be promoted to an
objectwise identification.

Finally, the hybrid 81 chart and its exact field conjugate give a graded E8
block chart

\[
I_{86}\oplus B_{81}\oplus\overline{B}_{81},\qquad 248=86+81+81.
\]

The grade-one rows are anchored to the frozen 81 E8 matter roots and the
grade-two rows to their ordered negatives.  The neutral block remains an
identity chart in the prior E6+A2 grading.  This is a vector-space atlas; the
Chevalley brackets between the three grades still have to be transported
before it is a full Lie-algebra compiler.

Evidence:

- `analysis/w33_hesse36_dark_schrodinger_strange_state.py`
- `analysis/w33_e8_matter81_hybrid_cubic_dark_basis.py`
- `analysis/w33_hybrid81_operator_equivariance_budget.py`
- `analysis/w33_minimal_symmetry_changing_81_compiler.py`
- `analysis/w33_fiber54_vs_equivariance54_no_go.py`
- `analysis/w33_e8_full_graded_hybrid_atlas.py`
