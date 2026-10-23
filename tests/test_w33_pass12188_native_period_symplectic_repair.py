from pathlib import Path
import itertools,json,hashlib,sys
import numpy as np
import sympy as s
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12188_native_period_symplectic_repair as m

@pytest.fixture(scope='module')
def cert():return json.loads((ROOT/'data/w33_pass12188_native_period_symplectic_repair.json').read_text())

def test_source_and_native_provenance(cert):
    assert cert['source_sha256']==hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()
    assert cert['native_input_sha256']==hashlib.sha256((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_bytes()).hexdigest()
    assert all(v is False for v in cert['scope'].values())

def test_exact_all_integral_forms_and_pfaffian(cert):
    _,R=m.native();C=m.invariant_equations(R);basis=C.nullspace()
    assert [list(map(int,v))for v in basis]==cert['invariant_form_basis']
    a,b=s.symbols('a b');F=m.alternating(a*basis[0]+b*basis[1])
    assert s.factor(m.pfaffian(F))==-3*a*(a+b)
    # Coordinates z1=-a and z5=b certify saturation over Z, not just Q.
    assert F[0,2]==-a and F[2,3]==b
    assert s.factor(F.det())==9*a*a*(a+b)**2

def test_independent_all729_ternary_alternating_forms_are_degenerate():
    _,R=m.native();valid=[]
    for v in itertools.product(range(3),repeat=6):
        F=m.alternating(v)
        if all(all(int(x)%3==0 for x in M.T*F*M-F)for M in R.values()):valid.append(F)
    assert len(valid)==9 and all(int(F.det())%3==0 for F in valid)

def test_unique_blocking_is_among_all40_hyperplanes(cert):
    _,R,S,T=m.repaired()
    assert m.stable_hyperplanes(R)==[(0,0,1,2)]
    assert S.det()==3 and all(int(x)%3==0 for x in s.Matrix([[0,0,1,2]])*S)
    assert np.array_equal(np.array(S).astype(int)%2,np.eye(4,dtype=int))
    assert all(all(x.q==1 for x in M)for M in T.values())

def test_minimal_forms_both_repair_and_keep_binary_polar(cert):
    _,_,S,T=m.repaired()
    binary=json.loads((ROOT/'data/w33_pass12186_context_cover_holonomy.json').read_text())
    for row in cert['minimal_forms']:
        F=s.Matrix(row['original']);G=s.Matrix(row['repaired'])
        assert row['Smith_original']==[1,1,3,3]
        assert F.det()==9 and S.T*F*S==3*G and G.det()==1
        assert all(M.T*G*M==G for M in T.values())
        assert np.array_equal(np.array(F).astype(int)%2,binary['binary_quadric']['polar_matrix'])
    assert {r['repaired_pfaffian']for r in cert['minimal_forms']}=={-1,1}
    assert len(cert['repaired_projective_invariant_symplectic_forms'])==6

def test_period_and_logical_group_products_and_kernel(cert):
    _,R,S,T=m.repaired();rows=cert['logical_compiler']['actions'];Q={tuple(r['h']):np.array(r['matrix20_mod3'])for r in rows}
    for g,h in itertools.product(T,repeat=2):
        assert T[g]*T[h]==T[m.mul(g,h)]
        assert np.array_equal(Q[g]@Q[h]%3,Q[m.mul(g,h)])
    assert len({A.tobytes()for A in Q.values()})==9
    assert {g for g,A in Q.items()if np.array_equal(A,np.eye(20,dtype=int))}=={(0,0,c)for c in range(3)}

def test_actual_40_point_code_and_20_label_maps_recomputed(cert):
    _,_,_,T=m.repaired();G=s.Matrix(cert['minimal_forms'][0]['repaired'])
    assert m.logical_action(T,G)==cert['logical_compiler']
    rows=cert['logical_compiler']['actions']
    for row in rows:
        r=m.code.rank((np.array(row['matrix4_mod3'])-np.eye(4,dtype=int))%3,3)
        assert row['logical_ranks']=={0:[20,0,0,0],1:[20,10,3,0],2:[20,10,5,0]}[r]
    assert len({tuple(r['point_permutation'])for r in rows})==9

def test_six_distinct_connected_context_covers(cert):
    d,_=m.native();binary=json.loads((ROOT/'data/w33_pass12186_context_cover_holonomy.json').read_text());vec=np.array(list(itertools.product(range(2),repeat=4)));keys=set()
    for cover in cert['native_context_covers']:
        A=np.array(cover['binary_coefficients']);key=tuple(np.flatnonzero(np.all(vec@A.T%2==0,axis=1)));keys.add(key)
        row=next(x for x in binary['binary_successful_maps']if np.array_equal(np.array(x['coefficients']).reshape(2,4),A))
        assert m.connected_cover(d,row)==cover
        assert (cover['vertices'],cover['edges'],cover['connected'])==(324,1620,True)
    assert len(keys)==6

def test_unimodular_remarking_preserves_the_obstruction(cert):
    _,R=m.native();U=s.eye(4);U[0,1]=1;U[2,3]=-1
    F=s.Matrix(cert['minimal_forms'][0]['original']);Fnew=U.T*F*U
    assert Fnew.det()==9
    assert all((U.inv()*M*U).T*Fnew*(U.inv()*M*U)==Fnew for M in R.values())
    assert all(int(x)%3==0 for x in m.invariant_equations(R)*s.Matrix(cert['invariant_form_basis'][0]))

def test_discriminant_pairing_and_exact_qutrit_central_extension(cert):
    F=s.Matrix(cert['minimal_forms'][0]['original']);D=cert['discriminant_qutrit'];u,v=map(s.Matrix,D['representative_generators'])
    assert (u.T*F.inv()*v)[0]%1==s.Rational(1,3)
    classes=[a*u+b*v for a,b in itertools.product(range(3),repeat=2)]
    assert all(any(x.q!=1 for x in F.inv()*(a-b))for a,b in itertools.combinations(classes,2))
    H=list(itertools.product(range(3),repeat=3))
    for g,h in itertools.product(H,repeat=2):
        a,b,c=g;A,B,C=h;aa,bb,cc=m.mul(g,h)
        for t in range(3):assert (C-B*t+c-b*(t+A))%3==(cc-bb*t)%3
    # The centre acts as a nontrivial scalar, whereas the period action kills it.
    assert all((0,0,c) in {tuple(x)for x in cert['logical_compiler']['kernel']} for c in range(3))
    assert 'not an equivariant identification' in D['scope']

def test_modular_fixed_forms_jump_and_four_do_not_lift(cert):
    _,_,S,T=m.repaired();valid=[]
    for v in itertools.product(range(3),repeat=6):
        F=m.alternating(v)
        if all(all(int(x)%3==0 for x in M.T*F*M-F)for M in T.values()):valid.append(v)
    assert len(valid)==27
    assert np.array(cert['repaired_mod3_invariant_form_basis']).shape==(3,6)
    expected=[v for v in valid if any(v) and next(x for x in v if x)==1 and int(m.pfaffian(m.alternating(v)))%3]
    assert list(map(list,expected))==cert['repaired_projective_invariant_symplectic_forms']
    assert sum(int(m.pfaffian(m.alternating(v)))%3==1 for v in expected)==3
    assert sum(int(m.pfaffian(m.alternating(v)))%3==2 for v in expected)==3
    integral=[]
    for v in cert['invariant_form_basis']:
        G=S.T*m.alternating(v)*S/3
        assert all(x.q==1 for x in G)
        integral.append([int(G[i,j])%3 for i,j in m.PAIRS])
    span={tuple((a*np.array(integral[0])+b*np.array(integral[1]))%3)for a,b in itertools.product(range(3),repeat=2)}
    assert len(span)==9
    assert sum(v in span for v in expected)==2
