"""Extract DES Y3 cosmic shear from the public 2pt file into an npz: xi+, xi-, their covariance block and the source n(z).
File: 2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits from https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/datavectors/
usage: py -3 des_y3_convert.py in.fits out.npz"""
import sys
import numpy as np
from astropy.io import fits

h = fits.open(sys.argv[1])
hd = h["COVMAT"].header
assert hd["NAME_0"].lower() == "xip" and hd["NAME_1"].lower() == "xim" and hd["STRT_1"] == 200
cov = np.array(h["COVMAT"].data[:400, :400], float)
out = dict(cov=cov)
for n in ("xip", "xim"):
    d = h[n].data
    out[n + "_i"] = np.array(d["BIN1"], int) - 1
    out[n + "_j"] = np.array(d["BIN2"], int) - 1
    out[n + "_ang"] = np.array(d["ANG"], float)
    out[n] = np.array(d["VALUE"], float)
d = h["nz_source"].data
out["z"] = np.array(d["Z_MID"], float)
out["nz"] = np.array([d[f"BIN{k}"] for k in range(1, 5)], float)
np.savez_compressed(sys.argv[2], **out)
print({k: v.shape for k, v in out.items()})
