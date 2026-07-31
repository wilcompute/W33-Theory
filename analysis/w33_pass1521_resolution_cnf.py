#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, importlib.util, json
from pathlib import Path

def build_geometry():
    try:
        from w33_frame_hoffman_resolution_theorem import build_geometry
        return build_geometry()
    except ImportError:
        spec=importlib.util.spec_from_file_location('w','/mnt/data/w33_execute5.py')
        w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w)
        pts,A,lines,edges,frames,matchings,M,H=w.build()
        return {'points':pts,'point_adjacency':A,'lines':lines,'edges':edges,'frames':frames,'matchings':matchings,'incidence':M,'frame_graph':H}

def var(f,c): return 9*f+c+1

def generate(path:Path):
    g=build_geometry(); M=g['incidence']; clauses=[]
    for f in range(540):
        clauses.append([var(f,c) for c in range(9)])
        for a in range(9):
            for b in range(a+1,9): clauses.append([-var(f,a),-var(f,b)])
    edge_frames=[]
    for e in range(240):
        fs=[f for f in range(540) if int(M[f,e])==1]
        assert len(fs)==9;edge_frames.append(fs)
        for c in range(9):
            clauses.append([var(f,c) for f in fs])
            for i in range(9):
                for j in range(i+1,9): clauses.append([-var(fs[i],c),-var(fs[j],c)])
    for c,f in enumerate(edge_frames[0]): clauses.append([var(f,c)])
    assert len(clauses)==99909
    text='p cnf 4860 99909\n'+''.join(' '.join(map(str,cl))+' 0\n' for cl in clauses)
    path.write_text(text,encoding='ascii')
    return {'schema':'w33.pass1521.resolution_cnf.v1','status':'PASS','variables':4860,'clauses':99909,'bytes':len(text.encode()),'sha256':hashlib.sha256(text.encode()).hexdigest(),'symmetry_break_edge':0,'symmetry_break_frames':edge_frames[0]}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--json',type=Path);ap.add_argument('--check',action='store_true');a=ap.parse_args()
    result=generate(a.output)
    if a.json:a.json.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
