"""Global artanh-type log expansion for the completed cyclotomic defect package."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_dirichlet_log_artanh,
    completed_defect_dirichlet_log_artanh_profile,
)


PROFILE_LIMITS = [31, 1000, 10000, 100000, 1000000]
S_VALUES = [0.5, 1.0, 2.0]
MAX_TERMS = 8


def build_payload() -> dict[str, object]:
    profile = completed_defect_dirichlet_log_artanh_profile(PROFILE_LIMITS, S_VALUES, max_terms=MAX_TERMS)
    return {
        "profile": profile,
        "summary": {
            "statement": (
                "The logarithm of the completed defect Dirichlet package admits an exact artanh expansion: log Dhat_X(s) = 2 Sum_p [atanh((p^{-s}-1)/(p-1)) + (p^{-s}-1) log(1-1/p)]. "
                "Because |p^{-s}-1| < p-1 for every split prime p>=7 and Re(s)>0, this global log has an absolutely convergent odd-power series in the centered spectral variables u_p = p^{-s}-1."
            ),
            "largest_cutoff_exact_logs": {
                str(s): {
                    "real": completed_defect_dirichlet_log_artanh(PROFILE_LIMITS[-1], s).real,
                    "imag": completed_defect_dirichlet_log_artanh(PROFILE_LIMITS[-1], s).imag,
                    "series_error": profile[str(s)][-1]["abs_series_error"],
                }
                for s in S_VALUES
            },
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_artanh_log_expansion.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = Path("PART_MCIII_cyclotomic_artanh_log_expansion_results.json")
    result.write_text(json.dumps(payload["summary"], indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) CYCLOTOMIC GLOBAL ARTANH LOG EXPANSION")
    print("=" * 88)
    for s_key, rows in payload["profile"].items():
        print(f"s={s_key}: exact_log={rows[-1]['exact_log_real']} + {rows[-1]['exact_log_imag']}i ; series_error={rows[-1]['abs_series_error']}")
    print(f"wrote {out}")
    print(f"wrote {result}")


if __name__ == "__main__":
    main()
