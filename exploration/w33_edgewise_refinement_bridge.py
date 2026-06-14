"""Edgewise/Freudenthal-Kuhn replacement bridge for the CP2_9/K3_16 tower.

This module is the R3-safe replacement for the barycentric refinement count layer.
BT983 showed that barycentric refinement is not shape-regular, so the named
CMS/Dodziuk-Patodi/FEEC convergence theorems cannot be applied to that tower.
For a 4-simplex, edgewise k=2 refinement produces 2^4 = 16 shape-regular
4-simplices; barycentric refinement produces 5! = 120 and loses fatness.

The module deliberately records only what follows from the existing seed
f-vectors. Exact lower-dimensional incidence matrices require explicit CP2_9 and
K3_16 facet lists.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
import json
from math import comb
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_edgewise_refinement_bridge_summary.json"


@dataclass(frozen=True)
class EdgewiseSeedProfile:
    name: str
    vertices: int
    f_vector: tuple[int, int, int, int, int]
    euler_characteristic: int
    top_simplex_multiplier_per_step: int = 16
    shape_regular_tower: bool = True

    def top_simplices(self, level: int) -> int:
        return self.f_vector[4] * (self.top_simplex_multiplier_per_step ** level)

    def to_dict(self, max_level: int = 6) -> dict[str, Any]:
        data = asdict(self)
        data["levels"] = [
            {
                "level": r,
                "edgewise_top_4simplices": self.top_simplices(r),
                "mesh_width_scale": f"2^-{r}",
            }
            for r in range(max_level + 1)
        ]
        return data


def neighborly_4manifold_f_vector(n: int) -> tuple[int, int, int, int, int]:
    f0 = n
    f1 = comb(n, 2)
    f2 = comb(n, 3)
    f4 = (3 * f2 - 2 * f1) // 5
    f3 = 5 * f4 // 2
    return (f0, f1, f2, f3, f4)


def euler_characteristic(fv: tuple[int, int, int, int, int]) -> int:
    return sum(((-1) ** i) * fv[i] for i in range(5))


def cp2_edgewise_seed() -> EdgewiseSeedProfile:
    fv = neighborly_4manifold_f_vector(9)
    return EdgewiseSeedProfile("CP2_9", 9, fv, euler_characteristic(fv))


def k3_edgewise_seed() -> EdgewiseSeedProfile:
    fv = neighborly_4manifold_f_vector(16)
    return EdgewiseSeedProfile("K3_16", 16, fv, euler_characteristic(fv))


@lru_cache(maxsize=1)
def build_edgewise_refinement_summary() -> dict[str, Any]:
    seeds = [cp2_edgewise_seed(), k3_edgewise_seed()]
    return {
        "status": "ok",
        "tower": "edgewise/Freudenthal-Kuhn k=2",
        "dimension": 4,
        "top_simplex_multiplier_per_step": 16,
        "old_barycentric_top_multiplier_per_step": 120,
        "shape_regular_tower": True,
        "seeds": [s.to_dict() for s in seeds],
        "density_warning": (
            "Do not reuse barycentric density constants such as 120/19 or 860/19 "
            "for R3. Edgewise top growth is 16^r and lower-dimensional incidence "
            "densities must be recomputed from explicit CP2_9/K3_16 facets."
        ),
        "bridge_verdict": (
            "This is the theorem-carrier replacement for the curved external tower: "
            "edgewise refinement preserves shape-regularity, has mesh width 2^-r, "
            "and reduces top-dimensional growth by a factor (120/16)^r relative to "
            "the old barycentric tower."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_edgewise_refinement_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
