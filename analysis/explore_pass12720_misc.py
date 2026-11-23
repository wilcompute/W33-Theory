"""Pass 12720 (2) and (5).
 (2) Vacuum stability with the newest inputs: M_t = 172.80 +- 0.26 (toponium-corrected global fit, arXiv:2603.28865) with 0 / 0.25 / 0.5 GeV
     scheme uncertainty, alpha_s PDG 0.1180(9) or FLAG 0.1183(7); M_t^c(alpha_s) from Pass 12709.  FCC-ee: preferred project (CERN Council,
     22 May 2026), final decision 2028; run order Z (4 yr), WW (2), ZH (3), ttbar (5): the threshold scan is ~9 years after the start.
 (5) Qutrit codes with measured hardware errors: best two-qutrit transmon gate 97.3% process fidelity (Goss et al. 2022) -> error 2.7%;
     typical two-qubit gate error 0.3-0.6%.  [[5,1,3]]_d: failure ~ C (f p)^2, per encoded bit ~ f^2 / log2 d: qutrits win only if f < sqrt(log2 3).
usage: py -3 analysis/explore_pass12720_misc.py"""
import json, math, os
from scipy.stats import norm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P09 = json.load(open(os.path.join(ROOT, "data", "toe_pass12709_round.json"), encoding="utf-8"))["stability"]
crit = {float(k): v for k, v in P09["Mt_crit"].items()}; dMc = P09["dMc_dalpha_s"]
res = {}
st = []
for a3, sa in ((0.1180, 0.0009), (0.1183, 0.0007)):
    mc = crit[0.118] + dMc * (a3 - 0.1180)
    for sch in (0.0, 0.25, 0.5):
        s = math.sqrt(0.26 ** 2 + sch ** 2 + (dMc * sa) ** 2)
        z = (mc - 172.80) / s
        st.append(dict(alpha_s=a3, scheme=sch, Mt_crit=mc, sigma=s, z=z, P_stable=float(norm.cdf(z))))
        print(f"(2) alpha_s {a3}, scheme {sch}: M_t^c = {mc:.2f}, sigma {s:.2f} -> {-z:.1f} sigma from stability, P(stable) = {norm.cdf(z):.1e}")
res["stability"] = dict(rows=st, fcc="FCC-ee preferred (May 2026), decision 2028; ttbar threshold ~9 yr after start (Z 4, WW 2, ZH 3)")

p2_lo, p2_hi, p3 = 0.003, 0.006, 0.027
qd = []
for p2 in (p2_lo, p2_hi):
    f = p3 / p2
    fail = lambda p: 1 - (1 - p) ** 5 - 5 * p * (1 - p) ** 4
    r = dict(p_qubit=p2, p_qutrit=p3, f=f, fail_qubit_per_bit=fail(p2), fail_qutrit_per_bit=fail(p3) / math.log2(3),
             ratio=fail(p3) / math.log2(3) / fail(p2))
    qd.append(r)
    print(f"(5) two-qubit error {p2:.1%} vs two-qutrit {p3:.1%} (f = {f:.1f}): [[5,1,3]] failure per encoded bit {r['fail_qubit_per_bit']:.1e} (qubit) vs "
          f"{r['fail_qutrit_per_bit']:.1e} (qutrit) -> qutrits {r['ratio']:.0f}x worse; break-even needs f < sqrt(log2 3) = {math.sqrt(math.log2(3)):.2f}")
res["qutrit"] = dict(rows=qd, break_even_f=math.sqrt(math.log2(3)), source="Goss et al. 2022 (Nat. Commun.), 97.3% two-qutrit CZ-type gate")
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12720_misc.json"), "w"), indent=1)
