"""12490: is a given even line set of W(3,q) a regulus-matching set S(R0, M)?  Test: the twin pairs of S (same neighbourhood) number
(q+1)/2 and their 2 * (q+1)/2 = q+1 lines R0 are pairwise disjoint and closed under "lines meeting three of them" (a regulus: every
line meeting three lines of R0 meets all of them), and S = R0 + the perps {L, L'}^perp of the pairs.
Then: sample many DIFFERENT 40-line optima at q = 7 with CP-SAT (weight fixed to 40, each new solution excluded, random hints) and
recognise every one.  usage: py -3 cube_recognise.py [n_samples] [seconds_each]"""
import sys, json, random, itertools, collections
from ortools.sat.python import cp_model
from even_line_sets_gf import build


def twins(S, sets):
    nb = {L: frozenset(M for M in S if M != L and sets[L] & sets[M]) for L in S}
    cl = collections.defaultdict(list)
    for L in S: cl[nb[L]].append(L)
    return [c for c in cl.values() if len(c) == 2], nb


def is_regulus_set(S, sets, q):
    S = set(S)
    if sizes := {len(sets[L]) for L in S}: pass
    if any(sets[a] & sets[b] for a, b in itertools.combinations(S, 2)): return False
    # all lines of PG(3,q) that meet three given members must meet all members: check with the isotropic transversal count instead:
    # a regulus of isotropic lines has every member meeting exactly the same transversals; equivalently, for three members, every
    # isotropic line meeting all three meets every member
    a, b, c = list(S)[:3]
    trans = [j for j, M in enumerate(sets) if M & sets[a] and M & sets[b] and M & sets[c]]
    return all(all(sets[t] & sets[L] for L in S) for t in trans)


def recognise(Sidx, sets, q):
    S = set(Sidx)
    pairs, nb = twins(S, sets)
    if len(pairs) != (q + 1) // 2: return dict(cube=False, twin_pairs=len(pairs))
    R0 = {L for p in pairs for L in p}
    perps = set()
    for L, Lp in pairs:
        perps |= {j for j, M in enumerate(sets) if M & sets[L] and M & sets[Lp]}
    reg = is_regulus_set(R0, sets, q)
    return dict(cube=bool(reg and S == R0 | perps), twin_pairs=len(pairs), regulus=reg, union_matches=S == R0 | perps)


def sample(q, n, tl, seed=7):
    pts, lines, N = build(q); n_pts, m = N.shape
    sets = [frozenset(l) for l in lines]
    rng = random.Random(seed)
    md = cp_model.CpModel(); y = [md.NewBoolVar(f"y{j}") for j in range(m)]
    for i in range(n_pts):
        z = md.NewIntVar(0, (q + 1) // 2, f"z{i}"); md.Add(sum(y[j] for j in range(m) if N[i, j]) == 2 * z)
    md.Add(sum(y) == (q + 1) * (q + 3) // 2)
    out = []
    for k in range(n):
        md.ClearHints()
        for j in rng.sample(range(m), 30): md.AddHint(y[j], rng.random() < 0.5)
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 8; s.parameters.random_seed = k
        st = s.Solve(md)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            out.append(dict(status=s.StatusName(st))); continue
        S = [j for j in range(m) if s.Value(y[j])]
        rec = recognise(S, sets, q); rec["status"] = s.StatusName(st); out.append(rec)
        md.Add(sum(y[j] for j in S) <= len(S) - 1)          # exclude this solution
        print(k, rec, flush=True)
    return out


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10; tl = float(sys.argv[2]) if len(sys.argv) > 2 else 300
    q = 7
    pts, lines, N = build(q); sets = [frozenset(l) for l in lines]
    known = []
    for fn in ("symmetric_q7_r8.json", "symmetric_q7_r4.json"):
        for rec in json.load(open(fn)):
            if rec.get("weight") == 40:
                known.append(dict(source=f"{fn} k={rec['k']}", **recognise(rec["chosen"], sets, q)))
    for x in known: print(x)
    res = dict(known=known, sampled=sample(q, n, tl))
    json.dump(res, open("cube_recognise_q7.json", "w"), indent=1)
