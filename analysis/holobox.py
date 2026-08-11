#!/usr/bin/env python3
"""HoloBox: OCI-shaped CLI for the recursive W33 chamber microVM runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
from typing import Any

from w33_fractal_microvm_runtime import (
    Chamber,
    ContentStore,
    GEOMETRY,
    MicroVMImage,
    route_address,
)


def parse_address(text: str) -> tuple[int, ...]:
    if not text:
        return ()
    address = tuple(int(part) for part in text.replace(",", "/").split("/"))
    if any(not 0 <= digit < 40 for digit in address):
        raise ValueError("every address digit must be in 0..39")
    return address


def parse_program(text: str) -> tuple[str, ...]:
    program = tuple(part.strip() for part in text.split(",") if part.strip())
    if not program:
        raise ValueError("program is empty")
    return program


def print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def output_path(value: str) -> Path:
    """Return an absolute output name without following a final symlink."""

    return Path(value).expanduser().absolute()


def validate_output_path(
    source: Path | None, destination: Path, force: bool
) -> None:
    """Validate replacement policy without mutating the destination."""

    if source is not None:
        resolved_source = source.resolve()
        resolved_destination = destination.resolve(strict=False)
        if (
            resolved_source == resolved_destination
            or resolved_source in resolved_destination.parents
            or resolved_destination in resolved_source.parents
        ):
            raise ValueError("source and output bundle paths must be disjoint")
    if destination.exists() or destination.is_symlink():
        if not force:
            raise FileExistsError(f"output bundle already exists: {destination}")


def replace_output(destination: Path, force: bool) -> None:
    """Remove a validated destination immediately before materialisation."""

    if not destination.exists() and not destination.is_symlink():
        return
    if not force:
        raise FileExistsError(f"output bundle already exists: {destination}")
    if destination.is_symlink() or destination.is_file():
        destination.unlink()
    else:
        shutil.rmtree(destination)


def command_build(args: argparse.Namespace) -> int:
    output = output_path(args.output)
    validate_output_path(None, output, args.force)
    image = MicroVMImage(args.name, parse_program(args.program))
    store = ContentStore()
    tree = store.uniform_tree(image, args.levels)
    replace_output(output, args.force)
    store.export_layout(
        output,
        tree["root"],
        {
            "org.opencontainers.image.title": args.name,
            "org.w33.microvm.levels": str(args.levels),
            "org.w33.microvm.network-instances": str(tree["network_vm_instances"]),
            "org.w33.microvm.leaf-vms": str(tree["leaf_vm_instances"]),
            "org.w33.microvm.total-stateful-vms": str(
                tree["total_stateful_vm_instances"]
            ),
        },
    )
    print_json(
        {
            "status": "BUILT",
            "bundle": str(output),
            "root": tree["root"],
            "levels": args.levels,
            "network_vm_instances": tree["network_vm_instances"],
            "leaf_vm_instances": tree["leaf_vm_instances"],
            "total_stateful_vm_instances": tree["total_stateful_vm_instances"],
            "unique_node_blobs": tree["unique_node_blobs"],
        }
    )
    return 0


def command_inspect(args: argparse.Namespace) -> int:
    bundle = Path(args.bundle).resolve()
    store, root = ContentStore.import_layout(bundle)
    state = store.get(root)
    image = store.get(state["image"])
    graph = store.verify_graph(root)
    print_json(
        {
            "status": "VALID",
            "bundle": str(bundle),
            "root": root,
            "root_level": state.get("level", 1),
            "root_children": len(state.get("children", [])),
            "image": image,
            **graph,
        }
    )
    return 0


def command_verify(args: argparse.Namespace) -> int:
    store, root = ContentStore.import_layout(Path(args.bundle).resolve())
    print_json({"status": "PASS", "root": root, **store.verify_graph(root)})
    return 0


def command_run(args: argparse.Namespace) -> int:
    bundle = Path(args.bundle).resolve()
    store, root = ContentStore.import_layout(bundle)
    address = parse_address(args.address)
    destination = output_path(args.commit) if args.commit else None
    if destination is not None:
        validate_output_path(bundle, destination, args.force)
    execution = store.execute_at(root, address, args.fuel)
    new_root = execution["root"]
    if destination is not None:
        replace_output(destination, args.force)
        store.export_layout(
            destination,
            new_root,
            {
                "org.w33.microvm.parent": root,
                "org.w33.microvm.operation": "run",
                "org.w33.microvm.address": "/".join(map(str, address)),
            },
        )
    print_json(
        {
            "status": "HALTED" if execution["halted"] else "YIELDED",
            "old_root": root,
            "new_root": new_root,
            "address": list(address),
            "copy_on_write_new_blobs": execution["new_blobs"],
            "accumulator": execution["accumulator"],
            "final_chamber": execution["final_chamber"],
            "trace_root": execution["trace_root"],
            "committed_bundle": str(destination) if destination is not None else None,
        }
    )
    return 0


def command_send(args: argparse.Namespace) -> int:
    source_bundle = Path(args.bundle).resolve()
    destination = output_path(args.output)
    store, root = ContentStore.import_layout(source_bundle)
    validate_output_path(source_bundle, destination, args.force)
    source = parse_address(args.source)
    target = parse_address(args.target)
    if len(source) != len(target):
        raise ValueError("source and target addresses must have equal depth")
    delivery = store.send_at(root, target, args.message, source)
    replace_output(destination, args.force)
    store.export_layout(
        destination,
        delivery["root"],
        {
            "org.w33.microvm.parent": root,
            "org.w33.microvm.operation": "send",
            "org.w33.microvm.source": "/".join(map(str, source)),
            "org.w33.microvm.target": "/".join(map(str, target)),
            "org.w33.microvm.message-digest": delivery["message_digest"],
        },
    )
    print_json(
        {
            "status": "DELIVERED",
            "old_root": root,
            "new_root": delivery["root"],
            "source": list(source),
            "target": list(target),
            "route_hops": delivery["route_hops"],
            "route_bound": 2 * len(source),
            "copy_on_write_new_blobs": delivery["path_copy_new_blobs"],
            "receipt_new_blobs": delivery["receipt_new_blobs"],
            "total_new_blobs": delivery["new_blobs"],
            "message_digest": delivery["message_digest"],
            "delivery_receipt": delivery["delivery_receipt"],
            "delivery_log_head": delivery["delivery_log_head"],
            "bundle": str(destination),
        }
    )
    return 0


def command_fork(args: argparse.Namespace) -> int:
    source = Path(args.bundle).resolve()
    destination = output_path(args.output)
    store, root = ContentStore.import_layout(source)
    validate_output_path(source, destination, args.force)
    address = parse_address(args.address)
    root_level = int(store.get(root).get("level", 1))
    if len(address) != root_level:
        raise ValueError(
            f"address has {len(address)} digits; root level {root_level} requires {root_level}"
        )
    new_root, new_blobs = store.mutate_leaf(root, address, args.delta)
    replace_output(destination, args.force)
    store.export_layout(
        destination,
        new_root,
        {
            "org.w33.microvm.parent": root,
            "org.w33.microvm.operation": "fork",
            "org.w33.microvm.address": "/".join(map(str, address)),
        },
    )
    print_json(
        {
            "status": "FORKED",
            "source_root": root,
            "new_root": new_root,
            "address": list(address),
            "copy_on_write_new_blobs": new_blobs,
            "bundle": str(destination),
        }
    )
    return 0


def command_route(args: argparse.Namespace) -> int:
    source = parse_address(args.source)
    target = parse_address(args.target)
    trace = route_address(source, target)
    print_json(
        {
            "status": "ROUTED",
            "source": list(source),
            "target": list(target),
            "hops": len(trace),
            "bound": 2 * len(source),
            "stored_next_hop_tables": 0,
            "trace": trace,
        }
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    build = commands.add_parser("build", help="build a recursive immutable bundle")
    build.add_argument("--output", required=True)
    build.add_argument("--name", default="w33/microvm")
    build.add_argument("--program", default="HP0,HL1,ADD:7,HP2,HL0,HALT")
    build.add_argument("--levels", type=int, default=6)
    build.add_argument("--force", action="store_true")
    build.set_defaults(handler=command_build)

    inspect = commands.add_parser("inspect", help="inspect and verify a bundle")
    inspect.add_argument("bundle")
    inspect.set_defaults(handler=command_inspect)

    verify = commands.add_parser("verify", help="verify every reachable digest")
    verify.add_argument("bundle")
    verify.set_defaults(handler=command_verify)

    run = commands.add_parser("run", help="run the root VM through the common loader")
    run.add_argument("bundle")
    run.add_argument("--address", default="", help="nested radix-40 address")
    run.add_argument("--fuel", type=int, default=10_000)
    run.add_argument("--commit")
    run.add_argument("--force", action="store_true")
    run.set_defaults(handler=command_run)

    send = commands.add_parser("send", help="route and persist one mailbox message")
    send.add_argument("bundle")
    send.add_argument("--source", required=True)
    send.add_argument("--target", required=True)
    send.add_argument("--message", required=True)
    send.add_argument("--output", required=True)
    send.add_argument("--force", action="store_true")
    send.set_defaults(handler=command_send)

    fork = commands.add_parser("fork", help="copy-on-write one nested leaf")
    fork.add_argument("bundle")
    fork.add_argument("--address", required=True)
    fork.add_argument("--delta", type=int, default=1)
    fork.add_argument("--output", required=True)
    fork.add_argument("--force", action="store_true")
    fork.set_defaults(handler=command_fork)

    route = commands.add_parser("route", help="route between radix-40 VM addresses")
    route.add_argument("source")
    route.add_argument("target")
    route.set_defaults(handler=command_route)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
