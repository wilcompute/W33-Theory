"""Five genus-six followups: surface chains, periods, surgery, oscillators, Pauli ABI.
Sources: Lutz manifold_2_12_4_5; Tadokoro arXiv:1211.6910;
prior w33_k12_genus_polarization, singular_css_closure, Holotrade b63daac.
Finite mathematical models; no physical calibration or canonical curve selection.
"""
from pathlib import Path
from collections import defaultdict, deque
from itertools import combinations, product
import hashlib
import json
import numpy as np
import sympy as s
import mpmath as mp
from scipy.integrate import solve_ivp
from scipy.linalg import expm
from w33_k12_genus_polarization import darboux, integral

ROOT = Path(__file__).resolve().parents[1]
# Frank Lutz catalogue, manifold_2_12_4_5, relabeled from 1..12 to 0..11.
# https://www3.math.tu-berlin.de/IfM/Nachrufe/Frank_Lutz/stellar/2_manifolds.txt
FACETS_ONE = [[1,2,4],[1,2,7],[1,3,8],[1,3,12],[1,4,11],[1,5,9],[1,5,11],[1,6,10],[1,6,12],[1,7,8],[1,9,10],[2,3,5],[2,3,6],[2,4,8],[2,5,12],[2,6,10],[2,7,9],[2,8,10],[2,9,11],[2,11,12],[3,4,7],[3,4,9],[3,5,8],[3,6,11],[3,7,11],[3,9,10],[3,10,12],[4,5,6],[4,5,10],[4,6,9],[4,7,12],[4,8,12],[4,10,11],[5,6,8],[5,7,10],[5,7,11],[5,9,12],[6,7,9],[6,7,12],[6,8,11],[7,8,10],[8,9,11],[8,9,12],[10,11,12]]
TORUS_ONE = [[1,2,4],[1,2,6],[1,3,4],[1,3,7],[1,5,6],[1,5,7],[2,3,5],[2,3,7],[2,4,5],[2,6,7],[3,4,6],[3,5,6],[4,5,7],[4,6,7]]

def incidence(faces):
    ef = defaultdict(list)
    for i,f in enumerate(faces):
        for a,b in zip(f,f[1:]+f[:1]):
            ef[tuple(sorted((a,b)))].append((i,1 if a<b else -1))
    return ef

def orient(faces):
    faces=[tuple(sorted(f)) for f in faces]
    ef=incidence(faces)
    if any(len(x)!=2 for x in ef.values()): raise ValueError('edge is not two-sided')
    adj=defaultdict(list)
    for (i,a),(j,b) in ef.values():
        adj[i].append((j,-a*b));adj[j].append((i,-a*b))
    signs={0:1}; queue=[0]
    while queue:
        i=queue.pop()
        for j,t in adj[i]:
            want=signs[i]*t
            if j in signs:
                if signs[j]!=want: raise ValueError('nonorientable')
            else: signs[j]=want;queue.append(j)
    if len(signs)!=len(faces): raise ValueError('disconnected face dual')
    return [f if signs[i]==1 else (f[0],f[2],f[1]) for i,f in enumerate(faces)]

def validate_surface(faces):
    if len({tuple(sorted(f)) for f in faces})!=len(faces): raise ValueError('duplicate face')
    vertices=sorted(set(sum((list(f) for f in faces),[])))
    if any(len(set(f))!=3 for f in faces): raise ValueError('degenerate face')
    faces=orient(faces); ef=incidence(faces)
    for v in vertices:
        adj=defaultdict(set)
        for f in faces:
            if v in f:
                a,b=[w for w in f if w!=v];adj[a].add(b);adj[b].add(a)
        if any(len(x)!=2 for x in adj.values()): raise ValueError('link is not degree two')
        seen=set(); queue=[min(adj)]
        while queue:
            a=queue.pop()
            if a in seen:continue
            seen.add(a);queue.extend(adj[a]-seen)
        if len(seen)!=len(adj):raise ValueError('disconnected vertex link')
    chi=len(vertices)-len(ef)+len(faces)
    assert (2-chi)%2==0
    return {'V':len(vertices),'E':len(ef),'F':len(faces),'genus':(2-chi)//2}

def rank_mod(M,p):
    A=np.array(M,dtype=np.int64)%p; r=0
    for c in range(A.shape[1]):
        k=next((i for i in range(r,len(A)) if A[i,c]),None)
        if k is None:continue
        A[[r,k]]=A[[k,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
        for i in range(len(A)):
            if i!=r:A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
        if r==len(A):break
    return r

def surface_chains():
    faces=orient([tuple(x-1 for x in f) for f in FACETS_ONE])
    topo=validate_surface(faces);assert topo==dict(V=12,E=66,F=44,genus=6)
    edges=sorted(incidence(faces));ei={e:i for i,e in enumerate(edges)}
    d1=s.zeros(12,66);d2=s.zeros(66,44)
    for j,(a,b) in enumerate(edges):d1[a,j]=-1;d1[b,j]=1
    for j,f in enumerate(faces):
        for a,b in zip(f,f[1:]+f[:1]):d2[ei[tuple(sorted((a,b)))],j]=1 if a<b else -1
    assert d1*d2==s.zeros(12,44)
    # K12 permits the star at zero as a primal spanning tree.
    tree=[ei[(0,v)] for v in range(1,12)]
    chords=[i for i in range(66) if i not in tree]
    cycles=s.zeros(66,55)
    for j,e in enumerate(chords):
        a,b=edges[e];cycles[e,j]=1;cycles[ei[(0,a)],j]=1;cycles[ei[(0,b)],j]=-1
    assert d1*cycles==s.zeros(12,55)
    ef=incidence(faces);dual=defaultdict(list)
    for e in chords:
        (a,_),(b,_)=ef[edges[e]];dual[a].append((b,e));dual[b].append((a,e))
    seen={0};queue=deque([0]);cotree=[]
    while queue:
        a=queue.popleft()
        for b,e in sorted(dual[a]):
            if b not in seen:seen.add(b);queue.append(b);cotree.append(e)
    assert len(cotree)==43
    free=[e for e in chords if e not in cotree];assert len(free)==12
    R=d2.extract(cotree,list(range(1,44)));assert abs(R.det())==1
    # Coordinates on H1: eliminate face boundaries along the dual spanning tree.
    H=s.zeros(12,66)
    for j,e in enumerate(free):H[j,e]=1
    correction=-d2.extract(free,list(range(1,44)))*R.inv()
    for i in range(12):
        for j,e in enumerate(cotree):H[i,e]=correction[i,j]
    integral(H);assert H*d2==s.zeros(12,44)
    C=cycles[:,[chords.index(e) for e in free]];assert H*C==s.eye(12)
    # Alexander-Whitney cup product on sorted vertices, evaluated on orientation.
    cup=s.zeros(12)
    for f in faces:
        a,b,c=sorted(f);sgn=1 if tuple(f) in [(a,b,c),(b,c,a),(c,a,b)] else -1
        cup+=sgn*H[:,ei[(a,b)]]*H[:,ei[(b,c)]].T
    assert cup.T==-cup and cup.det()==1
    intersection=-cup.inv();S=darboux(intersection)
    standard=s.diag(*([s.Matrix([[0,1],[-1,0]])]*6))
    assert S.T*intersection*S==standard
    Cstd=C*S
    prior=json.loads((ROOT/'analysis/w33_k12_genus_polarization.json').read_text())
    T=s.Matrix(prior['darboux_basis']);E=s.Matrix(prior['eisenstein_alternating_form'])
    lattice_to_cycles=Cstd*T.inv()
    assert d1*lattice_to_cycles==s.zeros(12)
    assert (S*T.inv()).T*intersection*(S*T.inv())==E
    from w33_reye_k12_orientable_horizon_completion import oriented_horizon_faces
    try:validate_surface(oriented_horizon_faces())
    except ValueError as exc:negative=str(exc)
    else:raise AssertionError('old pseudocomplex incorrectly accepted')
    return {'topology':topo,'oriented_faces':faces,'edges':edges,'d1':integral(d1),'d2':integral(d2),
            'homology_projection':integral(H),'cup_matrix':integral(cup),
            'symplectic_cycles':integral(Cstd),'lattice_to_cycles':integral(lattice_to_cycles),
            'dual_tree_minor_determinant':int(R.det()),'betti':[1,12,1],
            'old_reye_negative_control':negative,'source':'Lutz manifold_2_12_4_5'}

def period_model(dps):
    with mp.workdps(dps):
        z=mp.exp(2j*mp.pi/13)
        A=mp.matrix(6,6);B=mp.matrix(6,6)
        for i in range(1,7):
            for j in range(1,7):
                A[i-1,j-1]=z**(i*(2*j-1))-z**(2*i*j)
                B[i-1,j-1]=sum((-1)**(k+1)*z**(i*k) for k in range(2*j))
        tau=A**-1*B
        assert mp.norm(tau-tau.T)<mp.mpf(10)**(-dps+10)
        X=mp.matrix([[mp.re(tau[i,j]) for j in range(6)] for i in range(6)])
        Y=mp.matrix([[mp.im(tau[i,j]) for j in range(6)] for i in range(6)])
        eig=mp.eigsy(Y,eigvals_only=True);assert min(eig)>0
        # Multiplication by i on real period coordinates (a_1..a_6,b_1..b_6).
        P=mp.matrix(12);J0=mp.matrix(12)
        for i in range(6):
            P[i,i]=1;J0[i,6+i]=-1;J0[6+i,i]=1
            for j in range(6):P[i,6+j]=X[i,j];P[6+i,6+j]=Y[i,j]
        J=P**-1*J0*P
        perm=[x for i in range(6) for x in (i,i+6)]
        J=mp.matrix([[J[i,j] for j in perm] for i in perm])
        prior=json.loads((ROOT/'analysis/w33_k12_genus_polarization.json').read_text())
        T=mp.matrix(prior['darboux_basis']);E=mp.matrix(prior['eisenstein_alternating_form'])
        G=mp.matrix(prior['real_gram']);W=mp.matrix(prior['eisenstein_unit'])
        Jlat=T*J*T**-1;metric=E*Jlat
        assert mp.norm(Jlat*Jlat+mp.eye(12))<mp.mpf(10)**(-dps+10)
        assert mp.norm(metric-metric.T)<mp.mpf(10)**(-dps+10)
        assert min(mp.eigsy(metric,eigvals_only=True))>0
        assert mp.norm(Jlat*W-W*Jlat)>1  # old scalar symmetry is not retained
        assert mp.norm(Jlat.T*G*Jlat-G)>1  # original metric is not retained
        return tau,Jlat,float(min(eig)),float(mp.norm(Jlat*W-W*Jlat))

def digest(faces):return hashlib.sha256(json.dumps(faces,sort_keys=True).encode()).hexdigest()

class HandleVM:
    """Classical topology register; allocated handles carry two field coordinates.
    FREE is allowed only for a matching surgery receipt and empty handle state.
    """
    def __init__(self,faces):self.faces=[tuple(f) for f in faces];validate_surface(self.faces);self.stack=[]
    def allocate(self):
        before=list(self.faces);base=orient(before);torus=orient([tuple(x-1 for x in f) for f in TORUS_ONE])
        a,b=base[0],torus[0]
        mapping=dict(zip(b,(a[0],a[2],a[1])))
        fresh=max(sum((list(f) for f in base),[]))+1
        for v in range(7):
            if v not in mapping:mapping[v]=fresh;fresh+=1
        after=base[1:]+[tuple(mapping[x] for x in f) for f in torus[1:]]
        old=validate_surface(before);new=validate_surface(after)
        assert new['genus']==old['genus']+1
        assert [new[k]-old[k] for k in ['V','E','F']]==[4,18,12]
        self.faces=after;self.stack.append({'before':before,'after_hash':digest(after),'state':[0,0]})
        return new
    def write(self,a,b,p=3):
        if not self.stack:raise ValueError('no allocated handle')
        self.stack[-1]['state']=[a%p,b%p]
    def free(self):
        if not self.stack:raise ValueError('no surgery receipt')
        r=self.stack[-1]
        if digest(self.faces)!=r['after_hash']:raise ValueError('topology changed since allocation')
        if any(r['state']):raise ValueError('live handle state would be discarded')
        validate_surface(r['before']);self.faces=r['before'];self.stack.pop()

def surgery_audit(faces):
    vm=HandleVM(faces);original=digest(vm.faces);trace=[validate_surface(vm.faces)]
    for _ in range(3):trace.append(vm.allocate())
    vm.write(1,2)
    try:vm.free()
    except ValueError:live=True
    else:raise AssertionError('live deletion accepted')
    vm.write(0,0);saved=vm.faces[0];vm.faces[0]=(99,98,97)
    try:vm.free()
    except ValueError:tamper=True
    else:raise AssertionError('modified topology accepted')
    vm.faces[0]=saved
    for _ in range(3):vm.free();trace.append(validate_surface(vm.faces))
    assert digest(vm.faces)==original
    return {'trace':trace,'live_state_rejected':live,'tamper_rejected':tamper,'exact_roundtrip':True,
            'instruction_delta':[4,18,12],'scope':'connected sum with a seven-vertex torus; not fixed-vertex JR handle subtraction'}

def oscillator_audit():
    lines=[(0,1,3),(0,2,5),(0,4,6),(1,2,4),(1,5,6),(2,3,6),(3,4,5)]
    F=np.zeros((7,7))
    for j,L in enumerate(lines):F[list(L),j]=1
    A=np.block([[np.zeros((7,7)),F],[F.T,np.zeros((7,7))]])
    P=(9*np.eye(14)-A@A)/7;L=3*np.eye(14)-A
    v=P[:,0];v/=np.linalg.norm(v);times=np.linspace(0,20,101)
    sol=solve_ivp(lambda t,y:np.r_[y[14:],-L@y[:14]],(0,20),np.r_[v,np.zeros(14)],t_eval=times,rtol=1e-11,atol=1e-12)
    eigen,U=np.linalg.eigh(L);freq=np.sqrt(np.maximum(eigen,0))
    exact=np.array([U@(np.cos(freq*t)*(U.T@v)) for t in times])
    first=np.array([np.cos(np.sqrt(2)*t)*v-1j*np.sin(np.sqrt(2)*t)*(A@v)/np.sqrt(2) for t in times])
    exp_error=max(np.linalg.norm(first[i]-expm(-1j*A*t)@v) for i,t in enumerate(times))
    energy=np.array([.5*(y[14:]@y[14:]+y[:14]@L@y[:14]) for y in sol.y.T])
    err=float(np.max(np.abs(sol.y[:14].T-exact)));drift=float(max(abs(energy-energy[0])))
    assert sol.success and err<1e-8 and drift<1e-8 and exp_error<1e-10
    return {'mechanical_frequencies':[float(np.sqrt(3-np.sqrt(2))),float(np.sqrt(3+np.sqrt(2)))],
            'first_order_frequency':float(np.sqrt(2)),'mechanical_ode_max_error':err,'energy_drift':drift,
            'first_order_exponential_error':float(exp_error),'rows':[[float(t),float(exact[i]@v),float(np.real(first[i]@v))] for i,t in enumerate(times)],
            'units':'unit masses, stiffness 3I-A and first-order generator A; no fitted hardware units'}

def modular_audit():
    prior=json.loads((ROOT/'analysis/w33_k12_genus_polarization.json').read_text())
    E=np.array(prior['eisenstein_alternating_form'],dtype=np.int64)
    D=np.array(prior['gaussian_alternating_form'],dtype=np.int64)
    T=np.array(prior['darboux_basis'],dtype=np.int64)
    rows=[]
    for p in (2,3,5,7):
        re,rd=rank_mod(E,p),rank_mod(D,p)
        assert re==12 and rd==(6 if p==3 else 12)
        rows.append({'prime':p,'E_rank':re,'D_rank':rd,'D_radical_dimension':12-rd,'D_quantum_pairs':rd//2})
    # Embed existing two-qutrit labels into the first two Darboux pairs.
    # Swap each pair to match the repo Pauli convention z*x' - x*z'.
    embedding=T[:,[1,0,3,2]]%3
    labels=list(product(range(3),repeat=4));checked=0
    def c(v,w):return (v[1]*w[0]+v[3]*w[2])%3
    for v in labels:
        for w in labels:
            a=embedding@np.array(v);b=embedding@np.array(w)
            assert int(a@E@b)%3==(c(v,w)-c(w,v))%3
            checked+=1
    # Exact central-extension multiplication; bilinearity proves associativity
    # on the entire module. Basis triples exercise signs in every coordinate.
    for p in (2,3,5,7):
        for form in (E,D):
            C=np.triu(form,1)%p
            assert np.array_equal((C-C.T)%p,form%p)
            basis=np.eye(12,dtype=np.int64)
            for u,v,w in product(basis,repeat=3):
                coc=lambda a,b:int(a@C@b)%p
                assert (coc(u,v)+coc(u+v,w)-coc(v,w)-coc(u,v+w))%p==0
    return {'reductions':rows,'two_qutrit_embedding':embedding.tolist(),'pauli_pairs_checked':checked,
            'multiplication':'(u,a)*(v,b)=(u+v,a+b+u^T C v) mod p; C=upper_triangle(form)',
            'basis_associativity_checks':4*2*12**3,
            'boundary':'Noncanonical symplectic embedding into six-qutrit phase space; not a canonical E8-to-K12 lattice map. D has six central coordinates mod 3.'}

def audit():
    surface=surface_chains()
    t1,j1,mineig,comm=period_model(50);t2,j2,_,_=period_model(80)
    with mp.workdps(80):
        difference=float(mp.norm(t1-t2));assert difference<1e-40
    # Store numerical matrices to 16 digits; exact provenance is the cyclotomic formula.
    periods={'curve':'y^2=x^13-1','genus':6,'source':'Tadokoro Proposition 4.1 and Section 4',
             'tau_real':[[float(mp.re(t2[i,j])) for j in range(6)] for i in range(6)],
             'tau_imag':[[float(mp.im(t2[i,j])) for j in range(6)] for i in range(6)],
             'lattice_complex_structure':[[float(j2[i,j]) for j in range(12)] for i in range(12)],
             'precision_comparison_error':difference,'minimum_imaginary_eigenvalue':mineig,
             'eisenstein_commutator_norm':comm,'original_CT_metric_preserved':False,
             'boundary':'An alternative Jacobian structure on the marked symplectic module, not a period realization preserving the CT metric or chosen triangulation geometry.'}
    return {'schema':'w33.genus-six-five-execution.v1','status':'PASS','surface':surface,'periods':periods,
            'handle_vm':surgery_audit(surface['oriented_faces']),'oscillator':oscillator_audit(),'modular':modular_audit()}

if __name__=='__main__':
    import sys
    result=audit()
    if '--write' in sys.argv:Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:({'status':'PASS'} if isinstance(v,dict) else v) for k,v in result.items()},indent=2))
