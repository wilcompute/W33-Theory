"""Exact nongauge finite-momentum zero of the supplied three-mixed curl.

Continuation of parallel commit9baf04f: its generic rank and leading cone
remain correct. At z=(omega,omega,1,1), omega^2+omega+1=0, one extra
magnetic zero survives. Arithmetic uses the faithful rational 2x2
representation of Q(omega), never numerical rank tolerances.
"""
from pathlib import Path
from functools import lru_cache
import hashlib
import json
from math import gcd, lcm
from functools import reduce
import sys

import numpy as np
import sympy as s
from sympy.polys.matrices import DomainMatrix

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'analysis'))
from w33_20261028_three_mixed_loop_minimal_maxwell import geometry

R = np.array([[1,0,5,-5,1,0],[0,1,-1,0,1,0],[0,0,5,-5,0,1]],dtype=object)
POWER = ((1,0),(0,1),(-1,-1))


def cyclotomic_row(face, voltages):
    a = np.zeros(135,dtype=object)
    b = a.copy()
    position = np.zeros(4,dtype=int)
    for edge, sign in face:
        edge, sign = int(edge),int(sign)
        if sign < 0:
            position -= voltages[edge]
        u,v = POWER[int(position[0]+position[1])%3]
        a[edge] += sign*u
        b[edge] += sign*v
        if sign > 0:
            position += voltages[edge]
    assert not position.any()
    return a,b


def rational_lift(a,b):
    """Multiplication by a+b*omega acts on coefficient pairs by this block."""
    return np.block([[a,-b],[b,a-b]])


def exact_rank(a,b):
    rank = DomainMatrix.from_Matrix(s.Matrix(rational_lift(a,b))).to_field().rank()
    assert rank%2 == 0
    return rank//2


@lru_cache(None)
def operators():
    _,V,edges,*_ = geometry()
    previous = json.loads((ROOT/'data/w33_20261027_native_bloch_face_module.json').read_text())
    faces = json.loads((ROOT/'data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json').read_text())
    short = [cyclotomic_row(f['boundary'],V) for f in faces['independent_face_basis']]
    loops = [cyclotomic_row(f,V) for f in previous['commutator_boundaries']]
    for loop in previous['commutator_boundaries']:
        identity_row = np.zeros(135,dtype=object)
        for edge,sign in loop:
            identity_row[edge] += sign
        assert not np.any(identity_row)
    s0,s1 = (np.array([x[j] for x in short],dtype=object) for j in (0,1))
    l0,l1 = (np.array([x[j] for x in loops],dtype=object) for j in (0,1))
    m0,m1 = np.vstack([s0,R@l0]),np.vstack([s1,R@l1])
    f0,f1 = np.vstack([s0,l0]),np.vstack([s1,l1])
    d0,d1 = np.zeros((135,27),dtype=object),np.zeros((135,27),dtype=object)
    for e,(u,v) in enumerate(edges):
        a,b = POWER[int(V[e,0]+V[e,1])%3]
        d0[e,u] = -1
        d0[e,v] = a
        d1[e,v] = b
    # omega conjugates to -1-omega.
    dagger0,dagger1 = (d0-d1).T,-d1.T
    return s0,s1,m0,m1,f0,f1,d0,d1,dagger0,dagger1


def apply_pair(a,b,x,y):
    return a@x-b@y, b@x+(a-b)@y


def witness():
    s0,s1,m0,m1,f0,f1,d0,d1,g0,g1 = operators()
    a,b = np.vstack([m0,g0]),np.vstack([m1,g1])
    dm = DomainMatrix.from_Matrix(s.Matrix(rational_lift(a,b))).to_field()
    basis = dm.nullspace().to_Matrix()
    assert basis.rows == 2
    vector = list(basis.row(0))
    denominator = lcm(*(int(x.q) for x in vector))
    values = [int(x*denominator) for x in vector]
    divisor = reduce(gcd,values)
    values = [x//divisor for x in values]
    x,y = np.array(values[:135],dtype=object),np.array(values[135:],dtype=object)
    assert all(z == 0 for z in sum((list(t) for t in apply_pair(m0,m1,x,y)),[]))
    assert all(z == 0 for z in sum((list(t) for t in apply_pair(g0,g1,x,y)),[]))
    norm = sum(a*a-a*b+b*b for a,b in zip(x,y))
    assert norm > 0
    six = apply_pair(f0,f1,x,y)
    assert any(v != 0 for t in six for v in t)
    return dict(a=list(map(int,x)),b=list(map(int,y)),norm_squared=int(norm),
                convention='edge amplitude a_e+b_e*omega, omega^2+omega+1=0',
                curl_zero=True,gradient_adjoint_zero=True,six_loop_curl_nonzero=True)


def certificate():
    s0,s1,m0,m1,f0,f1,d0,d1,g0,g1 = operators()
    ranks = dict(short=exact_rank(s0,s1),mixed=exact_rank(m0,m1),six=exact_rank(f0,f1),gradient=exact_rank(d0,d1))
    assert ranks == dict(short=105,mixed=107,six=108,gradient=27)
    assert not np.any(rational_lift(m0,m1)@rational_lift(d0,d1))
    w = witness()
    x,y = np.array(w['a'],dtype=object),np.array(w['b'],dtype=object)
    u,v = apply_pair(f0,f1,x,y)
    curl_norm = sum(a*a-a*b+b*b for a,b in zip(u,v))
    repair_cost = s.Rational(6,1000)*curl_norm/w['norm_squared']
    assert repair_cost > 0
    return dict(schema='w33.pass12340.mixed_loop_exception.v1',
                parallel_owner_commit='9baf04f1752fec07d95f6d6fa0dedf44a116f9e5',
                character=['omega','omega','1','1'],minimal_polynomial='omega^2+omega+1',
                exact_ranks=ranks, physical_magnetic_kernel_dimension=135-107-27,
                six_loop_physical_magnetic_kernel_dimension=135-108-27,
                witness=w,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                supplied_repair=dict(epsilon='1/1000',additional_cosines=24,
                    action='epsilon*sum_{mu=0..3,ab=0..5} [1-cos(f_ab(x+e_mu)-f_ab(x))]',
                    quadratic_symbol='epsilon*w(z)*L6(z)^dagger*L6(z), w(z)=sum_mu |z_mu-1|^2',
                    w_at_witness='6',normalized_witness_quadratic_form=str(repair_cost),
                    kernel_theorem='At every nonidentity unitary Bloch character w>0. The quadratic magnetic Hessian from the positive sum of short-face, mixed and difference-loop terms has kernel exactly ker(short) intersect ker(L6), identical to the six-loop completion. At identity all commutator chain rows vanish, giving equality there too.',
                    infrared_order='The translated loop difference contributes O(|k|^4) to the magnetic quadratic form: L6(k)=O(k), w(k)=O(|k|^2). Hence it preserves the existing leading O(|k|^2) common cone.',
                    limitations='A supplied positive finite-range lattice improvement, not a microscopic selection theorem or a minimal hardware construction. Kernel equality to the six-loop model does not prove that model has no other exceptional Bloch zeros or establish continuum Lorentz invariance.'),
                conclusion='The specified three-mixed compact action has one complex nongauge magnetic zero at this nonzero Bloch character. The six-loop completion has none there. This is a finite-momentum soft mode/doubler, not a contradiction of the proven generic-rank or leading small-k cone identities.',
                scope='The actual selected105 native faces and six literal commutator chains of the supplied periodic cover. Positive face weights and the supplied positive3x3 mixed K make ker(curl) equal the magnetic Hessian kernel. This does not prove instability, a negative mode, a failure of every three-channel discretization, or a physical extra particle. Electric dynamics and a full Bloch classification are separate.')


if __name__ == '__main__':
    c = certificate()
    path = ROOT/'data/w33_pass12340_mixed_loop_exception.json'
    path.write_text(json.dumps(c,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',exact_ranks=c['exact_ranks'],norm_squared=c['witness']['norm_squared'])))
