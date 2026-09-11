#!/usr/bin/env python3
"""Run or inspect the readable Passes 2953--2959 verifier programs."""
from __future__ import annotations
import argparse,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FRONTS={
  '2953_2958':ROOT/'analysis/bt2953_2958_conjugacy_and_hard_shell_fourier.py',
  '2954_2959':ROOT/'analysis/bt2954_2959_chirality_probe_and_mirror.py',
  '2955':ROOT/'analysis/bt2955_bayes_optimal_noisy_observer.py',
  '2956':ROOT/'analysis/bt2956_threecopy_css_closure.py',
}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--front',action='append',choices=tuple(FRONTS));args=parser.parse_args()
    selected=set(args.front or FRONTS)
    for name,path in FRONTS.items():
        if name not in selected:continue
        if not path.is_file():raise FileNotFoundError(path)
        print(f'=== {name}: {path.relative_to(ROOT)} ===',flush=True)
        runpy.run_path(str(path),run_name='__main__')
if __name__=='__main__':main()
