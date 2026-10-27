"""12330b: common-threshold scan M_X = 1e3 ... 1e16 GeV (SM below, the candidate's full spectrum above): k_Y needed where alpha_2 =
alpha_3, kept only where the crossing is perturbative (1/alpha > 0) and below 1e19 GeV.  Does any threshold give k_Y = 8/3?"""
import json, math
b = json.load(open('beta.json'))['b_full']
bF = dict(Y=eval(b['bY']), two=eval(b['b2']), three=eval(b['b3']))
MZ = 91.1876; ainv_em, s2, as_ = 127.95, 0.2312, 0.1180
a = dict(Y=1 / ainv_em / (1 - s2), two=1 / ainv_em / s2, three=as_)
bSM = dict(Y=41 / 6, two=-19 / 6, three=-7)
rows = []
for e in [3 + 0.25 * i for i in range(53)]:
    MX = 10 ** e
    def inv(i, mu):
        x = 1 / a[i] - bSM[i] / (2 * math.pi) * math.log(min(mu, MX) / MZ)
        if mu > MX: x -= bF[i] / (2 * math.pi) * math.log(mu / MX)
        return x
    lo, hi = math.log(MZ * 1.001), math.log(1e19)
    f = lambda L: inv('two', math.exp(L)) - inv('three', math.exp(L))
    if f(lo) * f(hi) > 0:
        rows.append(dict(log10MX=e, crossing=None)); continue
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0: hi = mid
        else: lo = mid
    M = math.exp(lo); ai = inv('two', M)
    rows.append(dict(log10MX=e, log10crossing=math.log10(M), alpha_inv=ai, perturbative=ai > 0 and inv('Y', M) > 0, k_needed=inv('Y', M) / ai))
pert = [r for r in rows if r.get('perturbative')]
ks = [r['k_needed'] for r in pert]
out = dict(rows=rows, perturbative_k_range=[min(ks), max(ks)] if ks else None, reaches_8_3=any(abs(k - 8 / 3) < 0.05 for k in ks))
print('perturbative crossings:', len(pert), 'k range', out['perturbative_k_range'], 'reaches 8/3:', out['reaches_8_3'])
json.dump(out, open('scan.json', 'w'), indent=1)
