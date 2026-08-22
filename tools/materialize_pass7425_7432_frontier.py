#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'analysis'/'PASS7425_7432_index_insert.html'
TOKEN='pass-7425-7432-global-leaf-d4-grid'
TARGETS=[ROOT/'docs'/'index.html',ROOT/'index.html']

def materialize(path:Path):
    src=SOURCE.read_text().strip()
    text=path.read_text()
    pat=re.compile(r'\n?<section id="'+re.escape(TOKEN)+r'".*?</section>\n?',re.S)
    text=pat.sub('\n',text)
    if '</body>' in text:text=text.replace('</body>','\n'+src+'\n</body>',1)
    else:text=text.rstrip()+'\n\n'+src+'\n'
    assert text.count('id="'+TOKEN+'"')==1
    path.write_text(text)

def main():
    for p in TARGETS:materialize(p)
    print('PASS',TOKEN)
if __name__=='__main__':main()
