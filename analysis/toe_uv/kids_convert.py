"""Extract KiDS-Legacy cosmic shear (Wright et al. 2025) from the public release KiDS_Legacy_xipm.fits into the npz layout used by class_des_fit.py.
Release: https://kids.strw.leidenuniv.nl/sci_data/KiDS_Legacy_cosmic_shear_data_release.tar.gz (data/KiDS_Legacy_xipm.fits, data/Nz_covariance.txt).
Also stores the correlated photo-z shift prior: dz = L u with L = chol(Nz_covariance), u ~ N(u_mean, 1) (their correlated_dz_priors with the uncorr_bias means of KiDS_Legacy_priors.ini), so mean = L u_mean, covariance = Nz_covariance.
Shear calibration m is included in the KiDS covariance (no m nuisances).
usage: py -3 -I kids_convert.py in.fits nzcov.txt out.npz"""
import sys
import numpy as np
from astropy.io import fits

h = fits.open(sys.argv[1])
print([x.name for x in h])
hd = h["COVMAT"].header
names = [hd.get(f"NAME_{i}") for i in range(4)]
strt = [hd.get(f"STRT_{i}") for i in range(4)]
print("COVMAT blocks", names, strt)
out = {}
lens = {}
for key, ext in (("xip", "xiP"), ("xim", "xiM")):
    d = h[ext].data
    print(ext, d.columns.names[:8], len(d))
    out[key + "_i"] = np.array(d["BIN1"], int) - 1
    out[key + "_j"] = np.array(d["BIN2"], int) - 1
    out[key + "_ang"] = np.array(d["ANG"], float)
    out[key] = np.array(d["VALUE"], float)
    lens[key] = len(d)
n = lens["xip"] + lens["xim"]
assert names[0].lower() == "xip" and names[1].lower() == "xim" and strt[1] == lens["xip"], (names, strt)
out["cov"] = np.array(h["COVMAT"].data[:n, :n], float)
d = h["NZ_SOURCE"].data
nb = sum(1 for c in d.columns.names if c.startswith("BIN"))
out["z"] = np.array(d["Z_MID"], float)
out["nz"] = np.array([d[f"BIN{k}"] for k in range(1, nb + 1)], float)
C = np.loadtxt(sys.argv[2])
u = np.array([2.5374, -2.44484, -1.37982, -0.494275, 1.40234, 6.26323])
L = np.linalg.cholesky(C)
out["dz_mean"] = L @ u
out["dz_cov"] = C
np.savez_compressed(sys.argv[3], **out)
print({k: v.shape for k, v in out.items()})
print("dz prior mean", np.round(out["dz_mean"], 4), "sd", np.round(np.sqrt(np.diag(C)), 4))
print("theta xip", np.unique(out["xip_ang"]).round(2))
