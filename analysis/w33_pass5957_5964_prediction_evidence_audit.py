#!/usr/bin/env python3
"""Pass5957-5964: fail-closed audit of recent physical prediction scripts.

This packet distinguishes exact finite/combinatorial arithmetic from actual physical
prediction derivations. It intentionally does not judge agreement with current data;
it asks the prior question: does the producer derive the observable without assuming
the desired scaling law, inserting an external physical scale, or back-solving a
target value?
"""
from __future__ import annotations
import json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS5957_5964_PREDICTION_EVIDENCE_AUDIT.json'

FILES={
 'linf': ROOT/'scripts'/'w33_linf_bracket_mass_ratios.py',
 'electron': ROOT/'scripts'/'w33_electron_seed_packet_derivation.py',
 'weyl': ROOT/'scripts'/'w33_weyl_law_4volume.py',
 'ym': ROOT/'scripts'/'w33_ym_mass_gap_1818.py',
 'nu': ROOT/'scripts'/'w33_neutrino_mass_leech.py',
 'inflation': ROOT/'scripts'/'w33_inflation_r_1_45.py',
 'scalar': ROOT/'scripts'/'w33_scalar_resonance_3215gev.py',
}

def text(k): return FILES[k].read_text()

def octahedron_tree_count():
    # Complete multipartite K_{2,2,2}: tau = n^(r-2) prod_i (n-n_i)^(n_i-1)
    # with n=6,r=3,n_i=2 gives 6*4^3=384.
    return 6*4**3

def main():
    S={k:text(k) for k in FILES}

    # 5957: L-infinity claim is not a computed MC solution / transferred bracket.
    assert "mc_residual = K - LA" in S['linf']
    assert "mc_sum_formal = Y1 + Y2 + Y3" in S['linf']
    assert "not zero" in S['linf']
    assert "mc_equation': 'l_1/1! + l_2/2! + l_3/3! = 0" in S['linf']

    # 5958: refinement exponent is inserted into the definition used to infer d=4.
    assert "return n**4 * N1" in S['weyl']
    assert "multiplicities scaled by n^4" in S['weyl']
    assert "dimension_from': 'N ~ n^4" in S['weyl']

    # 5959: electron packet is exact arithmetic, but the physical map is an ansatz.
    electron_D=2*7**2*(4**2+1)*4**2*13
    assert electron_D==346528
    assert "deviation_sigma':  deviation_pct / 0.87" in S['electron']

    # 5960: YM target is explicitly back-solved for the effective QCD scale.
    assert "Solve for Lambda_QCD_eff that gives exactly 1818 MeV" in S['ym']
    assert "lambda_eff = delta_ym_target / coeff" in S['ym']
    ym_coeff=12*math.sqrt(13/40)
    ym_lambda_backsolve=1818/ym_coeff

    # 5961: neutrino denominator was repaired after the initial formula missed by 4.
    assert "40,884,480  (too large!)" in S['nu']
    assert "So: 10,221,120 = 6 * 480 * 13 * 273" in S['nu']
    nu_D=6*480*13*(1+4**2+4**4)
    assert nu_D==10221120

    # 5962: inflation observable map is assignment r := reciprocal count.
    assert "r = Fraction(1, N_TRITANGENT_PLANES)" in S['inflation']
    assert "Physical interpretation:" in S['inflation']
    assert "slow-roll suppression factor is 1/45" in S['inflation']
    assert "ns_deviation_sigma" in S['inflation']

    # 5963: scalar graph count is exact; mass formula is an un-derived multiplier.
    assert "ratio = Fraction(tau_O, G_M)" in S['scalar']
    assert "m_scalar_gev = M_HIGGS_GEV * float(ratio)" in S['scalar']
    tau=octahedron_tree_count(); assert tau==384

    out={
      'schema':'w33.pass5957_5964.prediction_evidence_audit.v1',
      'status':'PASS_CORRECTION',
      'pass_5957_linf':{
        'verdict':'NOT_DERIVED',
        'evidence':['producer sets mc_residual=k-lambda=10, not zero',
                    'producer computes mc_sum_formal=Y1+Y2+Y3 and comments that it is not zero',
                    'l2/l3 mass ratios are assigned from pre-existing denominator formulas rather than evaluated from an explicit transferred L-infinity structure'],
        'retained':'exact arithmetic of the stated ratios may remain as an ansatz table'},
      'pass_5958_weyl':{
        'verdict':'CIRCULAR',
        'evidence':['N_n_count is defined to return n^4*N1',
                    'the same imposed n^4 scaling is then used to infer dimension d=4',
                    'finite spectrum has N(4)=362 and N(16)=440 while C_W=480 is inserted separately'],
        'retained':'finite D^2 spectrum and any independently proved refinement census'},
      'pass_5959_electron':{
        'verdict':'NUMERICAL_ANSATZ_NOT_PREDICTION',
        'exact_denominator':electron_D,
        'evidence':['factor product 2*49*17*16*13=346528 is exact',
                    'no mass operator/Yukawa dynamics in the producer forces this product',
                    'the reported sigma is manufactured as deviation_pct/0.87, not propagated from an uncertainty model'],
        'retained':'integer factorization and comparison-only status'},
      'pass_5960_yang_mills':{
        'verdict':'TARGET_BACKSOLVED',
        'coefficient_12_sqrt_13_over_40':ym_coeff,
        'lambda_eff_MeV_backsolved_for_1818':ym_lambda_backsolve,
        'evidence':['producer explicitly says solve for Lambda_QCD_eff that gives exactly 1818 MeV',
                    'producer sets delta_ym_target=1818 then lambda_eff=target/coeff',
                    'an externally supplied QCD scale remains necessary'],
        'retained':'dimensionless coefficient 12*sqrt(13/40) as an ansatz only'},
      'pass_5961_neutrino':{
        'verdict':'TARGET_FACTOR_REPAIRED_ANSATZ',
        'denominator':nu_D,
        'evidence':['initial stated 24*480*13*273 product equals 40,884,480, not target',
                    'producer notices factor-four miss and replaces 24 by 6 to obtain 10,221,120',
                    'electron mass is then used as the external dimensionful seed'],
        'retained':'integer identity 6*480*13*273=10,221,120'},
      'pass_5962_inflation':{
        'verdict':'OBSERVABLE_MAP_ASSUMED',
        'exact_combinatorics':'45 tritangent planes is retained where independently certified',
        'evidence':['producer defines r=1/N_tritangent rather than deriving r from an inflationary action/potential',
                    'its own single-field consistency calculation gives an n_s tension and then declares n_s requires a separate mechanism'],
        'retained':'45-count only, not r=1/45 as a prediction'},
      'pass_5963_scalar':{
        'verdict':'OBSERVABLE_MAP_ASSUMED',
        'octahedron_spanning_trees':tau,
        'evidence':['tau(K_2,2,2)=384 is exact',
                    'producer then defines mass as measured Higgs mass times 384/15 without a Hamiltonian, pole equation, coupling, or self-energy derivation'],
        'retained':'tau=384 and ratio 384/15 as combinatorial data only'},
      'pass_5964_release_policy':{
        'superseded_ranges':['5913-5932 physical-derivation claims','5933-5956 physical-prediction claims'],
        'claim_tier':'ANSATZ/COMPARISON_ONLY unless a later independent dynamics theorem supplies the observable map',
        'rule':'A producer that inserts n^d to infer d, solves an input scale for a target observable, repairs a factor after seeing the target, or defines an observable as the reciprocal/product of a combinatorial count has not derived a physical prediction.'}
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
    return out

if __name__=='__main__': main()
