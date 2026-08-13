import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def J(n):return json.loads((R/'data'/n).read_text())
def test_5036():
 x=J('PART_W33_PASS5036_APARTMENT_TRITANGENT_TRANSPORT.json');assert x['apartment_tritangent_Z_equals_YU']['rank']==25;assert x['apartment_tritangent_Z_equals_YU']['squared_singular_spectrum']=={'419904':1,'6264':24,'0':20}
def test_5037():
 x=J('PART_W33_PASS5037_STEINBERG_EIGHT_FF_ORBITALS.json');assert x['subdegrees']==[1,3,3,9,9,27,27,81];assert x['R_coefficients']==[81,-27,-27,9,9,-3,-3,1]
def test_5038():
 x=J('PART_W33_PASS5038_SUBDIVISION_JACOBIAN_H1_MOD2.json');assert x['reduced_mod2_laplacian_nullity']==81 and x['binary_cycle_dimension']==81
def test_5039():
 x=J('PART_W33_PASS5039_APARTMENT_FRAME_ROBUSTNESS.json');assert x['uniform_safe_removal_count']==46 and x['explicit_rank_drop_count']==81
def test_5040():assert 'outer apartment stabilizer: order 32' in (R/'analysis/PASS5040_LOCAL_GROUP_CERTIFICATE.md').read_text()
def test_5041():
 x=J('PART_W33_PASS5041_INTEGRAL_APARTMENT_GENERATION.json');assert x['unimodular_apartment_basis']['maximal_minor_determinant_abs']==1 and x['index_of_apartment_lattice_in_cycle_lattice']==1
def test_5042():
 x=J('PART_W33_PASS5042_MINIMUM_CYCLES.json');assert (x['length'],x['dimension'],x['minimum_weight'],x['minimum_vectors'])==(160,81,8,1620)
def test_5043():
 x=J('PART_W33_PASS5043_Q_GENERAL_BUILDING_FAMILY.json');assert x['exact_computational_checks']['q2']['rank']==16 and x['exact_computational_checks']['q3']['rank']==81
