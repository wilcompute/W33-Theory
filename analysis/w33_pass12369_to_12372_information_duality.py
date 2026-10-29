"""Passes 12369-12372: the duality that ties c, mu0 and eps0, rebuilt on the two-qutrit space F_3^4 (Claude track).

Established anchors (cited, not claimed): premetric electrodynamics -- a constitutive map kappa on 2-forms with the closure relation
kappa^2 = -1 is (up to sign) the Hodge star of a Lorentzian metric, so the light cone (and c) follows from it (Obukhov-Hehl gr-qc/9904067;
Gross-Rubilar; Hehl-Obukhov book); for an isotropic vacuum the closure relation is mu0 eps0 c^2 = 1.  Geometric quantum mechanics -- state
space is Kahler: metric g = uncertainty/probability, symplectic omega = dynamics, complex structure J = g^{-1} omega = i (Ashtekar-Schilling
gr-qc/9706069); any two of (g, omega, J) fix the third.  alpha = Z0 / (2 R_K): vacuum impedance over twice the quantum Hall resistance
(CODATA 2022).  Constitutive laws (eps, mu, conductivity) are Hodge stars in the Tonti/Bossavit 'Maxwell house'.  In-corpus: the counts
21060 (hyperbolic) and 16848 (elliptic) of quadratic forms on F_3^4 already appear as weights of the quadratic code (BT5744, PASS4938).

12369 -- finite closure theorem.  On Lambda^2 F_3^4 with the wedge pairing P, ALL P-symmetric kappa with kappa^2 = -1 were enumerated
  exactly: 16848.  Every one is +-kappa_g for an ELLIPTIC metric g (each kappa from exactly two metrics, g and -g); hyperbolic metrics
  give kappa_g^2 = +1; no non-metric solution exists.  So over F_3, as over R, 'mu0 eps0 c^2 = 1' (closure) produces the light cone.
12370 -- the quantum i.  Metrics compatible with the W(3,3) form omega (J = g^{-1} omega, J^2 = -1): exactly 540 = |Sp(4,3)| / |GU(2,3)|,
  ALL hyperbolic; J^2 = +1 (para-Kahler): 1080, all hyperbolic; none elliptic.  The quantum i lives on hyperbolic ('Euclidean') metrics,
  the electromagnetic i on elliptic ('Lorentzian') ones: no metric on the two-qutrit space is both (finite twin of 'a Lorentzian metric
  is never Hermitian').  Both duality circles x + y J, x + y kappa with x^2 + y^2 = 1 are the order-4 group {+-1, +-i} = norm-1 F_9.
12371 -- duality acting on the contexts.  omega, read as a bivector, is a non-null 'field' (Pfaffian omega ^ omega = 1, the E.B analogue).
  No light cone fixes omega (0 of 16848), so electromagnetic duality never preserves the commutation geometry; it maps omega to a second
  commutation form kappa omega.  Contexts shared by the two: 16 (a hyperbolic quadric, a 4 x 4 grid) exactly when the second invariant
  P(omega, kappa omega) (the E^2 - B^2 analogue) vanishes -- 6480 'null' cones -- and 10 (an elliptic quadric, an ovoid) otherwise --
  10368 cones; checked cone by cone.  Sp(4,3) orbits on cones: 3240, 3240 (null, stabiliser 16), 2592 x 4 (stabiliser 20).
  Each of the 540 quantum structures J commutes (on bivectors) with exactly 288 light cones, 96 of each invariant class.
12372 -- dictionary (interpretation, labelled as such in the md): topological laws = counting (information), constitutive laws = Hodge
  stars (transfer/impedance); closure = 'c^2 mu0 eps0 = 1'; alpha = ratio of the impedance of the EM duality to that of a quantum channel.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12369_to_12372_information_duality.json"
D = ROOT / "analysis" / "search_drivers_12369"


def main():
    checks, res = {}, {}
    c = json.loads((D / "closure.json").read_text())
    res["12369"] = c
    checks["12369: 16848 closure solutions, all +-Hodge stars of elliptic metrics (2 metrics each); hyperbolic kappa_g^2 = +1; none exotic"] = (
        c["all_solutions"] == 16848 and c["metric_solutions"] == 16848 and c["nonmetric"] == 0 and c["metric_by_type"] == {"elliptic": 16848}
        and c["lambda_hist"] == {"('hyperbolic', 1)": 21060, "('elliptic', 2)": 16848} and c["metrics_per_kappa"] == {"2": 16848})
    k = json.loads((D / "kahler.json").read_text())
    res["12370_12371"] = k
    checks["12370: 540 Kahler (J^2=-1) and 1080 para-Kahler metrics for omega, all hyperbolic; 540 = 51840/96"] = (
        k["compatible"] == {"hyperbolic J^2=+1": 1080, "hyperbolic J^2=-1": 540} and 51840 // 96 == 540)
    # the duality circles: x + y X with X^2 = -1 and x^2 + y^2 = 1 over F_3 -- the norm-1 group of F_9
    circle = [(x, y) for x in range(3) for y in range(3) if (x * x + y * y) % 3 == 1]
    res["duality_circle"] = circle
    checks["12370: the duality circle {x + yX : x^2 + y^2 = 1} has order 4 = q + 1"] = len(circle) == 4
    lk = json.loads((D / "link.json").read_text()); ob = json.loads((D / "orbits.json").read_text()); jt = json.loads((D / "joint.json").read_text())
    res["12371"] = dict(link=lk, orbits=ob, joint=jt)
    checks["12371: no cone fixes omega; shared contexts 16 iff null invariant (6480) else 10 (10368); Sp orbits 3240x2 + 2592x4"] = (
        k["kappa_with_omega_eigen"] == 0 and k["W33_lines"] == 40 and k["klein_points"] == 130 and k["pfaffian_omega"] == 1
        and lk == {"(0, 16)": 6480, "(1, 10)": 5184, "(2, 10)": 5184} and ob["sp_order"] == 51840
        and sorted(o["size"] for o in ob["orbits"]) == [2592, 2592, 2592, 2592, 3240, 3240])
    checks["12371: each of the 540 quantum J commutes with 288 cones, 96 per invariant class"] = (
        jt["distinct_J"] == 540 and jt["omega_fixed"] == 540 and jt["commuting_per_J"] == {"288": 540}
        and jt["second_invariant"] == {"0": 51840, "1": 51840, "2": 51840})
    q = json.loads((ROOT / "analysis" / "search_drivers_12372" / "qca.json").read_text())
    res["12372_qca"] = q
    checks["12372b: Dirac QCA -- exact light cone; cos w = n cos k; rest frequency = arcsin m; group velocity <= n (= 1 if massless)"] = all(
        v["outside_cone"] == 0 and v["dispersion_err"] < 1e-12 and abs(v["w0"] - v["arcsin_m"]) < 1e-9 and v["vmax"] <= v["n"] + 1e-5
        for v in q.values()) and abs(q["0.0"]["vmax"] - 1) < 1e-6
    checks = {kk: bool(v) for kk, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
