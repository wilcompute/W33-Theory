#!/usr/bin/env python3
"""Collision-safe loader for the Passes 3795-3812 exact verifier."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARTS = [HERE / f"_w33_pass3795_3812_impl_part{i}.pyinc" for i in range(1, 5)]
SOURCE = "".join(path.read_text(encoding="utf-8") for path in PARTS)
NAMESPACE = {
    "__name__": "w33_pass3795_3812_impl",
    "__file__": str(Path(__file__).resolve()),
}
exec(compile(SOURCE, str(Path(__file__).resolve()), "exec"), NAMESPACE)
build = NAMESPACE["build"]
main = NAMESPACE["main"]

if __name__ == "__main__":
    main()
