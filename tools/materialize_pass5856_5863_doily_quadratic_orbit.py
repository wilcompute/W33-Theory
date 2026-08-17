#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parents[1]; T='pass-5856-5863-doily-quadratic-orbit'; S=R/'analysis/PASS5856_5863_index_insert.html'
def main():
 h=S.read_text(); m=f'id="{T}"'
 for p in (R/'docs/index.html',R/'index.html'):
  x=p.read_text(); n=x.count(m)
  if n>1: raise ValueError(m)
  if n==0:
   q=x.lower().rfind('</main>'); q=q if q>=0 else x.lower().rfind('</body>')
   if q<0: raise ValueError('no insertion point')
   x=x[:q]+h.rstrip()+'\n'+x[q:]; p.write_text(x)
  assert p.read_text().count(m)==1
if __name__=='__main__':main()
