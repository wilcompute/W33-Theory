"""Pass 11901: the Kahler loophole for m_c = m_u is closed in all 12 SO(16)xSO(16) A8 survivors.

Background. In the 12 survivors (Passes 11095-11110) the three generations sit at the three fixed points of the
Wilson-line-free family torus. Pass 11105 D (Schur) and Pass 11109 (instanton Yukawas, diagonal moduli) give m_c = m_u,
and Pass 11103 showed that no alignment of the SM-neutral scalar vacuum splits them, naming "moduli-dependent Yukawa
couplings" as a possible escape. Pass 11900 found that the off-diagonal Kahler moduli do split a light pair, at third
order, but ONLY when left- and right-handed fields sit at different points (a != 0) of a Wilson-line torus.

Here:
  * From the frozen Pass 11103 coupling data: in all 12 models, for every light up- and down-type Higgs (72 rows), the
    renormalisable twisted triangles have geo = 0 for the top/bottom entry and geo = 1 for the two light entries (geo =
    number of tori on which the three fields are not at one point). So on BOTH Wilson-line tori Q, u^c (d^c) and H sit
    at the same point: a = 0.
  * With a = 0 the light entries are theta_(+1,0,0)(Z) and theta_(-1,0,0)(Z) of the full T6/Z3 Hermitian Kahler matrix
    Z (nine moduli). The instanton sum is even under x -> -x on all tori at once, so they are EQUAL for every Z
    (checked to 1e-15 for random 3x3 Hermitian Z, with a control: for a != 0 they differ at O(1)).
    Hence m_c = m_u and m_s = m_d hold for all nine Kahler moduli, off-diagonal ones included: the Kahler escape route
    of Pass 11103 is closed for the renormalisable couplings of the survivors.
  * The escape needs a != 0 on some Wilson-line torus. Because the Wilson-line classes of Q, u^c, H are common to all
    three families, the same a then enters the top coupling, which pays the instanton factor theta_(0,a)/theta_(0,0) of
    that torus (1/2 at the self-dual point, Pass 11109): a light-pair split is bought with a top suppression. This is a
    scan criterion for future models: a Yukawa triangle that is not single-pointed on some Wilson-line torus.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11897_11898_kahler_moduli_two_qutrit_weil as K  # noqa: E402

OUT = ROOT / "data" / "w33_pass11901_kahler_loophole_closed.json"
FROZEN = ROOT / "data" / "w33_pass11103_alignments_hidden_unbroken.json"
S3 = 1j * np.sqrt(3)


def theta_coset(Z, mu, O):
    x = [O + mu[i] / S3 for i in range(3)]
    X = np.stack(np.meshgrid(*x, indexing="ij"), -1).reshape(-1, 3)
    return np.exp(2j * np.pi * np.einsum("ni,ij,nj->n", X.conj(), Z, X)).sum()


def main():
    rng = np.random.default_rng(11901)
    d = json.loads(FROZEN.read_text())
    rows, patterns = 0, {}
    for m, r in d.items():
        for s in ("up", "down"):
            for row in r["res"][s]:
                rows += 1
                g = sorted(row["geo"].values())
                patterns[str(g)] = patterns.get(str(g), 0) + 1
    O = K.lattice(4)
    even, ctrl = [], []
    for _ in range(3):
        Z = K.rand_Z(rng, n=3, ymin=0.9, yscale=4.0)
        t1, t2 = theta_coset(Z, (1, 0, 0), O), theta_coset(Z, (2, 0, 0), O)
        even.append(float(abs(t1 - t2) / abs(t1)))
        c1, c2 = theta_coset(Z, (1, 1, 0), O), theta_coset(Z, (2, 1, 0), O)
        ctrl.append(float(abs(c1 - c2) / abs(c1)))
    # top cost: theta_(0,a) / theta_(0,0) on one torus along the imaginary axis
    O1 = K.lattice(10)
    cost = {}
    for y in (0.3, 0.5, 1.0, 2.0):
        th0 = np.exp(2j * np.pi * (1j * y) * abs(O1) ** 2).sum()
        th1 = np.exp(2j * np.pi * (1j * y) * abs(O1 + 1 / S3) ** 2).sum()
        cost[str(y)] = float(abs(th1 / th0))
    rho = -0.5 + 1j * np.sqrt(3) / 2
    th0 = np.exp(2j * np.pi * rho * abs(O1) ** 2).sum()
    th1 = np.exp(2j * np.pi * rho * abs(O1 + 1 / S3) ** 2).sum()
    cost["rho"] = float(abs(th1 / th0))
    res = dict(pass_id=11901, survivor_models=len(d), higgs_rows=rows, geo_patterns=patterns,
               even_light_entries_rel_diff=even, control_a_nonzero_rel_diff=ctrl, top_cost_theta_ratio=cost)
    res["checks"] = {k: bool(v) for k, v in dict(
        twelve_models=len(d) == 12,
        all_rows_single_pointed_on_wilson_tori=patterns == {"[0, 1, 1]": rows} and rows == 72,
        light_entries_equal_all_kahler_moduli=max(even) < 1e-12,
        control_a_nonzero_splits=min(ctrl) > 1e-3,
        top_cost_monotone=cost["0.3"] > cost["0.5"] > cost["1.0"] > cost["2.0"],
        same_normalisation_as_pass_11109=abs(cost["1.0"] - (np.sqrt(3) - 1) / 2) < 1e-12
        and abs(cost["2.0"] - 0.045) < 1e-3 and abs(cost["rho"] - 0.5) < 1e-12,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
