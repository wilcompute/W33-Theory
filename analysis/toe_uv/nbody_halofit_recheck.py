"""Pass 12573's N-body control was compared against CLASS halofit for the relaxing radion, a scalar-field run, i.e. against the
faulty halofit (Pass 12632).  Recompute that comparison against the patched halofit: the N-body control's P/P_lin is stored
(nbody_*.json: P_over_linear_control, k_common); the patched boost P_nl/P_lin at z = 0 comes from the same class_massive run
with the patched build (nbody_ic_hf.npz from nbody_ic.py with MASSBIN=class_massive_hf).  The coupled/control ratio, the actual
N-body result, never used halofit and is unaffected.
usage: python3 nbody_halofit_recheck.py"""
import json, os
import numpy as np
BG = os.path.dirname(os.path.abspath(__file__)); os.chdir(BG)
ic = np.load("nbody_ic_hf.npz")
boost = lambda k: np.interp(np.log(k), np.log(ic["P0k"]), ic["P0nl"]) / np.interp(np.log(k), np.log(ic["P0k"]), ic["P0"])
out = {}
for f in sorted(x for x in os.listdir(".") if x.startswith("nbody_L") and x.endswith(".json")):
    d = json.load(open(f))
    if "P_over_linear_control" not in d:
        continue
    k = np.array(d["k_common"]); pl = np.array(d["P_over_linear_control"]); old = np.array(d["P_over_halofit_control"])
    new = pl / boost(k)
    sel = (k >= 0.3) & (k <= 2.9)
    out[f] = dict(k=k.tolist(), P_over_halofit_orig=old.tolist(), P_over_halofit_patched=new.tolist(),
                  maxdev_orig_0p3_2p9=float(np.max(np.abs(old[sel] - 1))) if sel.any() else None,
                  maxdev_patched_0p3_2p9=float(np.max(np.abs(new[sel] - 1))) if sel.any() else None)
    print(f, "k 0.3-2.9: max |P/halofit - 1| orig %.3f -> patched %.3f" % (out[f]["maxdev_orig_0p3_2p9"] or -1, out[f]["maxdev_patched_0p3_2p9"] or -1), "| patched by k:", np.round(new, 2).tolist())
json.dump(out, open("nbody_halofit_recheck.json", "w"), indent=1)
