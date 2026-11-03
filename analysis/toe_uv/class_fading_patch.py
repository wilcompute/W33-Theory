"""Patch CLASS v3.3.1 (commit 5668031) for the fading dark sector: V = A H0^2 exp(-lambda phi) (A dimensionless because the shooting tolerance of CLASS is absolute), m_cdm = m0 exp(-c' phi), reduced Planck units, phi = phi' = 0 deep in the radiation era.
scf_parameters = lambda, c', A, phi_ini, phi'_ini; scf_tuning_index = 2; omega_cdm is the value at phi = 0; gauge stays synchronous, where CLASS's Klein-Gordon equation is complete (its Newtonian form omits the psi terms).
Synchronous gauge, residual freedom fixed by theta_cdm(ini) = 0.  CDM no longer stays comoving because of the fifth force, so theta_cdm is evolved:
    delta_c' = -theta_c - h'/2 - c' dphi'
    theta_c' = -(aH - c' phi') theta_c - c' k^2 dphi
    dphi''   = -2 aH dphi' - (h'/2) phi' - (k^2 + a^2 V'') dphi + a^2 c' rho_c delta_c
    phi''    = -2 aH phi' - a^2 V' + a^2 c' rho_c,   rho_c' = -(3 aH + c' phi') rho_c
Momentum is conserved between CDM and the field by construction: d(rho_c theta_c)/dtau has the exchange term -c' rho_c k^2 dphi, the opposite of the one in d(k^2 phi' dphi / a^2)/dtau.
CLASS rho is rho/(3 M_Pl^2), hence the factor 3 next to rho_cdm.  The budget closes by H(today) = H0, not by a target Omega_scf.
usage: python3 class_fading_patch.py path_to_class_public"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
EDITS = {
    "source/background.c": [
        ("pvecback[pba->index_bg_rho_cdm] = pba->Omega0_cdm * pow(pba->H0,2) / pow(a,3);",
         "pvecback[pba->index_bg_rho_cdm] = pba->Omega0_cdm * pow(pba->H0,2) / pow(a,3) * ((pba->has_scf == _TRUE_) ? exp(-pba->scf_parameters[1]*pvecback_B[pba->index_bi_phi_scf]) : 1.);"),
        ("(-pvecback[pba->index_bg_phi_prime_scf]*pvecback[pba->index_bg_H]/a-2./3.*pvecback[pba->index_bg_dV_scf]);",
         "(-pvecback[pba->index_bg_phi_prime_scf]*pvecback[pba->index_bg_H]/a-2./3.*pvecback[pba->index_bg_dV_scf]+2./3.*pba->scf_parameters[1]*3.*pvecback[pba->index_bg_rho_cdm]);"),
        ("dy[pba->index_bi_phi_prime_scf] = - 2*y[pba->index_bi_phi_prime_scf] - a*dV_scf(pba,y[pba->index_bi_phi_scf])/H ;",
         "dy[pba->index_bi_phi_prime_scf] = - 2*y[pba->index_bi_phi_prime_scf] - a*dV_scf(pba,y[pba->index_bi_phi_scf])/H + a*pba->scf_parameters[1]*3.*pvecback[pba->index_bg_rho_cdm]/H;"),
        ("return  pow(phi - scf_B,  scf_alpha) +  scf_A;", "(void)scf_alpha; (void)scf_B; return scf_A*pba->H0*pba->H0;"),
        ("return   scf_alpha*pow(phi -  scf_B,  scf_alpha - 1);", "(void)scf_alpha; (void)scf_B; return 0.;"),
        ("return  scf_alpha*(scf_alpha - 1.)*pow(phi -  scf_B,  scf_alpha - 2);", "(void)scf_alpha; (void)scf_B; return 0.;"),
    ],
    "source/input.c": [
        ("output[i] = ba.background_table[(ba.bt_size-1)*ba.bg_size+ba.index_bg_rho_scf]/(ba.H0*ba.H0)-ba.Omega0_scf;",
         "output[i] = ba.background_table[(ba.bt_size-1)*ba.bg_size+ba.index_bg_rho_tot]/(ba.H0*ba.H0)-1.+ba.Omega0_k;"),
        ("/* Default: take the passed value as xguess and set dxdy to 1. */",
         "/* fading patch: V0 = 3 Omega H0^2 */ xguess[index_guess] = 3.15*ba.Omega0_scf; dxdy[index_guess] = 3.; break;"),
    ],
    "source/perturbations.c": [
        ("class_define_index(ppv->index_pt_theta_cdm,pba->has_cdm && (ppt->gauge == newtonian),index_pt,1);",
         "class_define_index(ppv->index_pt_theta_cdm,pba->has_cdm && ((ppt->gauge == newtonian) || (pba->has_scf == _TRUE_)),index_pt,1);"),
        ("        if (ppt->gauge == newtonian) {\n          ppv->y[ppv->index_pt_theta_cdm] =",
         "        if ((ppt->gauge == newtonian) || (pba->has_scf == _TRUE_)) {\n          ppv->y[ppv->index_pt_theta_cdm] ="),
        ("      if (ppt->gauge == newtonian)\n        ppw->rho_plus_p_theta = ppw->rho_plus_p_theta + ppw->pvecback[pba->index_bg_rho_cdm]",
         "      if ((ppt->gauge == newtonian) || (pba->has_scf == _TRUE_))\n        ppw->rho_plus_p_theta = ppw->rho_plus_p_theta + ppw->pvecback[pba->index_bg_rho_cdm]"),
        ("        if (ppt->gauge == newtonian)\n          rho_plus_p_theta_m += ppw->pvecback[pba->index_bg_rho_cdm]",
         "        if ((ppt->gauge == newtonian) || (pba->has_scf == _TRUE_))\n          rho_plus_p_theta_m += ppw->pvecback[pba->index_bg_rho_cdm]"),
        ("      if (ppt->gauge == synchronous) {\n        theta_cdm = 0.;\n      }",
         "      if ((ppt->gauge == synchronous) && (pba->has_scf != _TRUE_)) {\n        theta_cdm = 0.;\n      }"),
        ("        dy[pv->index_pt_delta_cdm] = -metric_continuity; /* cdm density */",
         "        dy[pv->index_pt_delta_cdm] = -metric_continuity; /* cdm density */\n"
         "        if (pba->has_scf == _TRUE_) {\n"
         "          dy[pv->index_pt_delta_cdm] += -y[pv->index_pt_theta_cdm] - pba->scf_parameters[1]*y[pv->index_pt_phi_prime_scf];\n"
         "          dy[pv->index_pt_theta_cdm] = -(a_prime_over_a - pba->scf_parameters[1]*pvecback[pba->index_bg_phi_prime_scf])*y[pv->index_pt_theta_cdm] - pba->scf_parameters[1]*k2*y[pv->index_pt_phi_scf];\n"
         "        }"),
        ("        - (k2 + a2*pvecback[pba->index_bg_ddV_scf])*y[pv->index_pt_phi_scf]; //checked",
         "        - (k2 + a2*pvecback[pba->index_bg_ddV_scf])*y[pv->index_pt_phi_scf] //checked\n"
         "        + a2*pba->scf_parameters[1]*3.*pvecback[pba->index_bg_rho_cdm]*y[pv->index_pt_delta_cdm];"),
        # diagnostic columns, for the Einstein trace-equation control in class_controls.py
        ('class_store_columntitle(ppt->scalar_titles,"phi",_TRUE_);',
         'class_store_columntitle(ppt->scalar_titles,"phi",_TRUE_); class_store_columntitle(ppt->scalar_titles,"h_prime",_TRUE_); class_store_columntitle(ppt->scalar_titles,"h_prime_prime",_TRUE_);'),
        ("class_store_double(dataptr, phi, _TRUE_, storeidx);",
         "class_store_double(dataptr, phi, _TRUE_, storeidx); class_store_double(dataptr, ppw->pvecmetric[ppw->index_mt_h_prime], _TRUE_, storeidx); class_store_double(dataptr, ppw->pvecmetric[ppw->index_mt_h_prime_prime], _TRUE_, storeidx);"),
    ],
}
for name, edits in EDITS.items():
    p = root / name
    s = p.read_text()
    for old, new in edits:
        assert s.count(old) == 1, (name, old, s.count(old))
        s = s.replace(old, new)
    p.write_text(s)
print("patched")
