#!/usr/bin/env python3
"""Insert Passes 4269-4276 into the shared frontier in numerical order."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex'
LINE=r'\input{analysis/BT4269_BT4276_h145_fusion_hodge_gds_strata_outside_box_insert}%'
text=P.read_text();lines=text.splitlines()
if LINE not in lines:
    inserted=False
    for i,s in enumerate(lines):
        m=re.search(r'BT(\d+)',s)
        if m and int(m.group(1))>4269:
            lines.insert(i,LINE);inserted=True;break
    if not inserted:lines.append(LINE)
    P.write_text('\n'.join(lines)+'\n')
