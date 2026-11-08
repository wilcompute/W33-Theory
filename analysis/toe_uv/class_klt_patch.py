"""Second-stage patch on top of class_fading_patch.py: the Khoury-Lin-Trodden dark-axion / dark-baryon model (arXiv:2503.16415, 2607.16191) as I read their abstract-level and Eq. (15) summaries:
  dark-matter mass  m(phi) = m0 [1 + 2 s sqrt(1 - xi sin^2(phi/2f))] / (1 + 2 s)   (normalised to 1 at phi = 0), s = sigma_N/m0, xi = 4 m_u m_d/(m_u+m_d)^2 = 0.98765 (m_u = 0.8 m_d, their Appendix B);
  potential         V(phi) = A H0^2 [1 - sqrt(1 - xi sin^2(phi/2f))]   (pion-mass-term axion potential, no constant term: their 'v = 0' case).
Coupling c'(phi) = -d ln m/dphi analytically; dc'/dphi by central finite difference.  The exponential factor is switched off by lambda = scf_parameters[0] = 0.
scf_parameters = 0 (lambda), s, A, f (reduced Planck units), phi_ini, phi'_ini.  scf_tuning_index = 2 (A) as before.
Caveats: my reading of their equations from summaries; finite-density corrections and their exact normalisation are not reproduced; this is a test model in their family, not their code.
usage: python3 class_klt_patch.py path_to_fading_patched_class"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
HELP = """
/* KLT patch helpers */
#define KLT_XI 0.98765432098765
static double klt_root(struct background *pba, double phi) {
  double f = pba->scf_parameters[3]; double sn = sin(0.5 * phi / f);
  return sqrt(1. - KLT_XI * sn * sn);
}
static double klt_mfac(struct background *pba, double phi) {
  double s = pba->scf_parameters[1];
  return (1. + 2. * s * klt_root(pba, phi)) / (1. + 2. * s);
}
static double klt_cp(struct background *pba, double phi) {
  double s = pba->scf_parameters[1], f = pba->scf_parameters[3]; double r = klt_root(pba, phi);
  return s * KLT_XI * sin(phi / f) / (2. * f * r * (1. + 2. * s * r));
}
static double klt_cpp(struct background *pba, double phi) {
  double h = 1e-6 * pba->scf_parameters[3];
  return (klt_cp(pba, phi + h) - klt_cp(pba, phi - h)) / (2. * h);
}
"""
HELP_PERT = HELP
EDITS = {
    "source/background.c": [
        ('#include "background.h"\n', '#include "background.h"\n' + HELP),
        ("exp(-pba->scf_parameters[1]*pvecback_B[pba->index_bi_phi_scf])", "klt_mfac(pba,pvecback_B[pba->index_bi_phi_scf])"),
        ("+2./3.*pba->scf_parameters[1]*3.*pvecback[pba->index_bg_rho_cdm]);", "+2./3.*klt_cp(pba,pvecback_B[pba->index_bi_phi_scf])*3.*pvecback[pba->index_bg_rho_cdm]);"),
        ("+ a*pba->scf_parameters[1]*3.*pvecback[pba->index_bg_rho_cdm]/H;", "+ a*klt_cp(pba,y[pba->index_bi_phi_scf])*3.*pvecback[pba->index_bg_rho_cdm]/H;"),
        ("(void)scf_alpha; (void)scf_B; return scf_A*pba->H0*pba->H0;",
         "(void)scf_alpha; (void)scf_B; return scf_A*pba->H0*pba->H0*(1.-klt_root(pba,phi));"),
        ("(void)scf_alpha; (void)scf_B; return 0.;\n",
         "(void)scf_alpha; (void)scf_B; { double f = pba->scf_parameters[3]; double x = 0.5*phi/f; return pba->scf_parameters[2]*pba->H0*pba->H0*KLT_XI*sin(2.*x)/(4.*f*klt_root(pba,phi)); }\n"),
    ],
    "source/perturbations.c": [
        ('#include "perturbations.h"\n', '#include "perturbations.h"\n' + HELP_PERT),
        ("          dy[pv->index_pt_delta_cdm] += -y[pv->index_pt_theta_cdm] - pba->scf_parameters[1]*y[pv->index_pt_phi_prime_scf];",
         "          dy[pv->index_pt_delta_cdm] += -y[pv->index_pt_theta_cdm] - klt_cp(pba,pvecback[pba->index_bg_phi_scf])*y[pv->index_pt_phi_prime_scf] - klt_cpp(pba,pvecback[pba->index_bg_phi_scf])*pvecback[pba->index_bg_phi_prime_scf]*y[pv->index_pt_phi_scf];"),
        ("          dy[pv->index_pt_theta_cdm] = -(a_prime_over_a - pba->scf_parameters[1]*pvecback[pba->index_bg_phi_prime_scf])*y[pv->index_pt_theta_cdm] - pba->scf_parameters[1]*k2*y[pv->index_pt_phi_scf];",
         "          dy[pv->index_pt_theta_cdm] = -(a_prime_over_a - klt_cp(pba,pvecback[pba->index_bg_phi_scf])*pvecback[pba->index_bg_phi_prime_scf])*y[pv->index_pt_theta_cdm] - klt_cp(pba,pvecback[pba->index_bg_phi_scf])*k2*y[pv->index_pt_phi_scf];"),
        ("        + a2*pba->scf_parameters[1]*3.*pvecback[pba->index_bg_rho_cdm]*y[pv->index_pt_delta_cdm];",
         "        + a2*3.*pvecback[pba->index_bg_rho_cdm]*(klt_cp(pba,pvecback[pba->index_bg_phi_scf])*y[pv->index_pt_delta_cdm] + klt_cpp(pba,pvecback[pba->index_bg_phi_scf])*y[pv->index_pt_phi_scf]);"),
    ],
}
for name, edits in EDITS.items():
    p = root / name
    s = p.read_text()
    for old, new in edits:
        n = s.count(old)
        if old.startswith("(void)scf_alpha; (void)scf_B; return 0.;"):
            # first occurrence is dV_p, second is ddV_p (it enters the dphi equation as a mass term, so it must be right)
            assert n == 2, (name, old[:60], n)
            s = s.replace(old, new, 1)
            s = s.replace(old, "(void)scf_alpha; (void)scf_B; { double f = pba->scf_parameters[3]; double x = 0.5*phi/f; double r = klt_root(pba,phi); return pba->scf_parameters[2]*pba->H0*pba->H0*(KLT_XI*cos(2.*x)/(4.*f*f*r) + KLT_XI*KLT_XI*pow(sin(2.*x),2)/(16.*f*f*r*r*r)); }" + chr(10), 1)
            continue
        assert n == 1, (name, old[:80], n)
        s = s.replace(old, new)
    p.write_text(s)
print("klt patched")
