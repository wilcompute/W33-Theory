"""Patch CLASS halofit for scalar-field dark energy.

Bug (public CLASS, background.c ~l.486): a scalar field is split into 'matter' rho - 3p and 'radiation' 3p
("not very meaningful for oscillatory models").  For a slow-rolling dark-energy field (p ~ -rho) halofit then
reads Omega_m ~ Omega_m,true + 4 Omega_phi ~ 3 and Omega_v = 1 - Omega_m - Omega_r ~ 0, and fnu uses the
inflated Omega0_m.  Measured (halofit_check.py): LCDM through the scf path gets P_nl/P_lin = 4.22 at k = 1 h/Mpc,
z = 0, against 5.91 through plain Lambda or a w = -1 fluid; 8.3 vs 19.9 at k = 3.

Fix (halofit.c only; background and perturbations untouched): at each call remove the scalar-field parts from
Omega_m and Omega_r, set Omega_v = 1 - Omega_m - Omega_r, and use w = p_DE / rho_DE with rho_DE, p_DE summed over
scf, Lambda and fluid (the same instantaneous-w approximation CLASS uses for a CPL fluid).  fnu uses the corrected
Omega0_m.
usage: python3 class_halofit_scf_patch.py <class_dir>   (then make class in that dir)"""
import sys

d = sys.argv[1]
f = d + "/external/Halofit/halofit.c"
s = open(f).read()
if "HF_SCF_FIX" in s:
    print("already patched")
    sys.exit(0)
NL = chr(10)

FIX = NL.join([
    "    /* HF_SCF_FIX: undo background.c's split of the scalar field into matter (rho-3p) and radiation (3p) */",
    "    if (pba->has_scf == _TRUE_) {",
    "      double rc_ = pvecback[pba->index_bg_rho_crit];",
    "      double rs_ = pvecback[pba->index_bg_rho_scf], ps_ = pvecback[pba->index_bg_p_scf];",
    "      double rde_ = rs_, pde_ = ps_;",
    "      double Om_r_ = pvecback[pba->index_bg_Omega_r] - 3.*ps_/rc_;",
    "      Omega_m = pvecback[pba->index_bg_Omega_m] - (rs_ - 3.*ps_)/rc_;",
    "      Omega_v = 1. - Omega_m - Om_r_;",
    "      if (pba->has_lambda == _TRUE_) { rde_ += pvecback[pba->index_bg_rho_lambda]; pde_ -= pvecback[pba->index_bg_rho_lambda]; }",
    "      if (pba->has_fld == _TRUE_) { rde_ += pvecback[pba->index_bg_rho_fld]; pde_ += pvecback[pba->index_bg_w_fld]*pvecback[pba->index_bg_rho_fld]; }",
    "      HF_W_LINE",
    "    }",
])

# 1) default branch (w is computed right after Omega_v there): insert after the w_fld call
old1 = "    class_call(background_w_fld(pba,pvecback[pba->index_bg_a],&w,&dw_over_da_fld,&integral_fld), pba->error_message, pfo->error_message);" + NL
assert s.count(old1) == 1, "w_fld call not found"
s = s.replace(old1, old1 + FIX.replace("HF_W_LINE", "w = pde_/rde_;") + NL)

# 2) second Omega_m/Omega_v site (sigma / k_nl integrator; no w there)
old2 = "  Omega_m = pvecback[pba->index_bg_Omega_m];" + NL + "  Omega_v = 1.-pvecback[pba->index_bg_Omega_m]-pvecback[pba->index_bg_Omega_r];" + NL
assert s.count(old2) == 1, "second Omega site not found"
s = s.replace(old2, old2 + FIX.replace("HF_W_LINE", "(void)pde_; (void)rde_;") + NL)

# 3) fnu with the corrected Omega0_m (today's background row)
old3 = "    fnu = pba->Omega0_ncdm_tot/pba->Omega0_m;" + NL
assert s.count(old3) == 1, "fnu line not found"
new3 = NL.join([
    "    {",
    "      double Om0_ = pba->Omega0_m; /* HF_SCF_FIX */",
    "      if (pba->has_scf == _TRUE_) {",
    "        double *row_ = pba->background_table + (pba->bt_size-1)*pba->bg_size;",
    "        Om0_ -= (row_[pba->index_bg_rho_scf] - 3.*row_[pba->index_bg_p_scf])/row_[pba->index_bg_rho_crit];",
    "      }",
    "      fnu = pba->Omega0_ncdm_tot/Om0_;",
    "    }",
]) + NL
s = s.replace(old3, new3)
open(f, "w").write(s)
print("patched", f)
