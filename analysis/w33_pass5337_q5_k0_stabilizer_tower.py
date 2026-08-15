#!/usr/bin/env python3
"""Pass5337: exact homogeneous-bundle stabilizer tower for the q=5 K0 shell.

Let G=PSp4(5). A minimum-shell label is (p,{l1,l2}), a W point plus an unordered
pair of its six incident W-lines. The point stabilizer P has order 30000 and its
six-line action has image A5 of order60, hence kernel order500. A pair stabilizer
in A5 is V4 of order4, so its preimage H has order2000. Therefore

  H < P < G,  [P:H]=15, [G:P]=156, [G:H]=2340,

and the shell is the homogeneous bundle G/H -> G/P with fiber P/H=A5/V4.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5337_Q5_K0_STABILIZER_TOWER.json'

def main():
    G0=build_W(5);pts=G0['pts'];pi={p:i for i,p in enumerate(pts)}
    def norm(v):
        for x in v:
            if x:
                s=pow(x,-1,5);return tuple(s*y%5 for y in v)
        raise ValueError
    def sp(u,v):return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%5
    def pperm(v):
        out=[]
        for x in pts:
            a=sp(x,v);out.append(pi[norm(tuple((x[k]+a*v[k])%5 for k in range(4)))])
        return Permutation(out)
    gens=[pperm(v) for v in ((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,0,1))]
    G=PermutationGroup(gens);assert G.order()==4680000
    P=G.stabilizer(0);assert P.order()==30000
    lines0=[li for li,L in enumerate(G0['lines']) if 0 in L];assert len(lines0)==6
    lk={tuple(sorted(L)):i for i,L in enumerate(G0['lines'])};li={x:i for i,x in enumerate(lines0)}
    # Strong generators fixing point0, restricted to its six incident lines.
    base,strong=G.schreier_sims_incremental(base=[0]);stabgens=[g for g in strong if g(0)==0]
    six=[]
    for g in stabgens:
        six.append(Permutation([li[lk[tuple(sorted(g(p) for p in G0['lines'][L]))]] for L in lines0]))
    A5=PermutationGroup(six);assert A5.order()==60
    kernel_order=P.order()//A5.order();assert kernel_order==500
    pairs=list(itertools.combinations(range(6),2));pidx={p:i for i,p in enumerate(pairs)}
    A15=PermutationGroup([Permutation([pidx[tuple(sorted((g(a),g(b))))] for a,b in pairs]) for g in A5.generators])
    assert A15.order()==60 and len(A15.orbit(0))==15
    V4=A15.stabilizer(0);assert V4.order()==4
    H_order=kernel_order*V4.order();assert H_order==2000
    assert P.order()//H_order==15 and G.order()//P.order()==156 and G.order()//H_order==2340
    out={'pass':5337,'status':'THEOREM_Q5_K0_SHELL_IS_HOMOGENEOUS_A5_OVER_V4_FIBER_BUNDLE',
      'G':'PSp4(5)','G_order':4680000,
      'point_stabilizer_order':30000,'point_orbit_size':156,
      'six_line_image':'A5','six_line_image_order':60,'six_line_kernel_order':500,
      'pair_stabilizer_image':'V4','pair_stabilizer_image_order':4,
      'shell_label_stabilizer_order':2000,'fiber_index':15,'shell_orbit_size':2340,
      'tower':'H_shell(2000) < P_point(30000) < PSp4(5)(4680000)',
      'bundle':'G/H -> G/P with fiber P/H ~= A5/V4 of size15',
      'induction_identity':'C[G/H] = Ind_P^G(C[A5/V4]) and C[A5/V4]=1+4+2*5.',
      'boundary':'Exact finite homogeneous-space theorem. It does not assign physical bundle/monodromy meaning.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
