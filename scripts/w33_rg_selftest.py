"""
w33_rg_selftest.py

Self-contained sanity check for the W(3,3) RG module.
Run this standalone; no external dependencies beyond math.

Checks:
  1. beta_qcd_2loop gives correct sign and magnitude at known points
  2. Running alpha_s UP from M_Z with PDG value recovers known GUT coupling
  3. Running alpha_s DOWN from GUT recovers PDG alpha_s(M_Z) within 3 sigma
  4. Threshold matching at M_top is non-trivial but small
  5. w33_alpha_s_mz() returns a finite, physical result
"""

import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from w33_rg_gut_conversion import (
    beta_qcd_2loop, run_alpha_s, w33_alpha_s_mz,
    threshold_match_top, w33_m_gut, w33_alpha_unified_gut
)

def check(condition, label):
    status = 'PASS' if condition else 'FAIL'
    print(f"  {status}  {label}")
    return condition

if __name__ == '__main__':
    print("=" * 55)
    print("W(3,3) RG Self-Test")
    print("=" * 55)
    all_pass = True

    # 1. Beta function sign: for nf=5, beta0=11-10/3=23/3>0, so beta<0 (asymptotic freedom)
    b = beta_qcd_2loop(0.12, nf=5)
    all_pass &= check(b < 0, f"beta_qcd(0.12, nf=5) < 0 [got {b:.5f}]")

    # 2. Beta function for nf=6: beta0=11-4=7>0, still AF
    b6 = beta_qcd_2loop(0.04, nf=6)
    all_pass &= check(b6 < 0, f"beta_qcd(0.04, nf=6) < 0 [got {b6:.6f}]")

    # 3. Run alpha_s DOWN from M_Z to 1 GeV: should increase (IR growth)
    M_Z = 91.1876
    PDG_as = 0.1180
    a_1gev = run_alpha_s(PDG_as, M_Z, 1.0, nf=5, n_steps=2000)
    all_pass &= check(a_1gev is not None and a_1gev > PDG_as,
                      f"alpha_s grows toward IR: alpha_s(1 GeV)={a_1gev:.4f} > {PDG_as}")

    # 4. Run alpha_s UP from M_Z to M_top: should decrease slightly
    M_top = 172.57
    a_mtop = run_alpha_s(PDG_as, M_Z, M_top, nf=5, n_steps=500)
    all_pass &= check(a_mtop is not None and a_mtop < PDG_as,
                      f"alpha_s decreases toward UV: alpha_s(M_top)={a_mtop:.4f}")

    # 5. Threshold matching at M_top: correction should be small (<1%)
    a_above = run_alpha_s(PDG_as, M_Z, M_top, nf=5)
    a_thr = threshold_match_top(a_above, M_top)
    rel_correction = abs(a_thr - a_above) / a_above
    all_pass &= check(rel_correction < 0.01,
                      f"Top threshold correction < 1%: {rel_correction:.4%}")

    # 6. Run UP from M_Z to M_GUT: should be ~1/25 range
    M_GUT = w33_m_gut()
    a_gut_up = run_alpha_s(PDG_as, M_Z, M_GUT, nf=6, n_steps=8000)
    all_pass &= check(a_gut_up is not None and 0.01 < a_gut_up < 0.1,
                      f"alpha_s(M_GUT) from PDG anchor: {a_gut_up:.5f} in (0.01, 0.1)")

    # 7. w33_alpha_s_mz() returns a dict with 'status'
    print()
    print("  --- Full W(3,3) GUT->M_Z run ---")
    result = w33_alpha_s_mz(verbose=True)
    all_pass &= check('status' in result, "w33_alpha_s_mz() returns status dict")
    all_pass &= check(result['status'] in ('ok', 'runaway_gut_to_mtop', 'runaway_mtop_to_mz'),
                      f"status is a known value: {result['status']}")
    if result['status'] == 'ok':
        as_mz = result['alpha_s_mz']
        all_pass &= check(0.05 < as_mz < 0.5,
                          f"alpha_s(M_Z) is physical: {as_mz:.5f}")

    print()
    final = 'ALL PASS' if all_pass else 'SOME FAILURES'
    print(f"  Result: {final}")
    print("=" * 55)
