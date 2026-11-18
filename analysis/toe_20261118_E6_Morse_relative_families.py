"""Native E6 charged module + specified PW/Morse defect operator controls.

Inputs: a supplied harmonic Higgs background and defect/boundary pattern.
Known framework:0905.1968,1812.06072. Not an assembled G2/AdS vacuum.
"""
import json
import sys
import time
from collections import Counter
from itertools import combinations,product
from math import gcd,lcm
from pathlib import Path
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass10950_clock_albert_lorentz_spinor as P
from toe_20261118_Albert_qubit_qutrit_SM_selector import independent


def native_charged_sector():
    J=P.build_clock_albert(); n=27
    den=lcm(*[v.denominator for v in J['prod'].flat])
    Pi=np.array([[[int(v*den) for v in row] for row in plane] for plane in J['prod']],dtype=np.int64)
    L=np.stack([Pi[i].T for i in range(n)])
    frame=[J['idx'][g] for g in J['G']]; c=frame[0]
    H=[i for i in range(n) if 2*L[c,i,i]==den]
    eye=np.eye(n,dtype=np.int64)
    deriv=independent([L[i]@L[j]-L[j]@L[i] for i,j in combinations(range(n),2)])
    tl=[eye[:,i] for i in range(n) if i not in frame]
    tl += [eye[:,i]-eye[:,frame[-1]] for i in frame[:-1]]
    basis=[s.Matrix(M) for M in deriv]+[s.Matrix(np.tensordot(v,L,axes=1)) for v in tl]
    assert len(basis)==78
    Psi=6*s.Matrix(L[c])/den-2*s.eye(n)
    assert Psi.eigenvals()=={s.Integer(-2):10,s.Integer(1):16,s.Integer(4):1}
    charged={}
    for q in [-3,0,3]:
        rows=s.Matrix.hstack(*[s.Matrix(list(Psi*M-M*Psi-q*M)) for M in basis]).tolist()
        vectors=P.nullspace(rows); mats=[]
        for v in vectors:
            scale=lcm(*[a.denominator for a in v]); nums=[int(a*scale) for a in v]
            g=gcd(*nums)
            mats.append(sum((s.Integer(a//g)*M for a,M in zip(nums,basis)),s.zeros(n)))
        charged[q]=mats
    assert [len(charged[q]) for q in [-3,0,3]]==[16,46,16]
    assert all(A*B==B*A for A,B in combinations(charged[-3],2))
    E=s.Matrix.hstack(*[M[:,c].extract(H,[0]) for M in charged[-3]])
    dual=s.Matrix.vstack(*[M[c,:].extract([0],H) for M in charged[3]])
    assert E.rank()==dual.rank()==16
    old=json.loads((ROOT/'data/toe_20261118_biCayley_Peirce16_SM.json').read_text())
    assert old['status']=='PASS'
    Y27=s.Matrix([[s.sympify(v) for v in row] for row in old['full27_hypercharge_matrix']])
    assert Psi*Y27==Y27*Psi and Y27[:,c]==s.zeros(27,1)
    Y=Y27.extract(H,H)
    minus=Counter({str(k):int(v) for k,v in (E.inv()*Y*E).eigenvals().items()})
    plus=Counter({str(k):int(v) for k,v in (-dual*Y*dual.inv()).eigenvals().items()})
    assert minus==Counter({'1':6,'2':3,'-4':3,'-3':2,'6':1,'0':1})
    assert plus==Counter({str(-s.Integer(k)):v for k,v in minus.items()})
    # The SU5 Wilson element is exp(2pi*i*3Q6Y/4). In the larger
    # Spin10 x U1_Psi sector it does NOT have only the SM centralizer.
    def ad(M): return Y27*M-M*Y27
    wilson=s.Matrix.hstack(*[s.Matrix(list(ad(ad(ad(M)))-16*ad(M))) for M in charged[0]])
    invariant_dimension=len(wilson.nullspace())
    assert invariant_dimension==20
    q5=[-2,-2,-2,3,3]
    d5roots=[a*q5[i]+b*q5[j] for i,j in combinations(range(5),2)
             for a,b in product([-1,1],repeat=2)]
    spin10_centralizer=5+sum(q%4==0 for q in d5roots)
    assert spin10_centralizer==19 and spin10_centralizer+1==invariant_dimension
    all_C4=[]
    for color,weak in product(range(4),repeat=2):
        if color==weak or (3*color+2*weak)%4: continue
        w=[color]*3+[weak]*2
        dim=5+sum((a*w[i]+b*w[j])%4==0 for i,j in combinations(range(5),2)
                  for a,b in product([-1,1],repeat=2))
        all_C4.append(dict(color=color,weak=weak,Spin10_centralizer_dimension=dim))
    assert [v['Spin10_centralizer_dimension'] for v in all_C4]==[21,19,19]
    return dict(Psi27_eigenvalues={'-2':10,'1':16,'4':1},
        adjoint_charge_dimensions={'-3':16,'0':46,'3':16},
        minus3_family_Q6Y=dict(minus),plus3_dual_Q6Y=dict(plus),
        native_minus3_map_to_Peirce16=[[str(v) for v in row] for row in E.tolist()],
        full_Wilson_gauge_dimension=20,Spin10_Wilson_gauge_dimension=19,
        full_Wilson_gauge_algebra='su4 + su2 + u1 + u1_Psi',
        all_SU5_SM_C4_choices_in_Spin10=all_C4,
        gauge_scope='The12-dimensional SM is a subgroup used to label modes. '
            'This Wilson element preserves6 extra Spin10 roots and extra '
            'Abelian generators; additional Higgs/bundle data are required.',
        single_sheet_cubic_Yukawa_control='All120 brackets between native '
            'q=-3 generators vanish: a bracket would need q=-6, absent from E6. '
            'The bare adjoint PW cubic therefore supplies no two-family Yukawa '
            'from this single charged16 sector. Higher operators, new sectors '
            'or changed Higgs data have not been constructed.',
        interpretation='Complexified E6 root sectors; q=-3 maps c to the native '
            'Peirce16 and q=+3 maps its dual back to c. No arbitrary16 is substituted.')


def local_witten_operator():
    create=[]
    for i in range(3):
        M=s.zeros(8)
        for mask in range(8):
            if not(mask>>i&1): M[mask|(1<<i),mask]=(-1)**((mask&((1<<i)-1)).bit_count())
        create.append(M)
    destroy=[M.T for M in create]; I=s.eye(8)
    for i,j in product(range(3),repeat=2):
        assert create[i]*destroy[j]+destroy[j]*create[i]==(I if i==j else s.zeros(8))
        assert create[i]*create[j]+create[j]*create[i]==s.zeros(8)
    lam=[2,-1,-1]
    assert sum(lam)==0
    rows=[]
    for q in [-3,3]:
        k=[q*a for a in lam]
        bosonic=sum(abs(a) for a in k)
        F=sum((a*(2*create[i]*destroy[i]-I) for i,a in enumerate(k)),s.zeros(8))
        H0=bosonic*I+F
        zero=[mask for mask in range(8) if H0[mask,mask]==0]
        assert len(zero)==1
        mask=zero[0]; v=s.eye(8)[:,mask]
        for i,a in enumerate(k):
            residual=(-abs(a)*(create[i]-destroy[i])+a*(create[i]+destroy[i]))*v
            assert residual==s.zeros(8,1)
        N=(s.prod(abs(a) for a in k)/s.pi**3)**s.Rational(1,4)
        assert s.simplify(N**2*s.prod(s.sqrt(s.pi/abs(a)) for a in k))==1
        rows.append(dict(q=q,kappa=k,zero_form_mask=mask,degree=mask.bit_count(),
            Gaussian_normalization=str(N),L2_zero_multiplicity_per_gauge_component=1,
            exact_Witten_Laplacian_gap=2*min(abs(a) for a in k)))
    assert [r['degree'] for r in rows]==[1,2]
    return dict(harmonic_gauge_function='f=x^2-y^2/2-z^2/2',
        operator='Dq=d+d_dagger+q(df wedge+i_gradf)',
        square='-Delta+sum kappa_i^2*x_i^2+sum kappa_i*(2N_i-1), kappa=q*(2,-1,-1)',
        controls=rows,
        scope='Exact noncompact quadratic PW operator with a supplied background/sign. '
            'Degree1 in q=-3 and degree2 in q=+3 describe a chiral family/CPT pair '
            'under the standard twisted7D dictionary, not two chiral families. '
            'No physical compactification or gap in measured units is implied.')


def four_pole_control():
    x=s.Symbol('x',real=True)
    poles=[-3,-1,1,3]
    g=sum(1/(x-a)**2 for a in poles[:3])-1/(x-3)**2
    polynomial=s.Poly(s.factor(s.together(g).as_numer_denom()[0]),x)
    assert g.subs(x,2)>0 and g.subs(x,s.Rational(21,10))<0
    roots=s.polys.polytools.intervals(polynomial,eps=s.Rational(1,10**12))
    brackets=[(a,b) for (a,b),m in roots if a>1 and b<3]
    assert len(brackets)==1
    a,b=brackets[0]
    S0=sum(s.Rational(1,abs(v)**3) for v in poles)
    assert S0==s.Rational(56,27)
    return dict(effective_function='f16=-sum_(a=-3,-1,1,3) 1/sqrt((x-a)^2+y^2+z^2)',
        critical_x=['-r','0','r'],r_bracket=[str(a),str(b)],
        r_polynomial=str(polynomial.as_expr()),
        complete_count_proof='The transverse gradient is(y,z)*sum r_a^-3, '
            'so every zero lies on the axis. On each of the3 intervals '
            'between poles the axial derivative strictly decreases from+infinity '
            'to-infinity; outside all poles it has one sign. Hence exactly3 zeros.',
        Hessian='diag(-2S,S,S), S=sum |x-a|^-3>0: all3 have Morse index1',
        Hessian_at_origin=['-112/27','56/27','56/27'],
        boundary_data='Four small inner spheres have negative outward normal '
            'derivative, one sufficiently large outer sphere has positive derivative.',
        limitation='Four poles and boundary data are chosen inputs, not a derivation '
            'of generation number. No complete7D ALE metric is constructed.')


def lens_relative_betti(character,negative,holes=5):
    t=character; m=len(negative)
    assert 0<m<holes and s.simplify(t**4-1)==0
    N=s.simplify(1+t+t**2+t**3)
    boundary=s.zeros(holes,holes)
    for j in range(holes-1): boundary[j+1,j]=1
    boundary[0,holes-1]=t-1
    for j in range(holes-1): boundary[j+1,holes-1]=-1
    d3=boundary[:,negative]
    d2=s.zeros(1+m,holes); d2[0,0]=N
    d1=s.Matrix([[t-1]+[1]*m])
    assert d1*d2==s.zeros(1,holes) and d2*d3==s.zeros(1+m,m)
    ranks=[d1.rank(),d2.rank(),d3.rank()]
    dims=[1,1+m,holes,m]
    betti=[dims[i]-(ranks[i-1] if i else 0)-(ranks[i] if i<3 else 0) for i in range(4)]
    return [int(v) for v in betti]


def global_lens_control():
    chi=s.Symbol('chi',positive=True)
    u=(s.pi-chi)*s.cot(chi)
    assert s.trigsimp(s.diff(u,chi,2)+2*s.cot(chi)*s.diff(u,chi))==2
    J=s.diag(s.Matrix([[0,-1],[1,0]]),s.Matrix([[0,-1],[1,0]]))
    assert J**4==s.eye(4)
    assert all((J**k-s.eye(4)).rank()==4 for k in [1,2,3])
    pts=[s.Matrix(v)/s.sqrt(sum(a*a for a in v)) for v in
         [(1,0,0,0),(0,0,1,0),(1,0,1,0),(1,0,0,1),(1,0,2,0)]]
    lifts=[J**k*p for p in pts for k in range(4)]
    assert len({tuple(v) for v in lifts})==20
    residues=[-1,-1,-1,-1,4]
    assert sum(residues)==0
    chars={r:lens_relative_betti(s.I**r,[0,1,2,3]) for r in range(4)}
    duals={r:lens_relative_betti(s.I**(-r),[4]) for r in range(4)}
    assert chars[0]==[0,3,0,0]
    assert all(chars[r]==[0,4,1,0] for r in [1,2,3])
    assert all(chars[r][1]==duals[r][2] and chars[r][2]==duals[r][1] for r in range(4))
    # Use the already certified even-Fock realization of the native16.
    old=json.loads((ROOT/'data/toe_20261118_biCayley_Peirce16_SM.json').read_text())
    fund=[2,2,2,1,1]
    charges={}
    for row in old['independent_even_Fock_control']:
        q=row['Q6Y']; w=sum(a*b for a,b in zip(fund,row['bits']))%4
        charges.setdefault(q,set()).add(w)
    assert all(len(v)==1 for v in charges.values())
    spectrum={}; d1=d2=0
    for name,row in old['SM_blocks'].items():
        q=row['Q6Y']; w=next(iter(charges[q])); b=chars[w]
        spectrum[name]=dict(Q6Y=q,dimension=row['dimension'],C4_character=w,
            chiral_copies=b[1],conjugate_chiral_copies=b[2],net_copies=b[1]-b[2])
        d1+=row['dimension']*b[1]; d2+=row['dimension']*b[2]
    assert [d1,d2]==[60,12]
    assert all(v['net_copies']==3 for v in spectrum.values())
    scans=[]
    for color,weak in product(range(4),repeat=2):
        if color==weak or (3*color+2*weak)%4: continue
        for p in range(4):
            weights=[color]*3+[weak]*2
            invariant=sum((sum(a*b for a,b in zip(weights,row['bits']))-3*p)%4==0
                          for row in old['independent_even_Fock_control'])
            scans.append(dict(color=color,weak=weak,Psi_C4_phase=p,
                invariant_family_dimension=invariant,
                chiral_components=64-invariant,conjugate_chiral_components=16-invariant,
                neutral_singlet_conjugate_copies=0 if p==0 else 1))
    assert len(scans)==12 and min(v['conjugate_chiral_components'] for v in scans)==8
    selected=[v for v in scans if (v['color'],v['weak'])==(2,1)]
    assert [v['conjugate_chiral_components'] for v in selected]==[12,8,12,16]
    assert s.Matrix([[-5,-3],[5,3]]).rank()==1
    return dict(gauge_locus='L(4,1) minus5 disjoint balls; pi1 remainsC4',
        effective_Green_function='sum_a r_a sum_(k=0)^3 G_S3(dist(x,J^k p_a)); '
            'G_S3(chi)=(pi-chi)cot(chi)/(4pi^2)',
        G_S3_Laplacian_away='1/(2pi^2); the constant cancels because sum residues=0',
        residues=residues,cover_pole_count=20,
        relative_chain_model='Mapping cone of boundaryS2 inclusions in the '
            'punctured lens CW complex: d1=t-1, d2=(1+t+t^2+t^3,0,...), '
            'boundary columns e_j and(t-1)e0-sum e_j.',
        relative_Betti_by_character=chars,conjugate_relative_Betti_by_character=duals,
        chosen_SU5_W='diag(-1,-1,-1,i,i)',family_spectrum=spectrum,
        total_complex_gauge_components=dict(chiral=60,conjugate_chiral=12,net=48),
        SU5_and_Psi_C4_scan=scans,
        mirror_floor='For this5-boundary model b2(V)=dimV-dimV^holonomy. '
            'No conjugate modes requires holonomy trivial on the family16. '
            'All12 tested SU5/Psi C4 choices retain at least8 conjugate gauge components.',
        elementary_SM_singlet_Higgs_control='With Psi phase0 only3 chiral nc '
            'singlets of(chi,Psi)=(-5,-3) are present: zero-FI D_Psi '
            'is -3 sum|N_i|^2 and has no nonzero D-flat solution. '
            'OtherPsi phases add one conjugate singlet pair, but the charges '
            'span onlyrank1. Even an algebraic paired VEV leaves3chi-5Psi '
            'unbroken. Additional independent singlets/coupled dynamics are needed; '
            'no classical zero-mode rank-breaking repair is provided.',
        conditional_index='3 complete SM family representations in the net index; '
            'extra vectorlike Q,dc,L,ec pairs remain. Source topology and flat '
            'holonomy are supplied, not dynamically selected.',
        no_complete_geometry='This is a source-free-away-from-poles PW Higgs '
            'background on an explicit punctured3-metric plus a local-system '
            'cohomology calculation, not a constructed G2 metric or the previous '
            'weak-G2 Freund-Rubin orbifold with new matter attached.')


if __name__=='__main__':
    start=time.time()
    result=dict(status='PASS',native_E6=native_charged_sector(),
        local_operator=local_witten_operator(),three_saddle_control=four_pole_control(),
        relative_global_model=global_lens_control(),
        extra_U1_Psi_anomalies_for_net_three16=dict(gravity=-144,cubic=-1296,
            SU3_squared=-18,SU2_squared=-18,Y_squared=-30,Psi_squared_Y=0),
        extra_U1_scope='If U1_Psi remains a4D gauge field, the three charged16s '
            'alone are anomalous. Additional states, inflow or a derived '
            'Green-Schwarz/Stueckelberg completion is required; none is supplied.',
        scope='Specified PW gauge-theory operator and boundary/local-system '
            'controls tied to native E6. No selected defect pattern, complete '
            'compactification, three-generation prediction, observed physics or '
            'solvedTOE. Smooth closed S3/C4 has H1real0, so sources are essential '
            'for this Abelian mechanism. Torsion-free PW equations are not '
            'assumed valid unchanged on weak-G2/AdS backgrounds.')
    # Keep the additional-U1 anomaly values derived from the actual family data.
    assert result['extra_U1_Psi_anomalies_for_net_three16']['gravity']==3*16*(-3)
    assert result['extra_U1_Psi_anomalies_for_net_three16']['cubic']==3*16*(-3)**3
    assert result['extra_U1_Psi_anomalies_for_net_three16']['SU3_squared']==3*(-3)*2
    assert result['extra_U1_Psi_anomalies_for_net_three16']['Y_squared']==3*(-3)*s.Rational(10,3)
    (ROOT/'data/toe_20261118_E6_Morse_relative_families.json').write_text(
        json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],adjoint=result['native_E6']['adjoint_charge_dimensions'],
        family_spectrum=result['relative_global_model']['family_spectrum'],seconds=time.time()-start)))
