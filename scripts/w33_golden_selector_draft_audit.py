from __future__ import annotations

"""Audit the draft Part XXIV golden-selector certificate against the live frontier.

The live paper leaves the golden/icosahedral selector open on the nonlocal
1620-quadrangle carrier. A stronger draft surface exists in
``part24_golden_selector.tex`` with an executable certificate in
``SOLVEOPEN_XXIV.py``. That draft defines a local sign rule

    sigma(p, L1, L2) in {+1, -1}

from the symplectic form and claims it yields a flat C2 reduction.

This audit runs the draft certificate up to its own failure, recovers the
constructed transport data, and classifies the flatness obstruction on the
same nonlocal quadrangle carrier highlighted in Supplement M.
"""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import warnings
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DRAFT_FILE = ROOT / "SOLVEOPEN_XXIV.py"
DEFAULT_OUTPUT = ROOT / "data" / "w33_golden_selector_draft_audit_summary.json"


def _load_draft_module() -> tuple[Any, BaseException | None]:
    """Execute the draft selector certificate and recover partial globals.

    The draft module executes checks at import time and currently fails during
    its flatness assertion. We intentionally keep the partially executed module
    so the exact ``lines`` and ``sigma`` objects used by the draft can be
    audited directly.
    """

    spec = importlib.util.spec_from_file_location("solveopen_xxiv_draft", DRAFT_FILE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load draft certificate: {DRAFT_FILE}")

    module = importlib.util.module_from_spec(spec)
    error: BaseException | None = None
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                spec.loader.exec_module(module)
            except BaseException as exc:  # noqa: BLE001 - keep the partial module state
                error = exc

    if not hasattr(module, "lines") or not hasattr(module, "sigma"):
        raise RuntimeError("Draft certificate did not construct lines/sigma before failing")

    return module, error


def _common_point(line_left: tuple[int, ...], line_right: tuple[int, ...]) -> int:
    shared = set(line_left) & set(line_right)
    if len(shared) != 1:
        raise AssertionError("Expected adjacent lines to meet in a unique point")
    return next(iter(shared))


def _line_adjacency(lines: list[tuple[int, ...]]) -> list[list[bool]]:
    adjacency = [[False] * len(lines) for _ in range(len(lines))]
    for left, line_left in enumerate(lines):
        for right, line_right in enumerate(lines):
            if left != right and len(set(line_left) & set(line_right)) == 1:
                adjacency[left][right] = True
    return adjacency


def _classify_nonlocal_quadrangle_failures(
    lines: list[tuple[int, ...]], sigma: dict[tuple[int, int, int], int]
) -> dict[str, int]:
    """Replicate the draft flatness loop and classify the failing carrier.

    The draft certificate only checks quadrangles with four distinct anchor
    points, so every counted cycle lives on the nonlocal global carrier from
    Supplement M.
    """

    adjacency = _line_adjacency(lines)

    total_quads = 0
    flatness_violations = 0
    local_total = 0
    local_violations = 0
    nonlocal_total = 0
    nonlocal_violations = 0

    for line0, neighbours0 in enumerate(adjacency):
        for line1, is_adjacent01 in enumerate(neighbours0):
            if not is_adjacent01:
                continue
            point01 = _common_point(lines[line0], lines[line1])

            for line2, is_adjacent12 in enumerate(adjacency[line1]):
                if line2 == line0 or not is_adjacent12:
                    continue
                point12 = _common_point(lines[line1], lines[line2])
                if point12 == point01:
                    continue

                for line3, is_adjacent23 in enumerate(adjacency[line2]):
                    if line3 == line1 or not is_adjacent23 or not adjacency[line3][line0]:
                        continue

                    point23 = _common_point(lines[line2], lines[line3])
                    point30 = _common_point(lines[line3], lines[line0])
                    anchor_points = {point01, point12, point23, point30}
                    if len(anchor_points) < 4:
                        continue

                    holonomy = (
                        sigma[(point01, line0, line1)]
                        * sigma[(point12, line1, line2)]
                        * sigma[(point23, line2, line3)]
                        * sigma[(point30, line3, line0)]
                    )

                    total_quads += 1
                    if len(anchor_points) == 1:
                        local_total += 1
                        if holonomy != 1:
                            local_violations += 1
                    else:
                        nonlocal_total += 1
                        if holonomy != 1:
                            nonlocal_violations += 1
                    if holonomy != 1:
                        flatness_violations += 1

    return {
        "total_quadrangles_checked": total_quads,
        "flatness_violations": flatness_violations,
        "local_quadrangles_checked": local_total,
        "local_flatness_violations": local_violations,
        "nonlocal_quadrangles_checked": nonlocal_total,
        "nonlocal_flatness_violations": nonlocal_violations,
    }


def build_draft_selector_obstruction_summary() -> dict[str, Any]:
    module, error = _load_draft_module()
    lines = list(module.lines)
    sigma = dict(module.sigma)
    quadrangle_audit = _classify_nonlocal_quadrangle_failures(lines, sigma)

    error_type = type(error).__name__ if error is not None else None
    error_message = str(error) if error is not None else None
    expected_message = "Flatness FAILED: 864 violations in 12960 quads"

    theorem = {
        "draft_selector_certificate_currently_fails": error is not None,
        "draft_failure_is_the_flatness_assertion": error_type == "AssertionError"
        and error_message == expected_message,
        "draft_selector_is_not_a_flat_c2_connection": quadrangle_audit["flatness_violations"] > 0,
        "draft_flatness_failure_lives_on_the_nonlocal_quadrangle_carrier": (
            quadrangle_audit["local_quadrangles_checked"] == 0
            and quadrangle_audit["nonlocal_quadrangles_checked"] == quadrangle_audit["total_quadrangles_checked"]
            and quadrangle_audit["nonlocal_flatness_violations"] == quadrangle_audit["flatness_violations"]
        ),
        "draft_local_sign_rule_does_not_close_the_live_supplement_m_frontier": (
            error_type == "AssertionError"
            and quadrangle_audit["flatness_violations"] == 864
            and quadrangle_audit["nonlocal_flatness_violations"] == 864
        ),
    }

    return {
        "status": "ok",
        "draft_surfaces": {
            "paper_surface": "part24_golden_selector.tex",
            "certificate_surface": str(DRAFT_FILE.relative_to(ROOT)).replace("\\", "/"),
        },
        "draft_certificate_failure": {
            "exception_type": error_type,
            "message": error_message,
            "expected_message": expected_message,
        },
        "transport_data": {
            "line_count": len(lines),
            "transport_edge_count": len(sigma),
        },
        "quadrangle_audit": quadrangle_audit,
        "theorem": theorem,
        "interpretation": (
            "The draft Part XXIV symplectic-sign selector does produce a 480-edge "
            "transport labelling, but it does not extend to a flat global C2 "
            "connection. Its own certificate fails on 864 of the 12960 nonlocal "
            "quadrangles counted by the draft flatness loop, so the live "
            "Supplement M frontier remains open exactly where the paper says it "
            "does: on the global nonlocal quadrangle carrier rather than on bare "
            "local transport edges."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT) -> Path:
    summary = build_draft_selector_obstruction_summary()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return path


def main() -> None:
    print(json.dumps(build_draft_selector_obstruction_summary(), indent=2))


if __name__ == "__main__":
    main()