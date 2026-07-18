#!/usr/bin/env python3
from pathlib import Path
import hashlib, io, json, tarfile

EXPECTED_ARCHIVE_SHA256 = "be4e0fddc0dbcd058ece3fb2693e1475942c040507e96792159527626252e469"
MANIFEST = {".github/workflows/pass405-409-five-frontiers.yml": "1e306f6f8efdef4b315beb9f862cf25cc6c87efcd01525f41b25b8714452bfb4", "PASS405_409_FIVE_FRONTIERS_RELEASE.md": "a644d2b5079cef63494010193806d061cf843132004a5d92a664705c60f7d9b4", "analysis/w33_pass405_universal_critical_group.py": "a73b04ed80c719c70f7e7bb4757cd30bb9f55d1e1dfca3762b5339a6e4cb3b06", "analysis/w33_pass406_nonabelian_clifford_compiler.py": "f503ffbe259f2288fb41c95a5328bc7046c27f247e1fb7bfeb423b040bd58db7", "analysis/w33_pass407_sandpile_calibration_memory.py": "55354f778467c26b31edfd376ccc61626982470416275588e9f019e11442ed02", "analysis/w33_pass408_full_automorphism_theorem.py": "14839ea0b396fe1ec98b2226d70bf27447faba73e5dc62238a3c39191763e9eb", "analysis/w33_pass409_sealed_hardware_falsifier.py": "98fda3119933903da6bf303c06b2c6882f69ba0234626359be72b0b1ce190444", "data/w33_pass405_universal_critical_group.json": "1d9582f05c51e09a6738110018b2943773e27ef576046958c5a79755547cf985", "data/w33_pass406_nonabelian_clifford_compiler.json": "e008d7a9015b187ef439698edd47c8c8801782142913b4bed1142858a49511bb", "data/w33_pass406_qutrit_clifford_schedule.json": "c1a19b144f670d85c883578c66dc92ce9cdc88d9299d88e260078cab7e210a81", "data/w33_pass407_sandpile_calibration_memory.json": "6ecd3cc8860af8ec484baed3f1c9d78b38ff319d1c0e82f7b6cc28aed08daea0", "data/w33_pass407_single_slip_decoder_q3.json": "a75c9d006adc9e21856b6485093afb1513e7abfa87c420f57abf6e32d2aa358d", "data/w33_pass408_full_automorphism_theorem.json": "b35867669d5659ac53c692f68d4071ae9ead4c7ea5b9d353b61c77b69b3f5195", "data/w33_pass409_nonclaim_blind_key.json": "a77ff689933b2dc6c87ecdbc43ca2e9bbbfbc5b025f7d88a61b8fe106b985798", "data/w33_pass409_nonclaim_calibration.json": "3302f6ec28e7c275876b3fe3629877e086cb1dfd7d896358d5488cc06ccaa58e", "data/w33_pass409_nonclaim_power_study.json": "1165696f0e0daaa26f9598cef046b6c18433a0e440f1f1e5faa5f56ab019386a", "data/w33_pass409_nonclaim_raw_counts.json": "15a3d1a8bde98460b4bbf06971c0431976e43d77195b1645041b6491f1a9c69c", "data/w33_pass409_preregistered_protocol.json": "cde97e244f9ff85d95cf5e67e3b71f8723fe20fa9f5b68507baf838c0b91d3ef", "data/w33_pass409_sealed_hardware_falsifier.json": "2001740548fbacca7ac82e7f8d50f3e452512915af5e9100d0fd0cf23ccd8526", "data/w33_pass409_vendor_neutral_bom.json": "b2463ab720583b8f48640079f91d61ca6da88dc599975bb1629357016daff3e5", "schemas/w33_pass409_preregistered_falsifier_v1.schema.json": "f5c40705a3f8de5005d903f627ef2d8a14318802957ec7c900eb0720d5136c1a", "tests/test_pass405_409_five_frontiers.py": "8671a8a02ca1b6212d919ab51a611acf903483f75ce164aae81c32772f374304"}

root = Path(__file__).resolve().parents[1]
parts = sorted((root / "analysis").glob("w33_pass405_409_payload_*.bin"))
if not parts:
    raise SystemExit("no bootstrap payload chunks found")
raw = b"".join(path.read_bytes() for path in parts)
archive_sha = hashlib.sha256(raw).hexdigest()
if archive_sha != EXPECTED_ARCHIVE_SHA256:
    raise SystemExit(f"archive hash mismatch: {archive_sha} != {EXPECTED_ARCHIVE_SHA256}")
with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
    archive.extractall(root, filter="data")
for rel, expected in MANIFEST.items():
    actual = hashlib.sha256((root / rel).read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"hash mismatch {rel}: {actual} != {expected}")
print(json.dumps({"files": len(MANIFEST), "archive_sha256": archive_sha}, sort_keys=True))
