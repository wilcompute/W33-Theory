"""12528: Jones at e^{i pi/3} and W(3,3).  Lickorish-Millett: |V_L(e^{i pi/3})| = sqrt(3)^{dim H_1(M_L; F_3)}, M_L the double branched cover.  Birman-Hilden: B6 acts on H_1(genus 2) by Dehn twists along a chain a1..a5, with a1 + a3 + a5 = 0, so mod 3 it is the transvection rep on W(3,3), and a plat closure caps (12)(34)(56) kill L0 = <a1, a3, a5>.
Test: for words in B6, compute the Kauffman bracket of the plat closure by an independent state sum (no W(3,3) input) at A = e^{5 pi i/12} (delta = sqrt 3), and compare with the prediction d = dim(L0 meet beta L0) = 2, 1, 0 for 4, 1, 0 common points.
Controls: another line in place of L0 fails; the standard closure against the reduced Burau matrix at t = -1 for n = 3, 4, 5; known knots.  usage: py -3 knots_w33.py"""
import cmath, collections, itertools, json, math, random, runpy
ns = runpy.run_path("braid_codewords.py")
pts, lines, w, T, gens, path, compose = (ns[k] for k in ("pts", "lines", "w", "T", "gens", "path", "compose"))
A = cmath.exp(5j * cmath.pi / 12); delta = -A ** 2 - A ** -2
assert abs(delta - math.sqrt(3)) < 1e-12
out = dict(path=path)
L0 = [frozenset(L) for L in lines if path[0] in L and path[2] in L]; assert len(L0) == 1; L0 = L0[0]; out["p4_on_line_of_p0_p2"] = path[4] in L0
out["all_three_commute"] = all(w(pts[path[a]], pts[path[b]]) == 0 for a, b in ((0, 2), (0, 4), (2, 4)))
inv_ = lambda g: tuple(sorted(range(40), key=lambda i: g[i]))
G6 = gens + [inv_(g) for g in gens]
def rep(word):
    r = tuple(range(40))
    for s in word:                       # word letters +-i, i = 1..5, leftmost acts last on the top; order fixed by a test below
        g = gens[abs(s) - 1] if s > 0 else inv_(gens[abs(s) - 1])
        r = compose(g, r)
    return r
def bracket(word, n, closure):
    """state sum: every crossing is resolved identity (A) or cup-cap (A^-1); count loops with a union-find on strand segments."""
    c = len(word); tot = 0j
    for st in range(1 << c):
        par = {}
        def f(x):
            par.setdefault(x, x)
            while par[x] != x:
                par[x] = par[par[x]]; x = par[x]
            return x
        def u(a, b): par[f(a)] = f(b)
        level = {}                       # segments: (strand position, layer); layer k is the part between crossing k-1 and crossing k
        for k, s in enumerate(word):
            i = abs(s) - 1
            for p in range(n):
                if p not in (i, i + 1): u((p, k), (p, k + 1))
            res_id = ((st >> k) & 1 == 0)
            use_id = res_id     # identity smoothing; its A-weight sign is carried in a_ below
            if use_id: u((i, k), (i, k + 1)); u((i + 1, k), (i + 1, k + 1))
            else: u((i, k), (i + 1, k)); u((i, k + 1), (i + 1, k + 1))
        if closure == "plat":
            for a in range(0, n, 2): u((a, 0), (a + 1, 0)); u((a, c), (a + 1, c))
        else:
            for p in range(n): u((p, 0), (p, c))
        loops = len({f(x) for x in [(p, k) for p in range(n) for k in range(c + 1)]})
        a_ = 0
        for k, s in enumerate(word):
            res_id = ((st >> k) & 1 == 0)
            a_ += (1 if res_id else -1) * (1 if s > 0 else -1)
        tot += A ** a_ * delta ** (loops - 1)
    return tot
def dim_from_abs(x):
    d = math.log(abs(x), math.sqrt(3)); r = round(d); assert abs(d - r) < 1e-7 and r >= 0, (x, d); return r
rng = random.Random(7)
def rand_word(n, L): return [rng.choice([1, -1]) * rng.randint(1, n - 1) for _ in range(L)]
# plat
ok = 0; tot = 0; cnt = collections.Counter(); other = list({frozenset(L) for L in lines} - {L0}); mism_other = collections.Counter(); bad = []
tests = [rand_word(6, rng.randint(2, 13)) for _ in range(220)]
ls = [frozenset(L) for L in lines]
for wd in tests:
    b = bracket(wd, 6, "plat"); d = dim_from_abs(b); g = rep(wd); img = frozenset(g[p] for p in L0); m = len(L0 & img); pred = {4: 2, 1: 1, 0: 0}[m]
    tot += 1; ok += pred == d; cnt[d] += 1
    if pred != d: bad.append(wd)
    for t, Lx in enumerate(other[:3]):
        imx = frozenset(g[p] for p in Lx); mism_other[t] += {4: 2, 1: 1, 0: 0}[len(Lx & imx)] != d
out["plat_tests"] = tot; out["plat_agree"] = ok; out["plat_dim_counts"] = dict(cnt); out["plat_first_bad"] = bad[:3]; out["control_other_lines_mismatches"] = dict(mism_other)
# standard closure with reduced Burau at t = -1 over F_3
def burau(s, n):
    M = [[int(i == j) for j in range(n - 1)] for i in range(n - 1)]; i = abs(s) - 1; t = -1
    M[i][i] = -t
    if i > 0: M[i][i - 1] = t
    if i < n - 2: M[i][i + 1] = 1
    return M
def mm(a, b, p=3): return [[sum(a[i][k] * b[k][j] for k in range(len(b))) % p for j in range(len(b))] for i in range(len(a))]
def minv(a, p=3):
    n = len(a); M = [r[:] + [int(i == j) for j in range(n)] for i, r in enumerate(a)]
    for c in range(n):
        v = next(r for r in range(c, n) if M[r][c] % p); M[c], M[v] = M[v], M[c]; s = pow(M[c][c], -1, p); M[c] = [x * s % p for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] % p: f = M[r][c]; M[r] = [(x - f * y) % p for x, y in zip(M[r], M[c])]
    return [r[n:] for r in M]
def rank(a, p=3):
    M = [r[:] for r in a]; rk = 0
    for c in range(len(M[0])):
        v = next((r for r in range(rk, len(M)) if M[r][c] % p), None)
        if v is None: continue
        M[rk], M[v] = M[v], M[rk]; s = pow(M[rk][rk + 0] if False else M[rk][c], -1, p); M[rk] = [x * s % p for x in M[rk]]
        for r in range(len(M)):
            if r != rk and M[r][c] % p: f = M[r][c]; M[r] = [(x - f * y) % p for x, y in zip(M[r], M[rk])]
        rk += 1
    return rk
std = {}
for n in (3, 4, 5, 6):
    a = t_ = 0; cn = collections.Counter(); badn = []
    for _ in range(90):
        wd = rand_word(n, rng.randint(2, 12)); d = dim_from_abs(bracket(wd, n, "closure"))
        M = [[int(i == j) for j in range(n - 1)] for i in range(n - 1)]
        for s in wd:
            X = [[x % 3 for x in r] for r in burau(s, n)]; X = X if s > 0 else minv(X); M = mm(M, X)
        co = (n - 1) - rank([[(M[i][j] - int(i == j)) % 3 for j in range(n - 1)] for i in range(n - 1)]); t_ += 1; a += co == d; cn[d] += 1
        if co != d and len(badn) < 2: badn.append((wd, co, d))
    std[n] = dict(tests=t_, agree=a, dims=dict(cn), bad=badn)
out["standard_closure_vs_burau"] = std
known = dict(trefoil=([1, 1, 1], 2, 1), figure8=([1, -2, 1, -2], 3, 0), Hopf=([1, 1], 2, 0), unknot=([1], 2, 0), connected_sum_two_trefoils=([1, 1, 1, 2, 2, 2], 3, 2), T35=([1, 2] * 5, 3, 0))
out["known"] = {k: dict(got=dim_from_abs(bracket(v[0], v[1], "closure")), expected=v[2]) for k, v in known.items()}
print(json.dumps(out, default=str)); json.dump(out, open("knots_w33.json", "w"), indent=1, default=str)
