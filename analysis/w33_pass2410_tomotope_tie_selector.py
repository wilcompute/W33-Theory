#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,hashlib,importlib.util,itertools,json
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
COMMON=ROOT/'analysis/w33_pass1801_1805_common.py';PACK=ROOT/'data/w33_pass1837_middle_layer_compression.json';CERT=ROOT/'data/w33_pass2410_tomotope_tie_selector.json'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def common():
 s=importlib.util.spec_from_file_location('c',COMMON);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m
def full():
 D=common().build_geometry();G=D['graph'];pack=json.loads(PACK.read_text());res=pack['residual_vertices'];duad_index=pack['residual_to_duad_index'];duads=list(itertools.combinations(range(6),2));local=[duads[duad_index[str(r)]] for r in res];octs=[set(D['octets'][r][0])|set(D['octets'][r][1]) for r in res]
 evs=[]
 for t in itertools.combinations(range(40),3):
  if G.subgraph(t).number_of_edges():continue
  c=set(range(40))-set(t)
  for x in t:c&=set(G[x])
  if len(c)==1:evs.append(tuple(sorted((next(iter(c)),)+t)))
 evs=sorted(set(evs));assert len(evs)==2880
 prof=collections.defaultdict(list);labels={}
 for e in evs:
  z=[len(set(e)&o) for o in octs];m=max(z);ix=tuple(i for i,v in enumerate(z) if v==m)
  k='unique_max_3' if (m,len(ix))==(3,1) else 'two_way_tie_max_2' if (m,len(ix))==(2,2) else 'two_way_tie_max_3' if (m,len(ix))==(3,2) else None
  assert k;prof[k].append(e);labels[e]=ix
 mult={}
 for k in ('two_way_tie_max_2','two_way_tie_max_3'):
  C=collections.Counter(tuple(sorted(labels[e])) for e in prof[k]);assert len(C)==60 and set(C.values())=={12};assert all(len(set(local[a])&set(local[b]))==1 for a,b in C);mult[k]=dict(collections.Counter(C.values()))
 fixed=0;layers={k:{e for e in prof[k] if fixed in labels[e]} for k in prof};assert {k:len(v) for k,v in layers.items()}=={'unique_max_3':96,'two_way_tie_max_2':96,'two_way_tie_max_3':96}
 S=sorted(layers['two_way_tie_max_2']|layers['two_way_tie_max_3']);typ={e:('tie2' if e in layers['two_way_tie_max_2'] else 'tie3') for e in S};H=nx.Graph();H.add_nodes_from(S)
 for a,b in itertools.combinations(S,2):
  if len(set(a)&set(b))==3:H.add_edge(a,b)
 comps=list(nx.connected_components(H));assert sorted(map(len,comps))==[24]*8;assert all(collections.Counter(typ[x] for x in c)=={'tie2':12,'tie3':12} for c in comps);assert all(H.subgraph(c).number_of_edges()==42 for c in comps)
 return {'event_valencies':{k:len(labels[v[0]]) for k,v in prof.items()},'components':[len(c) for c in comps]}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true');a=ap.parse_args();d=json.loads(CERT.read_text());assert d['sha256_without_hash_field']==digest(d) and all(d['checks'].values())
 if a.full:
  z=full();assert z['event_valencies']=={'unique_max_3':1,'two_way_tie_max_2':2,'two_way_tie_max_3':2};assert z['components']==[24]*8
 print(json.dumps({'status':d['status'],'sha256':d['sha256_without_hash_field']},sort_keys=True))
if __name__=='__main__':main()
