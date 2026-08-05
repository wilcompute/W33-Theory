"""Passes 3670-3686 exact nine-front Monster/tomotope verifier loader."""
from pathlib import Path
HERE = Path(__file__).resolve().parent
PARTS = [
    HERE / "_w33_pass3670_3686_impl_part1.pyinc",
    HERE / "_w33_pass3670_3686_impl_part2.pyinc",
]
source = "\n".join(path.read_text(encoding="utf-8") for path in PARTS)
exec(compile(source, str(PARTS[0]), "exec"), globals(), globals())
