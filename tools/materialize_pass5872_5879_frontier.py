#!/usr/bin/env python3
"""Idempotently materialize the two latest matrix/doily frontier cards.

The publication contract names docs/index.html as canonical, but root index.html is also
maintained. Each target is handled independently; duplicate IDs fail closed.
"""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TARGETS=(ROOT/"docs"/"index.html", ROOT/"index.html")
CARDS=(
    ("pass-5856-5863-doily-quadratic-orbit", ROOT/"analysis"/"PASS5856_5863_index_insert.html"),
    ("pass-5872-5879-coherent-css-rankmetric-clifford-discriminant", ROOT/"analysis"/"PASS5872_5879_index_insert.html"),
)

def place(path:Path, token:str, card:str)->str:
    marker=f'id="{token}"'
    text=path.read_text(encoding="utf-8")
    n=text.count(marker)
    if n>1: raise ValueError(f"duplicate {marker} in {path}")
    if n==1: return "already_materialized"
    low=text.lower(); pos=low.rfind("</main>")
    if pos<0: pos=low.rfind("</body>")
    if pos<0: raise ValueError(f"no </main> or </body> in {path}")
    out=text[:pos]+card.rstrip()+"\n"+text[pos:]
    assert out.count(marker)==1
    path.write_text(out,encoding="utf-8")
    return "inserted"

def main():
    for token,src in CARDS:
        card=src.read_text(encoding="utf-8")
        assert card.count(f'id="{token}"')==1
        for target in TARGETS:
            print(target.relative_to(ROOT), token, place(target,token,card))
    for token,_ in CARDS:
        for target in TARGETS:
            assert target.read_text(encoding="utf-8").count(f'id="{token}"')==1

if __name__=="__main__": main()
