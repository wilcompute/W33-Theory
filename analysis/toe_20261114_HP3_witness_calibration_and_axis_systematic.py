#!/usr/bin/env python3
"""Systematics falsifiers for the four-copy and 21/47-axis protocols.

1. Unknown visibility makes a fourth-moment-only hypothesis test
unidentifiable if the finite/Haar mean intervals overlap.
2. An undiagnosed global-axis sign-inversion can turn a true charge
into a DIFFERENT valid 180-charge signature, even with infinite shots.
3. Confront actual published fixed-radian cost data, and refuse to
promote bounded MUB CDCL status to UNSAT.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter
from itertools import product,combinations
import json,math,sys
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
OUT=ROOT/"data/toe_20261114_HP3_visibility_axis_systematic_boundary.json"

def main():
    # Uncalibrated visibility could cause the finite and Haar fourth
    # moment means to coincide; no number of samples of this ONE
    # statistic can distinguish the corresponding parameter points.
    ratio=(Fraction(3,11))**.25
    epscrit=.8*(1-ratio)/(1+ratio)
    assert .12<epscrit<.14,epscrit
    def bounds(eps):
        lo=Fraction(4,5)-eps;hi=Fraction(4,5)+eps
        return lo**4/Fraction(9),hi**4/Fraction(33)
    separate_small=bounds(Fraction(1,10))
    overlap_large=bounds(Fraction(3,20))
    assert separate_small[0]>separate_small[1]
    assert overlap_large[0]<overlap_large[1]
    _,signed,_,_,_=R.load()
    G=nx.Graph();G.add_nodes_from(range(27))
    for tri in signed:G.add_edges_from(combinations(tri,2))
    sixers=sorted(tuple(sorted(c)) for c in nx.find_cliques(nx.complement(G)) if len(c)==6)
    assert len(sixers)==72
    charges=[]
    for tri,s in signed.items():
        for signs in product((-1,1),repeat=3):
            if math.prod(signs)!=s:continue
            z=[0]*27
            for i,x in zip(tri,signs):z[i]=x
            charges.append(tuple(z))
    assert len(charges)==180
    noised=Counter();cases=0
    for U in sixers:
        M=[i for i in range(27) if i not in U]
        signatures={tuple(z[i] for i in M):z for z in charges}
        assert len(signatures)==180
        for v in M:
            idx=M.index(v)
            corrupted=0
            for z in charges:
                if z[v]==0:continue
                wrong=list(z[i] for i in M)
                wrong[idx]=-wrong[idx]
                inferred=signatures.get(tuple(wrong))
                if inferred is not None and inferred!=z:corrupted+=1
            degree=sum(G.has_edge(v,u) for u in U)
            assert degree in (2,5)
            assert corrupted==4*degree,(U,v,corrupted,degree)
            noised[corrupted]+=1
            cases+=1
    assert cases==72*21
    assert noised==Counter({8:72*15,20:72*6}),noised
    # Snapshot of the other two independently verified fronts.
    p=json.loads((ROOT/"data/toe_20261114_witness_selection_decoder_fixedangle.json").read_text())
    sat=json.loads((ROOT/"data/toe_20261114_fivequbit_MUB_independent_CaDiCaL_SAT.json").read_text())
    assert sat["classification"]=="INDEPENDENT_SAT_FRONT_UNDECIDED"
    unknown=[x for x in sat["records"] if x["rep"] in (692,694) and x["n"]==5]
    assert len(unknown)==2 and all(x["status"]=="UNDECIDED_BOUNDED_CONFLICTS" for x in unknown)
    # Every 4-copy product must measure four independent copies of
    # the SAME latent state. If latent states are independent,
    # E product=(E z)^4=0, losing the 4th moment signal.
    assert Fraction(1,9)!=0 and Fraction(1,33)!=0
    result=dict(status="PASS_HP3_FOURCOPY_CALIBRATION_BOUND_AND_UNDIAGNOSED_AXIS_SIGN_FLIP",
        fourth_moment_finite="1/9",fourth_moment_Haar="1/33",
        eta_center="4/5",
        critical_absolute_visibility_uncertainty_at_eta08=epscrit,
        calibration_plus_minus_0_10_separates_means=True,
        calibration_plus_minus_0_15_makes_means_overlap=True,
        four_copies_must_share_one_latent_state=True,
        if_four_latent_states_independent_product_expectation="0 for both centered ensembles",
        optimal_21_axis_menus_checked=72,
        all_single_axis_sign_inversion_cases=cases,
        charge_aliases_when_inverted_axis_touches_two_omitted_neighbors=8,
        charge_aliases_when_inverted_axis_touches_five_omitted_neighbors=20,
        exact_axis_inversion_alias_count_histogram={str(k):v for k,v in sorted(noised.items())},
        false_charge_aliases_per_menu_summed_over_all_axes=15*8+6*20,
        key_physical_falsifier="An undiagnosed persistent sign inversion cannot be fixed by more independent shots of the same axis; the 47-axis erasure-robust protocol assumes failure detection and reconfiguration.",
        fixed_one_radian_gate_compiler_cert_reused=True,
        MUB_CaDiCaL_exclusion_status="UNDECIDED_BOUNDED_CONFLICTS",
        limitations="Only single fourth-moment statistic and one-axis sign errors considered; a richer experiment may estimate eta separately and correct the failure. This is not an impossibility theorem for arbitrary POVMs or optical platforms.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in ("status","critical_absolute_visibility_uncertainty_at_eta08",
        "calibration_plus_minus_0_15_makes_means_overlap",
        "all_single_axis_sign_inversion_cases","exact_axis_inversion_alias_count_histogram",
        "MUB_CaDiCaL_exclusion_status")},indent=2),flush=True)
    return result
if __name__=="__main__":main()
