"""Concrete matched-metric, interacting-Ward, string-input and quantum-lift probes.

All Hamiltonians, auxiliary carriers and couplings are declared inputs.
No chiral continuum measure or complete new string partition function is claimed.
"""
from pathlib import Path
from itertools import product
import json,hashlib,sys
import numpy as np
import sympy as s
from scipy.optimize import minimize_scalar
sys.path.insert(0,str(Path(__file__).resolve().parent))
import w33_pass12377_12381_continuation as old
ROOT=Path(__file__).resolve().parents[1]

def matched_dispersion():
    a,b,V,faces,loops=old.geometry()
    K=np.array([[25/9,-5/3,-26/9],[-5/3,11/3,2],[-26/9,2,28/9]])
    cover=json.loads((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_text())
    G=np.array(s.Matrix(cover['exact_acoustic_metric']),float)
    points=[2*np.pi/3*np.array(v) for v in [(1,1,0,0),(1,1,1,1),(0,0,1,2),(0,1,1,0)]]
    points+=list(np.random.default_rng(12383).uniform(-np.pi,np.pi,size=(20,4)))
    items=[]
    def matrices(k):
        D=old.gradient(a,b,V,k);U,sv,_=np.linalg.svd(D,full_matrices=True);T=U[:,int(sum(sv>1e-11)):]
        F=old.curl(faces,V,k)@T;L=old.curl(loops,V,k)@T;R=old.R@L
        base=F.conj().T@F+R.conj().T@K@R
        w=sum(abs(np.exp(1j*k[:3])-1)**2)
        A=.001*w*np.outer(L[0].conj(),L[0]);B=.001*w*np.outer(L[5].conj(),L[5])
        return base,A,B
    for k in points:
        M,A,B=matrices(k);items.append((M,A,B,float(k@G@k)))
    def gaps(t):return [float(np.linalg.eigvalsh(M+t*A+(2-t)*B)[0]/scale) for M,A,B,scale in items]
    result=minimize_scalar(lambda t:-min(gaps(t)),bounds=(.01,1.99),method='bounded',options={'xatol':1e-7})
    optimum=float(result.x);assert min(gaps(optimum))>=min(gaps(1))-1e-10
    ir=[]
    for direction in [np.array([1,0,0,0]),np.array([1,2,-1,1])]:
        target=float(direction@G@direction);seq=[]
        for t in [.002,.001,.0005]:
            M,A,B=matrices(t*direction);ev=np.linalg.eigvalsh(M+optimum*A+(2-optimum)*B)
            seq.append({'t':t,'three_lambda_over_t2':(ev[:3]/t**2).tolist()})
        ir.append({'direction':direction.tolist(),'target_squared_speed':target,'samples':seq})
    return {'K':K.tolist(),'G':G.tolist(),'sample_momenta':[k.tolist() for k in points],
            'equal_budget_channel_weights':[optimum,2-optimum],'equal_weights_worst_sample_ratio':min(gaps(1)),
            'optimized_worst_sample_ratio':min(gaps(optimum)),'all_optimized_sample_ratios':gaps(optimum),
            'infrared':ir,'scope':'Fixed epsilon=.001 and channel-weight sum2. Optimization only on24 frozen samples; no uniform torus gap or physical light speed.'}

def interacting_ward():
    a,b,V,faces,loops=old.geometry();h=np.zeros((27,27));h[a,b]=-1;h[b,a]=-1
    B=old.gradient(a,b,V,np.zeros(4)).real
    phi=np.random.default_rng(12384).normal(size=27);phi-=phi.mean();long=B@phi;norm=np.linalg.norm(long);phi/=norm;long/=norm
    density=np.diag((phi[:,None]+phi[None,:]).ravel())
    transverse=old.curl(loops,V,np.array([.2,.1,-.3,.17]))[0].real
    # A real divergence-free link direction from an actual native triangle.
    cycle=old.curl(faces,V,np.zeros(4))[0].real;cycle/=np.linalg.norm(cycle)
    def link_ops(u):
        j=np.zeros((27,27),complex);c=np.zeros((27,27))
        j[a,b]=-1j*u;j[b,a]=1j*u;c[a,b]=u*u;c[b,a]=u*u
        return np.kron(j,np.eye(27))+np.kron(np.eye(27),j),np.kron(c,np.eye(27))+np.kron(np.eye(27),c)
    J,C=link_ops(long);JT,CT=link_ops(cycle);out=[]
    for coupling in [0.,2.,8.]:
        H=np.kron(h,np.eye(27))+np.kron(np.eye(27),h)+np.diag((coupling*np.eye(27)).ravel())
        E,U=np.linalg.eigh(H);ground=U[:,0];gap=E[1:]-E[0]
        assert min(gap)>0
        commutator=np.max(abs(J-1j*(H@density-density@H)))
        assert commutator<1e-13
        rho=U[:,1:].conj().T@density@ground;j=U[:,1:].conj().T@J@ground
        jt=U[:,1:].conj().T@JT@ground
        contact=float(np.vdot(ground,C@ground).real);ct=float(np.vdot(ground,CT@ground).real)
        rows=[]
        for omega in [0.,.5,2.,8.]:
            chi=float(np.sum(2*gap*abs(rho)**2/(gap**2+omega**2)))
            paramagnetic=float(np.sum(2*gap*abs(j)**2/(gap**2+omega**2)))
            kernel=contact-paramagnetic
            kt=float(ct-np.sum(2*gap*abs(jt)**2/(gap**2+omega**2)))
            residual=abs(kernel-omega**2*chi);assert residual<1e-12
            rows.append({'omega':omega,'density_susceptibility':chi,'longitudinal_current_kernel':kernel,
                         'contact_term':contact,'paramagnetic_sum':paramagnetic,
                         'ward_residual':residual,'native_triangle_current_kernel':kt})
        out.append({'onsite_U':coupling,'ground_energy':float(E[0]),'gap':float(gap[0]),'commutator_residual':float(commutator),'frequency_samples':rows})
    # Exact SM+right-neutrino chiral charge inventory, independent of Hubbard model.
    # dimension,Y, B-L. Multiplet degeneracy already includes colour and weak dimensions.
    charges=[(6,s.Rational(1,6),s.Rational(1,3)),(3,s.Rational(-2,3),s.Rational(-1,3)),
             (3,s.Rational(1,3),s.Rational(-1,3)),(2,s.Rational(-1,2),-1),(1,1,1),(1,0,1)]
    moments=[sum(d*y**i*z**j for d,y,z in charges) for i,j in [(1,0),(0,1),(3,0),(0,3),(2,1),(1,2)]]
    assert moments==[0]*6
    return {'Hilbert_dimension':729,'particles':'One up and one down fermion on27 native sites',
            'charge_inventory_dimension_Y_BL':[[d,str(y),str(z)] for d,y,z in charges],
            'Abelian_linear_cubic_moments':list(map(str,moments)),'runs':out,
            'scope':'Exact finite interacting Hamiltonian response at imaginary frequency. Chiral charge inventory is separate; no chiral hopping measure, interacting determinant of a4D gauge theory, or selected masses.'}

def quantum_lift():
    from w33_20261029_klein_e8_hamming_twistor_transform import generators,hamming_code
    gs=generators();codes=[hamming_code(g) for g in gs]
    permx=[1,2,0,3,4,5,6,7];permy=[0,1,2,4,5,3,6,7]
    def word(x,p):return sum(1<<p[j] for j in range(8) if x>>j&1)
    def action(p):return [codes.index(frozenset(word(x,p) for x in c)) for c in codes]
    px,py=action(permx),action(permy)
    for base in range(30):
        orbit=[]
        for a,b in product(range(3),repeat=2):
            v=base
            for _ in range(a):v=px[v]
            for _ in range(b):v=py[v]
            orbit.append(v)
        if len(set(orbit))==9:break
    C=np.zeros((256,9))
    for j,index in enumerate(orbit):C[list(codes[index]),j]=.25
    gram=4*C.T@C;assert np.array_equal(gram,3*np.eye(9)+np.ones((9,9)))
    w=np.exp(2j*np.pi/3);X=np.roll(np.eye(3),1,axis=0);Z=np.diag(w**np.arange(3))
    labels=list(product(range(3),repeat=2));F=np.array([[w**(-r*a-t*b)/3 for r,t in labels] for a,b in labels])
    norms=np.array([3 if (r,t)==(0,0) else .75 for r,t in labels]);states=C@F/np.sqrt(norms)[None,:]
    assert np.max(abs(states.conj().T@states-np.eye(9)))<1e-13
    T=np.zeros((768,27),complex)
    for j,(r,t) in enumerate(labels):T[:,3*j:3*j+3]=np.kron(states[:,j,None],np.linalg.matrix_power(X,t)@np.linalg.matrix_power(Z,r))
    residual=0.;group=[]
    for a,b,c in product(range(3),repeat=3):
        sigma=w**c*np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,(-b)%3)
        # Exact exponent identity establishes the controlled-Weyl intertwiner.
        for r,t in labels:
            for x in range(3):
                lhs=-b*x+r*((x+a)%3)
                rhs=r*a+t*b+r*x-b*((x+t)%3)
                assert (lhs-rhs)%3==0
        words=list(range(256))
        for _ in range(a):words=[word(x,permx) for x in words]
        for _ in range(b):words=[word(x,permy) for x in words]
        moved=np.zeros_like(T.reshape(256,3,27));moved[words]=np.einsum('ij,wjk->wik',sigma,T.reshape(256,3,27))
        source=np.kron(np.eye(9),sigma)
        residual=max(residual,float(np.max(abs(moved.reshape(768,27)-T@source))))
        group.append(sigma)
    assert residual<1e-13
    assert np.max(abs(T.conj().T@T-np.eye(27)))<1e-13
    return {'Hamming_nine_orbit_indices':orbit,'four_times_frame_Gram':gram.astype(int).tolist(),
            'Fourier_norm_squared':norms.tolist(),'source':'Nine copies of the faithful3D Schrodinger representation (operator27 type)',
            'target':'Actual256-amplitude8-qubit Hamming CSS span, tensor one auxiliary qutrit',
            'embedding_dimensions':[768,27],'embedding_rank':27,'maximum_intertwining_residual':residual,
            'formula':'T(|r,t> tensor |psi>)=normalized_Hamming_Fourier(r,t) tensor X^t Z^r |psi>',
            'native_law':'(a,b,c)(A,B,C)=(a+A,b+B,c+C-b*A)',
            'central_action':'omega I, supplied by the auxiliary qutrit','scope':'Faithful operator-H27 representation bridge, not a faithful coordinate-permutation action or an E6 dynamical realization. The auxiliary qutrit is a real extra resource. The regular address27 remains a different representation.'}

def string_input():
    # Published S-class example, arXiv2011.04113v2 equations5.1,7.4,7.6.
    A=np.array([
      [-1,-1,-1,1,-1,1,-1,-1,-1,1,1,1,-1],
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,-1,-1],
      [-1,-1,1,-1,1,1,1,-1,1,1,1,1,1],
      [1,-1,-1,-1,1,1,1,1,1,-1,1,1,-1],
      [-1,-1,1,1,1,1,1,-1,-1,1,-1,1,1],
      [1,-1,1,1,1,-1,1,1,-1,1,1,1,-1],
      [-1,-1,1,1,1,1,1,-1,-1,-1,1,-1,1],
      [-1,-1,-1,1,-1,1,-1,1,1,1,-1,1,-1],
      [-1,1,1,1,-1,-1,-1,1,-1,1,-1,1,-1],
      [1,-1,1,-1,1,1,-1,1,1,1,-1,1,1],
      [1,1,1,1,-1,1,1,-1,-1,-1,1,1,1],
      [1,-1,1,1,1,1,-1,1,1,1,1,1,-1],
      [-1,-1,1,-1,1,-1,1,-1,1,-1,-1,-1,-1]])
    names=['1','S']+['e'+str(i) for i in range(1,7)]+['b1','b2','z1','z2','alpha']
    # Real fermion columns: left20 and right44, complex right counted twice.
    left=['psi1','psi2']+['chi'+str(i) for i in range(1,7)]+['y'+str(i) for i in range(1,7)]+['w'+str(i) for i in range(1,7)]
    right=['Y'+str(i) for i in range(1,7)]+['W'+str(i) for i in range(1,7)]+[f'{name}{i}{copy}' for name,count in [('P',5),('E',3),('F',8)] for i in range(1,count+1) for copy in ['a','b']]
    cols=left+right;B=np.zeros((13,64),int)
    def setrow(j,items):
        for name in items:B[j,cols.index(name)]=1
    B[0]=1;setrow(1,left[:8])
    for i in range(1,7):setrow(i+1,[f'y{i}',f'w{i}',f'Y{i}',f'W{i}'])
    for row,indices,eta in [(8,[3,4,5,6],1),(9,[1,2,5,6],2)]:
        setrow(row,[f'{f}{i}' for f in ['chi','y','Y'] for i in indices]+[f'P{i}{c}' for i in range(1,6) for c in 'ab']+[f'E{eta}{c}' for c in 'ab'])
    for row,indices in [(10,range(1,5)),(11,range(5,9))]:setrow(row,[f'F{i}{c}' for i in indices for c in 'ab'])
    setrow(12,[f'P{i}{c}' for i in [4,5] for c in 'ab']+[f'F{i}{c}' for i in [1,2] for c in 'ab'])
    dot2=B[:,:20]@B[:,:20].T-B[:,20:]@B[:,20:].T
    assert np.all(np.diag(dot2)%8==0) and np.all(dot2%4==0)
    # Reciprocity Cij*Cji=exp(i*pi*vi.vj/2), vi.vj=dot2/2.
    reciprocity=(-1)**((dot2//4)%2)
    assert np.array_equal(A*A.T,reciprocity)
    assert all(A[i,i]==-(-1)**int(dot2[i,i]//8)*A[i,0] for i in range(13))
    assert all(A[1,names.index(n)]==-1 for n in ['e1','e2','e3','e4','e5','e6','z2','alpha']) and A[1,10]==1
    # Published necessary top-Yukawa projection rules, tested directly.
    checks=[]
    for i in [2,3]:checks.append(A[i,8]==-A[i,1])
    for i in [4,5]:checks.append(A[i,9]==-A[i,1])
    for i in [10,11]:checks.extend([A[i,8]==-A[i,1],A[i,9]==-A[i,1]])
    checks.extend([A[8,6]==A[9,6],A[8,7]==A[9,7],A[8,12]==-A[9,12]==A[1,12]])
    assert all(checks)
    terms=[(2,0,-8),(0,0,0),(16,1,1),(-192,2,2),(192,3,3),(-4,4,-4)]
    assert all((m-n)%8==0 for c,m,n in terms)
    return {'source':'https://arxiv.org/abs/2011.04113v2','equations':['5.1','7.4','7.6'],
            'basis_names':names,'real_fermion_labels':cols,'boundary_basis_13_by64':B.tolist(),
            'GGSO_matrix_13_by13':A.tolist(),'twice_signed_overlap':dot2.tolist(),
            'exact_basis_and_reciprocity_checks':True,'top_Yukawa_phase_checks':list(map(bool,checks)),
            'published_series_terms_coefficient_m8_n8':terms,
            'scope':'Published4D model inputs and necessary algebraic/series checks. Full8192-by8192 spin-structure phase extension, massive spectrum regeneration, S modular test and Higgs vacuum are not reconstructed here. Published tachyon freedom and chirality are not independently certified by these necessary checks.'}

if __name__=='__main__':
    out={}
    for name,f in [('matched_dispersion',matched_dispersion),('interacting_ward',interacting_ward),('quantum_lift',quantum_lift),('string_input',string_input)]:
        out[name]=f();print(name,'finished',flush=True)
    out['producer_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (ROOT/'data/w33_pass12383_12386_dualhost_fronts.json').write_text(json.dumps(out,indent=2)+'\n')
