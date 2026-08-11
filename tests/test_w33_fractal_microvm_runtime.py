"""Focused regression for the recursive W33 chamber microVM runtime."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_fractal_microvm_runtime.py"
GAP_SOURCE = ROOT / "analysis" / "w33_fractal_microvm_routing.g"
GAP_CERTIFICATE = ROOT / "data" / "w33_fractal_microvm_routing_gap.json"
SPEC = importlib.util.spec_from_file_location("w33_fractal_microvm_runtime", SOURCE)
assert SPEC is not None and SPEC.loader is not None
runtime = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = runtime
SPEC.loader.exec_module(runtime)


def test_geometry_and_deterministic_panel_isa() -> None:
    geometry = runtime.GEOMETRY
    assert len(geometry.points) == 40
    assert len(geometry.lines) == 40
    assert sum(sum(row) for row in geometry.adjacency) // 2 == 240

    flags = [
        runtime.Chamber(point, line)
        for line, points in enumerate(geometry.lines)
        for point in points
    ]
    assert len(flags) == 160
    for flag in flags:
        outputs = {
            flag.step(f"{panel}{selector}")
            for panel in ("HP", "HL")
            for selector in range(3)
        }
        assert len(outputs) == 6
        for selector in range(3):
            assert flag.step(f"HP{selector}").point == flag.point
            assert flag.step(f"HL{selector}").line == flag.line


def test_guest_replay_is_content_identical() -> None:
    image = runtime.MicroVMImage("test", ("HP0", "HL1", "ADD:7", "HALT"))
    first = runtime.MicroVM(image)
    second = runtime.MicroVM(image)
    first.run()
    second.run()
    first_store = runtime.ContentStore()
    second_store = runtime.ContentStore()
    assert first_store.snapshot(first) == second_store.snapshot(second)
    assert first.accumulator == second.accumulator == 7
    assert first.trace_root == second.trace_root

    one_instruction = runtime.MicroVM(
        runtime.MicroVMImage("fuel-boundary", ("ADD:1",))
    )
    one_instruction.run(fuel=1)
    assert one_instruction.halted is True
    assert one_instruction.accumulator == 1

    yielding = runtime.MicroVM(
        runtime.MicroVMImage("yield-boundary", ("YIELD", "ADD:3", "HALT"))
    )
    yielding.run()
    assert yielding.halted is False
    assert yielding.pc == 1
    yielding.run()
    assert yielding.halted is True
    assert yielding.accumulator == 3

    with pytest.raises(ValueError, match="unknown microVM instruction"):
        runtime.MicroVMImage("invalid", ("BAD",))


def test_uniform_six_level_image_and_copy_on_write() -> None:
    image = runtime.MicroVMImage("uniform", ("YIELD", "HALT"))
    store = runtime.ContentStore()
    tree = store.uniform_tree(image, 6)
    assert tree["network_vm_instances"] == 105_025_641
    assert tree["leaf_vm_instances"] == 4_096_000_000
    assert tree["total_stateful_vm_instances"] == 4_201_025_641
    assert tree["unique_node_blobs"] == 7

    mutated, added = store.mutate_leaf(tree["root"], (3, 7, 11, 19, 23, 31), 1)
    assert mutated != tree["root"]
    assert added == 7
    assert store.get(mutated)["mediaType"] == store.get(tree["root"])["mediaType"]


def test_nested_mailbox_execution_is_persistent() -> None:
    image = runtime.MicroVMImage("mailbox", ("RECV", "HALT"))
    store = runtime.ContentStore()
    tree = store.uniform_tree(image, 4)
    address = (1, 2, 3, 4)

    delivered = store.send_at(tree["root"], address, "11", (0, 0, 0, 0))
    assert delivered["path_copy_new_blobs"] == 5
    assert delivered["receipt_new_blobs"] == 1
    assert delivered["new_blobs"] == 6
    assert store.state_at(tree["root"], address)[1]["inbox"] == []
    assert store.state_at(delivered["root"], address)[1]["inbox"] == ["11"]
    graph = store.verify_graph(delivered["root"])
    assert graph["reachable_delivery_blobs"] == 1
    receipt = store.get(delivered["delivery_receipt"])
    assert receipt["message"] == "11"
    assert receipt["messageDigest"] == runtime.digest({"message": "11"})
    receipt_payload = store.blobs.pop(delivered["delivery_receipt"])
    with pytest.raises(ValueError, match="missing delivery blob"):
        store.verify_graph(delivered["root"])
    store.blobs[delivered["delivery_receipt"]] = receipt_payload

    sibling_before = store.state_at(delivered["root"], (1, 2, 3, 5))[0]
    executed = store.execute_at(delivered["root"], address)
    sibling_after = store.state_at(executed["root"], (1, 2, 3, 5))[0]
    assert executed["new_blobs"] == 5
    assert executed["accumulator"] == 11
    assert executed["inbox_depth"] == 0
    assert executed["halted"] is True
    assert sibling_after == sibling_before

    alternate = store.send_at(tree["root"], address, "11", (39, 39, 39, 39))
    assert alternate["root"] != delivered["root"]
    assert alternate["delivery_log_head"] != delivered["delivery_log_head"]
    assert delivered["route_hops"] <= 8

    before = len(store.blobs)
    with pytest.raises(ValueError, match="invalid literal"):
        store.send_at(tree["root"], address, "hello", (0, 0, 0, 0))
    assert len(store.blobs) == before


def test_delivery_receipt_is_bound_to_state_address_and_inbox() -> None:
    image = runtime.MicroVMImage("mailbox-binding", ("RECV", "HALT"))
    store = runtime.ContentStore()
    tree = store.uniform_tree(image, 1)
    delivered = store.send_at(tree["root"], (1,), "11", (0,))
    real_receipt = store.get(delivered["delivery_receipt"])

    wrong_target = {
        **real_receipt,
        "target": [2],
        "route": runtime.route_address((0,), (2,)),
    }
    wrong_target_key = store.put(wrong_target)

    def retarget_state(row: dict[str, object]) -> dict[str, object]:
        row["deliveryLogHead"] = wrong_target_key
        return row

    wrong_target_root, _, _, _ = store._rewrite_at(
        delivered["root"], (1,), retarget_state
    )
    with pytest.raises(ValueError, match="does not match its receiving state address"):
        store.verify_graph(wrong_target_root)

    wrong_message = {
        **real_receipt,
        "message": "99",
        "messageDigest": runtime.digest({"message": "99"}),
    }
    wrong_message_key = store.put(wrong_message)

    def remessage_state(row: dict[str, object]) -> dict[str, object]:
        row["deliveryLogHead"] = wrong_message_key
        return row

    wrong_message_root, _, _, _ = store._rewrite_at(
        delivered["root"], (1,), remessage_state
    )
    with pytest.raises(ValueError, match="does not match the newest inbox value"):
        store.verify_graph(wrong_message_root)

    deep_store = runtime.ContentStore()
    deep_tree = deep_store.uniform_tree(image, 2)
    deep_delivery = deep_store.send_at(deep_tree["root"], (2, 2), "7", (0, 0))
    aliased_root = deep_store.get(deep_delivery["root"])
    children = {child["slot"]: child["digest"] for child in aliased_root["children"]}
    children[1] = children[2]
    aliased_root["children"] = [
        {"slot": slot, "digest": children[slot]} for slot in sorted(children)
    ]
    with pytest.raises(ValueError, match="referenced at multiple addresses"):
        deep_store.verify_graph(deep_store.put(aliased_root))


def test_graph_handle_preserves_children_and_forks_immutably() -> None:
    image = runtime.MicroVMImage("handle", ("ADD:2", "HALT"))
    store = runtime.ContentStore()
    tree = store.uniform_tree(image, 2)
    root_handle = store.handle(tree["root"])
    leaf_handle = store.handle(tree["root"], (1, 2))
    methods = {"load", "step", "run", "send", "snapshot", "fork", "seal"}
    assert all(callable(getattr(root_handle, name)) for name in methods)
    assert all(callable(getattr(leaf_handle, name)) for name in methods)
    assert len(root_handle.load()["children"]) == 40
    assert leaf_handle.load()["children"] == []

    original_root = leaf_handle.snapshot()
    forked = leaf_handle.fork()
    stepped = forked.step()
    assert stepped["accumulator"] == 2
    assert stepped["new_blobs"] == 3
    assert forked.snapshot() != original_root
    assert leaf_handle.snapshot() == original_root
    assert len(store.handle(forked.seal()).load()["children"]) == 40


def test_internal_descriptor_validation_rejects_malformed_state() -> None:
    store = runtime.ContentStore()
    malformed = store.put({"mediaType": "application/vnd.w33.microvm.state.v1+json"})
    with pytest.raises(ValueError, match="image reference"):
        store.verify_graph(malformed)

    image = runtime.MicroVMImage("typed", ("HALT",))
    tree = store.uniform_tree(image, 2)
    leaf = tree["node_digests"][0]

    wrong_role = store.get(leaf)
    wrong_role["image"] = leaf
    wrong_role_key = store.put(wrong_role)
    with pytest.raises(ValueError, match="wrong mediaType"):
        store.verify_graph(wrong_role_key)

    wrong_level = store.get(tree["root"])
    wrong_level["children"][0]["digest"] = leaf
    wrong_level_key = store.put(wrong_level)
    with pytest.raises(ValueError, match="referenced at levels 0 and 1"):
        store.verify_graph(wrong_level_key)

    invalid_inbox = store.get(leaf)
    invalid_inbox["inbox"] = ["hello"]
    with pytest.raises(ValueError, match="inbox values must be canonical integers"):
        store.verify_graph(store.put(invalid_inbox))

    invalid_pc = store.get(leaf)
    invalid_pc["pc"] = 999
    with pytest.raises(ValueError, match="exceeds program length"):
        store.verify_graph(store.put(invalid_pc))


def test_recursive_route_is_table_free_and_line_legal() -> None:
    source = (0, 0, 0, 0, 0, 0)
    target = (39, 38, 37, 36, 35, 34)
    trace = runtime.route_address(source, target)
    assert len(trace) <= 12
    assert trace[-1]["to"] == list(target)
    for event in trace:
        changed = [
            index
            for index, pair in enumerate(zip(event["from"], event["to"]))
            if pair[0] != pair[1]
        ]
        assert len(changed) == 1
        level = changed[0]
        first = event["from"][level]
        second = event["to"][level]
        assert runtime.GEOMETRY.line_by_pair[(first, second)] == event["line_bus"]


def test_frozen_default_payload() -> None:
    payload = runtime.build_payload(6)
    assert payload["status"] == "PASS"
    assert len(payload["checks"]) == 19
    assert all(payload["checks"].values())
    assert payload["recursive_image"]["stored_next_hop_tables"] == 0
    assert "not provide Linux process isolation" in payload["boundary"]


@pytest.mark.skipif(shutil.which("gap") is None, reason="GAP is not installed")
def test_gap_logical_route_metric_replays_byte_exact(tmp_path: Path) -> None:
    (tmp_path / "data").mkdir()
    completed = subprocess.run(
        [shutil.which("gap"), "-q", "-b", str(GAP_SOURCE)],
        cwd=tmp_path,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    assert "HoloBox GAP routing: 7/7" in completed.stdout
    replay = tmp_path / "data" / GAP_CERTIFICATE.name
    assert replay.read_bytes() == GAP_CERTIFICATE.read_bytes()
    payload = json.loads(replay.read_text(encoding="utf-8"))
    assert payload["status"] == "PASS"
    assert payload["w33"]["diameter"] == 2
    assert payload["recursive_route"]["sample_hops"] == 12
    assert len(payload["checks"]) == 7
    assert all(payload["checks"].values())


def test_holobox_end_to_end_lifecycle(tmp_path: Path) -> None:
    cli = ROOT / "analysis" / "holobox.py"

    def invoke(*args: str) -> dict[str, object]:
        completed = subprocess.run(
            [sys.executable, str(cli), *args],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=60,
        )
        return json.loads(completed.stdout)

    bundle = tmp_path / "bundle"
    run_bundle = tmp_path / "run"
    fork_bundle = tmp_path / "fork"
    message_bundle = tmp_path / "message"
    nested_run_bundle = tmp_path / "nested-run"
    built = invoke(
        "build",
        "--output",
        str(bundle),
        "--levels",
        "3",
        "--program",
        "RECV,ADD:7,HALT",
    )
    assert built["status"] == "BUILT"
    assert built["network_vm_instances"] == 1641
    assert built["leaf_vm_instances"] == 64_000
    assert built["total_stateful_vm_instances"] == 65_641
    assert built["unique_node_blobs"] == 4

    verified = invoke("verify", str(bundle))
    assert verified["status"] == "PASS"
    assert verified["reachable_blobs"] == 5

    ran = invoke("run", str(bundle), "--commit", str(run_bundle))
    assert ran["status"] == "HALTED"
    assert ran["accumulator"] == 7

    forked = invoke(
        "fork",
        str(bundle),
        "--address",
        "1/2/3",
        "--output",
        str(fork_bundle),
    )
    assert forked["status"] == "FORKED"
    assert forked["copy_on_write_new_blobs"] == 4

    sent = invoke(
        "send",
        str(bundle),
        "--source",
        "0/0/0",
        "--target",
        "1/2/3",
        "--message",
        "11",
        "--output",
        str(message_bundle),
    )
    assert sent["status"] == "DELIVERED"
    assert sent["route_hops"] <= sent["route_bound"] == 6
    assert sent["copy_on_write_new_blobs"] == 4
    assert sent["receipt_new_blobs"] == 1
    assert sent["total_new_blobs"] == 5
    assert str(sent["delivery_log_head"]).startswith("sha256:")
    assert sent["delivery_receipt"] == sent["delivery_log_head"]

    message_verified = invoke("verify", str(message_bundle))
    assert message_verified["reachable_delivery_blobs"] == 1

    nested = invoke(
        "run",
        str(message_bundle),
        "--address",
        "1/2/3",
        "--commit",
        str(nested_run_bundle),
    )
    assert nested["status"] == "HALTED"
    assert nested["address"] == [1, 2, 3]
    assert nested["accumulator"] == 18
    assert nested["copy_on_write_new_blobs"] == 4

    routed = invoke("route", "0/0/0", "39/38/37")
    assert routed["status"] == "ROUTED"
    assert routed["hops"] <= routed["bound"] == 6
    assert routed["stored_next_hop_tables"] == 0

    valuable_output = tmp_path / "valuable-output"
    valuable_output.mkdir()
    valuable_marker = valuable_output / "KEEP"
    valuable_marker.write_text("must survive invalid input", encoding="utf-8")
    invalid_send = subprocess.run(
        [
            sys.executable,
            str(cli),
            "send",
            str(bundle),
            "--source",
            "0/0/0",
            "--target",
            "1/2/3",
            "--message",
            "not-an-integer",
            "--output",
            str(valuable_output),
            "--force",
        ],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    assert invalid_send.returncode != 0
    assert valuable_marker.read_text(encoding="utf-8") == "must survive invalid input"

    symlink_target = tmp_path / "symlink-target"
    symlink_target.mkdir()
    symlink_marker = symlink_target / "KEEP"
    symlink_marker.write_text("must not be recursively deleted", encoding="utf-8")
    symlink_output = tmp_path / "symlink-output"
    symlink_output.symlink_to(symlink_target, target_is_directory=True)
    symlink_send = invoke(
        "send",
        str(bundle),
        "--source",
        "0/0/0",
        "--target",
        "1/2/3",
        "--message",
        "5",
        "--output",
        str(symlink_output),
        "--force",
    )
    assert symlink_send["status"] == "DELIVERED"
    assert symlink_marker.read_text(encoding="utf-8") == "must not be recursively deleted"
    assert symlink_output.is_dir() and not symlink_output.is_symlink()

    for dangerous_output in (bundle, bundle / "derived", tmp_path):
        destructive = subprocess.run(
            [
                sys.executable,
                str(cli),
                "send",
                str(bundle),
                "--source",
                "0/0/0",
                "--target",
                "1/2/3",
                "--message",
                "5",
                "--output",
                str(dangerous_output),
                "--force",
            ],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=60,
        )
        assert destructive.returncode != 0
        assert "source and output bundle paths must be disjoint" in destructive.stdout
    assert invoke("verify", str(bundle))["status"] == "PASS"
