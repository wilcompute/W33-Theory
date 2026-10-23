"""12183: the nine-dimensional interpolations (-1)^F . delta . exp(2 pi i p.V) on a circle of radius R (alpha' = 1), one for
each real-form class of V.  Half-winding sector w in Z + 1/2, n in Z, right-moving NS vacuum (h = 0, energy -1/2): a state with
internal momentum p (p^2 = P) and left oscillator level N is physical iff level matched, n w = 1/2 - P/2 - N, and has
alpha' m^2 / 4 = (n/R - w R)^2 / 4 - 1/2.  The tachyonic window of R is computed exactly from the coset norms of E8 + V.
Control: V = 0 is the thermal ensemble; its window must be the heterotic Hagedorn interval (2 - sqrt2, 2 + sqrt2), i.e.
beta_H = 2 pi (1 + 1/sqrt2) sqrt(alpha') with R = 2 x the thermal radius (half winding)."""
import json
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit('\\', 1)[0] if '\\' in __file__ else '.')
from tenD import SHIFT, coset  # noqa: E402


def norms(c1, c2):
    _, n1 = coset(SHIFT[c1], 6)
    _, n2 = coset(SHIFT[c2], 6)
    tot = np.round((n1[:, None] + n2[None, :]).ravel() * 4) / 4
    return sorted(set(float(x) for x in tot if x <= 4))


def window(c1, c2):
    roots = []
    states = []
    for P in norms(c1, c2):
        for N in (0, 1):
            for w in (0.5, 1.5, 2.5):
                nw = 0.5 - P / 2 - N
                n = nw / w
                if abs(n - round(n)) > 1e-12:
                    continue
                n = int(round(n))
                # m^2 < 0  <=>  |n/R - w R| < sqrt2  ;  solve w R^2 -+ sqrt2 R - n = 0
                rs = []
                for s in (1, -1):
                    disc = 2 + 4 * w * n
                    if disc < 0:
                        continue
                    for sign in (1, -1):
                        r = (s * np.sqrt(2) + sign * np.sqrt(disc)) / (2 * w)
                        if r > 0:
                            rs.append(float(r))
                grid = np.linspace(0.05, 6, 12000)
                m2 = (n / grid - w * grid) ** 2 / 4 - 0.5
                if np.any(m2 < -1e-12):
                    lo, hi = float(grid[m2 < 0].min()), float(grid[m2 < 0].max())
                    states.append(dict(P=P, N=N, w=w, n=n, window=[lo, hi]))
                    roots += rs
                else:
                    states.append(dict(P=P, N=N, w=w, n=n, min_m2=float(m2.min())))
    tach = [s for s in states if "window" in s]
    win = [min(s["window"][0] for s in tach), max(s["window"][1] for s in tach)] if tach else None
    return dict(window=win, tachyonic_states=tach, lightest=[s for s in states if "min_m2" in s][:3])


if __name__ == "__main__":
    out = {}
    for c in [("0", "0"), ("split", "0"), ("split", "split"), ("clock", "clock")]:
        out["x".join(c)] = window(*c)
        print(c, out["x".join(c)]["window"], [(s["P"], s["n"], s["w"]) for s in out["x".join(c)]["tachyonic_states"]])
    print("Hagedorn control 2 +- sqrt2 =", 2 - np.sqrt(2), 2 + np.sqrt(2), " clock edge 2 sqrt2 =", 2 * np.sqrt(2))
    json.dump(out, open("thermal.json", "w"), indent=1)
