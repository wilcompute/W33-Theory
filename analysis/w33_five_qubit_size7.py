"""Pass 12649: does W(9,2) have a maximal partial spread of size 7?  Rank-code form with S1 = I, S2 over O(5)-orbit representatives,
then S3, S4, S5 by depth-first search with covering pruning: after k chosen matrices the uncovered set R must be covered by the
remaining r matrices, so some candidate must cover >= |R|/r of it (necessary).  Existence search with a time limit; reports
'exists' with an example, 'none' if the search completes, or 'undecided'.  Control: n = 3 size 7 (must be none: sizes 5 and 9 only).
usage: py -3 analysis/w33_five_qubit_size7.py"""
import json, os, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_five_qubit_size6.py")}
src = open(os.path.join(HERE, "w33_five_qubit_size6.py"), encoding="utf-8").read()
exec(src[: src.index(chr(10) + "def run(")], g)
setup, code_of, orthogonal_group, congr = g["setup"], g["code_of"], g["orthogonal_group"], g["congr"]
def search(n, k_total, tlimit):
    pos, sing, alt, ns = setup(n); N = len(ns); t0 = time.time()
    I = code_of(n, pos, [[int(i == j) for j in range(n)] for i in range(n)])
    O = orthogonal_group(n); cand = ns[~sing[ns ^ I]]
    seen = set(); reps = []
    for s in cand.tolist():
        if s in seen: continue
        orb = {congr(n, pos, A, s) for A in O}; seen |= orb; reps.append(s)
    nbm = lambda c: sing[ns ^ c]
    state = dict(found=None, timeout=False, nodes=0)
    def dfs(chosen, cov, cands, remaining):
        if state["found"] is not None or state["timeout"]: return
        state["nodes"] += 1
        if state["nodes"] % 2000 == 0 and time.time() - t0 > tlimit: state["timeout"] = True; return
        R = ns[~cov]
        if remaining == 0:
            if len(R) == 0: state["found"] = [int(c) for c in chosen]
            return
        if len(R) == 0: return  # covered with fewer matrices: then it would be a smaller maximal spread (none exist)
        if len(cands) == 0: return
        NBc = sing[R[None, :] ^ cands[:, None]]  # cands x |R|
        covc = NBc.sum(1)
        keep = covc * remaining >= len(R) - 0  # crude: best possible
        if covc.max() * remaining < len(R): return
        order = np.argsort(-covc)
        for idx in order:
            if covc[idx] * remaining < len(R): break
            c = cands[idx]
            nc = cands[(cands > c) & ~sing[cands ^ c]] if remaining > 1 else cands[:0]
            dfs(chosen + [c], cov | nbm(c), nc, remaining - 1)
            if state["found"] is not None or state["timeout"]: return
    for s2 in reps:
        c3 = cand[~sing[cand ^ s2]]
        dfs([I, s2], nbm(I) | nbm(s2), c3, k_total - 4)  # k_total = spread size; matrices = size - 2; I and s2 chosen
        if state["found"] is not None or state["timeout"]: break
    status = "exists" if state["found"] else ("undecided" if state["timeout"] else "none")
    r = dict(n=n, size=k_total, status=status, example=state["found"], nodes=state["nodes"], seconds=round(time.time() - t0, 1))
    print(r, flush=True); return r
res = dict(control_n3_size7=search(3, 7, 600), control_n3_size5=search(3, 5, 600), n5_size7=search(5, 7, 5400))
json.dump(res, open(os.path.join(ROOT, "data", "w33_five_qubit_size7.json"), "w"), indent=1)
