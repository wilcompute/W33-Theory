"""TOE70: exact native 160-edge radius-three and 17-edge subcube certificate.

Full 160-edge *global* minimax is NOT claimed. Every signed winding cycle
is reconstructed from W33, and all rationals use Python unbounded integers.
"""
from pathlib import Path
import itertools,collections,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_five_fronts import octagons,windings,HIGH
Q=(0,-1,1)
def certificate():
    ed,adj,cy=octagons()
    rows=windings(cy,ed)
    active=[]
    for i,w in rows:
        coef=(1 if sum(w)%2 else -1)*(w[2]-w[1])**2
        if coef:active.append((coef,tuple(sorted(cy[i]))))
    assert len(rows)==238 and len(active)==159
    n,d=245,1000
    weight=[(d+n)**k*(d-n)**(8-k) for k in range(9)]
    H=set(HIGH)
    singles=[0]*160;pairs=collections.defaultdict(int);triples=collections.defaultdict(int)
    base=0
    for coef,edges in active:
        h=len(H.intersection(edges))
        base+=coef*weight[h]
        delta={e:(-1 if e in H else 1) for e in edges}
        for e in edges:
            singles[e]+=coef*(weight[h+delta[e]]-weight[h])
        for a,b in itertools.combinations(edges,2):
            da,db=delta[a],delta[b]
            pairs[a,b]+=coef*(weight[h+da+db]-weight[h+da]-weight[h+db]+weight[h])
        for a,b,c in itertools.combinations(edges,3):
            da,db,dc=delta[a],delta[b],delta[c]
            triples[a,b,c]+=coef*(weight[h+da+db+dc]-weight[h+da+db]
                -weight[h+da+dc]-weight[h+db+dc]+weight[h+da]
                +weight[h+db]+weight[h+dc]-weight[h])
    assert base==-278181245315125293750000
    b1=(min(singles),singles.index(min(singles)))
    b2=min((singles[a]+singles[b]+pairs[a,b],a,b)
           for a,b in itertools.combinations(range(160),2))
    b3=min((singles[a]+singles[b]+singles[c]+pairs[a,b]
               +pairs[a,c]+pairs[b,c]+triples[a,b,c],a,b,c)
           for a,b,c in itertools.combinations(range(160),3))
    assert b1[0]==52315612734624060937500
    assert b2==(337991711991203123437500,37,56)
    assert b3==(303334787318187810937500,37,56,57)
    # Exhaustive 2^17 subcube: high-edge set may vary but all other edges
    # are forced to low. Gray-code updates change only touched cycles.
    bits=tuple(HIGH)
    count=[0]*len(active)
    link_cycles={e:[i for i,(coef,es) in enumerate(active) if e in es] for e in bits}
    value=sum(coef*weight[0] for coef,es in active)
    best=(value,0);tied=0;negative=0;current=0
    for i in range(1<<17):
        if i:
            k=(i&-i).bit_length()-1
            g=i^(i>>1);change=1 if (g>>k)&1 else -1
            for j in link_cycles[bits[k]]:
                old=count[j];count[j]+=change
                value+=active[j][0]*(weight[count[j]]-weight[old])
            current=g
        if value<best[0]:best=(value,current);tied=1
        elif value==best[0]:tied+=1
        if value<0:negative+=1
    assert best==(base,(1<<17)-1)
    assert tied==1 and negative==1
    return {
       "status":"PASS_TOE70_EXACT_RADIUS3_AND_17BIT_SUBCUBE",
       "positive_low_weight":"755/1000","positive_high_weight":"1245/1000",
       "active_winding_cycles":len(active),
       "all_native_edges":160,"high_edge_indices":list(bits),"integer_denominator":"1000^8",
       "baseline_negative_integer":str(base),
       "one_flip":{"count":160,"min_delta":str(b1[0]),"edge":[b1[1]]},
       "two_flip":{"count":12720,"min_delta":str(b2[0]),"edges":list(b2[1:])},
       "three_flip":{"count":669920,"min_delta":str(b3[0]),"edges":list(b3[1:])},
       "restricted_subcube":{"corners_checked":131072,
          "unique_global_minimum_at_all_17_high":True,
          "number_of_negative_corners":negative,
          "scope":"Exact optimum only when all 143 other native edges remain low and phase Rayleigh q=(0,-1,1) is fixed."},
       "scope":"Global 160-bit disorder minimax and all-phase Hessian eigenvalue remain unproved."
    }
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe70_disorder_exact.json").write_text(
        json.dumps(c,indent=2)+"\n")
    print(c["status"],c["restricted_subcube"]["number_of_negative_corners"])
