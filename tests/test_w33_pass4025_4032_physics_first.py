from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/PART_4025_4032_PHYSICS_FIRST_UNIVERSAL_COMPUTER.json'
def load():return json.loads(DATA.read_text(encoding="utf-8"))
def test_certificate_and_five_fronts():
 x=load();assert x['semantic_sha256']=='cc50a83926bd9d32770c33dcfb48ba04640d3601a3fbf64b29f34bb22f940a2f'
 assert x['status']=='PASS_EXACT_PHYSICS_FIRST_FIVE_FRONT_THREE_BONKERS_TOE_NOT_ESTABLISHED'
 assert x['pass4025_exact_revival_error_budget']['optimal_retiming']=='delta_tau = -(17*pi/288) delta_d'
 assert x['pass4026_exact_polar_compiler']['operator_error']<1e-12
 assert x['pass4027_mode_H1_bridge']['rank']==1
 assert x['pass4028_noise_aware_tomography']['common_delay_invariant'] is True
 assert x['pass4029_algebra_execution']['status']=='queued'
def test_three_bonkers_and_claim_boundary():
 x=load();assert x['pass4030_causality_speed']['diameters']=={'Levi':4,'W33':2,'line_graph':4}
 assert x['pass4031_spectral_dimension']['W33_ds_max']['value']<4
 assert abs(x['pass4032_thermodynamic_holographic_capacity']['capacity_bits']-6.339850002884624)<1e-15
 assert 'TOE remain hypotheses' in x['pass4032_thermodynamic_holographic_capacity']['verdict']
