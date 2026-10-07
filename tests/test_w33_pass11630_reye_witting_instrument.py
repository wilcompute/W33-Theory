"""Independent channel, exclusivity and corruption controls for Pass11630."""
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile
import numpy as np
import pytest
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11630_reye_witting_instrument as m

@pytest.fixture(scope='module')
def cert():return json.loads(m.OUT.read_text())

def mat(rows):return np.array([[complex(s.sympify(x)) for x in row] for row in rows])

def changed(z,name,data):
    b=io.BytesIO()
    with zipfile.ZipFile(b,'w') as out:
        for n in z.namelist():out.writestr(n,json.dumps(data) if n==name else z.read(n))
    return zipfile.ZipFile(io.BytesIO(b.getvalue()))

def test_source_transport_and_quarantine(cert):
    z,manifest=m.archive_inputs()
    assert len(manifest)==19 and len(z.namelist())==20
    assert hashlib.sha256(m.ARCHIVE.read_bytes()).hexdigest()==cert['input_archive_sha256']
    assert len(z.read('witting_experiment_results.json'))==147
    with pytest.raises(json.JSONDecodeError):json.loads(z.read('witting_experiment_results.json'))
    assert cert['producer_sha256']==hashlib.sha256(Path(m.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()

def test_dilation_trace_preservation_on_entangled_inputs(cert):
    W=mat(cert['instrument']['dilation']);K=W[:4,:4];F=W[4:,:4]
    assert np.allclose(W.conj().T@W,np.eye(8),atol=1e-12)
    # Choi positivity and input marginal, rather than only a unitary replay.
    choi=sum(np.outer(a.ravel(order='F'),a.ravel(order='F').conj()) for a in [K,F])
    assert np.linalg.eigvalsh(choi).min()>-1e-12
    assert np.allclose(np.trace(choi.reshape(4,4,4,4),axis1=1,axis2=3),np.eye(4))
    rng=np.random.default_rng(11630)
    v=rng.normal(size=8)+1j*rng.normal(size=8);v/=np.linalg.norm(v)
    branches=[np.kron(a,np.eye(2))@v for a in [K,F]]
    assert abs(sum(np.vdot(x,x).real for x in branches)-1)<1e-12

def test_random_complex_inputs_require_both_complementary_maps(cert):
    d=cert['instrument'];L=mat(d['projective_matrix']);U=mat(d['polar_unitary'])
    S=np.kron(np.array([[0,-1j],[1j,0]]),np.eye(2));pp=(np.eye(4)+S)/2;pm=(np.eye(4)-S)/2
    r=2-np.sqrt(3);p=(3-np.sqrt(3))/2
    K=L/np.sqrt(1+1/np.sqrt(3));Kd=U@(np.sqrt(r)*pp+pm)
    assert np.allclose((K.conj().T@K+Kd.conj().T@Kd)/2,p*np.eye(4))
    rng=np.random.default_rng(33)
    for _ in range(12):
        B=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));rho=B@B.conj().T;rho/=np.trace(rho)
        out=(K@rho@K.conj().T+Kd@rho@Kd.conj().T)/(2*p)
        eta=np.sqrt(2/3);expected=U@((1+eta)*rho/2+(1-eta)*S@rho@S/2)@U.conj().T
        assert np.allclose(out,expected,atol=1e-12) and abs(np.trace(out)-1)<1e-12
    # Single-branch success probability is not constant on complex states.
    vals=np.linalg.eigvalsh(K.conj().T@K)
    assert np.allclose(vals,[r,r,1,1])

def test_single_real_cell_maps_and_cross_duality(cert):
    d=cert['instrument'];L=mat(d['projective_matrix']);Ld=np.linalg.inv(L).conj().T
    a,b=m.real_cells();a=[np.array(v,complex).ravel() for v in a];b=[np.array(v,complex).ravel() for v in b]
    V=m.numeric_vectors()
    for vs,M,labels in [(a,L,d['primary_map']),(b,Ld,d['dual_map'])]:
        for v,j in zip(vs,labels):
            out=M@v;out/=np.linalg.norm(out)
            assert abs(np.vdot(V[:,j],out))**2>1-1e-12
    # This explicitly rejects the mistaken use of L for the second cell.
    assert max(abs(V.conj().T@(L@b[0]/np.linalg.norm(L@b[0])))**2)<.7
    assert np.allclose(L.conj().T@Ld,np.eye(4))

def test_channel_rigidity_is_not_just_a_fidelity_argument(cert):
    d=cert['instrument'];L=mat(d['projective_matrix'])
    assert d['pure_target_Kraus_constraint_rank']==15
    assert not np.allclose(L.conj().T@L,np.trace(L.conj().T@L)/4*np.eye(4))
    # Basis rays alone allow unequal column scales; the half-vector forbids it.
    D=np.diag([1,2,3,4]);v=np.ones(4)/2
    assert np.linalg.matrix_rank(np.column_stack([L@D@v,L@v]),tol=1e-12)==2

def test_gram_phase_corruption_is_detected_exactly():
    z,_=m.archive_inputs();d=json.loads(z.read('gram_reconstruction_certificate.json'))
    d['steps'][0]['triple_product'][0]+=.01
    bad=changed(z,'gram_reconstruction_certificate.json',d);G,_,_=m.graph_data()
    with pytest.raises(AssertionError):m.gram_audit(bad,G)

def test_critical_KS_needs_exclusivity_and_all_deletion_witnesses(cert):
    G,bases,_=m.graph_data();d=cert['KS'];C=set(d['critical_rays'])
    green=set(d['basis_only_coloring'])
    assert all(len(green&set(b))==1 for b in d['tetrads'])
    assert G.subgraph(green).number_of_edges()>0
    assert m.coloring(G,bases,C) is None
    for deleted,green in d['single_deletion_colorings'].items():
        present=C-{int(deleted)};green=set(green)
        assert green<=present and G.subgraph(green).number_of_edges()==0
        assert all(len(green&set(b))==1 for b in bases if set(b)<=present)

def test_a_corrupt_deletion_coloring_is_rejected():
    z,_=m.archive_inputs();d=json.loads(z.read('five_followup_results.json'))
    d['KS_extension']['deletion_coloring_witnesses']['0'].append(0)
    bad=changed(z,'five_followup_results.json',d);G,bases,ind=m.graph_data()
    with pytest.raises(AssertionError):m.ks_audit(bad,G,bases,ind)

def test_fixed_paired_union_is_still_colorable(cert):
    G,bases,_=m.graph_data();d=cert['instrument'];C=set(d['primary_map']+d['dual_map'])
    assert len(C)==24 and m.coloring(G,bases,C) is not None
    assert cert['KS']['relative_minimum']==6 and len(cert['KS']['extensions'])==48

def test_magic_preparation_uses_actual_filter_and_stabilizer_readout(cert):
    L=mat(cert['instrument']['projective_matrix']);K=L/np.sqrt(1+1/np.sqrt(3))
    plusplus=np.ones(4)/2;post=K@plusplus
    p=np.vdot(post,post).real;post/=np.sqrt(p)
    readout=np.kron(np.array([[1,1]])/np.sqrt(2),np.eye(2));q=readout@post
    readout_p=np.vdot(q,q).real;q/=np.sqrt(readout_p)
    expected=np.array([-1,2])/np.sqrt(5)
    assert np.allclose(np.outer(q,q.conj()),np.outer(expected,expected))
    assert abs(p-(3-np.sqrt(3))/2)<1e-12 and abs(readout_p-5/6)<1e-12
    X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
    bloch=np.array([np.vdot(q,A@q).real for A in [X,Y,Z]])
    assert np.allclose(bloch,[-4/5,0,-3/5]) and sum(abs(bloch))>1
    # Polytope boundary is independently checked before the decoder test.
    assert abs(sum(abs((5/7)*bloch))-1)<1e-12

def test_steane_projection_and_tight_output_noise_boundary(cert):
    d=cert['instrument']['magic_preparation']['Steane_distillation']
    assert d['status']=='PASS' and d['initial_coordinate']=='7*v/10'
    X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);H=(X+Z)/np.sqrt(2)
    magic=np.array([-1,2])/np.sqrt(5)
    B=np.zeros((128,2))
    for w in d['codewords']:
        i=int(w,2);B[i,0]=1/np.sqrt(8);B[127-i,1]=1/np.sqrt(8)
    assert np.allclose(B.conj().T@B,np.eye(2))
    for v in [0.,.5,5/7,.8,1.]:
        rho=v*np.outer(magic,magic)+(1-v)*np.eye(2)/2
        rotated=Y@rho@Y;twirl=(rotated+H@rotated@H)/2
        x=7*v/10
        assert np.allclose(twirl,(np.eye(2)+x*(X+Z))/2)
        full=twirl
        for _ in range(6):full=np.kron(full,twirl)
        out=B.conj().T@full@B;p=np.trace(out).real
        xo=x**3*(7+8*x**4)/(1+14*x**4)
        assert abs(p-(1+14*x**4)/64)<1e-12
        assert np.allclose(out/p,(np.eye(2)+xo*(X+Z))/2)
        assert (xo>x+1e-12)==(v>5/7)
        if v<=5/7:
            free=4*v/5*(np.eye(2)+X)/2+3*v/5*(np.eye(2)+Z)/2+(1-7*v/5)*np.eye(2)/2
            assert 1-7*v/5>=-1e-12 and np.allclose(free,rotated)
