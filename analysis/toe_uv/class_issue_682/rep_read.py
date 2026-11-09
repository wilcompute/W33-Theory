import numpy as np, re
def boost(r):
    li = np.loadtxt(f"/tmp/rep/{r}00_pk.dat"); nl = np.loadtxt(f"/tmp/rep/{r}00_pk_nl.dat")
    return {k: float(np.interp(k, *nl.T) / np.interp(k, *li.T)) for k in (0.1, 1.0, 3.0)}
for r in ("lam_", "scf2_"):
    print(r, {k: round(v, 3) for k, v in boost(r).items()})
lines = open("/tmp/rep/scf2_00_background.dat").read().split("\n")
hdr = [l for l in lines if l.startswith("#")][-1]
names = [re.sub(r"^\d+:", "", c).strip() for c in re.split(r"\s{2,}", hdr.strip("# ").strip())]
b = np.loadtxt("/tmp/rep/scf2_00_background.dat"); row = b[-1]
g = lambda s: row[names.index(s)]
rc = g("(.)rho_crit"); rs, ps = g("(.)rho_scf"), g("(.)p_scf")
rm = g("(.)rho_b") + g("(.)rho_cdm") + (g("(.)rho_ncdm[0]") - 3 * g("(.)p_ncdm[0]") if "(.)rho_ncdm[0]" in names else 0)
print("today: w_scf %.3f  Omega_scf %.3f  true Omega_m %.3f  Omega_m as halofit reads it %.3f  Omega_v as halofit reads it %.3f" % (ps / rs, rs / rc, rm / rc, (rm + rs - 3 * ps) / rc, 1 - (rm + rs - 3 * ps) / rc - (3 * ps) / rc))
