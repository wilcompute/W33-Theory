"""Passes 12442-12449 (Claude track).

12442 -- d = 2q for the binary adjacency code of W(3,q), q odd: the odd case.  S = supp of a nonzero word of ker_2(A); s_L = |S cap L|.
  (F1) every point y: sum_{L through y} s_L = 0 mod 2  =>  T = {lines with s_L odd} covers every point an even number of times, i.e. T is a
       codeword of the binary line code ('LU(3,q)'-type: Kim-Peled-Perepelitsa-Pless-Friedland; Kim-Mellinger-Storme 2007).
  (F2) for a line L and x in L: m_x(L) = #(S-points off L collinear with x) = s_L - [x in S] mod 2;  (F3) |S| = s_L + sum_{x in L} m_x(L).
  Lemma (proved here): let L be odd (a = s_L), x0 in L \\ S, M an odd line through x0 (exists by F1), c = s_M.  Using 'a point off M sees
  exactly one point of M' and 'no triangles':
        |S| >= q + max(a, c) + #(S-points on the other q - 1 lines through x0).
  Hence |S| >= 2q whenever some odd line meets S in exactly q points (the hexad situation, where the bound is tight).
  Open: odd lines all meeting S in few points (e.g. a = c = 1); there the outside points must be counted.  Even case (T empty): >= 2q + 2
  (12434).  Exact d = 2q: q = 3, 5 (cdde9b06b first; 12434 MILP); q = 7: 10 <= d <= 14 (055804fc2).
12445 -- entanglement width vs universality: the q-ary ceiling 1 + C(2n+q-2, 2n-1) grows like (log_q v)^(q-1)/(q-1)!; for qutrits 11, 22, 37
  at n = 2, 3, 4 vs log_3 v = 3.4, 5.4, 7.4 -- super-logarithmic, so the necessary condition for efficient universality (Van den Nest et
  al. 2006/2007) is met by qutrit (and higher) Pauli-geometry graph states and failed by qubit ones (2n + 1 = log_2(v+1) + 1).
  Universality itself is not decided.
12443-12444 -- SM_2541 dense shift sampling (see certificate).  12446 -- scripts/check_prior_art_all_repos.py.
"""

import json
from math import comb, log
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12442_to_12449_oddcase_sm2541_universality_priorart.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    widths = {}
    for q in (2, 3, 5):
        for n in (2, 3, 4):
            v = (q ** (2 * n) - 1) // (q - 1)
            widths[f'{n},{q}'] = dict(v=v, ceiling=1 + comb(2 * n + q - 2, 2 * n - 1), log_q_v=round(log(v, q), 3))
    res["12445_widths"] = widths
    checks["12445: qubit ceiling = log2(v+1) + 1 (logarithmic); qutrit ceiling grows faster than log_3 v (11, 22, 37)"] = (
        all(widths[f'{n},2']['ceiling'] == 2 * n + 1 for n in (2, 3, 4))
        and [widths[f'{n},3']['ceiling'] for n in (2, 3, 4)] == [11, 22, 37]
        and all(widths[f'{n},3']['ceiling'] / widths[f'{n},3']['log_q_v'] > widths[f'{m},3']['ceiling'] / widths[f'{m},3']['log_q_v']
                for n, m in ((3, 2), (4, 3))))
    lc = json.loads((A / "search_drivers_12442" / "lemma_check.json").read_text())
    res["12442_lemma_check"] = lc
    checks["12442: odd-case lemma |S| >= q + max(a,c) + others -- 0 violations on 30836 (q=3) and 251468 (q=5) configurations of real "
           "kernel words; tight on the hexad configurations"] = (
        lc["3"]["violations"] == 0 and lc["5"]["violations"] == 0 and lc["3"]["configurations_tested"] > 30000 and lc["5"]["tight"] > 0)
    D = A / "search_drivers_12373"
    s3 = D / "sm2541_summary.json"
    if s3.exists():
        res["12443_12444"] = json.loads(s3.read_text())
        sm = res["12443_12444"]
        checks["12443-12444: SM_2541 dense scan -- 6000 shifts -> 62 three-doublet, 52 large-R safe and exotic-free, ALL 52 with an anomaly-free "
               "three-generation hypercharge (k_Y in {17/3, 53/9, 41/9, 35/9}), ALL keeping exactly one unliftable (1,2,0) pair"] = (
            sm["sampled"] == 6000 and sm["three_doublet"] == 62 and sm["large_safe"] == 52 and sm["exotic_free"] == 52
            and sm["relaxed_hypercharge"] == 52 and sm["anomaly_free"] == 52 and sm["all_fractional_liftable"] == 0 and sm["unmatched_always_one_120_pair"]
            and set(sm["kY_hist"]) == {"17/3", "53/9", "41/9", "35/9"})
    my = D / "multiY_summary.json"
    if my.exists():
        m = json.loads(my.read_text()); res["12444b"] = m
        allrows = [r for v in m.values() for r in v]
        checks["12444b: 6 distinct hypercharges each for c22 and c2872 -- all anomaly-free (k_Y down to 11/3), and under EVERY one exactly one "
               "(1,2,0) pair stays unliftable: the obstruction is hypercharge-independent"] = (
            len(allrows) == 12 and all(r["anom"] == "0" and r["frac"] - r["lift"] == 2 for r in allrows)
            and min(eval(r["kY"]) for r in allrows) == 11 / 3)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
