"""Independent charge-cone, lattice, Gaussian and graph-matter controls."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, product
from functools import lru_cache
import hashlib, json, sys
import numpy as np
import sympy as S
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as p

@lru_cache(None)
def frozen():return json.loads(p.OUT.read_text())
@lru_cache(None)
def inputs():return p.load()

def test_original_gauge_embedding_reconstructs_all_massless_charges():
    raw,prior,fs,_,_=inputs();T=S.Matrix(raw['u1_embedding']).applyfunc(S.Rational)
    count=0
    for f in fs.values():
        for w in f['weights']:
            assert T*S.Matrix(w).applyfunc(S.Rational)==S.Matrix(f['q']).applyfunc(S.Rational)
            count+=1
    assert count==328 and len(fs)==176

def test_global_cocharacter_on_independent_E8_generators_and_twisted_cosets():
    raw,prior,fs,_,_=inputs();j=frozen()['pass11798'];t=S.Matrix(j['E8xE8_vector']).applyfunc(S.Rational)
    # All D8 roots plus the spinor generator generate each E8 lattice.
    roots=[]
    for i,k in combinations(range(8),2):
        for a,b in product([-1,1],repeat=2):
            z=S.zeros(8,1);z[i]=a;z[k]=b;roots.append(z)
    roots.append(S.ones(8,1)/2)
    for half in [t[:8],t[8:]]:
        assert all(S.Matrix(half).dot(z).q==1 for z in roots)
    assert any((S.Matrix(t[:8]).dot(z)/2).q!=1 for z in roots)
    assert list(map(int,j['shift_and_Wilson_pairings']))==[8,0,0,0,107,107,0,285]
    alpha=S.Matrix(j['charge_covector']).applyfunc(S.Rational)
    assert alpha[0]==0 and (alpha.T*S.Matrix(raw['u1_embedding']).applyfunc(S.Rational)).T==t
    for n,f in fs.items():
        assert (alpha.dot(S.Matrix(f['q']).applyfunc(S.Rational)))%2==prior['all176_field_parities'][n]
    assert j['continuous_gravitational_and_cubic_traces']==['0','0']

def test_FI_core_absent_from_every_neutral_kernel_and_fixed_in_outsider_F():
    _,_,_,support,q=inputs();mat=S.Matrix.hstack(*(S.Matrix(q[n]) for n in support))
    fi=['n_17','n_47','n_50','n_80','n_82']
    assert mat.rank()==8
    assert all(v[support.index(n)]==0 for v in mat.nullspace() for n in fi)
    ex,free=mat.gauss_jordan_solve(-S.Matrix(q['n_81']))
    assert [ex[support.index(n)] for n in fi]==[1,0,0,0,1]

def test_all_order_R_congruences_and_minimum_degree():
    allowed=[]
    for a,b in product(range(19),repeat=2):
        if (2*a+7*b+1)%6==0 and (1-a)%3==0 and (1-b)%2==0:allowed.append((a,b))
    assert allowed and all(a%3==1 and b%6==3 for a,b in allowed)
    assert min(2*(a+b) for a,b in allowed)==8
    j=frozen()['pass11797'];assert len(j['degree8_necessary_candidates'])==19
    assert len({tuple(sorted(r['fields'])) for r in j['degree8_necessary_candidates']})==16
    assert j['degree8_distinct_field_multisets']==16

def test_full_rank_flavor_mesons_reduce_all_doublet_F_terms():
    av=S.symbols('a:4');bv=S.symbols('b:4');c=S.Matrix(2,2,S.symbols('c:4'))
    A=S.Matrix(2,2,av);B=S.Matrix(2,2,bv);eps=S.Matrix([[0,1],[-1,0]])
    M=A.T*eps*B;W=sum(c[i,k]*M[i,k] for i,k in product(range(2),repeat=2))
    da=S.Matrix(2,2,[S.diff(W,z) for z in av]);db=S.Matrix(2,2,[S.diff(W,z) for z in bv])
    assert da==eps*B*c.T and db==-eps*A*c
    # A second full-rank flavor frame checks injectivity beyond the unit VEV.
    aa=S.Matrix([[2,1],[1,1]]);bb=S.Matrix([[1,3],[2,1]])
    linear=S.Matrix([*(eps*bb*c.T),*(-eps*aa*c)]).jacobian(list(c))
    assert linear.rank()==4

def test_outsider_oscillator_rule5_is_recovered_from_raw_quantum_numbers():
    _,_,fs,_,_=inputs();nl=nbar=0
    for n in ['n_81','n_17','n_82']:
        f=fs[n];diff=F(f['RQ'][0])-F(f['q_shift'][1]);number=int(f['oscillator_count'])
        # G2 is the only plane with a signed difference for these fields.
        assert all(F(f['RQ'][i])==F(f['q_shift'][i+1]) for i in [1,2])
        assert abs(diff)==number
        nl+=max(-diff,0);nbar+=max(diff,0)
    assert (nl,nbar)==(1,4) and nl<=nbar
    assert sum(F(int(fs[n]['k']),6) for n in ['n_81','n_17','n_82'])==2

@lru_cache(None)
def core_system():
    _,_,_,support,q=inputs();return S.Matrix.hstack(*(S.Matrix(q[n]) for n in support))

def independent_core(names):
    _,_,_,support,q=inputs();rhs=-sum((S.Matrix(q[n]) for n in names),S.zeros(9,1))
    try:ex,_=core_system().gauss_jordan_solve(rhs)
    except ValueError:return False
    fixed=[ex[support.index(n)] for n in ['n_17','n_47','n_50','n_80','n_82']]
    assert all(not x.free_symbols for x in fixed)
    return all(x.q==1 and x>=0 for x in fixed)

def test_all_color_cone_exclusions_and_exact_Hall_deficiency():
    _,_,fs,support,_=inputs();j=frozen()['pass11799']['mass_sectors']['d']
    for i,a in enumerate(j['rows']):
        for k,b in enumerate(j['columns']):
            if not independent_core([a,b]):assert j['all_order_nonnegative_core_mask'][i][k]==0
    rows=['d_1','d_3','d_6','d_7'];cols=['bd_1','bd_7']
    for a in rows:
        for b in j['columns']:
            if b not in cols:assert not independent_core([a,b])
    # Brute-force all seven-row assignments, independent of matching code.
    masks=[sum(int(x)<<k for k,x in enumerate(row)) for row in j['all_order_nonnegative_core_mask']]
    sets={0}
    for mask in masks:
        sets|={old|(1<<k) for old in sets for k in range(10) if mask>>k&1 and not old>>k&1}
    assert max(x.bit_count() for x in sets)==5
    assert frozen()['pass11799']['exact_color_triplet_Hall_obstruction']['maximum_7x10_mass_rank']==5

def test_integer_annihilator_exclusions_pair_integrally_with_all_generators():
    _,_,fs,support,_=inputs();den=frozen()['pass11799']['mass_lattice']['denominator']
    def v(n):return S.Matrix([den*x for x in p.augmented_charge(fs[n])])
    cols=[v(n) for n in support]
    for i,order in enumerate([6,3,2,2,6,3,2,2]):
        z=S.zeros(17,1);z[9+i]=den*order;cols.append(z)
    generator=S.Matrix.hstack(*cols);target=S.Matrix([0]*13+[-den]*3+[0]);tested=0
    for sector in frozen()['pass11799']['mass_sectors'].values():
        for proof in sector['exact_all_order_exclusions']:
            if 'integer_lattice_annihilator' not in proof:continue
            lam=S.Matrix([proof['integer_lattice_annihilator']]).applyfunc(S.Rational)
            assert all(x.q==1 for x in lam*generator)
            value=(lam*(target-sum((v(n) for n in proof['fields']),S.zeros(17,1))))[0]
            assert value.q!=1 and str(value)==proof['target_pairing'];tested+=1
    assert tested>0

def test_declared_up_and_neutrino_all_order_obstructions():
    _,_,_,_,_=inputs();basis=json.loads((ROOT/'data/w33_pass11793_order_four_matter_action.json').read_text())['candidate_three_family_Higgs_basis']
    up=frozen()['pass11799']['Yukawa_sectors']['u'];assert up['all_order_nonnegative_core_mask']==[[1,0,0],[0,0,0],[0,0,0]]
    for i,a in enumerate(basis['Q']):
        for k,b in enumerate(basis['u_c']):
            if (i,k)!=(0,0):assert not independent_core([a,b,basis['H_u'][0]])
    nu=frozen()['pass11799']['neutrino_sector'];hu=basis['H_u'][0]
    assert nu['Weinberg']['necessary_mask']==[[0]*3]*3
    assert all(not independent_core([a,hu,b,hu]) for a,b in product(basis['L'],repeat=2))
    assert nu['Dirac']['necessary_mask'][2]==[0]*29
    assert all(not independent_core([basis['L'][2],hu,n]) for n in nu['candidate_odd_singlets'])

def test_named_actual_orbifolder_checks_and_exact_label_fallback_provenance():
    checks=json.loads((ROOT/'data/w33_pass11797_corrected_named_coupling_checks.json').read_text())
    canonical=lambda rows:sorted(tuple(sorted(x['fields'])) for x in rows)
    assert canonical(checks['degree8']['rows'])==canonical(frozen()['pass11797']['degree8_necessary_candidates'])
    assert canonical(checks['finite_mass_and_outsider']['rows'])==sorted(tuple(x) for x in frozen()['pass11799']['requests'])
    assert checks['degree8']['original_recursion_controls_verified']==2
    assert checks['finite_mass_and_outsider']['original_recursion_controls_verified']==6
    assert all(x['allowed_count']==1 for k in ['degree8','finite_mass_and_outsider'] for x in checks[k]['rows'])
    for path,digest in checks['source_sha256'].items():assert hashlib.sha256((ROOT/path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==digest

def test_full_H_squared_norm_by_independent_Gaussian_quadrature():
    import w33_pass11769_quantized_current_vacuum as old
    geo=old.geometry();u,v=geo['u'],geo['v'];c,ci=old.spectral_covariance(geo)
    m,t,f,e=[x.mid() for x in p.parameters()];a=np.sqrt(.05)
    xx=t*v@c@v.T/2;zz=u@ci@u.T/(2*t);xz=v@u.T/2
    groups={}
    for i,k in product(range(160),repeat=2):
        key=tuple(np.round([xx[i,k],zz[i,k],xz[i,k],xz[k,i]],11))
        if key not in groups:groups[key]=[i,k,0]
        groups[key][2]+=1
    assert len(groups)==6
    nodes,weights=np.polynomial.hermite_e.hermegauss(5);weights/=np.sqrt(2*np.pi)
    normal=np.array(np.meshgrid(*([nodes]*4),indexing='ij')).reshape(4,-1)
    w=np.prod(np.array(np.meshgrid(*([weights]*4),indexing='ij')),axis=0).ravel()
    total=0.
    for i,k,count in groups.values():
        cov=np.array([[t*m,0,xx[i,k],xz[i,k]],[0,m/t,xz[k,i],zz[i,k]],
                      [xx[i,k],xz[k,i],t*m,0],[xz[i,k],zz[i,k],0,m/t]])
        d,b=np.linalg.eigh(cov);assert min(d)>-1e-12
        X,Z,Y,W=(b*np.sqrt(np.maximum(d,0)))@normal
        he=(X+a)**2*((f*X+a+1j*Z)**2+2*m/t)
        hk=(Y+a)**2*((f*Y+a+1j*W)**2+2*m/t)
        total+=count*float(w@(he.conjugate()*hk).real)
        assert abs(w@he-e/160)<1e-11
    j=frozen()['pass11800'];lo,hi=map(F,j['full_H_squared_norm_interval'])
    assert abs(total-float((lo+hi)/2))<2e-8
    variance=list(map(F,j['full_residual_variance_interval']));sigma=F(j['spectral_distance_upper_bound'])
    assert sigma*sigma>=variance[1]>variance[0]>0

@lru_cache(None)
def graph():
    j=json.loads((ROOT/'data/w33_pass11389_parabolic_spatial_cover.json').read_text())['line']
    edges=j['edges'];E=S.Matrix(j['fcc_harmonic_displacements']).applyfunc(S.Rational);V=S.Matrix(j['integer_voltage'])
    st=[[] for _ in range(80)]
    for i,(a,b) in enumerate(edges):st[a].append((b,i,1));st[b].append((a,i,-1))
    two=[(b,c,-si*E[i,:]+sj*E[k,:],-si*V[i,:]+sj*V[k,:]) for row in st for (b,i,si),(c,k,sj) in combinations(row,2)]
    channels=[(a,b,E[i,:],V[i,:]) for i,(a,b) in enumerate(edges)]+two
    return channels

@pytest.mark.parametrize('k',[(0,0,0),(.23,-.17,.31)])
def test_native_Bloch_two_hop_identity_at_distinct_wavevectors(k):
    channels=graph();L=np.zeros((80,80),complex);L2=L.copy()
    for target,cs in [(L,channels[:160]),(L2,channels[160:])]:
        for a,b,d,z in cs:
            phase=np.exp(1j*np.dot(k,np.array(z,dtype=float).ravel()))
            target[a,a]+=1;target[b,b]+=1;target[a,b]-=phase;target[b,a]-=phase.conjugate()
    assert np.max(abs(L2-(8*L-L@L)))<2e-13
    assert len(channels)==640

def test_native_metric_right_inverse_and_microscopic_fiber():
    cs=graph();response=S.Matrix([[d[0]**2,d[1]**2,d[2]**2,d[0]*d[1],d[0]*d[2],d[1]*d[2]] for a,b,d,z in cs])/80
    j=frozen()['pass11801'];indices=j['right_inverse_channels'];right=S.Matrix(j['right_inverse_values']).applyfunc(S.Rational)
    assert response[indices,:].T*right==S.eye(6)
    assert response[:160,:].rank()==4
    null=response.T.nullspace()[0];probe=j['exact_microscopic_metric_fiber_probe'];vertex=probe['vertex']
    assert response.T*null==S.zeros(6,1)
    energy=sum(null[i]*int((a==vertex)!=(b==vertex)) for i,(a,b,d,z) in enumerate(cs))
    assert energy==S.Rational(probe['fiber_energy_pairing'])!=0
    momentum=S.Matrix([2,-3,5]);change=right*S.Matrix([1,2,3,4,5,6]);K=S.Matrix([[1,4,5],[4,2,6],[5,6,3]])
    # Use all six explicitly changed channels, including native two hops.
    de=sum(change[i]*(cs[index][2].dot(momentum))**2/2 for i,index in enumerate(indices))
    assert de==40*(momentum.T*K*momentum)[0]

def test_exact_local_energy_continuity_and_general_SPD_metric_map():
    x,y,vx,vy,w,rho=S.symbols('x y vx vy w rho',real=True)
    acc=-w*(x-y)/rho
    dotEa=S.expand(rho*vx*acc+w*(x-y)*(vx-vy)/2)
    outward=w*(x-y)*(vx+vy)/2
    assert S.expand(dotEa+outward)==0
    assert 'I_ab=(w_ab/2)' in frozen()['pass11801']['conserved_graph_energy']
    B=S.Matrix([[1,1,0],[0,1,1],[0,0,1]]);K=B.T*S.diag(2,3,5)*B;rho=S.Rational(7)
    N=(K.det()/rho)**S.Rational(1,4);h=(rho*K.det())**S.Rational(1,2)*K.inv();volume=S.sqrt(h.det())
    assert S.simplify(volume/N)==rho
    assert (N*volume*h.inv()-K).applyfunc(S.simplify)==S.zeros(3)

def test_all_owned_source_and_input_hashes():
    j=frozen();assert j['source_sha256']==hashlib.sha256(Path(p.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    for path,digest in j['inputs_sha256'].items():
        file=ROOT/path;raw=file.read_bytes();raw=raw.replace(b'\r\n',b'\n') if file.suffix=='.json' else raw
        assert hashlib.sha256(raw).hexdigest()==digest
    assert all(j[f'pass{n}']['status']=='PASS' for n in range(11797,11802))


def test_single_condensate_escape_requires_coordinated_hidden_flavors():
    rows=frozen()['pass11799']['single_even_condensate_extension_audit']
    assert len(rows)==43 and len({r['field'] for r in rows})==43
    escapes=[r for r in rows if r['relaxed_structural_rank_upper_bound']>1]
    assert [r['field'] for r in escapes]==['n_69','n_74']
    assert all(r['dimension']=='1,1,4,1' for r in escapes)
    assert all(r['holomorphic_hidden_invariant_rank_upper_bound']==1 for r in rows)
    # Four identical commuting flavor vectors have identically zero baryon.
    v=S.Matrix(S.symbols('z:4'))
    assert S.Matrix.hstack(v,v,v,v).det()==0
    # Independently derive each FI direction from the raw nine charges.
    _,_,_,support,q=inputs();fi=['n_17','n_47','n_50','n_80','n_82']
    for row in rows:
        ex,_=core_system().gauss_jordan_solve(-S.Matrix(q[row['field']]))
        direction=[-ex[support.index(n)] for n in fi]
        assert list(map(str,direction))==row['FI_coordinate_direction']


@pytest.mark.parametrize('sector,rank',[('x',0),('v',8)])
def test_fractional_exotic_all_order_Hall_obstructions(sector,rank):
    j=frozen()['pass11799']['mass_sectors'][sector]
    masks=[sum(int(z)<<k for k,z in enumerate(r)) for r in j['all_order_nonnegative_core_mask']]
    # Exhaustive Hall deficiency over every row subset, a distinct algorithm.
    maximum=0
    for bits in range(1,1<<len(masks)):
        neighbors=0
        for i,row in enumerate(masks):
            if bits>>i&1:neighbors|=row
        maximum=max(maximum,bits.bit_count()-neighbors.bit_count())
    assert len(masks)-maximum==rank==j['all_order_mass_rank_upper_bound']
    for i,a in enumerate(j['rows']):
        for k,b in enumerate(j['columns']):
            if not independent_core([a,b]):assert masks[i]>>k&1==0
    if sector=='x':assert j['all_order_nonnegative_core_mask']==[[0,0],[0,0]]
