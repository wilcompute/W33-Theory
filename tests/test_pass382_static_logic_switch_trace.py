"""Regression guard for the static, certificate-only Pass 382 browser trace."""

from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "w33_pass382_reversible_logic_switch_controller.html"
CERTIFICATE = ROOT / "data" / "w33_pass382_reversible_logic_switch_controller.json"


class StaticTraceCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.state_rows: list[dict[str, str]] = []
        self.faults: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        classes = values.get("class", "").split()
        if tag == "tr" and "state-row" in classes:
            self.state_rows.append(values)
        if tag == "article" and "fault" in classes:
            self.faults.append(values)


def pair_text(pairs: list[list[int]]) -> str:
    return ";".join(f"{value}:{count}" for value, count in pairs)


def state_text(state: list[int]) -> str:
    return ",".join(str(value) for value in state)


def test_pass382_static_trace_copies_every_certified_transition_without_javascript() -> None:
    page = TRACE.read_text(encoding="utf-8")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    collector = StaticTraceCollector()
    collector.feed(page)

    assert "<script" not in page.lower()
    assert 'data-certified-source="../data/w33_pass382_reversible_logic_switch_controller.json"' in page
    assert len(collector.state_rows) == len(certificate["transition_table"]) == 48

    for shown, certified in zip(collector.state_rows, certificate["transition_table"], strict=True):
        assert shown["data-state"] == state_text(certified["state"])
        assert shown["data-operation"] == certified["operation"]
        assert shown["data-t-next"] == state_text(certified["next_state"])
        assert shown["data-t-previous"] == state_text(certified["previous_state"])
        assert shown["data-p-next"] == state_text(certified["phase_clock_next"])
        assert shown["data-latch"] == str(certified["latch_advances_edge"]).lower()
        assert shown["data-frame-wrap"] == str(certified["frame_wrap"]).lower()


def test_pass382_static_trace_copies_each_fault_summary_and_scope_boundary() -> None:
    page = TRACE.read_text(encoding="utf-8")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    collector = StaticTraceCollector()
    collector.feed(page)
    faults = {fault["data-fault"]: fault for fault in collector.faults}

    assert set(faults) == set(certificate["fault_injection"])
    for name, certified in certificate["fault_injection"].items():
        shown = faults[name]
        assert shown["data-map"] == certified["map"]
        assert shown["data-mismatch"] == str(certified["mismatched_expected_ticks"])
        assert shown["data-orbit-sizes"] == ",".join(
            str(size) for size in certified["orbit_sizes"]
        )
        assert shown["data-syndrome-pairs"] == pair_text(certified["syndrome_pairs"])
        if "mismatching_phases" in certified:
            assert shown["data-mismatching-phases"] == ",".join(
                str(phase) for phase in certified["mismatching_phases"]
            )

    assert "no actual header flag, Q6 edge, route, or physical-oscillator binding" in page
    assert "not a Q6 path closure" in page
    assert "no JavaScript and performs no mathematics in the browser" in page
