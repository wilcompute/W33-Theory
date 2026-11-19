"""Complete charged E8 census for a nonproportional Cartan PW model.

Local R3 operators, supplied polynomial profiles. Not a compact G2 vacuum.
Prior: ccdd3fe07 common-profile parity; d7280e023/9321eb27e local L2 proof.
"""
import json
from itertools import combinations, combinations_with_replacement, product
from collections import Counter
from pathlib import Path
from math import gcd, lcm
import numpy as np
import sympy as s
from scipy import sparse as sp
from scipy.sparse.linalg import eigsh
from scipy.special import roots_hermite
from toe_20261118_E8_H27_wire_index_parity import e8_roots_twice

ROOT=Path(__file__).resolve().parents[1]
x,y,z=s.symbols('x y z',real=True)
Q=[s.Matrix([1,0,0]),s.Matrix([0,1,0]),s.Matrix([0,0,1]),s.Matrix([-1,-1,-1])]


def profiles(tau):
    r2=x*x+y*y
    f1=(x**4-6*x*x*y*y+y**4)/4-r2/2+z*z-x
    f2=(x**3-3*x*y*y)/3-r2+2*z*z-4*x
    f3=tau*r2/2-tau*z*z
    ff=[f1,f2,f3,-f1-f2-f3]
    assert s.expand(sum(ff))==0
    assert all(s.expand(sum(s.diff(f,v,2) for v in (x,y,z)))==0 for f in ff)
    return ff


def count_profile(f):
    f=s.expand(f)
    cz=s.diff(f,z,2)/2
    assert cz != 0
    assert s.expand(s.diff(f,z)-2*cz*z)==0
    p=s.Poly(f.subs(z,0),x,y)
    degree=p.total_degree()
    if degree>2:
        leading=sum(c*x**i*y**j for (i,j),c in p.terms() if i+j==degree)
        holomorphic=s.re(s.expand_complex((x+s.I*y)**degree))
        ratio=s.expand(leading).coeff(x,degree)
        assert ratio != 0 and s.expand(leading-ratio*holomorphic)==0
        # Planar proper gradient degree=-(degree-1), no even L2 kernels.
        count=degree-1
        form=1 if cz>0 else 2
    else:
        H=s.hessian(f,(x,y,z))
        assert H.det()!=0
        form=sum(1 for v,m in H.eigenvals().items() for _ in range(m) if v<0)
        count=1
    return int(count),int(form),str(cz),degree


def root_and_native_checks():
    roots=e8_roots_twice()
    weights=Counter()
    for r in roots:
        q=tuple(-(r[5+(i+1)%3]+r[5+(i+2)%3])//2 for i in range(3))
        assert all((r[5+(i+1)%3]+r[5+(i+2)%3])%2==0 for i in range(3))
        weights[q]+=1
    assert weights[(0,0,0)]==40
    expected=Counter({(0,0,0):40})
    for qi in Q:
        expected[tuple(qi)]+=16;expected[tuple(-qi)]+=16
    for i,j in combinations(range(4),2):
        expected[tuple(Q[i]+Q[j])]+=10
    for i,j in product(range(4),repeat=2):
        if i!=j:expected[tuple(Q[i]-Q[j])]+=1
    assert weights==expected and sum(weights.values())+8==248
    native=json.loads((ROOT/'data/toe_20261118_biCayley_Peirce16_SM.json').read_text())
    nativeY={tuple(v['bits']):v['Q6Y'] for v in native['independent_even_Fock_control']}
    matched=0
    for last in ((1,-1,-1),(-1,1,-1),(-1,-1,1),(1,1,1)):
        block=[r for r in roots if all(abs(v)==1 for v in r) and tuple(r[5:])==last]
        assert len(block)==16
        for r in block:
            bits=tuple(int(v<0) for v in r[:5])
            assert sum(a*b for a,b in zip([2,2,2,-3,-3],r[:5]))//2==nativeY[bits]
            matched+=1
    rootset=set(roots)
    singlet=(0,0,0,0,0,2,2,0)
    assert singlet in rootset
    cubic_count=0
    for r in roots:
        if all(abs(v)==1 for v in r) and tuple(r[5:])==(-1,-1,1):
            conjugate=tuple(-v for v in r[:5])+(-1,-1,-1)
            assert conjugate in rootset
            assert tuple(a+b+c for a,b,c in zip(r,conjugate,singlet))==(0,)*8
            assert tuple(a+b for a,b in zip(r,singlet)) in rootset
            cubic_count+=1
    assert cubic_count==16
    return {'roots':240,'reflection_checks':57600,'uncharged_roots_plus_Cartan':48,
            'native_spinor_weight_matches':matched,
            'nonzero_16_3_bar16_4_S43_root_triangles':cubic_count,
            'branch':'(45,1)+(1,15)+(16,4)+(16bar,4bar)+(10,6)',
            'Cartan_basis':'diag(1,0,0,-1),diag(0,1,0,-1),diag(0,0,1,-1)'}


def inventory(tau):
    ff=profiles(tau); rows=[]
    for i,f in enumerate(ff):
        n,k,cz,degree=count_profile(f)
        sign=1 if k==1 else -1
        rows.append({'name':f'16_sheet{i+1}','rep':'16' if sign==1 else '16bar',
                     'dimension':16,'multiplicity':n,'charge':list(sign*Q[i]),
                     'profile_form_degree':k,'z_coefficient':cz,'polynomial_degree':degree})
    # Choose one from each conjugate pair of the real SU4 six.
    for i,j in ((0,1),(0,2),(1,2)):
        n,k,cz,degree=count_profile(ff[i]+ff[j]);sign=1 if k==1 else -1
        rows.append({'name':f'10_pair{i+1}{j+1}','rep':'10','dimension':10,
                     'multiplicity':n,'charge':list(sign*(Q[i]+Q[j])),
                     'profile_form_degree':k,'z_coefficient':cz,'polynomial_degree':degree})
    for i,j in combinations(range(4),2):
        n,k,cz,degree=count_profile(ff[i]-ff[j]);sign=1 if k==1 else -1
        rows.append({'name':f'S_{i+1}{j+1}','rep':'1','dimension':1,
                     'multiplicity':n,'charge':list(sign*(Q[i]-Q[j])),
                     'profile_form_degree':k,'z_coefficient':cz,'polynomial_degree':degree})
    grav=s.zeros(3,1);mixed=s.zeros(3,1)
    A=s.MutableDenseNDimArray.zeros(3,3,3)
    for row in rows:
        q=s.Matrix(row['charge']);n=row['multiplicity'];dim=row['dimension']
        grav+=n*dim*q
        index={'16':2,'16bar':2,'10':1,'1':0}[row['rep']]
        mixed+=n*index*q
        for i,j,k in product(range(3),repeat=3): A[i,j,k]+=n*dim*q[i]*q[j]*q[k]
    assert sum(r['multiplicity']*(1 if r['rep']=='16' else -1) for r in rows if r['dimension']==16)==3
    # Independent enumeration: select H^1 directly for EACH charged E8 root,
    # without using the branching-table orientation or multiplicities.
    root_left=Counter(); cache={}
    for root in e8_roots_twice():
        charge=tuple(-(root[5+(i+1)%3]+root[5+(i+2)%3])//2 for i in range(3))
        if not any(charge):continue
        if charge not in cache:
            cache[charge]=count_profile(sum(charge[i]*ff[i] for i in range(3)))
        multiplicity,form,_,_=cache[charge]
        if form==1:root_left[charge]+=multiplicity
    branched_left=Counter()
    for row in rows:
        branched_left[tuple(row['charge'])]+=row['dimension']*row['multiplicity']
    assert root_left==branched_left and sum(root_left.values())==241
    return {'tau':str(tau),'profiles':[str(s.expand(f)) for f in ff], 'multiplets':rows,
            'independent_charged_root_H1_components':sum(root_left.values()),
            'root_by_root_branching_match':True,
            'net_Spin10_spinor_index':3,'left16':6,'left16bar':3,'vector10':8,'singlets':17,
            'Tr_Q':list(grav),'Spin10_squared_Q':list(mixed),
            'Tr_QaQbQc':[[[A[i,j,k] for k in range(3)] for j in range(3)] for i in range(3)]}


def vacuum_cone(packet):
    rows=packet['multiplets']; fields=[]
    for row in rows:
        if row['dimension'] not in (1,16):continue
        chi=0 if row['rep']=='1' else (-5 if row['rep']=='16' else 5)
        fields.append({'name':row['name'],'charge4':[chi]+row['charge']})
    C=s.Matrix.hstack(*[s.Matrix(v['charge4']) for v in fields])
    rays=[]
    for k in range(1,C.rank()+2):
        for inds in combinations(range(C.cols),k):
            ns=C[:,inds].nullspace()
            if len(ns)!=1:continue
            v=ns[0]
            if all(t<0 for t in v):v=-v
            if not all(t>0 for t in v):continue
            den=lcm(*[int(s.denom(t)) for t in v]); vv=[int(t*den) for t in v]
            common=gcd(*vv);vv=[t//common for t in vv]
            rays.append({'fields':[fields[i]['name'] for i in inds],
                         'canonical_norm_squared_ratio':vv,'charge_span_rank':C[:,inds].rank()})
    cubics=[]
    for inds in combinations_with_replacement(range(len(fields)),3):
        if sum((C[:,i] for i in inds),s.zeros(4,1))==s.zeros(4,1):
            cubics.append([fields[i]['name'] for i in inds])
    return {'SM_singlet_charge_matrix_rank':C.rank(),'field_types':fields,
            'nonnegative_kernel_extreme_rays':rays,'charge_allowed_cubic_types':cubics,
            'scope':'all SM-singlet types among charged L2 multiplets; zero FI and no massive/UV fields'}


def anomaly_and_Yukawa_gates(packet):
    grav=s.Matrix(packet['Tr_Q']);mixed=s.Matrix(packet['Spin10_squared_Q'])
    u=grav.cross(mixed);common=gcd(*[int(t) for t in u]);u=u/common
    cubic=sum(packet['Tr_QaQbQc'][i][j][k]*u[i]*u[j]*u[k] for i,j,k in product(range(3),repeat=3))
    assert cubic!=0
    # With <=2 GS linear factors, independent grav/mixed vectors span them;
    # every anomaly polynomial must then vanish along their common kernel u.
    rows=packet['multiplets'];channels=[]
    spin=[r for r in rows if r['rep']=='16'];vec=[r for r in rows if r['rep']=='10']
    for i,j in combinations(range(len(spin)),2):
        for v in vec:
            if s.Matrix(spin[i]['charge'])+s.Matrix(spin[j]['charge'])+s.Matrix(v['charge'])==s.zeros(3,1):
                channels.append([spin[i]['name'],spin[j]['name'],v['name']])
    assert all('16_sheet3' in c for c in channels)
    return {'primitive_grav_mixed_common_kernel':list(u), 'Tr_Qkernel_cubed':cubic,
            'minimal_linear_factors_in_specified_GS_ansatz':3,
            'GS_scope':'4D factorization I6=sum L_r(F)*X_r(F,R), same charged spectrum, no additional inflow; not a constructed quantized axion sector',
            'charge_allowed_16_16_10_types':channels,
            'six_family_bare_10_Higgs_mass_rank_cap':2,
            'rank_scope':'all allowed cubic16-16-10 channels involve the single sheet3 mode; no higher operators/mirror mixing assumed'}


def odd_operator(f,n,omega=3.):
    m=n+3;pad=n+8
    lower=sp.diags(np.sqrt(np.arange(1,pad)),1,shape=(pad,pad),format='csc')
    X=(lower+lower.T)/np.sqrt(2*omega)
    deriv=np.sqrt(omega/2)*(lower-lower.T)
    powers={i:(X**i).tocsc()[:m,:n] for i in range(4)}
    J=powers[0]
    def poly_matrix(expr):
        result=sp.csc_matrix((m*m,n*n))
        for (i,j),c in s.Poly(s.expand(expr),x,y).terms():
            result+=float(c)*sp.kron(powers[i],powers[j],format='csc')
        return result
    fx=poly_matrix(s.diff(f,x));fy=poly_matrix(s.diff(f,y))
    Dx=sp.kron(deriv[:m,:n],J,format='csc');Dy=sp.kron(J,deriv[:m,:n],format='csc')
    D=sp.bmat([[-Dx+fx,-Dy+fy],[-Dy-fy,Dx+fx]],format='csc')
    return (D.T@D).tocsc()


def harmonic_modes(f,n,omega=3.):
    H=odd_operator(f,n,omega)
    ev,vec=eigsh(H,k=4,sigma=-1e-6,which='LM',tol=1e-10,
                 v0=np.random.default_rng(19).normal(size=2*n*n))
    order=np.argsort(ev);ev=ev[order];vec=vec[:,order]
    N=n+6;Hfull=odd_operator(f,N,omega)
    residuals=[]
    for j in range(3):
        embed=np.zeros((2,N,N));embed[:,:n,:n]=vec[:,j].reshape(2,n,n)
        residuals.append(float(np.linalg.norm(Hfull@embed.ravel()-ev[j]*embed.ravel())))
    return ev,vec[:,:3],residuals


def yukawa_overlap(n,tau=s.Rational(7,4),omega=3.):
    ff=profiles(tau)
    h=(-ff[3]).subs(z,0)
    g=(ff[3]-ff[2]).subs(z,0)
    eh,U,rh=harmonic_modes(h,n,omega)
    eg,V,rg=harmonic_modes(g,n,omega)
    tf=float(tau)
    nodes,weights=roots_hermite(n+8)
    scale=omega+tf/2
    t=np.sqrt(omega/scale)*nodes
    H=np.zeros((n,len(nodes)));H[0]=1
    if n>1:H[1]=np.sqrt(2)*t
    for k in range(1,n-1):H[k+1]=np.sqrt(2/(k+1))*t*H[k]-np.sqrt(k/(k+1))*H[k-1]
    C=np.sqrt(omega/(np.pi*scale))*(H*weights)@H.T
    # Weighted overlap with the exact planar Gaussian of the 16_sheet3 mode.
    block=V.reshape(2,n,n,3)
    weighted=np.empty_like(block)
    for comp,j in product(range(2),range(3)):weighted[comp,:,:,j]=C@block[comp,:,:,j]@C.T
    UV=U.reshape(2,n*n,3);WV=weighted.reshape(2,n*n,3)
    planar=np.sqrt(tf/np.pi)*(UV[0].T@WV[1]-UV[1].T@WV[0])
    z_factor=((2*tf/np.pi)*(2*(3-tf)/np.pi)*(2*(2*tf-3)/np.pi))**.25*np.sqrt(np.pi/(2*tf))
    matrix=z_factor*planar
    singular=np.linalg.svd(matrix,compute_uv=False)
    return {'N':n,'tau':str(tau),'omega':omega,'h_low_Ritz':eh.tolist(),'g_low_Ritz':eg.tolist(),
            'h_full_operator_residuals':rh,'g_full_operator_residuals':rg,
            'geometric_overlap_singular_values':singular.tolist(),'z_overlap_factor':z_factor,
            'meaning':'L2-normalized internal three-mode cubic, overall E8/g7 normalization unspecified; finite-Galerkin evidence, not interval proof'}


def run():
    result={'scope':'nonproportional local Cartan E8 model; net3 spinors with mirrors, not a completed vacuum',
            'E8':root_and_native_checks(),'chambers':[],'overlaps':[]}
    for tau in (s.Rational(1,2),s.Rational(5,4),s.Rational(7,4),s.Rational(5,2)):
        packet=inventory(tau);packet['vacuum']=vacuum_cone(packet)
        packet['gates']=anomaly_and_Yukawa_gates(packet)
        result['chambers'].append(packet)
        print('tau',tau,'net',packet['net_Spin10_spinor_index'],'rays',packet['vacuum']['nonnegative_kernel_extreme_rays'],flush=True)
    for n in (24,40,56):
        overlap=yukawa_overlap(n)
        result['overlaps'].append(overlap)
        print('overlap',n,overlap['geometric_overlap_singular_values'],flush=True)
    result['independent_width_overlap']=yukawa_overlap(96,omega=4.)
    high=result['independent_width_overlap']
    assert min(high['geometric_overlap_singular_values'])>.02
    assert max(high['h_full_operator_residuals']+high['g_full_operator_residuals'])<1e-5
    assert np.max(np.abs(np.array(high['geometric_overlap_singular_values'])-
                         np.array(result['overlaps'][-1]['geometric_overlap_singular_values'])))<1e-8
    result['limitations']=['supplied profiles and tau','H27 common-flavor holonomy not preserved',
        'three mirror16bars and eight10s remain','nonzero Abelian anomalies',
        'zero-FI singlet cone incomplete if extra fields/GS included','noncompact background, gauge constants not L2',
        'no full G2/source action or observed Yukawa predictions']
    path=ROOT/'data/toe_20261119_E8_nonproportional_PW.json'
    path.write_text(json.dumps(result,indent=2,default=lambda v:int(v))+'\n',encoding='utf-8')
    print('PASS',path,flush=True)
    return result


if __name__=='__main__':run()
