from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import w33_pass81_rotation_noise_tail_vm_classifier as pass81


def test_pass81_rotation_noise_tail_vm_classifier_payload() -> None:
    payload = pass81.build_payload()
    assert payload["status"] == "PASS"
    assert all(payload["checks"].values())

    rotation = payload["track1_k12_rotation_system"]
    assert rotation["counts"] == {
        "vertices": 12,
        "edges": 66,
        "faces": 44,
        "euler": -10,
        "genus": 6,
    }
    assert rotation["comparison_with_pass80_z_basis"]["face_boundary_rank"] == 43
    assert rotation["comparison_with_pass80_z_basis"]["pass80_z_rank"] == 47
    assert rotation["verified"] is True

    noisy = payload["track2_noisy_syndrome_simulator"]
    assert len(noisy["rows"]) == 36
    assert noisy["best_rows_at_p_0_001"]["0.01"]["rounds"] in [3, 5]
    assert all(noisy["checks"].values())

    tail = payload["track3_hashimoto_tail_gap"]
    assert tail["plus_eigenspace_dimension"] == 201
    assert tail["minus_eigenspace_dimension"] == 200
    assert tail["plus_dimension_sum"] == 201
    assert tail["minus_dimension_sum"] == 200

    vm = payload["track4_packet_vm_terwilliger_channels"]
    assert vm["terwilliger_op_count"] == 16
    assert all(vm["checks"].values())

    classifier = payload["track5_spence_universe_classifier"]
    assert classifier["classified_count"] == 28
    assert classifier["residual_after_local_plus_alpha"] == [[20, 24]]
    assert all(classifier["checks"].values())


def test_pass81_json_result_when_present() -> None:
    path = Path("w33_pass81_rotation_noise_tail_vm_classifier.json")
    if not path.exists():
        return
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["status"] == "PASS"
    assert payload["track1_k12_rotation_system"]["verified"] is True


if __name__ == "__main__":
    test_pass81_rotation_noise_tail_vm_classifier_payload()
    test_pass81_json_result_when_present()
