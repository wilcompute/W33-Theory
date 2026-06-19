#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_recovery_packet_pointer():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Recovery Packet" in text
    assert "docs/recovery_packet_landing.md" in text
    assert "data/bt1279_recovery_packet_index.json" in text
    assert "data/bt1275_strict_polar_path_recovery_certificate.json" in text
