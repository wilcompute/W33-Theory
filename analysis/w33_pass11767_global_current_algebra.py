"""Global W33 Levi current algebra: exact upper bound + replayable mod101 rank.

Prior: Oct8 eight_cycle_jacobi_identification owns sp6 semidirect h13 on C8;
h27_h13_five_frontiers owns the overlapping-center obstruction. This computes
all160 edge generators on all80 vertices, not a continuum gravity algebra.
"""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261008_five_physics_frontiers import projective_points_and_lines
OUT=ROOT/'data/w33_pass11767_global_current_algebra.json'


def actual_edges():
    points,lines=projective_points_and_lines();index={p:i for i,p in enumerate(points)}
    return [(index[p],40+j) for j,line in enumerate(lines) for p in line]


def rank_witness(edges,n,prime=101,target=None):
    """Sparse Lie saturation; every retained row has a replayable expression.

    Each expression is a generator or [earlier retained row,generator],
    minus a recorded combination of earlier rows, divided by a unit modp.
    Distinct leading entries certify independence; no floats or conjectural
    classification of transvection groups enter the dimension argument.
    """
    pivots={};rows=[];cols=[];keys=[];operations=[]
    def reduce(v,parent):
        steps=[]
        while v:
            pivot=min(v);c=v[pivot]
            if pivot not in pivots:
                scale=pow(c,-1,prime);v={k:x*scale%prime for k,x in v.items()}
                bid=len(keys);pivots[pivot]=(bid,v);keys.append(pivot)
                rr=[{} for _ in range(n)];cc=[{} for _ in range(n)]
                for k,x in v.items():i,j=divmod(k,n);rr[i][j]=x;cc[j][i]=x
                rows.append(rr);cols.append(cc);operations.append([parent,steps,scale])
                return
            bid,b=pivots[pivot];steps.append([bid,c])
            for k,x in b.items():
                z=(v.get(k,0)-c*x)%prime
                if z:v[k]=z
                else:v.pop(k,None)
    for ei,(i,j) in enumerate(edges):
        reduce({i*n+i:1,i*n+j:prime-1,j*n+i:1,j*n+j:prime-1},['g',ei])
    for bid,(rr,cc) in enumerate(zip(rows,cols)):
        for ei,(i,j) in enumerate(edges):
            v={}
            def put(a,b,x):
                k=a*n+b;z=(v.get(k,0)+x)%prime
                if z:v[k]=z
                else:v.pop(k,None)
            for k,x in cc[i].items():put(k,i,x);put(k,j,-x)
            for k,x in cc[j].items():put(k,i,x);put(k,j,-x)
            for k,x in rr[i].items():put(i,k,-x);put(j,k,-x)
            for k,x in rr[j].items():put(i,k,x);put(j,k,x)
            reduce(v,['b',bid,ei])
            if target is not None and len(keys)>=target:break
        if target is not None and len(keys)>=target:break
    return dict(prime=prime,n=n,edges=edges,pivots=keys,operations=operations,rank=len(keys))


def replay(witness):
    """Independent sparse matrix multiplication and elimination-certificate replay."""
    p=witness['prime'];n=witness['n'];edges=witness['edges'];basis=[];pivots=set()
    digest=hashlib.sha256()
    for bid,(parent,steps,scale) in enumerate(witness['operations']):
        tag=parent[0];v={}
        def put(k,x):
            z=(v.get(k,0)+x)%p
            if z:v[k]=z
            else:v.pop(k,None)
        if tag=='g':
            i,j=edges[parent[1]]
            v={i*n+i:1,i*n+j:p-1,j*n+i:1,j*n+j:p-1}
        else:
            assert tag=='b' and parent[1]<bid
            g={};i,j=edges[parent[2]]
            g={i*n+i:1,i*n+j:p-1,j*n+i:1,j*n+j:p-1}
            # Deliberately use direct sparse matrix multiplication, not the
            # producer's row/column caches and rank-one update formula.
            for ab,x in basis[parent[1]].items():
                a,b=divmod(ab,n)
                for cd,y in g.items():
                    c,d=divmod(cd,n)
                    if b==c:put(a*n+d,x*y)
                    if d==a:put(c*n+b,-y*x)
        for earlier,c in steps:
            assert earlier<bid
            old=basis[earlier];lead=min(old)
            assert v and min(v)==lead and v[lead]==c
            for k,x in old.items():put(k,-c*x)
        assert v and 0<scale<p and (v[min(v)]*scale)%p==1
        v={k:x*scale%p for k,x in v.items()};lead=min(v)
        assert lead==witness['pivots'][bid] and lead not in pivots
        pivots.add(lead);basis.append(v)
        digest.update((json.dumps(sorted(v.items()),separators=(',',':'))+'\n').encode())
    assert len(basis)==witness['rank']==len(witness['pivots'])
    return basis,digest.hexdigest()


def payload():
    edges=actual_edges();assert len(edges)==160 and all(i<40<=j for i,j in edges)
    assert all(sum(v in e for e in edges)==4 for v in range(80))
    witness=rank_witness(edges,80,target=6240);assert witness['rank']==6240
    basis,digest=replay(witness)
    # Each modular row independently satisfies the common exact constraints.
    for row in basis:
        rs=[0]*80;sc=[0]*80;tr=0
        for k,x in row.items():
            i,j=divmod(k,80);rs[i]+=x;sc[j]+=(1 if i<40 else -1)*x
            if i==j:tr+=x
        assert all(x%101==0 for x in rs+sc+[tr])
    sources=['analysis/w33_20261008_five_physics_frontiers.py',
             'analysis/w33_20261008_eight_cycle_jacobi_identification.py',
             'analysis/w33_20261008_h27_h13_five_frontiers.py']
    return dict(schema='w33.pass11767.global_current.v1',status='PASS',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        inputs={name:hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for name in sources},
        witness=witness,replayed_basis_sha256=digest,
        exact_rational_dimension=6240,quotient_carrier_dimension=78,
        common_constraints='A u=0, s^T A=0, tr(A)=0; u=ones(80), s=(ones(40),-ones(40)), s^T u=0',
        exact_upper_bound='Adapted basis u,78 columns spanning ker(s)/<u>,w gives A=[[0,r,z],[0,B,v],[0,0,0]],tr B=0. Dimension=(78^2-1)+78+78+1=6240.',
        lower_bound_proof='Every replayed mod101 row is a Lie combination of the160 actual integer edge generators. Distinct normalized leading positions certify6240 independent reductions. An integer-minor rank modulo a prime is a lower bound on rational rank; combined with the exact6240 upper bound this identifies the whole rational linear space.',
        rational_structure='sl(78,Q) semidirect Heisenberg_157(Q)',
        radical_dimension=157,center_dimension=1,center='Q*(u s^T)',perfect=True,
        no_preserved_symplectic_form_on_78_quotient=True,
        branching_explanation='For any invariant alternating form on the78 quotient, rank-one invariance forces Omega(u_e,.)=c_e v_e. For adjacent edges the pairings v_e(u_f)=v_f(u_e)=+1 at a point or-1 at a line, so c_e=-c_f. Three edges at one degree4 vertex force all three c_e=0. Connectedness propagates this to all160 edges, whose images span the quotient. Thus Omega=0; the local C8symplectic form cannot extend through the branching.',
        nonlocality='The full algebra contains dense long-range matrix directions; taking Lie closure does not restore nearest-neighbor locality. The local centers need not remain central; the surviving global center has support on every vertex.',
        prior='Oct8 local C8Jacobi identification and overlapping-center obstruction remain valid. This answers their explicit full80vertex Lie-closure question for the supplied scalar-current ansatz.',
        physical_boundary='This is an exact internal canonical-bilinear current algebra. It is not the Dirac hypersurface-deformation algebra, Lorentzian gravity, a continuum limit, chiral fermions or a completed TOE.')


if __name__=='__main__':
    result=payload();OUT.write_text(json.dumps(result,separators=(',',':'))+'\n')
    print('11767 PASS rational_dimension6240 sl78_semidirect_h157; witness replayed')
