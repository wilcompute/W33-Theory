#!/usr/bin/env python3
"""Six W33 frontiers: prime-power Pascal rank, C5/Frobenius, beta and optics.

All arithmetic calculations are exact unless explicitly marked numerical.
The rank theorem is classical incidence representation theory; this package
independently reconstructs the *noncollinearity* module for q=4,8,9.
Nothing proves classical RH or a physical photonic implementation.
"""
from __future__ import annotations
import itertools,json,math,random
from pathlib import Path
import numpy as np

def field(p,t,poly):
    """GF(p^t) via a monic irreducible polynomial poly[0..t]."""
    q=p**t
    digits=[tuple((n//p**i)%p for i in range(t)) for n in range(q)]
    lookup={v:i for i,v in enumerate(digits)}
    add=np.empty((q,q),dtype=np.int16)
    mul=np.empty((q,q),dtype=np.int16)
    for a in range(q):
        for b in range(q):
            add[a,b]=lookup[tuple((x+y)%p for x,y in zip(digits[a],digits[b]))]
            coeff=[0]*(2*t-1)
            for i,x in enumerate(digits[a]):
                for j,y in enumerate(digits[b]):
                    coeff[i+j]=(coeff[i+j]+x*y)%p
            for k in range(2*t-2,t-1,-1):
                c=coeff[k]
                for j in range(t):
                    coeff[k-t+j]=(coeff[k-t+j]-c*poly[j])%p
            mul[a,b]=lookup[tuple(coeff[:t])]
    inv={a:next(b for b in range(1,q) if mul[a,b]==1) for a in range(1,q)}
    neg=np.array([next(b for b in range(q) if add[a,b]==0) for a in range(q)])
    return q,add,mul,inv,neg

def rank_modp(B,p):
    M=np.asarray(B,dtype=np.int64).copy()%p
    rows,cols=M.shape;rank=0
    for col in range(cols):
        targets=np.flatnonzero(M[rank:,col])
        if not len(targets):continue
        s=rank+int(targets[0])
        M[[rank,s]]=M[[s,rank]]
        M[rank]=(M[rank]*pow(int(M[rank,col]),-1,p))%p
        ids=np.flatnonzero(M[rank+1:,col])+rank+1
        if len(ids):M[ids]=(M[ids]-M[ids,col,None]*M[rank,None,:])%p
        rank+=1
        if rank==rows:break
    return rank

def prime_power_jordan():
    cases=[]
    for p,t,poly in ((2,2,(1,1,1)),(2,3,(1,1,0,1)),(3,1,(0,1)),(3,2,(1,0,1))):
        q,add,mul,inv,neg=field(p,t,poly)
        pts=[]
        for first in range(4):
            for rem in itertools.product(range(q),repeat=3-first):
                pts.append((0,)*first+(1,)+rem)
        n=(q+1)*(q*q+1)
        assert len(pts)==n
        V=np.array(pts,dtype=np.int16)
        sym=np.zeros((n,n),dtype=np.int16)
        for a,b,sign in ((0,2,1),(1,3,1),(2,0,-1),(3,1,-1)):
            term=mul[V[:,a,None],V[None,:,b]]
            if sign<0:term=neg[term]
            sym=add[sym,term]
        B=(sym!=0).astype(np.int64)
        assert not np.any((B@B)%p)
        d=math.comb(p+2,3)**t
        actual=rank_modp(B,p)
        assert actual==d
        assert d*2<=n-1
        cases.append({"p":p,"t":t,"q":q,"vertices":n,"rank_B":actual,
                      "Pascal_digit_rank":math.comb(p+2,3),
                      "Jordan_blocks_size2":d,
                      "Jordan_blocks_size1":n-1-2*d})
    return {"status":"PASS_EXACT","cases":cases,
            "theorem":"rank_Fp(J-I-A) = binomial(p+2,3)^t for W(3,p^t); B^2=0 mod p",
            "proof":"Symplectic B_xy=<x,y>^(q-1); generalized Lucas no-carry multinomial exponents count binomial(p+2,3)^t. Their polynomial evaluation functions are linearly independent over Fq (degree <q separately in each variable).",
            "boundary":"Classical modular p-rank, not new mathematics and not the p-rank of the separate point-line incidence matrix."}

def order_five_equivariance():
    p=3
    def normalized(v):
        a=next(x for x in v if x)
        return tuple(x*a%3 for x in v)
    points=sorted({normalized(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    ids={v:i for i,v in enumerate(points)}
    def form(x,y):return (x[0]*y[2]+x[1]*y[3]-x[2]*y[0]-x[3]*y[1])%3
    lines=set()
    for i,j in itertools.combinations(range(40),2):
        if form(points[i],points[j])==0:
            line=frozenset(ids[normalized(tuple((a*x+b*y)%3 for x,y in zip(points[i],points[j])))]
                           for a,b in itertools.product(range(3),repeat=2) if a or b)
            lines.add(line)
    lines=sorted(lines,key=lambda s:tuple(sorted(s)))
    lineids={v:k for k,v in enumerate(lines)}
    N=np.array([[int(i in v) for v in lines] for i in range(40)],dtype=np.int64)
    Z=np.zeros((40,40),dtype=np.int64)
    L=np.block([[Z,N],[N.T,Z]])
    I=np.eye(80,dtype=np.int64);L2=L@L
    Q6=L2@(16*I-L2)
    Q0=(L2-6*I)@(L2-16*I)
    # Reproducible explicit random walk of symplectic transvections, then
    # freeze its certificate by the computed permutation traces.
    def trans(v):
        return tuple(ids[normalized(tuple((x+form(y,v)*z)%3 for x,z in zip(y,v)))]
                     for y in points)
    generators=[trans(v) for v in points]
    def comp(a,b):return tuple(a[b[i]] for i in range(40))
    rng=random.Random(20);perm=tuple(range(40));identity=perm
    for step in range(1000):
        perm=comp(generators[rng.randrange(40)],perm)
        power=identity
        for order in range(1,31):
            power=comp(perm,power)
            if power==identity:break
        if order==5:break
    assert order==5
    lineperm=[lineids[frozenset(perm[i] for i in line)] for line in lines]
    G=np.zeros((80,80),dtype=np.int64)
    for i,j in enumerate(perm):G[j,i]=1
    for i,j in enumerate(lineperm):G[40+j,40+i]=1
    assert np.array_equal(G@L,L@G)
    traces={}
    for name,Q,den,expected in (("quartic_96",Q6,60,[96,-4,-4,-4,-4]),
                                ("quadratic_60",Q0,96,[60,0,0,0,0])):
        vals=[int(2*np.trace(np.linalg.matrix_power(G,k)@Q)//den)
              for k in range(5)]
        assert vals==expected
        degree=vals[0];trace=vals[1]
        four=(degree-trace)//5
        triv=(degree+4*trace)//5
        assert triv+4*four==degree
        traces[name]={"powers_0_to_4":vals,
                      "trivial_C5_copies":triv,"cyclotomic_Qzeta5_copies":four}
    assert 3%5!=1 and 7%5!=1
    return {"status":"PASS_EXACT","permutation_fifth_order":True,
            "point_fixed_count":sum(i==j for i,j in enumerate(perm)),
            "line_fixed_count":sum(i==j for i,j in enumerate(lineperm)),
            "transfer_sector_characters":traces,
            "curve_mu5":"sigma(x,y)=(zeta_5*x,y); arithmetic Frobenius F sigma F^-1=sigma^p",
            "no_go":"The graph C5 commutes with Levi transfer; curve geometric mu5 does not commute with Frobenius for p=3,7 mod20. These two C5 actions cannot be identified by a simultaneously equivariant map.",
            "scope":"No-go for the obvious curve mu5 action; a twisted semidirect-product or other correspondence is not ruled out."}

def optical_clock():
    U4=np.zeros((4,4),complex)
    for j in range(3):U4[j+1,j]=1
    U4[0,3]=-1
    U2=np.array([[0,-1],[1,0]],complex)
    assert np.allclose(U4.conj().T@U4,np.eye(4))
    assert np.allclose(U2.conj().T@U2,np.eye(2))
    d4=np.array([.91*np.exp(.2j),.81*np.exp(.4j),.71*np.exp(-.1j),.64*np.exp(.9j)])
    d2=np.array([.81*np.exp(.4j),.69*np.exp(-.3j)])
    D4=np.diag(d4);D2=np.diag(d2)
    assert np.allclose(np.linalg.matrix_power(D4@U4,4),-np.prod(d4)*np.eye(4))
    assert np.allclose(np.linalg.matrix_power(D2@U2,2),-np.prod(d2)*np.eye(2))
    mixing=np.eye(4)+.03*(np.ones((4,4))-np.eye(4))
    residual=float(np.linalg.norm(np.linalg.matrix_power(mixing@D4@U4,4)+np.prod(d4)*np.eye(4)))
    assert residual>.01
    # Native 4D Bass companion is G-unitary, but not Euclidean passive.
    R4=np.zeros((4,4),float)
    for j in range(3):R4[j+1,j]=1
    R4[0,3]=-9
    G4=np.diag([1,3,9,27])
    assert np.array_equal(R4.T@G4@R4,3*G4)
    similarity=np.diag(np.sqrt(np.diag(G4)))
    assert np.allclose(similarity@(R4/np.sqrt(3))@np.linalg.inv(similarity),U4)
    return {"status":"PASS_EXACT_PLUS_NUMERICAL_NOISE",
            "four_mode_rule":"(D U4)^4=-det(D) I for any fixed diagonal complex D",
            "two_mode_rule":"(D U2)^2=-det(D) I for any fixed diagonal complex D",
            "chosen_mode_transmissions":[float(x*x) for x in abs(d4)],
            "normalized_state_revival_with_fixed_diagonal_loss":True,
            "mixing_error_03_four_step_residual":residual,
            "native_transfer_not_Euclidean_unitary":True,
            "boundary":"Passive surrogate and postselected normalized revival only; loss changes survival, and varying/crosstalk errors break the result."}

def arithmetic_frobenius():
    from analysis.w33_20261022_pascal_phinary_frobenius import cyclotomic_phi_audit,prime_power_extension
    a=cyclotomic_phi_audit();b=prime_power_extension()
    assert a["golden_unit_orders"]=={"3":8,"7":16,"23":48}
    assert b["cases"]==18
    return {"status":"PASS_EXACT","golden_unit_orders":a["golden_unit_orders"],
            "prime_power_extension_cases":b["cases"],
            "caution":"An F9 golden element of order 8 and complex Levi phase order 8 are not an arithmetic intertwiner."}

def analytic_boundary():
    from analysis.w33_20261022_ccm_compact_weil_trace import ccm_matrix,compact_weil,relative_trace
    small=ccm_matrix(N=4,cutoff=13)
    smooth=compact_weil(cutoff=13,a=.33)
    c1=relative_trace(small,eta=.05)
    c2=relative_trace(small,eta=.10)
    assert abs(c2["relative_trace2_theory"]-4*c1["relative_trace2_theory"])<1e-12
    return {"status":"PASS_SCOPED_NUMERICAL","CCM_small_N_first_zero_error":small["first_absolute_error"],
            "smooth_Weil_2D_min_eigenvalue":smooth["eigenvalues"][0],
            "relative_trace_eta_scaling":4,
            "limitation":"Replayed previous small-N experiment; no N=120 multiprecision implementation, rigorous interval Weil bound, Xi convergence theorem or classical RH."}

def release():
    result={
      "prime_power_modular_Jordan":prime_power_jordan(),
      "order_five_mu5_Galois":order_five_equivariance(),
      "optical_signed_clock":optical_clock(),
      "golden_primepower_basechange":arithmetic_frobenius(),
      "CCM_completed_Weil_controls":analytic_boundary(),
      "classical_RH_proved":False
    }
    assert all(v["status"].startswith("PASS") for k,v in result.items() if isinstance(v,dict))
    return result

if __name__=="__main__":
    result=release()
    dest=Path(__file__).resolve().parents[1]/"data"/"w33_20261022_six_algebra_optics_frontiers.json"
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:(v.get("status") if isinstance(v,dict) else v) for k,v in result.items()},indent=2))
