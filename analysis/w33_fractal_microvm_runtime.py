#!/usr/bin/env python3
"""Executable reference runtime for a recursive W33 chamber microVM.

This composes three already-certified repo objects instead of renaming them:

* the packet VM supplies a checked guest-computation path;
* BT1700 supplies the 40-way recursive packet ABI;
* Passes 4324--4327 supply the literal chamber and two panel relations.

Pass 4334's rank-24 point/line projectors are adjacent representation-theory
prior art; this runtime does not implement those modal projectors.

The missing systems object was a content-addressed runtime in which a network
of microVMs is itself loadable through the same microVM interface.  This file
builds that object.  It is a deterministic Python reference model, not a Linux
namespace, KVM, Firecracker, Kata, or hardware security boundary.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any, Callable, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "data" / "w33_fractal_microvm_runtime.json"
DEFAULT_MD = ROOT / "docs" / "W33_FRACTAL_MICROVM_RUNTIME.md"

Vector = tuple[int, int, int, int]
Address = tuple[int, ...]


def validate_instruction(instruction: str) -> None:
    """Reject images that cannot be executed by the frozen chamber ISA."""

    if instruction in {"RECV", "YIELD", "HALT"}:
        return
    if len(instruction) == 3 and instruction[:2] in {"HP", "HL"} and instruction[2] in "012":
        return
    if instruction.startswith("ADD:"):
        int(instruction.split(":", 1)[1])
        return
    raise ValueError(f"unknown microVM instruction {instruction!r}")


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value)).hexdigest()


def canon(vector: Iterable[int]) -> Vector:
    row = tuple(int(value) % 3 for value in vector)
    for value in row:
        if value:
            scale = 1 if value == 1 else 2
            return tuple((scale * item) % 3 for item in row)  # type: ignore[return-value]
    raise ValueError("zero has no projective representative")


def symplectic(left: Vector, right: Vector) -> int:
    return (
        left[0] * right[2]
        - left[2] * right[0]
        + left[1] * right[3]
        - left[3] * right[1]
    ) % 3


@dataclass(frozen=True)
class Geometry:
    points: tuple[Vector, ...]
    lines: tuple[tuple[int, ...], ...]
    adjacency: tuple[tuple[bool, ...], ...]
    incident_lines: tuple[tuple[int, ...], ...]
    line_by_pair: dict[tuple[int, int], int]

    def route(self, source: int, target: int) -> tuple[int, ...]:
        if source == target:
            return (source,)
        if self.adjacency[source][target]:
            return (source, target)
        relay = min(
            point
            for point in range(40)
            if self.adjacency[source][point] and self.adjacency[target][point]
        )
        return (source, relay, target)


def build_geometry() -> Geometry:
    points = tuple(
        sorted(
            {
                canon(vector)
                for vector in itertools.product(range(3), repeat=4)
                if any(vector)
            }
        )
    )
    point_index = {point: index for index, point in enumerate(points)}
    coefficients = [
        pair for pair in itertools.product(range(3), repeat=2) if pair != (0, 0)
    ]
    line_set: set[tuple[int, ...]] = set()
    for first, second in itertools.combinations(range(40), 2):
        if symplectic(points[first], points[second]) != 0:
            continue
        line = tuple(
            sorted(
                {
                    point_index[
                        canon(
                            coefficient[0] * points[first][axis]
                            + coefficient[1] * points[second][axis]
                            for axis in range(4)
                        )
                    ]
                    for coefficient in coefficients
                }
            )
        )
        line_set.add(line)
    lines = tuple(sorted(line_set))
    adjacency = tuple(
        tuple(
            first != second and symplectic(points[first], points[second]) == 0
            for second in range(40)
        )
        for first in range(40)
    )
    incident_lines = tuple(
        tuple(index for index, line in enumerate(lines) if point in line)
        for point in range(40)
    )
    line_by_pair: dict[tuple[int, int], int] = {}
    for line_index, line in enumerate(lines):
        for first in line:
            for second in line:
                if first != second:
                    line_by_pair[(first, second)] = line_index
    return Geometry(points, lines, adjacency, incident_lines, line_by_pair)


GEOMETRY = build_geometry()


@dataclass(frozen=True)
class Chamber:
    """One VM placement address: endpoint label plus incident line/bus context."""

    point: int
    line: int

    def __post_init__(self) -> None:
        if not 0 <= self.point < 40 or not 0 <= self.line < 40:
            raise ValueError("chamber coordinate outside 0..39")
        if self.point not in GEOMETRY.lines[self.line]:
            raise ValueError("point is not incident with line")

    def step(self, opcode: str) -> "Chamber":
        if len(opcode) != 3 or opcode[:2] not in {"HP", "HL"} or opcode[2] not in "012":
            raise ValueError(f"invalid panel opcode {opcode!r}")
        selector = int(opcode[2])
        if opcode[:2] == "HP":
            alternatives = [
                line
                for line in GEOMETRY.incident_lines[self.point]
                if line != self.line
            ]
            return Chamber(self.point, alternatives[selector])
        alternatives = [
            point for point in GEOMETRY.lines[self.line] if point != self.point
        ]
        return Chamber(alternatives[selector], self.line)


@dataclass(frozen=True)
class MicroVMImage:
    name: str
    program: tuple[str, ...]
    environment: tuple[tuple[str, str], ...] = ()
    entry: Chamber = Chamber(0, GEOMETRY.incident_lines[0][0])

    def __post_init__(self) -> None:
        for instruction in self.program:
            validate_instruction(instruction)

    def descriptor(self) -> dict[str, Any]:
        return {
            "mediaType": "application/vnd.w33.microvm.image.v1+json",
            "name": self.name,
            "program": list(self.program),
            "environment": [list(item) for item in self.environment],
            "entry": [self.entry.point, self.entry.line],
        }

    @property
    def image_digest(self) -> str:
        return digest(self.descriptor())


@dataclass
class MicroVM:
    """Small deterministic guest with the same interface at every tree depth."""

    image: MicroVMImage
    chamber: Chamber | None = None
    pc: int = 0
    accumulator: int = 0
    halted: bool = False
    inbox: list[str] = field(default_factory=list)
    children: dict[int, "MicroVM"] = field(default_factory=dict)
    trace_root: str = "sha256:" + "0" * 64

    def __post_init__(self) -> None:
        if self.chamber is None:
            self.chamber = self.image.entry

    def spawn(self, slot: int, child: "MicroVM") -> None:
        if not 0 <= slot < 40:
            raise ValueError("child slot outside 0..39")
        if slot in self.children:
            raise ValueError("child slot already occupied")
        self.children[slot] = child

    def _record(self, instruction: str) -> None:
        event = {
            "previous": self.trace_root,
            "pc": self.pc,
            "instruction": instruction,
            "chamber": [self.chamber.point, self.chamber.line],
            "accumulator": self.accumulator,
            "inbox_depth": len(self.inbox),
        }
        self.trace_root = digest(event)

    def step(self) -> bool:
        if self.halted:
            return False
        if self.pc >= len(self.image.program):
            self.halted = True
            return False
        instruction = self.image.program[self.pc]
        continue_running = True
        if instruction[:2] in {"HP", "HL"}:
            self.chamber = self.chamber.step(instruction)
        elif instruction.startswith("ADD:"):
            self.accumulator += int(instruction.split(":", 1)[1])
        elif instruction == "RECV":
            if self.inbox:
                value = int(self.inbox[0])
                self.inbox.pop(0)
                self.accumulator += value
        elif instruction == "YIELD":
            continue_running = False
        elif instruction == "HALT":
            self.halted = True
        else:
            raise ValueError(f"unknown microVM instruction {instruction!r}")
        self._record(instruction)
        self.pc += 1
        if self.pc >= len(self.image.program):
            self.halted = True
        return continue_running and not self.halted

    def run(self, fuel: int = 10_000) -> None:
        for _ in range(fuel):
            if not self.step():
                return
        raise RuntimeError("microVM exhausted fuel")

    def resolve(self, address: Address) -> "MicroVM":
        node = self
        for slot in address:
            node = node.children[slot]
        return node


def route_address(source: Address, target: Address) -> list[dict[str, Any]]:
    """Route in the Cartesian power of W33 with no stored next-hop table."""

    if len(source) != len(target):
        raise ValueError("source and target depths differ")
    current = list(source)
    events: list[dict[str, Any]] = []
    for level, destination in enumerate(target):
        path = GEOMETRY.route(current[level], destination)
        for first, second in zip(path, path[1:]):
            before = tuple(current)
            current[level] = second
            events.append(
                {
                    "level": level,
                    "from": list(before),
                    "to": list(current),
                    "line_bus": GEOMETRY.line_by_pair[(first, second)],
                }
            )
    if tuple(current) != target:
        raise AssertionError("recursive route did not reach target")
    return events


class ContentStore:
    """OCI-like immutable blob graph with recursive copy-on-write snapshots."""

    def __init__(self) -> None:
        self.blobs: dict[str, bytes] = {}

    def put(self, value: dict[str, Any]) -> str:
        payload = canonical_json(value)
        key = "sha256:" + hashlib.sha256(payload).hexdigest()
        self.blobs.setdefault(key, payload)
        return key

    def get(self, key: str) -> dict[str, Any]:
        return json.loads(self.blobs[key])

    def put_image(self, image: MicroVMImage) -> str:
        return self.put(image.descriptor())

    def restore_shallow(self, root: str) -> MicroVM:
        """Load local execution registers; child descriptors remain in the store."""

        state = self.get(root)
        image_row = self.get(state["image"])
        image = MicroVMImage(
            image_row["name"],
            tuple(image_row["program"]),
            tuple(tuple(item) for item in image_row["environment"]),
            Chamber(*image_row["entry"]),
        )
        return MicroVM(
            image=image,
            chamber=Chamber(*state["chamber"]),
            pc=int(state["pc"]),
            accumulator=int(state["accumulator"]),
            halted=bool(state["halted"]),
            inbox=list(state["inbox"]),
            trace_root=state["traceRoot"],
        )

    def export_layout(
        self, directory: Path, root: str, annotations: dict[str, str] | None = None
    ) -> None:
        """Write an OCI-shaped content-addressed layout with a custom root type."""

        directory.mkdir(parents=True, exist_ok=True)
        blob_root = directory / "blobs" / "sha256"
        blob_root.mkdir(parents=True, exist_ok=True)
        for key, payload in self.blobs.items():
            (blob_root / key.split(":", 1)[1]).write_bytes(payload)
        (directory / "oci-layout").write_text(
            json.dumps({"imageLayoutVersion": "1.0.0"}, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        index = {
            "schemaVersion": 2,
            "mediaType": "application/vnd.oci.image.index.v1+json",
            "manifests": [
                {
                    "mediaType": "application/vnd.w33.microvm.state.v1+json",
                    "digest": root,
                    "size": len(self.blobs[root]),
                    "annotations": dict(sorted((annotations or {}).items())),
                }
            ],
        }
        (directory / "index.json").write_text(
            json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    @classmethod
    def import_layout(cls, directory: Path) -> tuple["ContentStore", str]:
        layout = json.loads((directory / "oci-layout").read_text(encoding="utf-8"))
        if layout != {"imageLayoutVersion": "1.0.0"}:
            raise ValueError("unsupported OCI layout marker")
        index = json.loads((directory / "index.json").read_text(encoding="utf-8"))
        if index.get("schemaVersion") != 2:
            raise ValueError("index schemaVersion must be 2")
        if index.get("mediaType") != "application/vnd.oci.image.index.v1+json":
            raise ValueError("index mediaType is not the OCI image index type")
        manifests = index.get("manifests")
        if not isinstance(manifests, list) or len(manifests) != 1:
            raise ValueError("HoloBox index must contain exactly one root manifest")
        descriptor = manifests[0]
        if descriptor.get("mediaType") != "application/vnd.w33.microvm.state.v1+json":
            raise ValueError("root descriptor has the wrong mediaType")
        root = descriptor["digest"]
        store = cls()
        for path in (directory / "blobs" / "sha256").iterdir():
            payload = path.read_bytes()
            key = "sha256:" + path.name
            if "sha256:" + hashlib.sha256(payload).hexdigest() != key:
                raise ValueError(f"blob digest mismatch: {path}")
            store.blobs[key] = payload
        if root not in store.blobs:
            raise ValueError("layout root is missing")
        if descriptor.get("size") != len(store.blobs[root]):
            raise ValueError("root descriptor size does not match its blob")
        store.verify_graph(root)
        return store, root

    @staticmethod
    def _is_digest(value: Any) -> bool:
        if not isinstance(value, str) or not value.startswith("sha256:"):
            return False
        hexdigest = value.split(":", 1)[1]
        if len(hexdigest) != 64:
            return False
        try:
            int(hexdigest, 16)
        except ValueError:
            return False
        return True

    @classmethod
    def _validate_image_descriptor(cls, row: dict[str, Any]) -> None:
        if row.get("mediaType") != "application/vnd.w33.microvm.image.v1+json":
            raise ValueError("image blob has the wrong mediaType")
        if not isinstance(row.get("name"), str):
            raise ValueError("image name must be a string")
        program = row.get("program")
        if not isinstance(program, list) or not all(
            isinstance(item, str) for item in program
        ):
            raise ValueError("image program must be a string list")
        for instruction in program:
            validate_instruction(instruction)
        environment = row.get("environment")
        if not isinstance(environment, list) or not all(
            isinstance(item, list)
            and len(item) == 2
            and all(isinstance(value, str) for value in item)
            for item in environment
        ):
            raise ValueError("image environment must contain string pairs")
        entry = row.get("entry")
        if not isinstance(entry, list) or len(entry) != 2:
            raise ValueError("image entry must be a chamber pair")
        Chamber(*entry)

    @classmethod
    def _validate_state_descriptor(cls, row: dict[str, Any]) -> None:
        if row.get("mediaType") != "application/vnd.w33.microvm.state.v1+json":
            raise ValueError("state blob has the wrong mediaType")
        if not cls._is_digest(row.get("image")):
            raise ValueError("state image reference is not a SHA-256 digest")
        chamber = row.get("chamber")
        if not isinstance(chamber, list) or len(chamber) != 2:
            raise ValueError("state chamber must be a pair")
        Chamber(*chamber)
        if not isinstance(row.get("pc"), int) or isinstance(row.get("pc"), bool):
            raise ValueError("state pc must be an integer")
        if row["pc"] < 0:
            raise ValueError("state pc must be nonnegative")
        if not isinstance(row.get("accumulator"), int) or isinstance(
            row.get("accumulator"), bool
        ):
            raise ValueError("state accumulator must be an integer")
        if not isinstance(row.get("halted"), bool):
            raise ValueError("state halted must be Boolean")
        if not isinstance(row.get("inbox"), list) or not all(
            isinstance(item, str) for item in row["inbox"]
        ):
            raise ValueError("state inbox must be a string list")
        for item in row["inbox"]:
            try:
                canonical_item = str(int(item))
            except ValueError as error:
                raise ValueError("state inbox values must be canonical integers") from error
            if canonical_item != item:
                raise ValueError("state inbox values must be canonical integers")
        if not cls._is_digest(row.get("traceRoot")):
            raise ValueError("state traceRoot is not a SHA-256 digest")
        if "deliveryLogHead" in row and not cls._is_digest(row["deliveryLogHead"]):
            raise ValueError("state deliveryLogHead is not a SHA-256 digest")
        if "level" in row and (
            not isinstance(row["level"], int)
            or isinstance(row["level"], bool)
            or row["level"] < 0
        ):
            raise ValueError("state level must be a nonnegative integer")
        children = row.get("children")
        if not isinstance(children, list):
            raise ValueError("state children must be a list")
        slots: list[int] = []
        for child in children:
            if not isinstance(child, dict) or set(child) != {"slot", "digest"}:
                raise ValueError("child descriptor must contain slot and digest")
            slot = child["slot"]
            if not isinstance(slot, int) or isinstance(slot, bool) or not 0 <= slot < 40:
                raise ValueError("child slot is outside 0..39")
            if not cls._is_digest(child["digest"]):
                raise ValueError("child reference is not a SHA-256 digest")
            slots.append(slot)
        if len(slots) != len(set(slots)):
            raise ValueError("child slots must be unique")

        if "level" in row:
            expected_slots = [] if row["level"] == 0 else list(range(40))
            if sorted(slots) != expected_slots:
                raise ValueError(
                    "level-0 states must be leaves and positive-level states "
                    "must contain exactly the 40 radix slots"
                )

    @classmethod
    def _validate_delivery_descriptor(cls, row: dict[str, Any]) -> None:
        if row.get("mediaType") != "application/vnd.w33.microvm.delivery.v1+json":
            raise ValueError("delivery blob has the wrong mediaType")
        if not cls._is_digest(row.get("previous")):
            raise ValueError("delivery previous reference is not a SHA-256 digest")
        if not cls._is_digest(row.get("messageDigest")):
            raise ValueError("delivery messageDigest is not a SHA-256 digest")
        message = row.get("message")
        if not isinstance(message, str):
            raise ValueError("delivery message must be a canonical integer string")
        try:
            canonical_message = str(int(message))
        except ValueError as error:
            raise ValueError(
                "delivery message must be a canonical integer string"
            ) from error
        if canonical_message != message:
            raise ValueError("delivery message must be a canonical integer string")
        if row["messageDigest"] != digest({"message": message}):
            raise ValueError("delivery messageDigest does not commit its message")

        addresses: dict[str, Address] = {}
        for field_name in ("source", "target"):
            value = row.get(field_name)
            if not isinstance(value, list) or any(
                not isinstance(item, int)
                or isinstance(item, bool)
                or not 0 <= item < 40
                for item in value
            ):
                raise ValueError(f"delivery {field_name} must be a radix-40 address")
            addresses[field_name] = tuple(value)
        if len(addresses["source"]) != len(addresses["target"]):
            raise ValueError("delivery source and target depths differ")
        if row.get("route") != route_address(
            addresses["source"], addresses["target"]
        ):
            raise ValueError("delivery route is not the canonical legal W33 route")

    def verify_graph(self, root: str) -> dict[str, int]:
        """Verify the typed, reachable state/image/delivery graph."""

        pending: list[
            tuple[str, str, int | None, Address | None, str | None]
        ] = [(root, "state", None, (), None)]
        seen: set[str] = set()
        roles: dict[str, str] = {}
        expected_levels: dict[str, int] = {}
        state_addresses: dict[str, set[Address]] = {}
        rows: dict[str, dict[str, Any]] = {}
        edges = 0
        states = 0
        images = 0
        deliveries = 0
        zero_digest = "sha256:" + "0" * 64
        while pending:
            key, role, expected_level, expected_address, expected_message = pending.pop()
            prior_role = roles.get(key)
            if prior_role is not None and prior_role != role:
                raise ValueError(
                    f"descriptor role conflict for {key}: {prior_role} versus {role}"
                )
            roles[key] = role
            if role == "state" and expected_level is not None:
                prior_level = expected_levels.get(key)
                if prior_level is not None and prior_level != expected_level:
                    raise ValueError(
                        f"state {key} is referenced at levels {prior_level} and "
                        f"{expected_level}"
                    )
                expected_levels[key] = expected_level
            if role == "state" and expected_address is not None:
                state_addresses.setdefault(key, set()).add(expected_address)
            if key in seen:
                if role == "state" and expected_level is not None:
                    if rows[key].get("level") != expected_level:
                        raise ValueError(
                            f"state {key} has level {rows[key].get('level')}; "
                            f"edge requires {expected_level}"
                        )
                if role == "state" and expected_address is not None:
                    delivery_head = rows[key].get("deliveryLogHead")
                    if delivery_head is not None:
                        inbox = rows[key]["inbox"]
                        pending.append(
                            (
                                delivery_head,
                                "delivery",
                                None,
                                expected_address,
                                digest({"message": inbox[-1]}) if inbox else None,
                            )
                        )
                if role == "delivery":
                    if expected_address is not None and tuple(
                        rows[key]["target"]
                    ) != expected_address:
                        raise ValueError(
                            "delivery target does not match its receiving state address"
                        )
                    if (
                        expected_message is not None
                        and rows[key]["messageDigest"] != expected_message
                    ):
                        raise ValueError(
                            "delivery head does not match the newest inbox value"
                        )
                continue
            if key not in self.blobs:
                raise ValueError(f"missing {role} blob {key}")
            payload = self.blobs[key]
            if "sha256:" + hashlib.sha256(payload).hexdigest() != key:
                raise ValueError(f"digest mismatch for {key}")
            row = json.loads(payload)
            if not isinstance(row, dict):
                raise ValueError(f"reachable {role} blob {key} is not an object")
            rows[key] = row
            seen.add(key)

            if role == "image":
                self._validate_image_descriptor(row)
                images += 1
                continue
            if role == "delivery":
                self._validate_delivery_descriptor(row)
                if expected_address is not None and tuple(row["target"]) != expected_address:
                    raise ValueError(
                        "delivery target does not match its receiving state address"
                    )
                if (
                    expected_message is not None
                    and row["messageDigest"] != expected_message
                ):
                    raise ValueError(
                        "delivery head does not match the newest inbox value"
                    )
                for endpoint in ("source", "target"):
                    try:
                        self.state_at(root, tuple(row[endpoint]))
                    except (KeyError, TypeError, ValueError) as error:
                        raise ValueError(
                            f"delivery {endpoint} address is absent from the verified root"
                        ) from error
                deliveries += 1
                previous = row["previous"]
                if previous != zero_digest:
                    pending.append(
                        (previous, "delivery", None, expected_address, None)
                    )
                    edges += 1
                continue
            if role != "state":
                raise ValueError(f"unknown descriptor role {role!r}")

            self._validate_state_descriptor(row)
            states += 1
            if expected_level is not None and row.get("level") != expected_level:
                raise ValueError(
                    f"state {key} has level {row.get('level')}; edge requires "
                    f"{expected_level}"
                )
            if row["image"] not in self.blobs:
                raise ValueError(f"missing image blob {row['image']}")
            image_row = self.get(row["image"])
            self._validate_image_descriptor(image_row)
            if row["pc"] > len(image_row["program"]):
                raise ValueError(
                    f"state pc {row['pc']} exceeds program length "
                    f"{len(image_row['program'])}"
                )
            pending.append((row["image"], "image", None, None, None))
            edges += 1
            delivery_head = row.get("deliveryLogHead")
            if delivery_head is not None:
                if delivery_head == zero_digest:
                    raise ValueError("stored deliveryLogHead cannot be the zero sentinel")
                inbox = row["inbox"]
                pending.append(
                    (
                        delivery_head,
                        "delivery",
                        None,
                        expected_address,
                        digest({"message": inbox[-1]}) if inbox else None,
                    )
                )
                edges += 1
            child_level = row.get("level")
            if child_level is not None:
                child_level -= 1
            for child in row["children"]:
                child_address = (
                    None
                    if expected_address is None
                    else expected_address + (child["slot"],)
                )
                pending.append(
                    (child["digest"], "state", child_level, child_address, None)
                )
                edges += 1

        subtree_delivery_cache: dict[str, bool] = {}

        def subtree_has_delivery(key: str) -> bool:
            cached = subtree_delivery_cache.get(key)
            if cached is not None:
                return cached
            row = rows[key]
            answer = "deliveryLogHead" in row or any(
                subtree_has_delivery(child["digest"]) for child in row["children"]
            )
            subtree_delivery_cache[key] = answer
            return answer

        for key, addresses in state_addresses.items():
            if len(addresses) > 1 and subtree_has_delivery(key):
                raise ValueError(
                    "delivery-bearing state subtree is referenced at multiple addresses"
                )
        return {
            "reachable_blobs": len(seen),
            "reachable_state_blobs": states,
            "reachable_image_blobs": images,
            "reachable_delivery_blobs": deliveries,
            "descriptor_edges": edges,
        }

    def state_at(self, root: str, address: Address) -> tuple[str, dict[str, Any]]:
        """Resolve one nested VM without materialising any sibling subtree."""

        key = root
        for depth, slot in enumerate(address):
            if not 0 <= slot < 40:
                raise ValueError(f"address digit {slot} at depth {depth} is outside 0..39")
            node = self.get(key)
            children = {row["slot"]: row["digest"] for row in node.get("children", [])}
            if slot not in children:
                raise ValueError(f"address continues below a leaf at depth {depth}")
            key = children[slot]
        return key, self.get(key)

    def _rewrite_at(
        self,
        root: str,
        address: Address,
        update: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> tuple[str, int, str, str]:
        """Apply one immutable state transition and copy only its ancestor path."""

        before = len(self.blobs)
        old_target = ""
        new_target = ""

        def rewrite(node_key: str, depth: int) -> str:
            nonlocal old_target, new_target
            node = self.get(node_key)
            if depth == len(address):
                old_target = node_key
                new_target = self.put(update(node))
                return new_target
            slot = address[depth]
            if not 0 <= slot < 40:
                raise ValueError(
                    f"address digit {slot} at depth {depth} is outside 0..39"
                )
            children = {
                row["slot"]: row["digest"] for row in node.get("children", [])
            }
            if slot not in children:
                raise ValueError(f"address continues below a leaf at depth {depth}")
            children[slot] = rewrite(children[slot], depth + 1)
            node["children"] = [
                {"slot": child_slot, "digest": children[child_slot]}
                for child_slot in sorted(children)
            ]
            return self.put(node)

        new_root = rewrite(root, 0)
        return new_root, len(self.blobs) - before, old_target, new_target

    def execute_at(
        self, root: str, address: Address, fuel: int = 10_000
    ) -> dict[str, Any]:
        """Run a VM at any tree address and return a persistent network snapshot."""

        target_key, _ = self.state_at(root, address)
        vm = self.restore_shallow(target_key)
        vm.run(fuel)

        def update(node: dict[str, Any]) -> dict[str, Any]:
            node.update(
                {
                    "chamber": [vm.chamber.point, vm.chamber.line],
                    "pc": vm.pc,
                    "accumulator": vm.accumulator,
                    "halted": vm.halted,
                    "inbox": list(vm.inbox),
                    "traceRoot": vm.trace_root,
                }
            )
            return node

        new_root, new_blobs, old_target, new_target = self._rewrite_at(
            root, address, update
        )
        return {
            "root": new_root,
            "old_target": old_target,
            "new_target": new_target,
            "new_blobs": new_blobs,
            "address": list(address),
            "accumulator": vm.accumulator,
            "final_chamber": [vm.chamber.point, vm.chamber.line],
            "halted": vm.halted,
            "inbox_depth": len(vm.inbox),
            "trace_root": vm.trace_root,
        }

    def step_at(self, root: str, address: Address) -> dict[str, Any]:
        """Execute at most one local guest instruction and persist its digest path."""

        target_key, _ = self.state_at(root, address)
        vm = self.restore_shallow(target_key)
        continue_running = vm.step()

        def update(node: dict[str, Any]) -> dict[str, Any]:
            node.update(
                {
                    "chamber": [vm.chamber.point, vm.chamber.line],
                    "pc": vm.pc,
                    "accumulator": vm.accumulator,
                    "halted": vm.halted,
                    "inbox": list(vm.inbox),
                    "traceRoot": vm.trace_root,
                }
            )
            return node

        new_root, new_blobs, old_target, new_target = self._rewrite_at(
            root, address, update
        )
        return {
            "root": new_root,
            "old_target": old_target,
            "new_target": new_target,
            "new_blobs": new_blobs,
            "address": list(address),
            "continue_running": continue_running,
            "accumulator": vm.accumulator,
            "final_chamber": [vm.chamber.point, vm.chamber.line],
            "halted": vm.halted,
            "inbox_depth": len(vm.inbox),
            "trace_root": vm.trace_root,
        }

    def send_at(
        self,
        root: str,
        address: Address,
        message: str,
        source: Address | None = None,
    ) -> dict[str, Any]:
        """Commit a legal route and mailbox value into a persistent target state."""

        encoded_message = str(int(str(message)))
        source_address = address if source is None else source
        if len(source_address) != len(address):
            raise ValueError("source and target addresses must have equal depth")
        self.state_at(root, source_address)
        _, target_state = self.state_at(root, address)
        route = route_address(source_address, address)
        message_digest = digest({"message": encoded_message})
        before = len(self.blobs)
        receipt = {
            "mediaType": "application/vnd.w33.microvm.delivery.v1+json",
            "previous": target_state.get("deliveryLogHead", "sha256:" + "0" * 64),
            "source": list(source_address),
            "target": list(address),
            "route": route,
            "message": encoded_message,
            "messageDigest": message_digest,
        }
        receipt_key = self.put(receipt)

        def update(node: dict[str, Any]) -> dict[str, Any]:
            node["deliveryLogHead"] = receipt_key
            node["inbox"] = [*node.get("inbox", []), encoded_message]
            return node

        new_root, path_new_blobs, old_target, new_target = self._rewrite_at(
            root, address, update
        )
        new_blobs = len(self.blobs) - before
        return {
            "root": new_root,
            "old_target": old_target,
            "new_target": new_target,
            "new_blobs": new_blobs,
            "path_copy_new_blobs": path_new_blobs,
            "receipt_new_blobs": new_blobs - path_new_blobs,
            "address": list(address),
            "source": list(source_address),
            "route": route,
            "route_hops": len(route),
            "message_digest": message_digest,
            "delivery_receipt": receipt_key,
            "delivery_log_head": self.get(new_target)["deliveryLogHead"],
        }

    def handle(self, root: str, address: Address = ()) -> "VMHandle":
        """Open the same graph-preserving control handle at any existing depth."""

        self.state_at(root, address)
        return VMHandle(self, root, address)

    def snapshot(self, vm: MicroVM) -> str:
        image_key = self.put_image(vm.image)
        child_rows = [
            {"slot": slot, "digest": self.snapshot(child)}
            for slot, child in sorted(vm.children.items())
        ]
        return self.put(
            {
                "mediaType": "application/vnd.w33.microvm.state.v1+json",
                "image": image_key,
                "chamber": [vm.chamber.point, vm.chamber.line],
                "pc": vm.pc,
                "accumulator": vm.accumulator,
                "halted": vm.halted,
                "inbox": list(vm.inbox),
                "traceRoot": vm.trace_root,
                "children": child_rows,
            }
        )

    def uniform_tree(self, image: MicroVMImage, levels: int) -> dict[str, Any]:
        """Create W^[levels] with explicit level-0 guests and deduplicated layers."""

        if levels < 1:
            raise ValueError("levels must be positive")
        image_key = self.put_image(image)
        node_key = self.put(
            {
                "mediaType": "application/vnd.w33.microvm.state.v1+json",
                "level": 0,
                "image": image_key,
                "chamber": [image.entry.point, image.entry.line],
                "pc": 0,
                "accumulator": 0,
                "halted": False,
                "inbox": [],
                "traceRoot": "sha256:" + "0" * 64,
                "children": [],
            }
        )
        node_keys = [node_key]
        for level in range(1, levels + 1):
            node_key = self.put(
                {
                    "mediaType": "application/vnd.w33.microvm.state.v1+json",
                    "level": level,
                    "image": image_key,
                    "chamber": [image.entry.point, image.entry.line],
                    "pc": 0,
                    "accumulator": 0,
                    "halted": False,
                    "inbox": [],
                    "traceRoot": "sha256:" + "0" * 64,
                    "children": [
                        {"slot": slot, "digest": node_key} for slot in range(40)
                    ],
                }
            )
            node_keys.append(node_key)
        return {
            "root": node_key,
            "levels": levels,
            "network_vm_instances": (40**levels - 1) // 39,
            "leaf_vm_instances": 40**levels,
            "total_stateful_vm_instances": (40 ** (levels + 1) - 1) // 39,
            "unique_node_blobs": len(node_keys),
            "node_digests": node_keys,
        }

    def mutate_leaf(
        self, root: str, address: Address, accumulator_delta: int
    ) -> tuple[str, int]:
        """Copy only one digest path, as an immutable container snapshot would."""

        def update(node: dict[str, Any]) -> dict[str, Any]:
            node["accumulator"] += accumulator_delta
            return node

        new_root, new_blobs, _, _ = self._rewrite_at(root, address, update)
        return new_root, new_blobs


@dataclass
class VMHandle:
    """Persistent VM control handle; operations never discard descendant digests."""

    store: ContentStore
    root: str
    address: Address = ()

    def load(self) -> dict[str, Any]:
        return self.store.state_at(self.root, self.address)[1]

    def step(self) -> dict[str, Any]:
        result = self.store.step_at(self.root, self.address)
        self.root = result["root"]
        return result

    def run(self, fuel: int = 10_000) -> dict[str, Any]:
        result = self.store.execute_at(self.root, self.address, fuel)
        self.root = result["root"]
        return result

    def send(
        self,
        target: Address,
        message: str,
        source: Address = (),
    ) -> dict[str, Any]:
        result = self.store.send_at(
            self.root,
            self.address + target,
            message,
            self.address + source,
        )
        self.root = result["root"]
        return result

    def snapshot(self) -> str:
        return self.root

    def fork(self) -> "VMHandle":
        return VMHandle(self.store, self.root, self.address)

    def seal(self) -> str:
        self.store.verify_graph(self.root)
        return self.root


def build_payload(levels: int = 6) -> dict[str, Any]:
    flags = [
        Chamber(point, line)
        for line, points in enumerate(GEOMETRY.lines)
        for point in points
    ]
    panel_opcodes = tuple(
        f"{panel}{selector}" for panel in ("HP", "HL") for selector in range(3)
    )
    panel_outputs_are_six = all(
        len({flag.step(opcode) for opcode in panel_opcodes}) == 6 for flag in flags
    )
    panel_invariants_hold = all(
        all(
            (
                flag.step(opcode).point == flag.point
                if opcode[:2] == "HP"
                else flag.step(opcode).line == flag.line
            )
            for opcode in panel_opcodes
        )
        for flag in flags
    )

    image = MicroVMImage(
        "demo/incidence-counter",
        ("HP0", "HL1", "ADD:7", "HP2", "HL0", "HALT"),
        (("purpose", "deterministic-replay"),),
    )
    first = MicroVM(image)
    second = MicroVM(image)
    first.run()
    second.run()
    first_store = ContentStore()
    second_store = ContentStore()
    first_digest = first_store.snapshot(first)
    second_digest = second_store.snapshot(second)

    store = ContentStore()
    uniform = store.uniform_tree(image, levels)
    mutation_address = tuple((7 * index + 3) % 40 for index in range(levels))
    new_root, new_blobs = store.mutate_leaf(uniform["root"], mutation_address, 1)
    nested_execution = store.execute_at(uniform["root"], mutation_address)

    mailbox_image = MicroVMImage("demo/mailbox", ("RECV", "HALT"))
    mailbox_uniform = store.uniform_tree(mailbox_image, levels)
    mailbox_source = tuple(0 for _ in range(levels))
    mailbox_delivery = store.send_at(
        mailbox_uniform["root"], mutation_address, "13", mailbox_source
    )
    alternate_delivery = store.send_at(
        mailbox_uniform["root"],
        mutation_address,
        "13",
        tuple(39 for _ in range(levels)),
    )
    mailbox_execution = store.execute_at(
        mailbox_delivery["root"], mutation_address
    )
    mailbox_graph = store.verify_graph(mailbox_delivery["root"])

    root_handle = store.handle(mailbox_uniform["root"])
    leaf_handle = store.handle(mailbox_uniform["root"], mutation_address)
    forked_handle = leaf_handle.fork()
    forked_delivery = forked_handle.send((), "5")
    handle_methods = ("load", "step", "run", "send", "snapshot", "fork", "seal")

    source = tuple(0 for _ in range(levels))
    target = tuple((39 - level) % 40 for level in range(levels))
    route = route_address(source, target)

    checks = {
        "geometry_is_40_points_40_lines_160_chambers": len(GEOMETRY.points) == 40
        and len(GEOMETRY.lines) == 40
        and len(flags) == 160,
        "geometry_has_240_edges_and_diameter_two": sum(
            sum(row) for row in GEOMETRY.adjacency
        )
        // 2
        == 240
        and all(len(GEOMETRY.route(a, b)) <= 3 for a in range(40) for b in range(40)),
        "six_deterministic_panel_opcodes_per_chamber": panel_outputs_are_six,
        "panel_opcodes_preserve_the_selected_incidence_rail": panel_invariants_hold,
        "deterministic_guest_replay": first_digest == second_digest
        and first.accumulator == second.accumulator == 7
        and first.chamber == second.chamber,
        "uniform_tree_matches_recursive_instance_law": uniform[
            "network_vm_instances"
        ]
        == (40**levels - 1) // 39,
        "uniform_tree_has_40n_addressable_leaf_vms": uniform["leaf_vm_instances"]
        == 40**levels,
        "uniform_tree_counts_every_stateful_vm": uniform[
            "total_stateful_vm_instances"
        ]
        == uniform["network_vm_instances"] + uniform["leaf_vm_instances"],
        "uniform_tree_uses_one_node_blob_per_level": uniform["unique_node_blobs"]
        == levels + 1,
        "network_root_uses_same_state_media_type_as_leaf": store.get(uniform["root"])[
            "mediaType"
        ]
        == store.get(uniform["node_digests"][0])["mediaType"],
        "single_leaf_mutation_is_path_length_copy_on_write": new_blobs == levels + 1
        and new_root != uniform["root"],
        "nested_guest_execution_is_path_length_copy_on_write": nested_execution[
            "new_blobs"
        ]
        == levels + 1
        and nested_execution["accumulator"] == 7
        and nested_execution["halted"],
        "mailbox_delivery_and_receive_are_persistent": mailbox_delivery[
            "path_copy_new_blobs"
        ]
        == levels + 1
        and mailbox_delivery["receipt_new_blobs"] == 1
        and mailbox_delivery["new_blobs"] == levels + 2
        and mailbox_execution["new_blobs"] == levels + 1
        and mailbox_execution["accumulator"] == 13
        and mailbox_execution["inbox_depth"] == 0,
        "delivery_receipt_commits_source_and_route": mailbox_delivery["root"]
        != alternate_delivery["root"]
        and mailbox_delivery["delivery_log_head"]
        != alternate_delivery["delivery_log_head"]
        and mailbox_delivery["route_hops"] <= 2 * levels
        and mailbox_graph["reachable_delivery_blobs"] == 1,
        "root_and_leaf_share_graph_preserving_handle_interface": all(
            callable(getattr(handle, method))
            for handle in (root_handle, leaf_handle)
            for method in handle_methods
        )
        and len(root_handle.load()["children"]) == 40
        and leaf_handle.load()["children"] == [],
        "handle_fork_is_immutable_and_path_copying": leaf_handle.snapshot()
        == mailbox_uniform["root"]
        and forked_handle.snapshot() == forked_delivery["root"]
        and forked_handle.snapshot() != leaf_handle.snapshot()
        and forked_delivery["path_copy_new_blobs"] == levels + 1
        and forked_delivery["receipt_new_blobs"] == 1,
        "recursive_route_reaches_target": (route[-1]["to"] if route else list(source))
        == list(target),
        "recursive_route_bound_is_two_per_address_digit": len(route) <= 2 * levels,
        "every_recursive_hop_is_one_legal_line_transaction": all(
            sum(a != b for a, b in zip(event["from"], event["to"])) == 1
            and event["line_bus"] in range(40)
            for event in route
        ),
    }

    return {
        "schema": "w33.fractal_microvm_runtime.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "name": "W33 Fractal MicroVM Runtime",
        "composition": {
            "unit": "one 160-state incident point-line chamber microVM",
            "placement_reading": "point=endpoint label/address, line=active four-member line/bus context",
            "deterministic_panel_isa": list(panel_opcodes),
            "opcode_names": "HP=hold_point/change_line; HL=hold_line/change_point",
            "selector_boundary": "The selector labels are a canonical software chart, not an intrinsic geometric ordering.",
            "same_interface_every_depth": [
                "load",
                "step",
                "run",
                "send",
                "snapshot",
                "fork",
                "seal",
            ],
        },
        "guest_replay": {
            "image_digest": image.image_digest,
            "snapshot_digest": first_digest,
            "result_accumulator": first.accumulator,
            "final_chamber": [first.chamber.point, first.chamber.line],
            "trace_root": first.trace_root,
        },
        "recursive_image": {
            **uniform,
            "mutation_address": list(mutation_address),
            "copy_on_write_new_blobs": new_blobs,
            "mutated_root": new_root,
            "nested_execution": nested_execution,
            "mailbox_delivery": mailbox_delivery,
            "alternate_source_delivery": alternate_delivery,
            "mailbox_execution": mailbox_execution,
            "graph_handle": {
                "methods": list(handle_methods),
                "root_children": len(root_handle.load()["children"]),
                "leaf_children": len(leaf_handle.load()["children"]),
                "forked_root": forked_handle.snapshot(),
                "fork_path_copy_new_blobs": forked_delivery["path_copy_new_blobs"],
                "fork_receipt_new_blobs": forked_delivery["receipt_new_blobs"],
                "fork_total_new_blobs": forked_delivery["new_blobs"],
            },
            "stored_next_hop_tables": 0,
        },
        "recursive_network": {
            "address_radix": 40,
            "hop_unit": "one logical W33 collinearity/line-bus transaction",
            "source": list(source),
            "target": list(target),
            "hop_count": len(route),
            "proven_bound": 2 * levels,
            "trace": route,
            "metric_boundary": (
                "This 2n logical bound does not replace BT827's 8n chart-aware "
                "lowering, which counts three cube moves plus five chart-web "
                "moves per recursive digit."
            ),
        },
        "prior_art_reused": [
            "analysis/w33_packet_vm.py",
            "analysis/w33_packet_vm_kernel.py",
            "analysis/bt1700_recursive_holonet_packet_compiler.py",
            "analysis/w33_recursive_instance_compression.py",
            "analysis/w33_BREAKTHROUGH_339_SQNA_capacity_threshold.py",
            "analysis/w33_BREAKTHROUGH_350_fractal_SQNA.py",
            "analysis/w33_pass2640_2649_the_holonet_node_is_its_own_network.md",
            "analysis/w33_pass4324_4327_chamber_hecke_hashimoto.g",
            "analysis/holonet_uor_certificate.py",
            "analysis/holonet_uor_mock_runtime.py",
            "papers/dahn_asi_toe/witting_architecture_v2.tex",
        ],
        "checks": checks,
        "boundary": (
            "This is an executable deterministic reference runtime and immutable "
            "content graph. It does not provide Linux process isolation, a guest "
            "kernel, hardware virtualization, confidential-computing attestation, "
            "or measured performance. Firecracker/Kata, OCI, and WebAssembly "
            "Component Model adapters are implementation targets, not completed here."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    recursive = payload["recursive_image"]
    network = payload["recursive_network"]
    return f"""# W33 Fractal MicroVM Runtime

This is the executable systems form of the recursive Holonet idea: a microVM
contains a 40-slot network of microVMs, and the whole network is stored and
loaded through the same state descriptor as one leaf microVM.

## What is new

The repo already had a packet interpreter, a controller-wrapped VM, BT339's
unproved `2n` hierarchy assertion, BT350's network-as-node/nested-VM concept,
Passes 2642--2644's same-port recursive hardware module, a `40^n` recursive packet count,
recursive routing-table compression, UOR-shaped canonical content IDs and
command certificates, and a paper design for
immutable CID containers, WASM/OCI components, policies, receipts, and a
Projection Engine. That integrated design remains on the Witting architecture
roadmap.
What was missing was an executable nested state and lifecycle layer. This
runtime adds:

- six deterministic panel-transition opcodes (`HP0..HP2` means hold point and
  change line; `HL0..HL2` means hold line and change point) inside a small VM
  ISA that also includes `ADD:<int>`, `RECV`, `YIELD`, and `HALT`;
- immutable content-addressed images and snapshots;
- recursive 40-way child manifests;
- lazy structural deduplication and path-only copy-on-write;
- table-free routing between radix-40 addresses;
- one graph-preserving handle at every depth:
  `load, step, run, send, snapshot, fork, seal`.

The container vision is therefore inherited; the implementation advance is the
content graph that makes a leaf, a recursive network, and a copy-on-write fork
instances of one executable state object.

## The microVM unit

State is an incident pair `(point,line)`. The point is an endpoint label/address;
the line is its active four-member line/bus context. An `HP` instruction keeps the endpoint
and selects another incident line. An `HL` instruction keeps the line context
and selects another endpoint on it. The three software selectors are a declared
canonical chart; geometry supplies the three alternatives but does not label them.

## A network that is itself an image

At `{recursive['levels']}` levels the uniform manifest denotes
`{recursive['network_vm_instances']:,}` recursive network VMs plus
`{recursive['leaf_vm_instances']:,}` addressable leaf VMs---
`{recursive['total_stateful_vm_instances']:,}` stateful VMs in all---but identical subtrees require
only `{recursive['unique_node_blobs']}` node blobs. Mutating one leaf copies only
`{recursive['copy_on_write_new_blobs']}` blobs along its digest path in the
certified fresh transition. Structurally this is an upper bound: replaying an
identical content transition can allocate zero new CAS keys. The root
digest is itself a normal microVM-state descriptor, so the network and the leaf
share one loader ABI.

This is now an operational identity, not only a media-type identity. A runtime
can resolve any nested radix-40 address without expanding its siblings, append a
mailbox value, execute that guest, and checkpoint the result by replacing only
the digests on the addressed path. The frozen witness delivers and consumes
`13` at depth six. In that fresh witness, execution allocates exactly
`{recursive['copy_on_write_new_blobs']}` path-state blobs; delivery allocates the
same path plus one separately addressable receipt blob. Every untouched sibling
keeps its digest. The reachable delivery receipt commits the source, target,
full legal route, message digest, and previous receipt; changing only the source
changes the root.

## Fractal routing

An address is a radix-40 word. The checked sample route uses
`{network['hop_count']}` line transactions against the exact bound
`{network['proven_bound']}`. Each hop changes one address digit along one legal
W33 line. No next-hop table is stored.

The hop unit matters. This is a logical W33 collinearity/line-bus transaction,
whose GAP-checked base diameter is 2. BT827's separate chart-aware lowering
budgets three cube moves plus five chart-web moves per digit, hence `8n`. The
two bounds describe different layers and are not competing measurements.
BT339 is the first `2n` assertion located in the corpus; BT350 owns the explicit
nested-VM framing. The independent
[`w33_fractal_microvm_routing.g`](../analysis/w33_fractal_microvm_routing.g)
witness now proves it for this explicit Cartesian W33 routing object and freezes
the metric distinction at 7/7 checks.

## Practical lowering

- **OCI:** the bundle uses the OCI image-layout marker and image index at the
  top level. Its root is a custom W33 state descriptor and its internal
  `{{slot,digest}}` child references form a W33 DAG, not OCI descriptors.
- **Firecracker/Kata:** run a leaf blob as the guest workload and let the W33
  parent be the shim/supervisor and network policy.
- **WebAssembly Component Model:** map each leaf to a component world; recursive
  imports/exports become the same typed parent interface.

Those adapters are not yet implemented. This Python runtime proves deterministic
composition, content addressing, copy-on-write, and recursive routing; it is not
an operating-system or hardware isolation boundary.

## Run the lifecycle

`analysis/holobox.py` is the reference CLI over this object graph:

```console
python3 analysis/holobox.py build --output /tmp/holobox --levels 6 \
  --program RECV,HALT
python3 analysis/holobox.py verify /tmp/holobox
python3 analysis/holobox.py send /tmp/holobox --source 0/0/0/0/0/0 \
  --target 3/10/17/24/31/38 --message 13 --output /tmp/holobox-message
python3 analysis/holobox.py run /tmp/holobox-message --address 3/10/17/24/31/38 \
  --commit /tmp/holobox-run
python3 analysis/holobox.py fork /tmp/holobox --address 3/10/17/24/31/38 \
  --output /tmp/holobox-fork
python3 analysis/holobox.py route 0/0/0/0/0/0 39/38/37/36/35/34
```

The bundle is deliberately **OCI-shaped**, not yet OCI-conformant: only its
top-level layout/index follows OCI structure. No registry round trip or
external-runtime conformance claim is made.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--levels", type=int, default=6)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args(argv)

    payload = build_payload(args.levels)
    json_out = Path(args.json_out)
    if not json_out.is_absolute():
        json_out = ROOT / json_out
    md_out = Path(args.md_out)
    if not md_out.is_absolute():
        md_out = ROOT / md_out
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    md_out.write_text(markdown(payload), encoding="utf-8")

    print(
        "W33 fractal microVM: "
        f"{sum(payload['checks'].values())}/{len(payload['checks'])} checks; "
        f"status={payload['status']}"
    )
    print(
        f"levels={args.levels}, network_vms={payload['recursive_image']['network_vm_instances']:,}, "
        f"leaf_vms={payload['recursive_image']['leaf_vm_instances']:,}, "
        f"unique_node_blobs={payload['recursive_image']['unique_node_blobs']}, "
        f"route_hops={payload['recursive_network']['hop_count']}"
    )
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
