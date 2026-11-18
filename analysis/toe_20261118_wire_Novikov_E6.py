"""Wire-defect relative modes, native E6 chi monodromy and domain controls.

Specified auxiliary PW gauge model, not a completed G2 compactification.
Parents580972009/27665720c; literature1812.06072 and2009.07136.
"""
import json
import sys
import time
from collections import Counter
from itertools import combinations
from math import gcd,lcm
from pathlib import Path
import numpy as np
import sympy as s
from sympy import QQ_I
from sympy.polys.matrices import DomainMatrix

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass10950_clock_albert_lorentz_spinor as P
from toe_20261118_Albert_qubit_qutrit_SM_selector import independent


def kernel_combinations(basis,columns):
    C=s.Matrix.hstack(*[s.Matrix(c) for c in columns])
    ns=DomainMatrix.from_Matrix(C).convert_to(QQ_I).nullspace().to_Matrix()
    out=[]
    for j in range(ns.rows):
        row=list(ns.row(j))
        parts=[s.re(v) for v in row]+[s.im(v) for v in row]
        scale=lcm(*[int(v.q) for v in parts])
        common=gcd(*[int(v*scale) for v in parts])
        coeff=[s.simplify(v*scale/common) for v in row]
        out.append(sum((a*M for a,M in zip(coeff,basis)),s.zeros(basis[0].rows)))
    return out


def betti(dims,differentials):
    for i in range(len(differentials)-1):
        assert differentials[i]*differentials[i+1]==s.zeros(dims[i],dims[i+2])
    ranks=[M.rank() for M in differentials]
    return [int(dims[i]-(ranks[i-1] if i else 0)-(ranks[i] if i<len(ranks) else 0))
            for i in range(len(dims))]


def topology(t):
    assert t!=0
    # M=solid torus minus3balls retracts to S1 wedge3S2.
    absolute=betti([1,1,3],[s.Matrix([[t-1]]),s.zeros(1,3)])
    # Relative to the three negative spheres: mapping-cone differential.
    negative=betti([1,4,3,3],[s.Matrix([[t-1,1,1,1]]),s.zeros(4,3),s.eye(3)])
    # Relative to the positive torus. Torus d1=(t-1,0), d2=(0,t-1)^T;
    # its fundamental2-cell maps to minus the sum of the three spheres.
    d2=s.zeros(2,5);d2[0,3]=1;d2[1,3]=-(t-1)
    d3=s.Matrix([-1,-1,-1,0,-(t-1)])
    positive=betti([1,2,5,1],[s.Matrix([[t-1,1]]),d2,d3])
    torus=betti([1,2,1],[s.Matrix([[t-1,0]]),s.Matrix([0,t-1])])
    filled_points=betti([1,1],[s.Matrix([[t-1]])])
    assert negative==[0,3,0,0] and positive==[0,0,3,0]
    return dict(absolute=absolute,relative_negative=negative,relative_positive=positive,
        positive_torus=torus,fill_points_solid_torus=filled_points)


def native_E6():
    old=json.loads((ROOT/'data/toe_20261118_biCayley_Peirce16_SM.json').read_text())
    assert old['status']=='PASS'
    J=P.build_clock_albert();n=27
    den=lcm(*[v.denominator for v in J['prod'].flat])
    Pi=np.array([[[int(v*den) for v in row] for row in plane] for plane in J['prod']],dtype=np.int64)
    L=np.stack([Pi[i].T for i in range(n)])
    frame=[J['idx'][g] for g in J['G']]; c=frame[0]
    H=old['native_Peirce16_indices']
    x=s.zeros(n,1)
    for i,v in zip(H,old['tripotent1']):x[i]=s.sympify(v)
    def Dfull(a,b):
        return L[a]@L[b]-L[b]@L[a]+np.tensordot(Pi[a,b],L,axes=1)
    Dx=sum((x[i]*s.conjugate(x[j])*s.Matrix(Dfull(i,j))/den**2
            for i in range(n) for j in range(n) if x[i] and x[j]),s.zeros(n))
    Psi=6*s.Matrix(L[c])/den-2*s.eye(n)
    Chi=-8*Dx+2*s.Matrix(L[c])/den+2*s.eye(n)
    Y=s.Matrix([[s.sympify(v) for v in row] for row in old['full27_hypercharge_matrix']])
    assert Psi*Chi==Chi*Psi and Chi*Y==Y*Chi and s.trace(Chi)==0
    assert Chi[:,c]==s.zeros(n,1)
    assert Chi.eigenvals()=={s.Integer(-5):1,s.Integer(-1):10,s.Integer(3):5,
                            s.Integer(2):5,s.Integer(-2):5,s.Integer(0):1}
    deriv=independent([L[i]@L[j]-L[j]@L[i] for i,j in combinations(range(n),2)])
    eye=np.eye(n,dtype=np.int64)
    tl=[eye[:,i] for i in range(n) if i not in frame]
    tl += [eye[:,i]-eye[:,frame[-1]] for i in frame[:-1]]
    e6=[s.Matrix(d) for d in deriv]+[s.Matrix(np.tensordot(v,L,axes=1)) for v in tl]
    blocks={}
    for p,cs in [(-3,[-5,-1,3]),(0,[-4,0,4]),(3,[-3,1,5])]:
        ps=kernel_combinations(e6,[list(Psi*M-M*Psi-p*M) for M in e6])
        for q in cs:
            blocks[p,q]=kernel_combinations(ps,[list(Chi*M-M*Chi-q*M) for M in ps])
    expected={(-3,-5):1,(-3,-1):10,(-3,3):5,(0,-4):10,(0,0):26,(0,4):10,
              (3,-3):5,(3,1):10,(3,5):1}
    assert {k:len(v) for k,v in blocks.items()}==expected
    neutral=blocks[0,0]
    invariant=kernel_combinations(neutral,[list(Y*M-M*Y) for M in neutral])
    assert len(invariant)==14
    p0=blocks[0,-4]+blocks[0,0]+blocks[0,4]
    def ad(M):return Y*M-M*Y
    no_novikov=kernel_combinations(p0,[list(ad(ad(ad(M)))-16*ad(M)) for M in p0])
    assert len(no_novikov)==20
    # All q=-3 elements still commute, so the bare two-family cubic stayszero.
    family=sum((blocks[-3,q] for q in [-5,-1,3]),[])
    assert all(A*B==B*A for A,B in combinations(family,2))
    return dict(Psi_matrix=Psi,Chi_matrix=Chi,blocks=expected,
        qminus3_chi=dict(Nc=-5,ten=-1,barfive=3),
        no_Novikov_gauge_dimension=20,nonzero_Novikov_gauge_dimension=14,
        gauge_algebra='su3+su2+u1_Y+u1_chi+u1_Psi',
        nonzero_Novikov_rule='alpha=log2 and period(omega)=1: '
            'flat monodromy t=i^(3*6Y)*2^(-qchi); qchi nonzero cannot have t=1',
        bare_same_sheet_cubic_brackets=0)


def model_spectrum():
    old=json.loads((ROOT/'data/toe_20261118_biCayley_Peirce16_SM.json').read_text())
    records={}
    for row in old['independent_even_Fock_control']:
        y=row['Q6Y'];chi=2*sum(row['bits'])-5
        phase=sum(a*b for a,b in zip([2,2,2,1,1],row['bits']))%4
        records.setdefault(y,set()).add((chi,phase))
    assert all(len(v)==1 for v in records.values())
    out={}
    for name,row in old['SM_blocks'].items():
        chi,phase=next(iter(records[row['Q6Y']]))
        t=s.I**phase*s.Rational(2)**(-chi)
        b=topology(t)['relative_negative']
        dual=topology(1/t)['relative_positive']
        assert b==[0,3,0,0] and dual==[0,0,3,0]
        out[name]=dict(dimension=row['dimension'],Q6Y=row['Q6Y'],qPsi=-3,qchi=chi,
            monodromy=str(t),chiral_copies=3,conjugate_chiral_copies=0)
    assert sum(v['dimension']*v['chiral_copies'] for v in out.values())==48
    # Any neutral-sector extension to the closed lens must obey t^4=1.
    closed={}
    for phase in range(4):
        t=s.I**phase;N=sum(t**j for j in range(4))
        b=betti([1,1,1,1],[s.Matrix([[t-1]]),s.Matrix([[N]]),s.Matrix([[t-1]])])
        assert b==([1,0,0,1] if phase==0 else [0,0,0,0])
        closed[str(phase)]=b
    assert s.Rational(2)**(-4*4)!=1
    return dict(charged_family_sector=out,closed_lens_neutral_controls=closed,
        family_components=48,family_conjugate_components=0,
        no_EW_up_Higgs_in_counted_sector=True,
        scope='Zero modes of the specified charge-dependent flat differential '
            'and relative/regular domains. No unique UV defect domain or full '
            'quantum compactification is derived.')


if __name__=='__main__':
    start=time.time(); native=native_E6()
    tests={str(t):topology(t) for t in [1,-1,s.I,-s.I,2,s.Rational(1,2),2*s.I,s.I/8,32]}
    assert tests['1']['absolute']==[1,1,3]
    assert all(v['absolute']==[0,0,3] for k,v in tests.items() if k!='1')
    result=dict(status='PASS',native_E6={k:v for k,v in native.items() if k not in ['Psi_matrix','Chi_matrix','blocks']},
        native_adjoint_charge_blocks={str(k):v for k,v in native['blocks'].items()},
        native_chi_matrix=[[str(v) for v in row] for row in native['Chi_matrix'].tolist()],
        topology='M=L(4,1) minus a core-wire tube and3point balls; '
            'M retracts to S1 wedge3S2; negative boundary3S2, positive boundaryT2; pi1Z',
        exact_character_controls=tests,spectrum=model_spectrum(),
        background='On the round restricted3-metric choose f by the Dirichlet '
            'problem Delta f=0, f=-1 on3S2, f=+1 onT2; choose omega the '
            'absolute harmonic1-form with period1. Phi=Psi*d(f/(-3))+log2*chi*omega '
            'with a commuting flat unitary SU5 Wilson connection.',
        background_scope='Existence-defined elliptic boundary problems. Hopf '
            'normal signs and omega normal0 preserve the family relative domains. '
            'No explicit numerical Higgs metric or complete7D G2 metric is supplied.',
        domain_comparison='If all fields keep the punctured absolute domain, '
            'H1 neutral candidates survive and H2 has3boundary classes percharacter. '
            'If qPsi=0 fields extend through invisible point caps, nonzeroqchi '
            'sectors live on a solidtorus and are acyclic. If bothcharges0, '
            'the C4 flat bundle can extend across the wire to the closed lens: '
            'H1=H2=0. These are different stated domain choices, not an automatic '
            'consequence of the Lie algebra.',
        inherited_failures='No selected defect pattern/Wilson/period, no rank-breaking '
            'SM-singlet completion, U1Psi anomaly/inflow unresolved, no EW-upHiggs '
            'in the counted modes, same-sheet cubicYukawa zero. Gauge dimension14 '
            'still exceedsSM12. FullG2geometry/C-field/quantum completion remain open.',
        scope='Conditional PW/Novikov wire-defect operator test tied to nativeE6, '
            'not a clean three-generation Standard Model or a solvedTOE.')
    (ROOT/'data/toe_20261118_wire_Novikov_E6.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],gauge_before=20,gauge_after=14,
        family_components=48,conjugate_family_components=0,seconds=time.time()-start)))
