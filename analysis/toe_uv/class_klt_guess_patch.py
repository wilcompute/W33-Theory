"""Third-stage patch for the KLT-family build (after class_fading_patch.py and class_klt_patch.py): a shooting guess suited to the pion-type potential.
V = A H0^2 g(phi), g = 1 - sqrt(1 - xi sin^2(phi/2f)); the fading guess A ~ 3.15 Omega_scf assumes an exponential with g ~ 1 and fails to bracket when g(phi_ini) << 1 (klt_fit.py: f = 0.1 M_P failed).  Use A ~ 3.15 Omega_scf / g(phi_ini), dA/dOmega ~ 3 / g(phi_ini).
usage: python3 class_klt_guess_patch.py path_to_klt_patched_class"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
p = root / "source/input.c"
s = p.read_text()
old = "xguess[index_guess] = 3.15*ba.Omega0_scf; dxdy[index_guess] = 3.; break;"
new = ("{ double kf = ba.scf_parameters[3]; double ph = ba.scf_parameters[ba.scf_parameters_size-2]; double sn = sin(0.5*ph/kf); "
       "double gg = 1. - sqrt(1. - 0.98765432098765*sn*sn); if (gg < 1e-4) gg = 1e-4; "
       "xguess[index_guess] = 3.15*ba.Omega0_scf/gg; dxdy[index_guess] = 3./gg; } break;")
assert s.count(old) == 1, s.count(old)
p.write_text(s.replace(old, new))
print("klt guess patched")
