"""12526 follow-up: how few double-sixes are enough?  Using 6 rows per chosen double-six: (a) rank of the frame, (b) does the cubic moment detect exactly the 40 lines among collinear-or-not triples (T_abc at maximum exactly on the 160 collinear triples), (c) is the sub-frame tight on E_2?  Exhaustive search over small subsets up to S6-free symmetry is replaced by a stabiliser-orbit exhaustive search on pairs/triples plus greedy; the exact minimum for (a) has lower bound ceil(24/5) = 5.  usage: py -3 tomography_subset.py"""
import collections, itertools, json, random, runpy
import numpy as np, networkx as nx
ns = runpy.run_path("simplex_frame.py")
Z_groups, pts, lines, w = ns["Z_groups"], ns["pts"], ns["lines"], ns["w"]
sets = [set(L) for L in lines]; tri = list(itertools.combinations(range(40), 3)); col = np.array([any(set(t) <= L for L in sets) for t in tri])
ta, tb, tc = [np.array(x) for x in zip(*tri)]
def T3(Z): return (Z[:, ta] * Z[:, tb] * Z[:, tc]).sum(0)
def detects(idx):
    Z = np.vstack([Z_groups[i] for i in idx]); t = T3(Z)
    return bool(np.all(t[col] == t[col][0])) and bool(t[~col].max() < t[col][0])
out = {}; rng = random.Random(2)
E = np.linalg.svd(np.vstack(Z_groups).astype(float), full_matrices=False)[2][:24].T; 
def rank(idx): return int(np.linalg.matrix_rank(np.vstack([Z_groups[i] for i in idx])))
def tight(idx):
    Z = np.vstack([Z_groups[i] for i in idx]).astype(float); ev = np.linalg.eigvalsh(E.T @ Z.T @ Z @ E); return bool(abs(ev.max() - ev.min()) < 1e-8)
best = {}
for k in range(1, 13):
    samp = list(itertools.combinations(range(36), k)) if k <= 3 else [tuple(rng.sample(range(36), k)) for _ in range(1500)]
    rk = collections.Counter(rank(s) for s in samp) if k >= 3 else None
    dt = sum(detects(s) for s in samp[:600]); ti = sum(tight(s) for s in samp[:600])
    best[k] = dict(sampled=len(samp), max_rank=max(rank(s) for s in samp[:300]), rank24=(rk or {}).get(24, 0), detects_in_600=dt, tight_in_600=ti)
    print(k, best[k], flush=True)
    if dt and ti and k > 6: break
out["by_k"] = best
print(json.dumps(out)); json.dump(out, open("tomography_subset.json", "w"), indent=1)
