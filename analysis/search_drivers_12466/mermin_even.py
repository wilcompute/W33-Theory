"""12529: are minimal even line sets parity proofs?  Field reduction: W(3,q), q = 2^k, sits in the 2k-qubit Pauli group via (x, y) -> Tr_{F_q/F_2}; an F_q-line is a Lagrangian (a context of 2k-qubit Paulis).
An even set S is a noncontextual-assignable iff there is v: Paulis in S -> F_2 with v(a) + v(b) + v(a + b) = beta(a, b) for commuting a, b in one context, where P_a P_b = (-1)^beta P_{a+b}.  This is an exact linear system over F_2.
Control: q = 2 must be solvable on a single context and unsolvable on the 6-line set (the Mermin-Peres square).  Run the whole binary code at q = 2 and 4 (each codeword classified), the grids at q = 4, 8.  Odd q is not tested here: symmetric Weyl operators multiply without phase on commuting pairs, so v = 0 solves the analogous system (cf. Gross).
usage: py -3 mermin_even.py"""
import collections, itertools, json
from symmetric_even_sets_gf import setup
from symmetric_fast import fast_build


def pauli_phase(a, b, n):
    """Hermitian Paulis, a = (x|z) with x, z in F_2^n: P_a = i^{x.z} X^x Z^z.  For commuting a, b, P_a P_b = (-1)^beta P_{a+b}.  Exact, by exponents of i."""
    x1, z1 = a[:n], a[n:]; x2, z2 = b[:n], b[n:]
    x3 = [p ^ q for p, q in zip(x1, x2)]; z3 = [p ^ q for p, q in zip(z1, z2)]
    e = sum(p & q for p, q in zip(x1, z1)) + sum(p & q for p, q in zip(x2, z2)) + 2 * sum(p & q for p, q in zip(z1, x2)) - sum(p & q for p, q in zip(x3, z3))
    e %= 4; assert e in (0, 2), "commuting pair expected"
    return e // 2


def trace_setup(q):
    F, add, mul, inv, neg = setup(q)
    k = {2: 1, 4: 2, 8: 3}[q]
    # an F_2 basis of F_q and the trace map, by powers of Frobenius
    def fr(x): return mul[x][x]
    def tr(x):
        t, y = x, x
        for _ in range(k - 1):
            y = fr(y); t = add[t][y]
        return t
    assert all(tr(x) in (0, 1) for x in F)
    basis = None
    for b in itertools.combinations([x for x in F if x], k):
        span = set()
        for c in itertools.product((0, 1), repeat=k):
            s = 0
            for ci, bi in zip(c, b):
                if ci: s = add[s][bi]
            span.add(s)
        if len(span) == q: basis = b; break
    # dual basis under the trace form, so that the F_2 coordinates of y are read off against those of x as a standard symplectic form
    dual = []
    for i in range(k):
        dual.append(next(d for d in F if all(tr(mul[d][basis[j]]) == int(i == j) for j in range(k))))
    def coords(x, B):
        for c in itertools.product((0, 1), repeat=k):
            s = 0
            for ci, bi in zip(c, B):
                if ci: s = add[s][bi]
            if s == x: return c
        raise ValueError
    return F, add, mul, tr, basis, dual, coords, k


def analyse(q, label, sets_of_lines, B):
    F, add, mul, tr, basis, dual, coords, k, pts, lines = B
    # W(3,q) form: x0 y2 - x2 y0 + x1 y3 - x3 y1; so (x0, x1) carry X and (x2, x3) carry Z after the trace form
    def vec2(v):
        # x coordinates in the basis; z coordinates in the dual basis, so the F_2 symplectic product equals Tr of the F_q form
        return tuple(coords(v[0], basis)) + tuple(coords(v[1], basis)) + tuple(coords(v[2], dual)) + tuple(coords(v[3], dual))
    n = 2 * k; res = collections.Counter(); examples = {}
    for name, S in sets_of_lines:
        var = {}; eqs = []
        for j in S:
            allv = []
            ps = [pts[p] for p in lines[j]]
            for p in ps:
                for c in F:
                    if c: allv.append(vec2(tuple(mul[c][t] for t in p)))
            allv = sorted(set(allv)); assert len(allv) == q * q - 1
            for a, b in itertools.combinations(allv, 2):
                ab = tuple(x ^ y for x, y in zip(a, b))
                if ab < b: continue
                beta = pauli_phase(a, b, n)
                row = 0
                for t in (a, b, ab): row ^= 1 << var.setdefault(t, len(var))
                eqs.append((row, beta))
        piv = {}; ok = True
        for row, rhs in eqs:
            while row:
                h = row.bit_length() - 1
                if h in piv:
                    pr, pb = piv[h]; row ^= pr; rhs ^= pb
                else:
                    piv[h] = (row, rhs); break
            if not row and rhs: ok = False; break
        res[("noncontextual" if ok else "CONTEXTUAL", len(S))] += 1
        examples.setdefault(name, ok)
    return dict(q=q, label=label, classes={f"{a}|{b}": c for (a, b), c in res.items()}, sample=examples if len(examples) < 8 else None)


def nullspace_words(lines, npts, limit):
    """all codewords of ker_2 N when small, as line-index sets."""
    rows = []
    for p in range(npts):
        r = 0
        for j, L in enumerate(lines):
            if p in L: r |= 1 << j
        rows.append(r)
    m = len(lines); piv = {}
    for r in rows:
        while r:
            h = r.bit_length() - 1
            if h in piv: r ^= piv[h]
            else: piv[h] = r; break
    free = [j for j in range(m) if j not in piv]; basis = []
    for f in free:
        x = 1 << f
        for h in sorted(piv):
            if bin(piv[h] & x & ~(1 << h)).count("1") % 2: x |= 1 << h
        basis.append(x)
    assert all(bin(x & r).count("1") % 2 == 0 for x in basis for r in rows)
    return basis


out = []
for q in (2, 4, 8):
    F, add, mul, tr, basis, dual, coords, k = trace_setup(q)
    pts, lines = fast_build(q)
    B = (F, add, mul, tr, basis, dual, coords, k, pts, lines)
    # check the F_2 symplectic product is the trace of the F_q form on the 40-type points: every line is F_2-isotropic
    words = nullspace_words(lines, len(pts), 0); dim = len(words)
    sets_ = []
    if q == 2:
        sets_ = [("line", [0])]
    wlist = []
    if dim <= 22:
        for mask in range(1, 1 << dim):
            x = 0
            for i in range(dim):
                if mask >> i & 1: x ^= words[i]
            wlist.append(x)
        best = min(bin(x).count("1") for x in wlist)
        minimal = [x for x in wlist if bin(x).count("1") == best]
    else:
        best, minimal = None, []
    rec = dict(q=q, code_dim=dim, min_weight=best, minimal_words=len(minimal))
    if q == 2:
        rec["single_context"] = analyse(q, "one line", [("line", [0])], B)["classes"]
        rec["all_words"] = analyse(q, "all words", [(str(x), [j for j in range(len(lines)) if x >> j & 1]) for x in wlist], B)["classes"]
    if q == 2:
        rec["contextual_iff_weight_2_mod_4"] = all(("CONTEXTUAL|" + str(bin(x).count("1")) in analyse(q, "x", [("s", [j for j in range(len(lines)) if x >> j & 1])], B)["classes"]) == (bin(x).count("1") % 4 == 2) for x in wlist)
    elif q == 4:
        rec["minimal_words_classified"] = analyse(q, "minimal", [(str(x), [j for j in range(len(lines)) if x >> j & 1]) for x in minimal[:60]], B)["classes"]
        rec["basis_words_classified"] = analyse(q, "basis", [(str(x), [j for j in range(len(lines)) if x >> j & 1]) for x in words[:40]], B)["classes"]
        # controls and minimal contextual subsets
        import random
        rng = random.Random(4); sets_all = [set(L) for L in lines]
        isC = lambda T: "CONTEXTUAL|" + str(len(T)) in analyse(q, "x", [("s", T)], B)["classes"]
        rec["one_line_contextual"] = isC([0]); m = next(j for j in range(1, len(lines)) if sets_all[0] & sets_all[j]); rec["two_meeting_lines_contextual"] = isC([0, m])
        grow = []
        for trial in range(6):
            order = rng.sample(range(len(lines)), len(lines)); T = []
            for j in order:
                T.append(j)
                if len(T) >= 2 and isC(T): break
            core = T[:]
            for j in T:
                U = [x for x in core if x != j]
                if len(U) >= 1 and isC(U): core = U
            grow.append(dict(first_contextual_at=len(T), irreducible_core=len(core), core_graph_edges=sum(1 for a, b in itertools.combinations(core, 2) if sets_all[a] & sets_all[b]), core=core))
        rec["irreducible_contextual_cores"] = grow; rec["smallest_core"] = min(g["irreducible_core"] for g in grow)
    out.append(rec); print(rec, flush=True)
json.dump(out, open("mermin_even.json", "w"), indent=1, default=str)
