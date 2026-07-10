#!/usr/bin/env python3
"""Typed point/line packets for the runnable Holonet VM.

A valid packet is a cycle for one of the two square-zero Levi differentials:
point/address packets use A_P and an 8-bit homology syndrome; line/route packets
use A_L and a 20-bit syndrome. A legal mirror conversion applies M^T or M before
toggling the type. Merely retagging the payload is rejected.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import random
from typing import Iterable

import w33_levi_five_frontiers as levi


class PacketValidationError(ValueError):
    pass


class TypeConfusionError(PacketValidationError):
    pass


@dataclass(frozen=True)
class PacketContext:
    name: str
    type_bit: int
    differential: list[int]
    image: list[int]
    homology: list[int]
    tagged: dict[int, tuple[int, int]]

    @property
    def image_dimension(self) -> int:
        return len(self.image)

    @property
    def homology_dimension(self) -> int:
        return len(self.homology)


@dataclass(frozen=True)
class TypedPacket:
    type_bit: int
    syndrome: int
    payload: int

    def as_dict(self) -> dict:
        return {
            "type_bit": self.type_bit,
            "type": "point/address" if self.type_bit == 0 else "line/route",
            "syndrome": self.syndrome,
            "syndrome_hex": hex(self.syndrome),
            "payload_hex": f"0x{self.payload:010x}",
            "payload_weight": self.payload.bit_count(),
        }


class LeviTypedKernel:
    def __init__(self) -> None:
        self.geometry = levi.build_geometry(3)
        self.contexts = {
            0: self._context("point/address", 0, self.geometry.point_adjacency),
            1: self._context("line/route", 1, self.geometry.line_adjacency),
        }

    @staticmethod
    def _context(name: str, type_bit: int, differential: list[int]) -> PacketContext:
        image = levi.gf2_row_basis(differential)
        kernel = levi.gf2_nullspace(differential, 40)
        homology = levi.quotient_basis(kernel, image)
        return PacketContext(
            name=name,
            type_bit=type_bit,
            differential=differential,
            image=image,
            homology=homology,
            tagged=levi.tagged_basis(image + homology),
        )

    def _syndrome(self, context: PacketContext, payload: int) -> int:
        if payload < 0 or payload >= (1 << 40):
            raise PacketValidationError("payload must be a 40-bit nonnegative integer")
        if levi.gf2_apply(context.differential, payload) != 0:
            raise PacketValidationError(f"payload is not a cycle in the {context.name} complex")
        remainder, tag = levi.coordinates(payload, context.tagged)
        if remainder:
            raise PacketValidationError("cycle was not representable in image plus homology basis")
        return (tag >> context.image_dimension) & ((1 << context.homology_dimension) - 1)

    def encode(self, type_bit: int, payload: int) -> TypedPacket:
        if type_bit not in self.contexts:
            raise PacketValidationError("type bit must be 0 (point) or 1 (line)")
        context = self.contexts[type_bit]
        return TypedPacket(type_bit, self._syndrome(context, payload), payload)

    def validate(self, packet: TypedPacket) -> bool:
        context = self.contexts.get(packet.type_bit)
        if context is None:
            raise PacketValidationError("unknown packet type")
        actual = self._syndrome(context, packet.payload)
        if actual != packet.syndrome:
            raise PacketValidationError(
                f"syndrome mismatch for {context.name}: header={packet.syndrome}, actual={actual}"
            )
        return True

    def mirror(self, packet: TypedPacket) -> TypedPacket:
        self.validate(packet)
        if packet.type_bit == 0:
            payload = levi.gf2_apply(self.geometry.incidence_columns, packet.payload)
            target_type = 1
        else:
            payload = levi.gf2_apply(self.geometry.incidence_rows, packet.payload)
            target_type = 0
        converted = self.encode(target_type, payload)
        if converted.syndrome != 0:
            raise AssertionError("incidence mirror did not land in a target boundary")
        return converted

    def raw_retag(self, packet: TypedPacket) -> TypedPacket:
        """Attempt an illegal type toggle without applying the incidence map."""
        self.validate(packet)
        target = 1 - packet.type_bit
        try:
            retagged = self.encode(target, packet.payload)
        except PacketValidationError as exc:
            raise TypeConfusionError(str(exc)) from exc
        if retagged.syndrome != packet.syndrome:
            raise TypeConfusionError(
                f"payload occupies inequivalent syndrome namespaces: {packet.syndrome} != {retagged.syndrome}"
            )
        raise TypeConfusionError("raw retag forbidden even when both headers happen to be trivial")

    @staticmethod
    def _random_combination(rng: random.Random, basis: Iterable[int]) -> int:
        out = 0
        for generator in basis:
            if rng.getrandbits(1):
                out ^= generator
        return out

    def fuzz(self, seed: int = 0, trials: int = 256) -> dict:
        rng = random.Random(seed)
        legal_ok = 0
        retag_rejected = 0
        for _ in range(trials):
            type_bit = rng.randrange(2)
            context = self.contexts[type_bit]
            payload = self._random_combination(rng, context.image + context.homology)
            packet = self.encode(type_bit, payload)
            mirrored = self.mirror(packet)
            if self.validate(mirrored) and mirrored.syndrome == 0:
                legal_ok += 1
            representative = rng.choice(context.homology)
            probe = self.encode(type_bit, representative)
            try:
                self.raw_retag(probe)
            except TypeConfusionError:
                retag_rejected += 1
        return {
            "seed": seed,
            "trials": trials,
            "legal_mirrors_passed": legal_ok,
            "raw_retags_rejected": retag_rejected,
            "all_pass": legal_ok == trials and retag_rejected == trials,
        }

    def demo(self) -> dict:
        point_context = self.contexts[0]
        source = self.encode(0, point_context.homology[0])
        target = self.mirror(source)
        rejected = False
        reason = None
        try:
            self.raw_retag(source)
        except TypeConfusionError as exc:
            rejected = True
            reason = str(exc)
        return {
            "source": source.as_dict(),
            "legal_mirror": {"packet": target.as_dict(), "target_syndrome": target.syndrome},
            "raw_retag": {"rejected": rejected, "reason": reason},
        }

    def info(self) -> dict:
        return {
            "header": ["type_bit", "homology_syndrome", "40_bit_payload"],
            "types": {
                "0": {"name": self.contexts[0].name, "syndrome_width": 8, "differential_rank": 16},
                "1": {"name": self.contexts[1].name, "syndrome_width": 20, "differential_rank": 10},
            },
            "legal_conversion": "toggle type only after applying M^T or M; target syndrome must be zero",
            "illegal_conversion": "raw type retag is rejected",
        }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="holonet", description="Typed Levi packet kernel")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("packet-info")
    sub.add_parser("packet-demo")
    fuzz = sub.add_parser("packet-fuzz")
    fuzz.add_argument("--seed", type=int, default=0)
    fuzz.add_argument("--trials", type=int, default=256)
    args = parser.parse_args(argv)
    kernel = LeviTypedKernel()
    if args.cmd == "packet-info":
        out = kernel.info()
    elif args.cmd == "packet-demo":
        out = kernel.demo()
    else:
        out = kernel.fuzz(args.seed, args.trials)
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out.get("all_pass", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
