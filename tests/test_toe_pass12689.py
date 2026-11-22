"""Pass 12689: radius-independent y' in completion B; completion A scalar; prediction matrix."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12689_completion_matrix.json")))


def test_yprime_nearly_radius_independent():
    ys = [r["y_prime"] for r in D["completion_B_yprime_of_R"]["rows"]]
    assert 0.49 < min(ys) < max(ys) < 0.535 and max(ys) - min(ys) < 0.04
    assert ys == sorted(ys)          # monotone in R


def test_completion_A_and_matrix():
    assert 1e8 < D["completion_A"]["m_s_natural_GeV"] < 1e9
    assert len(D["matrix"]) == 8 and any(m["observable"] == "dark matter" for m in D["matrix"])
