"""Focused native-GAP regression for the Pass-4936 packet matrix units."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass4936_chamber_packet_matrix_units.g"
FROZEN = ROOT / "data" / "PART_W33_PASS4936_CHAMBER_PACKET_MATRIX_UNITS.json"
PASS_LINE = "Pass 4936 chamber packet matrix units: 20/20 checks; status=PASS"

EXPECTED_CHECKS = {
    "all_16_matrix_unit_laws",
    "carrier_ranks_24_24_48",
    "complex_switch_square",
    "hl_family_aggregate_reflection",
    "hp_family_aggregate_reflection",
    "line_carrier_packet_formula",
    "mode_switch_square",
    "new_units_span_same_algebra",
    "nilpotent_pair",
    "nilpotent_products_3840",
    "old_packet_algebra_dimension_4",
    "point_carrier_packet_formula",
    "reflection_anticommutator",
    "split_algebra_identity",
    "tag_mode_anticommutation",
    "tag_switch_square",
    "turn_characteristic_polynomial",
    "turn_corner_inverse",
    "turn_quadratic",
    "turn_rank_48_trace_minus_12",
}


def _assert_exact_payload(payload: dict[str, object]) -> None:
    assert payload["schema"] == "w33.pass4936.chamber_packet_matrix_units.v1"
    assert payload["status"] == "PASS"
    assert payload["objects"] == {
        "points": 40,
        "lines": 40,
        "chambers": 160,
        "packet_rank": 48,
        "lane_rank": 24,
        "matrix_algebra_dimension": 4,
    }
    assert payload["packet_basis"] == {
        "basis": ["Pi_48", "X", "Omega", "XOmega"],
        "relations": "X^2=6Pi_48, Omega^2=-60Pi_48, XOmega=-OmegaX",
        "point_carrier": "Q_p=(1/2)Pi_48+(1/8)X+(1/48)XOmega",
        "line_carrier": "Q_l=(1/2)Pi_48+(1/8)X-(1/48)XOmega",
    }
    assert payload["matrix_units"] == {
        "e11": "Q_p",
        "e22": "Pi_48-Q_p",
        "e12": (
            "(64/15)Q_p Q_l (Pi_48-Q_p)="
            "(10X-4Omega-XOmega)/30"
        ),
        "e21": (
            "(Pi_48-Q_p) Q_l Q_p="
            "(10X+4Omega-XOmega)/128"
        ),
        "multiplication": "e_ij e_kl=delta_jk e_il",
        "algebra": "M2(Q) acting on the multiplicity coordinate of V_24 tensor Q^2",
        "nilpotent_pair": (
            "N_plus=10X+4Omega-XOmega, N_minus=10X-4Omega-XOmega; "
            "N_plus^2=N_minus^2=0"
        ),
        "nilpotent_products": (
            "N_minus N_plus=3840e11, N_plus N_minus=3840e22"
        ),
    }
    assert payload["logic_switch"] == {
        "tag": "Z=e11-e22",
        "mode": "S=e12+e21",
        "relations": "Z^2=S^2=Pi_48, ZS=-SZ, (SZ)^2=-Pi_48",
        "reading": (
            "one exact rational two-state switch algebra repeated on "
            "24 representation lanes"
        ),
    }
    assert payload["holobox_panel_family_checksum"] == {
        "selector_sums": "HP0+HP1+HP2=P_panel, HL0+HL1+HL2=L_panel",
        "point_reflection": (
            "H_p=(Pi_48 P_panel Pi_48-Pi_48)/2=2Q_p-Pi_48"
        ),
        "line_reflection": (
            "H_l=(Pi_48 L_panel Pi_48-Pi_48)/2=2Q_l-Pi_48"
        ),
        "anticommutator": "H_p H_l+H_l H_p=-(1/2)Pi_48",
        "scope": (
            "chart-independent family aggregate only; "
            "no individual-selector intertwiner is asserted"
        ),
    }
    assert payload["aggregate_turn"] == {
        "operator": "T=H_p H_l",
        "quadratic": "2T^2+T+2Pi_48=0",
        "characteristic_polynomial": "t^112(t^2+(1/2)t+1)^24",
        "rank": 48,
        "trace": -12,
        "discriminant": "-15/4",
        "order": (
            "infinite on im(Pi_48): the irreducible minimal polynomial "
            "t^2+(1/2)t+1 is not cyclotomic and its roots are not "
            "algebraic integers"
        ),
    }
    assert payload["prior_art"] == [
        "Pass 4324 owns the four-dimensional chamber packet algebra",
        "Pass 4334 owns the point/line rank-24 carriers and squared angle 3/8",
        (
            "Pass 4777 owns the repository's earlier literal rational "
            "matrix-unit method on a different rank-40 residue block"
        ),
        (
            "PQP=tau P projection relations are standard Temperley-Lieb theory; "
            "this certificate claims only the explicit W33 packet instance"
        ),
    ]
    boundary = payload["boundary"]
    assert isinstance(boundary, str)
    assert "Individual HP/HL selector labels remain chart dependent" in boundary
    assert "No deterministic-selector packet intertwiner" in boundary
    assert "recursive-network composition law" in boundary
    assert payload["checks"] == {name: True for name in EXPECTED_CHECKS}


def test_native_gap_rebuild_matches_frozen_certificate(tmp_path: Path) -> None:
    gap = shutil.which("gap")
    assert gap is not None, "native GAP is required for Pass 4936"

    completed = subprocess.run(
        [gap, "-q", str(SOURCE)],
        cwd=tmp_path,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    assert completed.returncode == 0, completed.stdout[-6000:]
    assert PASS_LINE in completed.stdout.splitlines(), completed.stdout[-6000:]
    assert "Syntax warning" not in completed.stdout

    rebuilt = (
        tmp_path / "data" / "PART_W33_PASS4936_CHAMBER_PACKET_MATRIX_UNITS.json"
    )
    rebuilt_bytes = rebuilt.read_bytes()
    assert rebuilt_bytes == FROZEN.read_bytes()
    _assert_exact_payload(json.loads(rebuilt_bytes))
