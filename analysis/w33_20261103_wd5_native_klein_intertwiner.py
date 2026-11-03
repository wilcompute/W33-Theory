"""Actual native spinor stabilizer -> q5 frame hyperoval -> Clebsch actions.

Pass12525/12527 own the q5 frame identification; BT3418-3429 own the
Clebsch/W(D5) network. This supplies the intervening maps and native words.
"""
import itertools
import json
import pathlib
import sys

import numpy as np
import sympy as s

ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_spin6_rotation_group_audit import multiply
from w33_20261102_conditional_symplectic_vacuum import parity
from w33_20261102_toroidal_knight_clifford_bridge import matrices


def norm(v):
    v=tuple(int(x)%5 for x in v);a=next(x for x in v if x)
    return tuple(x*pow(a,-1,5)%5 for x in v)


def geometry():
    points=sorted({norm(v) for v in itertools.product(range(5),repeat=4) if any(v)})
    idx={p:i for i,p in enumerate(points)};lines=set()
    for i,a in enumerate(points):
        for b in points[i+1:]:
            if (a[0]*b[2]-a[2]*b[0]+a[1]*b[3]-a[3]*b[1])%5:continue
            lines.add(tuple(sorted({idx[b]}|{idx[norm(tuple(a[j]+t*b[j] for j in range(4)))] for t in range(5)})))
    lines=sorted(lines);quad=[]
    for line in lines:
        a,b=(points[i] for i in line[:2])
        def p(i,j):return (a[i]*b[j]-a[j]*b[i])%5
        assert (p(0,2)+p(1,3))%5==0
        quad.append(norm((3*(p(0,1)+p(2,3)),4*(p(0,1)-p(2,3)),3*(p(0,3)+p(1,2)),4*(p(0,3)-p(1,2)),p(0,2))))
    assert len(points)==len(lines)==len(set(quad))==156
    assert all(sum(x*x for x in v)%5==0 for v in quad)
    return points,lines,quad


def signed_action(element,v):
    p,b=element;out=[0]*len(p)
    for j,k in enumerate(p):out[k]=(-1)**((b>>j)&1)*v[j]
    return out


def build():
    d=json.loads((ROOT/'data/w33_20261102_spin6_rotation_group_audit.json').read_text());gens=[]
    for A in d['generator_orthogonal_matrices']:
        p=[];bits=0
        for j in range(6):
            i=next(i for i in range(6) if A[i][j]);p.append(i);bits|=int(A[i][j]<0)<<j
        gens.append((tuple(p),bits))
    identity=(tuple(range(6)),0);words={identity:[]};queue=[identity]
    for a in queue:
        for j,g in enumerate(gens):
            b=multiply(g,a)
            if b not in words:words[b]=words[a]+[j];queue.append(b)
    old={identity};todo=[identity]
    for a in todo:
        for g in gens[:6]:
            b=multiply(g,a)
            if b not in old:old.add(b);todo.append(b)
    stabilizer={a for a in words if a[0][0]==0 and not a[1]&1}
    assert len(stabilizer)==1920 and len(old)==960
    extra=min(stabilizer-old);chosen=gens[:6]+[extra]
    generated={identity};todo=[identity]
    for a in todo:
        for g in chosen:
            b=multiply(g,a)
            if b not in generated:generated.add(b);todo.append(b)
    assert generated==stabilizer
    print('WD5_GROUPS',len(stabilizer),'extra_word',words[extra],flush=True)
    _,blades,unitary,omega=matrices();allunit=unitary+[(s.eye(4)+s.I*blades[15])/s.sqrt(2)]
    U=s.eye(4)
    for j in words[extra]:U=(allunit[j]*U).applyfunc(s.expand)
    U=s.simplify(U);assert s.simplify(U*omega*U.T)==omega
    print('WD5_EXACT_SPINOR_WORD_CHECKED',flush=True)
    points,lines,quad=geometry();qindex={q:i for i,q in enumerate(quad)}
    selected=[i for i,q in enumerate(quad) if sum(x!=0 for x in q)==2]
    assert len(selected)==20
    print('WD5_KLEIN_GEOMETRY',len(points),len(selected),flush=True)
    coverage=[sum(i in line for line in [lines[j] for j in selected]) for i in range(156)]
    assert set(coverage)=={0,2}
    bits16=[x for x in range(32) if x.bit_count()%2==0];bidx={x:i for i,x in enumerate(bits16)}
    def reduced(a):return tuple(k-1 for k in a[0][1:]),a[1]>>1
    def line_permutation(a):
        g=reduced(a);return [qindex[norm(signed_action(g,q))] for q in quad]
    def clebsch_permutation(a):
        p,b=reduced(a);b^=31 if parity(p) else 0
        assert b.bit_count()%2==0
        return [bidx[sum((((x>>j)&1)^((b>>j)&1))<<p[j] for j in range(5))] for x in bits16]
    linegens=[line_permutation(a) for a in chosen];pointgens=[];clebschgens=[]
    pencils=[{j for j,line in enumerate(lines) if i in line} for i in range(156)]
    line_sets=[set(line) for line in lines]
    for a,permutation in zip(chosen,linegens):
        assert {permutation[j] for j in selected}==set(selected)
        pointmap=[]
        for pencil in pencils:
            common=set.intersection(*(line_sets[permutation[j]] for j in pencil));assert len(common)==1
            pointmap.append(common.pop())
        assert sorted(pointmap)==list(range(156))
        assert all({pointmap[i] for i in line}==line_sets[permutation[j]] for j,line in enumerate(lines))
        pointgens.append(pointmap);p=clebsch_permutation(a);clebschgens.append(p)
        assert all(((bits16[i]^bits16[j]).bit_count()==4)==((bits16[p[i]]^bits16[p[j]]).bit_count()==4) for i,j in itertools.combinations(range(16),2))
    hyperoval_actions={tuple(p[j] for j in selected) for a in stabilizer for p in [line_permutation(a)]}
    clebsch_actions={tuple(clebsch_permutation(a)) for a in stabilizer}
    assert len(hyperoval_actions)==len(clebsch_actions)==1920
    return dict(status='PASS_NATIVE_WD5_Q5_KLEIN_CLEBSCH_INTERTWINER',
        extra_native_spinor_word=words[extra],extra_native_spinor_matrix=[[str(x) for x in row] for row in U.tolist()],
        native_six_form_generators=[d['generator_orthogonal_matrices'][i] for i in range(6)],
        selected_generator_signed_six_states=[[list(p),b] for p,b in chosen],
        q5_points=points,q5_isotropic_lines=lines,line_to_quadric_coordinate=quad,selected_hyperoval_lines=selected,
        q5_line_generator_permutations=linegens,q5_point_generator_permutations=pointgens,
        Clebsch_even_weight_vertices=bits16,Clebsch_generator_permutations=clebschgens,
        faithful_hyperoval_action_order=1920,faithful_Clebsch_action_order=1920,spinor_stabilizer_order=3840,
        hyperoval_point_coverage={'0':coverage.count(0),'2':coverage.count(2)},
        map='Restrict the actual six-form action to the five coordinates perpendicular to iOmega, reduce its integral signed matrix modulo5, normalize projectively, then invert the explicit Klein bijection. For Clebsch, convert rotational signed R to even-sign Q=(-1)^parity(permutation)*R and act affinely on even five-bit weights.',
        ownership='Pass12525/12527 own the minimal q5 frame and W(D5). BT3418-3429 own Clebsch/half-spin/network identifications. This gives actual native spinor words and commuting actions connecting those models.',
        boundary='Explicit map to the frame realization of the q5 minimal hyperoval, with ambient156-point/line incidence checked. It is not a characteristic-changing physical process or an independently proved global minimal-hyperoval classification.')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261103_wd5_native_klein_intertwiner.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],d['extra_native_spinor_word'],d['hyperoval_point_coverage'],flush=True)
