"""Second-stage patch, applied on top of class_fading_patch.py: the axion-monodromy (D'Amico-Hamill-Kaloper 1605.00996) running coupling.
m_cdm(phi) = m0 sqrt(cos(theta0 + phi Fi) / cos(theta0)),  theta0 = atan(2 c'_0 / Fi),  so  c'(phi) = -d ln m/dphi = (Fi/2) tan(theta0 + phi Fi),  c'(0) = c'_0.
Fi = 1/F (reduced Planck units) is scf_parameters[3] (unused by the fading potential); Fi = 0 recovers the constant-c' fading model exactly (control).
scf_parameters = lambda, c'_0, A, Fi, phi_ini, phi'_ini (CLASS takes the initial conditions from the last two entries).
Perturbations gain the dc'/dphi terms:
   delta_c' += - c' dphi' - c'_phi phi' dphi          (from rho_c' = -(3aH + c' phi') rho_c)
   dphi''   += a^2 3 rho_c (c' delta_c + c'_phi dphi)   (perturbing the force c'(phi) rho_c)
usage: python3 class_monodromy_patch.py path_to_fading_patched_class"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
HELP = """
/* monodromy patch helpers */
static double mono_th0(struct background *pba) { return atan(2. * pba->scf_parameters[1] / pba->scf_parameters[3]); }
static double mono_cp(struct background *pba, double phi) {
  double Fi = pba->scf_parameters[3];
  if (Fi < 1e-12) return pba->scf_parameters[1];
  return 0.5 * Fi * tan(mono_th0(pba) + phi * Fi);
}
static double mono_cpp(struct background *pba, double phi) {
  double Fi = pba->scf_parameters[3];
  if (Fi < 1e-12) return 0.;
  double c = cos(mono_th0(pba) + phi * Fi);
  return 0.5 * Fi * Fi / (c * c);
}
static double mono_mfac(struct background *pba, double phi) {
  double Fi = pba->scf_parameters[3];
  if (Fi < 1e-12) return exp(-pba->scf_parameters[1] * phi);
  return sqrt(cos(mono_th0(pba) + phi * Fi) / cos(mono_th0(pba)));
}
"""
EDITS = {
    "source/background.c": [
        ('#include "background.h"\n', '#include "background.h"\n' + HELP),
        ("exp(-pba->scf_parameters[1]*pvecback_B[pba->index_bi_phi_scf])", "mono_mfac(pba,pvecback_B[pba->index_bi_phi_scf])"),
        ("+2./3.*pba->scf_parameters[1]*3.*pvecback[pba->index_bg_rho_cdm]);", "+2./3.*mono_cp(pba,pvecback_B[pba->index_bi_phi_scf])*3.*pvecback[pba->index_bg_rho_cdm]);"),
        ("+ a*pba->scf_parameters[1]*3.*pvecback[pba->index_bg_rho_cdm]/H;", "+ a*mono_cp(pba,y[pba->index_bi_phi_scf])*3.*pvecback[pba->index_bg_rho_cdm]/H;"),
    ],
    "source/perturbations.c": [
        ('#include "perturbations.h"\n', '#include "perturbations.h"\n' + HELP),
        ("          dy[pv->index_pt_delta_cdm] += -y[pv->index_pt_theta_cdm] - pba->scf_parameters[1]*y[pv->index_pt_phi_prime_scf];",
         "          dy[pv->index_pt_delta_cdm] += -y[pv->index_pt_theta_cdm] - mono_cp(pba,pvecback[pba->index_bg_phi_scf])*y[pv->index_pt_phi_prime_scf] - mono_cpp(pba,pvecback[pba->index_bg_phi_scf])*pvecback[pba->index_bg_phi_prime_scf]*y[pv->index_pt_phi_scf];"),
        ("          dy[pv->index_pt_theta_cdm] = -(a_prime_over_a - pba->scf_parameters[1]*pvecback[pba->index_bg_phi_prime_scf])*y[pv->index_pt_theta_cdm] - pba->scf_parameters[1]*k2*y[pv->index_pt_phi_scf];",
         "          dy[pv->index_pt_theta_cdm] = -(a_prime_over_a - mono_cp(pba,pvecback[pba->index_bg_phi_scf])*pvecback[pba->index_bg_phi_prime_scf])*y[pv->index_pt_theta_cdm] - mono_cp(pba,pvecback[pba->index_bg_phi_scf])*k2*y[pv->index_pt_phi_scf];"),
        ("        + a2*pba->scf_parameters[1]*3.*pvecback[pba->index_bg_rho_cdm]*y[pv->index_pt_delta_cdm];",
         "        + a2*3.*pvecback[pba->index_bg_rho_cdm]*(mono_cp(pba,pvecback[pba->index_bg_phi_scf])*y[pv->index_pt_delta_cdm] + mono_cpp(pba,pvecback[pba->index_bg_phi_scf])*y[pv->index_pt_phi_scf]);"),
    ],
}
for name, edits in EDITS.items():
    p = root / name
    s = p.read_text()
    for old, new in edits:
        assert s.count(old) == 1, (name, old[:80], s.count(old))
        s = s.replace(old, new)
    p.write_text(s)
print("monodromy patched")
