"""Four native period directions from the augmented H27 two-complex.

The choice of two character planes is explicit. Six such H27-invariant
four-spaces exist; none admits an H27-invariant Lorentz metric. A free GW
kernel on one connected cover is built; a chiral gauge measure is not.
"""
import itertools
import json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.linalg import eigh,svdvals
from sympy.matrices.normalforms import hermite_normal_form
from w33_20261015_toe85_h2_relation_module import geometry
from w33_20261015_toe82_native_H27_h1_character import mul
from w33_pass11980_heisenberg_fixed_holonomies import DIRECTIONS

ROOT=Path(__file__).resolve().parents[1]
CHARACTERS=((1,0),(0,1),(1,1),(1,2))


def native_geometry():
    H,faces,_=geometry();F=s.Matrix(faces);idx={g:i for i,g in enumerate(H)}
    triangles=sorted({tuple(sorted(idx[mul(g,t)] for t in ((0,0,0),d,mul(d,d)))) for g in H for d in DIRECTIONS})
    edges=sorted({e for f in triangles for e in itertools.combinations(f,2)});ei={e:i for i,e in enumerate(edges)}
    B=s.zeros(27,135)
    for j,(a,b) in enumerate(edges):B[a,j]=-1;B[b,j]=1
    actions=[]
    for g in H:
        p=[idx[mul(g,h)] for h in H];T=s.zeros(135)
        for j,(a,b) in enumerate(edges):T[ei[tuple(sorted((p[a],p[b])))],j]=1 if p[a]<p[b] else -1
        actions.append(T)
    assert B*F.T==s.zeros(27,99)
    return H,edges,B,F,actions


def cover_data():
    H,edges,B,F,actions=native_geometry();planes=[]
    full_kernel=B.col_join(F).nullspace()
    assert len(full_kernel)==26
    K=s.Matrix.hstack(*full_kernel)
    central=sum((T for g,T in zip(H,actions) if g[0]==g[1]==0),s.zeros(135))
    averaged=sum(actions,s.zeros(135))
    assert (central*K).rank()==8 and averaged*K==s.zeros(135,26)
    for a,b in CHARACTERS:
        numerator=sum(((2 if (a*g[0]+b*g[1])%3==0 else -1)*T for g,T in zip(H,actions)),s.zeros(135))
        kernel=B.col_join(F).col_join(numerator-27*s.eye(135)).nullspace()
        assert len(kernel)==2
        columns=[]
        for v in kernel:
            v=v*s.ilcm(*[x.q for x in v]);v=v/s.igcd(*list(v));columns.append(v)
        plane=s.Matrix.hstack(*columns)
        assert B*plane==s.zeros(27,2) and F*plane==s.zeros(99,2)
        planes.append(plane)
    C=planes[0].row_join(planes[1]);assert s.Matrix.hstack(*planes).rank()==8
    # Gauge away a spanning tree, then use the actual cycle-period image,
    # not Z4 by declaration, to make the connected deck lattice primitive.
    potential={0:s.zeros(1,4)};queue=[0]
    for a in queue:
        for e,(u,v) in enumerate(edges):
            if u==a and v not in potential:potential[v]=potential[a]+C[e,:];queue.append(v)
            if v==a and u not in potential:potential[u]=potential[a]-C[e,:];queue.append(u)
    assert len(potential)==27
    raw=s.Matrix.vstack(*[C[e,:]+potential[a]-potential[b] for e,(a,b) in enumerate(edges)])
    assert all(x.q==1 for x in raw)
    # Division during primitive-vector normalization can leave SymPy's
    # DomainMatrix in QQ even when every entry is integral; HNF needs ZZ.
    raw=s.Matrix(raw.rows,raw.cols,[s.Integer(x) for x in raw])
    lattice=hermite_normal_form(raw.T);assert lattice.shape==(4,4)
    V=raw*lattice.T.inv();harmonic=C*lattice.T.inv()
    assert all(x.q==1 for x in V)
    integral_V=s.Matrix(V.rows,V.cols,[s.Integer(x) for x in V])
    assert hermite_normal_form(integral_V.T)==s.eye(4)
    assert F*V==s.zeros(99,4) and B*harmonic==s.zeros(27,4)
    metric=harmonic.T*harmonic/27;left=(harmonic.T*harmonic).inv()*harmonic.T
    assert all(metric[:i,:i].det()>0 for i in range(1,5))
    deck_actions=[]
    for T in actions:
        M=left*T*harmonic
        assert T*harmonic==harmonic*M and all(x.q==1 for x in M) and abs(M.det())==1
        deck_actions.append(M)
    coefficients=s.symbols('g0:10');G=s.zeros(4)
    for z,(i,j) in zip(coefficients,itertools.combinations_with_replacement(range(4),2)):G[i,j]=G[j,i]=z
    equations=[]
    for g in ((1,0,0),(0,1,0)):
        # HNF can mix the two character lattices through finite-index
        # gluing. State the block-signature proof in character coordinates,
        # while retaining primitive integral deck matrices above.
        M=lattice.T.inv()*deck_actions[H.index(g)]*lattice.T
        equations.extend(list(M.T*G*M-G))
    matrix,_=s.linear_eq_to_matrix(equations,coefficients);invariants=matrix.nullspace()
    assert len(invariants)==2
    assert all(v[2]==v[3]==v[5]==v[6]==0 for v in invariants)  # no cross-plane terms
    return H,edges,B,F,V,harmonic,metric,deck_actions,planes,invariants,lattice


def bloch_incidence(edges,voltages,k,phases=None):
    phase=np.exp(1j*(voltages@np.asarray(k)+(np.zeros(135) if phases is None else phases)))
    B=np.zeros((135,27),complex);C=np.zeros_like(B)
    for e,(a,b) in enumerate(edges):B[e,a]=-1;B[e,b]=phase[e];C[e,a]=.5;C[e,b]=.5*phase[e]
    return B,C


def gamma4():
    X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
    gamma=[np.kron(X,X),np.kron(X,Y),np.kron(X,Z),np.kron(Z,np.eye(2))]
    chir=np.linalg.multi_dot(gamma)
    return gamma,chir


def polarized_lorentz_repair(H,actions,lattice):
    """Use the independently rank-selected TOE84/85 subgroup, not its size."""
    peer=json.loads((ROOT/'data/w33_20261015_toe85_h2_relation_module.json').read_text())
    A={tuple(g) for g in peer['F3']['H2_rank8_polarization']}
    previous=json.loads((ROOT/'data/w33_20261015_toe84_h27_logical_clifford.json').read_text())
    assert A=={tuple(g) for g in previous['ternary_rank16_polarization']}=={(0,b,c) for b in range(3) for c in range(3)}
    # A fixes the whole(1,0)-character plane. Choose one timelike line
    # in that plane; its selection and the sign of eta remain extra inputs.
    eta_character=s.diag(-1,1,1,1);eta_character[2,3]=eta_character[3,2]=-s.Rational(1,2)
    eta=lattice.inv()*eta_character*lattice.T.inv()
    clock=lattice.T[:,0]
    fixed={g for g,M in zip(H,actions) if M*clock==clock}
    preserved={g for g,M in zip(H,actions) if M.T*eta*M==eta}
    assert fixed==preserved==A
    assert (clock.T*eta*clock)[0]==-1
    equations=[];z=s.symbols('z0:4');v=s.Matrix(z)
    for g,M in zip(H,actions):
        if g in A:equations.extend(list(M*v-v))
    matrix,_=s.linear_eq_to_matrix(equations,z)
    assert len(matrix.nullspace())==2
    return dict(selected_subgroup=[list(g) for g in sorted(A)],
        matches_TOE84_H1_and_TOE85_H2_polarization=True,A_fixed_real_clock_plane_dimension=2,
        compatible_four_period_choices_containing_clock_plane=3,
        example_metric_in_character_coordinates=[[str(x) for x in row] for row in eta_character.tolist()],
        example_metric_in_primitive_deck_coordinates=[[str(x) for x in row] for row in eta.tolist()],
        clock_vector_primitive_coordinates=list(map(str,clock)),clock_norm_squared='-1',signature_negative_positive=[1,3],
        exact_metric_and_clock_stabilizer=[list(g) for g in sorted(preserved)],
        result='The SAME order9 maximalcommuting subgroup selected independently by ternaryH1/H2 ranks fixes a real2plane in thisnative4period quotient. BreakingH27 toA permits a genuine3+1 invariantmetric; the displayed rationalmetric and timelikevector have EXACTstabilizerA. The fullH27 Lorentzobstruction isnotuniversalafterbreaking.',
        open_choices='TOE83 squareorbitchoice andcharacteristic3 rankcriterion selectA combinatorially, not dynamically. Three4periodquotientchoices includeitsclockplane. The timelikelinewithinthatplane, Lorentziansignature itself, timeorientation, action andphysicalclocks are not selected.')


def overlap(edges,V,current,k,phases=None,mass=.5):
    B,C=bloch_incidence(edges,V,k,phases);L=B.conj().T@B;gamma,chir=gamma4()
    derivative=[C.conj().T@(current[:,i,None]*B) for i in range(4)]
    assert max(np.max(abs(d+d.conj().T)) for d in derivative)<1e-11
    DW=sum(np.kron(g,d) for g,d in zip(gamma,derivative))+np.kron(np.eye(4),L-mass*np.eye(27))
    G5=np.kron(chir,np.eye(27));Q=G5@DW
    assert np.max(abs(Q-Q.conj().T))<1e-10
    ev,U=eigh(Q);assert min(abs(ev))>1e-8
    D=np.eye(108)+G5@(U*np.sign(ev))@U.conj().T
    GW=float(np.max(abs(D@G5+G5@D-D@G5@D)))
    return D,Q,G5,dict(gap=float(min(abs(ev))),index=int(round(-sum(np.sign(ev))/2)),GW=GW)


def payload():
    H,edges,B,F,V,C,G,actions,planes,invariants,lattice=cover_data()
    vf=np.array(V,float);cf=np.array(C,float);gf=np.array(G,float)
    current=27*cf@np.linalg.inv(cf.T@cf)
    assert np.max(abs(np.array(B,float)@current))<1e-12
    acoustic=[];p=np.array([.2,-.3,.4,.5]);p/=np.linalg.norm(p)
    for a in (.04,.02,.01,.005):
        b,_=bloch_incidence(edges,vf,a*p);lam=float(np.linalg.eigvalsh(b.conj().T@b)[0])
        target=float(p@gf@p);acoustic.append(dict(spacing=a,lambda_over_spacing2=lam/a**2,quadratic_target=target,error=abs(lam/a**2-target)))
    assert acoustic[-1]['error']<acoustic[0]['error']/30
    D,Q,G5,origin=overlap(edges,vf,current,np.zeros(4));assert sum(svdvals(D)<1e-9)==4 and origin['index']==0
    dirac=[]
    for a in (.02,.01,.005):
        D,*_,control=overlap(edges,vf,current,a*p);low=np.sort(svdvals(D))[:4]*.5/a
        dirac.append(dict(spacing=a,scaled_singular_values=low.tolist(),max_error=float(max(abs(low-1))),**control))
    assert dirac[-1]['max_error']<dirac[0]['max_error']/2
    corners=[]
    for bits in itertools.product((0,1),repeat=4):
        d,*_,control=overlap(edges,vf,current,np.pi*np.array(bits))
        corners.append(dict(bits=list(bits),smallest_D_singular=float(min(svdvals(d))),**control))
    phases=np.random.default_rng(11991).uniform(-.04,.04,135);theta=np.linspace(-.5,.7,27)
    d,*_,random=overlap(edges,vf,current,np.zeros(4),phases)
    shifted=phases+np.array([theta[b]-theta[a] for a,b in edges]);dg,*_=overlap(edges,vf,current,np.zeros(4),shifted)
    U=np.kron(np.eye(4),np.diag(np.exp(1j*theta)));cov=float(np.max(abs(dg-U.conj().T@d@U)));assert cov<1e-10
    return dict(status='PASS',source='TOE83 augmented tritangent2complex, via TOE85 signedface geometry',
        cells=dict(vertices=27,edges=135,faces=99),H1_real_dimension=26,
        four_linear_character_planes=[dict(character=list(char),dimension=2,integer_harmonic_columns=plane.tolist()) for char,plane in zip(CHARACTERS,planes)],
        center_invariant_H1_dimension=8,center_faithful_minimum_real_irreducible_dimension=6,
        exact_harmonic_kernel_dimension=26,exact_full_group_fixed_dimension=0,
        possible_H27_invariant_real_rank4_quotients=6,
        selection='Pick characterplanes(1,0),(0,1) ofthefour; thispairchoiceisNOTselectedbytheaction. H27center actstrivially. Allsixchoices are nonfaithful4D realdecks.',
        raw_period_lattice_basis=lattice.tolist(),raw_period_index=int(abs(lattice.det())),
        primitive_integer_edge_voltages=V.tolist(),harmonic_voltages_Q=[[str(x) for x in row] for row in C.tolist()],
        exact_acoustic_metric=[[str(x) for x in row] for row in G.tolist()],
        exact_deck_actions=[dict(h=list(g),matrix=M.tolist()) for g,M in zip(H,actions)],
        invariant_metric_dimension=2,invariant_metric_nullspace_in_character_coordinates=[list(map(str,v)) for v in invariants],
        Lorentz_signature_obstruction='The two distinct nontrivial realC3 characterplanes are irreducible, inequivalent and have no cross invariantbilinearforms. Eachplane invariantmetric is a scalar multipleof a positivedefiniteform. Nondegenerate signatures are(4,0),(2,2),(0,4), never(3,1). Thus preservingthisH27 action cannotselect a physicalLorentzianmetric; time direction requires further symmetry breaking or changedcarrier.',
        parallel_polarization_Lorentz_repair=polarized_lorentz_repair(H,actions,lattice),
        cover_theorem='Treegauge and integralHNF give primitive rank4 cycleperiods, hence connected Z4-cover with27sites/cell. All99faceboundaries havezero deckvoltage. Its scalar BlochLaplacian has a singlequadratic acoustic band with positive4x4 metricG=(C.T C)/27; localCLT/periodicgraph analysis gives spectraldimension4. Four dimensions ariseafter anexplicit rank4quotientchoice, not fromauniquevacuum.',
        acoustic_refinement=acoustic,free_overlap_origin=origin,free_overlap_low_momentum=dirac,Brillouin_corner_controls=corners,
        random_link_control=random,gauge_covariance_max=cov,
        chiral_projector='Dov=I+gamma5 sign(gamma5 DW), DW=sum gamma_i D_i+L-.5. hatgamma5=-signQ gives exact modified Weylprojectors wheneverQ isgapped. Standard11984 anomalyfreeSU5 matter can beplacedonthiscarrier asadditionalcontent.',
        boundary='A selectednative4D periodicEuclideancover and free/finitelytested gaugecovariant GWkernel; no uniformallmomentum/allgauge gap/localitytheorem, globalnonAbelianWeylmeasure, interactingcontinuum, Lorentziantimeselection, derivedthreefamilies orphysicalgravity.',
        prior=['TOE83/84 codeH1 and chainactions','TOE85 H2/radicalmodule','analysis/2026-10-15_toe87_five_followups.md owns the binary semisimple multiplicities, Euler identity and three-orbit selector counterexample','analysis/2026-10-15_toe88_five_followups.md owns the binary augmentation equivalence and ternary failure','11977 earlier3Dnativecover plus suppliedtime overlap','11389 nativeparabolic3Dcover','Oct9 universalabeliancover andnoequivariant3space','11984 suppliedT4 hybrid regulator'],
        primary=['https://doi.org/10.1090/S0002-9947-00-02632-5','https://arxiv.org/abs/hep-lat/9801031'])


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11991_native_four_period_cover.json').write_text(json.dumps(d,indent=2,default=int)+'\n');print(d['status'],d['exact_acoustic_metric'],d['invariant_metric_dimension'])
