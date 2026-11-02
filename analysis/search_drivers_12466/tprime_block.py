"""12521: the 2-dim block of the B4 image.  Normalise each R_i on the block to det 1 (two square-root lifts differ by -1, and the group
generated contains -1, checked), generate the group, read off order, centre, element orders and the character on the three classes of
elements of order 3 / 4 / 6.  Checked against the kernel order 54 and projective image 12 of tl_braid_iso_exact.py."""
import cmath, collections, json, runpy
import numpy as np
ns = runpy.run_path("tl_braid_iso_exact.py")
R, blocks = ns["R"], ns["blocks"]
B = next(b for b in blocks if b.shape[1] == 2)
g = [B.conj().T @ r @ B for r in R[:3]]
g1 = [m / cmath.sqrt(np.linalg.det(m)) for m in g]
print("unitary", [bool(np.allclose(m.conj().T @ m, np.eye(2))) for m in g], "eigs of raw", [np.round(np.linalg.eigvals(m), 5).tolist() for m in g[:1]])
key = lambda m: tuple(np.round(m.flatten(), 7).tolist())
seen = {key(np.eye(2, dtype=complex)): np.eye(2, dtype=complex)}; fr = [np.eye(2, dtype=complex)]
while fr and len(seen) < 2000:
    nx = []
    for a in fr:
        for h in g1:
            b = h @ a; b += 0
            k = tuple(complex(round(z.real, 7) + 0.0, round(z.imag, 7) + 0.0) for z in b.flatten())
            if k not in seen: seen[k] = b; nx.append(b)
    fr = nx
els = list(seen.values())
def order(m):
    p = m.copy(); n = 1
    while not np.allclose(p, np.eye(2)) and n < 100: p = p @ m; n += 1
    return n
prof = collections.Counter(order(m) for m in els)
cent = sum(all(np.allclose(m @ h, h @ m) for h in g1) for m in els)
tr = collections.Counter((order(m), complex(np.round(np.trace(m), 5))) for m in els)
same_gens = [bool(np.allclose(g1[0], x)) or bool(np.allclose(g1[0], -x)) for x in g1]
out = dict(order=len(els), centre=int(cent), element_orders=dict(sorted(prof.items())), traces={f"{k[0]}:{k[1]}": v for k, v in sorted(tr.items(), key=lambda t: (t[0][0], t[0][1].real, t[0][1].imag))}, sigma1_equals_sigma3_up_to_sign=bool(np.allclose(g1[0], g1[2]) or np.allclose(g1[0], -g1[2])))
print(out); json.dump(out, open("tprime_block.json", "w"), indent=1)
