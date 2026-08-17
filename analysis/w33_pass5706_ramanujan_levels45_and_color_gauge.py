#!/usr/bin/env python3
"""Pass5706: extend the switching-gauge-fixed W33 2-lift tower to 1280 and 2560.

Pass5693 now fixes the hidden complementary-signing gauge: on a bipartite graph
sigma and -sigma are switching-equivalent, but choosing different labeled
representatives can alter the next deterministic matching factorization. We use
canonical representatives (0,1),(0,2),(0,3) of the three complement classes and
round spectral values before tie-breaking.

The resulting selected signed radii are approximately
  3.4232028039 (160 parent),
  3.3960725809 (320 parent),
  3.4539332142 (640 parent),
  3.4467824163 (1280 parent),
all below 2 sqrt(3). Hence the explicit connected Ramanujan hierarchy reaches
2560 vertices under a reproducible switching-gauge convention.

Raw matching-color labels still are not intrinsic: S4 relabels the four factor
matchings transitively on the three 2+2 partitions. A genuine all-level recursion
must be formulated in graph/switching invariants rather than these color names.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import w33_pass5683_balanced_ramanujan_levi_lifts as p5683
import w33_pass5693_explicit_ramanujan_levels23 as p5693
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5706_RAMANUJAN_LEVELS45_COLOR_GAUGE.json'
RAM=2*math.sqrt(3)
CANON={(0,1),(0,2),(0,3)}

def sparse_signed(E,n,neg):
    neg=set(neg);r=[];c=[];d=[]
    for i,(u,v) in enumerate(E):
      s=-1.0 if i in neg else 1.0
      r.extend([u,v]);c.extend([v,u]);d.extend([s,s])
    return sp.csr_matrix((d,(r,c)),shape=(n,n))

def rho(E,n,neg):
    vals=spla.eigsh(sparse_signed(E,n,neg),k=4,which='LM',return_eigenvectors=False,tol=1e-11,maxiter=200000)
    return float(max(abs(vals)))

def best(E,n):
    mats=p5693.factor4(E,n);ei={e:i for i,e in enumerate(E)};rows=[]
    for a,b in itertools.combinations(range(4),2):
      neg={ei[e] for e in mats[a]|mats[b]};rows.append((rho(E,n,neg),a,b,neg))
    D={(a,b):r for r,a,b,_ in rows}
    for x,y in [((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]:assert abs(D[x]-D[y])<1e-8
    canonical=[x for x in rows if (x[1],x[2]) in CANON]
    canonical.sort(key=lambda z:(round(z[0],10),z[1],z[2]))
    rows.sort(key=lambda z:(round(z[0],10),z[1],z[2]))
    return canonical[0],rows

def pack(rows):return [{'colors':[a,b],'signed_radius':float(r)} for r,a,b,_ in rows]

def main():
    E0=p5683.levi();neg0=set(p5683.NEG)
    E1=p5693.lift_edges(E0,80,neg0)
    b1,r1=best(E1,160);assert (b1[1],b1[2])==(0,1);E2=p5693.lift_edges(E1,160,b1[3])
    b2,r2=best(E2,320);assert (b2[1],b2[2])==(0,1);E3=p5693.lift_edges(E2,320,b2[3])
    b3,r3=best(E3,640);assert (b3[1],b3[2])==(0,1);E4=p5693.lift_edges(E3,640,b3[3])
    b4,r4=best(E4,1280);assert (b4[1],b4[2])==(0,2);E5=p5693.lift_edges(E4,1280,b4[3])
    for E,n in [(E1,160),(E2,320),(E3,640),(E4,1280),(E5,2560)]:assert p5693.components(E,n)==[n]
    for b in (b1,b2,b3,b4):assert b[0]<RAM

    # Child spectrum is parent spectrum union signed spectrum.
    base_r=math.sqrt(6);s0=3.2837688756800314
    signed=[s0,b1[0],b2[0],b3[0],b4[0]];graph_r=[base_r]
    for x in signed:graph_r.append(max(graph_r[-1],x))
    assert len(graph_r)==6 and all(x<RAM for x in graph_r)

    out={
      'pass':5706,'status':'SWITCHING_GAUGE_FIXED_W33_RAMANUJAN_TOWER_REACHES_2560__RAW_COLOR_RECURSION_IS_NONCANONICAL',
      'ramanujan_bound':RAM,
      'gauge_fix':'Complementary signings 01~23, 02~13, 03~12 are switching-equivalent; choose canonical representatives 01,02,03 and round rho to 1e-10 before lexical tie-break.',
      'signing_search':{
        '160_parent':pack(r1),'320_parent':pack(r2),'640_parent':pack(r3),'1280_parent':pack(r4),
        'selected':[{'parent_vertices':160,'colors':[b1[1],b1[2]],'rho':b1[0]},{'parent_vertices':320,'colors':[b2[1],b2[2]],'rho':b2[0]},{'parent_vertices':640,'colors':[b3[1],b3[2]],'rho':b3[0]},{'parent_vertices':1280,'colors':[b4[1],b4[2]],'rho':b4[0]}]
      },
      'explicit_graph_levels':[{'vertices':80*(2**i),'nontrivial_radius':float(graph_r[i])} for i in range(6)],
      'new_levels':{'1280_vertices':{'edges':len(E4),'ramanujan':True},'2560_vertices':{'edges':len(E5),'ramanujan':True}},
      'three_switching_classes':'The six 2-of-4 choices pair by complement. Global sign reversal on a bipartite signed adjacency is obtained by switching one bipartition, so each pair represents one lift class.',
      'recursion_no_go':'S4 relabels the four factor matchings and acts transitively on the three 2+2 partitions. Therefore the sequence 01,01,01,02 is a deterministic gauge convention, not an automorphism-invariant finite-state law. A canonical recursion must use intrinsic switching-class data.',
      'physics_boundary':'The explicit levels are internal expanders. They do not define spacetime refinement, physical distance, or a continuum metric.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
