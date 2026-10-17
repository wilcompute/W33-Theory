import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
bs = chr(92)
def cert(name): return bs + "cert{" + name.replace("_", bs + "_") + ".py}"
p = _os.path.join(_os.path.dirname(_ANA), 'papers', 'forty_points', 'sec09_physics.tex')
s = open(p, encoding="utf-8").read(); anchor = cert("w33_pass11936_radial_weld"); assert s.count(anchor) == 1
par = (" The finite part of the cusp is an elliptic curve, and the special orbits put it at the elliptic points: along the "
 "selected $" + bs + "log" + bs + "tfrac85$ orbit the boundary curve is the square torus, $" + bs + "tau'=i$, $j=1728$, for all 54 members (the $T$ orbit gives "
 "the hexagonal torus, $j=0$). The up/charm ratio is a boundary invariant, $0.80$ here; a small value would need the "
 "boundary curve itself to degenerate. " + cert("w33_pass11937_boundary_elliptic_points"))
s = s.replace(anchor, anchor + par); open(p, "w", encoding="utf-8").write(s)
q = _os.path.join(_os.path.dirname(_ANA), 'papers', 'forty_points', 'appA_ledger.tex'); t = open(q, encoding="utf-8").read()
r = "11937: the E8-selected direction degenerates the torus onto a cusp with square boundary curve ($" + bs + "tau'=i$, $j=1728$, all 54 orbit members); the $T$ orbit gives $j=0$; $m_u/m_c$ is a boundary invariant (0.80)"
i = t.rindex(bs + "end{longtable}"); t = t[:i] + r + " & " + bs + "tierB & " + cert("w33_pass11937_boundary_elliptic_points") + bs + bs + "\n" + t[i:]
open(q, "w", encoding="utf-8").write(t); print("ok")
