#!/usr/bin/env python3
"""Pass 2774: line x nonsquare-form compression of the 480 CX cosets."""
from __future__ import annotations

import gzip
import io
import itertools
import json
import os
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
Q = 3
Mat = tuple[tuple[int, ...], ...]
I4: Mat = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))
J = np.array(((0, 1, 0, 0), (2, 0, 0, 0), (0, 0, 0, 1), (0, 0, 2, 0)), dtype=int)
FP: Mat = ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
FF: Mat = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0))
SP: Mat = ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
SF: Mat = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1))
CX: Mat = ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1))
GENERATOR_CODES = {"Fp": 0, "Fp^-1": 1, "Ff": 2, "Ff^-1": 3, "Sp": 4, "Sp^-1": 5, "Sf": 6, "Sf^-1": 7, "CX": 8, "CX^-1": 9}
HASH_MODULUS = 223
HASH_WEIGHTS = [56, 193, 70, 109, 20, 134, 134, 109, 117, 52, 188, 170, 130, 46, 156, 123]


def mm(a: Mat, b: Mat) -> Mat:
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % Q for j in range(4)) for i in range(4))


def inv(a: Mat) -> Mat:
    aug = [list(a[i]) + [int(i == j) for j in range(4)] for i in range(4)]
    r = 0
    for c in range(4):
        p = next(i for i in range(r, 4) if aug[i][c] % Q)
        aug[r], aug[p] = aug[p], aug[r]
        scale = 1 if aug[r][c] % Q == 1 else 2
        aug[r] = [(scale * x) % Q for x in aug[r]]
        for i in range(4):
            if i != r and aug[i][c] % Q:
                f = aug[i][c] % Q
                aug[i] = [(aug[i][j] - f * aug[r][j]) % Q for j in range(8)]
        r += 1
    return tuple(tuple(row[4:]) for row in aug)


def generators() -> list[tuple[str, Mat]]:
    out = []
    for name, g in (("Fp", FP), ("Ff", FF), ("Sp", SP), ("Sf", SF), ("CX", CX)):
        out.append((name, g))
        gi = inv(g)
        if gi != g:
            out.append((name + "^-1", gi))
    return out


def generate_group() -> tuple[list[Mat], dict[Mat, tuple[Mat | None, str | None]], dict[Mat, int]]:
    parent: dict[Mat, tuple[Mat | None, str | None]] = {I4: (None, None)}
    distance = {I4: 0}
    q = deque([I4])
    gens = generators()
    while q:
        x = q.popleft()
        for name, g in gens:
            y = mm(x, g)
            if y not in parent:
                parent[y] = (x, name)
                distance[y] = distance[x] + 1
                q.append(y)
    assert len(parent) == 51840
    return list(parent), parent, distance


def word(g: Mat, parent: dict[Mat, tuple[Mat | None, str | None]]) -> list[str]:
    out = []
    while g != I4:
        prev, name = parent[g]
        assert prev is not None and name is not None
        out.append(name)
        g = prev
    return out[::-1]


def arr(g: Mat) -> np.ndarray:
    return np.array(g, dtype=int) % 3


def key(a: np.ndarray) -> tuple[int, ...]:
    return tuple(int(x) for x in a.ravel())


def rank3(a: np.ndarray) -> int:
    b = a.copy() % 3
    r = 0
    for c in range(b.shape[1]):
        p = next((i for i in range(r, b.shape[0]) if b[i, c]), None)
        if p is None:
            continue
        b[[r, p]] = b[[p, r]]
        b[r] = ((1 if b[r, c] == 1 else 2) * b[r]) % 3
        for i in range(b.shape[0]):
            if i != r and b[i, c]:
                b[i] = (b[i] - b[i, c] * b[r]) % 3
        r += 1
    return r


def normalize(v: np.ndarray) -> np.ndarray:
    v = v.copy() % 3
    first = next(int(x) for x in v if x)
    return (v * (1 if first == 1 else 2)) % 3


def line_basis(n: np.ndarray) -> tuple[np.ndarray, np.ndarray, tuple[tuple[int, ...], ...]]:
    basis: list[np.ndarray] = []
    for j in range(4):
        v = n[:, j]
        if np.any(v):
            candidate = np.column_stack(basis + [v]) if basis else v.reshape(-1, 1)
            if rank3(candidate) > len(basis):
                basis.append(v.copy())
    assert len(basis) == 2
    points = {
        tuple(normalize(a * basis[0] + b * basis[1]).tolist())
        for a, b in itertools.product(range(3), repeat=2)
        if a or b
    }
    ordered = sorted(points)
    l1 = np.array(ordered[0], dtype=int)
    l2 = next(np.array(v, dtype=int) for v in ordered[1:] if rank3(np.column_stack([l1, v])) == 2)
    return l1, l2, tuple(ordered)


def pairing(u: np.ndarray, v: np.ndarray) -> int:
    return int(u @ J @ v % 3)


def dual_complement(l1: np.ndarray, l2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    vectors = [np.array(v, dtype=int) for v in itertools.product(range(3), repeat=4)]
    for m1 in vectors:
        if pairing(l1, m1) != 1 or pairing(l2, m1) != 0:
            continue
        for m2 in vectors:
            if pairing(l1, m2) == 0 and pairing(l2, m2) == 1 and pairing(m1, m2) == 0:
                return m1, m2
    raise AssertionError("no dual complement")


def local_form(x: np.ndarray) -> tuple[tuple[tuple[int, ...], ...], tuple[int, int, int, int]]:
    n = (x - np.eye(4, dtype=int)) % 3
    assert rank3(n) == 2 and np.all(n @ n % 3 == 0)
    l1, l2, line = line_basis(n)
    m1, m2 = dual_complement(l1, l2)
    form = np.zeros((2, 2), dtype=int)
    for j, m in enumerate((m1, m2)):
        y = n @ m % 3
        coeff = next((a, b) for a, b in itertools.product(range(3), repeat=2) if np.array_equal((a * l1 + b * l2) % 3, y))
        form[:, j] = coeff
    assert form[0, 1] == form[1, 0]
    assert round(np.linalg.det(form)) % 3 == 2
    return line, tuple(int(v) for v in form.ravel())


def order(a: np.ndarray) -> int:
    x = np.eye(4, dtype=int)
    for n in range(1, 100):
        x = x @ a % 3
        if np.array_equal(x, np.eye(4, dtype=int)):
            return n
    raise AssertionError("order")


def subgroup(gens: list[np.ndarray]) -> list[np.ndarray]:
    ident = np.eye(4, dtype=int)
    seen = {key(ident): ident}
    q = deque([ident])
    while q:
        x = q.popleft()
        for g in gens:
            y = x @ g % 3
            if key(y) not in seen:
                seen[key(y)] = y
                q.append(y)
    return list(seen.values())


def power(a: np.ndarray, n: int) -> np.ndarray:
    x = np.eye(4, dtype=int)
    for _ in range(n):
        x = x @ a % 3
    return x


def encode_word(names: list[str]) -> int:
    assert len(names) <= 6
    packed = 0
    for i, name in enumerate(names):
        packed |= GENERATOR_CODES[name] << (4 * i)
    return packed


def build() -> dict:
    group, parent, distance = generate_group()
    cxa = arr(CX)
    best_by_conjugate: dict[tuple[int, ...], Mat] = {}
    matrix_by_conjugate: dict[tuple[int, ...], np.ndarray] = {}
    for g in group:
        ga = arr(g)
        x = ga @ cxa @ arr(inv(g)) % 3
        xkey = key(x)
        if xkey not in best_by_conjugate or distance[g] < distance[best_by_conjugate[xkey]] or (
            distance[g] == distance[best_by_conjugate[xkey]] and g < best_by_conjugate[xkey]
        ):
            best_by_conjugate[xkey] = g
            matrix_by_conjugate[xkey] = x
    assert len(best_by_conjugate) == 480

    representatives: dict[tuple[tuple[tuple[int, ...], ...], tuple[int, ...]], Mat] = {}
    for xkey, g in best_by_conjugate.items():
        packet = local_form(matrix_by_conjugate[xkey])
        assert packet not in representatives
        representatives[packet] = g
    assert len(representatives) == 480

    lines = sorted({packet[0] for packet in representatives})
    forms = sorted({packet[1] for packet in representatives})
    assert len(lines) == 40 and len(forms) == 12
    assert all((f[0] * f[3] - f[1] * f[2]) % 3 == 2 and f[1] == f[2] for f in forms)

    rep_rows = []
    for line_id, line in enumerate(lines):
        for form_id, form in enumerate(forms):
            g = representatives[(line, form)]
            names = word(g, parent)
            rep_rows.append({
                "class_id": 12 * line_id + form_id,
                "line_id": line_id,
                "form_id": form_id,
                "length": len(names),
                "word": names,
                "packed_word_hex": f"0x{encode_word(names):06x}",
                "representative_matrix": [list(row) for row in g],
            })
    assert max(row["length"] for row in rep_rows) == 6

    centralizer = [arr(g) for g in group if mm(g, CX) == mm(CX, g)]
    assert len(centralizer) == 108
    center = [c for c in centralizer if all(np.array_equal(c @ d % 3, d @ c % 3) for d in centralizer)]
    assert len(center) == 18
    a = b = None
    for ca in center:
        if order(ca) != 6:
            continue
        for cb in center:
            if order(cb) == 3 and len(subgroup([ca, cb])) == 18:
                a, b = ca, cb
                break
        if a is not None:
            break
    assert a is not None and b is not None
    center_keys = {key(c) for c in center}
    s = t = None
    for cs in centralizer:
        if order(cs) != 2 or key(cs) in center_keys:
            continue
        for ct in centralizer:
            if order(ct) != 3 or key(ct) in center_keys:
                continue
            h = subgroup([cs, ct])
            if len(h) == 6 and len({key(x) for x in h} & center_keys) == 1 and not np.array_equal(cs @ ct % 3, ct @ cs % 3):
                s, t = cs, ct
                break
        if s is not None:
            break
    assert s is not None and t is not None
    h_elements = [np.eye(4, dtype=int), t, power(t, 2), s, s @ t % 3, s @ power(t, 2) % 3]
    factor = {}
    for i, j, h_id in itertools.product(range(6), range(3), range(6)):
        c = power(a, i) @ power(b, j) % 3 @ h_elements[h_id] % 3
        factor[key(c)] = (i, j, h_id)
    assert len(factor) == 108

    hashes = {}
    suffix_rows = []
    for c in centralizer:
        hval = sum(w * v for w, v in zip(HASH_WEIGHTS, key(c))) % HASH_MODULUS
        assert hval not in hashes
        hashes[hval] = key(c)
        i, j, h_id = factor[key(c)]
        suffix_rows.append({"hash": hval, "c6": i, "c3": j, "s3": h_id, "code": i + 6 * j + 18 * h_id})
    assert len(hashes) == 108

    rep_bits = 480 * (3 + 6 * 4)
    suffix_bits = HASH_MODULUS * 7
    classifier_bits = 40 * 16 + 12 * 6
    compressed_bits = rep_bits + suffix_bits + classifier_bits
    baseline_bits = 51840 * 16
    return {
        "schema": "w33.pass2774.compressed_cx_compiler.v1",
        "status": "EXACT_LINE_FORM_AND_PERFECT_HASH_COMPILER",
        "theorem": {
            "cx_conjugacy_class": 480,
            "factorization": "40 Lagrangian lines x 12 invertible symmetric 2x2 forms of determinant 2 over F3",
            "lines": len(lines),
            "forms_per_line": len(forms),
            "form_alphabet": [list(f) for f in forms],
        },
        "representative_rom": {
            "rows": len(rep_rows),
            "maximum_word_length": max(row["length"] for row in rep_rows),
            "mean_word_length": sum(row["length"] for row in rep_rows) / len(rep_rows),
            "generator_codes": GENERATOR_CODES,
            "rows_data": rep_rows,
        },
        "centralizer_suffix": {
            "structure": "C6 x C3 x S3",
            "hash_modulus": HASH_MODULUS,
            "hash_weights": HASH_WEIGHTS,
            "occupied_hashes": len(suffix_rows),
            "factor_generators": {"C6": a.tolist(), "C3": b.tolist(), "S3_order2": s.tolist(), "S3_order3": t.tolist()},
            "rows": sorted(suffix_rows, key=lambda r: r["hash"]),
        },
        "storage": {
            "representative_rom_bits": rep_bits,
            "suffix_hash_rom_bits": suffix_bits,
            "line_and_form_classifier_bits": classifier_bits,
            "compressed_total_bits": compressed_bits,
            "compressed_total_bytes": (compressed_bits + 7) // 8,
            "baseline_51840_state_output_table_bits": baseline_bits,
            "compression_ratio": baseline_bits / compressed_bits,
        },
        "boundary": "The line/form classifier assumes the input is in the 480-element CX conjugacy class; suffix hashing assumes the computed residual lies in the order-108 centralizer.",
    }


def emit_rom(result: dict) -> None:
    rows = result["representative_rom"]["rows_data"]
    lines = [
        "// Pass 2774: 480-entry compressed representative-word ROM.",
        "module w33_pass2774_cx_rep_rom(input logic [8:0] class_id, output logic valid, output logic [2:0] length, output logic [23:0] packed_word);",
        "always_comb begin valid=1'b1; length=3'd0; packed_word=24'd0; case(class_id)",
    ]
    for row in rows:
        lines.append(f"9'd{row['class_id']}: begin length=3'd{row['length']}; packed_word=24'h{row['packed_word_hex'][2:]}; end")
    lines += ["default: begin valid=1'b0; length=3'd0; packed_word=24'd0; end", "endcase end", "endmodule", ""]
    (ROOT / "rtl" / "w33_pass2774_cx_rep_rom.sv").write_text("\n".join(lines))

    suffix = result["centralizer_suffix"]
    lines = [
        "// Pass 2774: perfect-hash decoder for C6 x C3 x S3 suffix coordinates.",
        "module w33_pass2774_cx_suffix_hash(input logic [31:0] matrix_trits, output logic valid, output logic [2:0] c6, output logic [1:0] c3, output logic [2:0] s3);",
        "integer i; integer acc; integer h;",
        "always_comb begin",
        "  acc=0;",
    ]
    for i, weight in enumerate(HASH_WEIGHTS):
        lines.append(f"  acc = acc + {weight} * matrix_trits[{2*i} +: 2];")
    lines += ["  h = acc % 223; valid=1'b1; c6=3'd0; c3=2'd0; s3=3'd0;", "  case(h)"]
    for row in suffix["rows"]:
        lines.append(f"  8'd{row['hash']}: begin c6=3'd{row['c6']}; c3=2'd{row['c3']}; s3=3'd{row['s3']}; end")
    lines += ["  default: begin valid=1'b0; c6=3'd0; c3=2'd0; s3=3'd0; end", "  endcase", "end", "endmodule", ""]
    (ROOT / "rtl" / "w33_pass2774_cx_suffix_hash.sv").write_text("\n".join(lines))


def deterministic_gzip(payload: bytes) -> bytes:
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as handle:
        handle.write(payload)
    return buf.getvalue()


def main() -> None:
    out = build()
    raw = (json.dumps(out, sort_keys=True, separators=(",", ":")) + "\n").encode()
    if os.environ.get("W33_EMIT_FULL_CERT") == "1":
        path = ROOT / "data" / "PART_BT2774_COMPRESSED_CX_COMPILER.json.gz"
        path.write_bytes(deterministic_gzip(raw))
    summary = {
        "schema": out["schema"],
        "status": out["status"],
        "theorem": out["theorem"],
        "storage": out["storage"],
        "maximum_word_length": out["representative_rom"]["maximum_word_length"],
        "centralizer_occupied_hashes": out["centralizer_suffix"]["occupied_hashes"],
    }
    (ROOT / "data" / "PART_BT2774_COMPRESSED_CX_COMPILER_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    emit_rom(out)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
