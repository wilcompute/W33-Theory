#!/usr/bin/env python3
from pathlib import Path
import base64, hashlib, zlib
ROOT = Path(__file__).resolve().parents[2]
encoded = (ROOT / "bootstrap/pass3486_3499/results.json.zlib.b64").read_text().strip()
data = zlib.decompress(base64.b64decode(encoded))
expected = "10034f25c8265145feb47a9a8c7d653441ea4e7fb8be4b6860137cd5d6d049c8"
assert hashlib.sha256(data).hexdigest() == expected
out = ROOT / "data/PART_BT3486_BT3499_RADIUS_CODE_BIPLANE_SUPPLEMENT_results.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(data)
print(out, expected)
