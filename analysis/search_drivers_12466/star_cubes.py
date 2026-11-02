"""12518: cube-and-conquer for hyperovals of Q(4,q) = coverage-{0,2} even line sets of W(3,q).

In such a set S, a chosen line X has exactly one further chosen line through each of its q+1 points: a STAR, i.e. a function
t: PG(1,q) -> F_q.  Stab(X) = q^3 : GL(2,q) acts on stars.  Its unipotent radical (symmetric S: (x,y) -> (x + S y, y)) moves each
t_p by a quadratic form evaluated at p, so stars modulo the radical are the cosets of a [q+1,3] code, and the first three
coordinates can always be normalised to a fixed reference (asserted below: the radical is regular on triples).  So every star is
equivalent to one of q^(q-2) normal forms, which are then reduced by GL(2,q) and the field automorphism by label propagation.

Each orbit representative fixes q+2 lines and leaves a much smaller exact problem.  Infeasibility of EVERY case at weight <= W proves
there is no hyperoval with at most W lines.  Controls: q = 3, 5, 7 must return the known minima 10, 20, 40.
usage: py -3 star_cubes.py q orbits           (count star orbits)
       py -3 star_cubes.py q solve W [secs]   (solve every orbit at weight <= W, per-case time limit)"""
import itertools
import json
import sys
import time

import numpy as np
from ortools.sat.python import cp_model
from symmetric_even_sets_gf import setup
from symmetric_fast import fast_build


def build(q):
    pts, lines = fast_build(q)
    F, add, mul, inv, neg = setup(q)
    pid = {p: i for i, p in enumerate(pts)}
    lid = {L: j for j, L in enumerate(lines)}
    norm = lambda v: tuple(mul[inv[next(t for t in v if t)]][t] for t in v)
    X = lid[tuple(sorted(pid[norm(v)] for v in ([(1, c, 0, 0) for c in F] + [(0, 1, 0, 0)])))]
    through = [[] for _ in pts]
    for j, L in enumerate(lines):
        for p in L:
            through[p].append(j)
    Xpts = list(lines[X])
    choices = [[j for j in through[p] if j != X] for p in Xpts]
    assert all(len(c) == q for c in choices)
    pos = {}
    for i, c in enumerate(choices):
        for k, j in enumerate(c):
            pos[j] = (i, k)

    def mat4(M, S):
        """(x, y) -> (M x + S M^{-T} y, M^{-T} y), a symplectic map fixing X, for symmetric S."""
        d = inv[add[mul[M[0][0]][M[1][1]]][neg[mul[M[0][1]][M[1][0]]]]]
        Mi = ((mul[d][M[1][1]], mul[d][neg[M[0][1]]]), (mul[d][neg[M[1][0]]], mul[d][M[0][0]]))
        MT = ((Mi[0][0], Mi[1][0]), (Mi[0][1], Mi[1][1]))

        def f(v):
            x, y = v[:2], v[2:]
            y2 = tuple(add[mul[MT[i][0]][y[0]]][mul[MT[i][1]][y[1]]] for i in range(2))
            x2 = tuple(add[add[mul[M[i][0]][x[0]]][mul[M[i][1]][x[1]]]][add[mul[S[i][0]][y2[0]]][mul[S[i][1]][y2[1]]]] for i in range(2))
            return (x2[0], x2[1], y2[0], y2[1])
        return f

    def on_lines(vmap):
        pm = [pid[norm(vmap(p))] for p in pts]
        return [lid[tuple(sorted(pm[x] for x in L))] for L in lines]
    return dict(q=q, pts=pts, lines=lines, X=X, Xpts=Xpts, choices=choices, pos=pos, through=through, F=F, add=add, mul=mul, inv=inv,
                neg=neg, mat4=mat4, on_lines=on_lines, lid=lid, pid=pid, norm=norm)


def star_action(B, lp):
    """A map fixing X as (permutation of the q+1 slots, per-slot permutation of the q choices)."""
    n, q = len(B["choices"]), B["q"]
    slot = np.zeros(n, dtype=np.int64)
    sub = np.zeros((n, q), dtype=np.int64)
    for i, c in enumerate(B["choices"]):
        for k, j in enumerate(c):
            i2, k2 = B["pos"][lp[j]]
            slot[i] = i2
            sub[i, k] = k2
    return slot, sub


def orbits(B):
    q = B["q"]
    F, n = B["F"], q + 1
    I = ((1, 0), (0, 1))
    # the radical: regular on the choices at slots 0, 1, 2
    rad = [B["on_lines"](B["mat4"](I, ((a, b), (b, c)))) for a, b, c in itertools.product(F, repeat=3)]
    triples = {}
    for lp in rad:
        slot, sub = star_action(B, lp)
        assert list(slot) == list(range(n)), "the radical fixes every point of X"
        triples[tuple(int(sub[i, 0]) for i in range(3))] = sub
    assert len(triples) == q ** 3, "the radical must be regular on triples"
    zero_sub = {}                                   # the radical element sending choices (a, b, c) at slots 0, 1, 2 to (0, 0, 0)
    for lp in rad:
        _, sub = star_action(B, lp)
        k = tuple(int(np.where(sub[i] == 0)[0][0]) for i in range(3))
        zero_sub[k] = sub
    assert len(zero_sub) == q ** 3
    # normal forms: slots 3..q free
    m = n - 3
    N = q ** m
    digits = np.zeros((N, n), dtype=np.int16)
    for i in range(m):
        digits[:, 3 + i] = (np.arange(N) // q ** i) % q
    powers = q ** np.arange(m)
    Zt = np.zeros((q, q, q, n, q), dtype=np.int16)
    for (a, b, c), sub in zero_sub.items():
        Zt[a, b, c] = sub

    def normal_index(T):                            # T: (N, n) array of choices -> index of its normal form
        idx = np.arange(n)
        S = Zt[T[:, 0], T[:, 1], T[:, 2]]           # (N, n, q)
        Z = np.take_along_axis(S, T[:, :, None], axis=2)[:, :, 0]
        assert not Z[:, :3].any()
        return (Z[:, 3:] * powers).sum(1)
    gens = []
    neg = B["neg"]
    prim = next(c for c in F if c and len({_pow(B, c, k) for k in range(q - 1)}) == q - 1)
    gens.append(B["on_lines"](B["mat4"](((prim, 0), (0, 1)), ((0, 0), (0, 0)))))
    gens.append(B["on_lines"](B["mat4"](((0, 1), (neg[1], 0)), ((0, 0), (0, 0)))))
    gens.append(B["on_lines"](B["mat4"](((1, 1), (0, 1)), ((0, 0), (0, 0)))))
    gens.append(B["on_lines"](B["mat4"](((1, prim), (0, 1)), ((0, 0), (0, 0)))))
    # the scalar similitude (x, y) -> (x, c y) preserves the form up to a factor, so it preserves W(3,q)
    gens.append(B["on_lines"](lambda v: (v[0], v[1], B["mul"][prim][v[2]], B["mul"][prim][v[3]])))
    p, k = _char(q)
    if k > 1:                                       # the field automorphism x -> x^p
        fro = lambda x: _pow(B, x, p)
        gens.append(B["on_lines"](lambda v: tuple(fro(t) for t in v)))
    maps = []
    for lp in gens:
        slot, sub = star_action(B, lp)
        T = np.zeros_like(digits)
        for i in range(n):
            T[:, slot[i]] = sub[i, digits[:, i]]
        maps.append(normal_index(T))
    label = np.arange(N)
    while True:
        old = label.copy()
        for mp in maps:
            np.minimum.at(label, mp, label.copy())
            label = np.minimum(label, label[mp])
        label = label[label]
        if (label == old).all():
            break
    B["label"], B["normal_index"], B["digits"] = label, normal_index, digits
    reps, counts = np.unique(label, return_counts=True)
    return digits, reps, counts


def _pow(B, x, k):
    r = 1
    for _ in range(k):
        r = B["mul"][r][x]
    return r


def _char(q):
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23):
        if q % p == 0:
            k = 0
            t = q
            while t % p == 0:
                t //= p
                k += 1
            return p, k
    return q, 1


def solve_case(B, star, W, tl, workers=8):
    """Hyperoval containing X and the star: every point on 0 or 2 chosen lines, at most W lines."""
    lines, through, X, q = B["lines"], B["through"], B["X"], B["q"]
    fixed = {X} | {B["choices"][i][int(star[i])] for i in range(q + 1)}
    md = cp_model.CpModel()
    y = {}
    banned = {j for p in B["Xpts"] for j in through[p]} - fixed
    for j in range(len(lines)):
        if j in fixed:
            y[j] = 1
        elif j in banned:
            y[j] = 0
        else:
            y[j] = md.NewBoolVar(f"y{j}")
    for p in range(len(B["pts"])):
        s = [y[j] for j in through[p]]
        z = md.NewBoolVar(f"z{p}")
        md.Add(sum(s) == 2 * z)
    md.Add(sum(y.values()) <= W)
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = tl
    sv.parameters.num_workers = workers
    st = sv.Solve(md)
    out = dict(status=sv.StatusName(st))
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        out["chosen"] = [j for j in range(len(lines)) if sv.Value(y[j])]
    return out


if __name__ == "__main__":
    q = int(sys.argv[1])
    B = build(q)
    t0 = time.time()
    digits, reps, counts = orbits(B)
    print(f"q={q}: {len(digits)} normal forms, {len(reps)} star orbits ({time.time() - t0:.0f}s), sizes {counts.min()}..{counts.max()}", flush=True)
    if sys.argv[2] == "solve":
        W = int(sys.argv[3])
        tl = float(sys.argv[4]) if len(sys.argv) > 4 else 600
        res = dict(q=q, W=W, star_orbits=len(reps), feasible=[], unknown=[], infeasible=0, seconds=None)
        for n, r in enumerate(reps):
            o = solve_case(B, digits[r], W, tl)
            if o["status"] == "INFEASIBLE":
                res["infeasible"] += 1
            elif "chosen" in o:
                res["feasible"].append(dict(rep=int(r), weight=len(o["chosen"]), chosen=o["chosen"]))
            else:
                res["unknown"].append(int(r))
            if (n + 1) % max(1, len(reps) // 20) == 0:
                print(f"  {n + 1}/{len(reps)}: infeasible {res['infeasible']}, feasible {len(res['feasible'])}, unknown {len(res['unknown'])}, "
                      f"{time.time() - t0:.0f}s", flush=True)
        res["seconds"] = round(time.time() - t0, 1)
        print(json.dumps({k: v for k, v in res.items() if k != "feasible"}), "feasible cases:", [f["weight"] for f in res["feasible"]][:30], flush=True)
        json.dump(res, open(f"star_cubes_q{q}_W{W}.json", "w"), indent=1)
