"""Second Reye execution packet. Prior: control_extensions and Schur kernel matrices.
Algorithms use explicit ideal controls; noise parameters are synthetic.
"""
import json
from pathlib import Path
from itertools import permutations, product
from heapq import heappush, heappop
from fractions import Fraction
import numpy as np
from scipy.linalg import expm
import w33_reye_control_extensions as e
c=e.c


def route(n, costs, a, b):
    """Minimum cost within swap-control / terminal CNOT / undo routing.
    costs maps directed CNOT edges to positive integers; swaps require both directions.
    """
    if type(n) is not int or n<2 or a==b or any(type(x) is not int or not 0<=x<n for x in (a,b)):
        raise ValueError('invalid operands')
    if any(u==v or not 0<=u<n or not 0<=v<n or type(w) is not int or w<=0 for (u,v),w in costs.items()):
        raise ValueError('positive directed costs required')
    dist={a:0};paths={a:[a]};q=[(0,a)]
    while q:
        d,u=heappop(q)
        if d!=dist[u]:continue
        for v in range(n):
            if v==b or (u,v) not in costs or (v,u) not in costs:continue
            w=2*min(2*costs[u,v]+costs[v,u],costs[u,v]+2*costs[v,u])
            if d+w<dist.get(v,float('inf')):
                dist[v]=d+w;paths[v]=paths[u]+[v];heappush(q,(d+w,v))
    choices=[(d+costs[u,b],paths[u]+[b]) for u,d in dist.items() if (u,b) in costs]
    if not choices:raise ValueError('no route in declared routing grammar')
    cost,path=min(choices);prefix=[]
    for u,v in zip(path[:-2],path[1:-1]):
        prefix += [(u,v),(v,u),(u,v)] if costs[u,v]<=costs[v,u] else [(v,u),(u,v),(v,u)]
    program=prefix+[(path[-2],b)]+list(reversed(prefix))
    assert sum(costs[x] for x in program)==cost
    return program,cost,path


def routing_audit():
    count=0;weighted_detour=None
    for n in range(2,7):
        # Ring, star and complete graphs, asymmetric costs. No randomness.
        for kind in range(3):
            edges={(u,v):1+(7*u+3*v)%5 for u in range(n) for v in range(n)
                   if u!=v and (kind==2 or (kind==1 and (u==0 or v==0)) or (kind==0 and (u-v)%n in (1,n-1)))}
            for a,b in permutations(range(n),2):
                p,cost,path=route(n,edges,a,b);v=np.arange(2**n)
                for x,y in p:v=e.cnot_permutation(n,x,y)[v]
                assert np.array_equal(v,e.cnot_permutation(n,a,b))
                # Independent exhaustive simple-path cost oracle.
                oracle=[]
                other=[x for x in range(n) if x not in (a,b)]
                for k in range(n-1):
                    for middle in permutations(other,k):
                        P=(a,)+middle+(b,)
                        if all((u,v) in edges and (v,u) in edges for u,v in zip(P[:-2],P[1:-1])) and (P[-2],b) in edges:
                            oracle.append(sum(2*min(2*edges[u,v]+edges[v,u],edges[u,v]+2*edges[v,u]) for u,v in zip(P[:-2],P[1:-1]))+edges[P[-2],b])
                assert cost==min(oracle);count+=1
    edges={(0,2):100,(2,0):100,(0,1):1,(1,0):1,(1,2):1,(2,1):1}
    _,cost,path=route(3,edges,0,2);assert cost==7 and path==[0,1,2]
    try:route(3,{(0,1):1},0,2)
    except ValueError:pass
    else:raise AssertionError('disconnected accepted')
    return {'checked_ordered_pairs':count,'weighted_detour':{'path':path,'cost':cost,'direct_cost':100},
      'scope':'Arbitrary finite directed positive-integer CNOT cost graph; optimal only in move-control-and-restore grammar, not all circuits. Tile ports must be supplied as actual edges.'}


def commute_reduce(program):
    """Exact rational-angle merge through a commuting interval; no phase dropped."""
    out=[]
    for w,t in program:
        t=Fraction(t)
        for j in range(len(out)-1,-1,-1):
            v,s=out[j]
            if v==w:
                out[j]=(w,s+t)
                if s+t==0:out.pop(j)
                break
            if c.anticommutes(v,w):
                if t:out.append((w,t))
                break
        else:
            if t:out.append((w,t))
    return out


def pulse_audit():
    proof,_=e.shortest_proof()
    # A real batch of all compiled generators; rational multiples of pi.
    batch=[]
    for w in sorted(proof):
        batch.extend((v,Fraction(t/np.pi).limit_denominator(10000)) for v,t in c.pulses(w,np.pi/7,proof))
    reduced=commute_reduce(batch)
    U=lambda p:e.unitary([(w,float(t)*np.pi) for w,t in p])
    err=float(np.max(abs(U(batch)-U(reduced))));assert err<1e-12
    rng=np.random.default_rng(3324);words=sorted(proof)
    for _ in range(80):
        p=[(words[int(rng.integers(63))],Fraction(int(rng.integers(-4,5)),7)) for _ in range(20)]
        assert np.max(abs(U(p)-U(commute_reduce(p))))<1e-12
    example=[('XII',Fraction(1,7)),('IZI',Fraction(1,9)),('XII',Fraction(-1,7))]
    assert commute_reduce(example)==[('IZI',Fraction(1,9))]
    assert len(reduced)<len(batch)
    return {'batch_before':len(batch),'batch_after':len(reduced),'matrix_error':err,'random_coherent_checks':80,
      'scope':'Cross-template commuting cancellation; exact rational angles, no claim of global optimality. Prior: PCOAST arXiv:2305.10966.'}


def robust_audit():
    theta=np.pi/4;phi=np.arccos(-theta/(2*np.pi));rows=[]
    for eps,det,cross,gamma in [(0,0,0,0),(.01,0,0,0),(.03,0,0,0),(.1,0,0,0),(0,.01,0,0),(0,0,.01,0),(0,0,0,.001),(.03,.001,.001,.0001)]:
        metrics=[]
        for axis,s,t in product('XYZ',(-1,1),(-1,1)):
            Q=(c.EYE+s*c.MATS['IZI'])@(c.EYE+t*c.MATS['IIX'])/4
            P=c.MATS[axis+'II']@Q;other={'X':'Y','Y':'Z','Z':'X'}[axis];R=c.MATS[other+'II']@Q
            def tilted(f):return np.cos(f)*P+np.sin(f)*R
            base=[(P,theta)]
            bb=[(P,theta/2),(tilted(phi),np.pi/2),(tilted(3*phi),np.pi),(tilted(phi),np.pi/2),(P,theta/2)]
            ideal=expm(-1j*theta*P)
            result=[]
            for seq in (base,bb):
                K=[c.EYE.copy()]
                for H,time in seq:
                    V=expm(-1j*time*((1+eps)*H+det*c.MATS['IZI']+cross*c.MATS['IXI']))
                    p=(1-np.exp(-2*gamma*time))/2
                    K=[A@k for A in (np.sqrt(1-p)*V,np.sqrt(p)*c.MATS['IZI']@V) for k in K]
                assert np.max(abs(sum(k.conj().T@k for k in K)-c.EYE))<1e-12
                fidelity=(sum(abs(np.trace(ideal.conj().T@k))**2 for k in K)/8+1)/9
                leak=max(0.,float(np.linalg.eigvalsh(Q@sum(k.conj().T@(c.EYE-Q)@k for k in K)@Q)[-1]))
                result.append((float(fidelity),leak))
            metrics.append(result)
        row={'eps':eps,'detuning':det,'crosstalk':cross,'dephasing':gamma,
             'base_min_fidelity':min(x[0][0] for x in metrics),'bb1_min_fidelity':min(x[1][0] for x in metrics),
             'base_max_leakage':max(x[0][1] for x in metrics),'bb1_max_leakage':max(x[1][1] for x in metrics)}
        if eps and not(det or cross or gamma):assert 1-row['bb1_min_fidelity']<(1-row['base_min_fidelity'])/100
        rows.append(row)
    assert rows[0]['bb1_min_fidelity']>1-1e-12
    assert rows[6]['bb1_min_fidelity']<rows[6]['base_min_fidelity']
    return {'rows':rows,'duration_ratio':9,'sector_settings':12,
      'controls':'Simultaneous independently phased quadratures of sector Hamiltonians Q X1 and Q Y1 (cyclic axes), each a sum of four commuting base controls. This is an added analog control assumption, not a lowering into sequential fixed-axis pulses.',
      'boundary':'BB1 amplitude-error compensation is prior art. Synthetic amplitude benefit trades ninefold duration against dephasing, detuning and crosstalk; no uniform robustness or device claim.'}


def normalizer_audit():
    import sympy as s
    import w33_schur_cross_kernel_matrices as k
    raw=json.loads(Path(k.__file__).with_suffix('.json').read_text())
    S=s.Matrix([[s.sympify(x) for x in row] for row in raw['conjugator_to_pauli']]);Si=S.inv()
    H=s.Matrix([[1,1],[1,-1]])/s.sqrt(2);D=s.diag(1,s.I);Z=s.diag(1,-1);X=s.Matrix([[0,1],[1,0]])
    labels=list(product(range(4),range(2),range(2)));paulis={g:s.I**g[0]*Z**g[1]*X**g[2] for g in labels}
    maps=[];lifts=[]
    for T in (H,D):
        lift=k.simp(S*T*Si);assert k.equal(lift.conjugate().T*s.diag(2,1)*lift,s.diag(2,1))
        perm=[]
        for g in labels:
            image=k.simp(T*paulis[g]*T.conjugate().T)
            matches=[j for j,h in enumerate(labels) if k.equal(image,paulis[h])];assert len(matches)==1
            perm.append(matches[0])
        maps.append(tuple(perm));lifts.append([[str(x) for x in row] for row in lift.tolist()])
    identity=tuple(range(16));group={identity:[]};todo=[identity]
    for a in todo:
        for j,b in enumerate(maps):
            z=tuple(b[a[i]] for i in range(16))
            if z not in group:group[z]=group[a]+[j];todo.append(z)
    assert len(group)==24
    # Exact finite frame maps preserve the entire multiplication table.
    for a in group:
        for x,y in product(range(16),repeat=2):
            assert labels[a[labels.index(k.mul(labels[x],labels[y]))]]==k.mul(labels[a[x]],labels[a[y]])
    # These are all possibilities: image Z has six signed axes, image X four
    # anticommuting signed axes; scalars fixed. U(1) kernel by Schur lemma.
    return {'projective_normalizer_order':24,'exact_frame_product_checks':24*256,
       'generators_in_quartic_coordinates':lifts,'frame_maps':[{'permutation':list(a),'generator_word':w} for a,w in group.items()],
       'full_unitary_normalizer':'U(1) central extension of the 24 projective Clifford classes; not a finite group of order 24',
       'boundary':'Normalizer of the sixteen kernel matrices in their supplied Hermitian metric. Normalizing that group does not imply preserving the original quartic or all eleven Schur blocks.'}


if __name__=='__main__':
    import sys
    out={'status':'PASS','routing':routing_audit(),'pulses':pulse_audit(),'robust_sector':robust_audit(),'normalizer':normalizer_audit()}
    if '--write' in sys.argv:Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='normalizer'},indent=2));print('normalizer',out['normalizer']['projective_normalizer_order'])
