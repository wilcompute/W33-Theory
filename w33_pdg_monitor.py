"""
W(3,3) PDG Monitoring Daemon
Continuously verifies the absolute W(3,3) combinatorial bounds against phenomenological 
envelopes (e.g., PDG values). Can be hooked into automated CI or an MCP server.
"""

import math
import sys
from w33.phenomenology import *
from w33.cosmology import *
from w33.clay_math import *

PDG_TARGETS = {
    "m_p_over_m_e": {"measured": 1836.15267, "error_margin": 1.0},
    "Gamma_W_over_M_W": {"measured": 0.0259396, "error_margin": 0.0005},
    "Lambda_QCD_mass_gap": {"measured": 1710, "error_margin": 150}, # MeV (0++ glueball lattice)
    "tensor_to_scalar_r": {"target_ceiling": 0.036}, 
}

def verify_structural_integrity():
    print("========================================")
    print(" W(3,3) TOPOLOGICAL INTEGRITY MONITOR   ")
    print("========================================")
    
    passed = True
    
    # 1. Proton / Electron Ratio
    m_p_e = get_proton_electron_ratio()
    delta_mpe = abs(m_p_e - PDG_TARGETS["m_p_over_m_e"]["measured"])
    status = "PASS" if delta_mpe < PDG_TARGETS["m_p_over_m_e"]["error_margin"] else "FAIL"
    print(f"[{status}] Proton/Electron : {m_p_e} (Target: {PDG_TARGETS['m_p_over_m_e']['measured']})")
    if status == "FAIL": passed = False
        
    # 2. W-Boson decay
    w_decay = get_w_boson_decay_fraction()
    delta_w = abs(w_decay - PDG_TARGETS["Gamma_W_over_M_W"]["measured"])
    status = "PASS" if delta_w < PDG_TARGETS["Gamma_W_over_M_W"]["error_margin"] else "FAIL"
    print(f"[{status}] W-Boson Decay   : {w_decay:.6f} (Target: {PDG_TARGETS['Gamma_W_over_M_W']['measured']})")
    if status == "FAIL": passed = False

    # 3. YM Mass Gap
    ym_gap = get_yang_mills_mass_gap()
    delta_ym = abs(ym_gap - PDG_TARGETS["Lambda_QCD_mass_gap"]["measured"])
    status = "PASS" if delta_ym < PDG_TARGETS["Lambda_QCD_mass_gap"]["error_margin"] else "FAIL"
    print(f"[{status}] YM Mass Gap     : {ym_gap:.1f} MeV (Lattice: {PDG_TARGETS['Lambda_QCD_mass_gap']['measured']} MeV)")
    if status == "FAIL": passed = False

    # 4. Cosmology Tensor-to-scalar
    r = get_tensor_to_scalar_ratio()
    status = "PASS" if r < PDG_TARGETS["tensor_to_scalar_r"]["target_ceiling"] else "FAIL"
    print(f"[{status}] Primordial r    : {r:.4f} (Ceiling: {PDG_TARGETS['tensor_to_scalar_r']['target_ceiling']})")
    if status == "FAIL": passed = False

    print("========================================")
    if passed:
        print("STATUS: SECURE. No parameters have been broken.")
        sys.exit(0)
    else:
        print("STATUS: CRITICAL DRIFT DETECTED. Substrate bounds violated.")
        sys.exit(1)

if __name__ == "__main__":
    verify_structural_integrity()
