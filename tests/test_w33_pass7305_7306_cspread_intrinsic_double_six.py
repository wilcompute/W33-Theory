import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis" / "w33_pass7305_7306_cspread_intrinsic_double_six.py"
CERTIFICATE = ROOT / "data" / "PART_W33_PASS7305_7306_CSPREAD_INTRINSIC_DOUBLE_SIX.json"

EXPECTED_WEIGHT_ENUMERATOR = {
    "0": 1,
    "5": 27,
    "8": 135,
    "10": 216,
    "11": 1080,
    "12": 1200,
    "13": 3285,
    "14": 10800,
    "15": 21168,
    "16": 33210,
    "17": 59760,
    "18": 117000,
    "19": 167400,
    "20": 167904,
    "21": 193230,
    "22": 272160,
    "23": 272160,
    "24": 193230,
    "25": 167904,
    "26": 167400,
    "27": 117000,
    "28": 59760,
    "29": 33210,
    "30": 21168,
    "31": 10800,
    "32": 3285,
    "33": 1200,
    "34": 1080,
    "35": 216,
    "37": 135,
    "40": 27,
    "45": 1,
}

EXPECTED_PROFILE_COUNTS = {
    (("0", 3), ("1", 10), ("2", 8), ("3", 5), ("4", 1)): 12960,
    (("1", 12), ("2", 12), ("3", 3)): 3240,
    (("0", 2), ("1", 10), ("2", 10), ("3", 5)): 2592,
    (("0", 4), ("1", 8), ("2", 8), ("3", 7)): 1620,
    (("0", 6), ("1", 9), ("2", 6), ("3", 3), ("5", 3)): 720,
    (("0", 12), ("3", 15)): 36,
}


def test_pass7305_7306_exact_replay_is_byte_stable():
    before = CERTIFICATE.read_bytes()
    completed = subprocess.run(
        [sys.executable, str(PRODUCER)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert '"status": "PASS"' in completed.stdout
    assert '"enumerated_words": 2097152' in completed.stdout
    assert CERTIFICATE.read_bytes() == before

    data = json.loads(before)
    assert data["status"] == "PASS"
    assert data["passes"] == "7305-7306"
    code = data["Cspread"]
    assert code["parameters"] == "[45,21,5]_2"
    assert code["rank"] == 21
    assert code["enumerated_words"] == 2**21
    assert code["weight_enumerator"] == EXPECTED_WEIGHT_ENUMERATOR
    assert sum(code["weight_enumerator"].values()) == 2**21
    assert code["minimum_shell_size"] == 27
    assert code["minimum_shell_equals_27_spread_generators"] is True
    assert code["weight15_shell_size"] == 21168

    profile_counts = {
        tuple(sorted(row["minimum_shell_intersection_histogram"].items())): row["count"]
        for row in data["weight15_minimum_shell_profiles"]
    }
    assert profile_counts == EXPECTED_PROFILE_COUNTS
    assert sum(profile_counts.values()) == 21168

    selector = data["intrinsic_selector"]
    assert selector == {
        "definition": "weight 15 and minimum-shell intersection histogram {0:12,3:15}",
        "selected_words": 36,
        "unique_profile_class_of_size_36": True,
        "uses_only_Cspread_and_its_minimum_shell": True,
    }
    identification = data["double_six_identification"]
    assert identification["current_N_columns"] == 36
    assert identification["N_column_weight"] == 15
    assert identification["selected_set_equals_current_N_columns"] is True

    graph = data["intrinsic_pair_intersection_graph"]
    assert graph["pair_intersections"] == {"3": 270, "6": 360}
    assert graph["parameters"] == "SRG(36,20,10,12)"
    assert graph["degrees"] == {"20": 36}
    assert graph["adjacent_common_neighbors"] == {"10": 360}
    assert graph["nonadjacent_common_neighbors"] == {"12": 270}
    assert graph["equals_current_H36_objectwise_under_N_column_labels"] is True

    boundary = data["prior_art_boundary"]
    assert "Pass7182_7184" in boundary
    assert "Pass7225_7248" in boundary
    assert "converse intrinsic characterization" in boundary["new_here"]
    assert boundary["scope"].startswith("Exact finite coding/incidence theorem only")
