"""Exact qubit/qutrit selector on the repo's E8-derived real Albert algebra.

Prior objects: Pass10950 and Pass11569. Group theorem: Baez--Schwahn
arXiv:2606.15235. Supplied selector, not a vacuum or a chiral SM spectrum.
"""
import json
import sys
import time
from collections import Counter
from itertools import combinations, product
from math import gcd, lcm
from pathlib import Path
import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass10950_clock_albert_lorentz_spinor as P
from toe_20261116_E6_full_cubic_SM_stabilizer import hypercharge_integer_weights


def independent(matrices):
    rows = [m.reshape(-1).tolist() for m in matrices]
    _, piv = P.dm(rows).transpose().rref()
    return [matrices[i] for i in piv]


def nullcomb(basis, rows):
    coeff = P.nullspace(rows)
    out = []
    for c in coeff:
        scale = lcm(*[t.denominator for t in c])
        v = [int(t*scale) for t in c]
        common = gcd(*v)
        out.append(sum((a//common)*m for a,m in zip(v,basis)))
    return out


def commutator_center(basis):
    blocks = []
    for a in basis:
        blocks.append(np.stack([(a@b-b@a).reshape(-1) for b in basis],axis=1))
    rows = np.concatenate(blocks).tolist()
    return nullcomb(basis,rows)


def run():
    J = P.build_clock_albert()
    n = J['n']
    den = lcm(*[x.denominator for x in J['prod'].flat])
    Pi = np.array([[[int(x*den) for x in row] for row in plane]
                   for plane in J['prod']],dtype=np.int64)
    L = np.stack([Pi[i].T for i in range(n)])
    frame = [J['idx'][g] for g in J['G']]
    eye = np.eye(n,dtype=np.int64)
    unit = sum(eye[:,i] for i in frame)
    c = frame[0]
    # Seek a closed H3(C) with the existing frame and two pair_re/pair_im
    # Peirce lines. No perturbation or floating tolerance is used.
    pairs = [(i,i+1) for i,x in enumerate(J['labels']) if x[0]=='pair_re']
    candidates = []
    for a,b in combinations(pairs,2):
        selected = set(frame+list(a)+list(b))
        while True:
            more = set(selected)
            for i in selected:
                for j in selected:
                    more.update(int(k) for k in np.flatnonzero(Pi[i,j]))
            if more == selected or len(more)>9:
                selected = more; break
            selected = more
        if len(selected)==9:
            candidates.append(sorted(selected))
    assert candidates
    B = candidates[0]
    outside = [i for i in range(n) if i not in B]
    assert not Pi[np.ix_(B,B,outside)].any()
    assert all(np.array_equal(L[i]@unit,den*eye[:,i]) for i in range(n))
    eig = [tuple(int(2*L[j][i,i]//den) for j in frame) for i in range(n)]
    assert all(not (L[j]-np.diag(np.diag(L[j]))).any() for j in frame)
    dims = [sum(i in B and eig[i][a]==eig[i][b]==1 for i in range(n))
            for a,b in combinations(range(3),2)]
    assert dims == [2,2,2]
    X = [i for i in B if L[c][i,i]==0]
    assert len(X)==4 and not Pi[np.ix_(X,X,[i for i in range(n) if i not in X])].any()
    comms = [L[i]@L[j]-L[j]@L[i] for i,j in combinations(range(n),2)]
    deriv = independent(comms)
    assert len(deriv)==52
    def preserve(subspace):
        out = [i for i in range(n) if i not in subspace]
        return [[int(d[i,j]) for d in deriv] for i in out for j in subspace]
    B_rows = preserve(B)
    c_rows = [[int(d[i,c]) for d in deriv] for i in range(n)]
    stabilizer_B = nullcomb(deriv,B_rows)
    stabilizer_c = nullcomb(deriv,c_rows)
    SM = nullcomb(deriv,B_rows+c_rows)
    SM_X = nullcomb(deriv,B_rows+preserve(X))
    assert [len(stabilizer_B),len(stabilizer_c),len(SM),len(SM_X)]==[16,36,12,12]
    color = nullcomb(SM,[[int(d[i,j]) for d in SM] for i in range(n) for j in B])
    assert len(color)==8
    derived = independent([a@b-b@a for a,b in combinations(SM,2)])
    center = commutator_center(SM)
    assert len(derived)==11 and len(center)==1 and not commutator_center(color)
    Z = s.Matrix(center[0])
    x = s.Symbol('x')
    fact = s.factor_list(Z.charpoly(x).as_expr())[1]
    quad = sorted([(s.Poly(f,x).all_coeffs()[-1],mult) for f,mult in fact
                   if s.degree(f,x)==2])
    assert len(quad)==3 and [v[1] for v in quad]==[6,3,2],quad
    scale2 = quad[0][0]
    assert [v[0]/scale2 for v in quad]==[1,4,9]
    scale = s.sqrt(scale2)
    assert scale.is_Rational
    Q = Z/scale
    # Spectral projectors of -Q^2, with weights0,1,4,9.
    H = -Q*Q
    projectors = {}
    for q2 in [0,1,4,9]:
        proj = s.eye(n)
        for r2 in [0,1,4,9]:
            if r2 != q2:
                proj = proj*(H-r2*s.eye(n))/(q2-r2)
        projectors[q2] = proj
    E0,E1,E4,E9 = [projectors[k] for k in [0,1,4,9]]
    assert E0+E9 == s.diag(*[int(i in B) for i in range(n)])
    peirce = s.eye(n)-8*s.Matrix(L[c])/den+8*(s.Matrix(L[c])/den)**2
    # +1 on Peirce0 and1, -1 on Peirce1/2.
    T2 = E0-E1+E4-E9
    assert T2==peirce and T2**2==s.eye(n)
    T3 = E0+E9-(E1+E4)/2+s.sqrt(3)*(Q*E1-Q*E4/2)/2
    assert (T3**3-s.eye(n)).applyfunc(s.simplify)==s.zeros(n)
    assert (T3*T2-T2*T3).applyfunc(s.simplify)==s.zeros(n)
    # Adjoint action on the full executable F4, in an independent basis.
    flat = s.Matrix.hstack(*[s.Matrix(d.reshape(-1).tolist()) for d in deriv])
    _, pivotrows = P.dm([d.reshape(-1).tolist() for d in deriv]).rref()
    minor = flat[list(pivotrows),:]
    images = s.Matrix.hstack(*[s.Matrix(list(Z*s.Matrix(d)-s.Matrix(d)*Z))
                             for d in deriv])
    adj = minor.inv()*images[list(pivotrows),:]/scale
    assert flat*adj==images/scale
    adjfact = s.factor_list(adj.charpoly(x).as_expr())[1]
    expected = x**12*(x*x+1)**6*(x*x+4)**9*(x*x+9)**2*(x*x+16)**3
    assert s.expand(adj.charpoly(x).as_expr()-expected)==0
    centralizers = {k:12+sum(2*m for q,m in [(1,6),(2,9),(3,2),(4,3)] if q%k==0)
                   for k in range(1,7)}
    assert [centralizers[k] for k in range(1,7)]==[52,36,16,18,12,12]
    standard = Counter(-q for q in hypercharge_integer_weights())
    folded = Counter({0:5,1:6,-1:6,2:3,-2:3,3:2,-3:2})
    assert sum(standard.values())==27
    assert standard!=Counter({-q:m for q,m in standard.items()})
    assert max(map(abs,standard))==6 and max(map(abs,folded))==3
    assert standard!=folded and standard!=Counter({-q:m for q,m in folded.items()})
    # Independent F4 root realization: the short24-cell and long D4 roots.
    roots = []
    for i in range(4):
        for sign in [-1,1]:
            r=s.zeros(4,1); r[i]=sign; roots.append(r)
    roots += [s.Matrix(v)/2 for v in product([-1,1],repeat=4)]
    for i,j in combinations(range(4),2):
        for a,b in product([-1,1],repeat=2):
            r=s.zeros(4,1); r[i]=a; r[j]=b; roots.append(r)
    direction=s.Matrix([1,1,1,3])
    root_counts=Counter([int(r.dot(direction)) for r in roots]+[0]*4)
    assert root_counts==Counter({0:12,1:6,-1:6,2:9,-2:9,3:2,-3:2,4:3,-4:3})
    color_root=s.Matrix([1,-1,0,0])
    weak_root=s.Matrix([1,1,1,-1])/2
    assert color_root.dot(direction)==weak_root.dot(direction)==0
    Tcolor=color_root/color_root.dot(color_root)
    Tweak=weak_root/weak_root.dot(weak_root)
    Y=direction/6
    assert Tweak.dot(Tweak)/Tcolor.dot(Tcolor)==2
    assert Tweak.dot(Tweak)/Y.dot(Y)==3
    # Verify the kinetic ratios on the actual27 matrices as well.
    weak = nullcomb(SM,[[int(np.trace(a@d)) for d in SM] for a in color+center])
    assert len(weak)==3
    wf = s.factor_list(s.Matrix(weak[0]).charpoly(x).as_expr())[1]
    wquad=sorted([(s.Poly(f,x).all_coeffs()[-1],m) for f,m in wf if s.degree(f,x)==2])
    assert len(wquad)==2 and wquad[1][0]==4*wquad[0][0]
    assert [m for _,m in wquad]==[8,1]
    weak_trace=-s.trace(s.Matrix(weak[0])**2)/(4*wquad[0][0])
    color_trace=None
    for d in color:
        cf=s.factor_list(s.Matrix(d).charpoly(x).as_expr())[1]
        cq=[(s.Poly(f,x).all_coeffs()[-1],m) for f,m in cf if s.degree(f,x)==2]
        if len(cq)==1 and cq[0][1]==6:
            color_trace=-s.trace(s.Matrix(d)**2)/(4*cq[0][0]);break
    assert color_trace==3 and weak_trace==6
    Y_trace=-s.trace(Q**2)/36
    assert Y_trace==2 and weak_trace/color_trace==2 and weak_trace/Y_trace==3
    # The repo's real str0(A) is E6(-26). Its compact continuation is
    # Der(A) + i L_(trace zero), not the same real matrix algebra.
    traceless = [eye[:,i] for i in range(n) if i not in frame]
    traceless += [eye[:,i]-eye[:,frame[-1]] for i in frame[:-1]]
    Ltl = [np.tensordot(v,L,axes=1) for v in traceless]
    assert len(Ltl)==26
    assert all(np.trace(d@a)==0 for d in deriv for a in Ltl)
    gramD = np.array([[np.trace(a@b) for b in deriv] for a in deriv])
    gramL = np.array([[np.trace(a@b) for b in Ltl] for a in Ltl])
    assert P.inertia_int(gramD)==(0,52,0) and P.inertia_int(gramL)==(26,0,0)
    return dict(status='PASS', parents=['Pass10950','Pass11569','arXiv:2606.15235'],
        basis_labels=J['labels'], frame_indices=frame, B_indices=B,X_indices=X,
        successful_seed_pairs=len(candidates),
        distinct_coordinate_H3C_candidates=len({tuple(v) for v in candidates}),
        B_Peirce_pair_dimensions=dims,
        exact_stabilizer_dimensions=dict(F4=52,B=16,c=36,B_and_c=12,B_and_X=12),
        color_ideal_dimension=8,color_ideal_center_dimension=0,
        SM_derived_dimension=11,SM_center_dimension=1,
        SM_algebra='compact su3 + su2 + u1',
        normalized_real_hypercharge_generator_Q=Q.tolist(),
        Q_normalization='Q=6Y as a real skew generator; eigenvalues i times integer charges',
        Albert27_charge_multiplicities={'0':5,'+/-1':6,'+/-2':3,'+/-3':2},
        traceless26_charge_multiplicities={'0':4,'+/-1':6,'+/-2':3,'+/-3':2},
        F4_adjoint_charge_multiplicities={'0':12,'+/-1':6,'+/-2':9,'+/-3':2,'+/-4':3},
        circle_finite_order_centralizer_dimensions=centralizers,
        order2_selector='T2=Peirce symmetry at c; fixed real Albert dimension11',
        order3_selector='T3=exp(2pi Q/3); fixed subspace equals B, dimension9',
        order6_selector='T2*T3, commuting exact orders2 and3; centralizer SM',
        order5_control='exp(2pi Q/5) has same SM Lie centralizer',
        compact_E6_control='Der(A)+i L_tracezero has trace-form inertia(0,78,0); '
            'complex conjugation fixes Der(A)=F4 and negates i L_tracezero. '
            'The real str0(A)=E6(-26) in Pass10950 is different.',
        parallel_E6_standard_27_Q6Y_census=dict(sorted(standard.items())),
        hypercharge_embedding_comparison='The standard E6 SM embedding has '
            'different 27 charge spectrum, with |6Y| up to6, versus3 for this F4 '
            'embedding. They are not conjugate inside E6, even allowing Y sign. '
            'A full F4 outer projection cannot preserve that standard hypercharge.',
        independent_root_control='Short24-cell plus longD4 roots with Q-direction '
            '(1,1,1,3) reproduces the complete executable adjoint charge census',
        direct_Albert27_kinetic_norms=dict(color_T3=str(color_trace),
            weak_T3=str(weak_trace),Y=str(Y_trace)),
        tree_coupling_control='With one F4 gauge kinetic form: g3^2=2*g2^2, '
            'gY^2=3*g2^2, sin^2(thetaW)=3/4 in the chosen quark-charge normalization. '
            'A conditional tree boundary relation, not matched observed couplings.',
        global_group_input='Baez-Schwahn stabilizer theorem identifies S(U2 x U3); '
            'matrix Lie calculation alone does not determine every disconnected extension',
        matter_limit='The real26 has conjugate-paired charge weights and |Y|<=1/2. '
            'It cannot itself be one chiral SM family, which also needs |Y|=2/3 and1. '
            'No fermion zero-mode or chiral index is computed.',
        scope='A supplied exact Jordan subalgebra selector on the existing E8-derived '
            'Albert algebra. No vacuum selection, E6 outer gauge bundle, localized '
            'chiral matter, physical couplings or full TOE is established.')


if __name__=='__main__':
    start=time.time()
    result=run()
    path=ROOT/'data/toe_20261118_Albert_qubit_qutrit_SM_selector.json'
    path.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],stabilizers=result['exact_stabilizer_dimensions'],
                         finite_orders=result['circle_finite_order_centralizer_dimensions'],
                         seconds=time.time()-start)))
