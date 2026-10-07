"""A phase-blind CP-even Hesse flavon EFT; no fitted physical flavor claim.

Prior owners11591/11597 supply the tensor pencil;10972 supplies the distinct
clock Landau selector. Tetrahedral/Hesse quotient geometry is classical.
"""
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/w33_pass11600_dynamical_hesse_flavor.json'


def exact_group():
    group = []
    for perm in itertools.permutations(range(3)):
        parity = (-1)**sum(perm[i] > perm[j] for i in range(3) for j in range(i+1, 3))
        for signs in itertools.product([-1, 1], repeat=3):
            if np.prod(signs) != 1:
                continue
            M = s.zeros(3)
            for i in range(3):
                M[i, perm[i]] = signs[i]
            group.append((M, parity))
    return group


def tensor_and_bloch():
    w = -s.Rational(1, 2) + s.I*s.sqrt(3)/2
    F = s.Matrix(3, 3, lambda i,j: w**(i*j)/s.sqrt(3))
    P = s.diag(1, 1, w)
    tensors = []
    for mode in range(2):
        tensors.append(s.Matrix([s.Integer(len(set(t)) == (1 if mode == 0 else 3))
                                 for t in itertools.product(range(3), repeat=3)]))
    B = s.Matrix.hstack(tensors[0]/s.sqrt(3), tensors[1]/s.sqrt(6))
    assert B.conjugate().T*B == s.eye(2)
    RF = s.Matrix([[1, s.sqrt(2)], [s.sqrt(2), -1]])/s.sqrt(3)
    RP = s.diag(1, w)
    for G, R in [(F, RF), (P, RP)]:
        residual = s.kronecker_product(G, G, G)*B-B*R
        assert all(s.simplify(v) == 0 for v in residual)
    old = json.loads((ROOT/'data/PART_W33_PASS11597_FAMILY_CLIFFORD_BREAKING.json').read_text())
    oldF = s.Matrix([[s.sympify(a) for a in row] for row in old['F_on_Hesse_pair']])
    C = s.diag(1, 1/s.sqrt(2))
    assert s.simplify(C*oldF*C.inv()-RF) == s.zeros(2)
    # Tetrahedral orthonormal axes: F is a pi rotation about axis0; P cycles them.
    axes = s.Matrix([[s.sqrt(s.Rational(2,3)), -s.sqrt(s.Rational(1,6)), -s.sqrt(s.Rational(1,6))],
                     [0, 1/s.sqrt(2), -1/s.sqrt(2)],
                     [1/s.sqrt(3), 1/s.sqrt(3), 1/s.sqrt(3)]])
    assert axes.T*axes == s.eye(3)
    pauli = [s.Matrix([[0,1],[1,0]]), s.Matrix([[0,-s.I],[s.I,0]]), s.diag(1,-1)]
    adj = lambda R: s.Matrix(3,3,lambda i,j:s.simplify(s.trace(pauli[i]*R*pauli[j]*R.conjugate().T)/2))
    rotations = [s.simplify(axes.T*adj(R)*axes) for R in [RF, RP]]
    assert rotations[0] == s.diag(1,-1,-1)
    assert rotations[1] == s.Matrix([[0,0,1],[1,0,0],[0,1,0]])
    cp = s.simplify(axes.T*s.diag(1,-1,1)*axes)
    assert cp == s.Matrix([[1,0,0],[0,0,1],[0,1,0]])
    return dict(normalized_F=[[str(a) for a in row] for row in RF.tolist()],
                normalized_P=[[str(a) for a in row] for row in RP.tolist()],
                tensor_norms=[3,6], prior_coordinate_conversion='C=diag(1,1/sqrt2); C F_old C^-1=F_normalized',
                Bloch_axes=[[str(a) for a in row] for row in axes.tolist()],
                Bloch_F=rotations[0].tolist(), Bloch_P=rotations[1].tolist(),
                coefficient_CP='complex conjugation swaps tetrahedral coordinates1 and2',
                coupling='Tensor field Phi transforms in Sym^3(V); Phi-dagger contracted with the symmetric family matter/Higgs tensor is invariant. With normalized components u, a=conjugate(u0)/sqrt3/M and b=conjugate(u1)/sqrt6/M, up to one overall real interaction coefficient.')


def invariants_and_minima():
    x,y,z,t = s.symbols('x y z t', real=True)
    variables = s.Matrix([x,y,z])
    p2=x*x+y*y+z*z; p3=x*y*z; p4=x**4+y**4+z**4
    W=(x*x-y*y)*(y*y-z*z)*(z*z-x*x)
    group = exact_group()
    for M, parity in group:
        sub = dict(zip(variables, M*variables))
        assert s.expand(p3.subs(sub, simultaneous=True)-p3) == 0
        assert s.expand(p4.subs(sub, simultaneous=True)-p4) == 0
        assert s.expand(W.subs(sub, simultaneous=True)-parity*W) == 0
    point=s.Matrix([1,2,3]); orbit={tuple(M*point) for M,parity in group}
    A4={tuple(M*point) for M,parity in group if parity==1}
    assert len(orbit)==24 and len(A4)==12
    # All global minima: squares have elementary symmetric data14,49,36.
    assert s.factor(t**3-14*t*t+49*t-36)==(t-1)*(t-4)*(t-9)
    jac=s.Matrix([[s.diff(f,v) for v in variables] for f in [p2,p3,p4]]).det()
    assert s.expand(jac+8*W)==0
    h=s.hessian((p3-6)**2+(p4-98)**2,variables).subs(dict(zip(variables,point)))
    tangent=s.Matrix([[2,3],[-1,0],[0,-1]])
    restricted=tangent.T*h*tangent
    assert restricted[0,0]>0 and restricted.det()==921600
    # Every generic CP-even phase-blind polynomial through field degree14,
    # restricted to fixed norm, is A p3+B p4+C p3^2+D p3 p4+constant.
    a,b,c,d=s.symbols('A B C D', real=True);i3,i4=s.symbols('I3 I4',real=True)
    angular=a*i3+b*i4+c*i3*i3+d*i3*i4
    assert s.hessian(angular,[i3,i4]).det()==-d*d
    return dict(parent_projective_group='G216',pencil_quotient='A4, order12',
        generic_projective_stabilizer='(C3xC3):C2, order18; projective image of Delta54. Exact vector stabilizers depend on the scalar lift and the separate U1 phase.',
        model_inventory='one canonical complex two-component tensor field, an exact common-phase U1, coefficient CP, polynomial scalar potential, no additional order parameters',
        invariant_ring='CP extends A4 to W(D3)=S4. R[x,y,z]^W=R[p2,p3,p4]; degrees2,3,4. At fixed rho=u-dagger u, p2=rho^2.',
        minimal_dimension='16: below field degree16 the generic fixed-radius angular potential has Hessian determinant -D^2 in coordinates(p3,p4), or an exactly flat p4 direction. No strict isolated generic ray minimum is possible in this declared CP-even phase-blind inventory.',
        potential='kappa(rho-v^2)^2 + lambda3/M^8 (xyz-[3/(7sqrt14)]rho^3)^2 + lambda4/M^12 (x^4+y^4+z^4-rho^4/2)^2, with all coefficients positive and M,v>0',
        global_minimum_energy=0, global_minimum_rays=24, A4_orbits=2, A4_orbit_sizes=[12,12],
        minimum_squared_Bloch_coordinates=['rho^2/14','2rho^2/7','9rho^2/14'],
        minimum_sign_product='positive', CP_odd_invariant_values=['+15rho^6/343','-15rho^6/343'],
        CP_breaking='The24 rays form two A4 orbits exchanged by coefficient conjugation. W is A4 invariant and CP odd, nonzero at every minimum; no generalized parent CP fixes a vacuum ray.',
        tangent_Hessian_at_unscaled_point=restricted.tolist(), tangent_Hessian_determinant=921600,
        phase_boundary='The common U1 gives a circle above each ray: one phase Goldstone if global, or a gauge redundancy if separately gauged. Only radial and two angular directions are stabilized; no fully gapped vacuum is claimed.',
        UV_boundary='Dimensions12 and16 operators are supplied EFT terms. Neither their coefficients nor v/M nor this extra tensor field are derived from W33. Holomorphic U1-breaking terms, extra fields and non-polynomial potentials evade the dimension16 bound.')


def CP_yukawa_witness():
    br,bi=s.symbols('br bi',real=True);b=br+s.I*bi
    Y=lambda h:s.Matrix([[h[0],b*h[2],b*h[1]],[b*h[2],h[1],b*h[0]],[b*h[1],b*h[0],h[2]]])
    U=Y([1,2,4]);D=Y([3,1,2]);Hu=U*U.conjugate().T;Hd=D*D.conjugate().T
    K=Hu*Hd-Hd*Hu;poly=s.factor(s.im(s.expand(s.trace(K**3))))
    scale=s.sqrt(14)+2*s.sqrt(3)
    value=s.simplify(poly.subs({br:-s.sqrt(3)/(2*scale),bi:-1/(2*scale)}))
    assert value != 0 and float(value)<-1700
    assert s.simplify(poly.subs(bi,-bi)+poly)==0
    return dict(a='1 (overall scale removed)',b='-(sqrt3+i)/[2(sqrt14+2sqrt3)]',
        real_Higgs_directions_up=[1,2,4],real_Higgs_directions_down=[3,1,2],
        Im_trace_commutator_cubed=str(value),numeric=float(value),CP_polynomial=str(poly),
        scope='One exact nonzero weak-basis CP witness at one selected ray and separately supplied real Higgs directions. Conjugating the vacuum reverses its sign. It does not predict CKM/PMNS, measured masses or a Higgs alignment.')


def angular_masses():
    m=s.Matrix([1,2,3])/s.sqrt(14);projector=s.eye(3)-m*m.T
    g3=projector*s.Matrix([m[1]*m[2],m[0]*m[2],m[0]*m[1]])
    g4=projector*s.Matrix([4*a**3 for a in m])
    G=s.simplify(s.Matrix.hstack(g3,g4).T*s.Matrix.hstack(g3,g4))
    assert G[0,0]==s.Rational(181,1372) and G.det()==s.Rational(3600,117649)
    assert s.factor(4*G.det()/G[0,0])==s.Rational(57600,62083)
    return dict(gradient_Gram=[[str(a) for a in row] for row in G.tolist()],
        canonical_kinetic='Lkin=partial u-dagger partial u; after phase quotient and rho=v^2 the Bloch kinetic term is v^2/4 |partial m|^2.',
        exact_masses='m_plus/minus^2=2/v^2 [A g3^2+B g4^2 +/- sqrt((A g3^2+B g4^2)^2-4AB detG)], A=lambda3 v^12/M^8, B=lambda4 v^16/M^12',
        heavy_leading='(181/343) lambda3 v^2 (v/M)^8',light_leading='(57600/62083) lambda4 v^2 (v/M)^12',
        boundary='These are two extra tensor-field angular masses in the declared EFT, not fermion masses. For positive fixed lambda3,lambda4 and v/M small the hierarchy follows. Symmetry also allows lower-dimension p3 and p4 terms; their absence/correlation is not radiatively protected here. Quantum corrections can change the vacuum and hierarchy. The common phase U1 must extend consistently to the Higgs/interaction sector or be only a scalar-sector assumption.')


def canonical_hash(path):
    if path.suffix=='.json':
        raw=json.dumps(json.loads(path.read_text()),sort_keys=True,separators=(',',':')).encode()
    else:
        raw=path.read_bytes().replace(b'\r\n',b'\n')
    return hashlib.sha256(raw).hexdigest()


def produce():
    result={'status':'PASS','reservation':'3db837b54','pass':11600}
    for key,fn in [('tensor',tensor_and_bloch),('dynamics',invariants_and_minima),('CP_transfer',CP_yukawa_witness),('angular_masses',angular_masses)]:
        result[key]=fn();print(key,'PASS',flush=True)
    inputs=['data/PART_W33_PASS11591_SPIN10_DELTA54_HESSE_YUKAWA.json',
            'data/PART_W33_PASS11597_FAMILY_CLIFFORD_BREAKING.json',
            'analysis/w33_pass10972_tetrahedral_cubic_clock_selector.py']
    result['source_sha256']={p:canonical_hash(ROOT/p) for p in inputs}
    result['producer_sha256']=canonical_hash(Path(__file__))
    OUT.write_text(json.dumps(result,indent=2,default=str)+'\n')
    return result


if __name__=='__main__':
    produce()
