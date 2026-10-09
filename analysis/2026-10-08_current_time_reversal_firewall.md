# Scope correction — dressed antiunitary found

The bare-K noninvariance verified below remains exact, but the proposed Pass11769 Hamiltonian **does possess** a different antiunitary symmetry that exchanges positions and momenta with the bipartition sign matrix D. See `analysis/2026-10-08_dressed_current_antiunitary.md` and `analysis/w33_20261008_dressed_current_antiunitary.py`. Thus do **not** infer intrinsic microscopic T breaking, physical CP or a thermodynamic arrow from the result below. All 160 currents are invariant under the dressed antiunitary.

---

# Canonical time reversal of the Pass11769 current Hamiltonian — exact firewall

Status: proved for ordinary Schrödinger complex-conjugation K only; NOT a classification of all possible antiunitary symmetries or a statement about experimental CP/CPT.

Pass11769 proposes J_e=(V_e.q+a)(U_e.p+a) and H=sum_e J_e^2 on L2(W), where a=1/sqrt(20), U_e=P_W(e_i+e_j), V_e=P_W(e_i-e_j). Because U_e.V_e=0, the two factors in each current commute.

Under the canonical antiunitary K, q stays q and p maps to -p. Thus, exactly as differential operators,

    H - K H K^-1 = 4a sum_e (V_e.q+a)^2 (U_e.p).

This is a nonzero operator: for every ordered pair of distinct W33 points p0,p1, choose a line l0 through p0 but not p1 and a line l1 through p1 but not p0. The existence follows from four lines per point and at most one common line. Set q=a(e_p0-e_p1), p=a(e_l0-e_l1), both in the 78-dimensional projected carrier W.

Every current then has dimensionless factors (1+Q_i) and (1+R_l). The sum of (1+Q_i)^2 on l0 is 7, on l1 it is 3. Consequently the exact classical polynomial/Weyl-symbol difference is

    H(q,p) - H(q,-p) = 4 a^4 (7-3) = 1/25.

The executable verifier builds the actual 160 Levi incidences from Pass11767, checks all 40*39=1560 ordered point pairs with exact integer arithmetic, and obtains this same difference every time. Sample: points (0,1), lines (1,4), integer energy numerators 186 versus 170 at denominator 400.

Connection to the Pass11769 variational state: its displayed two-parameter Gaussian energy obeys E(t,f)-E(t,-f)=1280*b*m*t*f, where b=1/20 and m=(6*sqrt(10)+15)/40. The reported optimum has f<0 and is lower in energy than its canonical-K conjugate; that is compatible with explicit T bias of H, not evidence that an originally T-symmetric law spontaneously chose a time arrow.

Important boundaries: K is the ordinary canonical time reversal, NOT necessarily the finite PGSp anti-symplectic involution. An internally dressed antiunitary may still exist and has not been excluded. The offset a is a supplied representational normalization; its physical choice and transformation law need derivation. This neither predicts observed CP violation nor gives a continuum limit, particle mass, cosmological constant, quantum gap or spacetime dynamics.

Source: analysis/w33_20261008_current_time_reversal_firewall.py; parents: analysis/w33_pass11767_global_current_algebra.py and analysis/w33_pass11769_quantized_current_vacuum.py.
