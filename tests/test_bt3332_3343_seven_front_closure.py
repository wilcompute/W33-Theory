import base64,importlib.util,json,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('bt',ROOT/'analysis/bt3332_3343_seven_front_closure.py')
BT=importlib.util.module_from_spec(SPEC); assert SPEC.loader; SPEC.loader.exec_module(BT)
def frozen(path):
    return json.loads(zlib.decompress(base64.b64decode((ROOT/path).read_text(encoding='ascii'))))
def test_frozen_certificate_and_manifest():
    got,manifest=BT.build_results()
    assert got==frozen(Path('data/PART_BT3332_BT3343_SEVEN_FRONT_CLOSURE_results.json.zlib.b64'))
    assert manifest==frozen(Path('data/PART_BT3332_BT3343_FAULT_ROUTE_manifest.json.zlib.b64'))
    assert got['checks_passed']==got['checks_total']==18
    assert got['pass3338_3339_guard_fault_recovery']['two_bit_recovery_tag']['exhaustive_decode_cases']==352
