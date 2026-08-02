#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, hashlib, importlib.util, json, time
from pathlib import Path
import numpy as np
from ortools.sat.python import cp_model
ROOT=Path(__file__).resolve().parents[1]
COMMON=ROOT/'analysis/w33_pass1801_1805_common.py'
FIBER_MOD=ROOT/'analysis/w33_pass2416_nine_signature_cover_fibers.py'
FIBER_CERT=ROOT/'data/w33_pass2416_nine_signature_cover_fibers.json'

def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m

def compose(p,q): return tuple(p[q[i]] for i in range(len(q)))

def build_cross_key(D):
 identp=tuple(range(40));seen={identp:(tuple(range(45)),tuple(range(540)))};q=collections.deque([identp])
 while q:
  pp=q.popleft();op,fp=seen[pp]
  for gp,ge,gl,gf,go,gos in D['acts']:
   np_=compose(gp,pp)
   if np_ not in seen:
    seen[np_]=(tuple(go[op[i]] for i in range(45)),tuple(gf[fp[i]] for i in range(540)));q.append(np_)
 assert len(seen)==25920
 acts=list(seen.values());unseen={(f,o) for f in range(540) for o in range(45)};orbits=[]
 while unseen:
  f,o=min(unseen);orb={(fp[f],op[o]) for op,fp in acts};unseen-=orb;orbits.append(orb)
 rows=[]
 for orb in orbits:
  fd=collections.Counter(f for f,o in orb);od=collections.Counter(o for f,o in orb);rows.append((len(orb),set(fd.values()),set(od.values()),orb))
 cand=[z for z in rows if z[1]=={1} and z[2]=={12}];assert len(cand)==1
 key=[None]*540
 R=np.zeros((540,45),dtype=np.uint8)
 for f,o in cand[0][3]:assert key[f] is None;key[f]=o;R[f,o]=1
 assert all(x is not None for x in key) and collections.Counter(key)==collections.Counter({o:12 for o in range(45)})
 return key,R,[(z[0],sorted(z[1]),sorted(z[2])) for z in rows]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--time-limit',type=float,default=3600);ap.add_argument('--workers',type=int,default=8);ap.add_argument('--write-json',type=Path);a=ap.parse_args()
 common=load(COMMON,'w33_common');fib=load(FIBER_MOD,'w33_fibers');D=common.build_geometry();key,R,cross=build_cross_key(D)
 frozen=json.loads(FIBER_CERT.read_text());assert hashlib.sha256(R.tobytes()).hexdigest()==frozen['relation']['sha256']
 targets=[fib.decode_signature(s) for s in fib.SIGNATURE_STRINGS];assert len(targets)==9
 assert all(sum(v)==60 for v in targets) and [sum(targets[s][o] for s in range(9)) for o in range(45)]==[12]*45
 frames=[tuple(x) for x in D['matchings']];assert len(frames)==540
 edge_frames=[[] for _ in range(240)]
 for f,es in enumerate(frames):
  assert len(es)==4
  for e in es:edge_frames[e].append(f)
 assert all(len(z)==9 for z in edge_frames)
 model=cp_model.CpModel();x=[[model.NewBoolVar(f'x_{f}_{c}') for c in range(9)] for f in range(540)];y=[[model.NewBoolVar(f'y_{c}_{s}') for s in range(9)] for c in range(9)]
 for f in range(540):model.AddExactlyOne(x[f])
 for e in range(240):
  for c in range(9):model.Add(sum(x[f][c] for f in edge_frames[e])==1)
 for c in range(9):model.AddExactlyOne(y[c])
 for s in range(9):model.AddExactlyOne(y[c][s] for c in range(9))
 by_oct=[[f for f in range(540) if key[f]==o] for o in range(45)]
 for c in range(9):
  for o in range(45):model.Add(sum(x[f][c] for f in by_oct[o])==sum(targets[s][o]*y[c][s] for s in range(9)))
 for c,f in enumerate(sorted(edge_frames[0])):model.Add(x[f][c]==1)
 model.AddDecisionStrategy([y[c][s] for c in range(9) for s in range(9)],cp_model.CHOOSE_FIRST,cp_model.SELECT_MAX_VALUE)
 solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=a.time_limit;solver.parameters.num_search_workers=a.workers;solver.parameters.log_search_progress=True;solver.parameters.cp_model_presolve=True
 t=time.time();status=solver.Solve(model);elapsed=time.time()-t;name=solver.StatusName(status)
 out={'schema':'w33.pass2432.signature_lift_cpsat.v2','status':name,'runtime_seconds':elapsed,'time_limit_seconds':a.time_limit,'workers':a.workers,
      'relation_sha256':hashlib.sha256(R.tobytes()).hexdigest(),'cross_orbitals':cross,'selected_signature_strings':fib.SIGNATURE_STRINGS,
      'selected_fiber_total_cardinality':frozen['selected_fiber_total_cardinality'],'variables':540*9+81,'frame_constraints':540,'edge_color_constraints':240*9,'signature_constraints':45*9,
      'branches':solver.NumBranches(),'conflicts':solver.NumConflicts(),'wall_time':solver.WallTime()}
 if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  assign=[next(c for c in range(9) if solver.Value(x[f][c])) for f in range(540)];sigassign=[next(s for s in range(9) if solver.Value(y[c][s])) for c in range(9)];classes=[[f for f in range(540) if assign[f]==c] for c in range(9)]
  assert all(len(z)==60 for z in classes) and sorted(sum(classes,[]))==list(range(540));assert all(len({assign[f] for f in edge_frames[e]})==9 for e in range(240))
  for c in range(9):assert [sum(1 for f in classes[c] if key[f]==o) for o in range(45)]==targets[sigassign[c]]
  out['solution']={'frame_colors':assign,'signature_assignment':sigassign,'color_classes':classes}
 if a.write_json:a.write_json.write_text(json.dumps(out,indent=2,sort_keys=True))
 print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
