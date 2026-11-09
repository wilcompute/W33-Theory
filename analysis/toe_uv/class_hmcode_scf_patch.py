"""Patch CLASS HMcode for scalar-field dark energy: a second, independent nonlinear model for the halofit fix.
Apply to a copy of the UNPATCHED build (not on top of class_halofit_scf_patch.py: step 1 corrects Omega0_m globally, which the
halofit patch's f_nu fix would then subtract twice).  Use with non_linear=hmcode only.

Same root cause as class_halofit_scf_patch.py (background.c files the field under matter rho-3p and radiation 3p).  HMcode reads it in
three places, and also takes its dark-energy parameters from Lambda and the fluid only (Omega_v = Omega0_lambda, Omega_w = Omega0_fld,
w0/wa = fluid values), so for a scalar field it integrates growth in an Omega_m = 1 universe.
  1. background.c: Omega0_m, Omega0_r without the field's parts; Omega0_de = 1 - Omega0_m - Omega0_r - Omega0_k.
  2. hmcode.c: Omega_m(tau) without the field's matter part.
  4. hmcode.c: lift the stock guard 'Cannot use scalar field scf with HMcode (not yet coded)'.
  3. hmcode.c: Omega_w = Omega_scf today; w0 = w_scf(a=1); wa = 2 [w_scf(a=1/2) - w0] (CPL through the field's w at a = 1 and 1/2).
usage: python3 class_hmcode_scf_patch.py <class_dir>   (then make class)"""
import sys

d = sys.argv[1]
NL = chr(10)

f = d + "/source/background.c"
s = open(f).read()
if "HM_SCF_FIX" not in s:
    old = "  pba->Omega0_de = 1. - (pba->Omega0_m + pba->Omega0_r + pba->Omega0_k);" + NL
    assert s.count(old) == 1
    new = old + NL.join([
        "  if (pba->has_scf == _TRUE_) { /* HM_SCF_FIX: undo the scf split into matter (rho-3p) and radiation (3p) for today's Omegas */",
        "    double *row_ = pba->background_table + (pba->bt_size-1)*pba->bg_size;",
        "    double rc_ = row_[pba->index_bg_rho_crit], rs_ = row_[pba->index_bg_rho_scf], ps_ = row_[pba->index_bg_p_scf];",
        "    pba->Omega0_m -= (rs_ - 3.*ps_)/rc_;",
        "    pba->Omega0_r -= 3.*ps_/rc_;",
        "    pba->Omega0_de = 1. - (pba->Omega0_m + pba->Omega0_r + pba->Omega0_k);",
        "  }",
    ]) + NL
    s = s.replace(old, new)
    open(f, "w").write(s)

f = d + "/external/HMcode/hmcode.c"
s = open(f).read()
if "HM_SCF_FIX" not in s:
    old2 = "  Omega_m = pvecback[pba->index_bg_Omega_m];//TBC"
    assert s.count(old2) == 1
    i = s.index(old2)
    j = s.index(NL, i) + 1
    s = s[:j] + NL.join([
        "  if (pba->has_scf == _TRUE_) /* HM_SCF_FIX */",
        "    Omega_m -= (pvecback[pba->index_bg_rho_scf] - 3.*pvecback[pba->index_bg_p_scf])/pvecback[pba->index_bg_rho_crit];",
    ]) + NL + s[j:]
    old3 = "  phg->wa = pba->wa_fld;" + NL
    assert s.count(old3) == 1
    s = s.replace(old3, old3 + NL.join([
        "  if (pba->has_scf == _TRUE_) { /* HM_SCF_FIX: the field is the dark energy */",
        "    double *row_ = pba->background_table + (pba->bt_size-1)*pba->bg_size;",
        "    double tau_h_, *bv_, w1_, wh_;",
        "    int li_ = 0;",
        "    phg->Omega_w = row_[pba->index_bg_rho_scf]/row_[pba->index_bg_rho_crit];",
        "    w1_ = row_[pba->index_bg_p_scf]/row_[pba->index_bg_rho_scf];",
        "    class_alloc(bv_, pba->bg_size*sizeof(double), pfo->error_message);",
        "    class_call(background_tau_of_z(pba, 1., &tau_h_), pba->error_message, pfo->error_message);",
        "    class_call(background_at_tau(pba, tau_h_, long_info, inter_normal, &li_, bv_), pba->error_message, pfo->error_message);",
        "    wh_ = bv_[pba->index_bg_p_scf]/bv_[pba->index_bg_rho_scf];",
        "    free(bv_);",
        "    phg->w0 = w1_;",
        "    phg->wa = 2.*(wh_ - w1_);",
        "  }",
    ]) + NL)
    # 4. the stock guard refusing scf (the treatment above supplies what it says is "not yet coded")
    g = "  class_test(pba->Omega0_scf>0,"
    assert s.count(g) == 1
    s = s.replace(g, "  class_test((pba->Omega0_scf>0) && 0, /* HM_SCF_FIX: scf now handled */")
    open(f, "w").write(s)
print("patched", d)
