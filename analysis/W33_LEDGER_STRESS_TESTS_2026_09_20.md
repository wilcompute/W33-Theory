# W33 finite stress tests of *The Law of the Ledger*

This packet tests five precise claims from the Ledger paper on, or immediately next to, the exact W(3,3) carrier. It is a stress test, not a merger of the theories.

## 1. Literal modular character

\`w33_ledger_modular_character_stress_test.py\` implements
\[
\chi(A,B)=\mathrm{Tr}[(\rho\otimes\rho)\Xi_B\Xi_A],\qquad \Xi_R=D_RS_RD_R
\]
with the Ledger dial. W33 itself is a two-qutrit carrier, so a third qutrit is the minimal extension with genuinely overlapping proper regions.

Result: coincident/disjoint windows are real to numerical precision, while overlapping windows have nonzero phase:
\[
\max |\Im\chi|=2.8990782409\times10^{-3},
\qquad
\max |\Im K_{\rm eff}|=1.0153154514\times10^{-3}.
\]
Order reversal conjugates the character and \(\chi(A,A)=\mathrm{rank}(\rho_A)^2\).

Boundary: this does not identify Tomita conjugations with W33 geometric mirrors.

## 2. Mirror-generated symmetry

\`w33_ledger_mirror_group_stress_test.py\` uses the anti-symplectic involution
\[
R=\operatorname{diag}(1,1,-1,-1),\quad R^T\Omega R=-\Omega.
\]
Exact permutation closure on the 40 W33 points gives:
- \(|PSp(4,3)|=25920\);
- 540 mirror conjugates, centralizer 48, 8 fixed projective points each;
- eight mirrors generate order 51840;
- even mirror products generate exactly the 25920 PSp core.

Thus W33 realizes the exact finite pattern \(PSp(4,3)\triangleleft PSp(4,3){:}2\). Boundary: these are geometric anti-symplectic mirrors, not state-dependent Tomita \(J_A\).

## 3. Audit completeness

\`w33_ledger_qutrit_audit_completeness.py\` reconstructs the Appendix A.8 regional-book algebra over exact finite-field arithmetic.

Controls reproduce the paper:
- two qubits: \(4/16\);
- three qubits: \(64/64\).

For three qutrits, across five exact witnesses:
\[
\mathrm{rank}(\mathcal A_1)=31,\qquad
\mathrm{rank}(\mathcal A_2)=649<729,
\]
despite noncommuting regional books of commutator rank 27. Therefore the depth-two implication does not naively lift from the qubit statement to qutrits.

A tested repair succeeds:
\[
\mathrm{rank}(\mathcal A_3)=729/729.
\]
The depth-two deficiency is 80, equal to the 80 point+line vertices of the W33 building; this is recorded only as a numerical resonance.

## 4. Monopoles and \(H^2\)

\`w33_ledger_monopole_cohomology.py\` builds the full W33 clique complex:
\[
(C_0,C_1,C_2,C_3)=(40,240,160,40).
\]
Boundary ranks are \((39,120,40)\) over several fields and Smith data are unit-only, giving
\[
(b_0,b_1,b_2,b_3)=(1,81,0,0),\quad H^2(W33;\mathbb Z)=H^2(W33;\mathbb F_3)=0.
\]
So every closed 2-cochain on this carrier is exact. This supports the Ledger no-monopole step on W33 specifically, because \(H^2=0\). It does not prove \(dF=0\Rightarrow F=dA\) on arbitrary spacetime topology or a nontrivial U(1) bundle.

The underlying W33 homology was prior repo work; this packet adds the Ledger gauge/cohomology interpretation and explicit cochain test.

## 5. Dark-bond no-go

\`w33_ledger_dark_bond_no_go.py\` tests H.4 as written:
\[
H=H_V\otimes I+I\otimes H_R.
\]
Then
\[
U=U_V\otimes U_R,\qquad \rho_V(t)=U_V\rho_V(0)U_V^\dagger,
\]
so the Schmidt spectrum and entropy cannot change. Also
\[
\operatorname{Tr}_R e^{-\beta H}=Z_R e^{-\beta H_V},
\]
hence
\[
-\log\operatorname{Tr}_R e^{-\beta H}=\beta H_V-\log Z_R,
\]
so tracing out R adds only a scalar and cannot induce a new visible operator.

The executable errors are below \(2\times10^{-15}\). A genuine interaction \(gZ_V\otimes Z_R\) is demonstrated as the minimal ordinary escape: it changes entanglement and induces a nonscalar visible effective term, but abandons the no-interaction premise and reopens naturalness/loop analysis.

## Suite verdict

Three finite structural tests pass; two load-bearing Ledger statements require correction:
1. PASS: literal modular-character overlap phase.
2. PASS: mirror double-cover group pattern.
3. CORRECTION: qutrit depth two is incomplete; depth three closes.
4. PASS ON W33 ONLY: \(H^2=0\) removes topological monopole classes on this carrier.
5. NO-GO AS WRITTEN: H.4's product Hamiltonian cannot power a changing dark bond or induce a new visible operator.

Run all five:
\`\`\`bash
python analysis/run_w33_ledger_stress_suite.py
\`\`\`
Aggregate certificate: \`data/PART_LEDGER_STRESS_SUITE.json\`.
