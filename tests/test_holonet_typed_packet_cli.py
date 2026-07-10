"""Installed-command dispatch tests for typed Levi packets."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analysis"))

import holonet_cmd  # noqa: E402


def test_installed_dispatch_packet_info(capsys) -> None:
    with pytest.raises(SystemExit) as exc:
        holonet_cmd.main(["packet-info"])
    assert exc.value.code == 0
    assert "syndrome_width" in capsys.readouterr().out


def test_installed_dispatch_packet_fuzz(capsys) -> None:
    with pytest.raises(SystemExit) as exc:
        holonet_cmd.main(["packet-fuzz", "--seed", "3", "--trials", "32"])
    assert exc.value.code == 0
    assert '"all_pass": true' in capsys.readouterr().out
