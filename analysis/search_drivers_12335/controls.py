"""12335 controls: (a) tau2 cutoff stability at R = 0.4 (T = 40 vs 120); (b) the tachyon edge: at R = 0.61, 0.612 the half-tower tachyon
term with a long cutoff must dominate and drive V down (convergence of exp((2 pi/3 - pi/(4R^2)) tau2) only for R^2 < 3/8)."""
import json, sys
sys.argv = ['x']
src = open('potential.py').read().split("out = dict(species")[0]
exec(src)
def V(R, T):
    tot = 0.0
    for (tw, c), d in species.items():
        q = 0.0 if tw == 'int' else 0.5; ell = -1 / 6 if c == 'T' else 0.0; sgn = -1 if c == 'F' else 1
        tot -= sgn * d * integral(q, ell, R, T=T)
    return tot
res = dict(R04_T40=V(0.4, 40.0), R04_T120=V(0.4, 120.0), R060_T400=V(0.60, 400.0), R061_T400=V(0.61, 400.0), R0612_T1500=V(0.612, 1500.0))
print(json.dumps(res, indent=1)); json.dump(res, open('controls.json', 'w'), indent=1)
