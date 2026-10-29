"""12428-12429.
12428: diameter of the W(3,q) collinearity graph (q = 3, 5, 7): mu = q + 1 > 0, so every two points are within 2 steps -- a local update
       reaches everything in two steps; no extended light cone exists on the fixed graph (cf. in-corpus toe54: a growing tessellation is
       needed).
12429: the qutrit clock and shift (Z X = w X Z, w = e^{2 pi i/3}) are magnetic translations with flux 1/3 per plaquette; the W(3,3)
       commutation form is this flux in each of two planes.  Hofstadter model at flux p/q = 1/3: band Chern numbers by the Fukui-Hatsugai-
       Suzuki lattice method (gauge-invariant link variables); TKNN Diophantine check r = q s_r + p t_r (Hall conductance of the lowest r
       bands = t_r e^2/h).  Two qutrits = flux 1/3 in two independent planes (4D Hofstadter, product bands): second Chern numbers
       C2 = C_a C_b, total over all band pairs.  Known 2D results (TKNN 1982; Hofstadter); the reading as a topological unit of W(3,3) is
       the new part."""
import json, itertools
import numpy as np
import networkx as nx
import sys
sys.path.insert(0, '../search_drivers_12419')
from two_codes import w3q

out = {}
out['12428_diameter'] = {q: nx.diameter(nx.from_numpy_array(w3q(q))) for q in (3, 5, 7)}


def hofstadter(kx, ky, p=1, q=3):
    H = np.zeros((q, q), dtype=complex)
    for m in range(q):
        H[m, m] = -2 * np.cos(ky + 2 * np.pi * p * m / q)
        H[m, (m + 1) % q] += -1
        H[(m + 1) % q, m] += -1
    H[0, q - 1] += -np.exp(-1j * q * kx) + 1 if q > 2 else 0
    H[q - 1, 0] += -np.exp(1j * q * kx) + 1 if q > 2 else 0
    return H


def chern_numbers(p=1, q=3, N=36):
    kxs = np.linspace(0, 2 * np.pi / q, N, endpoint=False)
    kys = np.linspace(0, 2 * np.pi, N, endpoint=False)
    vecs = np.empty((N, N, q, q), dtype=complex)
    for i, kx in enumerate(kxs):
        for j, ky in enumerate(kys):
            w, v = np.linalg.eigh(hofstadter(kx, ky, p, q))
            vecs[i, j] = v
    C = []
    for b in range(q):
        F = 0.0
        for i in range(N):
            for j in range(N):
                u1 = vecs[i, j, :, b]; u2 = vecs[(i + 1) % N, j, :, b]; u3 = vecs[(i + 1) % N, (j + 1) % N, :, b]; u4 = vecs[i, (j + 1) % N, :, b]
                l = np.vdot(u1, u2) * np.vdot(u2, u3) * np.vdot(u3, u4) * np.vdot(u4, u1)
                F += np.angle(l)
        C.append(int(round(F / (2 * np.pi))))
    return C


C = chern_numbers()
tknn = []
orient = -1     # the k-grid orientation here is opposite to the TKNN convention (bands come out (-1, 2, -1) = -(1, -2, 1))
for r in range(1, 3):
    t = orient * sum(C[:r])
    s = (r - t * 1) / 3
    tknn.append(dict(r=r, t=t, s=s, diophantine_ok=float(s).is_integer() and abs(t) <= 3 / 2))
second = {f'{a},{b}': C[a] * C[b] for a in range(3) for b in range(3)}
out['12429'] = dict(flux='1/3', band_chern=C, sum=sum(C), tknn=tknn, second_chern_two_qutrits=second,
                    lowest_band_pair_C2=C[0] * C[0], filled_lowest_bands_C2=sum(C[a] * C[b] for a in range(1) for b in range(1)))
print(json.dumps(out, indent=1))
json.dump(out, open('flux.json', 'w'), indent=1)
