"""Round33 exact Moore lower bounds for covers of W33 Levi geometry.

For 4-regular bipartite graph of girth >=2r, breadth-first
trees rooted on an edge contain >=2*(1+3+...+3^(r-1))
=3^r-1 distinct vertices. Degree-m W33 Levi cover has 80m.
"""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261010_toe33_girth_moore_bound.json'
def run():
 tests=[]
 for target in (8,10,12,14,16):
  r=target//2
  N=3**r-1
  minimum=(N+79)//80
  assert 80*(minimum-1)<N<=80*minimum
  tests.append(dict(target_girth_at_least=target,minimum_vertices=N,
                    minimum_W33_cover_degree=minimum,
                    minimum_HGP_n_at_that_degree=(160*minimum)**2+(80*minimum-1)**2))
 assert [(x['target_girth_at_least'],x['minimum_W33_cover_degree']) for x in tests]==[(8,1),(10,4),(12,10),(14,28),(16,82)]
 out=dict(status='PASS',
  theorem='Any finite graph that is 4-regular, bipartite and girth>=2r contains at least 3^r-1 vertices by breadth-first exploration of disjoint depth(r-1) neighborhoods around the two endpoints of an edge. A degree-m W33 Levi cover has 80m vertices, so m>=ceil((3^r-1)/80).',
  target_bounds=tests,
  role='These bounds are rigorous for ANY 4-regular bipartite W33 covering graph, including nonabelian and nonnormal covers. In particular m<=3 impossible for girth10 and m<=9 impossible for girth12, independent of CP-SAT. They do NOT prove m=13 impossible for girth10 or m=17 minimal.',
  prior='Base W33 Levi girth8, 80 vertices. Round30 degree83 and Round31 degree17 both have exact girth10.')
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 print('MOORE W33 covers',[(x['target_girth_at_least'],x['minimum_W33_cover_degree']) for x in tests],flush=True)
 return out
if __name__=='__main__':run()
