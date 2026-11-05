"""Haloscope limits against the PQ-assisted model (Pass 12606: E/N = 2/3, g = 0.653 g_KSVZ for N_DW = 1).
Data: the combined haloscope envelope from O'Hare's AxionLimits, limit_data/AxionPhoton/Haloscopes_Combined_microeV-meV.txt (m in eV, g in GeV^-1, 1 where nothing is excluded), downloaded to AXL.  Individual experiment files are polygons and are not used.
g(m) = alpha/(2 pi f_a) |E/N - 1.92|, f_a = 5.70e12 GeV / (m/ueV).
Controls: ADMX excludes KSVZ over 2.7 to 4 ueV and DFSZ over much of it; CAPP near 5 ueV at KSVZ.
usage: py -3 pq_haloscope_check.py [path to the combined file]"""
import json
import math
import sys
import numpy as np

AXL = sys.argv[1] if len(sys.argv) > 1 else "C:/tmp/axl/Haloscopes_Combined_microeV-meV.txt"
ALPHA = 1 / 137.036
d = np.loadtxt(AXL)
x, y = d[:, 0] * 1e6, d[:, 1]
o = np.argsort(x)
x, y = x[o], y[o]


def g(m, EN):
    return ALPHA / (2 * math.pi * 5.70e12 / m) * abs(EN - 1.92)


def frac(lo, hi, EN):
    m = np.geomspace(lo, hi, 20000)
    v = np.interp(m, x, y)
    return float(np.mean((v < 1e-3) & (g(m, EN) > v)))


res = {}
for lab, (lo, hi, EN) in dict(DFSZ_ADMX=(2.7, 4.0, 8 / 3), KSVZ_ADMX=(2.7, 4.0, 0.0), KSVZ_CAPP=(4.5, 5.5, 0.0), KSVZ_HAYSTAC=(16.5, 24.0, 0.0), ModelA_25_60=(25, 60, 2 / 3), ModelA_20_220=(20, 220, 2 / 3), ModelA_NDW5_25_60=(25, 60, 22 / 15)).items():
    res[lab] = frac(lo, hi, EN)
for lo, hi in ((25, 60), (60, 220)):
    m = np.geomspace(lo, hi, 20000)
    v = np.interp(m, x, y)
    k = v < 1e-3
    res[f"coverage_{lo}_{hi}"] = float(np.mean(k))
    res[f"best_ratio_{lo}_{hi}"] = float(np.min(v[k] / g(m[k], 2 / 3))) if k.any() else None
json.dump(res, open("pq_haloscope.json", "w"), indent=1)
print(res)
