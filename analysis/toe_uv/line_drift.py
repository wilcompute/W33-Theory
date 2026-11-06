import json, math, sys, numpy as np
sys.path.insert(0, "/mnt/c/tmp/toe_wt/analysis/toe_uv")
import os; os.chdir("/mnt/c/tmp/toe_wt/analysis/toe_uv")
import class_cmb as C
out = {}
for ds in ("dovekie", "desy5"):
    fits = json.load(open(f"class_fit_{ds}.json"))
    for m in ("free_neg", "free_pos"):
        p = fits[m]["p"]; kp = {}
        C.run_class(p, "fading", keep=kp)
        bc = kp["cols"]; b = kp["raw"]
        z = b[:, bc.index("z")][::-1]; ph = b[:, bc.index("phi_scf")][::-1]
        os.system(f"rm -rf {kp['tag']}")
        rows = {}
        for zz in (0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0):
            dphi = float(np.interp(zz, z, ph)) - float(ph[0])
            rows[str(zz)] = dict(dphi=dphi, M_over_M0=math.exp(-p["cp"] * dphi))
        out[f"{ds}_{m}"] = dict(cp=p["cp"], rows=rows)
        print(ds, m, {k: round((v["M_over_M0"] - 1) * 100, 3) for k, v in rows.items()}, "percent", flush=True)
json.dump(out, open("line_drift.json", "w"), indent=1)
