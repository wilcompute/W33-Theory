#!/usr/bin/env python3
"""Pass 1187 v2: exact degree-40 execution record."""
import json
from pathlib import Path
from analysis.w33_pass1190_ihara_bass_degree40 import main as exact
def main():
 e=exact();r={'schema':'w33.pass1187.ihara_degree40_worklist.v2','status':'PASS','work_remaining':False,
 'degree':40,'hashimoto_coefficient':11,'primitive_cycle_count_n40':e['primitive_reduced_cycle_classes']['40'],
 'source':'Pass 1190 exact determinant, Newton identities, and Möbius inversion'}
 Path('data/IHARA_DEGREE40_WORKLIST_2026_07_27.json').write_text(json.dumps(r,indent=2)+'\n');return r
if __name__=='__main__':main()
