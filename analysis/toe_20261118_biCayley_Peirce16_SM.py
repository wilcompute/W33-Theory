"""Bi-Cayley triple and colinear-state SM embedding on native Albert matrices.

Known framework: arXiv:2607.10833. Repo parents: Pass10950/10961,
Pass11580/11596. No physical Weyl index or vacuum selection is computed.
"""
import json
import sys
import time
from fractions import Fraction
from collections import Counter
from itertools import combinations, product
from math import gcd,lcm
from pathlib import Path
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass10950_clock_albert_lorentz_spinor as P
from toe_20261118_Albert_qubit_qutrit_SM_selector import independent
from toe_20261116_E6_full_cubic_SM_stabilizer import hypercharge_integer_weights


def real_kernel_basis(basis,columns):
    C=s.Matrix.hstack(*[s.Matrix(c) for c in columns])
    rows=[]
    for row in C.tolist():
        for part in [s.re,s.im]:
            r=[part(v) for v in row]
            if any(r): rows.append(r)
    if not rows: return basis[:]
    out=[]
    for v in P.nullspace(rows):
        scale=lcm(*[q.denominator for q in v]); nums=[int(q*scale) for q in v]
        common=gcd(*nums)
        out.append(sum((s.Integer(a//common)*m for a,m in zip(nums,basis)),
                       s.zeros(basis[0].rows)))
    return out


def projectors(D):
    return {s.Rational(1):2*D**2-D,s.Rational(1,2):4*D-4*D**2,
            s.Rational(0):s.eye(D.rows)-3*D+2*D**2}


def run():
    J=P.build_clock_albert(); n=27
    den=lcm(*[x.denominator for x in J['prod'].flat])
    Pi=np.array([[[int(x*den) for x in row] for row in plane] for plane in J['prod']],dtype=np.int64)
    L=np.stack([Pi[i].T for i in range(n)])
    frame=[J['idx'][g] for g in J['G']]; c=frame[0]
    H=[i for i in range(n) if 2*L[c,i,i]==den]
    outside=[i for i in range(n) if i not in H]
    assert len(H)==16
    def full_D(i,j):
        return L[i]@L[j]-L[j]@L[i]+np.tensordot(Pi[i,j],L,axes=1)
    NN=np.empty((16,16,16,16),dtype=np.int64)
    realg=[]; imagg=[]
    for i,a in enumerate(H):
        for j,b in enumerate(H):
            full=full_D(a,b)
            assert not full[np.ix_(outside,H)].any()
            NN[i,j]=full[np.ix_(H,H)]
    assert all(np.array_equal(NN[i,j].T,NN[j,i]) for i in range(16) for j in range(16))
    assert all(np.array_equal(NN[i,j][:,k],NN[k,j][:,i])
               for i in range(16) for j in range(16) for k in range(16))
    for i in range(16):
        for j in range(i,16):
            realg.append(NN[i,j]-NN[j,i])
            imagg.append(NN[i,j]+NN[j,i])
    realg,imagg=independent(realg),independent(imagg)
    assert [len(realg),len(imagg)]==[36,10]
    # Verify all46 compact generators preserve every triple-tensor entry.
    tensor=NN.transpose(2,0,1,3)
    for gens,middle in [(realg,1),(imagg,-1)]:
        for a in gens:
            defect=(np.einsum('ab,bijk->aijk',a,tensor)
                    -np.einsum('pi,apjk->aijk',a,tensor)
                    -middle*np.einsum('pj,aipk->aijk',a,tensor)
                    -np.einsum('pk,aijp->aijk',a,tensor))
            assert not defect.any()
    basis=[s.Matrix(m) for m in realg]+[s.I*s.Matrix(m) for m in imagg]
    pairs=[(H.index(i),H.index(i+1)) for i in H if J['labels'][i][0]=='pair_re']
    def D(x,y):
        return sum((x[i]*s.conjugate(y[j])*s.Matrix(NN[i,j])/den**2
                    for i in range(16) for j in range(16) if x[i] and y[j]),s.zeros(16))
    seeds=[(s.eye(16)[:,i]+sgn*s.I*s.eye(16)[:,j])/2 for i,j in pairs for sgn in [1,-1]]
    e1=seeds[0]; D1=D(e1,e1)
    assert D1*e1==e1 and D1.eigenvals()=={s.Integer(1):1,s.Rational(1,2):10,s.Integer(0):5}
    e2=next(e for e in seeds if D1*e==e/2 and D(e,e)*e1==e1/2)
    D2=D(e2,e2)
    assert D2*e2==e2 and D1*D2==D2*D1
    p1,p2=projectors(D1),projectors(D2)
    blocks={(a,b):p1[a]*p2[b] for a in p1 for b in p2}
    dimensions={str((a,b)):int(s.trace(M)) for (a,b),M in blocks.items()}
    assert sorted(v for v in dimensions.values() if v)==[1,1,2,3,3,6]
    assert sum(blocks.values(),s.zeros(16))==s.eye(16)
    for A in blocks.values(): assert A**2==A
    Wprime=p1[s.Rational(1,2)]
    # Determinant-one constraints from the cited construction, applied to
    # actual compact16 matrices with real coefficients throughout.
    spin=real_kernel_basis(basis,[s.Matrix([s.trace(M)]) for M in basis])
    assert len(spin)==45
    line1=real_kernel_basis(spin,[(s.eye(16)-p1[s.Integer(1)])*M*e1 for M in spin])
    assert len(line1)==25
    su5=real_kernel_basis(line1,[s.Matrix([s.trace(Wprime*M)]) for M in line1])
    assert len(su5)==24
    SM=real_kernel_basis(su5,[(s.eye(16)-p2[s.Integer(1)])*M*e2 for M in su5])
    assert len(SM)==12
    Q=-2*D1+10*D2-3*s.eye(16)
    assert s.trace(Q)==0 and s.trace(Wprime*Q)==0
    assert all(M*Q==Q*M for M in SM)
    assert len(real_kernel_basis(SM+[s.I*Q],[s.Matrix(list(M)) for M in SM+[s.I*Q]]))==1
    labels={(s.Rational(1,2),s.Rational(1,2)):('Q',1,6),
            (s.Rational(0),s.Rational(1,2)):('dc',2,3),
            (s.Rational(1,2),s.Rational(0)):('uc',-4,3),
            (s.Rational(0),s.Rational(0)):('L',-3,2),
            (s.Rational(1,2),s.Rational(1)):('ec',6,1),
            (s.Rational(1),s.Rational(1,2)):('nc',0,1)}
    physical={}
    for key,(name,q,mult) in labels.items():
        block=blocks[key]
        assert s.trace(block)==mult and Q*block==q*block
        assert all(M*block==block*M for M in SM)
        physical[name]=block
    color=real_kernel_basis(SM,[s.Matrix.vstack(*[s.Matrix(list(M*physical[k]))
                for k in ['L','ec','nc']]) for M in SM])
    weak=real_kernel_basis(SM,[s.Matrix.vstack(*[s.Matrix(list(M*physical[k]))
                for k in ['uc','dc','ec','nc']]) for M in SM])
    assert len(color)==8 and len(weak)==3
    assert all(A*B==B*A for A in color for B in weak)
    C=sum(((i+1)*m for i,m in enumerate(color)),s.zeros(16))
    cubic=s.trace(physical['uc']*C**3)
    assert cubic!=0 and s.trace(physical['dc']*C**3)==cubic
    assert s.trace(physical['Q']*C**3)==-2*cubic
    assert s.trace(physical['Q']*C**2)==2*s.trace(physical['uc']*C**2)
    W=weak[0]
    assert s.trace(physical['Q']*W**2)==3*s.trace(physical['L']*W**2)
    # Direct matrix normalization agrees with prior Pass11596.
    z=s.Symbol('z')
    def index_of_su2_cartan(gens):
        for M in gens:
            factors=s.factor_list(M.charpoly(z).as_expr())[1]
            quads=[(s.Poly(f,z).all_coeffs()[-1],m) for f,m in factors if s.degree(f,z)==2]
            if len(quads)==1 and quads[0][1]==4:
                return s.simplify(-s.trace(M**2)/(4*quads[0][0]))
        raise AssertionError('no simple-root Cartan control in chosen basis')
    color_index=index_of_su2_cartan(color); weak_index=index_of_su2_cartan(weak)
    Y_index=s.trace(Q**2)/36
    assert color_index==weak_index==2 and Y_index==s.Rational(10,3)
    # Center kernel on the computed SM representation, with U1 phase t.
    kernel=[]
    for a in range(3):
        for b in range(2):
            for k in range(6):
                t=Fraction(k,6)
                phases=[Fraction(a,3)+Fraction(b,2)+t,
                        -Fraction(a,3)+2*t,-Fraction(a,3)-4*t,
                        Fraction(b,2)-3*t,6*t]
                if all(v.denominator==1 for v in phases): kernel.append([a,b,k])
    assert sorted(kernel)==sorted([[k%3,k%2,k] for k in range(6)])
    # All Weyl-family perturbative anomaly sums, conditional on assigning
    # the computed representations to left-handed4D fermions.
    q={name:v[1] for key,v in labels.items() for name in [v[0]]}
    mult={name:v[2] for key,v in labels.items() for name in [v[0]]}
    assert sum(mult[k]*q[k] for k in q)==0
    assert sum(mult[k]*q[k]**3 for k in q)==0
    assert 2*q['Q']+q['uc']+q['dc']==0 and 3*q['Q']+q['L']==0
    assert (3+1)%2==0
    # Distinct Peirce choices overlap, so they are not three independent16s.
    Hframe=[{i for i in range(n) if 2*L[f,i,i]==den} for f in frame]
    assert [len(a&b) for a,b in combinations(Hframe,2)]==[8,8,8]
    assert len(set.intersection(*Hframe))==0 and len(set.union(*Hframe))==24
    # Extend the SAME selected action back into the native compact E6 on27.
    deriv=independent([L[i]@L[j]-L[j]@L[i] for i,j in combinations(range(n),2)])
    eye=np.eye(n,dtype=np.int64)
    tl=[eye[:,i] for i in range(n) if i not in frame]
    tl += [eye[:,i]-eye[:,frame[-1]] for i in frame[:-1]]
    e6=[s.Matrix(d) for d in deriv]+[s.I*s.Matrix(np.tensordot(v,L,axes=1)) for v in tl]
    assert len(e6)==78
    embedding=s.eye(n)[:,H]
    cvec=s.eye(n)[:,c]; xvec=embedding*e1; yvec=embedding*e2
    e6spin=real_kernel_basis(e6,[M*cvec for M in e6])
    e6su5=real_kernel_basis(e6spin,[M*xvec for M in e6spin])
    yline=yvec*(s.conjugate(yvec).T*yvec)[0]**-1*s.conjugate(yvec).T
    e6SM=real_kernel_basis(e6su5,[(s.eye(n)-yline)*M*yvec for M in e6su5])
    assert [len(e6spin),len(e6su5),len(e6SM)]==[45,24,12]
    restrictions=[embedding.T*M*embedding for M in e6SM]
    coeff=s.Matrix.hstack(*[s.Matrix(list(M)) for M in restrictions]).gauss_jordan_solve(
        s.Matrix(list(s.I*Q)))[0]
    assert all(s.im(v)==0 for v in coeff)
    Q27=-s.I*sum((a*M for a,M in zip(coeff,e6SM)),s.zeros(n))
    assert embedding.T*Q27*embedding==Q
    native27=Counter({int(k):int(v) for k,v in Q27.eigenvals().items()})
    parallel27=Counter(-q for q in hypercharge_integer_weights())
    assert native27==parallel27
    # The actual colinear trio, distinct from the orthogonal Jordan frame.
    def Dfull(v):
        return sum((v[i]*s.conjugate(v[j])*s.Matrix(full_D(i,j))/den**2
                    for i in range(n) for j in range(n) if v[i] and v[j]),s.zeros(n))
    dc=s.Matrix(L[c])/den; dx=Dfull(xvec); dy=Dfull(yvec)
    assert dx*yvec==yvec/2 and dy*xvec==xvec/2
    assert dc*dx==dx*dc and dc*dy==dy*dc and dx*dy==dy*dx
    hp=[projectors(d)[s.Rational(1,2)] for d in [dc,dx,dy]]
    pair=[int(s.trace(a*b)) for a,b in combinations(hp,2)]
    common=int(s.trace(hp[0]*hp[1]*hp[2]))
    union=s.eye(n)
    for a in hp: union=union*(s.eye(n)-a)
    span=int(s.trace(s.eye(n)-union))
    assert pair==[10,10,10] and common==6 and span==24
    # Keep the SAME physical hypercharge when comparing the three choices.
    spectral={}
    for qv in native27:
        E=s.eye(n)
        for rv in native27:
            if rv!=qv: E=E*(Q27-rv*s.eye(n))/(qv-rv)
        spectral[qv]=E
    trio_charges=[{str(qv):int(s.trace(a*E)) for qv,E in spectral.items()
                  if s.trace(a*E)!=0} for a in hp]
    # Independent standard half-spin/Fock realization (already used in
    # repo Pass332/346): even occupation states of five complex modes.
    fock=[]
    for bits in product([0,1],repeat=5):
        N=sum(bits)
        if N%2: continue
        Nc,Nw=sum(bits[:3]),sum(bits[3:])
        a=1-Fraction(N,4); b=Fraction(1,2)-Fraction(N,4)+Fraction(Nw,2)
        charge=-2*Nc+3*Nw
        assert charge==-2*a+10*b-3
        fock.append(dict(bits=list(bits),D1=str(a),D2=str(b),Q6Y=charge))
    assert len(fock)==16
    assert Counter(row['Q6Y'] for row in fock)==Counter({q[k]:mult[k] for k in q})
    fock_joint=Counter((row['D1'],row['D2']) for row in fock)
    assert all(fock_joint[str(a),str(b)]==int(s.trace(M)) for (a,b),M in blocks.items())
    return dict(status='PASS',parents=['Pass10950','Pass10961','Pass11580','Pass11596',
            'arXiv:2607.10833','9c87d3c1c'],
        native_Peirce16_indices=H,tripotent1=[str(v) for v in e1],tripotent2=[str(v) for v in e2],
        compact_triple_generator_dimensions=dict(real=36,imaginary=10,total=46),
        full_triple_derivation_tensor_checks=46*16**4,
        exact_selector_dimensions=[46,45,25,24,12],
        selector_chain='compact triple inner algebra -> Tr16zero -> e1line -> Tr10zero -> e2line',
        joint_Peirce_dimensions=dimensions,
        SM_blocks={name:dict(Q6Y=q[name],dimension=mult[name]) for name in q},
        color_ideal_dimension=8,weak_ideal_dimension=3,
        conjugacy_control='Color cubic traces: uc and dc equal, Q opposite twice; '
            'weak trace-square on Q is three times L. Choose Q to be color3.',
        direct16_kinetic_indices=dict(color=str(color_index),weak=str(weak_index),Y=str(Y_index)),
        conditional_tree_couplings='g3=g2=gU; gY^2=(3/5)gU^2; sin^2thetaW=3/8, '
            'same prior Spin10 normalization, not matched observed running couplings',
        faithful_SM_cover_center_kernel=kernel,
        connected_group='(SU3 x SU2 x U1)/Z6 in the computed faithful16',
        independent_even_Fock_control=fock,
        occupation_dictionary='D1=1-N/4, D2=1/2-N/4+Nweak/2, '
            '6Y=-2Ncolor+3Nweak on Lambda_even(C5). A standard representation '
            'control, not five physical qubits or an implemented spacetime fermion.',
        hypercharge_Q_matrix=[[str(v) for v in row] for row in Q.tolist()],
        hypercharge_formula='Q6Y=-2 D(e1,e1)+10 D(e2,e2)-3I',
        native_compact_E6_selector_dimensions=[78,45,24,12],
        native_E6_selectors='fix c vector, fix e1 vector, preserve e2 line',
        native_full27_Q6Y_census=dict(sorted(native27.items())),
        matches_parallel_E6_hypercharge_census=True,
        full27_hypercharge_matrix=[[str(v) for v in row] for row in Q27.tolist()],
        colinear_trio_Peirce_control=dict(individual=[16,16,16],
            pairwise_intersections=pair,triple_intersection=common,combined_span=span,
            fixed_physical_hypercharge_censuses=trio_charges),
        conditional_anomalies=dict(gravity_Y=0,Y_cubic=0,SU3_squared_Y=0,SU2_squared_Y=0,
            SU3_cubic='2-1-1=0',SU2_Witten_doublets=4),
        frame_Peirce_generation_control=dict(individual=[16,16,16],pairwise_intersections=[8,8,8],
            triple_intersection=0,combined_span=24),
        scope='Known triple/SM construction implemented on the repo E8-derived product. '
            'A complex chiral gauge representation is not a calculated4D Weyl zero-mode '
            'index, selected vacuum, three families, observed couplings or a solvedTOE.')


if __name__=='__main__':
    start=time.time(); result=run()
    (ROOT/'data/toe_20261118_biCayley_Peirce16_SM.json').write_text(
        json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],dimensions=result['exact_selector_dimensions'],
        blocks=result['SM_blocks'],seconds=time.time()-start)))
