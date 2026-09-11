#!/usr/bin/env python3
"""Pass 3065: proof-producing decision of the global 27-versus-28 D4 schedule question.

On the central element r^2, triangle syndromes are binary boundary parities. Distinguishing
all supports of weight at most two is equivalent to making every nonzero edge difference
of weight at most four visible. UNSAT for the exact CNF below proves no full-D4 27-row
schedule exists. SAT yields only a central candidate until all 48,826 D4 hypotheses pass.
"""
from __future__ import annotations
import argparse,itertools,json,math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';DATA.mkdir(exist_ok=True)
D4=[(a,b) for a in range(4) for b in range(2)];I=(0,0);FAULTS=[g for g in D4 if g!=I]
EDGES=list(itertools.combinations(range(10),2));TRIS=list(itertools.combinations(range(10),3))
VERIFIED28=[(0,1,3),(0,2,9),(0,3,7),(0,4,5),(0,4,7),(0,4,8),(0,5,6),(0,6,9),(1,2,3),(1,2,6),(1,4,6),(1,4,8),(1,5,8),(1,5,9),(1,7,9),(2,3,4),(2,3,8),(2,4,7),(2,5,9),(2,6,7),(2,8,9),(3,5,9),(3,6,8),(3,6,9),(3,7,9),(4,8,9),(5,6,7),(5,7,8)]

def mul(g,h):
 a,b=g;c,d=h;return((a+(-1 if b else 1)*c)%4,(b+d)%2)
def inv(g):
 a,b=g;return((-((-1 if b else 1)*a))%4,b)
def directed(edge,g,u,v):
 if (u,v)==edge:return g
 if (v,u)==edge:return inv(g)
 return I
def syndrome(hyp,selected):
 out=[]
 for ti in selected:
  i,j,k=TRIS[ti];p=I
  for u,v in ((i,j),(j,k),(k,i)):
   q=I
   for e,g in hyp:q=mul(directed(e,g,u,v),q)
   p=mul(q,p)
  out.append(p)
 return tuple(out)
def hypotheses():
 H=[tuple()];H.extend(((e,g),) for e in EDGES for g in FAULTS);H.extend(((e,g),(f,h)) for e,f in itertools.combinations(EDGES,2) for g in FAULTS for h in FAULTS);assert len(H)==48826;return H
def verify(selected):return len({syndrome(h,selected) for h in hypotheses()})==48826

def odd_clause(diff):
 D=set(diff);row=[]
 for i,t in enumerate(TRIS):
  bd={tuple(sorted((t[0],t[1]))),tuple(sorted((t[0],t[2]))),tuple(sorted((t[1],t[2])))}
  if len(D&bd)%2:row.append(i+1)
 assert row;return row
def separation_clauses():
 C=[odd_clause(d) for w in range(1,5) for d in itertools.combinations(EDGES,w)];assert len(C)==164220;return C

def write_cnf(path):
 from pysat.card import CardEnc,EncType
 C=separation_clauses();C.append([TRIS.index((0,1,2))+1])
 card=CardEnc.atmost(lits=list(range(1,121)),bound=27,top_id=120,encoding=EncType.seqcounter);C.extend(card.clauses);nv=max(card.nv,max(abs(x) for c in C for x in c))
 with path.open('w') as f:
  f.write(f'p cnf {nv} {len(C)}\n')
  for c in C:f.write(' '.join(map(str,c))+' 0\n')
 return C,nv

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cnf',type=Path,default=DATA/'bt3065_no27.cnf');ap.add_argument('--solve',action='store_true');ap.add_argument('--proof',type=Path,default=DATA/'bt3065_no27.drup');a=ap.parse_args()
 a.cnf.parent.mkdir(exist_ok=True);C,nv=write_cnf(a.cnf);upper=[TRIS.index(t) for t in VERIFIED28];assert verify(upper)
 out={'schema':'w33.pass3065.d4_fixed_optimum.v1','status':'SOURCE_COMPLETE_27_DECISION_PENDING','central_difference_constraints':164220,'cnf_variables':nv,'cnf_clauses':len(C),'symmetry_breaker':'(0,1,2) selected by S10 transitivity','verified_28_schedule':[list(t) for t in VERIFIED28],'verified_28_full_d4_unique':True,'current_exact_bounds':[23,28],'claim_boundary':'UNSAT plus independent proof checking proves optimum 28; SAT is only a central candidate until full D4 verification.'}
 if a.solve:
  from pysat.solvers import Solver
  with Solver(name='glucose4',bootstrap_with=C,with_proof=True) as s:
   sat=s.solve()
   if sat:
    model=set(s.get_model());sel=[i for i in range(120) if i+1 in model];full=len(sel)<=27 and verify(sel);out.update(status='SAT_FULL_D4_27_FOUND' if full else 'SAT_CENTRAL_ONLY_FULL_D4_REJECTED',sat_selected_count=len(sel),sat_schedule=[list(TRIS[i]) for i in sel],sat_full_d4_unique=full)
   else:
    proof=s.get_proof();a.proof.write_text('\n'.join(proof)+'\n');out.update(status='UNSAT_REPORTED_PROOF_REQUIRES_INDEPENDENT_CHECK',proof_path=str(a.proof.relative_to(ROOT)),proof_lines=len(proof))
 (DATA/'PART_BT3065_D4_FIXED_OPTIMUM_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:out[k] for k in ('status','central_difference_constraints','cnf_variables','cnf_clauses')},sort_keys=True))
if __name__=='__main__':main()
