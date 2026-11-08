#!/usr/bin/env python3
"""Reconstruct frozen S8 shear power/geometry two-factor experiment exactly.

Shapley two-player attribution is an algebraic decomposition, not calibrated
observational significance. Do not edit or re-freeze prereg_highz.json.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FILE={"des":"shear_hybrid_des.json","kids":"shear_hybrid_kids.json"}
BLOCKS=("all","low","high","mixed")

def produce(root=ROOT):
    d=root/"analysis/toe_uv"
    frozen=json.loads((d/"prereg_highz.json").read_text(encoding="utf8"))
    assert "S8_highz_shear" in frozen
    prereg=frozen["S8_highz_shear"]
    out={}
    for survey,filename in FILE.items():
        raw=json.loads((d/filename).read_text(encoding="utf8"))
        cells=raw["chi2"];observed=raw["split"];published=prereg["current_values"][survey]
        blocks={}
        for block in BLOCKS:
            F,C,P,G=[float(cells[x][block]) for x in ("F","C","C_geoF","F_geoC")]
            total=C-F
            power=P-F
            geometry=G-F
            interaction=C-P-G+F
            shpower=(P-F+C-G)/2
            shgeometry=(G-F+C-P)/2
            assert abs(total-power-geometry-interaction)<1e-11
            assert abs(shpower+shgeometry-total)<1e-11
            assert abs(shpower-(power+interaction/2))<1e-11
            assert abs(shgeometry-(geometry+interaction/2))<1e-11
            assert all(abs(observed[block][k]-v)<1e-11
                       for k,v in (("total",total),("power_part",power),("geometry_part",geometry)))
            assert all(abs(published[block][k]-v)<1e-11
                       for k,v in (("total",total),("power_part",power),("geometry_part",geometry)))
            blocks[block]=dict(
              chi2_fading_F=F,chi2_CPL_C=C,
              chi2_hybrid_CPL_power_fading_geometry=P,
              chi2_hybrid_fading_power_CPL_geometry=G,
              CPL_minus_fading_total=total,
              one_factor_power_at_fading_baseline=power,
              one_factor_geometry_at_fading_baseline=geometry,
              nonadditive_interaction=interaction,
              order_independent_shapley_power=shpower,
              order_independent_shapley_geometry=shgeometry,
              fractional_power_share=(shpower/total if total else None),
              fractional_geometry_share=(shgeometry/total if total else None))
        out[survey]=blocks
    assert abs(out["des"]["all"]["CPL_minus_fading_total"]-2.8844828876623865)<1e-10
    assert abs(out["kids"]["all"]["CPL_minus_fading_total"]-4.503428628031344)<1e-10
    assert out["des"]["all"]["nonadditive_interaction"]<-.9
    assert out["kids"]["all"]["nonadditive_interaction"]<-.5
    assert out["des"]["all"]["fractional_power_share"]>.54
    assert out["kids"]["all"]["fractional_power_share"]>.62
    return dict(
      schema="w33.20261108.S8_hybrid_shapley_audit.v1",
      status="EXACT_FROZEN_HYBRID_ARITHMETIC_INTERACTION_AND_ORDER_INDEPENDENT_SHAPLEY",
      frozen_prereg="analysis/toe_uv/prereg_highz.json",
      frozen_claim=prereg["claim"],
      original_hybrid_implementation="analysis/toe_uv/shear_hybrid.py",
      sources=list(FILE.values()),
      additive_identification_warning="The one-factor power and geometry effects both use the fading baseline. Their sum is NOT generally the observed CPL-fading difference; the nonadditive interaction is nonzero.",
      algebra="Let F=fading power+geometry, C=CPL power+geometry, P=CPL power with fading geometry, G=fading power with CPL geometry. Delta=C-F, interaction=C-P-G+F. Shapley_power=((P-F)+(C-G))/2, Shapley_geometry=((G-F)+(C-P))/2; their sum equals Delta exactly.",
      evidence_limit="These are deterministic recombinations of two already computed fixed-background hybrid likelihoods. No new raw DES/KiDS fit, covariance estimation, independent priors, posterior sampling, causal intervention or calibrated evidence ratio is derived. The frozen S8 claim remains untouched.",
      surveys=out)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=ROOT)
    p.add_argument("--out",type=Path,default=Path("data/w33_20261108_S8_hybrid_shapley_audit.json"))
    a=p.parse_args();x=produce(a.root);a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({s:{"total":v["all"]["CPL_minus_fading_total"],"interaction":v["all"]["nonadditive_interaction"],"shapley_power":v["all"]["order_independent_shapley_power"],"shapley_geometry":v["all"]["order_independent_shapley_geometry"]} for s,v in x["surveys"].items()}))
if __name__=="__main__":main()
