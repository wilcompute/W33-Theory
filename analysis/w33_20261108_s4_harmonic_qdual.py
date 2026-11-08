#!/usr/bin/env python3
"""Exact S4 representation of Forty Points H1 and prime-field Gaussian clock duality.

Mathematical certificates only. Does not identify gauge bosons or a Lorentz continuum.
"""
from __future__ import annotations
import argparse,itertools,json
from collections import defaultdict
from pathlib import Path
import numpy as np

V=list(itertools.product(range(3),repeat=3))
IX={v:i for i,v in enumerate(V)}
PROJ=[(1,0),(0,1),(1,1),(1,2)]
CLASSES=[(1,1,1,1),(2,1,1),(2,2),(3,1),(4,)]
IRREPS={'trivial':[1,1,1,1,1],'sign':[1,-1,1,1,-1],
        'standard3':[3,1,-1,0,-1],'signed_standard3':[3,-1,-1,0,1],
        'two_dimensional':[2,0,2,-1,0]}
def quad(v):return (v[0]*v[2]-v[1]**2)%3
def norm(v):
    for x in v:
        if int(x)%3:return tuple(int(y*pow(int(x),-1,3)%3) for y in v)
    raise ValueError('zero projective vector')
def cycles(perm):
    seen=set();out=[]
    for i in range(len(perm)):
        if i in seen:continue
        j=i;n=0
        while j not in seen:seen.add(j);n+=1;j=perm[j]
        out.append(n)
    return tuple(sorted(out,reverse=True))
def parity(a):return -1 if sum(a[i]>a[j] for i in range(len(a)) for j in range(i+1,len(a)))%2 else 1
def complex27():
    edges=[(i,j) for i in range(27) for j in range(i+1,27)
           if quad(tuple((V[i][a]-V[j][a])%3 for a in range(3)))==0]
    ei={e:k for k,e in enumerate(edges)}
    faces=[(i,j,k) for i in range(27) for j in range(i+1,27)
           for k in range(j+1,27) if (i,j) in ei and (i,k) in ei and (j,k) in ei]
    B1=np.zeros((27,108));B2=np.zeros((108,36))
    assert len(edges)==108 and len(faces)==36
    for a,(i,j) in enumerate(edges):B1[i,a]=-1;B1[j,a]=1
    for a,(i,j,k) in enumerate(faces):
        B2[ei[i,j],a]=1;B2[ei[i,k],a]=-1;B2[ei[j,k],a]=1
    assert np.max(abs(B1@B2))==0 and np.max(abs(B2.T@B2-3*np.eye(36)))==0
    return edges,faces,ei,B1,B2
def group24():
    pidx={norm(p):i for i,p in enumerate(PROJ)}
    grp={}
    for raw in itertools.product(range(3),repeat=4):
        G=np.array(raw,dtype=int).reshape(2,2)
        if (G[0,0]*G[1,1]-G[0,1]*G[1,0])%3==0:continue
        key=min(raw,tuple(int(x) for x in (-G%3).reshape(4)))
        if key in grp:continue
        pp=[pidx[norm(G@np.array(p))] for p in PROJ]
        pv=[]
        for a,b,c in V:
            Q=(G@np.array([[a,b],[b,c]])@G.T)%3
            pv.append(IX[(int(Q[0,0]),int(Q[0,1]),int(Q[1,1]))])
        assert sorted(pv)==list(range(27))
        grp[key]=(cycles(pp),pv)
    assert len(grp)==24
    return grp
def edge_action(pv,edges,ei):
    M=np.zeros((108,108))
    for col,(i,j) in enumerate(edges):
        a,b=pv[i],pv[j]
        M[ei[tuple(sorted((a,b)))],col]=1 if a<b else -1
    return M
def s4_harmonic():
    edges,faces,ei,B1,B2=complex27()
    byclass=defaultdict(list);avg=np.zeros((108,108))
    for cl,pv in group24().values():
        c0=sum(pv[i]==i for i in range(27))
        c1=sum(1 if pv[i]<pv[j] else -1 for i,j in edges
               if tuple(sorted((pv[i],pv[j])))==(i,j))
        c2=sum(parity([pv[i],pv[j],pv[k]]) for i,j,k in faces
               if tuple(sorted((pv[i],pv[j],pv[k])))==(i,j,k))
        byclass[cl].append((c0,c1,c2,c1-c0-c2+1))
        avg+=edge_action(pv,edges,ei)/24
    expected={(1,1,1,1):(27,108,36,46),(2,1,1):(9,18,6,4),
              (2,2):(3,0,0,-2),(3,1):(3,3,3,-2),(4,):(1,0,0,0)}
    assert [len(byclass[x]) for x in CLASSES]==[1,6,3,8,6]
    assert all(set(byclass[k])=={v} for k,v in expected.items())
    char=[expected[c][3] for c in CLASSES]
    sizes=[len(byclass[c]) for c in CLASSES]
    decomp={name:sum(n*h*v for n,h,v in zip(sizes,char,row))//24
            for name,row in IRREPS.items()}
    assert decomp=={'trivial':2,'sign':0,'standard3':7,
                    'signed_standard3':5,'two_dimensional':4}
    PH=np.eye(108)-B1.T@np.linalg.pinv(B1@B1.T,rcond=1e-12)@B1-B2@B2.T/3
    P=(PH@avg+avg.T@PH.T)/2
    eigen=np.linalg.eigvalsh(P)
    assert sum(eigen>.5)==2
    err=float(max(np.max(abs(P@P-P)),np.max(abs(B1@P)),np.max(abs(B2.T@P))))
    assert err<1e-10 and abs(np.trace(P)-2)<1e-10
    translations=np.zeros((108,108))
    _,vec=np.linalg.eigh(P)
    seed=vec[:,-2:]
    translated=[];overlaps=[]
    for sh in V:
        perm=[IX[tuple((v[i]+sh[i])%3 for i in range(3))] for v in V]
        R=edge_action(perm,edges,ei)
        translations+=R/27
        translated.extend((R@seed[:,0],R@seed[:,1]))
        overlaps.append(seed.T@R@seed)
    invariant_under_translations=float(np.trace(PH@translations))
    assert abs(invariant_under_translations)<1e-10
    orbit_singular=np.linalg.svd(np.column_stack(translated),compute_uv=False)
    orbit_span=int(np.count_nonzero(orbit_singular>1e-8))
    assert orbit_span==18
    root=np.exp(2j*np.pi/3)
    null_dirs=[(1,0,0),(0,0,1),(1,1,1),(1,2,1)]
    weights=defaultdict(list)
    for k in V:
        G=sum(root**((-sum(k[i]*sh[i] for i in range(3)))%3)*overlap
              for sh,overlap in zip(V,overlaps))/27
        n0=sum(sum(k[i]*d[i] for i in range(3))%3==0 for d in null_dirs)
        weights[n0].append(float(np.trace(G).real))
    targets={4:(1,0),1:(8,0),2:(12,1/12),0:(6,1/6)}
    assert all(len(weights[k])==n and max(abs(z-w) for z in weights[k])<1e-10
               for k,(n,w) in targets.items())
    return {'status':'S4_CHARACTER_EXACT_AND_INDEPENDENT_HODGE_NUMERIC',
        'vertices':27,'edges':108,'faces':36,'harmonic_dimension':46,
        'class_order':[str(c) for c in CLASSES],'class_sizes':sizes,
        'chain_traces':{str(c):{'C0':v[0],'C1_signed':v[1],
                               'C2_signed':v[2],'H1':v[3]} for c,v in expected.items()},
        'H1_character':char,'irreducible_multiplicities':decomp,
        'S4_invariant_dimension':2,'translation_invariant_dimension':0,
        'independent_projector_trace':float(np.trace(P)),
        'independent_projector_max_residual':err,
        'translation_averaged_harmonic_trace':invariant_under_translations,
        'S4_seed_translation_span_dimension_numeric':orbit_span,
        'unspanned_harmonic_dimensions':46-orbit_span,
        'S4_seed_fourier_weight_by_n0':{str(k):{'characters':len(v),'weight_per_character':sum(v)/len(v)}
                                       for k,v in weights.items()},
        'proof':'H1 character=chi(C1)-chi(C0)-chi(C2)+chi(H0), since triangle boundaries independent and H2=0. Decompose using S4 character table.',
        'boundary':'Two S4-invariant harmonic cochains are not identified as two photon polarizations; they are not translation invariant and lack physical dynamics.'}
def gauss_clocks(primes=(3,5,7,11,13,17)):
    out=[]
    for p in primes:
        assert p>2 and all(p%d for d in range(2,int(p**.5)+1))
        k=np.indices((p,p,p));q=(k[0]*k[2]-k[1]**2)%p
        U=np.fft.ifftn(np.exp(-2j*np.pi*q/p))
        dual=(k[0]*k[2]-pow(4,-1,p)*k[1]**2)%p
        fit=U[0,0,0]*np.exp(2j*np.pi*dual/p)
        err=float(np.max(abs(U-fit)))
        flat=float(np.max(abs(abs(U)**2-p**-3)))
        weights=np.fft.ifftn(q).real
        null=q==0;null[0,0,0]=False
        support=abs(weights)>1e-9;support[0,0,0]=False
        count=int(np.count_nonzero(support))
        assert count==(p**3-p**2 if p%4==1 else p**3-1)
        assert err<1e-12 and flat<1e-12
        out.append({'prime':p,'vertices':p**3,'inverse_four_coefficient':pow(4,-1,p),
                    'finite_gauss_phase_max_residual':err,
                    'flat_probability_max_residual':flat,
                    'nonzero_weighted_displacements':count,
                    'weighted_displacements_outside_null_cone':int(np.count_nonzero(support&~null)),
                    'same_coordinate_q_star_equals_q':p==3})
    return {'status':'GAUSS_SQUARE_COMPLETION_EXACT_IDENTITY_WITH_NUMERICAL_SUPPORT_COUNTS',
        'formula':'U(d)=U(0)*zeta_p^(d0*d2 - inv4*d1^2); |U(0)|=p^(-3/2)',
        'proof':'Finite-field completion of the square gives stationary momentum (d2,-d1/2,d0), and a nondegenerate 3D Gauss sum has modulus p^(3/2).',
        'odd_prime_q_equals_its_Fourier_dual_in_fixed_chart':'Only p=3 has inv4=1 modulo p. The statement depends on the chosen coordinate chart.',
        'support_limitation':'Off-diagonal Hamiltonian support sizes checked numerically to 1e-9; no theorem claimed for all primes.',
        'physics_limitation':'The weighted Hamiltonian is long-range and does not provide a local Lorentzian continuum.',
        'cases':out}
def produce():return {'schema':'w33.20261108.s4_harmonic_qdual.v1',
   'S4_H1':s4_harmonic(),'q_duality':gauss_clocks(),
   'prior_owners':['analysis/PASS20260924_HISTORY_COMPACTIFICATION_BREAKTHROUGH.md',
                   'analysis/w33_20261108_fivefront_continuation.py',
                   'analysis/w33_20261108_deep_fivefronts.py'],
   'claim_scope':'New explicit character decomposition and Fourier-duality certificate within the repo; not a TOE or physical particle prediction.'}
def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=Path('data/w33_20261108_s4_harmonic_qdual.json'))
    x=a.parse_args();result=produce();x.out.parent.mkdir(parents=True,exist_ok=True)
    x.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf8')
    print(json.dumps({'S4_decomposition':result['S4_H1']['irreducible_multiplicities'],
                      'S4_fixed':2,'translation_fixed':0,
                      'prime_support':[(c['prime'],c['nonzero_weighted_displacements']) for c in result['q_duality']['cases']]}))
if __name__=='__main__':main()
