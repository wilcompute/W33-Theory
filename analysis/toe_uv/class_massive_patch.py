"""CLASS for Lambda + Casimir of gravitons and N_f massive bulk Dirac fermions + sparse tower, on a copy of class_fading.  V = H0^2 (A + 3 Zn h(u)), u = lnx_i + b phi, h = exp(-4 u) (-5 + 4 N_f C(2 pi exp u)).  C(y) = c0 y^(5/2) sum_w w^(-5/2) K_{5/2}(w y), and K_{5/2} is closed form.  Derivatives by central differences in u, which is safe because h is smooth and they enter only the field equation.
scf_parameters = lambda (unused, kept for the CLASS prints), b, A, Zn, lnx_i, N_f, phi_ini, phi'_ini; scf_tuning_index = 2.
usage: python3 class_massive_patch.py path_to_a_copy_of_class_fading"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
p = root / "source/background.c"
s = p.read_text()
HELP = r"""
static double fading_C(double y) {
  double s = 0., w;
  double c0;
  if (y < 1e-6) return 1.;
  for (w = 1.; w < 60.; w += 1.) {
    double z = w*y;
    s += pow(w,-2.5)*sqrt(_PI_/(2.*z))*exp(-z)*(1.+3./z+3./(z*z));
    if (z > 60.) break;
  }
  c0 = 2.*pow(4.*_PI_,-2.5)*pow(2.,2.5)/(3.*1.03692775514337/(4.*_PI_*_PI_));
  return c0*pow(y,2.5)*s;
}
static double fading_h(struct background *pba, double phi) {
  double u = pba->scf_parameters[4] + pba->scf_parameters[1]*phi;
  return exp(-4.*u)*(-5. + 4.*pba->scf_parameters[5]*fading_C(2.*_PI_*exp(u)));
}
"""
marker = "double V_scf(\n"
assert s.count(marker) == 1
s = s.replace(marker, HELP + marker)
EDITS = [
    ("  return  V_e_scf(pba,phi)*V_p_scf(pba,phi);", "  return pba->H0*pba->H0*(pba->scf_parameters[2] + 3.*pba->scf_parameters[3]*fading_h(pba,phi));"),
    ("  return dV_e_scf(pba,phi)*V_p_scf(pba,phi) + V_e_scf(pba,phi)*dV_p_scf(pba,phi);", "  { double e = 1e-4; return pba->H0*pba->H0*3.*pba->scf_parameters[3]*(fading_h(pba,phi+e)-fading_h(pba,phi-e))/(2.*e); }"),
    ("  return ddV_e_scf(pba,phi)*V_p_scf(pba,phi) + 2*dV_e_scf(pba,phi)*dV_p_scf(pba,phi) + V_e_scf(pba,phi)*ddV_p_scf(pba,phi);", "  { double e = 1e-3; return pba->H0*pba->H0*3.*pba->scf_parameters[3]*(fading_h(pba,phi+e)-2.*fading_h(pba,phi)+fading_h(pba,phi-e))/(e*e); }"),
]
for old, new in EDITS:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
p.write_text(s)
print("patched")
