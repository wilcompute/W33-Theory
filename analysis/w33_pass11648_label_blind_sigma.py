"""Pass 11648: label-blind time II -- the label-sensitive arrows of a qutrit are exactly the arrows that survive on the
equal-spectra locus, with Hilbert series t^6 (1 + t - t^3) / ((1-t)(1-t^2)(1-t^3)).

Pass 11642: the label-blind arrows (S4-alternating functions of the four MUB outcome spectra) start at degree 9, and the
label-sensitive excess O_k - LB_k is 1, 2, 3, 4, 6, ... .
WHY THEY VANISH.  If two MUBs have equal spectra (the locus Sigma, real codimension 2), the transposition of their
labels fixes the spectral data, so every alternating function of the spectra vanishes there.  So LB is contained in the
odd invariants vanishing on Sigma, and dim(O_k restricted to Sigma) <= O_k - LB_k.
FOUND HERE.
  * Equality: the restriction of the full time-odd module to Sigma has dimension exactly O_k - LB_k for every degree
    k = 6..15 where the floating-point rank of the full module is certified (generic rank = O_k), and the values still
    match at k = 16, 17, 18 (numerical; random points on Sigma by Newton/least squares).  So the label-sensitive arrows
    are exactly what survives on states with two equal basis spectra.
  * Hilbert series (fitted to 20 values, degrees 6..25, three numerator terms):
        sum_k (O_k - LB_k) t^k = t^6 (1 + t - t^3) / ((1 - t)(1 - t^2)(1 - t^3)),
        sum_k LB_k t^k = (t^9 + t^10 + t^11 + t^12 - t^15 - t^16 - t^17 + t^19) / ((1-t)(1-t^2)(1-t^3)(1-t^4)(1-t^6)).
    The three-factor denominator matches a module supported on the 3-dimensional cone over Sigma.
  * A curiosity: every Z[omega] lattice point with entries a + b omega, |a|, |b| <= 3, lying on Sigma(Z, X) and with the
    other spectra distinct (1356 points) is time-symmetric: the whole odd module vanishes there through degree 20.
"""
import json, sys, itertools
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11648_label_blind_sigma.json"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import w33_pass11357_jarlskog_degree_by_dimension as P7
import w33_pass11434_h6_explicit as H
import w33_pass11534_time_arrow_module_exact as E
from scipy.optimize import least_squares
st, _ = H.stabiliser_states()
Cl = P7.clifford_group(3)
perms = H.group_permutations(Cl, st)
PM = np.array([p for p, _ in perms]); SG = np.array([s for _, s in perms], float)
# group stabiliser states into MUBs by orthogonality
G = np.abs(st.conj() @ st.T) ** 2
mubs = []
for i in range(12):
    if any(i in m for m in mubs): continue
    mubs.append([i] + [j for j in range(12) if j != i and G[i, j] < 1e-9])
assert len(mubs) == 4 and all(len(m) == 3 for m in mubs)
def probs(psi): return np.abs(st.conj() @ psi) ** 2
def R(m, odd, p):           # p: (pts,12)
    v = np.ones((len(PM), p.shape[0]))
    for i in m: v *= p[:, PM[:, i]].T
    w = SG if odd else np.ones(len(SG))
    return (w[:, None] * v).mean(0)
cert = json.load(open(ROOT / "data" / "w33_pass11534_time_arrow_module_exact.json"))
EG = {g: (v['degree'], v['monomial']) for g, v in cert['even_generators'].items()}
OG = {g: (v['degree'], v['monomial']) for g, v in cert['odd_generators'].items()}
def odd_basis_vals(k, p):
    ev = {g: R(m, False, p) for g, (d, m) in EG.items()}
    od = {g: R(m, True, p) for g, (d, m) in OG.items()}
    cols = []
    for g, (dg, _) in OG.items():
        if dg > k: continue
        for mon in E.monomials({e: d for e, (d, _) in EG.items()}, k - dg) if k > dg else [()]:
            v = od[g].copy()
            for e in mon: v = v * ev[e]
            cols.append(v)
    return np.stack(cols, 1)
def spec(p, b):
    q = p[:, mubs[b]]
    return q[:, 0]*q[:, 1] + q[:, 0]*q[:, 2] + q[:, 1]*q[:, 2], q.prod(1)
def sigma_points(N, a=0, b=1, seed=0):
    rng = np.random.default_rng(seed); out = []
    def f(x):
        psi = (x[:3] + 1j*x[3:]); psi = psi / np.linalg.norm(psi)
        p = probs(psi)[None]
        ea, pa = spec(p, a); eb, pb = spec(p, b)
        return np.array([ea[0]-eb[0], 100*(pa[0]-pb[0])])
    while len(out) < N:
        r = least_squares(f, rng.normal(size=6), xtol=1e-15, ftol=1e-15, gtol=1e-15)
        if np.abs(r.fun).max() < 1e-13:
            psi = r.x[:3] + 1j*r.x[3:]; out.append(psi/np.linalg.norm(psi))
    return np.array(out)
def rank(A, tol=1e-9):
    s = np.linalg.svd(A / np.abs(A).max(0, keepdims=True).clip(1e-300), compute_uv=False)
    return int((s > tol * s[0]).sum()), s


def stage_sigma(k_hi=18, n_sig=400):
    OKs = json.load(open(ROOT / "data" / "w33_pass11491_time_odd_molien.json"))["sequences"]["odd"]
    LBd = json.load(open(ROOT / "data" / "w33_pass11642_label_blind_time.json"))["by_degree"]
    rng = np.random.default_rng(1)
    gen = rng.normal(size=(600, 3)) + 1j * rng.normal(size=(600, 3))
    gen /= np.linalg.norm(gen, axis=1, keepdims=True)
    sig = sigma_points(n_sig)
    pg = np.array([probs(x) for x in gen])
    ps = np.array([probs(x) for x in sig])
    rows = {}
    for k in range(6, k_hi + 1):
        rg, _ = rank(odd_basis_vals(k, pg))
        rs, _ = rank(odd_basis_vals(k, ps))
        exc = OKs[k] - LBd[str(k)]["label_blind_odd"] if str(k) in LBd else None
        rows[k] = dict(O_k=OKs[k], generic_rank=rg, rank_on_Sigma=rs, excess=exc, certified=rg == OKs[k], equal=rs == exc)
        print(k, rows[k], flush=True)
    return rows


def stage_lb(D=25, npts=900):
    import sympy as sp
    import w33_pass11642_label_blind_time as LBm
    import w33_pass11534_time_arrow_module_exact as E
    t = sp.symbols("t")
    odd = sp.series(t ** 6 * (1 + t) / ((1 - t) * (1 - t ** 2) * (1 - t ** 3) * (1 - t ** 4) * (1 - t ** 6)), t, 0, D + 1).removeO()
    lb = LBm.LB(npts, 7)
    distinct = len({(int(a), tuple(sorted(zip(map(int, b), map(int, c))))) for a, b, c in zip(lb.n3, lb.e2, lb.P3)})
    rows = {}
    for k in range(9, D + 1):
        od = lb.space(k, True)
        r = E.rank_mod(np.stack(od, 1)) if od else 0
        rows[k] = dict(O_k=int(odd.coeff(t, k)), label_blind=r)
        print(k, rows[k], flush=True)
    return dict(rows=rows, distinct_spectral_points=distinct)


def fits(lbrows):
    import sympy as sp
    t = sp.symbols("t")
    X = t ** 6 * (1 + t - t ** 3) / ((1 - t) * (1 - t ** 2) * (1 - t ** 3))
    LBs = (t ** 9 + t ** 10 + t ** 11 + t ** 12 - t ** 15 - t ** 16 - t ** 17 + t ** 19) / (
        (1 - t) * (1 - t ** 2) * (1 - t ** 3) * (1 - t ** 4) * (1 - t ** 6))
    Ks = sorted(int(k) for k in lbrows)
    xs = sp.series(X, t, 0, max(Ks) + 1).removeO()
    ls = sp.series(LBs, t, 0, max(Ks) + 1).removeO()
    ok_x = all(int(xs.coeff(t, k)) == lbrows[k]["O_k"] - lbrows[k]["label_blind"] for k in Ks)
    ok_l = all(int(ls.coeff(t, k)) == lbrows[k]["label_blind"] for k in Ks)
    return dict(excess_series="t^6 (1 + t - t^3) / ((1-t)(1-t^2)(1-t^3))", excess_fit_all_degrees=ok_x,
                label_blind_series="(t^9+t^10+t^11+t^12-t^15-t^16-t^17+t^19)/((1-t)(1-t^2)(1-t^3)(1-t^4)(1-t^6))",
                label_blind_fit_all_degrees=ok_l, degrees=[min(Ks), max(Ks)])


def stage_lattice(R_=3, D=20):
    """all Z[omega] points with entries a + b omega, |a|, |b| <= R_, on Sigma(Z, X) with the other spectra distinct;
    exact mod-P rank of the whole odd module there (Pass 11534 generators)"""
    import w33_pass11534_time_arrow_module_exact as E
    PR = E.PR
    w3 = np.exp(2j * np.pi / 3)
    V = np.array([a + b * w3 for a in range(-R_, R_ + 1) for b in range(-R_, R_ + 1)])
    ids = np.array(list(itertools.product(range(len(V)), repeat=3)))
    psi = V[ids]
    q = np.rint(3 * np.abs(psi @ st.conj().T) ** 2).astype(np.int64)
    nz = np.abs(psi).sum(1) > 0

    def spec2(b):
        x = q[:, mubs[b]]
        return x[:, 0] * x[:, 1] + x[:, 0] * x[:, 2] + x[:, 1] * x[:, 2], x.prod(1)
    (ea, pa), (eb, pb), (ec, pc), (ed, pd) = (spec2(b) for b in range(4))
    on = nz & (ea == eb) & (pa == pb)
    gen = on & ~((ec == ed) & (pc == pd)) & ~((ea == ec) & (pa == pc)) & ~((ea == ed) & (pa == pd))
    P = psi[gen]
    qi = np.rint(3 * np.abs(P @ st.conj().T) ** 2).astype(np.int64) % PR
    PQ = np.stack([qi[:, perm] for perm, _ in perms])
    sgn = np.array([s for _, s in perms], np.int64)

    def rey(m, odd):
        vals = np.ones(PQ.shape[:2], np.int64)
        for i in m:
            vals = vals * PQ[:, :, i] % PR
        ww = sgn % PR if odd else np.ones(len(sgn), np.int64)
        return (ww[:, None] * vals % PR).sum(0) % PR * pow(432 * pow(3, len(m), PR) % PR, PR - 2, PR) % PR
    ev = {g: rey(m, False) for g, (dg, m) in EG.items()}
    od = {g: rey(m, True) for g, (dg, m) in OG.items()}
    ranks = {}
    for k in range(6, D + 1):
        cols = []
        for g, (dg, _) in OG.items():
            if dg > k:
                continue
            for mon in (E.monomials({e: dd for e, (dd, _) in EG.items()}, k - dg) if k > dg else [()]):
                v = od[g].copy()
                for e in mon:
                    v = v * ev[e] % PR
                cols.append(v)
        ranks[k] = E.rank_mod(np.stack(cols, 1))
    return dict(range=f"a + b omega, |a|, |b| <= {R_}", lattice_points=int(nz.sum()), on_Sigma_Z_X=int(on.sum()),
                with_other_spectra_distinct=int(gen.sum()), odd_module_rank_mod_P=ranks,
                all_time_symmetric=all(v == 0 for v in ranks.values()))


def main():
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    res = json.load(open(OUT)) if OUT.exists() else dict(pass_id=11648)
    if stage in ("sigma", "all"):
        res["sigma_restriction"] = stage_sigma()
        json.dump(res, open(OUT, "w"), indent=1, default=str)
    if stage in ("lb", "all"):
        lb = stage_lb()
        res["label_blind_mod_P"] = lb
        res["fits"] = fits(lb["rows"])
        json.dump(res, open(OUT, "w"), indent=1, default=str)
    if stage == "lattice":
        res["lattice_points_on_Sigma"] = stage_lattice()
        json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
