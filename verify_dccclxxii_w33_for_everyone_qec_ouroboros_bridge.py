#!/usr/bin/env python3
"""Verifier for Part DCCCLXXII."""

from scripts.w33_for_everyone_consistency_bridge import write_bridge


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
