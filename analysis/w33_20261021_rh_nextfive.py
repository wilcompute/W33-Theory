#!/usr/bin/env python3
"""Five post-20261021 RH frontiers: explicit matrix, arithmetic Weil tests, cycle basis.

All theorems are finitely scoped. Classical RH remains OPEN.
Requires numpy, scipy, mpmath and existing repo geometry module.
"""
from __future__ import annotations
import hashlib, itertools, json, math, sys
from pathlib import Path
import numpy as np
import mpmath as mp
from scipy.integrate import quad
from scipy.special import digamma, lambertw
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from analysis.w33_pass4461_line_signing_apartment_trace import geometry, simple_four_cycles

def canon(v):
    v=tuple(int(x)%3 for x in v)
    a=next(z for z in v if z)
    return tuple((a*z)%3 for z in v)

def transvection():
    pts,lines,A,N,_=geometry()
    lookup={v:i for i,v in enumerate(pts)}
    def act(v):
        # v -> v + <v,(1,0,0,0)>*(1,0,0,0)
        return canon(((v[0]-v[1])%3,v[1],v[2],v[3]))
    ip=[lookup[act(v)] for v in pts]
    assert sorted(ip)==list(range(40))
    line_lookup={frozenset(line):j for j,line in enumerate(lines)}
    il=[line_lookup[frozenset(ip[p] for p in line)] for line in lines]
    assert sorted(il)==list(range(40))
    G=np.zeros((80,80),dtype=np.int64)
    for i,j in enumerate(ip+ [40+x for x in il]):G[j,i]=1
    L=np.block([[np.zeros((40,40),dtype=np.int64),N],[N.T,np.zeros((40,40),dtype=np.int64)]])
    assert np.array_equal(G@L,L@G)
    assert not np.array_equal(G,np.eye(80,dtype=np.int64))
    return pts,A,N,L,G

def hecke_obstruction():
    pts,A,N,L,G=transvection()
    I=np.eye(40);J=np.ones((40,40))
    P2=(2/3)*I+A/6-J/15
    Pm=I/3-A/6+J/24
    one=np.ones(40)
    assert np.max(abs(P2@one))<1e-12
    assert np.max(abs(Pm@one))<1e-12
    assert [round(np.trace(P2)),round(np.trace(Pm))]==[24,15]
    return {"status":"PASS","transvection_nontrivial":True,
            "trivial_rep_to_24D_Hom_dimension":0,
            "trivial_rep_to_15D_Hom_dimension":0,
            "reason":"The W33 point action is transitive; an equivariant image of the 1D E4 Eisenstein eigenline must be invariant, hence constant. P2 and Pminus4 kill constants.",
            "qualification":"Obstruction only to a trivial-action E4 eigenline map; a new nontrivial source Hecke module is not ruled out."}

def gf_rank_columns(C,p=101):
    pivots={};ind=[]
    for j in range(C.shape[1]):
        v=np.array(C[:,j]%p,dtype=np.int64)
        for k in sorted(pivots):
            if v[k]:v=(v-v[k]*pivots[k])%p
        nz=np.flatnonzero(v)
        if not len(nz):continue
        k=int(nz[0]);pivots[k]=v*pow(int(v[k]),-1,p)%p;ind.append(j)
    return len(ind),ind

def gf_inverse(A,p=101):
    n=A.shape[0]
    M=np.concatenate([A%p,np.eye(n,dtype=np.int64)],axis=1)
    for k in range(n):
        q=next((i for i in range(k,n) if M[i,k]%p),None)
        assert q is not None,("noninvertible",k)
        M[[k,q]]=M[[q,k]]
        M[k]=M[k]*pow(int(M[k,k]),-1,p)%p
        for i in range(n):
            if i!=k and M[i,k]:
                M[i]=(M[i]-M[i,k]*M[k])%p
    return M[:,n:]

def levi_conjugator():
    pts,A,N,L,G=transvection()
    I=np.eye(80,dtype=np.int64);L2=L@L
    T=np.block([[L,-3*I],[I,np.zeros((80,80),dtype=np.int64)]])
    Q6=L2@(16*I-L2)
    Q0=(L2-6*I)@(L2-16*I)
    generators4=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,21,22,28,30,31]
    generators2=[0,1,2,3,4,5,6,7,8,9,10,12,13,14,18,40,41,42,44,45,47,48,50,51,53,54,56,57,59,60]
    columns=[];C=np.zeros((156,156),dtype=np.int64)
    pos=0
    for Q,gens,d,constant in [(Q6,generators4,4,9),(Q0,generators2,2,3)]:
        for i in gens:
            v=np.zeros(160,dtype=np.int64)
            if i<80:v[:80]=Q[:,i]
            else:v[80:]=Q[:,i-80]
            start=v.copy()
            for k in range(d):
                columns.append(v)
                if k<d-1:C[pos+k+1,pos+k]=1
                v=T@v
            assert np.array_equal(v,-constant*start)
            C[pos,pos+d-1]=-constant
            pos+=d
    assert pos==156
    S=np.column_stack(columns)
    assert np.array_equal(T@S,S@C)
    rank,rows=gf_rank_columns(S.T)
    assert rank==156 and len(rows)==156
    B=S[rows,:]%101
    inv=gf_inverse(B)
    assert np.array_equal((B@inv)%101,np.eye(156,dtype=np.int64))
    H=np.block([[G,np.zeros((80,80),dtype=np.int64)],
                [np.zeros((80,80),dtype=np.int64),G]])
    assert np.array_equal(T@H,H@T)
    M=inv@((H@S)[rows,:]%101)%101
    assert np.array_equal((S@M-H@S)%101,np.zeros_like(S))
    assert np.array_equal((M@C-C@M)%101,np.zeros_like(C))
    assert np.all(M[:96,96:]==0) and np.all(M[96:,:96]==0)
    sha=hashlib.sha256(np.asarray(S,dtype="<i8").tobytes()).hexdigest()
    return {"status":"PASS","exact_intertwiner_shape":[160,156],"rational_rank_witness_mod101":156,
            "blocks":{"x4_plus9":24,"x2_plus3":30},"matrix_sha256_le_int64":sha,
            "generator_sets":{"quartic":generators4,"quadratic":generators2},
            "pivot_row_indices_mod101":rows,"transvection_mod101":{
                "order3":bool(np.array_equal(np.linalg.matrix_power(M,3)%101,np.eye(156,dtype=np.int64))),
                "nontrivial":not np.array_equal(M,np.eye(156,dtype=np.int64))},
            "limitation":"S defines a rational companion-block conjugator on the nontrivial subspace. The transported graph action is not a canonical geometric action on etale cohomology."}

def sieve_lambdas(bound):
    sieve=[True]*(bound+1)
    sieve[0]=sieve[1]=False
    for k in range(2,math.isqrt(bound)+1):
        if sieve[k]:
            for j in range(k*k,bound+1,k):sieve[j]=False
    out=[]
    for p in range(2,bound+1):
        if not sieve[p]:continue
        n=p
        while n<=bound:
            out.append((n,math.log(p)));n*=p
    return sorted(out)

def rigorous_prime_tail_upper(a,d,M):
    """Analytic upper bound on omitted n>M von Mangoldt Gaussian terms.

    Lambda(n)<=log(n); the two nonnegative comparison summands
    log(x)/sqrt(x)*exp(-(log(x) +/- d)^2/(4a)) decrease for x>=M,
    for the registered a=.025, |d|<=1.5 and M=400.
    Bound their sums by integrals from M to infinity, evaluate by erfc.
    """
    L=math.log(M)
    total=0.
    for shift in (d,-d):
        mu=shift+a
        z=(L-mu)/(2*math.sqrt(a))
        integral=math.exp(shift/2+a/4)*(
            mu*math.sqrt(math.pi*a)*math.erfc(z)+2*a*math.exp(-z*z))
        total+=integral
    return math.sqrt(math.pi/a)/(2*math.pi)*total

def arithmetic_gaussian(a,d,lam):
    pole=2*math.exp(a/4)*math.cosh(d/2)
    arch=quad(lambda t:math.exp(-a*t*t)*math.cos(d*t)*
              (float(digamma(.25+.5j*t).real)-math.log(math.pi)),
              0,50,epsabs=2e-12,epsrel=2e-12,limit=300)[0]/math.pi
    c=-math.sqrt(math.pi/a)/(2*math.pi)
    prime=c*sum(v/math.sqrt(n)*(math.exp(-(math.log(n)-d)**2/(4*a))
                  +math.exp(-(math.log(n)+d)**2/(4*a))) for n,v in lam)
    return {"pole":pole,"gamma":arch,"prime_powers":prime,"total":pole+arch+prime}

def weil_completed_galerkin():
    a=.025
    lam=sieve_lambdas(400)
    mp.mp.dps=35
    zeros=np.array([float(mp.im(mp.zetazero(j))) for j in range(1,31)])
    vals={}
    for d in (0.,.5,1.,1.5):
        ar=arithmetic_gaussian(a,d,lam)
        z=float(2*np.sum(np.exp(-a*zeros**2)*np.cos(d*zeros)))
        ar["rigorous_prime_power_tail_bound"]=rigorous_prime_tail_upper(a,d,400)
        assert ar["rigorous_prime_power_tail_bound"]<1e-80
        ar["sum_first30_ordinates"]=z
        ar["formula_minus_zero_sum"]=ar["total"]-z
        assert abs(ar["formula_minus_zero_sum"])<5e-10,(d,ar)
        vals[str(d)]=ar
    xx=[0.,.5,1.,1.5]
    K=np.array([[vals[str(abs(x-y))]["total"] for y in xx] for x in xx])
    eig=np.linalg.eigvalsh(K)
    assert eig[0]>0
    return {"status":"PASS","a":a,"x_grid":xx,
            "complete_terms":["pole","gamma","von Mangoldt prime powers"],
            "prime_power_cutoff":400,"integral_cutoff":50,"number_ordinate_crosscheck":30,
            "cross_checks":vals,"eigenvalues_arithmetic_galerkin":eig.tolist(),
            "min_eigenvalue":float(eig[0]),
            "qualification":"Gaussian Fourier tests are not compactly supported; quadrature/prime cutoffs are finite numerical approximations, not rigorous interval certificates nor universal Weil positivity."}

def gf2_rank_bitsets(vectors):
    pivots={}
    for row in vectors:
        w=row
        while w:
            k=w.bit_length()-1
            if k in pivots:w^=pivots[k]
            else:pivots[k]=w;break
    return len(pivots)

def apartment_classification():
    pts,lines,A,N,edge_line=geometry()
    flags=sorted((p,j) for j,line in enumerate(lines) for p in line)
    assert len(flags)==160
    flag_id={v:i for i,v in enumerate(flags)}
    octagons=set()
    incidence=[0]*160
    for cycle in simple_four_cycles(A):
        support=set()
        for side in cycle:
            j=edge_line[side]
            for p in side:support.add(flag_id[(p,j)])
        assert len(support)==8
        mask=sum(1<<v for v in support)
        octagons.add(mask)
    assert len(octagons)==1620
    for c in octagons:
        for j in range(160):
            if (c>>j)&1:incidence[j]+=1
    assert set(incidence)=={81}
    rank=gf2_rank_bitsets(octagons)
    assert rank==81==160-80+1
    # Every gauge boundary is orthogonal to each cycle; a full 81D
    # cycle-span has annihilator of dimension 160-81=79=|V|-1.
    return {"status":"PASS","edges":160,"vertices":80,"apartments":len(octagons),
            "octagons_per_edge":81,"cycle_space_rank":81,
            "gauge_boundary_rank":79,"undetected_non_gauge_signings":0,
            "theorem":"All octagon holonomies +1 iff the binary signing is a vertex-switching coboundary.",
            "qualification":"Classifies Z2 gauge-triviality only; it does not classify which nontrivial signings have tempered Artin-Ihara L-factors."}

def completed_xi(s):
    return mp.mpf(".5")*s*(s-1)*mp.pi**(-s/2)*mp.gamma(s/2)*mp.zeta(s)

def spectral_determinant_falsifier():
    mp.mp.dps=40
    n=np.arange(1,3001,dtype=float)
    t=2*np.pi*(n-7/8)/np.real(lambertw((n-7/8)/math.e))
    th2=math.acos(1/math.sqrt(11));thm=math.acos(-2/math.sqrt(11))
    eig=t+.05*(24*np.cos(n*th2)+15*np.cos(n*thm))/39
    assert np.all(eig>0) and np.all(np.diff(eig)>0)
    target={}
    logxi=lambda z:mp.log(completed_xi(mp.mpf(".5")+z)/completed_xi(mp.mpf(".5")))
    for k in (1,2,3):
        coeff=mp.diff(logxi,0,2*k)/mp.factorial(2*k)
        true=float((-1)**(k+1)*k*coeff)
        model=float(np.sum(eig**(-2*k)))
        target[str(2*k)]={"xi_taylor":true,"truncated_inverse_spectrum":model,
                          "relative_error":model/true-1}
    det={}
    for x in (1,5,10):
        true=float(mp.re(completed_xi(mp.mpf(".5")+1j*x)/completed_xi(mp.mpf(".5"))))
        product=float(np.exp(np.sum(np.log1p(-(x/eig)**2))))
        det[str(x)]={"normalized_Xi":true,"finite_toy_determinant":product,
                     "relative_error":product/true-1}
    assert abs(det["10"]["relative_error"])>.5
    return {"status":"PASS","terms":len(eig),"inverse_moments":target,"normalized_determinants":det,
            "exact_Xi_determinant":False,
            "qualification":"Truncation and incomplete regularization remain; coefficient and off-zero determinants clearly differ. Leading T log T counting does not imply spectral equality."}

def build():
    a={"hecke_intertwiner_obstruction":hecke_obstruction(),
       "levi_explicit_conjugator":levi_conjugator(),
       "arithmetic_Weil_Galerkin":weil_completed_galerkin(),
       "apartment_holonomy_completeness":apartment_classification(),
       "arithmetic_spectrum_falsifier":spectral_determinant_falsifier()}
    assert all(x["status"]=="PASS" for x in a.values())
    return {"status":"PASS","classical_RH_proved":False,
            "claim":"Five narrowly scoped RH research frontiers; no classical RH theorem.",
            "frontiers":a}

if __name__=="__main__":
    result=build()
    out=ROOT/"data"/"w33_20261021_rh_nextfive_certificate.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
    print("Wrote",out)
