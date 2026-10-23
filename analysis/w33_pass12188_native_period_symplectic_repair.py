"""Exact native-period ternary repair, preserving the binary context geometry.

Builds a declared algebraic/coarse-cell bridge, not a causal Lorentzian action.
Native11991 matrices and12186 binary witnesses are prior inputs.
"""
from pathlib import Path
from collections import deque, Counter
import itertools,json,hashlib
import numpy as np
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
import w33_20261022_pascal_css_logical_transvection_jordan as code
ROOT=Path(__file__).resolve().parents[1]
PAIRS=list(itertools.combinations(range(4),2))


def mul(g,h):
    a,b,c=g;A,B,C=h
    return ((a+A)%3,(b+B)%3,(c+C-b*A)%3)


def alternating(v):
    F=s.zeros(4)
    for x,(i,j) in zip(v,PAIRS):F[i,j]=x;F[j,i]=-x
    return F


def pfaffian(F):
    return s.expand(F[0,1]*F[2,3]-F[0,2]*F[1,3]+F[0,3]*F[1,2])


def native():
    d=json.loads((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_text())
    R={tuple(x['h']):s.Matrix(x['matrix']).inv().T for x in d['exact_deck_actions']}
    assert all(all(v.q==1 for v in M) for M in R.values())
    return d,R


def invariant_equations(R):
    z=s.symbols('z:6');F=alternating(z)
    C,_=s.linear_eq_to_matrix([x for M in R.values() for x in M.T*F*M-F],z)
    return C


def stable_hyperplanes(R):
    out=[]
    for v in code.projective_points(3):
        a=s.Matrix(1,4,v)
        if all(all(int((a*M)[i]*a[j]-(a*M)[j]*a[i])%3==0 for i,j in PAIRS)for M in R.values()):out.append(v)
    return out


def repaired():
    d,R=native();S=s.eye(4);S[2,2]=3;S[2,3]=-2
    T={g:S.inv()*M*S for g,M in R.items()}
    assert all(all(x.q==1 for x in M)for M in T.values())
    return d,R,S,T


def logical_action(T,G):
    points=code.projective_points(3);X=np.array(points,dtype=int);index={v:i for i,v in enumerate(points)}
    B=((X@np.array(G).astype(int)@X.T)%3!=0).astype(int)
    C,_=code.rref(B,3);N=code.right_kernel(B,3)
    F=C.copy()
    for row in N:
        if code.rank(np.vstack((F,row)),3)>len(F):F=np.vstack((F,row))
    assert F.shape==(30,40)
    _,piv=code.rref(F,3);inv=np.array(s.Matrix(F[:,piv]).inv_mod(3)).astype(int)
    L=F[10:];module={};actions=[]
    for g,M in T.items():
        # Inverse point map gives a genuine right-action permutation matrix.
        P=np.array(M.inv()).astype(int)%3
        perm=[index[code.normalize(P@x,3)] for x in X]
        matrix=np.zeros((40,40),int);matrix[np.arange(40),perm]=1
        assert np.array_equal(matrix@B@matrix.T%3,B)
        coeff=(L@matrix)[:,piv]@inv%3
        assert np.array_equal(coeff@F%3,L@matrix%3)
        Q=coeff[:,10:];module[g]=Q
        D=(Q-np.eye(20,dtype=int))%3;ranks=[20];powD=np.eye(20,dtype=int)
        for _ in range(3):powD=powD@D%3;ranks.append(code.rank(powD,3))
        actions.append({'h':list(g),'matrix4_mod3':(np.array(M).astype(int)%3).tolist(),
                        'point_permutation':perm,'matrix20_mod3':Q.tolist(),'logical_ranks':ranks})
    assert all(np.array_equal(module[g]@module[h]%3,module[mul(g,h)])for g,h in itertools.product(T,repeat=2))
    assert len({Q.tobytes()for Q in module.values()})==9
    return {'dimension':20,'code_rank':len(C),'quotient_basis':L.tolist(),
            'image_order':9,'kernel':[list(g)for g,Q in module.items() if np.array_equal(Q,np.eye(20,dtype=int))],
            'rank_spectrum':{str(k):v for k,v in Counter(tuple(a['logical_ranks'])for a in actions).items()},
            'actions':actions}


def connected_cover(d,colour_row):
    H=list(itertools.product(range(3),repeat=3));idx={g:i for i,g in enumerate(H)}
    directions=((0,0,1),(0,1,1),(1,0,1),(1,1,0),(1,2,2))
    E=sorted({tuple(sorted((idx[g],idx[mul(g,t)])))for g in H for z in directions for t in(z,mul(z,z))})
    V=np.array(d['primitive_integer_edge_voltages'],int);A=np.array(colour_row['coefficients']).reshape(2,4)
    gain2=V@A.T%2;gain2=gain2[:,0]+2*gain2[:,1];gain3=V@np.array([0,0,1,2])%3
    edges=set();adj=[[]for _ in range(324)]
    def vertex(t,z,v):return (4*t+z)*27+v
    colours=[int(colour_row['vertex_colours'][v])^z for t in range(3)for z in range(4)for v in range(27)]
    for t,z in itertools.product(range(3),range(4)):
        for (u,v),a,b in zip(E,gain2,gain3):
            edge=tuple(sorted((vertex(t,z,u),vertex((t+int(b))%3,z^int(a),v))))
            edges.add(edge)
    for u,v in edges:
        assert colours[u]!=colours[v];adj[u].append(v);adj[v].append(u)
    seen={0};queue=deque([0])
    while queue:
        for v in adj[queue.popleft()]:
            if v not in seen:seen.add(v);queue.append(v)
    assert len(seen)==324 and len(edges)==1620 and all(len(n)==10 for n in adj)
    return {'vertices':324,'edges':1620,'connected':True,'deck':'Z3 x V4',
            'ternary_functional':[0,0,1,2],'binary_coefficients':A.tolist(),
            'colouring':colours,'edge_sha256':hashlib.sha256(json.dumps(sorted(edges)).encode()).hexdigest()}


def discriminant_qutrit(F):
    inverse=F.inv();K=3*inverse
    assert all(x.q==1 for x in K)
    i,j=next((i,j)for i,j in PAIRS if int(K[i,j])%3)
    u=s.eye(4)[:,i];v=pow(int(K[i,j])%3,-1,3)*s.eye(4)[:,j]
    assert int((u.T*K*v)[0])%3==1
    classes=[a*u+b*v for a,b in itertools.product(range(3),repeat=2)]
    for x,y in itertools.combinations(classes,2):assert any(t.q!=1 for t in inverse*(x-y))
    # Exact exponent arithmetic verifies a concrete 3D monomial representation.
    H=list(itertools.product(range(3),repeat=3))
    for g,h in itertools.product(H,repeat=2):
        a,b,c=g;A,B,C=h;aa,bb,cc=mul(g,h)
        for t in range(3):
            assert (t+A+a)%3==(t+aa)%3
            assert (C-B*t+c-b*(t+A))%3==(cc-bb*t)%3
    return {'Smith_type':[1,1,3,3],'group':'D=coker(F)=F3^2',
            'representative_generators':[list(map(int,u)),list(map(int,v))],
            'pairing':'x^T F^-1 y mod Z; displayed generators have pairing1/3 mod Z',
            'central_extension':'H27: (a,b,c)(A,B,C)=(a+A,b+B,c+C-b*A)',
            'qutrit_action':'W(a,b,c)|t>=omega^(c-b*t)|t+a>; omega=exp(2*pi*i/3)',
            'scope':'Associated discriminant Heisenberg group with supplied central character, not an equivariant identification with the native address action, a derived quantization law or a non-Clifford resource.'}


def build():
    d,R,S,T=repaired();C=invariant_equations(R);N=C.nullspace()
    assert N==[s.Matrix([-3,-1,-2,2,1,0]),s.Matrix([0,0,0,0,0,1])]
    a,b=s.symbols('a b');F=alternating(a*N[0]+b*N[1]);pf=s.factor(pfaffian(F))
    assert pf==-3*a*(a+b)
    # Independent exhaustive characteristic3 check, not just rational reduction.
    C3=np.array(C).astype(int)%3
    inv3=[v for v in itertools.product(range(3),repeat=6)if not np.any(C3@v%3)]
    assert len(inv3)==9 and all(int(pfaffian(alternating(v)))%3==0 for v in inv3)
    assert stable_hyperplanes(R)==[(0,0,1,2)]
    binary=json.loads((ROOT/'data/w33_pass12186_context_cover_holonomy.json').read_text())
    G=[];forms=[]
    for bv in(0,-2):
        F0=F.subs({a:1,b:bv});G0=S.T*F0*S/3
        assert all(x.q==1 for x in G0)and G0.det()==1
        assert all(M.T*G0*M==G0 for M in T.values())
        assert np.array_equal(np.array(F0).astype(int)%2,np.array(binary['binary_quadric']['polar_matrix']))
        assert np.array_equal(np.array(S).astype(int)%2,np.eye(4,dtype=int))
        forms.append({'a':1,'b':bv,'original':np.array(F0).astype(int).tolist(),
                      'Smith_original':[abs(int(x))for x in smith_normal_form(F0,domain=s.ZZ).diagonal()],
                      'repaired':np.array(G0).astype(int).tolist(),'repaired_pfaffian':int(pfaffian(G0))})
        G.append(G0)
    Cnew=np.array(invariant_equations(T)).astype(int)%3
    modular_basis=code.right_kernel(Cnew,3)
    assert modular_basis.shape==(3,6)
    repaired_nondegenerate=[]
    for v in itertools.product(range(3),repeat=6):
        if any(v) and next(x for x in v if x)==1 and not np.any(Cnew@v%3) and int(pfaffian(alternating(v)))%3:
            repaired_nondegenerate.append(v)
    assert len(repaired_nondegenerate)==6
    for g,h in itertools.product(R,repeat=2):assert R[g]*R[h]==R[mul(g,h)] and T[g]*T[h]==T[mul(g,h)]
    representatives={}
    vectors=np.array(list(itertools.product(range(2),repeat=4)))
    for row in binary['binary_successful_maps']:
        A=np.array(row['coefficients']).reshape(2,4)
        key=tuple(map(int,np.flatnonzero(np.all(vectors@A.T%2==0,axis=1))))
        representatives.setdefault(key,row)
    covers=[connected_cover(d,row)for row in representatives.values()]
    assert len(covers)==6
    return {'status':'EXACT_LATTICE_REPAIR_AND_EXPLICIT_FINITE_LOGICAL_COMPILER',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'native_input_sha256':hashlib.sha256((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_bytes()).hexdigest(),
            'invariant_form_basis':[list(map(int,v))for v in N],'Pfaffian':str(pf),
            'ternary_invariant_forms_including_zero':len(inv3),'ternary_nondegenerate_before_repair':0,
            'unique_stable_index3_hyperplane':[0,0,1,2],'blocking_basis':np.array(S).astype(int).tolist(),
            'minimal_forms':forms,'repaired_mod3_invariant_form_basis':modular_basis.tolist(),
            'repaired_projective_invariant_symplectic_forms':[list(v)for v in repaired_nondegenerate],
            'binary_context_geometry_preserved':True,
            'discriminant_qutrit':discriminant_qutrit(s.Matrix(forms[0]['original'])),
            'logical_compiler':logical_action(T,G[0]),'native_context_covers':covers,
            'scope':{'original_mod3_symplectic':False,'native_H27_faithful_logically':False,
                     'selected_Lorentz_clock':False,'selected_particle_families':False,
                     'derived_continuum_action':False},
            'boundary':'Index3 blocking is a declared integral module repair, not a GL4Z basis change. Symplectic form rescaling is supplied; two minimal signs remain. Built connected12sheet cover and encoded Clifford label maps are finite witnesses, not physical gate routing or a TOE.'}


if __name__=='__main__':
    result=build();out=ROOT/'data/w33_pass12188_native_period_symplectic_repair.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'certificate':str(out),'Pfaffian':result['Pfaffian'],
                      'logical_rank_spectrum':result['logical_compiler']['rank_spectrum'],
                      'cover_sizes':[(r['vertices'],r['edges'])for r in result['native_context_covers']]}))
