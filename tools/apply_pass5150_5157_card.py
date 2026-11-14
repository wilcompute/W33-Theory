#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/'docs/index.html'
CARD=(ROOT/'analysis/PASS5150_5157_index_insert.html').read_text()
MARK='id="pass5150-5157"'
text=PAGE.read_text()
if MARK in text:
    print('Pass5150-5157 card already present')
else:
    pos=text.lower().rfind('</body>')
    if pos<0: raise SystemExit('docs/index.html has no </body>')
    PAGE.write_text(text[:pos]+'\n'+CARD+'\n'+text[pos:])
    print('Inserted Pass5150-5157 card')
