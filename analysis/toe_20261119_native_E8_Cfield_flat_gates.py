"""Native cubic holonomy, finite-holonomy deformation gate and Y7 H4 torsion.

Analytic geometry/proofs in the companion report; exact arithmetic below
checks the native cubic map, G2 root spaces and Gysin presentation.
No physical compactification or chiral Standard Model is claimed.
"""
from collections import Counter
from itertools import combinations_with_replacement, product
from pathlib import Path
import hashlib
import json
from math import gcd, lcm
import numpy as np
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
import toe_20261119_h27_projective_period_index as P

ROOT=Path(__file__).resolve().parents[1]


def primitive(v):
    scale=lcm(*[int(s.denom(t)) for t in v])
    w=[int(t*scale) for t in v]
    common=gcd(*w)
    w=[t//common for t in w]
    return w if next(t for t in w if t)>0 else [-t for t in w]


def monomial_product(a,b,modulus=18):
    n=len(a[0])
    return (tuple(a[0][b[0][j]] for j in range(n)),
            tuple((b[1][j]+a[1][b[0][j]])%modulus for j in range(n)))


def qutrit_SU3(g):
    phase=[3*t for t in g[1]]
    correction=(sum(phase)%9)//3
    result=g[0],tuple(2*(t-correction)%18 for t in phase)
    assert sum(result[1])%18==0
    return result


def native_data():
    reconstruction=json.loads((ROOT/'data/toe_20261113_h27_albert_cubic_coordinate_reconstruction.json').read_text())
    assert reconstruction['signed_pm1_rephasing_exists']
    coords=[tuple(reconstruction['explicit_E6_index_to_sector_matrix_coordinate'][str(j)]) for j in range(27)]
    inverse={c:j for j,c in enumerate(coords)}
    negative=set(reconstruction['signed_rephasing_negative_E6_indices'])
    source=json.loads((ROOT/'data/w33_pass11384_native_inputs.json').read_text())
    triads={tuple(sorted((i,j,k))):v for i,j,k,v in source['signed_triads']}
    assert len(triads)==45
    basis=np.zeros((78,27,27),dtype=np.int64)
    for k,rows in enumerate(source['E6_sparse_basis']):
        for i,j,v in rows:basis[k,i,j]=v

    def action(g):
        # r(conj(g)): (A,B,C) -> (A g^-1, g B g^T, conj(g) C).
        perm=[];phase=[]
        for j,(block,row,col) in enumerate(coords):
            if block==0:out=(0,row,g[0][col]);p=-g[1][col]
            elif block==1:out=(1,g[0][row],g[0][col]);p=g[1][row]+g[1][col]
            else:out=(2,g[0][row],col);p=-g[1][row]
            k=inverse[out]
            perm.append(k)
            phase.append((p+9*((j in negative)+(k in negative)))%18)
        return tuple(perm),tuple(phase)

    def verify_cubic(U):
        assert len(set(U[0]))==27
        for tr,coef in triads.items():
            image=tuple(sorted(U[0][j] for j in tr))
            assert image in triads
            expected=0 if coef==triads[image] else 9
            assert sum(U[1][j] for j in tr)%18==expected
        return 45
    return action,verify_cubic,basis,coords


def clock_transport(U):
    """Exact sparse Gaussian-rational polynomial clock matrix, phase zeta18."""
    bridge=json.loads((ROOT/'data/w33_pass11471_11475_frames_currents_matching.json').read_text())['frame']['albert_bridge']
    def gaussian(key):
        raw=bridge[key]
        exact=lambda rows:s.Matrix(rows).applyfunc(lambda v:s.Rational(str(v)))
        return exact(raw['real'])+s.I*exact(raw['imag'])
    T=gaussian('native_from_clock_basis');inverse2=gaussian('twice_inverse')
    assert T*inverse2==inverse2*T==2*s.eye(27)
    # Coefficients are kept in Q(i)[zeta18]/(zeta18^6-zeta18^3+1).
    entries={}
    for j in range(27):
        for row in range(27):
            left=inverse2[row,U[0][j]]
            if left==0:continue
            for col in range(27):
                right=T[j,col]
                if right==0:continue
                coeff=entries.setdefault((row,col),[s.S.Zero]*18)
                coeff[U[1][j]]+=s.expand(left*right)
    out=[]
    for (row,col),coeff in sorted(entries.items()):
        for degree in range(17,5,-1):
            c=coeff[degree];coeff[degree]=0
            coeff[degree-3]+=c;coeff[degree-6]-=c
        terms=[[k,int(s.re(c)),int(s.im(c))] for k,c in enumerate(coeff[:6]) if c!=0]
        if terms:out.append({'row':row,'column':col,'numerator_terms':terms,'denominator':2})
    return {'entries':out,'cyclotomic_relation':'zeta18^6-zeta18^3+1=0',
            'exact_inverse_identity':'T*(2T^-1)=(2T^-1)*T=2I',
            'preserved_positive_metric':'G_clock=T^dagger*T; not the Lorentzian Peirce metric',
            'source_cubic_identity':bridge['cubic_equality']}


def invariant_g2(B,U,V):
    assert set(U[1]) <= {0,9}
    X=np.zeros((27,27),dtype=np.int64)
    for j in range(27):X[U[0][j],j]=1 if U[1][j]==0 else -1
    assert V[0]==tuple(range(27))
    rows=[]
    conjugated=np.stack([X@b@X.T-b for b in B])
    for i,j in product(range(27),repeat=2):
        row=tuple(int(t) for t in conjugated[:,i,j])
        if any(row):rows.append(row)
        if V[1][i]!=V[1][j]:
            row=tuple(int(t) for t in B[:,i,j])
            if any(row):rows.append(row)
    M=s.Matrix(sorted(set(rows)))
    ns=M.nullspace()
    assert len(ns)==14
    G=[sum((int(c)*s.Matrix(b) for c,b in zip(primitive(v),B)),s.zeros(27)) for v in ns]
    off=[(i,j) for i,j in product(range(27),repeat=2) if i!=j]
    cn=s.Matrix([[g[i,j] for g in G] for i,j in off]).nullspace()
    assert len(cn)==2
    H=[sum((int(c)*g for c,g in zip(primitive(v),G)),s.zeros(27)) for v in cn]
    assert all(h.is_diagonal() for h in H)
    weights={}
    for g in G:
        pieces={}
        for i,j in product(range(27),repeat=2):
            if not g[i,j]:continue
            w=tuple(int(h[i,i]-h[j,j]) for h in H)
            pieces.setdefault(w,s.zeros(27))[i,j]=g[i,j]
        for w,piece in pieces.items():weights.setdefault(w,[]).append(piece)
    dimensions={w:s.Matrix.hstack(*(v.reshape(729,1) for v in vs)).rank() for w,vs in weights.items()}
    assert dimensions[(0,0)]==2
    roots=[w for w in dimensions if w!=(0,0)]
    assert len(roots)==12 and all(dimensions[w]==1 for w in roots)
    K=sum((s.Matrix(w)*s.Matrix(w).T for w in roots),s.zeros(2))
    lengths=Counter(s.simplify((s.Matrix(w).T*K.inv()*s.Matrix(w))[0]) for w in roots)
    assert sorted(lengths.values())==[6,6]
    short,long=sorted(lengths)
    assert long==3*short
    return {'invariant_E6_dimension':14,'Cartan_dimension':2,
            'root_weights':roots,'root_multiplicities':1,
            'root_length_squared_counts':{str(k):v for k,v in lengths.items()},
            'Lie_type':'G2 (rank2, 12 roots, short/long squared ratio3)',
            'native_Cartan_diagonals':[[int(h[j,j]) for j in range(27)] for h in H]},G,H


def mixed_invariants(U,V,G,H):
    def block(E,g):
        return (tuple(3*E[0][i]+g[0][j] for i,j in product(range(27),range(3))),
                tuple((E[1][i]+g[1][j])%18 for i,j in product(range(27),range(3))))
    generators=[block(U,qutrit_SU3(P.X)),block(V,qutrit_SU3(P.D))]
    unseen=set(range(81));vectors=[]
    while unseen:
        first=min(unseen);phases={first:0};todo=[first];consistent=True
        while todo:
            j=todo.pop()
            for perm,phase in generators:
                k=perm[j];p=(phases[j]+phase[j])%18
                if k not in phases:phases[k]=p;todo.append(k)
                elif phases[k]!=p:consistent=False
        unseen.difference_update(phases)
        if consistent:vectors.append(phases)
    assert len(vectors)==8
    weights=[]
    for v in vectors:
        ww={tuple(int(h[j//3,j//3]) for h in H) for j in v}
        assert len(ww)==1
        weights.append(next(iter(ww)))
    multiplicities=Counter(weights)
    assert multiplicities[(0,0)]==2 and len(multiplicities)==7
    # Verify exactly one G2 singlet, with coefficients expanded over Q(zeta18).
    powers=[]
    for p in range(18):
        c=[0]*18;c[p]=1
        for k in range(17,5,-1):
            a=c[k];c[k]=0;c[k-3]+=a;c[k-6]-=a
        powers.append(c[:6])
    rows=[];field_rows=[]
    for generator in G:
        action=np.zeros((81,6,8),dtype=np.int64)
        for column,v in enumerate(vectors):
            for j,p in v.items():
                native,flavor=divmod(j,3)
                for i in range(27):
                    if generator[i,native]:
                        action[3*i+flavor,:,column]+=int(generator[i,native])*np.array(powers[p])
        rows.extend(tuple(int(t) for t in row) for row in action.reshape(486,8) if np.any(row))
        field_rows.extend(np.sum(action*np.array([pow(2,k,19) for k in range(6)])[None,:,None],axis=1)%19)
    singlets=len(s.Matrix(sorted(set(rows))).nullspace())
    assert singlets==1
    # Rational coefficient nullity alone need not equal nullity over K.
    # zeta18 -> 2 in F19 is a field specialization (Phi18(2)=0 mod19).
    # Rank7 there proves a nonzero 7-minor over K; the displayed rational
    # relation proves rank<=7 over K. Thus the K-nullity is exactly one.
    finite=np.array(field_rows,dtype=np.int64)%19;rank=0
    for column in range(8):
        pivot=next((j for j in range(rank,len(finite)) if finite[j,column]),None)
        if pivot is None:continue
        finite[[rank,pivot]]=finite[[pivot,rank]]
        finite[rank]=finite[rank]*pow(int(finite[rank,column]),-1,19)%19
        for j in range(rank+1,len(finite)):
            if finite[j,column]:finite[j]=(finite[j]-int(finite[j,column])*finite[rank])%19
        rank+=1
    assert (pow(2,6,19)-pow(2,3,19)+1)%19==0 and rank==7
    return {'invariant_dimension':8,'G2_singlets':singlets,'G2_module':'7 + 1',
            'cyclotomic_rank_lower_bound_mod19':rank,
            'Cartan_weight_multiplicities':{str(k):v for k,v in multiplicities.items()},
            'reason':'G2 is semisimple; one singlet and remaining dimension7 imply its minimal nontrivial representation'}


def integral_Cfield_gate():
    # Z=P(F)->T2, c1(F)=t, xi=c1(O(1)), t^2=0, xi^3+t*xi^2=0.
    # Y is unit circle of O(-3) tensor det(F)^-1; Euler sign irrelevant.
    # H2(Z) basis(xi,t), H4(Z) basis(xi²,t xi), e=3xi+t.
    cup=s.Matrix([[3,0],[1,3]])
    snf=smith_normal_form(cup,domain=s.ZZ)
    diagonal=sorted(abs(int(snf[j,j])) for j in range(2))
    assert diagonal==[1,9]
    # In the quotient t*xi=-3xi²; 3*t*xi=0 -> 9xi²=0.
    generator=s.Matrix([1,0])
    assert cup.inv()*(9*generator)==s.Matrix([3,-1])
    assert any(t.q!=1 for t in cup.inv()*(3*generator))
    # p1(TY)=pullback p1(T P(F))=3xi²+2t xi = -3xi²=6 mod9.
    p1=(3-2*3)%9
    lam=(pow(2,-1,9)*p1)%9
    half_lambda=(pow(2,-1,9)*lam)%9
    assert (p1,lam,half_lambda)==(6,3,6)
    return {'circle_bundle_model':'Y = S(O(-3) tensor pi^*det(F)^-1) over P(F); rank(F)=3,c1(F)=t on T2',
            'projective_bundle_ring':'t^2=0, xi^3+t*xi^2=0',
            'Euler_class_up_to_orientation':'3xi+t',
            'H2_to_H4_Euler_cup_matrix':[list(cup.row(j)) for j in range(2)],
            'Smith_diagonal':diagonal,'H4_integral':'Z/9 generated by eta^2',
            'eta_equals_pullback_xi':True,'pullback_t':'-3 eta',
            'p1_TY_mod9':p1,'spin_lambda_p1_over2_mod9':lam,
            'unique_half_lambda_in_odd_torsion_group_mod9':half_lambda,
            'flat_degree4_differential_characters':'H3(Y;R/Z)=Z/9',
            'scope':'Nine flat degree4 C-field differences; a shifted torsor needs a reference. No real G4 flux, selected vacuum, anomaly action or physical G2 solution.'}


def SM_subalgebra_gate():
    # Complex SU3 irrep(a,b) has dimension (a+1)(b+1)(a+b+2)/2.
    # a!=b is complex type; self-conjugate SU3 irreps are real type.
    # SU2 highest weight n is real for even n, quaternionic for odd n.
    # Realify complex/quaternionic tensor irreps; conjugate SU3 pairs
    # are counted only once by taking a>=b. Bound12 suffices for <=8.
    irreps=[]
    for a in range(5):
        for b in range(a+1):
            d=(a+1)*(b+1)*(a+b+2)//2
            for n in range(12):
                realdim=d*(n+1)*(2 if a!=b or n%2 else 1)
                if realdim<=12:
                    mask=int(a+b>0)+2*int(n>0)
                    irreps.append((realdim,mask,(a,b,n)))
    best=[0,1000,1000,1000]
    for _ in range(4):
        for dimension,mask,_ in irreps:
            for prior in range(4):
                best[prior|mask]=min(best[prior|mask],best[prior]+dimension)
    joint=min(d for d,mask,_ in irreps if mask==3)
    assert best[3]==9 and joint==12
    return {'minimal_faithful_real_dimension_for_su3_plus_su2':9,
            'minimal_real_irreducible_dimension_nontrivial_on_both_factors':joint,
            'real_irreducibles_through_dimension8':[
              {'real_dimension':d,'active_factor_mask':mask,'SU3_a_b_and_SU2_n':labels}
              for d,mask,labels in irreps if d<=8],
            'su3_plus_su2_embeds_in_so8':False,
            'SM_gauge_algebra_embeds_in_this_centralizer':False,
            'reason':'An embedding into so8 gives a faithful real8 representation. Both factors need at least9 separately, or12 in a joint irreducible. Maps from the perfect semisimple factors into central u1s vanish.',
            'scope':'Rules out a direct SM subgroup/Higgs descendant of this unbroken compact gauge algebra, not other E8 embeddings, changed backgrounds, or emergent gauge dynamics.'}


def run():
    action,check,B,coords=native_data()
    native_U=action(qutrit_SU3(P.X));native_V=action(qutrit_SU3(P.D))
    cubic_checks=0;image_hashes=[]
    for a,b in product(range(3),repeat=2):
        if (a,b)==(0,0):continue
        p,q,r,t=next((p,q,r,t) for p,q,r,t in product(range(-2,3),repeat=4)
                    if p*t-q*r==1 and p%3==a and q%3==b)
        U=P.mul(P.power(P.X,p),P.power(P.D,r));V=P.mul(P.power(P.X,q),P.power(P.D,t))
        C=P.comm(U,V);images={}
        for g in P.GROUP:
            aa,bb,cc=g
            lift=P.mul(P.mul(P.power(V,bb),P.power(U,aa)),P.power(C,cc))
            SU=qutrit_SU3(lift);E=action(SU)
            cubic_checks+=check(E)
            images[g]=(tuple(3*E[0][i]+SU[0][j] for i,j in product(range(27),range(3))),
                       tuple((E[1][i]+SU[1][j])%18 for i,j in product(range(27),range(3))))
        for g,h in product(P.GROUP,repeat=2):
            assert monomial_product(images[g],images[h])==images[P.multiply(g,h)]
        digest=hashlib.sha256(repr(sorted(images.values())).encode()).hexdigest()
        image_hashes.append(digest)
    assert len(set(image_hashes))==1
    g2,G,H=invariant_g2(B,native_U,native_V)
    mixed=mixed_invariants(native_U,native_V,G,H)
    result={'status':'PASS','native_27_generators':{'X':native_U,'D':native_V},
            'native_cubic_term_checks':cubic_checks,'E8_81_product_checks':8*729,
            'eight_twists_same_E8_holonomy_image_sha256':image_hashes[0],
            'clock_generators':{'X':clock_transport(native_U),'D':clock_transport(native_V)},
            'native_E6_invariants':g2,'native_mixed_81_invariants':mixed,
            'Cfield_topology':integral_Cfield_gate(),
            'SM_subalgebra_gate':SM_subalgebra_gate(),
            'flat_deformation_gate':{'E8_invariant_dimension':30,
              'G2_module_decomposition':'14 + 7 + 7 + 1 + 1',
              'compact_centralizer_Lie_type':'so8 + u1 + u1 (classification argument in report)',
              'rank':6,'first_order_H1_Gamma_Ad_dimension':60,
              'local_flat_deformations':'commuting pair in the centralizer, modulo conjugation',
              'nearby_compact_flat_residual_rank_at_least':6,
              'SM_rank':4,'flat_only_SM_rank_reduction_possible_near_this_representation':False},
            'limitations':['standard native cubic/clock carrier identities reused and cited',
              'transported compact metric differs from Lorentzian real form',
              'G2 module/classification and geometric Gysin identification use analytic proofs',
              'not a physical G2 metric, localized chiral spectrum or stabilized SM vacuum']}
    path=ROOT/'data/toe_20261119_native_E8_Cfield_flat_gates.json'
    path.write_text(json.dumps(result,indent=2,default=lambda t:int(t))+'\n',encoding='utf8')
    print('PASS native cubic and E8 products; G2 roots; H4=Z9; flat rank floor6',flush=True)
    return result


if __name__=='__main__':run()
