"""CLASS for Lambda + Casimir + sparse tower, on top of class_fading_patch.py: V = H0^2 (A + Z exp(-lambda phi)), one field.  Z < 0 is net bosons, and A is tuned by the shooting to close the budget.
scf_parameters = lambda, c' (= b), A, Z, phi_ini, phi'_ini; lambda = 4 b.  Z = 0 with c' = 0 is Lambda.  Fraction: f_idm = 1 - f as in class_fraction.py.
usage: python3 class_casimir_patch.py path_to_a_copy_of_class_fading"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
p = root / "source/background.c"
s = p.read_text()
EDITS = [
    ("  return  V_e_scf(pba,phi)*V_p_scf(pba,phi);", "  return pba->H0*pba->H0*(pba->scf_parameters[2] + pba->scf_parameters[3]*exp(-pba->scf_parameters[0]*phi));"),
    ("  return dV_e_scf(pba,phi)*V_p_scf(pba,phi) + V_e_scf(pba,phi)*dV_p_scf(pba,phi);", "  return -pba->scf_parameters[0]*pba->H0*pba->H0*pba->scf_parameters[3]*exp(-pba->scf_parameters[0]*phi);"),
    ("  return ddV_e_scf(pba,phi)*V_p_scf(pba,phi) + 2*dV_e_scf(pba,phi)*dV_p_scf(pba,phi) + V_e_scf(pba,phi)*ddV_p_scf(pba,phi);", "  return pba->scf_parameters[0]*pba->scf_parameters[0]*pba->H0*pba->H0*pba->scf_parameters[3]*exp(-pba->scf_parameters[0]*phi);"),
]
for old, new in EDITS:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
p.write_text(s)
print("patched")
