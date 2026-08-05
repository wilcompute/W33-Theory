from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_seven_front_digest():
    mod=load(ROOT/'analysis/bt3542_3548_borel_commutant_outer_s6_analytic.py','packet')
    result={
      'passes':list(range(3542,3549)),
      'pass3542_borel_cyclic_quotient':mod.borel_quotient(),
      'pass3543_borel_commutant':mod.borel_commutant(),
      'pass3544_clique_proof_certificates':mod.certificate_tests(),
      'pass3545_factorization_field_compiler':mod.factorization_field_contract(56),
      'pass3546_spectral_analytic_compiler':mod.spectral_analytic(),
      'pass3547_bonkers_outer_S6_HS':mod.outer_s6_hs(),
      'pass3548_bonkers_field_fusion':{
          'statement':'The Perkel Borel commutant has two intrinsic imaginary quadratic channels sqrt(-19) and sqrt(-3), while adjacency adds the independent golden field sqrt(5) on the 36-space.',
          'field_stack':['Q(sqrt(-19))','Q(sqrt(-3))','Q(sqrt(5))'],
          'commutative_adjacency_layer':'Q[A,B19] ~= Q x Q x Q x Q(sqrt(5)), exact matrix-span dimension 5',
          'full_equivariant_layer':'Q + M3(Q(sqrt(-19))) + Q(sqrt(-3)), dimension 21',
          'interpretation':'symmetry field, phase field, and spectral field are distinct exact channels rather than one numerological field identification',
          'boundary':'Algebraic decomposition only; no physical unification claim.'},
    }
    assert mod.sha(result)=='a98621cc2f2378eaed09b8f747022f419a16fbb33433336eeb8f2414f4273f1a'


def test_borel_and_commutant_fronts():
    mod=load(ROOT/'analysis/bt3542_3548_borel_commutant_outer_s6_analytic.py','packet2')
    b=mod.borel_quotient()
    assert b['branch_partition']==[56,56,56]
    assert b['total_internal_signature_count']==24
    c=mod.borel_commutant()
    assert c['orbital_rank']==21
    assert c['simple_component_dimensions_over_Q']==[1,2,18]
    assert c['adjacency_block_algebra']['dimension']==5


def test_outer_s6_and_analytic_fronts():
    mod=load(ROOT/'analysis/bt3542_3548_borel_commutant_outer_s6_analytic.py','packet3')
    o=mod.outer_s6_hs()
    assert o['outer_automorphism_certificate']['faithful_pentad_action_order']==720
    assert o['outer_automorphism_certificate']['pentad_image_type']==[2,2,2]
    assert o['HS_reconstruction'].endswith('SRG(50,7,0,1).')
    f=mod.factorization_field_contract(56)
    assert f['constructed_vertices']==3250 and f['degree']==57
    a=mod.spectral_analytic()
    assert a['graphs'][0]['ihara_reciprocal'].startswith('(1-u^2)^200')
    assert a['graphs'][1]['closed_walk_traces_0_to_10']['3']==0


def test_proof_dag_self_tests():
    mod=load(ROOT/'analysis/bt3544_clique_proof_dag.py','proofdag')
    result=mod.self_tests()
    assert result=={
        'cases':31,
        'digest':'37aef1439c7474fe54d3cc3bcdf62e4ab5085f43f4edd9706f9bce2a153753d6',
    }
