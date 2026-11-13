"""Pass 12653: does W(9,2) (five qubits) have a maximal partial spread of size 8?  Rank-code form (Pass 12649): S1 = I, S2 over the
8 O(5)-orbit representatives, then 6 - 2 = 4 more nonsingular symmetric matrices, pairwise sums nonsingular, such that every
nonsingular symmetric T is 'killed' (T + S_i singular for some i, or T chosen).
Search: exact-cover style branching (Knuth's 'most constrained item'): at each node pick the uncovered compatible T with the FEWEST
possible killers among the remaining candidates (c = T or T + c singular) and branch over those killers, excluding the earlier siblings
in later branches (complete and non-redundant).  Plus the valid top-r coverage prune of Pass 12649.
Controls (must reproduce): n = 3 size 5 exists, size 7 none; n = 5 size 7 none (Pass 12649 DFS, 8,668,424 nodes, 2,695 s);
n = 5 size 9 exists (Pass 12650).  usage: py -3 analysis/w33_five_qubit_size8_dlx.py [size] [workers]"""
import json, os, sys, time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_five_qubit_size6.py")}
src = open(os.path.join(HERE, "w33_five_qubit_size6.py"), encoding="utf-8").read()
exec(src[: src.index(chr(10) + "def run(")], g)
setup, code_of, orthogonal_group, congr = g["setup"], g["code_of"], g["orthogonal_group"], g["congr"]
_S = {}
REVERSE = os.environ.get("DLX_REVERSE") == "1"  # independent second run: last-index tie-break and reversed killer order


def prep(n):
    if n in _S: return _S[n]
    pos, sing, alt, ns = setup(n)
    I = code_of(n, pos, [[int(i == j) for j in range(n)] for i in range(n)])
    O = orthogonal_group(n); cand = ns[~sing[ns ^ I]]
    seen = set(); reps = []
    for s in cand.tolist():
        if s in seen: continue
        orb = {congr(n, pos, A, s) for A in O}; seen |= orb; reps.append(s)
    _S[n] = (pos, sing, ns, I, cand, reps); return _S[n]


def search_rep(args):
    n, size, s2, tlimit = args
    pos, sing, ns, I, cand, reps = prep(n)
    t0 = time.time(); st = dict(found=None, nodes=0, timeout=False)

    def rec(chosen, R, cands, remaining):
        # R: codes still compatible with all chosen and not yet killed (they include cands)
        if st["found"] is not None or st["timeout"]: return
        st["nodes"] += 1
        if st["nodes"] % 5000 == 0 and time.time() - t0 > tlimit: st["timeout"] = True; return
        if st["nodes"] % 200000 == 0:
            print(f"  progress s2={int(s2)} nodes={st['nodes']} top={st.get('top')} t={time.time() - t0:.0f}s", flush=True)
        if len(R) == 0:
            if remaining == 0: st["found"] = [int(c) for c in chosen]
            return  # covered too early: a smaller maximal set (none exist below the target in the runs we make)
        if remaining == 0 or len(cands) == 0: return
        K = sing[cands[:, None] ^ R[None, :]] | (cands[:, None] == R[None, :])
        cnt = K.sum(0)
        if cnt.min() == 0: return
        if np.sort(K.sum(1))[-remaining:].sum() < len(R): return
        j = int(np.argmin(cnt)) if not REVERSE else int(len(cnt) - 1 - np.argmin(cnt[::-1]))
        killers = np.flatnonzero(K[:, j])
        if REVERSE: killers = killers[::-1]
        excluded = np.zeros(len(cands), bool)
        for kidx, ki in enumerate(killers):
            if len(chosen) == 2: st["top"] = f"{kidx + 1}/{len(killers)}"
            c = cands[ki]
            keep = ~excluded & ~sing[cands ^ c]; keep[ki] = False
            nc = cands[keep]
            nR = R[~sing[R ^ c] & (R != c)]
            rec(chosen + [c], nR, nc, remaining - 1)
            if st["found"] is not None or st["timeout"]: return
            excluded[ki] = True

    R0 = ns[~sing[ns ^ I] & ~sing[ns ^ s2] & (ns != I) & (ns != s2)]
    c3 = R0.copy()
    rec([I, s2], R0, c3, size - 4)
    return dict(s2=int(s2), found=st["found"], nodes=st["nodes"], timeout=st["timeout"], seconds=round(time.time() - t0, 1))


def run(n, size, workers, tlimit):
    pos, sing, ns, I, cand, reps = prep(n); t0 = time.time()
    if n == 5 and os.environ.get("DLX_REPS"):  # restrict to S3-class representatives (w33_rank_code_s3_symmetry.py)
        reps = [r for r in reps if str(r) in os.environ["DLX_REPS"].split(",")]
    with Pool(workers) as P:
        rs = P.map(search_rep, [(n, size, s2, tlimit) for s2 in reps], chunksize=1)
    found = next((r["found"] for r in rs if r["found"]), None)
    status = "exists" if found else ("undecided" if any(r["timeout"] for r in rs) else "none")
    out = dict(n=n, size=size, status=status, example=found, nodes=sum(r["nodes"] for r in rs), per_rep=rs, wall=round(time.time() - t0, 1))
    print({k: v for k, v in out.items() if k != "per_rep"}, flush=True); return out


if __name__ == "__main__":
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    tl = float(sys.argv[3]) if len(sys.argv) > 3 else 200000
    res = {}
    res["control_n3_size5"] = run(3, 5, 1, 60); assert res["control_n3_size5"]["status"] == "exists"
    res["control_n3_size7"] = run(3, 7, 1, 60); assert res["control_n3_size7"]["status"] == "none"
    if size == 7 or "--controls" in sys.argv:
        res["control_n5_size7"] = run(5, 7, workers, tl); assert res["control_n5_size7"]["status"] == "none"
    if size == 9 or "--controls" in sys.argv:
        res["control_n5_size9"] = run(5, 9, workers, 3600)
    if size == 8:
        res["n5_size8"] = run(5, 8, workers, tl)
    tag = "_reverse" if REVERSE else ""
    json.dump(res, open(os.path.join(ROOT, "data", f"w33_five_qubit_size{size}_dlx{tag}.json"), "w"), indent=1)
