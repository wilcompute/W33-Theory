#!/usr/bin/env python3
"""Reversible binary-object loader for the W(3,3) VM.

Raw program bits should not be identified with W(3,3) points directly.  Points
are projective control addresses; bytes are payload.  This loader keeps that
boundary clean:

    bytes -> fixed-width trits -> 81-trit pages -> W33 point addresses
          -> line-bus transfer metadata -> bytes again.

Each byte is encoded as six base-3 digits because 3^6 = 729 > 256.  Pages are
81 trits, matching the q^4 logical register scale used throughout the Holonet
architecture.  W33 supplies addressing, route/bus metadata, and symmetry handles;
the payload remains exactly reversible.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import holonet_node as hn
from w33_component_execution_simulator import line_lookup
from w33_uor_runtime_model import ROOT, all_lines, point_id


DEFAULT_JSON = ROOT / "data" / "w33_binary_object_loader.json"
DEFAULT_MD = ROOT / "docs" / "w33_binary_object_loader.md"
PAGE_TRITS = 81
TRITS_PER_BYTE = 6


SAMPLES: dict[str, bytes] = {
    "hello_program": b"print('hello holonet')\n",
    "binary_0_to_63": bytes(range(64)),
    "device_packet": b"USB:keyboard:interrupt:HELLO",
}


def byte_to_trits(value: int) -> list[int]:
    if not 0 <= value <= 255:
        raise ValueError(value)
    digits = []
    current = value
    for _ in range(TRITS_PER_BYTE):
        digits.append(current % 3)
        current //= 3
    return list(reversed(digits))


def trits_to_byte(trits: list[int]) -> int:
    if len(trits) != TRITS_PER_BYTE:
        raise ValueError("expected six trits")
    value = 0
    for digit in trits:
        if digit not in (0, 1, 2):
            raise ValueError(f"not a trit: {digit}")
        value = 3 * value + digit
    if value > 255:
        raise ValueError(f"trits exceed byte range: {value}")
    return value


def bytes_to_trits(blob: bytes) -> list[int]:
    out: list[int] = []
    for value in blob:
        out.extend(byte_to_trits(value))
    return out


def trits_to_bytes(trits: list[int], byte_len: int) -> bytes:
    needed = byte_len * TRITS_PER_BYTE
    trimmed = trits[:needed]
    return bytes(
        trits_to_byte(trimmed[idx : idx + TRITS_PER_BYTE])
        for idx in range(0, needed, TRITS_PER_BYTE)
    )


def point_for_page(object_digest: str, page_index: int, page_trits: list[int]) -> int:
    payload = (
        object_digest
        + ":"
        + str(page_index)
        + ":"
        + "".join(map(str, page_trits[:18]))
    ).encode("ascii")
    digest = hashlib.sha256(payload).digest()
    return int.from_bytes(digest[:4], "big") % len(hn.POINTS)


def page_records(name: str, blob: bytes) -> dict[str, Any]:
    lines = all_lines()
    lookup = line_lookup(lines)
    trits = bytes_to_trits(blob)
    padded_len = math.ceil(len(trits) / PAGE_TRITS) * PAGE_TRITS if trits else PAGE_TRITS
    padded = trits + [0] * (padded_len - len(trits))
    digest = hashlib.sha256(blob).hexdigest()
    pages = []
    for page_index in range(0, padded_len // PAGE_TRITS):
        page = padded[page_index * PAGE_TRITS : (page_index + 1) * PAGE_TRITS]
        point_idx = point_for_page(digest, page_index, page)
        phase_sum = sum(page) % 3
        pages.append(
            {
                "page_index": page_index,
                "trit_count": len(page),
                "used_trits": max(0, min(PAGE_TRITS, len(trits) - page_index * PAGE_TRITS)),
                "point_index": point_idx,
                "point_label": point_id(hn.POINTS[point_idx]),
                "phase_sum_mod3": phase_sum,
                "orbit_handle_mod51840": int(
                    hashlib.sha256((digest + f":orbit:{page_index}").encode()).hexdigest()[:8],
                    16,
                )
                % 51840,
                "trits": page,
            }
        )

    transfers = []
    for left, right in zip(pages, pages[1:]):
        src = hn.POINTS[left["point_index"]]
        dst = hn.POINTS[right["point_index"]]
        route = hn.route(src, dst)
        route_indices = [hn.POINTS.index(point) for point in route]
        hop_lines = [
            lookup[(a, b)] for a, b in zip(route_indices, route_indices[1:])
        ]
        transfers.append(
            {
                "from_page": left["page_index"],
                "to_page": right["page_index"],
                "route": [point_id(point) for point in route],
                "hops": len(route_indices) - 1,
                "line_buses": hop_lines,
            }
        )

    recovered = trits_to_bytes(padded, len(blob))
    return {
        "name": name,
        "byte_len": len(blob),
        "sha256": digest,
        "trit_len": len(trits),
        "page_trits": PAGE_TRITS,
        "page_count": len(pages),
        "pages": pages,
        "transfers": transfers,
        "roundtrip_sha256": hashlib.sha256(recovered).hexdigest(),
        "roundtrip_matches": recovered == blob,
    }


def build_payload() -> dict[str, Any]:
    objects = [page_records(name, blob) for name, blob in SAMPLES.items()]
    checks = {
        "all_roundtrips_match": all(obj["roundtrip_matches"] for obj in objects),
        "all_pages_are_81_trits": all(
            page["trit_count"] == PAGE_TRITS
            for obj in objects
            for page in obj["pages"]
        ),
        "all_points_are_w33_points": all(
            0 <= page["point_index"] < 40 for obj in objects for page in obj["pages"]
        ),
        "all_transfers_diameter_two": all(
            transfer["hops"] <= 2 for obj in objects for transfer in obj["transfers"]
        ),
        "six_trits_per_byte_is_reversible": all(
            trits_to_byte(byte_to_trits(value)) == value for value in range(256)
        ),
        "sample_count": len(objects) == len(SAMPLES),
    }
    return {
        "schema": "w33.binary_object_loader.v1",
        "theorem": "reversible binary object to W33-addressed trit pages",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "encoding": {
            "trits_per_byte": TRITS_PER_BYTE,
            "page_trits": PAGE_TRITS,
            "reading": "payload bytes are reversible trit pages; W33 points are control addresses, not raw bit buckets",
        },
        "objects": objects,
        "checks": checks,
        "interpretation": (
            "Arbitrary program bits enter the VM as reversible trit pages. Page "
            "addresses are W33 points, page-to-page transfer uses W33 routes and "
            "line buses, and the original bytes can be reconstructed exactly."
        ),
        "honesty_boundary": (
            "This is a loader/addressing witness. It does not execute the bytes "
            "as code and does not claim compression of arbitrary payload entropy."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    rows = []
    for obj in payload["objects"]:
        rows.append(
            "| {name} | {byte_len} | {trit_len} | {page_count} | `{sha256}` | {roundtrip_matches} |".format(
                **obj
            )
        )
    return f"""# W(3,3) Binary Object Loader

Raw bits are payload. W33 points are control addresses. This loader maps bytes
to reversible trit pages, assigns those pages to W33 point addresses, records
page-to-page route metadata, and reconstructs the original bytes exactly.

| Object | Bytes | Trits | Pages | SHA-256 | Roundtrip |
|---|---:|---:|---:|---|---|
{chr(10).join(rows)}

Encoding: `{TRITS_PER_BYTE}` trits per byte, `{PAGE_TRITS}` trits per page.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args(argv)

    payload = build_payload()
    json_out = Path(args.json_out)
    if not json_out.is_absolute():
        json_out = ROOT / json_out
    md_out = Path(args.md_out)
    if not md_out.is_absolute():
        md_out = ROOT / md_out
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_out.write_text(markdown(payload), encoding="utf-8")
    print(f"status: {payload['status']}")
    for obj in payload["objects"]:
        print(
            f"{obj['name']}: bytes={obj['byte_len']}, trits={obj['trit_len']}, "
            f"pages={obj['page_count']}, roundtrip={obj['roundtrip_matches']}"
        )
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
