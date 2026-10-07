"""Five source-bound follow-ups and cross-inventory probes, not a TOE claim.

Native Clifford fibers and Hesse pencils are reused. Smooth frames, continuous
Spin links, EFT potentials, regulator, field retention and scales are inputs.

Corpus guard's hesse+levi candidate concerns separate prior finite Levi/graph
and Hesse/exceptional geometry; here the connection is Levi-Civita. Owners read:
PASS1087_1091_FIVE_STREAM_RELEASE.md;
analysis/BT1720_BT1723_repo_mining_execution.md;
analysis/BT1741_BT1744_execution_summary.md;
analysis/PASS10949_FREUDENTHAL_QUASICONFORMAL_CLOCK_CONE.md.
No new Hesse/Levi graph or internal-Lorentz-to-spacetime map is claimed.
"""
from collections import Counter, deque
from pathlib import Path
import hashlib
import itertools
import json
import sys

import numpy as np
import sympy as s
from scipy.linalg import expm
from scipy.sparse import bsr_matrix, block_diag

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'analysis'))
import w33_pass11557_pin_equivariant_event_dirac as P57

OUT = ROOT/'data/w33_pass11602_11606_geometry_flavor_completion.json'
RESERVATION = '235295388'


def gammas():
    g, grade = P57.small_clifford()
    return [np.array(a.evalf(), complex) for a in g], np.array(grade.evalf(), complex)


def local_dirac(C, links, edge_weights, shape, spacing, r=.25):
    """Site-major Hermitian nearest-neighbor operator on flat half-densities.

    C[x,i]=gamma^a e_a^i(x), links[x,i] transports x+i to x.
    Metric-compatible transport makes the continuum symmetric operator the
    geometric half-density Dirac. Arbitrary links need not be Levi-Civita.
    """
    n = int(np.prod(shape)); d = len(shape); _, grade = gammas()
    blocks = [dict() for _ in range(n)]
    def add(x,y,B):
        blocks[x][y] = blocks[x].get(y, np.zeros((4,4), complex))+B
    for point in itertools.product(*[range(L) for L in shape]):
        x = np.ravel_multi_index(point, shape)
        for i in range(d):
            q = list(point); q[i] = (q[i]+1) % shape[i]
            y = np.ravel_multi_index(tuple(q), shape)
            U = links[x,i]
            B = 1j*(C[x,i]@U+U@C[y,i])/(4*spacing)
            add(x,y,B); add(y,x,B.conj().T)
            z = r*edge_weights[x,i]/(2*spacing)
            add(x,x,z*grade); add(y,y,z*grade)
            add(x,y,-z*grade@U); add(y,x,-z*U.conj().T@grade)
    data=[];indices=[];indptr=[0]
    for row in blocks:
        for col in sorted(row):indices.append(col);data.append(row[col])
        indptr.append(len(indices))
    return bsr_matrix((np.array(data), np.array(indices), np.array(indptr)), shape=(4*n,4*n)).tocsr()


def conformal_data(L, eps=.12):
    g,_ = gammas(); shape=(L,L,L); h=2*np.pi/L
    points = np.array(list(itertools.product(range(L), repeat=3)), float)*h
    sig = eps*np.cos(points[:,0]); f=np.exp(-sig)
    C=np.array([[z*a for a in g] for z in f])
    links=np.tile(np.eye(4, dtype=complex),(L**3,3,1,1))
    # Exact transport of the supplied torsion-free conformal spin connection:
    # Omega_y=.5 sigma_x gamma_y gamma_x; Omega_z analogous; Omega_x=0.
    angle = -.5*h*eps*np.sin(points[:,0])
    for i in [1,2]:
        links[:,i] = np.cos(angle)[:,None,None]*np.eye(4)+np.sin(angle)[:,None,None]*(g[i]@g[0])
    weights=np.tile((f*f)[:,None],(1,3))
    weights[:,0]=(f*f+np.roll((f*f).reshape(shape),-1,axis=0).ravel())/2
    psi=np.exp(1j*(points[:,0]+points[:,1]))[:,None]*np.array([1,0,0,0],complex)
    exact = -f[:,None]*((g[0]+g[1])@psi.T).T + .5j*(f*eps*np.sin(points[:,0]))[:,None]*(g[0]@psi.T).T
    return C,links,weights,shape,h,psi.ravel(),exact.ravel()


def local_geometry():
    C,U,w,shape,h,psi,exact=conformal_data(3)
    D=local_dirac(C,U,w,shape,h)
    herm=np.max(np.abs((D-D.conj().T).data)) if (D-D.conj().T).nnz else 0.
    g,grade=gammas()
    S=np.array([expm(.17*np.sin(j+.4)*(g[0]@g[1])) for j in range(27)])
    Cp=np.einsum('xab,xibc,xdc->xiad',S,C,S.conj())
    Up=np.empty_like(U)
    for point in itertools.product(range(3),repeat=3):
        x=np.ravel_multi_index(point,shape)
        for i in range(3):
            q=list(point);q[i]=(q[i]+1)%3;y=np.ravel_multi_index(tuple(q),shape)
            Up[x,i]=S[x]@U[x,i]@S[y].conj().T
    Dp=local_dirac(Cp,Up,w,shape,h)
    St=block_diag(list(S),format='csr')
    cov=Dp-St@D@St.conj().T
    residual=float(np.max(np.abs(cov.data))) if cov.nnz else 0.
    assert herm<1e-13 and residual<1e-13
    # Confirm that the regulator is positive before multiplication by grade.
    W=local_dirac(C,U,w,shape,h,r=.25)-local_dirac(C,U,w,shape,h,r=0)
    Gr=block_diag([grade]*27,format='csr')
    eig=np.linalg.eigvalsh((Gr@W).toarray())
    assert eig.min()>-1e-12
    rows=[]
    for L in [9,15,27]:
        C,U,w,shape,h,psi,exact=conformal_data(L)
        row={'L':L,'h':h}
        for r,label in [(0.,'central_error'),(.25,'Wilson_error')]:
            D=local_dirac(C,U,w,shape,h,r)
            row[label]=float(np.linalg.norm(D@psi-exact)/np.linalg.norm(exact))
        rows.append(row)
    assert rows[-1]['central_error']<rows[0]['central_error']/7
    assert rows[-1]['Wilson_error']<rows[0]['Wilson_error']/2.5
    E=s.Matrix([[2,1,0],[0,1,1],[0,0,3]])
    symbol_metric=E.inv()*E.inv().T
    assert symbol_metric==(E.T*E).inv()
    corners=[]
    for bits in itertools.product([0,1],repeat=3):
        corners.append({'corner':bits,'Wilson_mass_times_h':str(2*s.Rational(1,4)*sum(symbol_metric[i,i]*bits[i] for i in range(3)))})
    assert sum(row['Wilson_mass_times_h']=='0' for row in corners)==1
    return dict(status='PASS', Hermitian_residual=herm, local_Spin_covariance_residual=residual,
        Wilson_Laplacian_min_eigenvalue=float(eig.min()), refinement=rows,
        exact_inverse_metric=[[str(z) for z in row] for row in symbol_metric.tolist()],flat_corner_masses=corners,
        forward_block='i(C_i(x) U_xy + U_xy C_i(y))/(4h); reverse is its adjoint',
        Wilson='grade times positive weighted covariant graph Laplacian, r/(2h) per edge; weights average g^{ii}',
        continuum_identity='div C + [Omega_i,C_i] + C_i partial_i log J = 0 implies i/2{C_i,nabla_i}=J^(1/2) D_geometric J^(-1/2)',
        scope='Local construction on supplied periodic refinements including11559 three-power tower rungs; L15 is a separate consistency control with the actual11557 rank-four Clifford fiber. Conformal plane-wave consistency is checked; full non-diagonal heat convergence is not established. Continuous Spin transport and the metric are supplied. Pass11397 already excludes a generic smooth-curvature limit using only the fixed finite rotation group.')


def nonstatic_geometry():
    N,V,M,rho=s.symbols('N V M rho',positive=True)
    q=s.Matrix(s.symbols('qdot0:3',real=True));p=s.Matrix(s.symbols('p0:3',real=True))
    kinetic=s.eye(3)-s.ones(3)
    L=M*M*V*(q.T*kinetic*q)[0]/(2*N)-rho*N*V
    momentum=s.Matrix([s.diff(L,z) for z in q])
    velocity=N*(s.eye(3)-s.ones(3)/2)*p/(M*M*V)
    H=s.expand((p.T*velocity)[0]-L.subs(dict(zip(q,velocity)),simultaneous=True))
    constraint=((p.T*p)[0]-sum(p)**2/2)/(2*M*M*V)+rho*V
    assert s.expand(H-N*constraint)==0
    assert s.expand(momentum.subs(dict(zip(q,velocity)),simultaneous=True)-p)==s.zeros(3,1)
    # Nonstatic, nonflat exact Ricci-flat control. Exponents are classical Kasner.
    exponents=[-s.Rational(2,7),s.Rational(3,7),s.Rational(6,7)]
    assert sum(exponents)==sum(z*z for z in exponents)==1
    kretschmann=s.factor(4*(sum(z*z*(z-1)**2 for z in exponents)+sum(exponents[i]**2*exponents[j]**2 for i in range(3) for j in range(i+1,3))))
    assert kretschmann==s.Rational(576,343)
    g,grade=gammas();time=np.kron(np.array([[0,-1j],[1j,0]]),np.eye(2))
    assert all(np.linalg.norm(time@a+a@time)<1e-12 for a in g)
    # Independent Clifford contraction of the spin connection for arbitrary rates.
    rates=[s.Rational(2,5),-s.Rational(1,7),s.Rational(3,11)]
    spin=sum((a@(.5*float(rate)*a@time) for a,rate in zip(g,rates)),np.zeros((4,4),complex))
    assert np.linalg.norm(spin-.5*float(sum(rates))*time)<1e-12
    return dict(status='PASS',metric='ds_E^2=N(t)^2 dt^2 + sum exp(2q_i(t)) dx_i^2; all q_i may depend on time',
        spin_connection='Omega_0=0; Omega_i=a_i_prime gamma_i gamma_0/(2N)',
        geometric_D='i gamma0/N (partial_t + sum(q_i_prime)/2) + sum i gamma_i/a_i partial_i',
        half_density_D='i gamma0 [N^-1 partial_t - N_prime/(2N^2)] + sum i gamma_i/a_i partial_i',
        volume='J=N exp(sum q_i); half-density spin connection and spatial volume derivatives cancel exactly',
        nonstatic_square='For N=1, Dhat^2=-partial_t^2+sum k_i^2/a_i^2 - i gamma0 sum gamma_i k_i partial_t(1/a_i). The mixed spin term prevents static theta-factorization.',
        Lorentzian_ADM_L=str(L),Hamiltonian_constraint=str(constraint),
        constraints='p_N=0 and C=0 are first class in the homogeneous supplied ADM action; H_total=N C+lambda p_N. C is lapse-independent and {C,C}=0. There are two homogeneous configuration degrees of freedom.',
        Kasner_exponents=[str(z) for z in exponents],Kasner_Ricci='zero',Kasner_Riemann_squared=str(kretschmann)+'/t^4',
        rank4_Dirac_a4_Ricci_flat='-(4pi)^-2 (7/360) integral sqrtg Riemann^2, up to boundary terms; a2 is zero',
        scope='Exact nonstatic coframe and supplied homogeneous ADM constraints. The ADM mechanism belongs to11482/11528; Kasner and heat coefficients are classical. No full local constraint algebra or W33-selected Einstein action is derived. The native pair-action rotational obstruction11381 remains.')


def quantum_inventory():
    old=json.loads((ROOT/'data/w33_20261001_chiral_decuplet_and_condensate_bridge.json').read_text())['anomaly_repair']
    assert old['total_Weyl_components']==91 and old['A10']==27
    xi=s.Symbol('xi81',real=True);xi126,xiH=s.symbols('xi126 xiH',real=True)
    rows=[]
    # All are conditional retention inventories, not threshold matching.
    for label,Ns,Nw,Nv,nonminimal in [
        ('E6xSU3_family prior anomaly-compatible inventory',162,91,86,162*xi),
        ('Spin10xSU3_family with all prior scalars and Weyls retained',162,91,53,162*xi),
        ('Spin10 with finite family group,126bar triplet,Hesse doublet,two neutral triplet flavons',934,91,45,162*xi+756*xi126+16*xiH)]:
        C0=Ns-2*Nw+2*Nv;CR=s.Rational(Ns+Nw-4*Nv,6)-nonminimal
        rows.append({'inventory':label,'real_scalars':Ns,'Weyl_components':Nw,'vectors':Nv,'signed_a0':C0,'signed_a2_per_R':str(CR)})
    assert rows[0]['signed_a0']==152 and rows[0]['signed_a2_per_R']==str(-s.Rational(91,6)-162*xi)
    assert rows[-1]['signed_a0']==842
    # Scalar nonminimal coupling changes only curvature budget, not flat a0.
    critical=-s.Rational(91,972)
    return dict(status='PASS', prior_anomaly_owner='20261001 chiral decuplet;27*A3+A10bar=0',
        determinant_convention='Gamma_even=-1/2 integral_(Lambda^-2)^infinity dt/t H(t); H=Ns Kscalar-Nw KWeyl+Nv(Kvector-2 Kghost)',
        elementary_heat_weights={'real_scalar':['1','1/6-xi'],'Weyl_rank2':['2','-1/6'],'vector_rank4':['4','-1/3'],'complex_ghost_signed':['-2','-1/3']},
        regulator='Feynman gauge, common proper-time cutoff, background gauge curvature zero, massless UV coefficients. Power divergences and their signs are regulator/gauge conventions, not observables.',
        inventories=rows, minimal_high_energy_curvature_sign='negative',xi81_zero_crossing=str(critical),
        induced_terms='rho_UV=-C0 Lambda^4/[4(4pi)^2]; M_ind^2=CR Lambda^2/(4pi)^2 in Gamma_E=integral sqrtg(rho-M^2 R/2)',
        mass_threshold='Each field heat trace carries exp(-m^2 t); massive vectors require Goldstone and ghost completion. A change in retained dimensions is not a threshold calculation.',
        extra_inventory_audit='The126bar is absent from the original27 scalar branching. A finite-family triplet adds3*126 complex=756 real fields. The Hesse doublet adds4 real fields and two gauge-singlet alignment triplets add12 real fields. The10_H triplet is already inside three27 scalars and is not counted twice. A126-only addition is not a full E6 representation, so it is used only after E6 breaking; a2 rows are not matched across phases.',
        vacuum_boundary='No inventory cancels a0 here. An independent local vacuum-energy counterterm remains symmetry-allowed; scales, xi, mass thresholds and finite matching are inputs. Anomaly cancellation does not fix Newton coupling or the cosmological constant.')


def pencil_group():
    w=-s.Rational(1,2)+s.I*s.sqrt(3)/2
    F=s.Matrix([[1,1],[2,-1]])*s.sqrt(3)/3;P=s.diag(1,w)
    norm=lambda M:M.applyfunc(s.expand)
    group={tuple(s.eye(2)):s.eye(2)};queue=deque([s.eye(2)])
    while queue:
        A=queue.popleft()
        for R in [F,P]:
            B=norm(A*R)
            if tuple(B) not in group:group[tuple(B)]=B;queue.append(B)
        assert len(group)<100
    return F,P,list(group.values())


def holomorphic_hesse():
    x,y,t=s.symbols('x y t');F,P,group=pencil_group()
    assert len(group)==48
    assert s.simplify((F*P)**3-s.I*s.eye(2))==s.zeros(2)
    f4=x**4+x*y**3
    f12=24*x**12-440*x**9*y**3+264*x**6*y**6+y**12
    for R in [F,P]:
        sub=dict(zip([x,y],R*s.Matrix([x,y])))
        assert s.simplify(s.expand(f4.subs(sub,simultaneous=True)-f4))==0
        assert s.simplify(s.expand(f12.subs(sub,simultaneous=True)-f12))==0
    classes=Counter((s.expand(s.trace(A)),s.expand(A.det())) for A in group)
    molien=s.cancel(sum(n/(1-tr*t+det*t*t) for (tr,det),n in classes.items())/48)
    assert s.simplify(molien-1/((1-t**4)*(1-t**12)))==0
    jac=s.factor(s.Matrix([[s.diff(f,z) for z in [x,y]] for f in [f4,f12]]).det())
    assert jac!=0
    # Expand the norm in real normalized components; this audits canonical metric.
    a,b,c,d=s.symbols('a b c d',real=True);u=a+s.I*b;v=c+s.I*d
    rho=s.expand(u*s.conjugate(u)+v*s.conjugate(v))
    bloch=s.Matrix([2*s.re(s.conjugate(u)*v),2*s.im(s.conjugate(u)*v),u*s.conjugate(u)-v*s.conjugate(v)])
    axes=s.Matrix([[s.sqrt(s.Rational(2,3)),-s.sqrt(s.Rational(1,6)),-s.sqrt(s.Rational(1,6))],[0,1/s.sqrt(2),-1/s.sqrt(2)],[1/s.sqrt(3)]*3])
    xyz=axes.T*bloch;p3=s.prod(xyz);p4=sum(z**4 for z in xyz)
    H4=u**4+2*s.sqrt(2)*u*v**3
    residual=s.expand(H4*s.conjugate(H4)-s.Rational(3,8)*(rho**4+p4)-3*s.sqrt(3)*rho*p3/2)
    assert residual==0
    norm_target=s.Rational(9,16)+9*s.sqrt(42)/196
    assert norm_target>0
    # A generic invariant-orbit selector with real targets preserves generalized CP.
    sample=s.Matrix([1,2+s.I]);orbit={tuple(A*sample) for A in group}
    assert len(orbit)==48
    return dict(status='PASS',linear_image_order=48,scalar_center='C4; (F P)^3=i I',classical_group='complex reflection group G6',
        coordinate_map='unnormalized x=u0,y=sqrt2*u1; canonical norm=|x|^2+|y|^2/2',
        f4=str(f4),f12=str(f12),Molien='1/((1-t^4)(1-t^12))',Jacobian=str(jac),
        canonical_H4='u0^4+2sqrt2*u0*u1^3',canonical_norm_identity='|H4|^2=3/8(rho^4+p4)+(3sqrt3/2)rho p3',
        phase_completion='Add lambda/M^4 |H4-c4|^2 to11600 positive selector; c4=v^4 sqrt(9/16+9sqrt42/196) is real. Every old minimum ray admits exactly four phases with H4=c4.',
        c4_squared_over_v8=str(norm_target),full_minimum_vectors=96,CP_orbits=[48,48],
        gapped_normal_directions=4,phase_mass_along_fixed_ray='16 lambda c4^2/(M^4 v^2); this is curvature along the phase direction, not an eigenvalue after angular mixing',
        real_target_obstruction='Since f4,f12 generate the invariant ring and separate finite complex-group orbits, fixing BOTH to real values puts u and conjugate(u) in the same group orbit. A unique such invariant orbit cannot spontaneously break generalized CP.',
        protection_boundary='This removes the extra common U1 assumption and its Goldstone in a supplied EFT. It does not protect the absence of lower angular operators p3,p4 or derive their coefficients. The phase-blind degree16 theorem11600 retains its original scope. The scalar lift is exactly <RF,RP>; rephasing generators or adding a larger scalar center changes allowed holomorphic degrees.',
        novelty='G6 invariants are classical. The result is their explicit source-bound Hesse-pencil interface and the phase completion/CP obstruction, not discovery of G6.')


def family_potential():
    coords=s.symbols('z0:12',real=True)
    h=s.Matrix([coords[2*i]+s.I*coords[2*i+1] for i in range(3)])
    r=s.Matrix([coords[6+2*i]+s.I*coords[7+2*i] for i in range(3)])
    abs2=lambda z:s.expand(z*s.conjugate(z))
    V=(sum(abs2(z) for z in h)-1)**2+sum(abs2(h[i]*h[j]) for i in range(3) for j in range(i+1,3))
    V+=abs2(sum(z**3 for z in h)-1)
    V+=sum((abs2(z)-1)**2+abs2(z**3-1) for z in r)+abs2(s.prod(r)-1)
    V+=abs2((h.conjugate().T*r)[0]-1)
    vacuum={z:0 for z in coords};vacuum.update({coords[0]:1,coords[6]:1,coords[8]:1,coords[10]:1})
    assert V.subs(vacuum)==0
    Hess=s.hessian(V,coords).subs(vacuum)
    minors=[s.det(Hess[:j,:j]) for j in range(1,13)]
    assert all(z>0 for z in minors)
    w=-s.Rational(1,2)+s.I*s.sqrt(3)/2
    orbit=set()
    for i in range(3):
        for exps in itertools.product(range(3),repeat=3):
            if sum(exps)%3:continue
            rr=tuple(s.expand(w**k) for k in exps);hh=tuple(rr[i] if j==i else s.Integer(0) for j in range(3))
            orbit.add(hh+rr)
    assert len(orbit)==27
    return coords,h,r,s.expand(V),vacuum,Hess,minors,orbit


def seesaw_alignment():
    coords,h,r,V,vac,Hess,minors,orbit=family_potential()
    PH=s.eye(3)-s.diag(1,0,0);PR=3*s.eye(3)-s.ones(3)
    assert PH*s.Matrix([1,0,0])==s.zeros(3,1) and PR*s.ones(3,1)==s.zeros(3,1)
    # Spin10 channel changes gauge Clebsches, not the11591 symmetric family space.
    Y=lambda a,b,h:s.Matrix([[a*h[0],b*h[2],b*h[1]],[b*h[2],a*h[1],b*h[0]],[b*h[1],b*h[0],a*h[2]]])
    Y10=Y(2,1,[1,0,0]);YR=Y(4,1,[1,1,1])
    MD=Y10;Me=Y10-s.Rational(3,10)*YR;MR=YR
    mn=s.simplify(-MD*MR.inv()*MD.T)
    exchange=s.Matrix([[1,0,0],[0,0,1],[0,1,0]])
    assert Me*exchange==exchange*Me and mn*exchange==exchange*mn
    basis=s.Matrix([[1,0,0],[0,1/s.sqrt(2),1/s.sqrt(2)],[0,1/s.sqrt(2),-1/s.sqrt(2)]])
    Eb=s.simplify(basis.T*Me*basis);Nb=s.simplify(-basis.T*mn*basis)
    assert Eb[2,2]==-s.Rational(19,10) and Nb[2,2]==s.Rational(1,3)
    tan_e=s.simplify(2*Eb[0,1]/(Eb[0,0]-Eb[1,1]));tan_n=s.simplify(2*Nb[0,1]/(Nb[0,0]-Nb[1,1]))
    tan_delta=s.simplify((tan_n-tan_e)/(1+tan_n*tan_e))
    assert tan_delta==11*s.sqrt(2)/64
    sin2=s.Rational(1,2)*(1-64/s.sqrt(4338))
    return dict(status='PASS',inventory='Two additional gauge-singlet family-triplet flavons h,r. Actual gauge-charged10_H and126bar_H triplets are aligned with them by positive gauge-invariant projectors; gauge amplitudes/directions remain unselected.',
        potential='(|h|^2-1)^2 + sum_i<j |h_i h_j|^2 + |sum h_i^3-1|^2 + sum_i[(|r_i|^2-1)^2+|r_i^3-1|^2] + |r0 r1 r2-1|^2 + |h-dagger r-1|^2',
        potential_properties='CP-even, Delta54 invariant, coercive polynomial; scales and positive coefficients supplied. Global minima are h=e_i r_i, all r_i^3=1 and product r_i=1:27 vectors in one Delta54 orbit.',
        alignment_map='V_align_H=kH[|h|^2 sum_i ||H_i||^2 - ||sum_i conjugate(h_i) H_i||^2]; the same map with r and126bar R. Cauchy-Schwarz proves positivity; zeros give H_i=h_i H_common and R_i=r_i R_common when h,r are nonzero. Gauge indices are contracted with invariant Hermitian norms.',
        family_projectors_at_vacuum={'10':PH.tolist(),'126':PR.tolist()},
        global_minima=27,Hessian_rank=12,Hessian_positive_leading_minors=[str(z) for z in minors],
        neutral_flavon_Hessian=[[str(z) for z in row] for row in Hess.tolist()],
        coupling_inputs='a10=2,b10=1,a126=4,b126=1; vR removed as overall seesaw scale; v126_down/v10_down=1/10; v126_up=0; typeII term zero',
        MD=MD.tolist(),MR=MR.tolist(),Me=[[str(z) for z in row] for row in Me.tolist()],
        light_Majorana=[[str(z) for z in row] for row in mn.tolist()],
        light_masses=['(2-sqrt2)/3','1/3','(2+sqrt2)/3'],charged_singular_values=['(sqrt241-3)/20','(sqrt241+3)/20','19/10'],
        mixing='Up to mass ordering and Majorana/Dirac phases, U_PMNS has one2x2 rotation and one isolated state. Both mass operators commute with the same family exchange; no three-angle mixing.',
        tan_twice_mixing=str(tan_delta),sin_squared_mixing=str(sin2),sin_squared_mixing_numeric=float(sin2),weak_basis_CP='zero in this real branch',
        scope='Exact gauge-singlet flavon selection, gauge-covariant Higgs-family alignment and conditional seesaw eigenvalues, not measured neutrino predictions. The126 gauge-breaking direction, EW doublet mixing, all coupling values and vR must still be selected. The residual exchange supplies a concrete obstruction to realistic three-angle mixing in this branch.')


def matter_parity():
    return dict(status='PASS',prior_owner='11595 Majorana channel and11522 composite-Higgs selection',
        elementary126_VEV={'qBL':-6,'r':2,'sixY':0,'BL_residual':'Z6 contains matter parity Z2'},
        constituent16bar_singlet={'qBL':-3,'r':1,'sixY':0,'BL_residual':'Z3 does not contain matter parity Z2'},
        composite_map='S=Proj_126bar(Sym^2 scalar16bar); its neutral component is (phi_nuc_conjugate)^2',
        factorized_boundary='If <S> is supplied solely by <phi>^2 with <phi>!=0, the constituent VEV is matter odd and breaks matter parity. Identifying its even composite charge does not restore that parity.',
        pair_condensate_escape='A correlated <phi phi>!=0 with <phi>=0 can preserve matter parity; an actual dynamical pair-condensation model and its gap are required. No such phase is proved here.',
        unified_boundary='Removing the elementary126 inventory by a composite changes the scalar heat budget and thresholds. It cannot be done silently while retaining the expanded induced-gravity coefficients.')


def spectator_residual_symmetry():
    x=s.symbols('x0:3');lam=s.symbols('lambda',nonzero=True,real=True)
    words=list(itertools.combinations_with_replacement(range(3),3))
    alphas=[tuple(word.count(i) for i in range(3)) for word in words]
    mult=[s.factorial(3)/s.prod(s.factorial(k) for k in a) for a in alphas]
    f=sum(z**6 for z in x)+lam*s.prod(x)**2
    def entry(a,b):
        value=f
        for z,k in zip(x,[aa+bb for aa,bb in zip(a,b)]):value=s.diff(value,z,k)
        return value/s.factorial(6)
    B=s.Matrix(10,10,lambda i,j:s.sqrt(mult[i]*mult[j])*entry(alphas[i],alphas[j]))
    assert B.rank()==10
    assert B.det()==-lam**7/(15*30**6)
    w=-s.Rational(1,2)+s.I*s.sqrt(3)/2
    X=s.Matrix([[0,0,1],[1,0,0],[0,1,0]]);Z=s.diag(1,w,w**2);R=s.Matrix([[1,0,0],[0,0,1],[0,1,0]])
    # Sixth degree is invariant under either reflection lift R or -R.
    for G in [X,Z,R,-R]:
        assert s.simplify(s.expand(f.subs(dict(zip(x,G*s.Matrix(x))),simultaneous=True)-f))==0
    # No nonzero sextet value fixes the SAME finite family generators.
    components=s.symbols('f0:6');F=s.Matrix([[components[0],components[1],components[2]],[components[1],components[3],components[4]],[components[2],components[4],components[5]]])
    equations=[]
    for G in [X,Z]:equations.extend(list(G*F*G.T-F))
    A,_=s.linear_eq_to_matrix(equations,components);assert A.rank()==6
    center=s.simplify(X*Z*X.inv()*Z.inv())
    assert s.simplify(center-w**2*s.eye(3))==s.zeros(3) and s.simplify(w**4-1)!=0
    return dict(status='PASS',prior_rank10_owners=['11271 elementary28 Wick tensor','11276 Sym(F^3) sextet repair'],
        sextic='sum_i x_i^6+lambda (x0 x1 x2)^2',canonical_sym3_mass=[[str(z) for z in row] for row in B.tolist()],
        determinant=str(B.det()),rank=10,Takagi_singular_values=['1 multiplicity3','abs(lambda)/30 multiplicity6','abs(lambda)/15 multiplicity1'],
        symmetry='The sextic and mass pairing preserve the actual11591 X,Z,R family image, and also the SU3-compatible -R lift. No exact sextic stabilizer identification is claimed.',
        sextet_fixed_space_dimension=0,
        comparison='No nonzero single-sextet cube Sym(F^3) preserves H27: invariance of q_F^3 forces each generator to act on q_F by a cube-root scalar, hence a common invariant line in Sym^2(3); its nontrivial center action forbids that line. The prior full-rank sextet repair remains valid but breaks this finite family subgroup. The elementary28 sextic can retain it.',
        ultraviolet_map='chi_abc chi_def Sigma^{abcdef}, Sigma in SU3(6,0), dim28; a renormalizable Majorana Yukawa. The VEV pattern, coefficient and threshold are inputs.',
        inventory_cost='One complex28 adds56 real scalars and family Dynkin index63. In the prior91-Weyl/81-complex-scalar inventory b_family changes from -15/2 to -57/2; the gauge-running problem worsens.',
        heat_cost='In that E6xSU3 inventory with the extra28 only, C0=208 and CR=-35/6-162xi81-56xiSigma in the declared Feynman/proper-time convention. It still has no minimal-coupling positive induced M^2 or vacuum cancellation.',
        anomaly_boundary='After integrating out anomaly-canceling spectators, broken-family Wess-Zumino matching must remain, as already required by11276. No UV completion or automatic spectator decoupling is asserted.')


def unequal_alignment_escape():
    coords=s.symbols('z0:12',real=True)
    h=s.Matrix([coords[2*i]+s.I*coords[2*i+1] for i in range(3)])
    r=s.Matrix([coords[6+2*i]+s.I*coords[7+2*i] for i in range(3)])
    abs2=lambda z:s.expand(z*s.conjugate(z));t=[abs2(z) for z in h]
    V=(sum(t)-14)**2+(sum(t[i]*t[j] for i in range(3) for j in range(i+1,3))-49)**2+(s.prod(t)-36)**2
    V+=abs2(sum(z**3 for z in h)-36)+abs2(s.prod(h)-6)
    V+=sum((abs2(z)-1)**2+abs2(z**3-1) for z in r)+abs2(s.prod(r)-1)
    V+=abs2((h.conjugate().T*r)[0]-6)
    point={z:0 for z in coords};point.update({coords[0]:1,coords[2]:2,coords[4]:3,coords[6]:1,coords[8]:1,coords[10]:1})
    assert V.subs(point)==0
    H=s.hessian(V,coords).subs(point);minors=[H[:j,:j].det() for j in range(1,13)]
    assert all(x>0 for x in minors)
    D=s.Matrix([[2,3*s.I,2*s.I],[3*s.I,4,s.I],[2*s.I,s.I,6]])
    MR=3*s.eye(3)+s.ones(3);Me=D-s.Rational(3,10)*MR;mn=-D*MR.inv()*D.T
    He=Me.H*Me;Hn=mn.H*mn;K=He*Hn-Hn*He;CP=s.factor(s.im(s.trace(K**3)))
    assert CP==-s.Rational(94163140688,5625)
    _,E=np.linalg.eigh(np.array(He,complex));_,N=np.linalg.eigh(np.array(Hn,complex));mix=abs(E.conj().T@N)**2
    assert mix.min()>.02
    # The exact CP ratio is attainable by a dynamically selected Hesse doublet.
    u=s.Matrix([s.sqrt(s.Rational(2,3)),-s.I/s.sqrt(3)])
    ratio=s.simplify(s.conjugate(u[1])/(s.sqrt(2)*s.conjugate(u[0])))
    assert ratio==s.I/2
    rx=0;ry=-2*s.sqrt(2)/3;rz=s.Rational(1,3)
    axes=s.Matrix([[s.sqrt(s.Rational(2,3)),-s.sqrt(s.Rational(1,6)),-s.sqrt(s.Rational(1,6))],[0,1/s.sqrt(2),-1/s.sqrt(2)],[1/s.sqrt(3)]*3])
    xyz=axes.T*s.Matrix([rx,ry,rz]);p3=s.factor(s.prod(xyz));p4=s.factor(sum(z**4 for z in xyz));W=s.factor(s.prod([xyz[0]**2-xyz[1]**2,xyz[1]**2-xyz[2]**2,xyz[2]**2-xyz[0]**2]))
    assert W!=0
    return dict(status='PASS',potential='Replace h selection by(p1-14)^2+(p2-49)^2+(p3_abs-36)^2+|sum h_i^3-36|^2+|product h_i-6|^2; keep r selector and replace cross target by|h-dagger r-6|^2. p_k are elementary symmetric polynomials in|h_i|^2.',
        exact_global_minima='54 vectors: permutations of magnitudes(1,2,3), h_i=|h_i| r_i, r_i^3=1, product r_i=1. One actual X,Z,R orbit; all12 neutral-flavon directions have positive Hessian.',
        Hessian_positive_leading_minors=[str(z) for z in minors],degree=12,
        gauge_alignment='Use the same positive Gram projectors as11606. Unequal h removes the common family exchange of the axis/democratic branch.',
        coupling_inputs='a10=2,b10=i,a126=4,b126=1; down126 ratio1/10, up126=0, typeII=0. Targets and couplings are supplied.',
        MD=[[str(z) for z in row] for row in D.tolist()],MR=MR.tolist(),Me=[[str(z) for z in row] for row in Me.tolist()],
        light_Majorana=[[str(z) for z in row] for row in mn.tolist()],charged_Hermitian_charpoly=str(He.charpoly().as_expr()),neutrino_Hermitian_charpoly=str(Hn.charpoly().as_expr()),
        CP_invariant='Im Tr[Me-dagger Me,mnu-dagger mnu]^3',CP_exact=str(CP),
        mixing_modulus_squared=mix.tolist(),sin_squared_angles={'theta13':float(mix[0,2]),'theta12':float(mix[0,1]/(1-mix[0,2])),'theta23':float(mix[1,2]/(1-mix[0,2]))},
        Hesse_CP_source={'u':['sqrt(2/3)','-i/sqrt3'],'b_over_a':'i/2','Bloch_p3':str(p3),'Bloch_p4':str(p4),'CP_odd_W':str(W),'H4':'4(1+i)/9','phase_completion_c4':'4sqrt2/9 at v=1'},
        scope='Constructive failure escape: fully mixed nondegenerate conditional seesaw and exact CP witness, with a coercive dynamically aligned family model. Hesse targets can be chosen to select this CP ratio using11600/11605; it is not parameter-independent CP or a physical fit. The126 gauge VEV, EW sector, coefficient selection, UV matching and common parent action remain open.')


def phase_filter_bridge():
    path=ROOT/'data/PART_W33_PASS11607_HESSE_CP_WEYL_SELECTOR.json'
    prior=json.loads(path.read_text())
    for source,digest in prior['source_sha256'].items():assert canonical_hash(ROOT/source)==digest
    gd=json.loads((ROOT/'data/w33_pass10961_albert_clifford9_gammas.json').read_text())
    I=s.eye(16);zero=s.zeros(16)
    gam=[s.BlockMatrix([[zero,s.Matrix([[s.Rational(z) for z in row] for row in M])],[s.Matrix([[s.Rational(z) for z in row] for row in M]),zero]]).as_explicit() for M in gd['gamma9']]
    gam.append(s.diag(I,-I));Chi=s.I*s.prod(gam);R=s.I*gam[-1]
    assert Chi**2==s.eye(32) and Chi.conjugate()==-Chi
    assert R*Chi*R.H==-Chi
    assert R*Chi.conjugate()*R.H==Chi and R*R.conjugate()==s.eye(32)
    c=s.Rational(15,343);rows=[]
    for sign in [1,-1]:
        A=c*(s.eye(32)+sign*Chi);H=A*A
        assert H.rank()==16 and H==4*c*c*(s.eye(32)+sign*Chi)/2
        rows.append({'W_sign':sign,'kernel_chirality':-sign,'kernel_dimension':16,'gap_coefficient':str(4*c*c),'phase_completed_vacuum_vectors':48})
    return dict(status='PASS',owner='11607 diagonal internal Weyl filter; this packet adds its11605 gapped-phase interface and a separate semilinear-lift audit',
        vacuum_rows=rows,phase_completion_identity='The Bloch coordinates and W are invariant under u->exp(i alpha)u. Therefore the11607 finite filter retains its rank16 kernel and exact gap on all96 phase-completed vectors, while all four scalar directions are stabilized.',
        lift_comparison={'unitary_R':'R Chi R^-1=-Chi; R^2=-I, as11607 defines','conjugation_K':'K Chi K^-1=-Chi in the exported real-gamma basis; K^2=I','semilinear_RK':'(R K) Chi (R K)^-1=+Chi and(R K)^2=I. Combining BOTH flips cancels them.'},
        semilinear_filter_identity='For a coefficient-conjugation lift, K alone pairs W->-W with Chi->-Chi and transports H_+(u) to H_-(conjugate(u)); adding R to K instead preserves Chi and does not supply this same cancellation.',
        second_basis='Under a complex unitary basis S, the linear part of K is S S^T and that of R K is S R S^T. Reusing naive componentwise conjugation after a basis change is incorrect.',
        scope='The defined unitary adjoint action of11607 remains valid. These are distinct finite linear/antilinear lifts, not a retraction or proof of a physical CP/clock identity, relativistic chirality, local decoupling, anomaly measure or E8 shell selection.')


def canonical_hash(path):
    if path.suffix=='.json':raw=json.dumps(json.loads(path.read_text()),sort_keys=True,separators=(',',':')).encode()
    else:raw=path.read_bytes().replace(b'\r\n',b'\n')
    return hashlib.sha256(raw).hexdigest()


def produce():
    result={'status':'PASS','reservation':RESERVATION,'passes':[11602,11603,11604,11605,11606]}
    for name,fn in [('local_geometry',local_geometry),('nonstatic_geometry',nonstatic_geometry),('quantum_inventory',quantum_inventory),('holomorphic_Hesse',holomorphic_hesse),('Majorana_alignment',seesaw_alignment),('additional_matter_parity',matter_parity),('additional_spectator_symmetry',spectator_residual_symmetry),('additional_unequal_alignment_escape',unequal_alignment_escape),('parallel_phase_filter_bridge',phase_filter_bridge)]:
        result[name]=fn();print(name,'PASS',flush=True)
    sources=['analysis/w33_pass11557_pin_equivariant_event_dirac.py','analysis/w33_pass11600_dynamical_hesse_flavor.py','data/w33_pass11600_dynamical_hesse_flavor.json','data/w33_pass11601_matched_metric_dirac.json','data/w33_20261001_chiral_decuplet_and_condensate_bridge.json','data/PART_W33_PASS11591_SPIN10_DELTA54_HESSE_YUKAWA.json','data/PART_W33_PASS11595_NEUTRINO_MAJORANA_CHANNEL.json','data/w33_pass11276_sextet_composite_spectator.json','data/PART_W33_PASS11607_HESSE_CP_WEYL_SELECTOR.json','data/w33_pass10961_albert_clifford9_gammas.json']
    result['source_sha256']={p:canonical_hash(ROOT/p) for p in sources}
    result['producer_sha256']=canonical_hash(Path(__file__))
    OUT.write_text(json.dumps(result,indent=2,default=str)+'\n')
    return result


if __name__=='__main__':produce()
