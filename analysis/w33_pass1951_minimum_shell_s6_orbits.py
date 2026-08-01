#!/usr/bin/env python3
from __future__ import annotations
import collections,hashlib,importlib.util,itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];ROWS=ROOT/'data/w33_pass1876_rows45_hex.txt';COLS=ROOT/'data/w33_pass1848_syndrome_columns.txt';COMP=ROOT/'data/w33_pass1837_middle_layer_compression.json';COMMON=ROOT/'analysis/w33_pass1801_1805_common.py';OUT=ROOT/'data/w33_pass1951_minimum_shell_s6_orbits.json'
def canon(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load_common():
 s=importlib.util.spec_from_file_location('c',COMMON);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m
def main():
 rows=[]
 for line in ROWS.read_text().splitlines():
  limbs=[int(x,16) for x in line.split()];rows.append(sum(x<<(64*i) for i,x in enumerate(limbs)))
 cols=list(map(int,COLS.read_text().split()));prof=[]
 for e in range(240):prof.append((sum(rows[i]>>e&1 for i in range(30)),sum(rows[i]>>e&1 for i in range(30,45))))
 buck=collections.defaultdict(list)
 for i,j in itertools.combinations(range(240),2):buck[cols[i]^cols[j]].append((i,j))
 words=set()
 for ps in buck.values():
  for x,y in itertools.combinations(ps,2):
   q=x+y
   if len(set(q))==4:words.add(tuple(sorted(q)))
 D=load_common().build_geometry();pack=json.loads(COMP.read_text());F=[tuple(x) for x in pack['canonical_six_line_pack']];Fset={frozenset(x) for x in F}
 def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))
 idp=tuple(range(40));seen={idp:(tuple(range(240)),tuple(range(45)))};q=collections.deque([idp])
 while q:
  pp=q.popleft();ep,op=seen[pp]
  for gp,ge,gl,gf,go,gos in D['acts']+[D['outer']]:
   np=compose(gp,pp)
   if np not in seen:seen[np]=(tuple(ge[ep[i]] for i in range(240)),tuple(go[op[i]] for i in range(45)));q.append(np)
 stab=[ep for pp,(ep,op) in seen.items() if {frozenset(op[i] for i in x) for x in F}==Fset]
 unseen=set(words);orbs=[]
 while unseen:
  w=min(unseen);o={tuple(sorted(ep[i] for i in w)) for ep in stab};unseen-=o;orbs.append(o)
 pn={(0,3):'residual',(2,1):'pair',(3,0):'phase'};summary=[]
 for o in orbs:
  rep=min(o);typ=tuple(sorted(collections.Counter(pn[prof[e]] for e in rep).items()));fix=sum(tuple(sorted(ep[i] for i in rep))==rep for ep in stab);deg=collections.Counter(e for w in o for e in w)
  z={'type':[[a,b] for a,b in typ],'orbit_size':len(o),'stabilizer_order':fix,'support_union':len(deg),'coordinate_degree_distribution':dict(sorted(collections.Counter(deg.values()).items())),'representative':list(rep)}
  if len(o)==15:z['geometric_name']='residual tetrahedral boundaries'
  elif len(o)==45:z['geometric_name']='pair-coordinate parallel tetrads'
  elif len(o)==120:z['geometric_name']='mixed residual-triangle flags'
  elif typ==(('pair',4),):z['geometric_name']='pair rectangles'
  else:z['geometric_name']='pair-phase bridges'
  summary.append(z)
 summary.sort(key=lambda z:(z['type'],z['orbit_size']))
 checks={'weight4_540':len(words)==540,'frames_equal_shell':words==set(map(tuple,D['matchings'])),'s6_order720':len(stab)==720,'five_orbits':len(summary)==5,'orbit_sizes':sorted(z['orbit_size'] for z in summary)==[15,45,120,180,180],'stabilizers':sorted(z['stabilizer_order'] for z in summary)==[4,4,6,16,48]}
 out={'schema':'w33.pass1951.minimum_shell_s6_orbits.v1','status':'PASS','checks':checks,'orbits':summary,'theorem':'The 540 minimum words are exactly the 540 frame matchings. Under exceptional S6 they split into five orbits of sizes 15,45,120,180,180; the nominal 225 pair-only split type is two geometrically distinct orbits of sizes 45 and 180.','designs':{'size15':'The 15 residual-only words are boundaries of tetrahedra on four-subsets of six; each residual triad occurs three times.','size45':'The 45 pair-only tetrads partition all 180 pair coordinates exactly once.','size120':'Each residual coordinate occurs six times and each pair coordinate twice.','pair180':'Each pair coordinate occurs four times.','pair_phase180':'Each pair coordinate occurs twice and each phase coordinate nine times.'},'boundary':'These are exact S6 orbit and incidence structures; no physical interpretation is attached.'}
 assert all(checks.values());out['sha256_without_hash_field']=canon(out);OUT.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'sha':out['sha256_without_hash_field'],'orbits':summary},indent=2));return out
if __name__=='__main__':main()
