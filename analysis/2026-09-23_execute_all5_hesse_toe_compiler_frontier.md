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

## Gauge selector: 1,179,648 -> 6 -> 2 -> 1 in the frozen physical orientation

The Q8 bridge admitted 1,179,648 equivariant gauges. Full Clifford covariance reduces these to the 3! = 6 assignments of the three C3 characters to the safe center sheets. Requiring beta=0 to carry the trivial character leaves two conjugate survivors: (0,1,2) and (0,2,1).

Real E6 cubic signs and integer Qpsi/matter-parity data cannot distinguish them.

The repository already fixes an oriented physical root gauge:
- the full compiler quotient generator is address z=(0,0,1);
- the physical Clifford dictionary uses normal form Z^a X^b z^c and its distinguished central record has physical coordinate (0,0,1);
- the external-A2 E8 theorem fixes z=Z_FI=exp(2*pi*i Qpsi/3)=omega I in the Pass5727 orientation.

Therefore, relative to that already-frozen orientation, the compiler character assignment is uniquely (0,1,2), with beta mapping to the character z -> omega^beta. The other survivor is exactly the conjugate/opposite-center convention.

Firewall: this is gauge-coordinate closure, not a dynamical proof of spontaneous CP/chirality selection or a heterotic vacuum preference. Reversing the frozen Coxeter orientation reverses the selected assignment.

Evidence: analysis/w33_hesse36_compiler_gauge_selector_audit.py and analysis/w33_hesse36_physical_fi_orientation_selector.py.

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

The finite architecture now separates cleanly into:
1. scheduler/address geometry: regular H27 x C3;
2. instruction compiler: exact full-rank Clifford/Fourier transform on all 270 cubic instructions;
3. operator execution algebra: Pauli243 acting as I9 tensor M9;
4. root basis: cubic incidence sees a 73-dimensional quotient and misses exactly chi_ext + chi_ext^2 + V_omega + V_omega^2.

The remaining 81-root problem is therefore not to discover an arbitrary 81x81 matrix. It is to attach exactly those four missing irreducible sectors to the already-closed 73-dimensional cubic channel, while respecting the frozen FI orientation and the Pauli243 execution algebra.
