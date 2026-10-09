"""Exhaustive 176-field cubic *necessary* condition audit.
Recombination with full CFT vertex operators is impossible from the present
compressed metadata; no claim about nonzero worldsheet amplitudes.
"""
from pathlib import Path
import sys,json,math
from itertools import combinations_with_replacement
from collections import defaultdict,Counter
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
import w33_pass11797_11801_five_physical_fronts as P

def main():
    raw,prior,fields,support,q=P.load()
    names=sorted(fields)
    # A uniform integer lattice embedding of every printed rational charge.
    denominator=math.lcm(*(x.denominator for v in q.values() for x in v))
    charges=[tuple(int(denominator*x) for x in q[n]) for n in names]
    neg=lambda v:tuple(-x for x in v)
    pair_map=defaultdict(list)
    for i in range(len(names)):
        for j in range(i,len(names)):
            pair_map[tuple(a+b for a,b in zip(charges[i],charges[j]))].append((i,j))
    gauge_candidates=[]
    for k,v in enumerate(charges):
        for i,j in pair_map.get(neg(v),[]):
            if j<=k:gauge_candidates.append((names[i],names[j],names[k]))
    screening=Counter(); retained=[]; examples=[]
    for mono in gauge_candidates:
        screening['gauge_neutral_with_repetition']+=1
        fits=P.selection(mono,fields)
        screening['necessary_R_and_nonR_pass']+=int(fits)
        screening['necessary_R_and_nonR_fail']+=int(not fits)
        if fits:
            retained.append(mono)
            hodd=sum(abs(int(fields[n]['dim'].split(",")[3]))==2 for n in mono)
            screening['hidden_SU2_even_doublets']+=int(hodd%2==0)
    for names3 in [('n_17','n_82','n_81'),('n_17','n_82','n_83')]:
        assert all(sum(q[n][j] for n in names3)==0 for j in range(9))
        examples.append({"fields":list(names3),"necessary_R_and_nonR":bool(P.selection(names3,fields)),
          "total_oscillator_count":sum(fields[n]['oscillator_count'] for n in names3),
          "corrected_R":[[str(v) for v in P.corrected_r(fields[n])] for n in names3]})
    assert examples[0]['necessary_R_and_nonR'] and not examples[1]['necessary_R_and_nonR']
    field_keys=set.intersection(*(set(v.keys()) for v in fields.values()))
    required_absent=["constructing_space_group_element_full","left_moving_oscillator_polarizations",
        "right_moving_picture_changing_distribution","gamma_eigenphase_full_action",
        "worldsheet_instanton_solutions","kahler_complex_structure_moduli"]
    assert not (set(required_absent)&field_keys)
    out=dict(status="PASS",model=raw['model'],field_count=len(names),
        exact_charge_integer_denominator=denominator,
        cubic_repetition_policy="monomials a<=b<=c (with replacement), not unordered distinct-only triples",
        screening=dict(screening),number_screened_by_R_but_not_worldsheet=len(retained),
        examples=examples,required_amplitude_inputs_missing_from_field_schema=required_absent,
        present_field_schema=sorted(field_keys),
        decisive_boundary="Passing these necessary U1, corrected-R, nonR tests cannot infer nonzero superpotential amplitude. The source does not supply the polarized oscillator/constructing-group/instanton data needed for complete Rules 4/5, worldsheet correlator or F/D-flatness.",
        literature=["https://arxiv.org/abs/1107.2137","https://arxiv.org/abs/1401.6162"])
    target=ROOT/"data/w33_20261009_round18_heterotic_cubic_information_bound.json"
    target.write_text(json.dumps(out,indent=2)+"\n")
    print("HETEROTIC SCREENING",dict(screening),"EXAMPLES",examples,flush=True)
if __name__=="__main__":main()
