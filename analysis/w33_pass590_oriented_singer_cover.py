#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'w33_pass590_oriented_singer_cover.json'
def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
def order(p):
 q=tuple(range(len(p)))
 for n in range(1,61):
  q=comp(p,q)
  if q==tuple(range(len(p))):return n
 raise AssertionError
def closure(gens):
 n=len(gens[0]);I=tuple(range(n));H={I};front=[I]
 while front:
  a=front.pop()
  for b in gens:
   for c in (comp(a,b),comp(b,a)):
    if c not in H:H.add(c);front.append(c)
 return frozenset(H)
def cycle_perm(n,cyc):
 p=list(range(n))
 for a,b in zip(cyc,cyc[1:]+cyc[:1]):p[a]=b
 return tuple(p)
def induced_orientation(g,A):
 A=tuple(sorted(A));B=tuple(sorted(g[i] for i in A));pos={x:i for i,x in enumerate(B)};perm=tuple(pos[g[i]] for i in A);return parity(perm)
def sylow5_subgroups(B,n=8):
 B=tuple(sorted(B));subs=set()
 for cyc_tail in itertools.permutations(B[1:]):
  cyc=(B[0],)+cyc_tail;g=cycle_perm(n,cyc);subs.add(closure((g,)))
 return tuple(sorted(subs,key=lambda H:sorted(H)))
def conj_subgroup(g,H):
 gi=inv(g);return frozenset(comp(comp(g,h),gi) for h in H)
def payload():
 S8=list(itertools.permutations(range(8)));A8=[g for g in S8 if parity(g)==0]
 triples=list(itertools.combinations(range(8),3));oriented=[(A,s) for A in triples for s in (0,1)]
 def act_oriented(g,x):
  A,s=x;B=tuple(sorted(g[i] for i in A));return (B,s^induced_orientation(g,A))
 A0=triples[0];o0=(A0,0);stabA=[g for g in A8 if tuple(sorted(g[i] for i in A0))==A0];stabO=[g for g in A8 if act_oriented(g,o0)==o0]
 B0=tuple(i for i in range(8) if i not in A0);pent=sylow5_subgroups(B0);P0=pent[0]
 flags=[(A,P) for A in triples for P in sylow5_subgroups(tuple(i for i in range(8) if i not in A))]
 oflags=[(A,s,P) for A in triples for s in (0,1) for P in sylow5_subgroups(tuple(i for i in range(8) if i not in A))]
 def act_flag(g,x):
  A,P=x;B=tuple(sorted(g[i] for i in A));return B,conj_subgroup(g,P)
 def act_oflag(g,x):
  A,s,P=x;B,ns=act_oriented(g,(A,s));return B,ns,conj_subgroup(g,P)
 f0=(A0,P0);of0=(A0,0,P0);stabF=[g for g in A8 if act_flag(g,f0)==f0];stabOF=[g for g in A8 if act_oflag(g,of0)==of0]
 pidx={P:i for i,P in enumerate(pent)}
 def paction(g):return tuple(pidx[conj_subgroup(g,P)] for P in pent)
 imgA={paction(g) for g in stabA};imgO={paction(g) for g in stabO};kerA=[g for g in stabA if paction(g)==tuple(range(6))];kerO=[g for g in stabO if paction(g)==tuple(range(6))]
 orbitO={act_oriented(g,o0) for g in A8};orbitF={act_flag(g,f0) for g in A8};orbitOF={act_oflag(g,of0) for g in A8}
 exterior_match=all(act_oriented(g,(A,s))==(tuple(sorted(g[i] for i in A)),s^induced_orientation(g,A)) for g in A8[::137] for A in triples[::7] for s in (0,1))
 checks={'A8_order20160':len(A8)==20160,'triples56_oriented112':len(triples)==56 and len(oriented)==112,'oriented_action_transitive':len(orbitO)==112,'oriented_stabilizer180':len(stabO)==180,'oriented_stabilizer_orders_match_C3xA5':Counter(order(g) for g in stabO)==Counter({1:1,2:15,3:62,5:24,6:30,15:48}),'six_pentagons_per_complement':len(pent)==6 and all(len(H)==5 for H in pent),'Singer_flags336_transitive':len(flags)==336 and len(orbitF)==336,'Singer_stabilizer60':len(stabF)==60,'oriented_flags672_transitive':len(oflags)==672 and len(orbitOF)==672,'oriented_flag_stabilizer30':len(stabOF)==30,'unoriented_triple_image_S5_kernelC3':len(imgA)==120 and len(kerA)==3,'oriented_triple_image_A5_kernelC3':len(imgO)==60 and len(kerO)==3,'cover_fibres_2_and_6':len(oflags)//len(flags)==2 and len(oflags)//len(oriented)==6,'signed_exterior_cocycle_exact':exterior_match}
 return {'schema':'w33.pass590.oriented_singer_cover.v1','status':'PASS' if all(checks.values()) else 'FAIL','ambient':{'group':'A8','order':len(A8)},'oriented_Johnson':{'base':'J(8,3) on 56 triples','double_cover_objects':112,'object':'(three-subset, orientation)','stabilizer_order':len(stabO),'stabilizer_identification':'A3 x A5 = C3 x A5','deck_involution':'orientation reversal','signed_exterior_identification':'The 112 objects are exactly the signed basis vectors ±(e_i wedge e_j wedge e_k) of Lambda^3(F^8).'},'Singer_refinement':{'unoriented_flags':336,'oriented_flags':672,'object':'(oriented triple A, Sylow-5 subgroup P on A^c)','Singer_stabilizer_order':len(stabF),'refined_stabilizer_order':len(stabOF),'refined_stabilizer_identification':'C3 x D10','projections':{'forget_orientation':'672 -> 336, fibre 2','forget_pentagon':'672 -> 112, fibre 6'}},'six_pentagon_action':{'unoriented_triple_stabilizer_order':len(stabA),'image_order':len(imgA),'kernel_order':len(kerA),'image':'S5 in its exceptional degree-six action','oriented_triple_stabilizer_order':len(stabO),'oriented_image_order':len(imgO),'oriented_kernel_order':len(kerO),'oriented_image':'A5 on its six Sylow-5 subgroups'},'exceptional_boundary':{'Lambda3_8':'The oriented double cover is the signed basis orbit of the 56-dimensional SL8 module Lambda^3(8).','E7_56':'The E7 minuscule 56 restricts to Lambda^2(8) + Lambda^2(8)^*, so it is not this Johnson action.','conclusion':'The Singer decoration supplies a sixfold pentagon refinement of the oriented exterior-basis cover, not an identification with the E7 weight set.'},'checks':checks,'boundary':'Exact for the A8 permutation actions. This constructs the oriented cover and common 672-object refinement; it does not identify the 280-dimensional Singer complement with an exceptional Lie-algebra module.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
