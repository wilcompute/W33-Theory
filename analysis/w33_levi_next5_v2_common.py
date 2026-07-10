#!/usr/bin/env python3
"""Five deeper closures for the W(3,3) / Photonic Holonet architecture.

Tracks
------
1. Exact symbolic proof certificate for the odd-q binary Levi rank theorem.
2. Sentinel [40,15,8]_2 code integrated into authenticated packet admission.
3. Exact lift of 1 + U14- through the chiral 2-adic discriminant form.
4. Native PSp(4,3):2 action on all 51840 runtime states.
5. Loss-aware photonic compiler for the integral 8x80 Levi-to-E8 map.
"""
from __future__ import annotations

import argparse
import cmath
from collections import Counter, deque
from dataclasses import replace
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import struct
from typing import Iterable

import numpy as np
from sympy import Matrix, ZZ, simplify, symbols
from sympy.matrices.normalforms import smith_normal_decomp

import w33_levi_five_frontiers as base
from holonet_typed_packet import PacketValidationError, TypedPacket
from holonet_typed_fault_stack import AdmissionError, RouteRetry, TransportEnvelope, TypedFaultStack

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_2026_07_10_LEVI_NEXT5_V2_results.json"

BT982_B = Matrix([
    [-1, 1, 1, -2, 1, 1, -1, 0],
    [-1, 2, 0, -3, 2, 2, -2, 0],
    [-1, 2, 0, -4, 3, 3, -3, -1],
    [-1, 1, 0, -3, 2, 3, -2, -1],
    [-1, 0, 0, -2, 2, 2, -2, 0],
    [-1, 0, 0, -1, 1, 1, -1, 0],
    [0, 0, 0, -1, 1, 0, 0, 0],
    [-1, 1, 0, -2, 2, 1, -1, -1],
])


def canonical_hash(payload: object) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def bit_columns_to_rows(columns: Iterable[int], height: int) -> list[int]:
    columns = list(columns)
    return [sum(((column >> row) & 1) << col for col, column in enumerate(columns)) for row in range(height)]

