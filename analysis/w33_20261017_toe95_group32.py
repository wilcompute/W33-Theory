"""TOE95 G32 numerical unitary closure with exact short cyclotomic braid.

Five order-three four-mode Witting transvection lifts yield 25920
projective ray permutations. Check every Cayley edge against its stored
U(4) lift and classify the scalar holonomies in mu_6. An exact
Q(zeta12) braid establishes a nontrivial mu_3 scalar, supplementing
TOE94's exact -I4 commutator. The 155520 full-order statement remains
numerical unless every matrix enumeration is made exact.
"""
from __future__ import annotations
import json
from collections import Counter,deque
from pathlib import Path
import numpy as np
import sympy as S
from analysis.w33_20261015_toe93_central_extension import V
from analysis.w33_20261015_toe91_symplectic_phase_audit import transvection
from analysis.w33_20261015_toe91_symplectic_unitary_lift import lift
from analysis.w33_20261015_toe92_full_symplectic_4mode import comp
from analysis.w33_20261015_toe94_exact_central import recognized,matzero

ROOT=Path(__file__).resolve().parents[1]

def generators():
    perms=[tuple(transvection(v)) for v in V]
    unitaries=[]
    for p in perms:
        u,err,s=lift(p)
        u=u*np.exp(-1j*np.angle(s)/3)
        assert np.max(abs(u@u@u-np.eye(4)))<1e-9
        unitaries.append(u)
    return perms,unitaries

def exact_braid(unitaries):
    matrices=[S.Matrix(4,4,lambda i,j:
                recognized(u[i,j].real)+S.I*recognized(u[i,j].imag))
              for u in unitaries]
    assert all(matzero(u.conjugate().T*u-S.eye(4)) for u in matrices)
    def word(seq):
        m=S.eye(4)
        for i in seq:m=(matrices[i]*m).applyfunc(S.expand)
        return m
    omega=(-1+S.I*S.sqrt(3))/2
    x=word((4,1,4));y=word((1,4,1))
    assert matzero(x-omega*y)
    dets=[S.expand(S.det(u)) for u in matrices]
    assert all(S.simplify(d-omega**2)==0 for d in dets[:4])
    assert S.expand(dets[4]-1)==0
    return {'identity':'U4 U1 U4 = omega U1 U4 U1',
            'omega':'(-1+i sqrt(3))/2','verified_field':'Q(sqrt(3),i)',
            'exact_generator_determinants':['omega^2']*4+['1'],
            'all_five_order_three':True}

def certificate():
    perms,unit=generators()
    braid=exact_braid(unit)
    identity=tuple(range(40))
    nodes={identity:0}
    allp=[identity];allu=[np.eye(4,dtype=complex)]
    queue=deque([0])
    scalar_hist=Counter();max_residual=0.
    while queue:
        i=queue.popleft();p=allp[i];u=allu[i]
        for j,g in enumerate(perms):
            q=comp(g,p);product=unit[j]@u
            if q not in nodes:
                nodes[q]=len(allp)
                allp.append(q);allu.append(product)
                queue.append(nodes[q])
            else:
                target=allu[nodes[q]]
                alpha=np.trace(target.conj().T@product)/4
                residual=float(np.max(abs(product-alpha*target)))
                max_residual=max(max_residual,residual)
                k=int(np.rint(np.angle(alpha)/(np.pi/3)))%6
                phase=np.exp(1j*np.pi*k/3)
                assert abs(alpha-phase)<1e-8,(alpha,k)
                scalar_hist[k]+=1
        assert len(nodes)<=25920
    assert len(nodes)==25920
    assert max_residual<1e-9
    assert set(scalar_hist)==set(range(6))
    assert sum(scalar_hist.values())==5*25920-(25920-1)
    assert scalar_hist=={0:46642,1:10292,2:12743,3:10920,4:12250,5:10834},scalar_hist
    return {
       'projective_group_size':len(nodes),
       'number_of_projective_Cayley_edges_tested':5*len(nodes),
       'scalar_kernel_candidates_numerically_observed':6,
       'scalar_mu6_powers_histogram':{str(k):int(v) for k,v in sorted(scalar_hist.items())},
       'numerical_full_unitary_group_order_if_mu6_is_exact_kernel':len(nodes)*6,
       'max_projective_unitary_closure_error':round(max_residual,12),
       'exact_cyclotomic_braid':braid,
       'exact_order_two_scalar_relation':'TOE94 U_A U_B U_A^-1 U_B^-1 = -I4',
       'literature_crosscheck':'Shephard-Todd G32 is a 4D complex reflection group of order 155520; its derived subgroup has order 51840 and is Sp(4,3). See MathOverflow question 360582 / Shephard Todd (1954).',
       'scope':'The six-scalar kernel enumeration is numerical; exact braid and TOE94 -I relation prove mu3 and mu2 elements, but a full exact group presentation/upper bound on the scalar kernel has not been proved here.'
    }
if __name__=='__main__':
    z=certificate()
    print('TOE95 G32',z['projective_group_size'],
          z['numerical_full_unitary_group_order_if_mu6_is_exact_kernel'])
    (ROOT/'data/w33_20261017_toe95_group32.json').write_text(json.dumps(z,sort_keys=True,indent=2)+'\n')
