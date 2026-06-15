#!/usr/bin/env python3
from pathlib import Path
import argparse

ROW = "\\input{paper/sections/sec_bt1126_1128_holonet_mainpaper_fixture_numeric}\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    p = Path("photonic_holonet.tex")
    s = p.read_text()
    marker = "\\subsection{The ethos}"
    print(f"target={p}")
    print(f"planned_inserts={0 if ROW.strip() in s else 1}")
    if ROW.strip() in s:
        return
    if marker not in s:
        raise SystemExit("marker not found")
    if args.dry_run:
        print(ROW)
        return
    p.write_text(s.replace(marker, ROW + marker, 1))


if __name__ == "__main__":
    main()
