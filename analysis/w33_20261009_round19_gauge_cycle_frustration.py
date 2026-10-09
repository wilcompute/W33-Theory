"""Native W33 8-cycle span and exact THREE-PLAQUETTE frustration witness.
Every simple eight-cycle flux is a gauge-invariant linear combination of
oriented edge angles. A triple of eight-cycles can sum to zero, making
simultaneous *frustrated* minima impossible.
"""
from pathlib import Path
import sys,json
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261008_5state_ritz import geometry
from w33_20261009_round18_chirality_plaquette_audit import cycles_touching

def rank_f2(bitmasks):
    pivots={}
    for row in bitmasks:
        a=row
        while a:
            k=a.bit_length()-1
            if k not in pivots:pivots[k]=a;break
            a ^= pivots[k]
    return len(pivots)
def modrank(rows,p):
    pivots={}
    for row in rows:
        a={k:v%p for k,v in row.items() if v%p}
        while a:
            k=min(a)
            if k not in pivots:
                inv=pow(a[k],-1,p)
                pivots[k]={q:v*inv%p for q,v in a.items()}
                break
            x=a[k]
            for q,v in pivots[k].items():
                value=(a.get(q,0)-x*v)%p
                if value:a[q]=value
                else:a.pop(q,None)
    return len(pivots)
def cycle_vectors():
    edges,*_=geometry()
    cycles=set()
    for j in range(len(edges)):cycles.update(cycles_touching(edges,j))
    index={tuple(sorted(e)):i for i,e in enumerate(edges)}
    masks=[];rows=[]
    for cyc in sorted(cycles):
        x=0;v={}
        for a,b in zip(cyc,cyc[1:]+cyc[:1]):
            k=index[tuple(sorted((a,b)))]
            x^=1<<k
            v[k]=1 if (a,b)==edges[k] else -1
        assert x.bit_count()==8
        masks.append(x);rows.append(v)
    return edges,sorted(cycles),masks,rows
def main():
    edges,cycles,masks,rows=cycle_vectors()
    assert len(masks)==1620
    b=rank_f2(masks)
    odd=modrank(rows,3)
    assert b==odd==len(edges)-80+1==81,(b,odd)
    # Construct a 3-cycle theta: two overlapping plaquette bitvectors xor into
    # a third one. The three edge-cycle vectors satisfy +/- c1 +/- c2 +/- c3=0.
    lookup={v:i for i,v in enumerate(masks)}
    trip=None
    for i in range(len(masks)):
        for j in range(i+1,len(masks)):
            k=lookup.get(masks[i]^masks[j])
            if k is not None and k>j:
                trip=(i,j,k);break
        if trip:break
    assert trip is not None
    v1,v2,v3=(rows[i] for i in trip)
    def equivalent(signs):
        return all(sum(signs[t]*z.get(edge,0) for t,z in enumerate((v1,v2,v3)))==0 for edge in range(160))
    signs=next((s for s in ((a,b,c) for a in [-1,1] for b in [-1,1] for c in [-1,1]) if equivalent(s)),None)
    assert signs is not None
    # For any edge angles, signed loop fluxes x+y+z=0; frustrated cos(2flux)
    # sum >= -3/2 (standard AF triangle inequality).
    out=dict(status='PASS',graph_vertices=80,graph_edges=160,cycle8_count=1620,
      rank_binary=b,rank_mod3=odd,physical_gauge_rank=79,gauge_invariant_cycle_dimension=81,
      explicit_theta_plaquette_indices=list(trip),theta_flux_relation_signs=list(signs),
      theta_cycle_vertices=[list(cycles[i]) for i in trip],
      theta_edge_intersections=[[int((masks[trip[a]]&masks[trip[b]]).bit_count()) for b in range(3)] for a in range(3)],
      global_frustrated_plaquette_nogo='For S=+g sum over all 1620 plaquettes cos(2F_c), g>0, not all terms can reach -g: the displayed 3-cycle theta has +/-F1 +/-F2 +/-F3=0 (mod 2pi), whereas F_i=pi/2 modulo pi for all three contradicts parity.',
      local_triangle_exact_minimum='For ANY three loops satisfying signed flux sum zero, sum cos(2F_i)>=-3/2; naive -3 is forbidden. Relative to -3g, this triple costs >=3g/2. The rest of the 1620-cycle lattice is not globally minimized here.',
      unfrustrated_quadratic='S=-g sum cos(F_c) has Hessian g C^T C at all-zero link phase with rank81 for g>0, kernel=79 gradient-gauge directions; this is a compact U(1) classical small-fluctuation toy, not quantum rotor spectrum.',
      boundary='No edge-flux physical couplings have been derived from W33 geometry; a classical toy gauge potential was postulated. The 79 gauge modes are graph vertex U(1) redundancy; this is not 3+1-dimensional gauge dynamics.')
    target=ROOT/'data/w33_20261009_round19_gauge_cycle_frustration.json'
    target.write_text(json.dumps(out,indent=2)+'\n')
    print('CYCLES',len(cycles),'RANKS',b,odd,'THETA',trip,signs,'OVERLAPS',out['theta_edge_intersections'],flush=True)
if __name__=='__main__':main()
