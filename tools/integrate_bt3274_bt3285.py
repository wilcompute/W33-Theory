#!/usr/bin/env python3
"""Byte-preserving, idempotent integration for Passes 3274-3285."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX_INSERT = (ROOT / "analysis" / "BT3274_BT3285_twisted_rom_runtime_reset_insert.tex").read_bytes()
HTML_INSERT = (ROOT / "analysis" / "BT3274_BT3285_twisted_rom_runtime_reset_index_insert.html").read_bytes()
TEX_BEGIN = b"% BEGIN BT3274-BT3285 TWISTED ROM RUNTIME RESET\n"
TEX_END = b"% END BT3274-BT3285 TWISTED ROM RUNTIME RESET\n"
HTML_BEGIN = b"<!-- BEGIN BT3274-BT3285 TWISTED ROM RUNTIME RESET -->"
HTML_END = b"<!-- END BT3274-BT3285 TWISTED ROM RUNTIME RESET -->"


def splice(path: Path, begin: bytes, end: bytes, payload: bytes, anchors: tuple[bytes,...]) -> None:
    data = path.read_bytes()
    block = begin + payload.rstrip() + b"\n" + end
    if begin in data:
        left = data.index(begin)
        right = data.index(end, left) + len(end)
        new = data[:left] + block + data[right:]
    else:
        positions = [(data.rfind(anchor), anchor) for anchor in anchors if data.rfind(anchor) >= 0]
        if not positions:
            raise RuntimeError(f"no integration anchor in {path}")
        position, _ = max(positions)
        new = data[:position] + b"\n" + block + b"\n" + data[position:]
    path.write_bytes(new)


def main() -> None:
    for name in ("w33_paper.tex", "photonic_holonet.tex", "holonet_machine_blueprint.tex"):
        splice(ROOT/name, TEX_BEGIN, TEX_END, TEX_INSERT, (b"\\end{document}",))
    splice(ROOT/"docs"/"index.html", HTML_BEGIN, HTML_END, HTML_INSERT,
           (b"</main>", b"</body>", b"</html>"))
    print("integrated BT3274-BT3285 into three papers and docs/index.html")


if __name__ == "__main__": main()
