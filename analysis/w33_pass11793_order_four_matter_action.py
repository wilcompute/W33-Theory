"""A full field-lattice Z4 action missed by an order-two-character gate.

Uses the parallel assignment-aware D-flat witness. This is exact charge
arithmetic, not F-flatness, a physical vacuum, or a mass/Yukawa calculation.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from math import lcm,gcd
import gzip,hashlib,json,re
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_pass11793_order_four_matter_action.json'

def certificate():
    witness_path=ROOT/'data/w33_20261009_corrected_assignment_dflat_certificate.json'
    ledger_path=ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz'
    witness=json.loads(witness_path.read_text());raw=json.loads(gzip.decompress(ledger_path.read_bytes()))[witness['model']]
    fields={r['name']:r for r in raw['left']};q={n:list(map(F,r['q'])) for n,r in fields.items()}
    x=list(map(F,witness['BL_coefficients']))
    assert x[0]==0 # No component along the ledger's anomalous U1 coordinate.
    bl={n:sum(a*b for a,b in zip(x,v)) for n,v in q.items()}
    k={n:6*b for n,b in bl.items()}
    assert all(b.denominator==1 for b in k.values())
    charges={n:int(b)%4 for n,b in k.items()}
    order=4//gcd(4,*charges.values());assert order==4
    den=lcm(*(z.denominator for v in q.values() for z in v))
    matrix=sp.Matrix([[int(z*den) for z in v] for v in q.values()])
    basis=hermite_normal_form(matrix.T)
    eps=6*basis.T*sp.Matrix([sp.Rational(z.numerator,z.denominator) for z in x])/den
    assert all(z.q==1 for z in eps)
    eps4=[int(z)%4 for z in eps]
    for i,n in enumerate(q):
        coords=basis.inv()*matrix.row(i).T
        assert all(z.q==1 for z in coords)
        assert sum(a*int(b) for a,b in zip(eps4,coords))%4==charges[n]
    support=witness['positive_support']
    assert all(bl[n]==0 and charges[n]==0 for n in support)
    selected=witness['physical_family_constraints']
    assert all(charges[n]==2 for n in selected)
    fields_sm={'Q':'q_1','u_c':'bu_1','d_c':'bd_3','e_c':'be_1','L':'l_2','H_d':'l_1','H_u':'bl_1'}
    sm={role:charges[n] for role,n in fields_sm.items()}
    assert sm=={'Q':2,'u_c':2,'d_c':2,'e_c':2,'L':2,'H_d':0,'H_u':0}
    operators={'Q_u_Hu':['Q','u_c','H_u'],'Q_d_Hd':['Q','d_c','H_d'],
       'L_e_Hd':['L','e_c','H_d'],'mu_Hu_Hd':['H_u','H_d'],
       'udd':['u_c','d_c','d_c'],'LQd':['L','Q','d_c'],
       'LLe':['L','L','e_c'],'LHu':['L','H_u'],
       'QQQL':['Q','Q','Q','L'],'uude':['u_c','u_c','d_c','e_c']}
    selection={n:dict(charge=sum(sm[z] for z in roles)%4,allowed_by_this_character=sum(sm[z] for z in roles)%4==0)
               for n,roles in operators.items()}
    assert all(selection[n]['allowed_by_this_character'] for n in ['Q_u_Hu','Q_d_Hd','L_e_Hd','mu_Hu_Hd','QQQL','uude'])
    assert all(not selection[n]['allowed_by_this_character'] for n in ['udd','LQd','LLe','LHu'])
    dims={n:abs(__import__('math').prod(int(re.match(r'(-?\d+)',z).group(1)) for z in f['dim'].split(','))) for n,f in fields.items()}
    grav=sum(dims[n]*bl[n] for n in fields);cubic=sum(dims[n]*bl[n]**3 for n in fields)
    assert grav==cubic==0
    vev_matrix=sp.Matrix([[sp.Rational(z.numerator,z.denominator) for z in q[n]] for n in support])
    family_basis={'Q':['q_1','q_2','q_3'],'u_c':['bu_1','bu_2','bu_3'],
                  'd_c':['bd_3','bd_5','bd_9'],'e_c':['be_1','be_2','be_3'],
                  'L':['l_2','l_3','l_4'],'H_d':['l_1'],'H_u':['bl_1']}
    return dict(schema='w33.pass11793.order_four.v1',status='PASS',model=witness['model'],
        source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        input_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n') if p.suffix=='.json' else p.read_bytes()).hexdigest() for p in [witness_path,ledger_path]},
        prior='Parallel3fdef4a22 owns the assignment-aware support and B-L covector;975aad94e independently checks its rational charges and absence of full-lattice Z2 character. This constructs the larger character instead of inferring impossibility from Z2.',
        generator='g(phi_n)=exp(i*pi*3*BL(phi_n))*phi_n=i^(6BL(phi_n))*phi_n',
        field_action_order=order,lattice_rank=basis.cols,lattice_denominator=den,
        integral_charge_lattice_basis=[[str(z) for z in row] for row in basis.tolist()],
        integral_character=[int(z) for z in eps],character_mod4=eps4,
        charge_multiplicities=dict(sorted(Counter(charges.values()).items())),all_field_charges=charges,
        vev_charges={n:charges[n] for n in support},all_vevs_continuous_BL_neutral=True,
        selected_matter_charges={n:charges[n] for n in selected},candidate_three_family_Higgs_basis=family_basis,
        MSSM_role_charges=sm,operator_selection=selection,
        quotient_action='On the selected matter/Higgs carrier, g^2 acts trivially and the image Z4/<g^2> is Z2 with matter odd and Higgs even. On64 full fields g has phases+/-i, so its full field action has order4. No order-two element of this cyclic image acts as selected matter parity.',
        continuous_gravitational_trace=str(grav),continuous_cubic_trace=str(cubic),anomalous_U1_coefficient=str(x[0]),
        vev_charge_rank=vev_matrix.rank(),unbroken_abelian_lie_dimension=9-vev_matrix.rank(),
        limits='Charge action and classical D-flat support only. Neutrality of condensates preserves a continuous BL direction in this gauge-charge model; a physical discrete remnant also requires axion/global-gauge-group analysis. Extra unbroken U1s remain. No F-flatness, exact physical family/Higgs identification, axion/Stueckelberg/discrete anomaly completion, Yukawa coefficients, vectorlike mass ranks or dimension5 proton protection is established. Allowed operators are not proved present; QQQL and uude are not forbidden by this character.',
        literature=['https://arxiv.org/abs/0708.2691','https://arxiv.org/abs/hep-ph/0512163'])

if __name__=='__main__':
    j=certificate();OUT.write_text(json.dumps(j,indent=2)+'\n')
    print('11793 PASS exact order4 field character',j['character_mod4'],'MSSM matter sign,VEVs/Higgs neutral; not F-flat vacuum')
