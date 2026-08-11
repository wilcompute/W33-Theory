import json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def J(name): return json.loads((ROOT/'data'/name).read_text())

def test_pass4833_4840_packet():
    a=J('PART_W33_PASS4833_4838_LEVI_SUBCODE_CODE399.json')
    assert a['dimensions']=={'Levi':64,'kernel':378,'code399':399,'intersection_Levi_code399':64,'sum_Levi_code399':399,'quotient_code399_over_Levi':335}
    assert a['cold_puncture']['injective']

    s=J('PART_W33_PASS4834_CODE399_OPTIMAL_SCHEDULE.json')
    assert s['optimal_schedule_depth']==3 and s['rank']==1626
    assert s['maximum_outer_coordinate_multiplicity']==4
    assert s['layer_check_counts']==[945,675,6]

    d=J('PART_W33_PASS4835_4839_INTRINSIC_DUALSHELL_AUT_FALSIFIER.json')
    assert d['quotient_automorphism_group']['structure']=='S3^135 : S135'
    assert not d['comparison_to_PGSp']['equal']

    c=J('PART_W33_PASS4836_LEVI_MINIMUM_ORBITS.json')
    assert c['minimum_words']==1080
    assert c['PSp']['orbit_count_on_minimum_words']==1 and c['PSp']['stabilizer_order']==24
    assert c['PGSp']['orbit_count_on_minimum_words']==1 and c['PGSp']['stabilizer_order']==48

    i=J('PART_W33_PASS4840_LEVI_CYCLE_K33_INCIDENCE.json')
    assert (i['binary_cycle_degree'],i['K33_degree'],i['total_incidence'])==(3,9,3240)
    assert i['incidence_matrix_ranks']=={'F2':324,'F3':359,'F5':360,'F7':360}

    b=J('PART_W33_PASS4825_BRAUER_LOEWY_CLOSURE.json')
    assert b['trivial_composition_multiplicity']==71
    assert b['Loewy_consequences']['Loewy_length_lower_bound']==3
    assert b['Loewy_consequences']['trivial_factors_forced_strictly_between_trivial_socle_and_head_at_least']==66

    r=J('PART_W33_PASS4827_PGSP_SIGN_BURNSIDE.json')
    assert r['PSp']['Burnside_orbit_count']==711679993497112
    assert r['PGSp']['Burnside_orbit_count']==355840805040988
    assert r['PSp']['affine_fixed_sign_sectors']==r['PGSp']['affine_fixed_sign_sectors']==1

    h=J('PART_W33_PASS4830_SIGN_LEVI_MODULE_INTERTWINER.json')
    assert h['PSp']['Hom_dimension']==h['PGSp']['Hom_dimension']==1
    assert h['PSp']['unique_nonzero_intertwiner_rank']==h['PGSp']['unique_nonzero_intertwiner_rank']==64

    f=J('PART_W33_PASS4828_PARAMETRIC_OUTAGE_FLOW.json')
    expected={'one_hot':'67/5952','two_hot_adjacent':'665/59746','two_hot_nonadjacent':'133/11946','one_vertex_fiber_removed':'189/16538','two_vertex_adjacent_removed':'1767/153094','two_vertex_nonadjacent_removed':'351/30670'}
    for name,val in expected.items():
        C=f['cases'][name]; assert C['lambda_at_rho1']==val
        lines=[(Fraction(P['A']),Fraction(P['B'])) for P in C['pieces']]
        assert min(A+B for A,B in lines)==Fraction(val)
        bp=[Fraction(x) for x in C['breakpoints']]
        assert bp==sorted(bp)
        for (A,B),(D,E),x in zip(lines,lines[1:],bp): assert A+B*x==D+E*x

    z=J('PART_W33_PASS4837_HEAVY_EVIDENCE_CLOSURE.json')
    assert z['closed_carryovers']==[4825,4827,4828,4830]
