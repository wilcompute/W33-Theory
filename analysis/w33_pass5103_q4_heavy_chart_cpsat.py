#!/usr/bin/env python3
"""Pass5103: exact q=4 heavy-chart minimum-shell solver.

The q=4 apartment code is represented as the dual of the apartment-boundary
map.  Gauge-fix a Levi 1-cochain on a spanning tree; the remaining 256 chord
bits are coordinates on H^1 of the 170-vertex, 425-edge Levi graph.  For every
one of the 13,600 apartments, its code bit is the XOR of the selected chord
bits on its 8-cycle boundary.

A fixed opposite-pair chart is a K5 on five geodesic roots.  A heavy local cut
has type 2|3 and therefore weight 6 on the chart's ten apartment coordinates.
The chart stabilizer is transitive on 2|3 cuts, so fixing {0,1}|{2,3,4} loses
no generality within a chart type.  q=4 is self-dual, but we solve one point
chart and one line chart independently as a firewall.

OR-Tools CP-SAT supplies native XOR constraints, avoiding the large parity-
slack MILP used in earlier exploratory runs.  OPTIMAL is required before this
script promotes a heavy-sector minimum.
"""
from __future__ import annotations
import itertools, json, time
from pathlib import Path
from ortools.sat.python import cp_model

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'PART_W33_PASS5103_Q4_HEAVY_CHART_CPSAT.json'

class GF4:
    q=4
    @staticmethod
    def add(a,b): return a^b
    @staticmethod
    def mul(a,b):
        a0,a1=a&1,(a>>1)&1; b0,b1=b&1,(b>>1)&1
        c0=a0*b0; c1=(a0*b1)^(a1*b0); c2=a1*b1
        return (c0^c2)|((c1^c2)<<1)
    def inv(self,a):
        return next(b for b in range(1,4) if self.mul(a,b)==1)

def build_W4():
    q=4; F=GF4(); add,mul,inv=F.add,F.mul,F.inv
    def smul(a,v): return tuple(mul(a,x) for x in v)
    def vadd(x,y): return tuple(add(a,b) for a,b in zip(x,y))
    def norm(v):
        for x in v:
            if x:return smul(inv(x),v)
        raise ValueError
    pts=sorted({norm(v) for v in itertools.product(range(q),repeat=4) if any(v)})
    pidx={p:i for i,p in enumerate(pts)}
    def symp(x,y):
        return add(add(mul(x[0],y[2]),mul(x[2],y[0])),
                   add(mul(x[1],y[3]),mul(x[3],y[1])))
    def span(x,y):
        out={norm(vadd(x,smul(t,y))) for t in range(q)}; out.add(norm(y)); return frozenset(out)
    nbr=[set() for _ in pts]; lineset=set()
    for i,j in itertools.combinations(range(len(pts)),2):
        if symp(pts[i],pts[j])==0:
            nbr[i].add(j); nbr[j].add(i)
            lineset.add(frozenset(pidx[z] for z in span(pts[i],pts[j])))
    lines=sorted(lineset,key=lambda s:tuple(sorted(s))); pair_line={}
    for li,L in enumerate(lines):
        for a,b in itertools.combinations(sorted(L),2): pair_line[(a,b)]=li
    flags=[(p,li) for li,L in enumerate(lines) for p in sorted(L)]
    fidx={f:i for i,f in enumerate(flags)}
    aptset=set(); oppP=[]
    for p,r in itertools.combinations(range(len(pts)),2):
        if r not in nbr[p]:
            common=sorted(nbr[p]&nbr[r]); assert len(common)==5; oppP.append((p,r,common))
            for a,b in itertools.combinations(common,2): aptset.add(frozenset((p,r,a,b)))
    apartments=sorted(aptset,key=lambda s:tuple(sorted(s))); aidx={A:i for i,A in enumerate(apartments)}
    apt_lines=[]; apt_edges=[]
    for A in apartments:
        es=[]
        for a,b in itertools.combinations(sorted(A),2):
            if b in nbr[a]:
                li=pair_line[(a,b)]; es.extend([(a,li),(b,li)])
        assert len(es)==8
        apt_edges.append(tuple(fidx[e] for e in es)); apt_lines.append(frozenset(li for _,li in es))
    laidx={A:i for i,A in enumerate(apt_lines)}
    lnbr=[set() for _ in lines]
    for i,j in itertools.combinations(range(len(lines)),2):
        if lines[i]&lines[j]: lnbr[i].add(j); lnbr[j].add(i)
    oppL=[]
    for l,m in itertools.combinations(range(len(lines)),2):
        if m not in lnbr[l]: oppL.append((l,m,sorted(lnbr[l]&lnbr[m])))
    charts=[]
    for p,r,common in oppP:
        charts.append(('P',{(i,j):aidx[frozenset((p,r,common[i],common[j]))]
                            for i,j in itertools.combinations(range(5),2)}))
    for l,m,common in oppL:
        charts.append(('L',{(i,j):laidx[frozenset((l,m,common[i],common[j]))]
                            for i,j in itertools.combinations(range(5),2)}))
    assert (len(pts),len(lines),len(flags),len(apartments),len(charts))==(85,85,425,13600,5440)
    return pts,lines,flags,apartments,apt_edges,charts

def chord_coordinates(flags):
    # Levi vertices: point 0..84, line 85..169.  Tree edges are gauged to zero.
    adj=[[] for _ in range(170)]
    for e,(p,l) in enumerate(flags):
        u,v=p,85+l; adj[u].append((v,e)); adj[v].append((u,e))
    parent=[-1]*170; parent[0]=0; tree=set(); queue=[0]
    for u in queue:
        for v,e in adj[u]:
            if parent[v]<0:
                parent[v]=u; tree.add(e); queue.append(v)
    assert len(tree)==169
    chords=[e for e in range(425) if e not in tree]
    assert len(chords)==256
    return chords,{e:i for i,e in enumerate(chords)}

def solve_chart(apt_edges, charts, chart_type, seconds):
    chart_index=next(i for i,(t,_) in enumerate(charts) if t==chart_type)
    loc=charts[chart_index][1]
    _,chord_index=chord_coordinates(FLAGS)
    model=cp_model.CpModel()
    y=[model.NewBoolVar(f'y_{i}') for i in range(256)]
    x=[model.NewBoolVar(f'x_{a}') for a in range(len(apt_edges))]
    for a,edges in enumerate(apt_edges):
        lits=[y[chord_index[e]] for e in edges if e in chord_index]
        # XOR(lits) == x_a  <=> XOR(lits + not x_a) == 1.
        model.AddBoolXOr(lits+[x[a].Not()])
    # fixed representative of a 2|3 cut {0,1}|{2,3,4}
    for (i,j),a in loc.items():
        target=int((i<2)!=(j<2))
        model.Add(x[a]==target)
    # already certified global code distance; useful as an exact redundant cut.
    model.Add(sum(x)>=256)
    model.Minimize(sum(x))
    solver=cp_model.CpSolver()
    solver.parameters.max_time_in_seconds=float(seconds)
    solver.parameters.num_search_workers=8
    solver.parameters.log_search_progress=True
    start=time.time(); status=solver.Solve(model); elapsed=time.time()-start
    status_name=solver.StatusName(status)
    result={'chart_type':chart_type,'chart_index':chart_index,'status':status_name,
            'wall_seconds':elapsed,'objective':None,'best_bound':float(solver.BestObjectiveBound()),
            'branches':int(solver.NumBranches()),'conflicts':int(solver.NumConflicts())}
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        result['objective']=int(round(solver.ObjectiveValue()))
        result['selected_chords']=[i for i,v in enumerate(y) if solver.Value(v)]
        result['selected_chord_weight']=len(result['selected_chords'])
        result['heavy_chart_bits']={f'{i}{j}':int(solver.Value(x[a])) for (i,j),a in loc.items()}
    return result

def main():
    global FLAGS
    _,_,FLAGS,_,apt_edges,charts=build_W4()
    results=[solve_chart(apt_edges,charts,t,900) for t in ('P','L')]
    exact=all(r['status']=='OPTIMAL' for r in results)
    out={'pass':5103,'status':'THEOREM' if exact else 'BOUNDED_SOLVER_RESULT',
         'q':4,'code_parameters':'[13600,256,256]_2','model':'Levi spanning-tree gauge + native XOR CP-SAT',
         'fixed_heavy_cut':'{0,1}|{2,3,4}','results':results,
         'promotion_condition':'Both P and L cases must be OPTIMAL before claiming the heavy-sector minimum.',
         'implication_if_384':'Combined with Pass5090: if both optima are 384, every weight-256 word has no heavy chart and hence is one of the 425 chamber stars; the next heavy sector begins at 384.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    if exact:
        assert all(r['objective']==384 for r in results), results
if __name__=='__main__': main()
