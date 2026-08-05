"""Passes 3635-3648 exact Monster/U4(2) completion verifier.

The implementation is split into two adjacent source fragments to keep the
GitHub connector writes inspectable.  This loader concatenates and executes
them as one audited Python program.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARTS = [
    HERE / "_w33_pass3635_3648_impl_part1.pyinc",
    HERE / "_w33_pass3635_3648_impl_part2.pyinc",
]
source = "\n".join(path.read_text(encoding="utf-8") for path in PARTS)
exec(compile(source, str(PARTS[0]), "exec"), globals(), globals())
