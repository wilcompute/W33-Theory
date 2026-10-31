"""12489: an explicit family of even line sets of W(3,q), q odd, of size (q+1)(q+3)/2.

Take a regulus R0 of q+1 totally isotropic lines whose OPPOSITE regulus contains no isotropic line (antiregularity: 0 or 2), and a
perfect matching of R0 into (q+1)/2 pairs {L, L'}.  The candidate is
    S = R0  u  U_pairs {L, L'}^perp        (|S| = (q+1) + (q+1)/2 * (q+1) = (q+1)(q+3)/2)
(the perps are pairwise disjoint and miss R0, because a line meeting three lines of R0 lies in the opposite regulus, which has no
isotropic line).  Every point of R0 is covered exactly twice by construction; the matching decides the rest.  This script builds R0
from three pairwise skew isotropic lines, tests EVERY perfect matching, and reports how many give an even set.
usage: py -3 regulus_matching.py q [max_tries_of_R0]"""
import sys, json, itertools, random
import numpy as np
from even_line_sets_gf import build


def main(q, tries=50, seed=1):
    pts, lines, N = build(q)
    pid = {p: i for i, p in enumerate(pts)}

    def norm(v):
        v = tuple(x % q for x in v)
        f = next(x for x in v if x); s = pow(f, -1, q)
        return tuple(x * s % q for x in v)

    def span(vecs):
        """all projective points of the span of the given vectors"""
        out = set()
        for coef in itertools.product(range(q), repeat=len(vecs)):
            if any(coef):
                v = [sum(c * u[k] for c, u in zip(coef, vecs)) % q for k in range(4)]
                if any(v): out.add(pid[norm(v)])
        return out

    def line_pts(a, b):
        return frozenset(span([pts[a], pts[b]]))

    lidx = {frozenset(l): j for j, l in enumerate(lines)}
    rng = random.Random(seed)
    results = []
    for _ in range(tries):
        T = rng.sample(range(len(lines)), 3)
        Ls = [frozenset(lines[t]) for t in T]
        if any(Ls[a] & Ls[b] for a, b in ((0, 1), (0, 2), (1, 2))): continue
        # transversals of T1, T2, T3: through p in T1, the point of T3 in the plane <p, T2>
        trans = []
        for p in Ls[0]:
            pl = span([pts[p]] + [pts[x] for x in list(Ls[1])[:2]])
            r = pl & Ls[2]
            if len(r) != 1: break
            trans.append(line_pts(p, next(iter(r))))
        if len(trans) != q + 1: continue
        opp_isotropic = sum(1 for U in trans if U in lidx)
        if opp_isotropic != 0: continue               # need the antiregular "0" case
        # R0 = the lines meeting three transversals (it contains T1, T2, T3)
        U1, U2, U3 = trans[:3]
        R0, R0_param = [], []
        U1l = sorted(U1); u, v = pts[U1l[0]], pts[U1l[1]]

        def param(x):
            for t in range(q):
                if pid[norm([u[k] + t * v[k] for k in range(4)])] == x: return t
            return "inf"
        for s in U1:
            pl = span([pts[s]] + [pts[x] for x in list(U2)[:2]])
            t = pl & U3
            if len(t) != 1: break
            R0.append(line_pts(s, next(iter(t)))); R0_param.append(param(s))
        if len(R0) != q + 1 or not all(L in lidx for L in R0): continue
        R0i = [lidx[L] for L in R0]
        # perps {L, L'}^perp for all pairs of R0
        sets = [frozenset(l) for l in lines]
        perp = {}
        for a, b in itertools.combinations(range(q + 1), 2):
            La, Lb = sets[R0i[a]], sets[R0i[b]]
            perp[(a, b)] = [j for j, M in enumerate(sets) if M & La and M & Lb]
            assert len(perp[(a, b)]) == q + 1
        base = np.zeros(len(pts), dtype=np.int64)
        for j in R0i: base[list(lines[j])] += 1
        cov = {k: np.bincount([p for j in v for p in lines[j]], minlength=len(pts)) for k, v in perp.items()}

        def matchings(items):
            if not items:
                yield []
                return
            a = items[0]
            for i in range(1, len(items)):
                rest = items[1:i] + items[i + 1:]
                for m in matchings(rest):
                    yield [(a, items[i])] + m
        good, total, example, good_list = 0, 0, None, []
        for m in matchings(list(range(q + 1))):
            total += 1
            c = base.copy()
            for pr in m: c = c + cov[pr]
            if not (c % 2).any():
                good += 1; good_list.append([(R0_param[a], R0_param[b]) for a, b in m])
                if example is None:
                    S = set(R0i) | {j for pr in m for j in perp[pr]}
                    example = dict(matching=m, size=len(S), coverage=sorted(set(int(x) for x in c)))
        results.append(dict(R0=R0i, matchings=total, even=good, example=example, good_matchings_param=good_list))
        if good:
            break
    return dict(q=q, predicted_size=(q + 1) * (q + 3) // 2, tried_R0=len(results), results=results)


if __name__ == "__main__":
    q = int(sys.argv[1]); tries = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    out = main(q, tries)
    print(json.dumps({k: v for k, v in out.items() if k != "results"}),
          [(r["matchings"], r["even"], r["example"] and r["example"]["size"]) for r in out["results"]])
    json.dump(out, open(f"regulus_matching_q{q}.json", "w"), indent=1)
