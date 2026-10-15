"""Native opposite-shell E6 charts: overlap obstruction and projector descent.

TOE79 owns each canonical shell completion. Here all forty completions are
assembled explicitly; no common 27D fiber or four-manifold is assumed.
"""
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp
from w33_pass11980_heisenberg_fixed_holonomies import field_basis

from w33_pass1081_1086_core import build_w33, symp

ROOT = Path(__file__).resolve().parents[1]


def holonomy_closure(embedded,transport,denominator,A):
    q=sp.Matrix(embedded[0].tolist());cols=q.rref()[1];basis=q[:,list(cols)]
    rows=basis.T.rref()[1];square=basis[list(rows),:]
    left=sp.zeros(6,40)
    for j,r in enumerate(rows):left[:,r]=square.inv()[:,j]
    den=sp.ilcm(*[v.q for v in left]);ln=np.array(left*den,dtype=np.int64);bn=np.array(basis,dtype=np.int64)
    triangles=[(0,r,s) for r,s in itertools.combinations(range(1,40),2) if not A[0,r] and not A[0,s] and not A[r,s]]
    selected=[triangles[int(i)] for i in np.linspace(0,len(triangles)-1,20)]
    def product(x,y):
        a,b=x;c,d=y
        return a@c+3*b@d,a@d+b@c
    loops=[]
    divisor=int(den)*denominator**3
    for p,r,s in selected:
        lhs=tuple((ln@v).astype(object) for v in transport[0,s])
        rhs=tuple((v@bn).astype(object) for v in transport[r,0])
        raw=product(product(lhs,tuple(v.astype(object) for v in transport[s,r])),rhs)
        loops.append(tuple(np.array([[Fraction(int(v),divisor) for v in row] for row in m],dtype=object) for m in raw))
    witness=None
    for i in range(len(loops)):
        for j in range(i+1,len(loops)):
            trace=tuple(sum(m[k,k] for k in range(6)) for m in product(loops[i],loops[j]))
            if any(x.denominator!=1 for x in trace):
                witness=dict(triangles=[selected[i],selected[j]],trace_Q_sqrt3=[str(x) for x in trace]);break
        if witness:break
    # Rank over a residue field lower-bounds exact characteristic-zero rank.
    pairs=list(itertools.combinations(range(6),2))
    def commutant(prime):
        root=next(r for r in range(prime) if r*r%prime==3)
        def reduce_fraction(x):return x.numerator*pow(x.denominator,-1,prime)%prime
        constraints=[];ranks=[]
        for aa,bb in loops[:8]:
            h=np.array([[reduce_fraction(aa[i,j])+root*reduce_fraction(bb[i,j]) for j in range(6)] for i in range(6)],dtype=np.int64)%prime
            wedge=np.array([[h[i,k]*h[j,l]-h[i,l]*h[j,k] for k,l in pairs] for i,j in pairs],dtype=np.int64)%prime
            constraints.append(np.kron(wedge.T,np.eye(15,dtype=np.int64))-np.kron(np.eye(15,dtype=np.int64),wedge))
            rank=field_basis(np.concatenate(constraints),prime).shape[1];ranks.append(rank)
            if rank==224:break
        return root,ranks
    prime=1009;root,ranks=commutant(prime);root2,ranks2=commutant(1021)
    assert ranks[-1]==ranks2[-1]
    def exact_matrix(pair):
        return sp.Matrix(pair[0].tolist())+sp.sqrt(3)*sp.Matrix(pair[1].tolist())
    determinants=[sp.simplify(exact_matrix(loop).det(method='domain-ge')) for loop in loops[:3]]
    assert determinants==[-1,-1,-1]
    determinant=determinants[0]
    full=witness is not None and ranks[-1]==224
    return dict(triangle_generators_checked=[list(x) for x in selected],
        exact_infinite_order_product_witness=witness,
        wedge2_commutant_modular_rank=ranks[-1],wedge2_commutant_rank_progress=ranks,
        residue_prime=prime,sqrt3_residue=root,commutant_variables=225,
        independent_second_prime=1021,second_sqrt3_residue=root2,second_rank_progress=ranks2,
        first_triangle_determinant=str(determinant),full_compact_closure_O6_proved=full and determinant==-1,
        first_three_triangle_determinants=[str(d) for d in determinants],
        source_fiber_Gram=np.array(basis.T*basis,dtype=int).tolist(),
        first_three_loop_matrices_Q_sqrt3=[dict(triangle=list(selected[i]),rational=[[str(v) for v in row] for row in loops[i][0]],sqrt3_coefficient=[[str(v) for v in row] for row in loops[i][1]]) for i in range(3)],
        identity_component_SO6_proved=full,
        proof='A product trace with nonintegral coefficients in Q(sqrt3) is not an algebraic integer because O_Qsqrt3=Z[sqrt3]; hence it has infinite order. The compact holonomy closure therefore has nonzero Lie algebra inside so6. Rank224 of225 commutant equations proves the wedge2 representation irreducible overR (orthogonal reducibility would give a nonscalar commuting projector). Its nonzero invariant holonomy Lie algebra is allso6, so the identity component isSO6. This conclusion is used only if both checks pass.',
        boundary='A mathematical compact holonomy closure of the chosen finite polar connection; not a derived physical gauge group, coupling, spin lift, spacetime or Einstein equations.')


def payload():
    pts,_,lines,*_=build_w33()
    A=np.array([[int(i!=j and symp(x,y)==0) for j,y in enumerate(pts)] for i,x in enumerate(pts)],dtype=np.int64)
    assert np.array_equal(A@A,8*np.eye(40,dtype=int)-2*A+4*np.ones((40,40),dtype=int))
    chart={}; assembled=np.zeros((40,40),dtype=np.int64);embedded={}
    graph_sum=np.zeros_like(assembled)
    for p in range(40):
        opp=[q for q in range(40) if q!=p and not A[p,q]]
        assert len(opp)==27
        # Canonical center fibers: the three other points of <p,q>.
        fibers=set()
        for q in opp:
            span=[]
            for r in opp:
                if any(all((a*pts[p][k]+b*pts[q][k]-c*pts[r][k])%3==0 for k in range(4))
                       for a,b,c in itertools.product(range(3),range(1,3),range(1,3))):
                    span.append(r)
            assert len(span)==3
            fibers.add(tuple(span))
        assert len(fibers)==9
        completed={tuple(sorted((q,r))) for q,r in itertools.combinations(opp,2) if A[q,r]}
        completed.update(e for f in fibers for e in itertools.combinations(f,2))
        B=np.array([[int(tuple(sorted((q,r))) in completed) if q!=r else 0 for r in opp] for q in opp],dtype=np.int64)
        assert set(B.sum(axis=1))=={10}
        assert np.array_equal(B@B,5*np.eye(27,dtype=int)-4*B+5*np.ones((27,27),dtype=int))
        Q=3*np.eye(27,dtype=int)-3*B+np.ones((27,27),dtype=int)
        assert np.array_equal(Q@Q,18*Q)
        assembled[np.ix_(opp,opp)]+=Q
        embedded[p]=np.zeros((40,40),dtype=np.int64);embedded[p][np.ix_(opp,opp)]=Q
        graph_sum[np.ix_(opp,opp)]+=B
        chart[p]=(opp,completed)
    overlaps=Counter();transports=Counter()
    for p,r in itertools.combinations(range(40),2):
        overlap=set(chart[p][0])&set(chart[r][0])
        assert len(overlap)==18
        ep={e for e in chart[p][1] if set(e)<=overlap}
        er={e for e in chart[r][1] if set(e)<=overlap}
        mismatch=len(ep^er)
        overlaps[(int(A[p,r]),mismatch)]+=1
        product=embedded[r]@embedded[p]
        rank=field_basis(product,101).shape[1]
        assert rank==field_basis(product,103).shape[1]
        trace=int(np.trace(product))
        transports[(int(A[p,r]),rank,trace)]+=1
    J=np.ones((40,40),dtype=int);I=np.eye(40,dtype=int)
    assert np.array_equal(graph_sum,16*A+2*(J-I))
    # P15=(8I-4A+J)/24 is the native -4 adjacency sector.
    Q15=8*I-4*A+J
    assert np.array_equal(Q15@Q15,24*Q15)
    assert np.array_equal(assembled,12*Q15)
    assert all(np.array_equal(Q15@q,24*q) for q in embedded.values())
    incidence=np.array([[int(v in line) for line in lines] for v in range(40)],dtype=np.int64)
    assert not (assembled@incidence).any()
    # Squared principal cosines:1,1/3,1/3,1/3,1/3,1/9.
    # Exact polar transport lies in Q(sqrt3), not in Q.
    denominator=8*324**3;transport={}
    for p,r in itertools.combinations(range(40),2):
        qp,qr=embedded[p],embedded[r];T=qp@qr@qp
        if A[p,r]:
            assert np.array_equal(T@T,5832*T)
            continue
        assert not (T@(T-5832*np.eye(40,dtype=int))@(T-1944*np.eye(40,dtype=int))@(T-648*np.eye(40,dtype=int))).any()
        product=qr@qp;product2=product@product;product3=product2@product
        rational=41*324**2*product-168*324*product2+135*product3
        irrational=-6*324**2*product+60*324*product2-54*product3
        # Prevent a machine-integer wrap from masquerading as an exact identity.
        norm0=max(sum(int(x)**2 for x in row) for row in rational.T)
        norm1=max(sum(int(x)**2 for x in row) for row in irrational.T)
        assert norm0+3*norm1<2**63 and 2*(norm0+norm1)<2**63
        assert np.array_equal(rational.T@rational+3*irrational.T@irrational,(denominator**2//18)*qp)
        assert not (rational.T@irrational+irrational.T@rational).any()
        transport[r,p]=(rational,irrational);transport[p,r]=(rational.T,irrational.T)
    triple=next((p,r,s) for p,r,s in itertools.combinations(range(40),3) if not A[p,r] and not A[r,s] and not A[s,p])
    p,r,s=triple
    def quadratic_product(x,y):
        a,b=(v.astype(object) for v in x);c,d=(v.astype(object) for v in y)
        return a@c+3*b@d,a@d+b@c
    loop=quadratic_product(quadratic_product(transport[p,s],transport[s,r]),transport[r,p])
    trace=[Fraction(int(np.trace(v)),denominator**3) for v in loop]
    curvature=(loop[0]-(denominator**3//18)*embedded[p].astype(object),loop[1])
    basis=np.linalg.eigh(embedded[p].astype(float))[1][:,-6:]
    small=basis.T@((np.array(loop[0],float)+np.sqrt(3)*np.array(loop[1],float))/denominator**3)@basis
    assert np.max(abs(small.T@small-np.eye(6)))<1e-10
    return dict(status='PASS',charts=40,wedges_per_point=6,
        chart_size=27,chart_rank=6,overlap_size=18,
        overlap_mismatch_histogram={f'centers_collinear={a},changed_edges={b}':n for (a,b),n in sorted(overlaps.items())},
        canonical_projection_transport_histogram={f'centers_collinear={a},rank={r},Tr_Qp_Qr={t}':n for (a,r,t),n in sorted(transports.items())},
        polar_transport=dict(domain='noncollinear-center edges only; collinear-center projection maps have rank2, so do not define invertible6D transport',
            exact_formula='With V=QrQp,D=8*324^3: U=(41*324^2 V-168*324 V^2+135V^3 +sqrt3[-6*324^2 V+60*324 V^2-54V^3])/D.',
            exact_isometry_identity='U_rp^T U_rp=Pp, U_rp U_rp^T=Pr',
            triangle=list(triple),exact_triangle_trace_Q_sqrt3=[str(v) for v in trace],triangle_curvature_nonzero=any(v.any() for v in curvature),
            infinite_order_proved_by_nonintegral_trace=any(v.denominator!=1 for v in trace),
            triangle_transport_eigenvalues=[[float(z.real),float(z.imag)] for z in np.linalg.eigvals(small)],
            boundary='This polar connection is a declared canonical construction on subspaces, not the original point-label identity, a spacetime spin connection, Einstein dynamics or a predictedphysicalgaugecoupling.'),
        compact_holonomy_closure=holonomy_closure(embedded,transport,denominator,A),
        exact_projector_sum='sum_p R_p^T P6(p) R_p = 16 P15(W33); P15=(8I-4A+J)/24',
        exact_integer_witness=assembled.tolist(),
        assembled_rank=15,assembled_nonzero_eigenvalue=16,
        assembled_target='kernel of the actual40x40 W33 point-line incidence transpose',
        assembled_graph='sum_p R_p^T A_E6(p) R_p=16 A_W33+2(J-I)',
        assembled_graph_spectrum={'270':1,'30':24,'-66':15},
        gluing_boundary='At one center the six wedge charts share the same completed shell. Across centers the partial identity on the18shared point labels changes36 or16 adjacency entries, so it cannot be an isometry of the local minuscule Gram. The scalar restriction maps glue, while the E6 relations need additional transport data.',
        prior=['TOE79 canonical opposite-shell-plus-center cubic completion','TOE80 local rank6 projector','native15D incidence kernel is prior; the specific40-chart frame assembly is tested here'],
        scope='Exact finite atlas/frame identity, not globally glued E6 gauge fields, physical matter families, a manifold or gravity.')


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11983_atlas_projector_descent.json').write_text(json.dumps(d,indent=2)+'\n')
    print(d['status'],d['overlap_mismatch_histogram'],d['exact_projector_sum'])
