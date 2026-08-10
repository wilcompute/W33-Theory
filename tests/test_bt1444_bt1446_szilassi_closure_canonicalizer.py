import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / 'tools' / script)], check=True, cwd=ROOT)
    return json.loads((ROOT / 'data' / data).read_text(encoding="utf-8"))


def test_bt1444_szilassi_fixed_face_extractor():
    result = run_tool('bt1444_szilassi_fixed_face_extractor.py', 'bt1444_szilassi_fixed_face_extractor.json')
    assert result['verified'] is True
    assert result['checks']['same_fixed_face_index'] is True
    assert result['realizations'][0]['fixed_face_index'] == 4
    assert result['realizations'][0]['fixed_face_vertices'] == [11, 9, 12, 10, 8, 13]
    assert result['realizations'][0]['boundary_cyclic_shift'] == 3


def test_bt1445_closure_orientation_transport():
    result = run_tool('bt1445_closure_orientation_transport.py', 'bt1445_closure_orientation_transport.json')
    assert result['verified'] is True
    assert result['boundary_shift'] == 3
    assert result['opposite_pairs'] == [[11, 10], [9, 8], [12, 13]]
    assert result['checks']['guard_bins_are_24'] is True
    assert result['checks']['transport_lands_in_168_bus'] is True


def test_bt1446_frobenius_involution_canonicalizer():
    result = run_tool('bt1446_frobenius_involution_canonicalizer.py', 'bt1446_frobenius_involution_canonicalizer.json')
    assert result['verified'] is True
    assert result['canonical_choice']['involution']['fixed'] == [4]
    assert result['canonical_choice']['involution']['pairs'] == [[0, 1], [2, 6], [3, 5]]
    assert len(result['canonical_strand_order']) == 12
    assert len(result['canonical_fano_flag_order']) == 21
