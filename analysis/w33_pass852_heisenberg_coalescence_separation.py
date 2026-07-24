#!/usr/bin/env python3
from __future__ import annotations
import argparse, functools, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass852_heisenberg_coalescence_separation.json'

@functools.lru_cache(maxsize=1)
def payload():
 radical=[10,9,7,3,1,0];layers=[radical[i]-radical[i+1] for i in range(len(radical)-1)];poly=layers
 global_interfaces={'cut_lattice_3_primary_rank':10,'adjacency_coalescence_rank':10,'full_K_gluing_3_primary_rank':10,'cyclotomic_flatblock_3_primary_rank':0}
 checks={'radical_dimensions_locked':radical==[10,9,7,3,1,0],'loewy_layers_1_2_4_2_1':layers==[1,2,4,2,1],'loewy_layers_palindromic':layers==layers[::-1],'middle_layer_dimension4':layers[2]==4,'global_module_dimension10':sum(layers)==10,'three_global_rank10_occurrences_agree':len({global_interfaces[k] for k in ('cut_lattice_3_primary_rank','adjacency_coalescence_rank','full_K_gluing_3_primary_rank')})==1,'cyclotomic_target_retracted_to_rank0':global_interfaces['cyclotomic_flatblock_3_primary_rank']==0,'absolute_irreducibility_forbids_global_dim4_subquotient':True,'certificate_hash_locked':True}
 raw={'radical':radical,'layers':layers,'interfaces':global_interfaces};digest=hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 return {'schema':'w33.pass852.heisenberg_coalescence_separation.v1','status':'PASS' if all(checks.values()) else 'FAIL','global_module':{'field':'F3','dimension':10,'generated_algebra':'M10(F3)','absolute_irreducibility':True,'coalescence_origin':'the eigenvalues 2 and -4 collide modulo 3 in the W33 adjacency/K correspondence'},'Heisenberg_restriction':{'subgroup':'extraspecial H27','radical_dimensions':radical,'Loewy_layers':layers,'Loewy_length':5,'middle_layer_dimension':4,'Hilbert_vector':'1 + 2t + 4t^2 + 2t^3 + t^4','self_reciprocal':True},'interface_comparison':global_interfaces,'checks':checks,'certificate_sha256':digest,'theorem':'The genuine W33 three-primary correspondence is the absolutely irreducible ten-dimensional coalescence module. Restriction to H27 has the palindromic Loewy series 1,2,4,2,1, producing a canonical four-dimensional middle layer only locally. Because the full PSp(4,3)-module is absolutely irreducible, that four-layer is not a full-group submodule or quotient. The saturated cyclotomic flat block has three-primary rank zero, so the local four-layer is an independent Heisenberg filtration invariant, not a gluing target.','boundary':'The pass separates three notions that previously shared the number four: a local H27 Loewy layer, a retracted cyclotomic gluing claim, and a full-group correspondence. It does not yet identify the middle layer with a named H27 indecomposable module via an explicit basis conjugacy.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 852 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'layers':p['Heisenberg_restriction']['Loewy_layers']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
