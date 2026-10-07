"""Pass11630: independently audit supplied Witting data; complete its Reye map.

Perplexity input owns the explicit projective embedding and extension search.
Pass4963 owns exact Eisenstein rays/phases/W33 discrimination;11625-11629
owns the previous Peres/coherent-query resource controls. This packet adds an
exact operational completion, not a new contextuality or universality theorem.
"""
from __future__ import annotations
import csv
import hashlib
import io
import itertools as it
import json
from collections import Counter, deque
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
import sys
import zipfile
import networkx as nx
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass4963_witting_pancharatnam_w33_reaudit import inner, mul, conj, neg, POW, ZERO
from w33_reye_witting_context_resource_audit import coloring
ARCHIVE=ROOT/'data/w33_pass11630_perplexity_input.zip'
ARCHIVE_SHA='0e85aef7030468d45048aa14d59fed7c1b2fb5e64ed40d53ef8dc0d7f4bb8659'
OUT=ROOT/'data/w33_pass11630_reye_witting_instrument.json'

def archive_inputs():
    b=ARCHIVE.read_bytes()
    assert len(b)==826497 and hashlib.sha256(b).hexdigest()==ARCHIVE_SHA
    z=zipfile.ZipFile(io.BytesIO(b))
    manifest=json.loads(z.read('source_manifest.json'))
    for x in manifest:
        b=z.read(x['name'])
        assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256']
    assert len(manifest)==19
    try: json.loads(z.read('witting_experiment_results.json'))
    except json.JSONDecodeError: pass
    else: raise AssertionError('Expected the documented truncated input')
    return z,manifest

def rays():
    """Pass4963's coordinates reordered to the supplied block convention."""
    R=[]
    for j in range(4): R.append(tuple((int(i==j),0) for i in range(4)))
    one=(1,0)
    for j in range(4):
        for a,b in it.product(range(3),repeat=2):
            R.append([(ZERO,one,neg(POW[a]),POW[b]),
                      (one,ZERO,neg(POW[a]),neg(POW[b])),
                      (one,neg(POW[a]),ZERO,POW[b]),
                      (one,POW[a],POW[b],ZERO)][j])
    return R

def exact_vectors():
    w=(-1+s.sqrt(3)*s.I)/2
    return [s.Matrix([a+b*w for a,b in v]).applyfunc(s.expand) for v in rays()]

def numeric_vectors():
    w=np.exp(2j*np.pi/3)
    V=np.array([[a+b*w for a,b in v] for v in rays()],complex).T
    return V/np.linalg.norm(V,axis=0)

def graph_data():
    R=rays();G=nx.Graph();G.add_nodes_from(range(40))
    G.add_edges_from((i,j) for i,j in it.combinations(range(40),2) if inner(R[i],R[j])==ZERO)
    bases=sorted(tuple(sorted(c)) for c in nx.find_cliques(G))
    independent=sorted(tuple(sorted(c)) for c in nx.find_cliques(nx.complement(G)))
    assert len(bases)==40 and all(len(c)==4 for c in bases)
    assert Counter(map(len,independent))=={4:90,7:2880}
    return G,bases,independent

@lru_cache(maxsize=2048)
def algebraic_zero(x):
    x=s.simplify(s.expand(x))
    if x==0:return True
    # Equal nested-radical expressions may survive simplify. No numerical
    # tolerance or forced branch choice is used for this exact fallback.
    return s.to_number_field(x).as_expr()==0 if not x.free_symbols else False
def zero(M): return all(algebraic_zero(x) for x in M)
def simplify(M): return M.applyfunc(lambda x:s.simplify(s.expand(x)))
def proportional(v,w):
    return all(s.simplify(s.expand(v[i]*w[j]-v[j]*w[i]))==0 for i,j in it.combinations(range(len(v)),2))

def real_cells():
    a=[s.eye(4)[:,i] for i in range(4)]
    a += [s.Matrix((1,)+signs)/2 for signs in it.product([-1,1],repeat=3)]
    b=[]
    for i,j in it.combinations(range(4),2):
        for sign in [-1,1]:
            v=s.zeros(4,1);v[i]=1;v[j]=sign;b.append(v/s.sqrt(2))
    return a,b

def steane_resource(magic):
    """Reichardt0411036's known decoder, built from its eight codewords.

    New application: the supplied Reye operation's depolarized output reaches
    this decoder through a stabilizer-only Y conjugation and I/H twirl.
    """
    X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]])
    Z=s.diag(1,-1);H=(X+Z)/s.sqrt(2);v=s.symbols('v',real=True)
    rho=v*magic*magic.H+(1-v)*s.eye(2)/2
    rotated=Y*rho*Y
    twirl=simplify((rotated+H*rotated*H)/2)
    assert zero(twirl-(s.eye(2)+s.Rational(7,10)*v*(X+Z))/2)
    x=s.symbols('x',real=True);R=(s.eye(2)+x*(X+Z))/2
    words=['0000000','0001111','0110011','0111100',
           '1010101','1011010','1100110','1101001']
    S=[[int(b) for b in w] for w in words]
    T=[[1-b for b in w] for w in S]
    def entry(a,b):return s.prod(R[i,j] for i,j in zip(a,b))
    decoded=s.Matrix([[s.expand(sum(entry(a,b) for a in A for b in B)/8)
                       for B in [S,T]] for A in [S,T]])
    acceptance=s.factor(s.trace(decoded));xo=s.factor(s.trace(X*decoded)/acceptance)
    assert s.cancel(acceptance-(1+14*x**4)/64)==0
    assert xo==x**3*(7+8*x**4)/(1+14*x**4)
    assert zero(decoded/acceptance-(s.eye(2)+xo*(X+Z))/2)
    gain=s.factor(xo-x)
    assert s.cancel(gain-x*(1-x**2)*(4*x**2-1)*(1-2*x**2)/(1+14*x**4))==0
    # At and below the boundary the untwirled state itself is free.
    PX=(s.eye(2)+X)/2;PZ=(s.eye(2)+Z)/2
    assert zero(rotated-(4*v*PX/5+3*v*PZ/5+(1-7*v/5)*s.eye(2)/2))
    return dict(status='PASS',source='Reichardt quant-ph/0411036, SectionII; decoder is published prior art',
        noise_model='IID output qubits rho_v=v|m><m|+(1-v)I/2, 0<=v<=1; perfect stabilizer operations',
        preprocessing='Y conjugation then choose I or H uniformly and forget the choice',
        twirled_Bloch=['7*v/10','0','7*v/10'],codewords=words,
        acceptance=str(acceptance),output_coordinate=str(xo),improvement_factor=str(gain),
        initial_coordinate='7*v/10',ideal_first_acceptance=str(acceptance.subs(x,s.Rational(7,10))),
        ideal_first_output=str(xo.subs(x,s.Rational(7,10))),
        threshold='v>5/7 is necessary and sufficient for this output-state family with perfect stabilizer control. The Steane recursion increases x for1/2<x<1/sqrt(2) and converges to1/sqrt(2); at v<=5/7 the input is a stabilizer mixture.',
        free_decomposition=['(4*v/5)|+X><+X|','(3*v/5)|+Z><+Z|','(1-7*v/5)I/2'],
        boundary='Threshold for IID depolarization AFTER successful preparation, not for noisy K, noisy readout, correlated errors or a fault-tolerant physical machine; acceptance/resource cost is not efficient near threshold.')

def instrument(z):
    d=json.loads(z.read('reye_exact_certificate.json'))
    L=s.Matrix([[s.sympify(x) for x in row] for row in d['projective_matrix']])
    V=exact_vectors();a,b=real_cells()
    correspond=list(csv.DictReader(io.StringIO(z.read('reye_point_correspondence.csv').decode())))
    amap=[int(x['witting_ray_id']) for x in correspond]
    Ldual=simplify(L.H.inv())
    bmap=[]
    for v in b:
        hits=[j for j,w in enumerate(V) if proportional(Ldual*v,w)]
        assert len(hits)==1;bmap.append(hits[0])
    assert set(amap)==set(d['primary_reye']) and set(bmap)==set(d['dual_reye'])
    assert all(proportional(L*v,V[j]) for v,j in zip(a,amap))
    M=simplify(L.H*L);I=s.eye(4);c=1/s.sqrt(3)
    J=simplify((M-I)/(s.I*c))
    assert J==s.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
    assert J.T==-J and J*J==-I and zero(s.re(M)-I)
    Pplus=(I+s.I*J)/2;Pminus=(I-s.I*J)/2
    p=s.simplify(1/(1+c));r=s.simplify((1-c)/(1+c))
    K=L/s.sqrt(1+c);F=s.sqrt(1-r)*Pminus
    assert zero(K.H*K+F.H*F-I)
    # Polar factor and an explicit 8D unitary: no implicit "dilation exists".
    rootr=(s.sqrt(3)-1)/s.sqrt(2)
    assert s.simplify(rootr**2-r)==0 and rootr.is_positive
    D=Pplus+rootr*Pminus;E=s.sqrt(1-r)*Pminus
    U=K*(Pplus+Pminus/rootr)
    assert zero(U.H*U-I)
    dilation=(U*D).row_join(-U*E).col_join(E.row_join(D))
    assert zero(dilation.H*dilation-s.eye(8))
    assert zero(dilation[:4,:4]-K) and zero(dilation[4:,:4]-F)
    # Duality uses the inverse adjoint, not the same map on both 24-cells.
    Lminus=s.sqrt(s.Rational(2,3))*Ldual
    assert zero(Lminus.H*Lminus-(I-s.I*c*J))
    Kminus=U*(rootr*Pplus+Pminus);Fminus=s.sqrt(1-r)*Pplus
    assert zero(Kminus.H*Kminus+Fminus.H*Fminus-I)
    # This exact projector identity proves Kminus is a nonzero scalar times
    # L^-dag, without asking a symbolic assumption engine to compare large
    # nested-radical minors of the expanded polar matrix.
    assert zero((Pplus+r*Pminus)*(rootr*Pplus+Pminus/rootr)-rootr*I)
    assert zero((K.H*K+Kminus.H*Kminus)/2-p*I)
    # Forgetting the success branch gives an exact Pauli dephasing channel,
    # conjugated by the common polar U. Prove equality on all 16 matrix units.
    eta=s.sqrt(s.Rational(2,3));S=s.I*J
    assert S==s.kronecker_product(s.Matrix([[0,-s.I],[s.I,0]]),s.eye(2))
    for i,j in it.product(range(4),repeat=2):
        rho=s.zeros(4);rho[i,j]=1
        left=(D*rho*D+(rootr*Pplus+Pminus)*rho*(rootr*Pplus+Pminus))/(2*p)
        right=(1+eta)*rho/2+(1-eta)*S*rho*S/2
        assert zero(left-right)
    # The paired 24-ray image is a tight one-design, but still KS-colorable.
    frame=sum((L*v*v.H*L.H for v in a),s.zeros(4))
    frame+=sum((Lminus*v*v.H*Lminus.H for v in b),s.zeros(4))
    assert zero(frame-6*I)
    assert zero(L.H*Lminus-s.sqrt(s.Rational(2,3))*I)
    # The failure branch has a fixed qubit carrier, not an arbitrary 4D loss.
    B=s.Matrix([[1,0],[0,1],[-s.I,0],[0,-s.I]])/s.sqrt(2)
    assert zero(B.H*B-s.eye(2)) and zero(B*B.H-Pminus)
    qubits=[s.Matrix([1,0]),s.Matrix([0,1]),s.Matrix([1,1]),s.Matrix([1,-1]),s.Matrix([1,s.I]),s.Matrix([1,-s.I])]
    failure=[]
    for v in a+b:
        assert s.simplify((v.H*K.H*K*v)[0]-p)==0
        q=B.H*F*v;hits=[i for i,w in enumerate(qubits) if proportional(q,w)]
        assert len(hits)==1;failure.append(hits[0])
    assert Counter(failure)=={i:4 for i in range(6)}
    real_orth=[];lost=[];preserved=[];created=[]
    for i,j in it.combinations(range(12),2):
        was=(a[i].T*a[j])[0]==0;now=s.simplify((a[i].T*M*a[j])[0])==0
        if was:real_orth.append([i,j]);(preserved if now else lost).append([i,j])
        elif now:created.append([i,j])
    assert (len(real_orth),len(preserved),len(lost),len(created))==(18,12,6,0)
    # Six lost pairs collapse to identical rays in the heralded failure branch.
    assert all(failure[i]==failure[j] for i,j in lost)
    # Pure outputs force every success Kraus operator into the SAME one-
    # dimensional subspace. Four basis rays give A=L diag(c_i); a single
    # all-nonzero real half-vector then forces all c_i equal. Verify the
    # projective linear constraints independently rather than assuming it.
    constraints=[]
    for v in a[:5]:
        t=L*v
        for i,j in it.combinations(range(4),2):
            row=[s.S(0)]*16
            for k in range(4):row[4*i+k]+=v[k]*t[j];row[4*j+k]-=v[k]*t[i]
            constraints.append(row)
    C=s.Matrix(constraints)
    from sympy.polys.matrices import DomainMatrix
    rank=DomainMatrix.from_Matrix(C).convert_to(s.QQ.algebraic_field(s.I*s.sqrt(3))).rank()
    assert rank==15 and zero(C*s.Matrix(list(L)))
    # A concrete magic preparation uses just |++>, this K, and an X readout.
    assert amap[11]==4 and a[11]==s.ones(4,1)/2
    phi=L*a[11];T=s.kronecker_product(s.Matrix([[1,1]])/s.sqrt(2),s.eye(2))
    q=T*phi;prob=s.simplify((q.H*q)[0]);assert prob==s.Rational(5,6)
    magic=s.Matrix([-1,2])/s.sqrt(5)
    assert zero(q*q.H/prob-magic*magic.H)
    pauli=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
    bloch=[s.simplify((magic.H*A*magic)[0]) for A in pauli]
    assert bloch==[-s.Rational(4,5),0,-s.Rational(3,5)]
    return dict(status='PASS',projective_matrix=[[str(x) for x in row] for row in L.tolist()],
        primary_map=amap,dual_map=bmap,dual_map_rule='Ldual=(Ldag)^-1; its normalized real-isometric representative is sqrt(2/3)Ldual',
        exact_minor_checks=144,determinant=str(s.simplify(L.det())),
        pullback_metric=[[str(x) for x in row] for row in M.tolist()],J=[[int(x) for x in row] for row in J.tolist()],
        metric_law='Ldag L=I+iJ/sqrt(3), J^T=-J, J^2=-I; Re(Ldag L)=I',
        slant_angle_cosine='1/sqrt(3)',success_probability=str(p),failure_probability=str(s.simplify(1-p)),
        effect_spectrum={'1':2,str(r):2},pure_target_Kraus_constraint_rank=15,
        optimality='For a completely positive success operation with the specified pure outputs on just the four basis rays and one all-nonzero half-vector, every Kraus operator is a_j L. Trace nonincrease forces sum|a_j|^2 <= 1/(1+1/sqrt(3)). All real-unit input rays have uniform success at this bound, and K saturates it. A deterministic CPTP map with these same pure outputs is impossible since Ldag L is not scalar.',
        dilation=[[str(x) for x in row] for row in dilation.tolist()],failure_qubit_labels=failure,
        polar_unitary=[[str(x) for x in row] for row in U.tolist()],
        paired_effect_law='(Kplusdag Kplus+Kminusdag Kminus)/2=p I for every complex input, p=(3-sqrt(3))/2',
        forgotten_branch_channel='Conditional on success, discard the uniformly chosen branch: U[(1+sqrt(2/3))/2 rho+(1-sqrt(2/3))/2 (Y tensor I)rho(Y tensor I)]Udag. Checked on all16 matrix units.',
        paired_frame_law='Sum of the24 normalized image projectors is6 I; the two complementary pullback metrics cancel the skew part.',
        magic_preparation=dict(input='|++>',heralded_success_ray=4,readout='Measure X on first qubit; keep + outcome',
            conditional_readout_probability='5/6',magic_ray=['-1','2'],normalization='sqrt(5)',Bloch=[str(x) for x in bloch],
            total_success_probability=str(s.simplify(p*prob)),mean_independent_attempts=str(s.simplify(1/(p*prob))),
            depolarized_nonstabilizer_condition='Visibility v>5/7 gives Bloch l1=7v/5>1. The separately constructed Y/H twirl and Steane decoder make this a tight IID output-depolarization threshold with perfect stabilizer control.',
            Steane_distillation=steane_resource(magic),
            universality='If this K can actually be repeatedly implemented with stabilizer preparation/readout/control, it prepares a pure non-Pauli qubit. Reichardt quant-ph/0411036 then gives conditional computational universality. No free K, error-corrected distiller or microscopic Hamiltonian is supplied.'),
        failure_Pauli_multiplicities={str(k):v for k,v in sorted(Counter(failure).items())},lost_real_orthogonal_pairs=lost,
        instrument_boundary='A supplied exact CP instrument with an ancilla-unitary specification; no microscopic interaction, fault-tolerant synthesis or Clifford-only implementation is derived. Its explicit pure nonstabilizer output cannot be prepared by Clifford/stabilizer operations alone. This is an additional resource, not a free consequence of KS incidence.')

# Exact field Q(omega,sqrt(3)); each value below is sqrt(3)^t*(a+b*omega).
def emul(x,y):
    a,b=mul(x[:2],y[:2]);t=x[2]+y[2]
    return (a*(3 if t==2 else 1),b*(3 if t==2 else 1),t%2)
def econj(x): return (*conj(x[:2]),x[2])
def einv(x):
    a,b=conj(x[:2]);n=x[0]**2-x[0]*x[1]+x[1]**2
    f=n*(3 if x[2] else 1)
    return (Q(a)/f,Q(b)/f,x[2])
def enumeric(x): return 3**(x[2]/2)*(float(x[0])+float(x[1])*np.exp(2j*np.pi/3))

def gram_audit(z,G):
    R=rays();norms=[inner(v,v)[0] for v in R]
    H={}
    for i,j in it.product(range(40),repeat=2):
        a,b=inner(R[i],R[j]);nn=norms[i]*norms[j]
        H[i,j]=(Q(a,nn if nn in (1,3) else 3),Q(b,nn if nn in (1,3) else 3),int(nn==3))
    d=json.loads(z.read('gram_reconstruction_certificate.json'))
    tree=[tuple(e) for e in d['spanning_tree_edges']]
    T=nx.Graph();T.add_nodes_from(range(40));T.add_edges_from(tree)
    assert len(tree)==39 and nx.is_tree(T)
    gauge={0:(Q(1),Q(0),0)};seed=(Q(1,3),Q(0),1)
    for u,v in nx.bfs_edges(T,0):gauge[v]=emul(gauge[u],emul(econj(H[u,v]),einv(seed)))
    known={(i,i):(Q(1),Q(0),0) for i in range(40)}
    for u,v in tree:known[u,v]=known[v,u]=seed
    for step in d['steps']:
        i,j,k=step['triangle'];u,v=step['recovered_oriented_edge'];links=[(i,j),(j,k),(k,i)]
        assert [x for x in links if x not in known]==[(u,v)]
        target=emul(emul(H[i,j],H[j,k]),H[k,i]);product=(Q(1),Q(0),0)
        assert abs(enumeric(target)-complex(*step['triple_product']))<1e-13
        for edge in links:
            if edge in known:product=emul(product,known[edge])
        known[u,v]=emul(target,einv(product));known[v,u]=econj(known[u,v])
    edges=set(tuple(sorted(e)) for e in nx.complement(G).edges())
    assert len(d['steps'])==501 and all(e in known for e in edges)
    for (i,j),value in known.items(): assert value==emul(emul(econj(gauge[i]),H[i,j]),gauge[j])
    return dict(status='PASS',edges=540,tree_edges=39,exact_triangle_updates=501,
        exact_known_oriented_entries=len(known),field='Q(omega,sqrt(3))',
        scope='Constructive labeled-Gram rigidity by exact rational field replay, with fixed edge magnitudes and all listed labeled triple products. No support-only rigidity theorem or inference from mod-two homology alone.')

def ks_audit(z,G,bases,independent):
    d=json.loads(z.read('five_followup_results.json'))['KS_extension']
    c=json.loads(z.read('reye_exact_certificate.json'));base=set(c['primary_reye']+c['dual_reye'])
    bmask=[sum(1<<i for i in b) for b in bases]
    coverage=[sum(1<<j for j,b in enumerate(bases) if set(b)&set(S)) for S in independent]
    missing=np.array([((1<<40)-1)^x for x in coverage],dtype=np.uint64)
    def feasible(S):
        sm=sum(1<<i for i in S);active=sum(1<<j for j,b in enumerate(bmask) if b&sm==b)
        return bool(np.any((missing&np.uint64(active))==0))
    outside=sorted(set(G)-base);tested=0;ext=[]
    for k in range(7):
        for extra in it.combinations(outside,k):
            tested+=1
            if not feasible(base|set(extra)):ext.append(extra)
        if ext:break
    assert (k,len(ext),tested)==(6,48,14893)
    assert feasible(base)
    critical=set(d['ray_deletion_critical_subset']);contexts=[b for b in bases if set(b)<=critical]
    assert len(critical)==29 and len(contexts)==14 and G.subgraph(critical).number_of_edges()==132
    assert not feasible(critical) and coloring(G,bases,critical) is None
    deletions=d['deletion_coloring_witnesses']
    for i in critical:
        green=set(deletions[str(i)]);present=critical-{i}
        assert green<=present and not G.subgraph(green).number_of_edges()
        assert all(len(green&set(b))==1 for b in bases if set(b)<=present)
    # A separate search with only the fourteen tetrads must be satisfiable.
    context_only=nx.empty_graph(40)
    context_only.add_edges_from(e for b in contexts for e in it.combinations(b,2))
    basis_green=coloring(context_only,contexts,critical)
    assert basis_green is not None and all(len(set(b)&set(basis_green))==1 for b in contexts)
    return dict(status='PASS',relative_minimum=6,extensions=ext,candidate_subsets=tested,
        critical_rays=sorted(critical),tetrads=contexts,orthogonality_edges=132,basis_only_coloring=basis_green,
        single_deletion_colorings=deletions,scope='Minimum extension of this fixed paired-Reye union; no global KS minimum or fourteen-tetrad-only contradiction.')

def arrays_audit(z,G,bases,independent):
    V=numeric_vectors();P=np.array([np.outer(v,v.conj()) for v in V.T]);H=V.conj().T@V
    def npz(name):return np.load(io.BytesIO(z.read(name)),allow_pickle=False)
    with npz('witting_operators.npz') as x:
        assert np.allclose(x['rays'],V) and np.allclose(x['projectors'],P)
        F=x['operator_basis'];C=x['structure_constants']
        assert np.max(abs(F-F.conj().transpose(0,2,1)))<1e-13
        assert np.max(abs(np.trace(F,axis1=1,axis2=2)))<1e-13
        assert np.allclose(np.einsum('aij,bji->ab',F,F),np.eye(15),atol=1e-13)
        for a,b in it.product(range(15),repeat=2):
            assert np.linalg.norm(-1j*(F[a]@F[b]-F[b]@F[a])-np.einsum('c,cij->ij',C[a,b],F))<1e-12
        rows=list(csv.DictReader(io.StringIO(z.read('su4_structure_constants.csv').decode())));structure_rows=len(rows)
        seen=set()
        for row in rows:
            idx=tuple(int(row[k]) for k in 'abc');seen.add(idx)
            assert abs(float(row['coefficient'])-C[idx])<1e-13
        assert seen==set(zip(*np.where(abs(C)>1e-9)))
    with npz('witting_symmetry_and_phase_data.npz') as x:
        assert np.allclose(x['rays'],V)
        assert np.allclose(x['triple_products'],np.einsum('ij,jk,ki->ijk',H,H,H),atol=1e-13)
        supplied=x['unitary_group_permutations'].copy();pair=x['paired_reye_stabilizer'].copy()
        J=x['local_intertwiner'];K=x['canonical_qutrit_mub_rays'];W=V[1:,sorted(G[0])]
        scores=abs(K.conj().T@J@W)**2
        assert np.allclose(scores.max(axis=0),1) and len(set(scores.argmax(axis=0)))==12
    for name,expected in [('witting_bases.csv',bases),('witting_sics.csv',[c for c in independent if len(c)==4])]:
        rows=list(csv.DictReader(io.StringIO(z.read(name).decode())))
        assert [tuple(map(int,row['ray_ids'].split(','))) for row in rows]==expected
    assert all(np.linalg.matrix_rank(V[:,c],tol=1e-12)==2 for c in independent if len(c)==4)
    assert z.read('witting_sics.csv')==z.read('witting_sics (1).csv')
    with npz('reye_embedding.npz') as x:
        a,b=real_cells();R=np.array([np.array(v,float).ravel() for v in a]);mapping=x['point_correspondence']
        assert np.allclose(x['real_reye_rays'],R)
        for v,j in zip(R,mapping):assert np.linalg.norm((np.eye(4)-P[j])@x['real_to_witting_map']@v)<1e-12
        assert len(x['selected_lines'])==16 and len(x['selected_points'])==12
    # Exact triflection permutations: numerical labels are checked afterward.
    R=rays();exact_gens=[]
    for k in [0,1,2,3,4,13,22,31]:
        g=[];den=inner(R[k],R[k])[0]
        for v in R:
            coeff=mul((-1,1),inner(R[k],v)) # omega-1
            out=tuple((Q(a)+Q(x,den),Q(b)+Q(y,den)) for (a,b),(x,y) in zip(v,[mul(t,coeff) for t in R[k]]))
            hits=[]
            for j,w in enumerate(R):
                if all(mul(out[a],w[b])==mul(out[b],w[a]) for a,b in it.combinations(range(4),2)):hits.append(j)
            assert len(hits)==1;g.append(hits[0])
        exact_gens.append(np.array(g,dtype=np.uint8))
    ident=np.arange(40,dtype=np.uint8);group={ident.tobytes():ident};queue=deque([ident])
    while queue:
        p=queue.popleft()
        for g in exact_gens:
            q=p[g];key=q.tobytes()
            if key not in group:group[key]=q;queue.append(q)
    assert len(group)==25920 and {p.tobytes() for p in supplied}==set(group)
    c=json.loads(z.read('reye_exact_certificate.json'));rset=set(c['primary_reye']);dset=set(c['dual_reye'])
    orbit=set();pairs=set();r_stab=[];p_stab=[]
    def pairkey(a,b):return tuple(sorted((tuple(sorted(a)),tuple(sorted(b)))))
    target=pairkey(rset,dset)
    for p in group.values():
        r=tuple(sorted(map(int,p[list(rset)])));d=tuple(sorted(map(int,p[list(dset)])))
        orbit.add(r);pairs.add(pairkey(r,d))
        if set(r)==rset:r_stab.append(p)
        if pairkey(r,d)==target:p_stab.append(p)
    assert (len(orbit),len(pairs),len(r_stab),len(p_stab))==(540,270,48,96)
    assert {p.tobytes() for p in pair}=={p.tobytes() for p in p_stab}
    return dict(status='PASS',array_files=3,embedding_arrays=1,csv_structure_rows=structure_rows,
        projective_unitary_group=25920,exact_triflection_generators=[g.tolist() for g in exact_gens],
        Reye_orbit=540,paired_orbit=270,Reye_stabilizer=48,pair_stabilizer=96,
        scope='Every supplied array entry is loaded; ray/projector, algebra, phase, symmetry, embedding and CSV data are checked. Matrix-array checks use declared tolerances; group generation and generator projective matches use exact Eisenstein arithmetic.')

def produce():
    z,manifest=archive_inputs();G,bases,independent=graph_data()
    operation=instrument(z);print('exact paired instrument and magic preparation PASS',flush=True)
    gram=gram_audit(z,G);print('exact Gram reconstruction PASS',flush=True)
    ks=ks_audit(z,G,bases,independent);print('relative KS extension and deletion controls PASS',flush=True)
    arrays=arrays_audit(z,G,bases,independent);print('all supplied arrays and exact group PASS',flush=True)
    out=dict(status='PASS',pass_number=11630,input_archive_sha256=ARCHIVE_SHA,source_manifest=manifest,
        quarantined=['witting_experiment_results.json: truncated at147 bytes; rejected'],
        external_attribution='Supplied Perplexity artifacts own the Reye projective map, paired orbit and relative-extension witness. Both supplied scripts freshly replayed in an isolated output directory; first script uses pandas as well as declared numpy/scipy/networkx/sympy. First projective determinant may be -2/3 under a different correspondence/gauge, not an invariant contradiction.',
        instrument=operation,exact_Gram=gram,KS=ks,arrays=arrays,
        prior_art=['Pass4963 exact Witting/W33 point graph and Bargmann phase table','Pass8909-8916 complementary D4/Reye selector','11625-11629 Peres and coherent-query controls','Vlasov2208.13644v2 Witting coordinates,90 complex lines,measurement circuits'],
        boundary='An exact finite-geometry audit and an engineered quantum instrument. No observed masses, mixing, spacetime action, universal hardware or complete TOE is derived.')
    out['producer_sha256']=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    OUT.write_text(json.dumps(out,indent=2)+'\n')
    print('Pass11630 intake, exact Gram, relative KS search and heralded Reye instrument: PASS')
    return out

if __name__=='__main__':produce()
