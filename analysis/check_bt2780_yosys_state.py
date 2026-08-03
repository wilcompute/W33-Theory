#!/usr/bin/env python3
"""Fail when a stateful controller synthesizes to constants or a trivial shell."""
from __future__ import annotations
import argparse,json
from pathlib import Path
def main():
 ap=argparse.ArgumentParser();ap.add_argument('json_path',type=Path);ap.add_argument('top');ap.add_argument('--min-dff',type=int,required=True);ap.add_argument('--min-cells',type=int,required=True);args=ap.parse_args();data=json.loads(args.json_path.read_text());cells=list(data['modules'][args.top].get('cells',{}).values());dff=sum(1 for c in cells if c.get('type','').startswith('SB_DFF'));total=len(cells);print(f'{args.top}: cells={total} dff={dff}')
 if dff<args.min_dff or total<args.min_cells:raise SystemExit(f'synthesis-fold guard failed: expected >= {args.min_dff} DFF and >= {args.min_cells} cells')
if __name__=='__main__':main()
